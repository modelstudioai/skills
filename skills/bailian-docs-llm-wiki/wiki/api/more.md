# more

`more` 是百炼平台提供的扩展能力集合，用于支持应用层高级功能，如服务权限管理、临时凭证分发和知识库精细化检索。它不构成独立 API 接口，而是以配套能力形式嵌入在应用生命周期与知识库调用流程中。开发者需结合具体场景按需启用，所有能力均依赖主服务（如 `chat` 或 `search`）的上下文生效。

## 支持的模型/功能

`more` 本身不绑定特定大模型，其功能面向整个应用架构层：
- **服务关联角色（SLR）**：为百炼应用自动创建最小权限 IAM 角色，用于访问 OSS、NAS 等云资源；该机制是 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 文档的核心内容。
- **临时 API Key 生成**：支持为终端用户或第三方系统颁发短期有效的 `temporary_token`，适用于多租户或前端直连场景；详细实现见 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **知识库 SearchFilters**：在 `retrieval` 请求中通过 `filters` 字段对向量检索结果施加元数据条件过滤（如 `doc_type: "pdf" AND updated_at > "2024-01-01"`），能力说明参见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `expires_in` | integer | 否 | 临时 token 有效期（秒），默认 3600，最大 86400；仅在调用 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md) 时生效 |
| `filters` | object | 否 | JSON 对象，字段名需与知识库 schema 中定义的元数据字段一致；使用方式详见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) |
| `role_name` | string | 否 | 自定义 SLR 名称前缀，若未指定则由平台自动生成；参考 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) |

> **注意**：`filters` 不支持嵌套布尔逻辑（如 `(A AND B) OR C`），仅支持扁平化 `AND` 组合；复杂查询需在应用层做二次过滤，此限制在 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) 中未明确说明，但实测 v2.3.0+ 版本 API 返回 `400` 错误。

## 使用方式

- **服务关联角色**：首次部署含 OSS/NAS 集成的应用时，平台自动创建 SLR；如需手动触发，调用 `POST /v1/applications/{app_id}/service-linked-role`（需 `Admin` 权限）。
- **临时 [Token](../concepts/token.md)**：向 `/v1/applications/{app_id}/temporary-token` 发起 POST 请求，携带 `scope`（如 `"retrieval"`）和可选 `expires_in`；响应体含 `token` 和 `expires_at`。
- **SearchFilters**：在知识库 `retrieval` 请求的 `body` 中添加 `"filters": { "tag": "public", "source": "manual" }`，字段值区分大小写。

## 限制和注意事项

- 单个应用最多绑定 1 个服务关联角色，重复创建请求将返回 `409 Conflict`。
- 临时 token 不可撤销，仅能等待过期；高频调用建议复用同一 token（需控制 `expires_in` 时长）。
- `filters` 中的字段必须已在知识库 schema 中声明为 `filterable: true`，否则查询时静默忽略该条件——该行为与 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 中描述的“严格校验”原则存在隐式冲突，建议以实际 API 响应为准。

## 来源文档

- [更多](../../raw/application-api-reference/more.md)


