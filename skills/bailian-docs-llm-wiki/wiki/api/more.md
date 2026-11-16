# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限管理、安全认证机制与高级知识库检索控制三大方向。它不构成独立服务，而是支撑工作流编排、数据接入、安全存储、可观测性及 RAG 应用等核心场景的关键基础设施。开发者需按需启用对应能力，并严格遵循最小权限原则配置关联资源。

## 支持的模型/功能

`more` 本身不提供模型，而是为以下功能提供底层支持：

- **服务关联角色（SLR）**：自动创建并托管跨云服务访问权限，支撑函数计算节点调用、OSS 数据导入、ADB-PG 向量库接入、MNS 消息监听、OpenTelemetry 监控上报、内容安全审核、SLS/CMS 日志与指标采集等。具体角色列表及对应功能详见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key 生成**：面向不可信前端环境（如浏览器、App）的安全鉴权方案，用于临时授权调用模型或知识库接口。
- **知识库 SearchFilters**：在 `Retrieve` 接口请求中嵌入结构化过滤条件，对语义检索结果进行字段级精准筛选，显著提升 RAG 结果相关性，尤其适用于结构化数据表（如员工信息、产品目录）。

> **注意**：文档 1 中 `AliyunServiceRoleForSFMAccessingMNS` 的说明称其“请勿修改、删除”，但其他 SLR（如 `AliyunServiceRoleForSFMAccessFC`）均明确允许删除并给出前置条件。该表述存在矛盾，实际操作应以各角色章节的**删除服务关联角色**小节为准，而非统一禁止。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|------|--------|------|------|------|-----------|
| 临时 API Key | `expire_in_seconds` | Integer | 否 | 临时 Token 有效期（TTL） | `[1, 1800]` 秒，默认 `60` |
| SearchFilters（OpenAPI） | `searchFilters` | Array of Object | 否 | 过滤条件数组；每个元素为平铺 Key-Value Map，支持 `_operator: "OR"` | 不支持嵌套 `_conditions`；同一字段不可重复出现 |
| SearchFilters（RAG API / Spring AI SDK） | `search_filters` | Array of Object | 否 | 过滤条件数组；支持 `_operator` + `_conditions` 嵌套结构 | 支持 `eq`/`neq`/`gt`/`gte`/`lt`/`lte`/`like` 等操作符，支持同一字段多条件 |

## 使用方式

- **服务关联角色**：首次启用对应功能（如发布含 FC 节点的工作流、配置 OSS 数据源）时，系统自动创建 SLR。无需手动调用 API，但需确保主账号具备 `ram:CreateServiceLinkedRole` 权限。角色策略细节与删除流程请参考 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key**：通过后端服务向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起带 `Authorization: Bearer <永久APIKey>` 的 POST 请求，可选传 `expire_in_seconds`。响应返回 `token`（前缀 `st-`）与 `expires_at`（Unix 时间戳）。[生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md) 提供了完整 cURL 示例与错误处理说明。
- **SearchFilters**：在 `Retrieve` 请求体中添加 `searchFilters`（OpenAPI）或 `search_filters`（RAG API）字段。语法因调用方式而异：
  - OpenAPI SDK：仅支持平铺 Map，例如 `[{"姓名": "张三"}, {"岗位": "技术员"}]`；
  - RAG API 或 Spring AI SDK：支持复杂逻辑，例如 `[{"_operator":"OR","_conditions":[{"部门":"Corporate"},{"部门":{"like":"%Research%"}}]}]`。详细语法与示例见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制和注意事项

- **SLR 删除风险**：删除任一 SLR 将导致其关联功能立即失效（如删除 `AliyunServiceRoleForSFMAccessFC` 后无法调用函数计算节点），且必须先清理依赖资源（如删除工作流中的 FC 节点、断开安全存储空间的 OSS/ADB 连接）。操作前务必阅读对应角色的“删除服务关联角色”章节。
- **临时 API Key 不可撤销**：Token 生命周期固定，到期自动失效，**不支持手动删除或提前吊销**。应严格控制 `expire_in_seconds` 时长，并确保生成服务自身安全。
- **SearchFilters 兼容性差异**：
  - OpenAPI Retrieve 不支持同一字段多条件（如 `{"age": {"gte": 25, "lte": 35}}` 需拆为两个子分组）、不支持嵌套 `_conditions`，误传将导致过滤失效；
  - RAG API 与 Spring AI SDK 支持完整表达能力，但需使用对应 Endpoint（如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/indices/rag/index/retrieve`）。
- **权限继承**：临时 API Key 完全继承生成所用永久 API Key 的权限范围（包括模型白名单、知识库访问控制等），不得用于越权场景。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


