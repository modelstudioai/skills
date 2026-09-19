# long term memory new

[长期记忆](../concepts/memory.md)（Long Term Memory）是百炼平台提供的结构化记忆管理能力，支持事实记忆的语义化存储与检索，以及基于画像模板的用户属性提取。该能力通过统一 API 接口提供，分为“事实记忆”和“用户画像”两大功能域，所有操作均需通过 DashScope 网关鉴权调用。记忆数据默认永续保存，无自动过期机制。

## 支持的模型/功能

- **事实记忆**：支持 `Add`、`Search`、`List`、`Update`、`Delete` 五类操作，底层使用专用记忆抽取模型（区分 `Pro`/`Lite` 版本），支持对话消息自动解析或自定义内容写入。  
- **用户画像**：支持画像模板（`ProfileSchema`）的全生命周期管理（创建、查询、更新、删除），以及基于模板的用户属性提取与查询。画像提取与事实记忆写入解耦，需显式传入 `profile_schema_id` 才触发提取流程。  
- **策略版本控制**：`AddMemory` 的 `plan_version` 决定记忆抽取质量；`SearchMemory` 的 `plan_version`（或 `enable_rerank`）决定是否启用重排（Rerank），详见[搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)文档。

> **注意**：文档 1 和文档 2 均声明商业化计费时间为 **2026 年 8 月 20 日**，但文档 1 明确标注为“北京时间”，而文档 2 未注明时区。开发者应以文档 1 的时区说明为准，避免计费生效时间误判。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `user_id` | 请求体/Query | string | 是 | 记忆归属实体 ID，最大 64 字符，用于隔离不同用户的数据 |
| `messages` / `custom_content` | 请求体 | array/string | 是（互斥） | 对话消息列表（含 `role`/`content`）或纯文本内容，`custom_content` 优先级更高 |
| `profile_schema_id` | 请求体（Add）或路径参数（Get） | string | 否（Add）/是（Get） | 画像模板 ID；Add 时不传则**不触发画像提取**；Get 时必须传入，见[获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md) |
| `plan_version` | 请求体 | string | 否 | `Pro`（默认，启用 Rerank/高质量抽取）或 `Lite`（关闭 Rerank/基础抽取），大小写不敏感 |
| `top_k` / `min_score` | 请求体 | number | 否 | `SearchMemory` 专属：召回数量上限（1–100，默认 10）和最小相似度阈值（0.0–1.0，默认 0.3） |

## 使用方式

1. **准备凭证**：在[百炼控制台](https://bailian.console.aliyun.com)获取 `DASHSCOPE_API_KEY`，并配置为环境变量（如 `export DASHSCOPE_API_KEY="sk-..."`），详见[鉴权](../../raw/application-api-reference/long-term-memory-new/overview/authentication.md)。  
2. **写入记忆**：调用 `POST /add`，传入 `user_id` 和 `messages`（或 `custom_content`）；若需同步提取画像，**必须**附加 `profile_schema_id`。  
3. **检索记忆**：调用 `POST /memory_nodes/search`，传入 `user_id` 和当前 `messages`，可选 `top_k`、`min_score` 及 `plan_version`。  
4. **管理画像**：先调用 `POST /profile_schemas` 创建模板，再在 `AddMemory` 中引用；之后通过 `GET /profile_schemas/{id}/user_profile?user_id=...` 查询结果。  
5. **调试建议**：所有响应均含 `request_id`，排查问题时务必提供该字段；限流错误（HTTP 429）需按指数退避重试（1s/2s/4s），详见[错误码](../../raw/application-api-reference/long-term-memory-new/overview/errors.md)。

## 限制和注意事项

- **限流**：阿里云账号级总限流 3000 QPM；其中 `Add` 接口限 120 QPM，`Search` 接口限 300 QPM。扩容需[提交工单](https://smartservice.console.aliyun.com/service/create-ticket)。  
- **数据持久性**：生成的记忆片段与用户画像**暂无失效日期**，但删除操作（`DELETE /memory_nodes/{id}` 或 `DELETE /profile_schemas/{id}`）**不可逆**，且后者会连带清除已提取的画像数据。  
- **画像提取延迟**：调用 `AddMemory` 后，画像提取存在约 3 秒异步延迟，立即调用 `GetUserProfile` 可能返回空值，需等待后重试。  
- **互斥逻辑**：`messages` 与 `custom_content` 在 `AddMemory` 中互斥；`plan_version` 与 `enable_rerank` 在 `SearchMemory` 中互斥（前者优先级更高）。  
- **安全要求**：API Key 必须通过 `Authorization: Bearer $DASHSCOPE_API_KEY` 传递，严禁硬编码或提交至代码仓库，详见[鉴权](../../raw/application-api-reference/long-term-memory-new/overview/authentication.md)的安全建议。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [API 概览](../../raw/application-api-reference/long-term-memory-new/overview.md)
- [鉴权](../../raw/application-api-reference/long-term-memory-new/overview/authentication.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/overview/errors.md)
- [事实记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [删除画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/delete-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)


