# long term memory new

[长期记忆](../concepts/memory.md)（Long Term Memory）是百炼平台提供的结构化用户状态管理能力，支持将对话历史、用户画像、技能知识等持久化为可检索、可更新的事实记忆。其核心是基于语义理解的记忆抽取与向量检索双引擎，开发者可通过统一 API 接口完成写入、搜索、管理全生命周期操作。

## 支持的模型/功能

[长期记忆](../concepts/memory.md)提供两类核心能力：**事实记忆**（Observation/Skill）和**用户画像**（User Profile）。

- **事实记忆**：支持从 `messages` 自动抽取结构化事件（如“每天11点提醒点外卖”），或直接写入 `custom_content`；支持多模态内容（文本+图片 URL）输入，但仅在启用多模态能力的项目中解析图片 [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)。
- **用户画像**：通过预定义的 `profile_schema` 模板提取用户属性（如年龄、职业、爱好），支持异步抽取与增量更新 [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)。
- **技能记忆**：支持以 `skill_name`/`skill_description`/`skill_tags` 三元组形式注册可复用的业务逻辑片段，导出时可获取完整技能元信息 [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)。

> **注意**：同步 `AddMemory` 接口在 `intelligent` 模式下可能超时，官方主推异步接口 `AddMemoryAsync`；二者功能覆盖一致，但异步方式更稳定、支持多项目并行与 [skill](../guides/skill.md) 抽取 [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)。

## 关键参数

| 参数 | 说明 | 必填 | 备注 |
|------|------|------|------|
| `user_id` | 子用户唯一标识，用于记忆隔离 | 是 | 所有读写接口均需传入 |
| `memory_library_id` | 记忆库 ID | 否 | 不传则使用默认库；影响限流配额归属 |
| `project_id` / `project_ids` | 项目 ID 或 ID 列表 | 否 | 用于二级隔离；`project_ids` 最多 5 个，与 `project_id` 互斥 |
| `profile_schema` | 画像模板 ID | 条件必填 | 提取用户画像时必须传入，且需与 `AddMemory` 中 `extract_mode=profile_only` 配合使用 |
| `plan_version` | 计费计划版本 | 否 | `pro`（默认）支持 `min_score` 过滤与 Rerank；`lite` 仅基础检索，不生效 `min_score` [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md) |
| `extract_scene` | 抽取场景 | 否 | `efficient`（默认，低延迟）或 `intelligent`（高精度，可能超时） |

## 使用方式

1. **鉴权准备**：获取 `DASHSCOPE_API_KEY` 并通过 `Authorization: Bearer $DASHSCOPE_API_KEY` 请求头传递 [鉴权](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)。
2. **写入记忆**：
   - 实时写入：调用 `POST /add`，适用于 `efficient` 场景；
   - 异步写入（推荐）：调用 `POST /add-async` 获取 `event_id`，再轮询 `GET /events/{event_id}` 查询结果；
   - 直接写入自定义内容：传 `custom_content`，跳过抽取逻辑。
3. **检索记忆**：
   - 语义搜索：`POST /memory_nodes/search`，传 `messages` 和 `user_id`，返回带 `score` 的相关记忆；
   - 列表浏览：`GET /memory_nodes`，支持分页与 `project_id` 筛选；
   - 单条查询：`GET /memory_nodes/{memory_node_id}` 或 `GET /skill/export/{memory_node_id}`（仅 [skill](../guides/skill.md) 类型）。
4. **管理画像**：
   - 创建模板：`POST /profile_schemas` 定义字段；
   - 写入画像：在 `AddMemory` 中传 `profile_schema` + `messages`；
   - 查询结果：`GET /profile_schemas/{id}/user_profile?user_id=xxx`。

## 限制和注意事项

- **限流规则**（阿里云账号级）：全部接口总计 ≤ 3000 QPM；`add` 接口 ≤ 120 QPM；`search` 接口 ≤ 300 QPM [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。
- **计费时间点**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式商业化，Add/Search 调用按 `pro`/`lite` 版本计费。
- **删除不可逆**：`DELETE /memory_nodes/{id}` 操作永久删除，无回收站 [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)。
- **异步任务状态**：`GetEvent` 返回 `status` 为 `PENDING` 或 `RUNNING` 时需主动轮询，不支持 webhook 回调。
- **多模态兼容性**：`image_url` 仅在显式开通多模态能力的项目中被解析，其他项目忽略图片字段。
- **画像提取延迟**：`GetUserProfile` 首次调用可能返回空值，需按业务逻辑重试，确认 `AddMemory` 已正确传入 `profile_schema` [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)。

## 来源文档

- [API 概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [鉴权](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)
- [事实记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)
- [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)
- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
- [查询记忆节点](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-memory-node.md)
- [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)


