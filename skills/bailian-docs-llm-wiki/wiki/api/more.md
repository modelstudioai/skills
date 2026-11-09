# more

`more` 是百炼平台提供的扩展能力集合，用于支持服务权限管理、临时凭证分发、知识库高级检索等进阶场景。它不构成独立 API 接口，而是以配套功能模块形式补充核心应用能力。开发者需结合具体使用场景按需调用对应子功能。

## 支持的模型/功能

`more` 当前包含以下三类关键扩展功能：
- **服务关联角色（SLR）**：用于授予百炼服务访问其他阿里云资源（如 OSS、VPC）所需的最小权限，避免手动创建自定义角色；详情见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **生成临时 API Key**：为前端 SDK 或第三方系统提供短期、可撤回的身份凭证，适用于无服务端代理的轻量集成；参考 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **知识库 SearchFilters**：在 `knowledge_search` 调用中支持字段级过滤（如 `source_id`, `doc_type`, `update_time`），提升检索精准度；用法说明见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 关键参数

各子功能参数独立定义，无全局共享参数：
- SLR 创建无需传参，通过 RAM 控制台或 `CreateServiceLinkedRole` API 触发；
- 临时 API Key 接口要求必填 `application_id` 和 `expires_in_seconds`（最大 3600），返回 `access_token` 与 `expires_at`；
- SearchFilters 以 JSON 对象形式嵌入 `knowledge_search` 请求体的 `filters` 字段，仅支持 `eq`, `in`, `gt`, `lt` 四种操作符，详见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 使用方式

- SLR 需在首次调用依赖资源的 API 前完成绑定（如启用知识库自动同步 OSS 文件时）；
- 临时 API Key 必须通过服务端调用 `/v1/applications/{app_id}/temporary-tokens` 获取，禁止前端直连；
- SearchFilters 仅在 `knowledge_search` 的 `POST /v1/knowledge_search` 请求中生效，不适用于 `chat` 或 `completion` 接口。

## 限制和注意事项

- 单个应用最多同时存在 100 个有效临时 [Token](../concepts/token.md)；超期后自动失效，不可刷新；
- SearchFilters 不支持全文检索字段（如 `content`）上的过滤，仅作用于元数据字段；
- > **注意**：[生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md) 文档中示例的 `scope` 参数在 v2.3+ 版本已废弃，实际请求中应忽略该字段，否则将返回 400 错误；
- > **注意**：[服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 描述的默认策略权限范围较宽，生产环境建议基于最小权限原则，通过自定义策略进一步收紧（如限定特定 OSS Bucket）。

## 来源文档

- [更多](../../raw/application-api-reference/more.md)


