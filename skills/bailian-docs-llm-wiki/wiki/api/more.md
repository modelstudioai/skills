# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限管理、安全认证机制与高级检索控制三大方向。它不构成独立服务，而是支撑工作流编排、知识库检索、数据接入、监控分析等核心场景的关键基础设施。开发者需根据具体功能需求，按需启用对应组件并配置相应权限或参数。

## 支持的模型/功能

`more` 本身不提供模型，而是为以下功能提供底层支持：

- **服务关联角色（SLR）**：自动创建并托管云资源访问权限，支撑工作流应用调用函数计算（FC）、知识库对接 ADB-PG、OSS 数据导入、内容安全审核、SLS/CMS 监控上报等场景。例如，[工作流应用](raw/application-user-guide/llm-application/workflow-application.md)依赖 `AliyunServiceRoleForSFMAccessFC` 访问 FC 资源；[创建和使用知识库](raw/application-user-guide/knowledge-base/rag-knowledge-base.md)依赖 `AliyunServiceRoleForSFMAccessADB` 连接 ADB-PG 实例 [服务关联角色 (raw/application-api-reference/more/bailian-service-linked-role.md)](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key**：用于在前端等不可信环境安全调用模型 API，避免永久密钥泄露。其权限继承自生成它的主 API Key，适用于浏览器、移动 App 等客户端直连场景 [生成临时API Key (raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **知识库 SearchFilters**：在 `Retrieve` 接口请求中传入结构化过滤条件，对语义检索结果进行二次精准筛选，显著提升结构化数据（如员工信息表）的召回准确率 [知识库SearchFilters (raw/application-api-reference/more/how-to-use-search-filters.md)](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 1 中 `AliyunServiceRoleForSFMAccessFC` 的权限策略仅包含 `fc:ListFunctions` 和 `fc:InvokeFunction`，但实际工作流节点可能还需 `fc:GetFunction` 或 `fc:CreateFunction`（如动态部署）。请以控制台实时策略或最新 SDK 文档为准，该差异表明策略可能已更新而文档未同步。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例值 |
|------|--------|------|------|------|--------|
| 临时 API Key | `expire_in_seconds` | Integer | 否 | [Token](../concepts/token.md) 有效期（秒），范围 `[1, 1800]`，默认 `60` | `1800` |
| SearchFilters（OpenAPI） | `searchFilters` | Array of Object | 否 | 过滤条件数组，每个元素为平铺 Key-Value Map，子分组间为 AND 关系 | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| SearchFilters（RAG API / Spring AI） | `_operator`, `_conditions` | String, Array | 否 | 指定子分组内条件逻辑（`AND`/`OR`）及嵌套多条件 | `{"_operator": "OR", "_conditions": [{"部门": "Corporate"}, {"部门": {"like": "%Research%"}}]}` |

## 使用方式

- **服务关联角色**：首次启用对应功能（如添加 FC 节点、配置 OSS 数据源）时，系统自动创建 SLR；无需手动调用 API。角色名称与策略由平台预定义，不可修改。删除前必须解除所有依赖该角色的功能绑定（如删除工作流中的 FC 节点、断开安全存储空间的 OSS 连接）。
- **临时 API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起带 `Authorization: Bearer <MASTER_API_KEY>` 的 POST 请求，可选传 `expire_in_seconds`。响应返回 `token`（即临时 Key）与 `expires_at`（Unix 时间戳）。该 [Token](../concepts/token.md) 可直接用于后续模型 API 调用（如 `POST /api/v1/services/aigc/text-generation/generation`）。
- **SearchFilters**：
  - OpenAPI Retrieve：将 `searchFilters` 作为 JSON 数组直接嵌入请求体，**不支持嵌套 `_conditions`**，同一字段多条件需拆分至不同子分组。
  - RAG API / Spring AI SDK：支持完整语法，包括 `_operator` 和 `_conditions` 嵌套，可表达同一字段的 `OR`、`LIKE`、范围查询等复杂逻辑。详见 [知识库SearchFilters (raw/application-api-reference/more/how-to-use-search-filters.md)](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制和注意事项

- **服务关联角色**：
  - 删除 SLR 将导致依赖功能完全失效（如删除 `AliyunServiceRoleForSFMAccessFC` 后，工作流无法调用任何 FC 函数），且无回滚机制。
  - `AliyunServiceRoleForSFMAccessingMNS` 明确禁止手动修改或删除，因其由平台内部强依赖。
- **临时 API Key**：
  - 不可手动撤销或提前失效，仅能等待自然过期。
  - 权限严格继承自签发 Key，若主 Key 拥有全量模型访问权，则临时 Key 亦然；建议为不同场景创建最小权限的专用主 Key。
- **SearchFilters**：
  - OpenAPI SDK 的 `SearchFilters` 字段类型为 `Map<String, String>`，若传入嵌套结构（如 `_conditions`），请求虽可能成功，但**过滤逻辑将被忽略**，返回未过滤结果。
  - 字段名必须与知识库 Schema 中定义的字段名**完全一致（大小写敏感）**，且仅支持已索引字段。
  - 多值查询需将数组序列化为 JSON 字符串（如 `{"姓名": "[\"张三\",\"李四\"]"}`），而非原生数组。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


