# long term memory new

[长期记忆](../concepts/long-term-memory.md)（记忆库）是百炼平台提供的结构化、可检索的用户与对话上下文持久化服务，支持事实记忆（observation）、技能记忆（skill）和用户画像（user profile）三类数据的写入、检索与管理。所有操作通过统一的 REST API 或 `agentscope-runtime` SDK 完成，需配合业务空间专属域名与 API Key 使用。服务将于 2026 年 8 月 20 日起正式商业化计费，Add 和 Search 接口区分 Pro/Lite 两个策略版本 [原文标题](../../raw/application-api-reference/long-term-memory-new/api-overview.md)。

## 支持的模型/功能

- **记忆类型**：支持 `observation`（事实记忆，如“用户明天要开会”）、`skill`（技能记忆，如“会议纪要整理流程”）和 `user_profile`（用户画像，如年龄、职业等结构化属性）。
- **抽取能力**：
  - 同步抽取：通过 `/add` 接口在响应中直接返回结果，适合 `efficient` 模式下的低延迟场景；但 `intelligent` 模式下可能超时 [原文标题](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)。
  - 异步抽取：通过 `/add-async` 提交任务，用 `/events/{event_id}` 查询状态与结果，支持多项目并行、技能抽取及画像联合提取 [原文标题](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)。
- **多模态支持**：当项目启用多模态能力时，`messages` 中的 `image_url` 可被解析；否则仅处理文本内容。
- **用户画像**：需先创建画像模板（`CreateProfileSchema`），再在 `AddMemory` 中传入 `profile_schema` 触发抽取，最后通过 `GetUserProfile` 获取结果 [原文标题](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)。

> **注意**：文档 5 和文档 7 对同步/异步接口的适用场景描述存在差异——文档 5 称同步接口“适合 `efficient` 模式”，而文档 7 未限定模式但强调异步接口“支持多项目并行抽取”。实际应以文档 7 的能力说明为准，同步接口在 `intelligent` 模式下虽可能超时，但并非完全不可用；开发者应根据 SLA 要求选择：强实时性选同步（配好超时重试），高吞吐或复杂抽取选异步。

## 关键参数

- **必填通用参数**：
  - `user_id`：子用户 ID，用于跨用户记忆隔离。
  - `Authorization: Bearer $DASHSCOPE_API_KEY`：请求头，API Key 需与业务空间匹配 [原文标题](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)。
- **记忆写入核心参数**：
  - `messages` 或 `custom_content`：二选一，前者触发模型抽取，后者直接存为原始内容。
  - `project_id` / `project_ids`：用于二级隔离；`project_ids` 最多 5 个，与 `project_id` 互斥。
  - `profile_schema`：画像模板 ID，仅当需抽取画像时传入。
  - `extract_mode="profile_only"`：仅抽取画像，不生成 observation/skill 记忆。
- **搜索关键参数**：
  - `top_k`：最大召回数，默认 10。
  - `min_score`：最小相似度阈值，默认 0.3，**仅 `plan_version="pro"` 时生效**。
  - `memory_types`：默认 `["observation"]`，可显式指定 `["skill"]` 或 `["observation","skill"]`。
  - `plan_version`：`pro`（启用 Rerank、支持 `min_score`）或 `lite`（基础向量检索），不区分大小写。

## 使用方式

1. **环境准备**：
   - 设置环境变量：`export DASHSCOPE_API_KEY="sk-..."` 和 `export MEMORY_SERVICE_ENDPOINT="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory"`（末尾无 `/`）[原文标题](../../raw/application-api-reference/long-term-memory-new/api-overview.md)。
2. **写入记忆**：
   - 同步：调用 `POST /add`，传 `user_id` + `messages`，立即获得 `memory_nodes` 结果。
   - 异步：调用 `POST /add-async`，获取 `event_id`，再轮询 `GET /events/{event_id}` 直至 `status="SUCCEEDED"`。
3. **检索记忆**：
   - 语义搜索：`POST /memory_nodes/search`，传 `user_id` + `messages`（查询语句），按 `score` 排序返回。
   - 列表浏览：`GET /memory_nodes?user_id=xxx`，支持分页（`page_num`/`page_size`）。
4. **用户画像工作流**：
   - 创建模板 → `POST /profile_schemas`
   - 写入时指定 `profile_schema` → `POST /add`
   - 查询结果 → `GET /profile_schemas/{id}/user_profile?user_id=xxx`

## 限制和注意事项

- **限流**：阿里云账号级总限流 3000 QPM；其中 `/add` 接口 120 QPM，`/memory_nodes/search` 接口 300 QPM [原文标题](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。
- **计费时间点**：2026 年 8 月 20 日 10:00（北京时间）起，Add 和 Search 调用按 Pro/Lite 版本计费，详见[计费说明](raw/application-user-guide/agent-billing/billing.md)。
- **安全要求**：
  - API Key 必须通过环境变量注入，禁止硬编码或提交至代码仓库。
  - 业务空间专属域名仅接受同空间 API Key 的请求，跨空间调用将返回 403 [原文标题](../../raw/application-api-reference/long-term-memory-new/api-overview.md)。
- **其他**：
  - 所有记忆与画像暂无自动过期机制，需自行管理生命周期。
  - 删除操作（`DELETE /memory_nodes/{id}`）不可逆，务必确认 `memory_node_id` 准确性。
  - 错误响应均含 `request_id`，排查问题时必须提供该字段 [原文标题](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)。

## 来源文档

- [概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [记忆管理](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
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


