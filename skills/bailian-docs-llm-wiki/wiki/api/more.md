# more

`more` 是百炼平台提供的扩展能力集合，用于支持服务授权、临时凭证分发、知识库高级检索等关键场景。它不提供独立的模型推理接口，而是作为应用层 API 的补充功能模块，需配合主 API（如 `chat` 或 `embeddings`）协同使用。开发者应根据具体业务需求选择对应子功能，并注意各功能的权限与调用约束。

## 支持的模型/功能

`more` 本身不封装任何大语言模型或嵌入模型，其下辖功能均为平台级基础设施能力：
- **服务关联角色（SLR）**：用于授予百炼服务访问其他阿里云资源（如 OSS、KMS）所需的最小权限，避免手动配置 RAM 策略；详见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **生成临时 API Key**：为前端 SDK 或不可信客户端安全分发短期有效凭证，支持细粒度权限控制和自动过期；详见 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **知识库 SearchFilters**：在 `retrieval` 或 `chat` 请求中通过 `filters` 字段对知识库文档元数据进行布尔组合过滤（如 `source_type == "pdf" AND updated_at > "2024-01-01"`），提升召回精准度；详见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 关键参数

- `temporary_token_ttl_seconds`（仅限临时 Token 接口）：指定 Token 有效期，取值范围 900–3600 秒（15–60 分钟），默认 3600；超出范围将返回 `InvalidParameter.TTLSecondsOutOfRange` 错误。
- `filters`（仅限知识库相关接口）：JSON 对象，遵循 [Elasticsearch Query DSL 子集语法](../../raw/application-api-reference/more/how-to-use-search-filters.md)，不支持全文检索字段（如 `_text`）直接参与过滤。
- `role_name`（仅限 SLR 接口）：固定为 `AliyunServiceRoleForBailian`，不可自定义；调用前需确保主账号已同意创建该角色。

## 使用方式

所有 `more` 功能均通过独立 HTTP 接口调用，路径格式为 `POST /api/v1/more/{subpath}`，例如：
- 创建临时 Token：`POST /api/v1/more/temporary-authentication-token`
- 查询当前 SLR 状态：`GET /api/v1/more/service-linked-role`
- 验证 SearchFilters 语法：`POST /api/v1/more/validate-search-filters`

请求需携带主账号长期 AccessKey（或 STS Token），且调用方 Identity 必须具备 `bailian:CreateTemporaryToken`、`bailian:GetServiceLinkedRole` 等对应 `bailian:*` 权限。> **注意**：[生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md) 文档中示例使用的 `POST /v1/temporary-token` 路径已过时，正确路径为 `/api/v1/more/temporary-authentication-token`，请以 OpenAPI Spec 为准。

## 限制和注意事项

- 每个百炼应用每日最多创建 10,000 个临时 Token；单次请求最多生成 100 个，超出将返回 `Throttling.TooManyTokensPerRequest`。
- SearchFilters 仅在知识库 ID 显式传入且启用向量检索时生效；若请求中未指定 `knowledge_id` 或设置 `enable_retrieval: false`，`filters` 将被静默忽略。
- SLR 仅支持主账号首次调用时自动创建，RAM 用户无法触发创建流程；若文档 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 中提及“子用户可操作”，该描述与当前 v2.3.0 平台行为不符，属过时信息。

## 来源文档

- [更多](../../raw/application-api-reference/more.md)


