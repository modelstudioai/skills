# long term memory new

[长期记忆](../concepts/memory.md)（Long Term Memory）是百炼平台提供的结构化记忆管理能力，支持事实记忆（Observation/Skill）与用户画像（User Profile）两类核心数据的写入、检索、更新与导出。所有操作通过统一的 REST API 提供，基于 DashScope 网关鉴权，适用于构建具备上下文感知与个性化能力的智能体应用。该能力将于 2026 年 8 月 20 日起正式商业化计费。

## 支持的模型/功能

[长期记忆](../concepts/memory.md)提供两类独立但可协同的数据模型：

- **事实记忆**：用于存储用户行为、意图、技能流程等结构化片段，分为 `observation`（如“用户需每天11点点外卖”）和 `skill`（如“会议纪要整理”，含 `skill_name`/`skill_description`/`skill_tags`）。支持同步写入（`/add`）与异步抽取（`/add-async`），后者可并行处理多项目、多类型抽取任务 [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)。
- **用户画像**：基于预定义模板（`profile_schema`）从对话中提取用户属性（如年龄、爱好）。模板支持字段增删改（`attributes_operations`）及 `plan_version`/`extract_scene` 策略配置 [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)。画像提取为异步过程，需调用 `GetUserProfile` 查询结果 [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)。

> **注意**：文档 6（[添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)）称同步接口在 `intelligent` 模式下“可能超时”，而文档 16（[创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)）将 `extract_scene` 默认值设为 `efficient`，且未说明 `intelligent` 模式对同步写入的影响。实际使用中，若需高精度画像提取，应优先选用 `/add-async` 并配合重试逻辑。

## 关键参数

- **身份隔离**：`user_id`（必填）用于跨用户记忆隔离；`memory_library_id` 和 `project_id`/`project_ids` 提供二级隔离。
- **抽取控制**：
  - `extract_mode="profile_only"`：仅触发画像提取（需同时传 `profile_schema` 和 `messages`）。
  - `skill_name`/`skill_description`/`skill_tags`：仅当 `custom_content` 用于 [skill](../guides/skill.md) 写入时为必填。
- **搜索过滤**：
  - `top_k`：最大召回数（默认 10）。
  - `min_score`：仅 `plan_version="pro"` 时生效，默认阈值 0.3，低于此值的结果被过滤。
  - `memory_types`：指定检索类型，如 `["observation", "skill"]`。
- **策略版本**：`plan_version`（`pro`/`lite`）影响计费与能力（如 `min_score` 过滤、Rerank 是否开启），全局默认为 `pro` [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)。

## 使用方式

1. **准备凭证**：在百炼控制台获取 `DASHSCOPE_API_KEY`，通过 `Authorization: Bearer $DASHSCOPE_API_KEY` 请求头传递 [鉴权](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)。
2. **写入记忆**：
   - 同步写入（低延迟场景）：调用 `POST /add`，传 `messages` 或 `custom_content` + `user_id`。
   - 异步写入（推荐）：调用 `POST /add-async`，获取 `event_id` 后轮询 `GET /events/{event_id}` 查询状态与结果。
3. **检索记忆**：
   - 语义搜索：`POST /memory_nodes/search`，传 `messages`（查询语句）和 `user_id`。
   - 列表浏览：`GET /memory_nodes?user_id=xxx`，支持分页（`page_num`/`page_size`）。
4. **管理画像**：
   - 创建模板：`POST /profile_schemas` 定义 `attributes`。
   - 写入画像：在 `AddMemory` 或 `AddMemoryAsync` 中传 `profile_schema` ID。
   - 查询画像：`GET /profile_schemas/{schema_id}/user_profile?user_id=xxx`。

## 限制和注意事项

- **限流**：阿里云账号级总限流 3000 QPM；`/add` 接口 120 QPM，`/memory_nodes/search` 接口 300 QPM [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。
- **异步任务状态**：`/add-async` 返回 `status=PENDING` 或 `RUNNING` 时，需主动轮询 `GET /events/{event_id}` 获取最终结果；`SUCCEEDED` 状态下 `result` 字段才包含有效记忆节点 [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)。
- **不可逆操作**：`DELETE /memory_nodes/{id}` 删除后无法恢复，务必校验 `memory_node_id`。
- **元信息更新**：`PATCH /memory_nodes/{id}` 对 `meta_data` 采用增量更新，未传入的键保持原值。
- **错误处理**：HTTP 429（限流）需指数退避重试（1s/2s/4s）；5xx 错误最多重试 3 次。所有响应均含 `request_id`，用于问题排查 [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [API 概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [鉴权](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)
- [事实记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)
- [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
- [查询记忆节点](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-memory-node.md)
- [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)


