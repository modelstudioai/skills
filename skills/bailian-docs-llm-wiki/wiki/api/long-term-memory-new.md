# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory）是百炼平台提供的结构化记忆管理能力，支持事实记忆（Observation/Skill）与用户画像（Profile）两类核心数据的写入、检索、更新与导出。所有接口通过统一的 DashScope 网关提供服务，采用 API Key 鉴权，适用于 Agent 场景下的上下文持久化与个性化建模。该能力已于 2024 年全面上线，计划于 2026 年 8 月 20 日起正式商业化计费。

## 支持的模型/功能

[长期记忆](../concepts/long-term-memory.md)提供两类独立但可协同的数据模型：

- **事实记忆（Fragments）**：包括 `observation`（用户行为/意图片段）和 `skill`（可复用的执行流程），支持同步/异步添加、语义搜索、分页列表、单点查询、导出与增删改。其中 `skill` 类型记忆需通过 [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md) 接口获取完整元信息（如 `skill_name`、`skill_description`）。
- **用户画像（Profiles）**：基于预定义模板（`profile_schema`）提取结构化用户属性。需先调用 [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)，再在 `AddMemory` 中传入 `profile_schema` 参数触发抽取；最终通过 [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md) 查询结果。

> **注意**：文档 14 和文档 18 明确要求画像提取依赖 `AddMemory` 调用时显式传入 `profile_schema`；而文档 4 的 `AddMemory` 参数说明中未强调此为“必填”条件（仅标注“否”），实际业务中若遗漏将导致画像无法生成。请以文档 18 的说明为准。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `user_id` | Query / Body | string | 是 | 子用户 ID，用于跨用户记忆隔离，所有读写接口均需提供 |
| `memory_library_id` | Query / Body | string | 否 | 记忆库 ID，不传则使用默认库；影响写入归属与检索范围 |
| `project_id` / `project_ids` | Body | string / array | 否 | 项目级二级隔离标识，`project_ids` 最多支持 5 个，与 `custom_content` 互斥 |
| `plan_version` | Body | string | 否 | 计费策略，`pro`（支持 `min_score` 过滤）或 `lite`（基础检索），默认 `pro`；见 [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md) |
| `extract_mode` | Body | string | 否 | 抽取模式，`profile_only` 表示仅提取画像（需同时传 `profile_schema` 和 `messages`） |
| `min_score` | Body | number | 否 | 搜索分数阈值（仅 `plan_version=pro` 时生效），默认 `0.3` |

## 使用方式

1. **认证准备**：获取 `DASHSCOPE_API_KEY` 并通过 `Authorization: Bearer $DASHSCOPE_API_KEY` 请求头传递，详见 [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)。
2. **写入记忆**：
   - 实时性要求高 → 用同步 `POST /add`（[添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)）；
   - 需支持 Skill/Profile 多类型抽取或批量处理 → 用异步 `POST /add-async`（[异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)），再通过 `GET /events/{event_id}` 查询结果。
3. **检索记忆**：调用 `POST /memory_nodes/search`，传入 `messages`（语义查询）和 `user_id`，按需设置 `top_k`、`min_score`、`memory_types`。
4. **管理画像**：先 `POST /profile_schemas` 创建模板，再在 `AddMemory` 中指定 `profile_schema` 触发抽取，最后 `GET /profile_schemas/{id}/user_profile?user_id=xxx` 获取结果。
5. **工具封装**：推荐使用 `agentscope_runtime.tools.modelstudio_memory` 中的 SDK 工具类（如 `AddMemory`, `SearchMemory`, `GetUserProfile`），其已封装鉴权、重试与错误处理逻辑。

## 限制和注意事项

- **限流**：阿里云账号级总限流 3000 QPM；`/add` 接口单独限流 120 QPM，`/memory_nodes/search` 限流 300 QPM。超限返回 HTTP 429，需按 [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md) 文档执行指数退避重试（1s/2s/4s）。
- **异步任务状态**：`/add-async` 返回 `status=PENDING` 或 `RUNNING` 时，必须轮询 `/events/{event_id}` 直至 `status=SUCCEEDED` 或 `FAILED`，不可假设立即完成。
- **删除不可逆**：`DELETE /memory_nodes/{id}` 操作永久删除，无回收站机制，调用前务必校验 `memory_node_id`。
- **多模态支持**：仅部分项目支持图片解析，`messages[].content` 中的 `image_url` 在非多模态项目中会被忽略。
- **计费变更**：所有 Add/Search 调用自 2026 年 8 月 20 日起区分 `Pro`/`Lite` 版本计费，策略差异详见 [计费说明](../../raw/application-user-guide/agent-context/memory-library-overview/integration-overview/billing.md)。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)
- [事实记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
- [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)
- [查询记忆节点](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-memory-node.md)
- [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)


