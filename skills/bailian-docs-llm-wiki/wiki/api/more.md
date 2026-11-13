# more

`more` 是百炼平台提供的扩展能力集合，用于支持服务权限管理、临时凭证分发及高级检索控制等关键场景。它不构成独立 API 接口，而是以配套功能模块形式嵌入应用生命周期与知识库交互流程中。开发者需结合具体使用上下文（如应用鉴权、RAG 检索）按需调用相关能力。

## 支持的模型/功能

`more` 当前不关联任何大语言模型，其下功能均为平台级支撑能力：
- 服务关联角色（BailianServiceLinkedRole），用于授予百炼服务访问其他阿里云资源的最小权限；
- 生成临时 API Key，供前端 SDK 或受限环境安全调用后端 API；
- 知识库 `SearchFilters`，支持在 `retrieval` 阶段对向量检索结果施加结构化过滤条件（如 `source_type: "pdf"` 或 `updated_at > "2024-01-01"`）。  
这些能力均在 [更多](../../raw/application-api-reference/more.md) 文档中统一归类说明。

## 关键参数

- `temporary_token_ttl_seconds`：生成临时 Token 时必填，取值范围 900–3600 秒，超时后自动失效；  
- `filter`：`SearchFilters` 的 JSON 字符串格式输入，字段名与知识库文档元数据 schema 严格一致，大小写敏感；  
- `role_name`：服务关联角色创建时指定的唯一标识，必须符合 IAM 角色命名规范。  
详细参数约束请参考 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md) 和 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) 原文。

## 使用方式

1. **服务关联角色**：首次部署需通过 RAM 控制台或 `CreateServiceLinkedRole` API 显式创建，后续调用无需重复操作；  
2. **临时 API Key**：调用 `/v1/applications/{app_id}/temporary-token` 接口，传入 `temporary_token_ttl_seconds` 及可选 `scope`；  
3. **SearchFilters**：在 `POST /v1/knowledge_bases/{kb_id}/retrieve` 请求体中，将 `filter` 字段设为合法 JSON 对象（非字符串），例如 `{"status": "published"}`。  
所有流程均需基于已认证的主账号或具备对应权限的子账号执行，详见 [更多](../../raw/application-api-reference/more.md) 中的权限说明。

## 限制和注意事项

- 单个应用最多同时存在 10 个未过期的临时 Token，超出后旧 Token 不会自动回收，需主动调用 `DELETE /v1/applications/{app_id}/temporary-token/{token_id}` 清理；  
- `SearchFilters` 仅作用于向量检索后的重排序前结果集，不改变原始向量相似度计算逻辑；  
- 服务关联角色一旦创建，删除后可能导致依赖该角色的自动化任务失败，且恢复需重新授权。  
> **注意**：[生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md) 文档中示例使用的 `scope` 参数在 v2.3+ 版本已废弃，实际请求中应忽略该字段，否则将返回 400 错误。  
> **注意**：[知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) 所述的 `filter` 字段类型为 `object`，但部分旧版 SDK 仍将其序列化为字符串，务必校验请求体结构是否符合 OpenAPI 定义。

## 来源文档

- [更多](../../raw/application-api-reference/more.md)


