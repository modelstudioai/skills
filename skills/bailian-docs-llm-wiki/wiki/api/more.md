# more

`more` 是百炼平台提供的扩展能力集合，用于支持服务权限管理、临时凭证分发及高级检索控制等关键场景。它不构成独立 API 接口，而是以配套功能模块形式嵌入应用生命周期与知识库交互流程中。开发者需结合具体上下文按需启用对应子能力。

## 支持的模型/功能

`more` 当前涵盖三类核心扩展功能：
- **服务关联角色（SLR）**：为百炼应用自动创建最小权限 IAM 角色，用于访问 OSS、NAS 等云资源，避免手动配置权限风险；详情见 [更多](../../raw/application-api-reference/more.md)。
- **生成临时 API Key**：支持通过 `application_obtain_temporary_authentication_token` 接口签发具备时效性与作用域限制的临时认证凭证，适用于前端直连或第三方集成场景；该机制在 [更多](../../raw/application-api-reference/more.md) 中统一归类说明。
- **知识库 SearchFilters**：允许在 `retrieve` 或 `chat` 请求中通过 `filters` 字段对向量检索结果施加元数据条件过滤（如 `source_type == "pdf"`），提升召回精度；用法详见 [更多](../../raw/application-api-reference/more.md)。

## 关键参数

- `duration_seconds`（临时 Token）：有效时长，取值范围 900–3600 秒，默认 3600；超出此范围将被拒绝。
- `filters`（SearchFilters）：JSON 对象，支持 `==`、`!=`、`in`、`not_in` 四种操作符，字段名须预注册于知识库 schema；不支持嵌套路径或全文检索表达式。
- `role_name_prefix`（SLR）：可选，指定自动生成 SLR 的命名前缀；若未提供，平台使用默认前缀 `AliyunServiceRoleForBailian`。

## 使用方式

- 服务关联角色：在控制台「应用设置 → 权限管理」中勾选「启用服务关联角色」，或调用 `CreateApplication` 时设置 `enable_service_linked_role: true`。
- 临时 API Key：向 `POST /applications/{app_id}/temporary-authentication-token` 发起请求，需携带 `App-Bearer` 主密钥认证头。
- SearchFilters：在知识库检索请求的 `retrieval_config.filters` 或聊天请求的 `input.parameters.retrieval_config.filters` 中传入过滤对象。

## 限制和注意事项

- 单个应用最多绑定 1 个服务关联角色；重复启用将复用已有角色而非新建。
- 临时 API Key 不支持刷新，过期后必须重新申请；且不可用于调用 `more` 下属文档中的管理类接口（如 SLR 创建）。
- > **注意**：[生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md) 文档中示例使用的 `POST /v1/applications/{app_id}/temp_token` 路径已废弃，当前仅支持 `/applications/{app_id}/temporary-authentication-token`（以 `temporary-authentication-token` 为准），请以 [更多](../../raw/application-api-reference/more.md) 中的导航链接指向的最新版本为准。

## 来源文档

- [更多](../../raw/application-api-reference/more.md)


