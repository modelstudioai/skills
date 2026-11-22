# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限治理、安全认证机制与高级检索控制三大方向。它不构成独立 API 服务，而是以服务关联角色（SLR）、临时凭证生成和知识库语义过滤等形态，支撑工作流编排、数据接入、可观测性、安全存储及 RAG 等核心场景的合规性与可控性。开发者需按实际使用功能显式启用对应组件，并理解其权限边界与生命周期约束。

## 支持的模型/功能

`more` 本身不提供模型，但为以下关键功能提供底层支持：

- **服务集成与资源访问**：通过预置服务关联角色（SLR），使百炼能安全调用函数计算（FC）、OSS、ADB-PG、MNS、SLS、CMS、OpenTelemetry、内容安全、DTS、CPFS 等阿里云服务。例如，[工作流应用](raw/application-user-guide/agent-development/llm-application/workflow-application.md)依赖 `AliyunServiceRoleForSFMAccessFC` 调用 FC 函数；[安全存储空间](raw/model-user-guide/security-and-compliance/secure-storage.md)依赖 `AliyunServiceRoleForAccessOSS` 和 `AliyunServiceRoleForSFMAccessADB` 访问受控 OSS 存储与 ADB-PG 向量库。
- **临时身份认证**：提供 `/api/v1/tokens` 接口，支持后端服务基于永久 API Key 生成带 TTL 的临时 API Key（`st-***`），用于前端等不可信环境的安全调用。
- **知识库精准检索**：通过 `searchFilters` 参数增强 `Retrieve` 接口能力，支持在语义检索结果上叠加结构化过滤（如字段等值、范围、模糊、多值、标签查询），显著提升 RAG 输出相关性，尤其适用于员工信息表、制度文档等结构化知识库场景。该能力在 [知识库SearchFilters](raw/application-api-reference/more/how-to-use-search-filters.md) 文档中有完整定义。

> **注意**：文档 1 中列出的 `AliyunServiceRoleForSFMTelemetry` 权限策略内容被截断（末尾缺失 JSON 结构），实际策略内容应以控制台或最新版 RAM 策略文档为准；其应用场景仍有效，即支撑 [用量监控与性能分析](raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md) 对 OpenTelemetry 实例的访问。

## 关键参数

| 参数 | 位置 | 类型 | 说明 | 示例 |
|------|------|------|------|------|
| `expire_in_seconds` | Query String | Integer | 临时 API Key 有效期（秒），取值范围 `[1, 1800]`，默认 `60` | `?expire_in_seconds=1800` |
| `searchFilters` | Request Body (JSON) | Array of Objects | 知识库 `Retrieve` 请求中的结构化过滤条件数组，支持子分组（AND）、字段内 OR、嵌套 `_conditions`（RAG API/Spring AI）等语法 | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| `_operator` | Within `searchFilters` item | String | 控制同一子分组内多个字段条件的逻辑关系，可选 `"AND"`（默认）、`"OR"`（大小写不敏感） | `{"_operator": "OR", "doc_name": "A", "title": "B"}` |
| `_conditions` | Within `searchFilters` item (RAG API only) | Array | 支持同一字段多条件（如 `eq` + `like`）及复杂嵌套，仅 RAG API 和 Spring AI SDK 支持 | `[{"department": "Corporate"}, {"department": {"like": "%Research%"}}]` |

## 使用方式

- **服务关联角色（SLR）**：无需手动创建。当您首次在控制台启用对应功能（如添加函数计算节点、配置 OSS 数据源、开启安全存储空间）时，百炼自动为您创建并绑定所需 SLR。角色名称与策略已固化，详见 [服务关联角色](raw/application-api-reference/more/bailian-service-linked-role.md)。
- **生成临时 API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起 `POST` 请求，Header 携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，Query 可选传 `expire_in_seconds`。响应返回 `token`（临时密钥）与 `expires_at`（UNIX 时间戳）。**重要**：该密钥继承源 API Key 的全部权限，包括模型/知识库访问限制。
- **使用 SearchFilters**：
  - 对于 OpenAPI `Retrieve`（`bailian.cn-beijing.aliyuncs.com/{WorkspaceId}/index/retrieve`）：使用平铺 Map 格式，支持 `_operator`，**不支持** `_conditions` 嵌套。
  - 对于 RAG API（`{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/indices/rag/index/retrieve`）或 Spring AI Alibaba SDK：支持完整语法，包括 `_conditions` 数组与混合操作符。务必确认所用 SDK 版本（如 Spring AI Alibaba 1.1.2.3+）及知识库 Schema 字段类型（如 `age` 需为 `double` 才支持 `gte`/`lte`）。

## 限制和注意事项

- **SLR 删除风险高**：删除任一 SLR（如 `AliyunServiceRoleForSFMAccessFC`）将导致其关联功能（工作流[函数调用](../concepts/function-calling.md)）立即失效。删除前必须先解除所有依赖（如删除函数计算节点、断开 OSS/ADB 连接、停止数据导入任务），否则操作失败或引发功能中断。详情见 [服务关联角色](raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key 不可撤销**：生成后无法手动删除或禁用，仅能等待自然过期（最长 1800 秒）。密钥泄露即等同于源 API Key 泄露，务必确保生成服务自身安全。
- **SearchFilters 兼容性差异**：
  - OpenAPI Retrieve **不支持**同一字段的多条件（如 `{"age": {"gte": 25, "lte": 35}}` 或 `{"tag": ["a", "b"]}`），若传入嵌套结构，请求可能成功但过滤无效。
  - RAG API 支持完整语法，但要求知识库索引字段类型与查询操作符严格匹配（如对 `string` 字段使用 `gte` 将静默忽略）。
- **地域隔离**：临时 API Key 的生成 Endpoint 与源 API Key 所属地域强绑定（北京、新加坡、弗吉尼亚、中国香港），跨地域调用将返回 `InvalidApiKey` 错误。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


