# more

`more` 是百炼平台提供的扩展能力集合，用于支持服务权限管理、临时凭证分发、知识库高级检索等进阶场景。它不提供独立的 API 接口，而是作为应用层能力补充，需配合主 API（如 `/v1/chat/completions` 或 `/v1/knowledge_bases/{kb_id}/search`）协同使用。所有功能均需通过应用（Application）上下文调用，且依赖对应权限配置。

## 支持的模型/功能

`more` 本身不绑定特定大模型，其功能与底层模型无关，但部分能力需在特定服务模式下生效：
- **服务关联角色（SLR）**：为百炼应用自动创建并绑定 `AliyunBailianDefaultRole`，用于访问 OSS、NAS 等云资源；该角色由平台统一维护，不可手动修改 [更多](../../raw/application-api-reference/more.md)。
- **生成临时 API Key**：为前端 SDK 或受限客户端颁发短期有效的 `temporary_token`，有效期最长 24 小时，适用于无服务端代理的直连场景 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **知识库 SearchFilters**：在 `/v1/knowledge_bases/{kb_id}/search` 请求中通过 `filters` 字段实现字段级过滤（如 `source_type: "pdf"`、`doc_id: ["abc", "def"]`），支持 AND 逻辑与嵌套结构 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `application_id` | Header / Query | string | 是 | 应用唯一标识，用于鉴权和 SLR 绑定上下文 |
| `temporary_token` | Header (`x-bailian-temporary-token`) | string | 仅临时凭证场景 | 由 `/more/temporary_token` 接口返回，替代 `Authorization: Bearer <api_key>` |
| `filters` | Request Body (knowledge search) | object | 否 | JSON 对象，遵循 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) 定义的语法，不支持全文检索字段（如 `content`）直接过滤 |

> **注意**：文档 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md) 中提及的 `expires_in` 单位为“秒”，但实际响应中该字段值为整数毫秒（如 `3600000` 表示 1 小时），请以实际接口返回为准，避免按秒解析导致过期判断错误。

## 使用方式

1. **SLR 配置**：在控制台创建应用时勾选「启用服务关联角色」，或调用 `POST /v1/applications/{app_id}/enable-slr`；角色策略自动更新，无需手动同步 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
2. **获取临时 Token**：向 `POST /more/temporary_token` 发送请求（需携带 `Authorization: Bearer <master_api_key>`），响应体含 `temporary_token` 和 `expires_at`（ISO8601 时间戳）。
3. **使用 SearchFilters**：在知识库搜索请求的 body 中添加 `filters` 字段，例如：<br>`{ "filters": { "source_type": "pdf", "tags": ["report", "2024"] } }`；注意字段名必须与知识库文档元数据定义完全一致。

## 限制和注意事项

- 每个应用最多同时存在 100 个有效 `temporary_token`；超出后旧 token 不会自动失效，需主动调用 `/more/temporary_token/revoke` 撤销。
- `filters` 仅支持精确匹配与 `IN` 列表，**不支持**模糊匹配（`like`）、范围查询（`gt`/`lt`）或布尔运算符（`AND`/`OR` 字符串）；复杂逻辑需在客户端聚合结果。
- SLR 权限最小化原则：默认策略仅授予知识库所需 OSS `GetObject` 权限；若应用需写入 NAS，须在控制台手动附加自定义策略 —— 此行为与 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 文档描述一致，但当前控制台 UI 中“附加策略”入口暂未开放，建议暂通过 RAM 控制台操作。

## 来源文档

- [更多](../../raw/application-api-reference/more.md)


