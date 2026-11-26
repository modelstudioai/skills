# more

`more` 是百炼平台为高级用例提供的扩展能力集合，涵盖服务权限治理、安全凭证分发、知识库精准检索等关键能力。它不构成独立 API 服务，而是分散在工作流、知识库、模型调用等核心场景中的增强机制。开发者需根据具体功能目标选择对应子能力，并严格遵循其权限模型与参数约束。

## 支持的模型/功能

`more` 不对应单一模型，而是支撑以下三类关键功能：

- **服务关联角色（SLR）**：为百炼各子系统（如工作流、数据管理、安全存储空间、模型监控等）访问外部云资源（FC、OSS、ADB-PG、MNS、SLS 等）提供最小权限委托。例如 `AliyunServiceRoleForSFMAccessFC` 用于函数计算节点调用，`AliyunServiceRoleForAccessOSS` 用于安全存储空间读写 OSS [服务关联角色 (raw/application-api-reference/more/bailian-service-linked-role.md)](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key 生成**：面向不可信前端环境（如浏览器、App），通过后端调用 `/api/v1/tokens` 接口签发短期有效凭证，继承源 API Key 的全部权限边界 [生成临时API Key (raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **知识库 SearchFilters**：在 `Retrieve` 接口请求中传入结构化过滤条件，对语义检索结果进行字段级后置过滤（如 `{"姓名": "张三"}`），显著提升结构化数据召回精度 [知识库SearchFilters (raw/application-api-reference/more/how-to-use-search-filters.md)](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 1 中 `AliyunServiceRoleForSFMAccessADB` 的应用场景描述为“安全存储空间”使用，但其权限策略（`gpdb:CreateVectorManagerAccount` 等）明确指向向量数据库操作，实际也服务于知识库 RAG 场景；而文档 3 的 SearchFilters 示例和前置步骤均基于知识库 `Retrieve` 接口，二者存在功能耦合。开发者应以实际接口行为为准，而非仅依赖文档归类。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例值 |
|------|--------|------|------|------|--------|
| 临时 API Key | `expire_in_seconds` | Integer | 否 | [Token](../concepts/token.md) 有效期（秒），范围 `[1, 1800]`，默认 `60` | `1800` |
| SearchFilters（OpenAPI） | `searchFilters` | Array of Object | 否 | 过滤条件数组，每个元素为平铺 Key-Value Map；子分组内默认 `AND`，支持 `_operator: "OR"` | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| SearchFilters（RAG API / Spring AI） | `search_filters` | Array of Object | 否 | 支持嵌套 `_conditions` 和 `_operator`，可表达同一字段多条件 OR（如 `{"department": {"like": "%Research%"}}`） | `[{"_operator":"OR","_conditions":[{"department":"Corporate"},{"department":{"like":"%Research%"}}]}]` |

## 使用方式

- **服务关联角色**：首次启用对应功能（如添加函数计算节点、配置 OSS 数据源）时，系统自动创建 SLR；无需手动调用 API。角色策略已固化，不可修改。查看与管理请前往 [RAM 控制台](https://ram.console.aliyun.com/) > 角色管理。
- **临时 API Key**：后端服务使用永久 API Key（`DASHSCOPE_API_KEY`）向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起 POST 请求，携带 `expire_in_seconds` 查询参数。响应返回 `token` 字符串与 `expires_at` 时间戳。
- **SearchFilters**：
  - OpenAPI Retrieve：将 `searchFilters` 字段作为 JSON 数组直接嵌入请求体，**不支持嵌套 `_conditions`**；
  - RAG API 或 Spring AI SDK：使用 `search_filters` 字段，支持 `_operator` 和 `_conditions` 嵌套结构，实现复杂逻辑组合。

## 限制和注意事项

- **SLR 删除风险**：删除任一服务关联角色（如 `AliyunServiceRoleForSFMAccessFC`）将导致依赖该角色的功能**立即失效**（如工作流无法调用 FC 函数），且删除前必须先清理所有关联资源（如删除函数计算节点、断开 OSS/ADB 连接）[服务关联角色 (raw/application-api-reference/more/bailian-service-linked-role.md)](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key 不可撤销**：[Token](../concepts/token.md) 生命周期固定，到期自动失效，**不支持手动删除或提前吊销**；应严格控制 `expire_in_seconds` 时长，避免过度授权 [生成临时API Key (raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **SearchFilters 兼容性陷阱**：OpenAPI SDK 的 `searchFilters` 仅接受平铺 Map，若误传嵌套结构（如 `_conditions`），请求可能成功但**过滤逻辑不生效**；RAG API 路径（`/api/v1/indices/rag/index/retrieve`）才支持完整嵌套语法 [知识库SearchFilters (raw/application-api-reference/more/how-to-use-search-filters.md)](../../raw/application-api-reference/more/how-to-use-search-filters.md)。
- **权限继承严格**：临时 API Key 完全继承源 API Key 的权限集（含模型白名单、知识库访问限制等），后端生成时需确保源密钥权限最小化。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


