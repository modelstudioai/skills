# long term memory new

[长期记忆](../concepts/memory.md)（Long Term Memory）是百炼平台提供的结构化记忆管理服务，支持事实记忆的语义化存储与检索，以及基于模板的用户画像自动提取。它通过统一 API 接口提供写入、搜索、列表、更新、删除等操作，并支持同步/异步两种添加模式，适用于对话系统、智能体状态持久化等场景。

## 支持的模型/功能

- **事实记忆（Observation）**：从对话消息（`messages`）或自定义文本（`custom_content`）中自动抽取关键事实，生成结构化记忆节点。支持最多 50 轮对话输入，`role` 支持 `user`/`assistant`/`tool` [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)。
- **用户画像（Profile）**：基于预定义的画像模板（`profile_schema`），从对话中提取用户属性（如年龄、职业、兴趣）。模板字段由 `name` 和 `description` 定义，支持 `Pro`/`Lite` 两种提取策略 [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)。
- **异步处理**：对长对话或多模态输入，推荐使用 `add-async` 接口，后台执行记忆抽取与画像生成，通过 `event_id` 查询状态 [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)。
- **语义搜索增强**：`SearchMemory` 支持查询改写（`enable_rewrite`）、意图判别（`enable_judge`）、结果重排（`enable_rerank` 或 `plan_version`）及相似度阈值过滤（`min_score`）。

> **注意**：文档 1 和文档 2 对商业化时间的描述存在不一致——文档 1 写为“2026 年 8 月 20 日”，文档 2 写为“2026 年 8 月 20 日 10:00（北京时间）”。以文档 2 的精确时间戳为准。

## 关键参数

| 参数 | 说明 | 示例/约束 |
|--------|------|-----------|
| `user_id` | 记忆归属实体 ID，必填，最大 64 字符 | `"user_001"` |
| `messages` / `custom_content` | 互斥：`messages` 为对话数组（含 `role`/`content`），`custom_content` 为纯文本（≤512 字符） | `[{ "role": "user", "content": "每天9点喝水" }]` |
| `profile_schema` | 画像模板 ID；不传则仅写入事实记忆，不触发画像提取 | `"50edf54eaa5842e891d959ae115205be"` |
| `project_id` / `project_ids` | 记忆规则隔离标识；`project_ids` 支持多规则混合检索 | `["project_001"]` |
| `top_k` / `min_score` | 搜索时控制召回数量（1–100）和最小相似度（0.0–1.0） | `top_k=10`, `min_score=0.3` |
| `plan_version` | 统一控制质量策略：`Pro`（默认，开启 Rerank）或 `Lite`（关闭 Rerank），大小写不敏感 | `"Lite"` |

## 使用方式

1. **准备凭证**：在[百炼控制台](https://bailian.console.aliyun.com)获取 `DASHSCOPE_API_KEY`，并设置环境变量或请求头 `Authorization: Bearer $DASHSCOPE_API_KEY` [鉴权](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)。
2. **写入记忆**：
   - 同步：调用 `/add`，立即返回记忆节点（适合短对话）；
   - 异步：调用 `/add-async`，返回 `event_id`，再用 `/events/{event_id}` 查询执行结果 [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)。
3. **检索记忆**：调用 `/memory_nodes/search`，传入 `user_id` + `messages`（当前查询上下文），按需配置 `top_k`、`min_score` 和 `plan_version`。
4. **管理画像**：
   - 创建模板 → 调用 `/add` 时传入 `profile_schema` → 等待约 3 秒 → 调用 `/profile_schemas/{id}/user_profile?user_id=xxx` 获取结果。
5. **调试与排障**：所有响应均含 `request_id`，错误时参考 [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md) 处理；限流失败（HTTP 429）需指数退避重试。

## 限制和注意事项

- **限流**：阿里云账号级总限流 3000 QPM；其中 `add` 接口 ≤120 QPM，`search` 接口 ≤300 QPM。超出需[提交工单](https://smartservice.console.aliyun.com/service/create-ticket)申请扩容 [使用限制](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。
- **数据生命周期**：当前生成的记忆片段与用户画像**暂无自动失效机制**，需自行管理生命周期。
- **画像提取延迟**：调用 `AddMemory` 后，画像需约 3 秒完成提取，立即调用 `GetUserProfile` 可能返回空值 [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)。
- **不可逆操作**：`DeleteMemory` 和 `DeleteProfileSchema` 均不可恢复，且后者会**同时清除已提取的全部画像数据**。
- **安全要求**：API Key 必须通过环境变量等方式保密，禁止硬编码或提交至代码仓库 [鉴权](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)。

## 来源文档

- [API 概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [鉴权](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)
- [事实记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)
- [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)
- [删除画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/delete-schema.md)


