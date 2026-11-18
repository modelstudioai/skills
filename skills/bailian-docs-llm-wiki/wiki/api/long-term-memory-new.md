# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory, LTM）是百炼平台提供的结构化记忆管理服务，支持事实记忆（`observation`）、技能记忆（`skill`）和用户画像（`user_profile`）三类数据的写入、检索、更新与生命周期管理。所有操作通过 RESTful API 或 `agentscope-runtime` SDK 完成，基于业务空间专属域名和 API Key 鉴权，适用于 Agent 场景下的上下文增强与个性化建模。

## 支持的模型/功能

- **记忆类型**：支持 `observation`（事实性事件，如“用户明天要出差”）、`skill`（可复用的操作流程，如“会议纪要整理”）和 `user_profile`（结构化用户属性，如年龄、职业）三类记忆节点。
- **抽取能力**：
  - `AddMemory` 和 `AddMemoryAsync` 支持从对话消息（`messages`）中自动抽取记忆，或直接写入 `custom_content`；
  - 技能抽取依赖 `tool_calls`（OpenAI 格式）并需指定 `project_id` 或 `project_ids`；
  - 用户画像抽取需提前创建 `profile_schema`，并在写入时传入 `profile_schema` 参数，详见[创建画像模板](raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)。
- **多模态支持**：`messages[].content` 可包含 `text` 或 `image_url` 类型内容，但仅在启用多模态能力的项目中解析图片；其他项目将忽略图片字段 [原文标题](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)。
- **异步处理**：`AddMemoryAsync` 接口返回 `event_id`，后续通过 [GetEvent](raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md) 查询执行状态与结果，适合批量或耗时抽取任务 [原文标题](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)。

> **注意**：文档 15（`AddMemory`）称该同步接口“在 `intelligent` 模式下可能超时”，而文档 6（`AddMemoryAsync`）明确推荐其为“主推”方式；二者功能重叠但适用场景不同。开发者应优先使用异步接口，仅在 `efficient` 模式且对实时性有强要求时选用同步接口。

## 关键参数

- **必填通用参数**：
  - `user_id`：子用户 ID，用于跨用户记忆隔离；
  - `Authorization: Bearer $DASHSCOPE_API_KEY`：请求头，API Key 需与业务空间匹配 [原文标题](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)。
- **记忆写入相关**：
  - `project_id` / `project_ids`：指定记忆规则，决定抽取类型（`observation` 或 `skill`）；
  - `profile_schema`：画像模板 ID，触发用户画像抽取；
  - `extract_mode=profile_only`：仅抽取画像，此时 `messages` 必须存在且 `profile_schema` 必填。
- **搜索相关**：
  - `top_k`：最大召回数量，默认 `10`；
  - `min_score`：最小相似度阈值，默认 `0.3`，**仅 `plan_version=pro` 时生效**；
  - `memory_types`：筛选记忆类型，默认 `["observation"]`；
  - `plan_version`：搜索策略版本，`pro`（支持 Rerank + `min_score` 过滤）或 `lite`（基础向量检索），不区分大小写。
- **分页参数**（`ListMemory`、`ListProfileSchemas` 等）：
  - `page_num`（从 1 开始）、`page_size`（默认 `10`）。

## 使用方式

1. **准备凭证**：获取业务空间 ID（`WorkspaceId`）和 `DASHSCOPE_API_KEY`，设置环境变量：
   ```bash
   export MEMORY_SERVICE_ENDPOINT="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory"
   export DASHSCOPE_API_KEY="sk-xxxxxxxxxxxxxxxx"
   ```
2. **写入记忆**：
   - 同步：调用 `POST /add`，响应中直接返回 `memory_nodes`；
   - 异步：调用 `POST /add-async`，获取 `event_id` 后轮询 `GET /events/{event_id}` 获取结果。
3. **检索记忆**：调用 `POST /memory_nodes/search`，传入 `messages` 和 `user_id`，按 `score` 排序返回 `memory_nodes`。
4. **管理用户画像**：
   - 创建模板：`POST /profile_schemas` 定义 `attributes`；
   - 写入画像：在 `AddMemory` 或 `AddMemoryAsync` 中传入 `profile_schema`；
   - 查询画像：`GET /profile_schemas/{profile_schema_id}/user_profile?user_id=xxx`。
5. **SDK 调用**：推荐使用 `agentscope-runtime` 工具类（如 `AddMemory`, `SearchMemory`, `GetUserProfile`），封装了 endpoint 和鉴权逻辑。

## 限制和注意事项

- **限流**（阿里云账号级别）：
  - 全部接口总计 ≤ 3000 QPM；
  - `add` 接口 ≤ 120 QPM；
  - `search` 接口 ≤ 300 QPM；
  - 超限返回 HTTP 429，需按指数退避（1s/2s/4s）重试 [原文标题](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)。
- **商业化时间**：服务将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式计费，`Add` 和 `Search` 均区分 `Pro`/`Lite` 版本，影响抽取质量与 Rerank 能力 [原文标题](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。
- **数据持久性**：生成的记忆片段与用户画像**暂无失效日期**，但软删除（`status=delete`）后仍可通过 `GetMemoryNode` 查询历史记录。
- **安全要求**：
  - API Key 必须通过环境变量注入，禁止硬编码或提交至代码仓库；
  - RAM 子账号需显式授权 `AliyunBailianFullAccess` 或最小权限策略。
- **关键约束**：
  - `custom_content` 与 `project_ids` / `project_id` 互斥；
  - `skill_name`、`skill_description`、`skill_tags` 必须同时传入（当写入 skill 类型且使用 `custom_content` 时）；
  - 更新 `profile_schema` 的 `plan_version` 仅影响新写入的记忆，已提取画像不受影响。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)
- [记忆管理](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)
- [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
- [查询记忆节点](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-memory-node.md)
- [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)


