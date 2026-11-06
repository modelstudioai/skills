# more

`more` 是百炼平台提供的扩展能力集合，用于支持服务授权、临时凭证分发、知识库高级检索等进阶场景。它不构成独立 API 接口，而是以功能模块形式嵌入在应用管理、知识库查询等主流程中。开发者需结合具体上下文按需启用对应能力。

## 支持的模型/功能

`more` 当前涵盖三类关键扩展功能：  
- **服务关联角色（SLR）**：为百炼应用自动创建最小权限的阿里云服务角色，用于访问 OSS、NAS 等后端资源；  
- **临时 API Key 生成**：允许应用在运行时动态获取具备时效性与作用域限制的临时认证凭据；  
- **知识库 SearchFilters**：在 `knowledge_search` 调用中支持结构化过滤条件（如 `source_id`, `doc_id`, `timestamp_range`），提升召回精度。  
这些能力均非模型推理能力，而是平台级基础设施支撑，详见 [更多](../../raw/application-api-reference/more.md)。

## 关键参数

各功能对应的关键参数如下：  
- SLR 创建无显式参数，由控制台或 OpenAPI `CreateApp` 时通过 `EnableServiceLinkedRole: true` 触发；  
- 临时 [Token](../concepts/token.md) 通过 `ObtainTemporaryAuthenticationToken` 接口调用，需传入 `app_id`、`expires_in`（秒，默认 3600）、`scope`（如 `knowledge:read`）；  
- SearchFilters 以 JSON 对象形式嵌入 `knowledge_search` 请求体的 `filters` 字段，语法严格遵循 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) 定义。  
> **注意**：`scope` 参数值在 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md) 文档中标注为可选，但实测若缺失将返回 `400 Bad Request` —— 请始终显式指定。

## 使用方式

- SLR 功能仅对新创建的应用生效，存量应用需手动调用 `AttachServiceLinkedRole`；  
- 临时 [Token](../concepts/token.md) 必须通过服务端调用（不可前端直连），且需使用主账号或具备 `bailian:ObtainTemporaryAuthenticationToken` 权限的 RAM 子账号密钥签名；  
- SearchFilters 仅在 `knowledge_search` 的 `top_k > 0` 且 `enable_rerank: false` 时完全生效（启用重排可能弱化过滤效果），具体行为参见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制和注意事项

- 单个应用最多持有 10 个未过期的临时 [Token](../concepts/token.md)；超过限额时新请求将自动失效最旧的一个；  
- SearchFilters 不支持全文检索字段（如 `content`）上的模糊匹配，仅支持精确值、范围及存在性判断；  
- SLR 权限策略为只读预设，不可自定义修改，如需写权限请改用自建 RAM 角色；  
- 所有 `more` 功能均依赖百炼应用已成功部署并处于 `ACTIVE` 状态，否则调用将返回 `ResourceNotReady` 错误。  
以上约束细节请同步参考 [更多](../../raw/application-api-reference/more.md) 及其子文档。

## 来源文档

- [更多](../../raw/application-api-reference/more.md)


