# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限治理、安全鉴权机制与高级知识库检索控制等关键功能。它不构成独立服务，而是支撑工作流编排、数据接入、模型监控、RAG 精准检索等核心场景的底层能力模块。开发者需结合具体使用场景（如启用函数计算节点、调用 Retrieve 接口或配置可观测性）按需启用和配置相关组件。

## 支持的模型/功能

`more` 本身不提供模型，而是为以下功能提供基础设施支持：

- **服务关联角色（SLR）**：自动创建并管理百炼访问其他云服务所需的最小权限角色，覆盖函数计算（FC）、OSS、ADB-PG、MNS、OpenTelemetry、内容安全、SLS、CMS、DTS、CPFS 等十余类云资源。例如，[工作流应用](raw/application-user-guide/agent-development/llm-application/workflow-application.md)依赖 `AliyunServiceRoleForSFMAccessFC` 调用 FC 函数；[安全存储空间](raw/model-user-guide/security-and-compliance/secure-storage.md)依赖 `AliyunServiceRoleForSFMAccessADB` 连接 ADB-PG 向量库；[用量监控与性能分析](raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)依赖 `AliyunServiceRoleForSFMTelemetry` 上报 OpenTelemetry 数据。  
- **临时 API Key 生成**：提供 `/api/v1/tokens` 接口，用于在不可信前端环境（如浏览器、App）中安全派生短期凭证，避免永久密钥泄露。  
- **知识库 SearchFilters**：支持在 `Retrieve` 接口请求中传入结构化过滤条件，对语义检索结果进行字段级、逻辑级（AND/OR）、操作级（eq/like/gte 等）二次筛选，显著提升 RAG 结果相关性，尤其适用于结构化数据表（如员工信息表）场景。该能力详见 [知识库SearchFilters](raw/application-api-reference/more/how-to-use-search-filters.md) 文档。

> **注意**：文档 1 中 `AliyunServiceRoleForSFMTelemetry` 的策略定义在末尾被截断（JSON 不完整），实际权限应以控制台或最新版 RAM 策略为准；其应用场景描述与 [用量监控与性能分析](raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md) 一致，但策略内容需参考完整版本。

## 关键参数

| 功能 | 参数名 | 类型 | 说明 | 约束 |
|------|--------|------|------|------|
| 临时 API Key | `expire_in_seconds` | Integer | 指定临时 [Token](../concepts/token.md) 有效期（秒） | 必须在 `[1, 1800]` 范围内；默认 `60` |
| SearchFilters（OpenAPI） | `searchFilters` | Array of Object | 检索过滤条件数组，每个元素为平铺 Key-Value Map | 子分组内字段默认 `AND`；支持 `_operator: "OR"`；不支持嵌套 `_conditions` |
| SearchFilters（RAG API / Spring AI SDK） | `searchFilters` | Array of Object | 同上，但支持 `_conditions` 数组与更丰富操作符 | 支持 `eq`, `neq`, `gt`, `gte`, `lt`, `lte`, `like` 及多值、标签查询 |

## 使用方式

- **服务关联角色**：首次在控制台启用对应功能（如添加函数计算节点、配置 OSS 数据源、开启安全存储空间 ADB 连接）时，系统自动创建 SLR；无需手动调用 API。角色名称与权限策略已固化，不可修改。  
- **生成临时 API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起带 `Authorization: Bearer <PERMANENT_API_KEY>` 的 POST 请求，并可选传 `?expire_in_seconds=1800`。响应返回 `token`（字符串）与 `expires_at`（Unix 时间戳）。示例见 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。  
- **使用 SearchFilters**：在 `Retrieve` 请求体中添加 `searchFilters` 字段。语法取决于调用方式：  
  - OpenAPI（`bailian.cn-beijing.aliyuncs.com/{WorkspaceId}/index/retrieve`）：仅支持平铺 Map，如 `[{"姓名": "张三"}, {"岗位": "技术员"}]`；  
  - RAG API 或 Spring AI SDK（`{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/indices/rag/index/retrieve`）：支持 `_conditions` 与复杂操作，如 `[{"_operator": "OR", "_conditions": [{"部门": "Corporate"}, {"部门": {"like": "%Research%"}}]}]`。详细语法见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制和注意事项

- **SLR 删除风险高**：删除任一服务关联角色将导致其关联功能完全失效（如删除 `AliyunServiceRoleForSFMAccessFC` 后，所有工作流中的函数计算节点无法调用）。删除前必须先解除所有依赖（如删除函数节点、断开 OSS/ADB 连接、停止数据导入任务），否则操作失败。  
- **临时 API Key 不可撤销**：[Token](../concepts/token.md) 生命周期固定，到期自动失效，**不支持手动删除或禁用**。务必严格控制 `expire_in_seconds` 时长，避免过度宽松（如设为 1800 秒仅限必要场景）。  
- **SearchFilters 兼容性差异**：OpenAPI SDK 的 `search_filters` 字段**不支持嵌套结构**（如 `_conditions`）。若错误传入，请求可能成功但过滤逻辑不生效，返回未预期结果。务必根据所用接口类型（OpenAPI vs RAG API）选择对应语法。此差异已在 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) 中明确区分。  
- **权限继承与最小化原则**：临时 API Key 继承父密钥的全部权限（含模型、知识库访问限制），因此生产环境应为不同用途创建专用永久密钥，再派生临时 [Token](../concepts/token.md)，避免权限过大。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


