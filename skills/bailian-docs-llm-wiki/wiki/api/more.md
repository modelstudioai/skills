# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限管理、知识库高级检索控制、临时认证机制等关键功能模块。这些能力不直接暴露在基础模型调用链路中，但对构建安全、可控、可观察的企业级 AI 应用至关重要。开发者需根据具体场景（如工作流集成、结构化知识过滤、前端直连调用）按需启用和配置。

## 支持的模型/功能

`more` 本身不是模型，而是支撑多种核心功能的底层能力集，包括：
- **服务关联角色（SLR）**：为百炼子系统（如工作流、数据管理、安全存储空间）自动申请并托管对其他云服务（FC、OSS、ADB-PG、MNS、SLS 等）的最小必要访问权限。例如，[工作流应用](raw/application-user-guide/llm-application/workflow-application.md)依赖 `AliyunServiceRoleForSFMAccessFC` 调用函数计算资源；[安全存储空间](raw/model-user-guide/security-and-compliance/secure-storage.md)依赖 `AliyunServiceRoleForSFMAccessADB` 访问 ADB-PG 向量库。
- **知识库高级检索（SearchFilters）**：提供结构化过滤能力，支持在 `Retrieve` 接口调用时对语义检索结果进行字段级精确/范围/模糊/多值过滤，显著提升 RAG 结果相关性。
- **临时 API Key 生成**：通过后端服务调用 `/api/v1/tokens` 接口，为不可信客户端（如浏览器、App）签发短期有效的凭证，避免永久密钥泄露风险。

> **注意**：文档 1 中列出的 `AliyunServiceRoleForSFMTelemetry` 权限策略内容被截断（末尾为 `"log:Get*"`），其完整权限范围需以 [服务关联角色 (raw/application-api-reference/more/bailian-service-linked-role.md)](../../raw/application-api-reference/more/bailian-service-linked-role.md) 的最新发布版本为准，当前摘要无法确认是否包含 `log:ListLogStores` 等必需操作。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例 |
|------|--------|------|------|------|------|
| **临时 API Key** | `expire_in_seconds` | integer | 否 | 有效期（秒），取值范围 `[1, 1800]`，默认 `60` | `1800` |
| **SearchFilters（OpenAPI）** | `searchFilters` | array of object | 否 | 过滤条件数组，每个对象为平铺 key-value 对，子分组间为 AND 关系；同一分组内默认 AND，可设 `_operator: "OR"` | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| **SearchFilters（RAG API / Spring AI）** | `search_filters` | array of object | 否 | 支持嵌套 `_conditions` 和 `_operator`，允许同一字段多条件（如 `eq` + `like`）组合 | `[{"_operator":"OR","_conditions":[{"department":"Corporate"},{"department":{"like":"%Research%"}}]}]` |

## 使用方式

- **服务关联角色**：无需手动创建。当您首次在控制台启用对应功能（如添加函数计算节点、配置 OSS 数据源、开启安全存储空间）时，百炼自动为您创建所需 SLR。角色名称与权限策略已固化，详见 [服务关联角色 (raw/application-api-reference/more/bailian-service-linked-role.md)](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **SearchFilters**：在调用知识库 `Retrieve` 接口时，将过滤条件作为 `searchFilters`（OpenAPI）或 `search_filters`（RAG API）字段传入请求体。**务必确保知识库索引已正确配置对应字段（如 `姓名`、`年龄`）为可检索属性**。不同调用方式语法差异较大，详见 [知识库SearchFilters (raw/application-api-reference/more/how-to-use-search-filters.md)](../../raw/application-api-reference/more/how-to-use-search-filters.md)。
- **临时 API Key**：后端服务使用永久 `DASHSCOPE_API_KEY` 向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起带 `Authorization: Bearer <permanent_key>` 的 POST 请求，并可选附加 `?expire_in_seconds=N`。响应中的 `token` 字段即为可用临时密钥，需透传给前端用于后续模型或知识库调用。

## 限制和注意事项

- **服务关联角色删除风险高**：删除任一 SLR（如 `AliyunServiceRoleForSFMAccessFC`）将导致依赖该角色的功能（如工作流中的函数节点）**立即失效**。删除前必须先解除所有业务绑定（如删除函数节点、断开 OSS/ADB 连接、停止数据导入任务），否则操作会被拒绝。详情见 [服务关联角色 (raw/application-api-reference/more/bailian-service-linked-role.md)](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **SearchFilters 兼容性限制**：OpenAPI SDK 的 `searchFilters` 仅接受平铺 Map，**不支持嵌套 `_conditions` 或同一字段多个独立条件**（如 `{"age": {"gte": 25, "lte": 35}}` 在 OpenAPI 中需拆分为两个分组）。若需复杂逻辑，必须切换至 RAG API 或 Spring AI Alibaba SDK。
- **临时 API Key 权限继承与不可撤销**：临时密钥完全继承签发者（永久 API Key）的全部权限，包括模型白名单、知识库访问策略等。且**无法手动提前吊销**，只能等待自然过期（最长 30 分钟）。因此，签发永久密钥时应遵循最小权限原则。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)


