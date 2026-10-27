# long term memory new

长期记忆（Long Term Memory）是百炼平台提供的结构化记忆管理服务，支持事实记忆（Observation/Skill）与用户画像（User Profile）两类核心能力。开发者可通过 REST API 或 `agentscope-runtime` SDK 进行编程式写入、检索、更新与管理，所有操作均基于 `user_id` 隔离，支持多记忆库、多项目二级隔离。服务采用统一鉴权与协议约定，2026 年 8 月 20 日起正式商业化计费。

## 支持的模型/功能

- **事实记忆**：支持从对话消息中自动抽取 `observation`（用户行为/意图）和 `skill`（可复用的工具流程），也支持直接写入 `custom_content`。抽取过程支持多模态内容（文本+图片），但仅限启用多模态能力的业务空间生效 [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)。
- **用户画像**：通过预定义模板（`ProfileSchema`）声明结构化字段（如“年龄”“爱好”），调用 `AddMemory` 时传入 `profile_schema` 即可触发异步提取；提取结果通过 `GetUserProfile` 查询 [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)。
- **异步处理**：`AddMemoryAsync` 接口支持高并发、多项目并行抽取，并返回 `event_id` 供轮询状态；`GetEvent` 可获取完整抽取结果（含 `observation`/`skill`/`user_profile` 类型） [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)。

> **注意**：文档 4 和文档 8 均指出 `AddMemory`（同步）在 `intelligent` 模式下可能超时，而 `AddMemoryAsync` 明确支持技能抽取和用户画像抽取。二者适用场景不同，不应混用为替代方案；同步接口仅推荐用于 `efficient` 模式下的低延迟写入。

## 关键参数

- **必填认证参数**：`Authorization: Bearer $DASHSCOPE_API_KEY`（需与业务空间匹配）、`Content-Type: application/json`、服务地址中的 `{WorkspaceId}`（取自控制台[业务空间管理](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)）。
- **核心业务参数**：
  - `user_id`：所有读写接口必填，用于记忆隔离；
  - `memory_library_id`：指定记忆库（不传则使用默认库）；
  - `project_id` / `project_ids`：用于二级隔离，`search` 和 `add-async` 接口支持多项目；
  - `profile_schema`：提取用户画像时必传，值为 `CreateProfileSchema` 返回的 `profile_schema_id`；
  - `plan_version`：`search` 和 `profile_schema` 创建/更新时可选 `pro`（支持 `min_score` 过滤、Rerank）或 `lite`（基础语义检索）；
  - `extract_mode`：`AddMemory` 中设为 `profile_only` 时仅触发画像提取（需同时传 `messages` 和 `profile_schema`）。

## 使用方式

1. **初始化**：设置环境变量 `DASHSCOPE_API_KEY` 和 `MEMORY_SERVICE_ENDPOINT="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory"`（Python SDK 专用）。
2. **写入记忆**：
   - 同步：调用 `POST /add`，适用于 `efficient` 模式且对实时性要求高的场景；
   - 异步：调用 `POST /add-async`，立即返回 `event_id`，再用 `GET /events/{event_id}` 轮询结果。
3. **检索记忆**：调用 `POST /memory_nodes/search`，传入 `messages`（查询语句）和 `user_id`，按 `top_k` 和 `min_score`（`pro` 版本）控制召回质量。
4. **管理画像**：先调用 `POST /profile_schemas` 创建模板，再在 `AddMemory` 中传入 `profile_schema` 触发提取，最后用 `GET /profile_schemas/{id}/user_profile?user_id=xxx` 获取结果。
5. **SDK 快速接入**：推荐使用 `agentscope-runtime` 工具包（如 `AddMemory`, `SearchMemory`, `GetUserProfile`），封装了请求构造与错误重试逻辑 [概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)。

## 限制和注意事项

- **限流**：阿里云账号级总限流 3000 QPM；其中 `add` 接口 120 QPM，`search` 接口 300 QPM。超限返回 HTTP 429，需按指数退避（1s/2s/4s）重试 [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)。
- **数据持久性**：生成的记忆片段与用户画像暂无自动失效机制，需自行管理生命周期。
- **安全要求**：API Key 具有账号级权限，严禁硬编码或提交至公开仓库；建议为不同应用分配独立 Key 并定期轮转 [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)。
- **删除不可逆**：`DELETE /memory_nodes/{id}` 操作不可恢复，调用前务必确认。
- **计费提示**：2026 年 8 月 20 日起，`Add` 和 `Search` 接口将区分 `Pro`/`Lite` 版本计费，`Pro` 版本支持 Rerank 与 `min_score` 过滤，`Lite` 版本仅提供基础能力。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
- [概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [事实记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)
- [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)
- [查询记忆节点](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-memory-node.md)
- [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)


