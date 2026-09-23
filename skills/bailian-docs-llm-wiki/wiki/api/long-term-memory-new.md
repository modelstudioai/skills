# long term memory new

[长期记忆](../concepts/memory.md)（Long Term Memory, LTM）New 是百炼平台提供的结构化记忆管理服务，支持事实记忆（observation/[skill](../guides/skill.md)）与用户画像（profile）两类核心能力。它通过统一 API 提供记忆写入、语义检索、模板化画像抽取与管理等功能，适用于需要持久化用户上下文、行为模式或技能沉淀的智能体应用。服务基于 DashScope 网关提供，所有接口均需 API Key 鉴权。

## 支持的模型/功能

[长期记忆](../concepts/memory.md) New 提供两类独立但可协同使用的功能模块：

- **事实记忆**：支持从对话消息中自动抽取结构化记忆节点（`observation` 类型），或显式注册技能流程（`skill` 类型）。抽取过程由后端模型完成，开发者无需指定具体模型名称，但可通过 `extract_mode` 和 `plan_version` 控制抽取策略。异步接口（`/add-async`）支持多项目并行抽取与 [skill](../guides/skill.md)/user_profile 混合提取；同步接口（`/add`）适用于对实时性要求高且内容较简短的场景 [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)。
- **用户画像**：基于预定义的画像模板（`profile_schema`），从对话中异步提取用户属性（如年龄、职业、偏好等）。模板支持字段增删改、`plan_version`（`pro`/`lite`）与 `extract_scene`（`efficient`/`intelligent`）配置，影响抽取精度与延迟 [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)。

> **注意**：文档中多次提及 `plan_version` 参数在 `AddMemory`、`SearchMemory` 和 `CreateProfileSchema` 中均存在，但其语义不一致：在 `AddMemory` 中未定义该参数（仅 `AddMemoryAsync` 支持 `profile_schema` 与 `extract_mode`），在 `SearchMemory` 中控制 Rerank 是否启用，在 `CreateProfileSchema` 中则关联画像抽取质量。实际调用时请严格依据各接口文档，避免混淆。

## 关键参数

| 参数 | 位置 | 说明 | 必填 |
|------|------|------|------|
| `user_id` | Query / Body | 子用户 ID，用于记忆隔离，是所有读写操作的强制隔离维度 | 是 |
| `memory_library_id` | Query / Body | 记忆库 ID，用于跨应用/租户隔离；不传则使用默认库 | 否 |
| `project_id` / `project_ids` | Query / Body | 项目 ID 或 ID 列表，用于二级隔离；`project_id` 与 `project_ids` 互斥 | 否 |
| `profile_schema` | Body | 用户画像模板 ID，仅在需触发画像抽取时传入（配合 `messages`） | 条件必填 |
| `extract_mode` | Body | 抽取模式，仅 `AddMemoryAsync` 支持 `profile_only`；`AddMemory` 不支持此参数 | 否 |
| `plan_version` | Body (SearchMemory, CreateProfileSchema) / Path (AddMemoryAsync) | `pro` 启用高级 Rerank 或高精度抽取；`lite` 为轻量级版本。**`AddMemory` 接口不接受该参数** | 否（默认 `pro`） |
| `top_k`, `min_score` | Body (SearchMemory) | 检索结果数量上限与最小相似度阈值（仅 `plan_version=pro` 时 `min_score` 生效） | 否 |

## 使用方式

1. **鉴权准备**：获取 `DASHSCOPE_API_KEY` 并通过 `Authorization: Bearer $DASHSCOPE_API_KEY` 请求头传递 [鉴权](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)。
2. **写入记忆**：
   - 同步写入（低延迟）：调用 `POST /add`，传入 `messages` 或 `custom_content` + `user_id`。
   - 异步写入（推荐）：调用 `POST /add-async`，获取 `event_id` 后轮询 `GET /events/{event_id}` 查询状态与结果 [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)。
3. **检索记忆**：调用 `POST /memory_nodes/search`，传入查询 `messages` 和 `user_id`，支持 `top_k`、`min_score`（Pro 版）和 `memory_types` 过滤。
4. **管理画像**：
   - 创建模板：`POST /profile_schemas` 定义属性列表；
   - 写入画像：在 `AddMemoryAsync` 中传入 `profile_schema`；
   - 查询画像：`GET /profile_schemas/{schema_id}/user_profile?user_id=xxx`，注意首次查询可能为空，需重试 [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)。
5. **其他操作**：`GET /memory_nodes` 分页列出、`GET /memory_nodes/{id}` 查单条、`PATCH /memory_nodes/{id}` 更新、`DELETE /memory_nodes/{id}` 删除。

## 限制和注意事项

- **限流**：全接口阿里云账号级总计 ≤ 3000 QPM；其中 `add` 接口 ≤ 120 QPM，`search` 接口 ≤ 300 QPM。超限返回 `429`，需按指数退避（1s/2s/4s）重试 [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)。
- **计费时间点**：服务将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式商业化计费，`Add` 和 `Search` 调用将区分 `Pro` 与 `Lite` 版本 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。
- **异步任务状态**：`AddMemoryAsync` 返回 `status: PENDING` 或 `RUNNING` 时，必须主动轮询 `GetEvent` 接口获取最终结果；`SUCCEEDED` 状态下 `result` 字段才包含有效记忆数据。
- **画像提取延迟**：用户画像为异步生成，`GetUserProfile` 首次调用可能返回空值，需按业务逻辑重试，而非立即报错。
- **安全要求**：API Key 必须通过环境变量注入，严禁硬编码或提交至代码仓库 [鉴权](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)
- [API 概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [事实记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)
- [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
- [查询记忆节点](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-memory-node.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)
- [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)
- [鉴权](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)


