# long term memory new

[长期记忆](../concepts/memory.md)（Long Term Memory）是百炼平台提供的结构化记忆管理能力，支持将对话内容自动提取为事实记忆（observation）和用户画像（profile），并提供语义检索、增删改查等完整生命周期管理。所有接口通过 DashScope 网关统一接入，采用标准 RESTful 设计与 API Key 鉴权机制。

## 支持的模型/功能

- **事实记忆（Observation）**：从对话 `messages` 或自定义 `custom_content` 中自动抽取关键事实，生成结构化记忆节点（`memory_node`），支持同步添加（`/add`）与异步添加（`/add-async`）两种模式。  
- **用户画像（Profile）**：基于预定义的画像模板（`profile_schema`），从对话中提取用户属性（如年龄、职业、兴趣）。需在 `AddMemory` 调用中显式传入 `profile_schema` 才会触发提取，否则仅写入事实记忆 [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)。  
- **混合检索能力**：`SearchMemory` 支持查询改写（`enable_rewrite`）、意图判别（`enable_judge`）及结果重排（Rerank），其中 Rerank 行为由 `plan_version`（`Pro`/`Lite`）控制，而非 `enable_rerank` 参数 [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)。  
- **多级隔离支持**：通过 `project_id` 或 `project_ids` 实现记忆的逻辑分组与跨项目混合检索；`skill_name`/`skill_description`/`skill_tags` 用于 [skill](../guides/skill.md) 类型记忆的元数据标注 [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)。

> **注意**：文档 2 和文档 1 均提及商业化计费时间，但存在不一致：文档 1 写为“2026 年 8 月 20 日”，文档 2 写为“2026 年 8 月 20 日 10:00（北京时间）”。以文档 2 的精确时间戳为准。

## 关键参数

| 参数 | 说明 | 示例/约束 |
|------|------|-----------|
| `user_id` | 记忆归属实体 ID，必填，最大 64 字符 | `"user_001"` |
| `messages` / `custom_content` | 互斥：`messages` 为 role-content 对话数组（最多 50 条）；`custom_content` 为纯文本（最大 512 字符） | `[{ "role": "user", "content": "..." }]` |
| `profile_schema` | 画像模板 ID，**不传则完全跳过画像提取** | `"50edf54eaa5842e891d959ae115205be"` |
| `plan_version` | 控制模型策略版本：`Pro`（默认，启用 Rerank/高质量抽取）或 `Lite`（低成本，关闭 Rerank）；大小写不敏感，优先级高于 `enable_rerank` | `"Lite"` |
| `top_k` / `min_score` | 检索参数：召回数量（1–100，默认 10）、最小相似度（0.0–1.0，默认 0.3） | `top_k=5`, `min_score=0.5` |
| `project_ids` | 数组形式，支持多规则混合检索；与 `project_id` 互斥 | `["proj_a", "proj_b"]` |

## 使用方式

1. **准备凭证**：在[百炼控制台](https://bailian.console.aliyun.com)获取 `DASHSCOPE_API_KEY`，并通过环境变量或 Header 传递：`Authorization: Bearer $DASHSCOPE_API_KEY` [鉴权](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)。  
2. **创建画像模板（可选）**：调用 `POST /profile_schemas` 定义字段（如年龄、爱好），获取 `profile_schema_id`。  
3. **写入记忆**：  
   - 同步写入：`POST /add`，适用于轻量对话（≤50 轮）；若需画像，**必须传 `profile_schema`**。  
   - 异步写入：`POST /add-async`，返回 `event_id`，后续用 `GET /events/{event_id}` 查询状态与结果，适合长对话或多模态输入。  
4. **检索与管理**：  
   - 语义搜索：`POST /memory_nodes/search`，推荐设置 `plan_version` 明确策略。  
   - 全量查看：`GET /memory_nodes?user_id=xxx`（分页）。  
   - 更新/删除：`PATCH /memory_nodes/{id}` / `DELETE /memory_nodes/{id}`（不可逆）。  
5. **获取画像**：`GET /profile_schemas/{schema_id}/user_profile?user_id=xxx`，需等待约 3 秒确保提取完成。

## 限制和注意事项

- **限流**：阿里云账号级总限流 3000 QPM；其中 `add` 接口 ≤120 QPM，`search` 接口 ≤300 QPM。超限返回 HTTP 429，需按指数退避（1s/2s/4s）重试 [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)。  
- **参数互斥性**：`messages` 与 `custom_content` 不能共存；`project_id` 与 `project_ids` 互斥；`skill` 类型记忆若使用 `custom_content`，**必须同时传 `skill_name`/`skill_description`/`skill_tags`**。  
- **画像提取依赖**：`GetUserProfile` 返回空值时，首要排查是否在 `AddMemory` 中漏传 `profile_schema` —— 这是常见误用点 [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)。  
- **异步任务状态**：`add-async` 返回 `PENDING` 后，需轮询 `GET /events/{event_id}` 直至 `status` 变为 `SUCCEEDED` 或 `FAILED`；`result` 字段仅在 `SUCCEEDED` 时存在。  
- **安全性**：API Key 具有账号级权限，禁止硬编码或提交至代码仓库；建议按应用分配独立 Key 并定期轮转。

## 来源文档

- [API 概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [鉴权](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [事实记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)
- [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [删除画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/delete-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)


