# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory）是百炼平台提供的结构化记忆管理能力，支持将对话自动提取为事实记忆（如待办事项、用户偏好）和用户画像（如年龄、职业、兴趣），并提供语义检索、更新与生命周期管理。所有操作通过统一的 REST API 完成，适用于构建具备上下文感知与个性化能力的智能体应用。

## 支持的模型/功能

[长期记忆](../concepts/long-term-memory.md)包含两大核心功能模块：**事实记忆**（Memory Nodes）与**用户画像**（User Profile）。

- **事实记忆**：基于对话消息或自定义内容，自动抽取结构化记忆片段（如“用户每天上午9点需要喝水提醒”）。支持添加、搜索、列表、更新、删除全生命周期操作，详见 [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md) 和 [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)。
- **用户画像**：需先创建画像模板（定义字段如“年龄”“爱好”），再在 `AddMemory` 调用中传入 `profile_schema` ID 触发提取；提取完成后通过 `GetUserProfile` 查询结果。模板支持 `Pro`/`Lite` 两种策略版本，影响提取精度与延迟，详见 [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)。

> **注意**：文档 1 和文档 2 均指出记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）正式商业化计费**，且 `Add` 和 `Search` 接口均区分 `Pro` 与 `Lite` 版本。但文档 14（获取画像模板）响应示例中 `plan_version` 字段值为 `"pro"`（小写），而文档 15（更新画像模板）明确要求传入 `"Pro"` 或 `"Lite"`（首字母大写）。实际调用时请以文档 15 的大小写约定为准，避免因大小写不匹配导致参数被忽略。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `user_id` | 请求体/查询参数 | string | 是 | 记忆归属实体唯一标识，最大 64 字符，所有接口均需指定 |
| `messages` / `custom_content` | 请求体 | array / string | 是\* | 互斥：`messages` 用于对话提取（最多 50 条），`custom_content` 用于直接写入文本（最大 512 字符） |
| `profile_schema` | 请求体 | string | 否 | 画像模板 ID；**不传则完全跳过用户画像提取流程**，仅写入事实记忆 |
| `plan_version` | 请求体 | string | 否 | `Pro`（默认，开启 Rerank/高精度提取）或 `Lite`（关闭 Rerank/低成本）；大小写敏感，见 [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md) 和 [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md) |
| `top_k`, `min_score`, `enable_rerank` | 请求体 | number/boolean | 否 | 搜索控制参数：`top_k`（1–100，默认 10），`min_score`（0.0–1.0，默认 0.3），`enable_rerank` 被 `plan_version` 覆盖 |

## 使用方式

1. **准备凭证**：获取 `DASHSCOPE_API_KEY`，通过环境变量配置，并在请求 Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY` 和 `Content-Type: application/json`（[鉴权](../../raw/application-api-reference/long-term-memory-new/overview/authentication.md)）。
2. **写入记忆**：
   - 同步写入：调用 `POST /add`，传入 `messages` 或 `custom_content` + `user_id`；若需画像，**必须同时传入 `profile_schema`**（[添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)）。
   - 异步写入（推荐用于长对话）：调用 `POST /add-async`，立即返回 `event_id`，后续用 `GET /events/{event_id}` 查询状态与结果（[异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)）。
3. **检索记忆**：调用 `POST /memory_nodes/search`，传入 `user_id` + `messages`（当前查询上下文），可选 `top_k`/`min_score`/`plan_version`。
4. **管理画像**：
   - 创建模板：`POST /profile_schemas`，定义字段（[创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)）；
   - 提取后查询：`GET /profile_schemas/{schema_id}/user_profile?user_id=xxx`（[获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)）。

## 限制和注意事项

- **限流**：阿里云账号级总限流 3000 QPM；其中 `Add` 接口 120 QPM，`Search` 接口 300 QPM。超限返回 HTTP 429，需按指数退避重试（1s/2s/4s）（[错误码](../../raw/application-api-reference/long-term-memory-new/overview/errors.md)）。
- **数据持久性**：生成的记忆片段与用户画像**暂无失效日期**，长期保留（[长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)）。
- **关键约束**：
  - `messages` 与 `custom_content` 严格互斥，后者优先级更高；
  - 删除操作（`DELETE /memory_nodes/{id}` 或 `DELETE /profile_schemas/{id}`）**不可逆**，且删除画像模板会一并清除已提取的画像数据；
  - 用户画像提取存在约 3 秒延迟，`GetUserProfile` 需在 `AddMemory` 成功后稍等再调用；
  - `project_id` 与 `project_ids` 互斥，用于记忆二级隔离，非必需。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [API 概览](../../raw/application-api-reference/long-term-memory-new/overview.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/overview/errors.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [事实记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [鉴权](../../raw/application-api-reference/long-term-memory-new/overview/authentication.md)
- [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [删除画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/delete-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)


