# more

`more` 是百炼平台提供的辅助能力集合，用于支持应用层高级功能，如服务权限管理、临时凭证分发和知识库检索过滤等。它不直接参与模型推理，而是为 API 调用提供基础设施级支撑。所有 `more` 相关能力均通过独立的 HTTP 接口暴露，需配合主 API（如 `/v1/chat/completions`）协同使用。

## 支持的模型/功能

`more` 本身**不绑定任何大语言模型**，其下辖功能均为平台级服务：
- 服务关联角色（BailianServiceLinkedRole）：用于授予百炼应用访问云资源（如 OSS、NAS）所需的最小权限 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)  
- 生成临时 API Key：为前端 SDK 或第三方系统颁发短期有效的认证凭证，避免长期密钥泄露风险 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)  
- 知识库 SearchFilters：在 `retrieval` 阶段对向量检索结果施加结构化过滤（如按 `doc_id`、`source`、自定义元字段），提升召回精准度 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `app_id` | string | 是 | 百炼控制台创建的应用唯一标识，所有 `more` 接口均需校验该 ID 的归属权 |
| `expires_in` | integer | 否（默认 3600） | 仅限临时 API Key 接口，单位为秒，取值范围 900–3600；超出将被拒绝 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md) |
| `filter` | object | 否（仅 SearchFilters） | JSON 对象，支持 `eq`、`in`、`gt`、`lt` 等操作符，字段名须与知识库文档元数据定义一致 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) |

> **注意**：`filter` 中若使用嵌套字段（如 `metadata.author.name`），部分旧版 SDK 可能解析失败；建议优先展平元数据结构，详见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) 中的兼容性说明。

## 使用方式

1. 所有 `more` 接口均以 `POST /more/{subpath}` 形式调用，例如：  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/more/temporary-auth-token \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -d '{"app_id": "app-xxx", "expires_in": 1800}'
   ```
2. 请求体必须为 `application/json`，且需携带 `Authorization: Bearer <API_KEY>`（主账号或子账号密钥）  
3. 响应中 `data.token` 即为可直接用于后续 `/v1/chat/completions` 调用的临时凭证（有效期由 `expires_in` 决定）

## 限制和注意事项

- 单个应用每分钟最多调用 `temporary-auth-token` 接口 60 次，超限返回 `429 Too Many Requests`  
- `SearchFilters` 仅在 `retrieval` 模式下生效（即 `input.parameters.retrieval_enabled = true`），在纯 LLM 模式下被忽略  
- 服务关联角色需在应用创建后**手动启用**，未启用时调用依赖云资源的插件（如文件读取）将返回 `403 Forbidden` —— 该行为与 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 文档描述一致，但控制台 UI 中“自动启用”开关实际为灰显状态，属已知 UI 延迟问题。

## 来源文档

- [更多](../../raw/application-api-reference/more.md)


