# more

`more` 是百炼平台提供的扩展能力集合，用于支持应用层高级功能，如服务权限管理、临时凭证分发和知识库精细化检索。这些能力不直接参与模型推理，但对构建安全、可控、可扩展的 AI 应用至关重要。开发者需结合具体场景按需调用，所有接口均通过 HTTPS RESTful 方式访问。

## 支持的模型/功能

`more` 本身不提供模型服务，而是提供三类关键支撑功能：  
- **服务关联角色（SLR）管理**：用于授予百炼服务访问其他阿里云资源（如 OSS、NAS）所需的最小权限，避免手动配置 RAM 角色；  
- **临时 API Key 生成**：为前端 SDK 或第三方客户端颁发短期有效的认证凭证，实现无密访问；  
- **知识库 SearchFilters 配置**：在 `Retrieve` 阶段对向量检索结果施加元数据过滤条件（如 `doc_type: "faq" AND updated_at > "2024-01-01"`），提升召回精准度。  
详见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)、[生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md) 和 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 关键参数

- `DurationSeconds`（临时 Token）：有效时长，范围 900–3600 秒，默认 3600，不可超过主账号允许的最大会话时间；  
- `Filter`（SearchFilters）：JSON 格式字符串，字段名须与知识库文档元数据 schema 完全一致，不支持嵌套字段或模糊匹配（如 `*`）；  
- `RoleSessionName`（SLR）：会话标识符，需全局唯一且符合 `[a-zA-Z0-9+=,.@_-]` 正则，长度 2–64 字符；  
- 所有请求必须携带 `X-Bailian-Date` 和 `Authorization` 签名头，签名算法与百炼主 API 一致。

## 使用方式

1. **SLR 绑定**：首次使用前，调用 `CreateServiceLinkedRole` 接口（或通过控制台启用），百炼将自动创建 `AliyunServiceRoleForBailian` 角色；  
2. **获取临时 Token**：向 `/v1/applications/{app_id}/temporary-token` 发送 POST 请求，需提供 `app_id` 和 `DurationSeconds`；  
3. **应用 SearchFilters**：在知识库 `retrieve` 请求体中，于 `retrieval_config.filters` 字段传入序列化 JSON 字符串（非对象）。  
> **注意**：`application-obtain-temporary-authentication-token.md` 中示例请求体误将 `DurationSeconds` 写为字符串类型，实际应为整型——请以 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md) 的最新 OpenAPI Schema 为准。

## 限制和注意事项

- 单个应用每分钟最多调用 100 次临时 Token 接口，超出将返回 `429 Too Many Requests`；  
- SearchFilters 仅在 `retrieval_strategy: "vector"` 且知识库已启用元数据索引时生效，纯关键词检索（`keyword`）不支持该参数；  
- SLR 权限变更后，已有会话不会自动刷新，需重新调用 `AssumeRole` 获取新凭证；  
- 所有 `more` 功能均依赖应用已通过 `POST /v1/applications` 创建并处于 `active` 状态，未激活应用调用将返回 `404 Not Found`。  
> **注意**：`how-to-use-search-filters.md` 中提及“支持布尔运算符 `OR`”，但当前版本（v202405）仅支持 `AND` 连接多个条件，`OR` 将被静默忽略——该差异已在 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) 的勘误注释中说明。

## 来源文档

- [更多](../../raw/application-api-reference/more.md)


