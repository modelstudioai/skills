# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory）是百炼平台提供的结构化记忆管理能力，支持事实记忆（Observation、Skill）和用户画像（User Profile）两类核心数据的写入、检索、更新与管理。所有操作通过统一的 RESTful API 完成，基于 DashScope 网关提供服务，需使用 `DASHSCOPE_API_KEY` 鉴权。该能力已于 2024 年全面上线，计划于 2026 年 8 月 20 日起正式商业化计费。

## 支持的模型/功能

[长期记忆](../concepts/long-term-memory.md)提供两类语义化记忆能力：
- **事实记忆**：包括 `observation`（用户行为/意图片段）和 `skill`（可复用的流程化能力），支持同步/异步写入、语义搜索、分页列表、单节点查询及导出（[导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)）；
- **用户画像**：通过预定义模板（Schema）提取结构化属性（如年龄、爱好），支持模板创建、更新、列表及用户级画像查询（[获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)）。

> **注意**：文档 6（[添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)）称同步接口在 `intelligent` 模式下“可能超时”，而文档 14（[创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)）明确 `extract_scene` 参数支持 `efficient` 和 `intelligent` 两种值。但文档 17（[更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)）指出 `extract_scene` 可更新，且未说明 `intelligent` 模式对同步写入的兼容性。实践中应优先使用 `efficient` 场景或异步接口以保障稳定性。

## 关键参数

| 参数 | 作用 | 示例/说明 |
|------|------|-----------|
| `user_id` | 必填，用于跨用户记忆隔离 | `"user_001"` |
| `memory_library_id` | 可选，指定记忆库；不传则使用默认库 | `"memory_library_001"` |
| `project_id` / `project_ids` | 可选，用于二级隔离；`project_ids` 最多 5 个，与 `project_id` 互斥 | `["project_001"]` |
| `plan_version` | 搜索/模板类接口可选，取值 `pro` 或 `lite`；`pro` 支持 `min_score` 过滤（[搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)） | `"pro"` |
| `extract_mode` | 写入时可选，`profile_only` 表示仅抽取画像（需同时传 `profile_schema`） | `"profile_only"` |
| `min_score` | 仅 `plan_version=pro` 时生效，默认 `0.3`，低于此值的结果被过滤 | `0.6` |

## 使用方式

1. **鉴权**：在请求 Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY`（[鉴权](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)）；
2. **写入记忆**：
   - 同步写入（低延迟场景）：调用 `/add`，直接返回抽取结果；
   - 异步写入（推荐）：调用 `/add-async` 获取 `event_id`，再轮询 `/events/{event_id}` 查询状态与结果；
3. **检索记忆**：
   - 语义搜索：`POST /memory_nodes/search`，传入 `messages` 和 `user_id`；
   - 列表查询：`GET /memory_nodes`，支持 `page_num`/`page_size` 分页；
4. **管理用户画像**：
   - 先创建模板（`POST /profile_schemas`），再调用 `AddMemory` 时传 `profile_schema` 触发抽取；
   - 抽取完成后，用 `GET /profile_schemas/{schema_id}/user_profile?user_id=xxx` 获取结果。

## 限制和注意事项

- **限流**：阿里云账号级总限流 3000 QPM；其中 `add` 接口 ≤120 QPM，`search` 接口 ≤300 QPM（[长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)）；
- **异步任务状态**：`GetEvent` 返回 `status` 为 `PENDING` 或 `RUNNING` 时需轮询，不可立即读取 `result`；
- **删除不可逆**：`DELETE /memory_nodes/{id}` 操作无回收机制，务必校验 `memory_node_id`；
- **画像提取延迟**：`GetUserProfile` 首次调用可能返回空值，需按业务逻辑重试（[获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)）；
- **多模态支持**：仅部分项目支持图片解析，`messages[].content[].type="image_url"` 仅在启用多模态能力时生效。

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
- [查询记忆节点](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-memory-node.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
- [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)


