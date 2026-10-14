# long term memory new

长期记忆（Long Term Memory）是百炼平台提供的结构化记忆管理能力，支持事实记忆（Observation/Skill）与用户画像（User Profile）两类核心数据的写入、检索、更新与导出。所有操作通过统一的 RESTful API 提供，基于 DashScope 网关鉴权，适用于 Agent 场景下的上下文持久化与个性化建模。服务已于 2024 年全面上线，商业化计费将于 2026 年 8 月 20 日起正式生效。

## 支持的模型/功能

长期记忆提供两类独立但可协同的数据模型：

- **事实记忆**：包括 `observation`（用户行为/意图片段）和 `skill`（可复用的工具流程），支持同步添加（`/add`）、异步批量抽取（`/add-async`）、语义搜索（`/memory_nodes/search`）、分页列表（`/memory_nodes`）及细粒度 CRUD 操作。`skill` 类型记忆额外支持导出完整元信息（如 `skill_name`、`skill_tags`），详见 [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)。
- **用户画像**：基于预定义模板（`profile_schema`）提取结构化属性（如年龄、爱好）。需先调用 [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)，再在 `AddMemory` 中传入 `profile_schema` 触发抽取；最终通过 [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md) 查询结果。画像提取为异步过程，首次查询可能为空，需按业务逻辑重试。

> **注意**：文档 6（[添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)）称同步接口“在 `intelligent` 模式下可能超时”，而文档 15（[创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)）将 `extract_scene` 默认值设为 `efficient`，且未说明 `intelligent` 模式对同步写入的影响。实际使用中，若需高精度画像或复杂 observation 抽取，应优先选用 `/add-async` 接口，并通过 [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md) 轮询状态。

## 关键参数

- **身份隔离**：所有接口必须传 `user_id`（子用户 ID）；可选 `memory_library_id`（记忆库 ID）和 `project_id` / `project_ids`（项目级二级隔离）。
- **抽取控制**：
  - `extract_mode="profile_only"`：仅触发画像抽取（需同时传 `profile_schema` 和 `messages`）。
  - `plan_version`：影响计费与能力，`pro` 支持 `min_score` 过滤（[搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)）、更高质量抽取；`lite` 为轻量版本。
  - `extract_scene`（仅画像模板）：`efficient`（低延迟）或 `intelligent`（高精度），影响抽取模型选择。
- **搜索与分页**：
  - `top_k`（默认 10）、`min_score`（`pro` 专属，默认 0.3）、`memory_types`（默认 `["observation"]`）控制搜索结果。
  - 列表接口（`/memory_nodes`, `/profile_schemas`）使用 `page_num`（从 1 开始）和 `page_size`（默认 10）分页。

## 使用方式

1. **认证**：在请求 Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，API Key 通过 [百炼控制台](https://bailian.console.aliyun.com) 获取，详见 [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)。
2. **基础流程**：
   - 写入：对事实记忆，推荐使用 `/add-async`（高可靠）或 `/add`（低延迟）；对用户画像，需先创建模板，再调用 `/add` 并传 `profile_schema`。
   - 检索：用 `/memory_nodes/search` 基于对话消息语义搜索；用 `/memory_nodes` 分页查看全量记忆；用 `/profile_schemas/{id}/user_profile?user_id=xxx` 查询画像。
   - 管理：通过 `/memory_nodes/{id}` 查看单条记忆；`/skill/export/{id}` 导出 skill 元信息；`/profile_schemas` 系列接口管理模板。
3. **SDK 支持**：`agentscope_runtime.tools.modelstudio_memory` 提供 `AddMemory`, `SearchMemory`, `GetUserProfile` 等异步封装，降低集成成本。

## 限制和注意事项

- **限流**：阿里云账号级别总计 ≤ 3000 QPM；其中 `/add` ≤ 120 QPM，`/memory_nodes/search` ≤ 300 QPM。超限返回 HTTP 429，建议按指数退避（1s/2s/4s）重试。
- **异步任务**：`/add-async` 返回 `event_id` 后，需轮询 `/events/{event_id}` 获取结果；`status` 为 `PENDING` 或 `RUNNING` 时需等待，详见 [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)。
- **数据生命周期**：当前生成的记忆片段与用户画像**无自动失效机制**，长期有效。如需清理，须显式调用 `/memory_nodes/{id}` 删除。
- **安全**：API Key 具有账号级权限，严禁硬编码或提交至代码仓库；建议按应用拆分并定期轮转。
- **兼容性**：所有接口仅支持 HTTPS；请求/响应体为 UTF-8 编码 JSON；多模态内容（图片）仅在启用对应能力的项目中被解析。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)
- [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
- [事实记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)
- [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)
- [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)
- [查询记忆节点](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-memory-node.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)


