# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory）是百炼平台提供的结构化记忆管理能力，支持事实记忆（Observation/Skill）与用户画像（User Profile）两类核心数据的写入、检索、更新与导出。所有操作均通过 RESTful API 实现，需使用 `DASHSCOPE_API_KEY` 鉴权，服务地址统一为 `https://dashscope.aliyuncs.com/api/v2/apps/memory/`。该能力已于 2024 年全面上线，计划于 2026 年 8 月 20 日起正式商业化计费。

## 支持的模型/功能

[长期记忆](../concepts/long-term-memory.md)提供两类独立但可协同的数据模型：

- **事实记忆**：用于存储用户行为、意图、任务等动态事实，分为 `observation`（通用事实）和 `skill`（可复用的流程化能力）。支持同步写入（`/add`）、异步批量抽取（`/add-async`）、语义搜索（`/memory_nodes/search`）、分页列表（`/memory_nodes`）及细粒度 CRUD 操作。[添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md) 和 [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md) 是写入入口，后者推荐用于高吞吐或含多模态内容的场景。
  
- **用户画像**：用于结构化描述用户静态属性，需先定义模板（`profile_schema`），再通过 `AddMemory` 触发抽取。模板支持字段增删改（`attributes_operations`）、提取场景（`efficient`/`intelligent`）与计费策略（`pro`/`lite`）配置。画像提取为异步过程，结果需通过 [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md) 查询。

> **注意**：文档 6（`/add`）称其“在 `intelligent` 模式下可能超时”，而文档 15（`CreateProfileSchema`）将 `extract_scene` 默认设为 `efficient` 且未说明 `intelligent` 对 `/add` 的兼容性。实际调用中，若需 `intelligent` 提取画像，应优先使用 `/add-async` 并显式传入 `profile_schema`，避免同步接口超时风险。

## 关键参数

| 参数 | 位置 | 类型 | 说明 | 示例 |
|------|------|------|------|------|
| `user_id` | Query / Body | string | **必填**，子用户 ID，用于跨用户记忆隔离 | `"user_001"` |
| `memory_library_id` | Query / Body | string | 可选，指定记忆库；不传则使用默认库 | `"memory_library_001"` |
| `project_id` / `project_ids` | Query / Body | string / array | 可选，用于二级隔离；`project_ids` 最多 5 个，与 `project_id` 互斥 | `["project_a", "project_b"]` |
| `plan_version` | Body (schema) / Query (search) | string | `pro` 或 `lite`，影响抽取质量与 Rerank 能力；`pro` 支持 `min_score` 过滤 | `"pro"` |
| `min_score` | Body (search) | number | 仅 `plan_version=pro` 时生效，默认 `0.3`，低于此值的结果被过滤 | `0.6` |
| `extract_mode` | Body (add) | string | `profile_only` 表示仅抽取画像（需同时传 `profile_schema` 和 `messages`） | `"profile_only"` |

## 使用方式

1. **鉴权准备**：在百炼控制台获取 `DASHSCOPE_API_KEY`（以 `sk-` 开头），并通过环境变量或 Header 传递：`Authorization: Bearer $DASHSCOPE_API_KEY`。详见 [鉴权](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)。
2. **写入记忆**：
   - 同步写入（低延迟）：调用 `POST /add`，传入 `messages` 或 `custom_content` + `user_id`。
   - 异步写入（高可靠）：调用 `POST /add-async`，获取 `event_id` 后轮询 `GET /events/{event_id}` 查询结果。
3. **检索记忆**：
   - 语义搜索：`POST /memory_nodes/search`，传入 `messages`（查询语句）和 `user_id`，支持 `top_k` 和 `min_score`。
   - 列表浏览：`GET /memory_nodes?user_id=xxx`，支持分页（`page_num`/`page_size`）。
4. **管理画像**：
   - 创建模板：`POST /profile_schemas`，定义 `attributes` 字段。
   - 写入触发：在 `AddMemory` 请求中传入 `profile_schema` ID。
   - 查询结果：`GET /profile_schemas/{id}/user_profile?user_id=xxx`。

## 限制和注意事项

- **限流**：阿里云账号级总限流 3000 QPM；其中 `add` 接口限 120 QPM，`search` 接口限 300 QPM。超限返回 HTTP 429，需按指数退避重试（1s/2s/4s）。详见 [限流说明](../../raw/application-user-guide/memory-library-overview/integration-overview/limits.md)。
- **计费时间点**：所有接口将于 **2026 年 8 月 20 日 10:00（北京时间）** 起正式计费，`Add` 和 `Search` 均区分 `Pro`/`Lite` 版本。[计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md) 中明确 `Pro` 版本支持 Rerank 与 `min_score` 过滤，`Lite` 版本不支持。
- **安全要求**：API Key 具有账号级权限，**严禁硬编码或提交至代码仓库**，建议按应用拆分并定期轮转。
- **异步行为**：`/add-async` 返回 `PENDING` 或 `RUNNING` 状态时，必须主动轮询 `GET /events/{event_id}` 获取最终结果；`GetUserProfile` 首次调用可能为空，需业务侧实现重试逻辑。
- **不可逆操作**：`DELETE /memory_nodes/{id}` 删除后无法恢复，请谨慎执行。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [鉴权](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
- [API 概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
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
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)


