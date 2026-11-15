# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory, LTM）是百炼平台提供的结构化记忆管理服务，支持事实记忆（`observation`）、技能记忆（`skill`）和用户画像（`user_profile`）三类记忆的写入、检索、更新与生命周期管理。所有操作均通过 RESTful API 或 `agentscope-runtime` SDK 完成，需使用业务空间专属域名和 `DASHSCOPE_API_KEY` 鉴权。记忆数据默认持久化且无自动过期机制，适用于构建具备上下文延续能力的智能体应用。

## 支持的模型/功能

- **记忆类型**：支持 `observation`（事实记忆，如用户偏好、事件记录）、`skill`（技能记忆，如工具调用流程、自动化步骤）和 `user_profile`（用户画像，基于模板抽取的结构化属性）三类记忆节点，类型由 `project_id` 对应的记忆规则或显式参数决定。
- **抽取能力**：
  - 同步抽取（`/add`）：适用于实时性要求高的场景，但 `intelligent` 模式下存在超时风险；详见[添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)。
  - 异步抽取（`/add-async`）：主推方式，支持多项目并行、技能抽取及画像联合提取，结果通过事件 ID 查询；详见[异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)。
- **检索能力**：`/memory_nodes/search` 支持语义相似度检索，可按 `memory_types`（默认仅 `["observation"]`）、`project_id`/`project_ids`、`top_k` 和 `min_score`（仅 `plan_version=pro` 生效）筛选结果。
- **用户画像**：需先创建画像模板（`/profile_schemas`），再在 `AddMemory` 或 `AddMemoryAsync` 中传入 `profile_schema` 触发抽取；画像属性值通过 `/profile_schemas/{schema_id}/user_profile` 获取；详见[创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)。

> **注意**：文档 6 明确指出同步接口在 `intelligent` 模式下“可能超时”，而文档 7 推荐异步接口为“主推方式”。二者存在明确的适用性差异，开发者应优先选用异步路径以保障稳定性。

## 关键参数

- **认证参数**：`Authorization: Bearer $DASHSCOPE_API_KEY`（必填 Header），API Key 必须属于目标业务空间；服务地址为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory/`，其中 `{WorkspaceId}` 需从控制台[业务空间管理](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)页面获取；详见[认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)。
- **核心业务参数**：
  - `user_id`：所有写入/检索接口必填，用于记忆隔离。
  - `project_id` / `project_ids`：指定记忆归属项目，决定抽取规则（如 `observation` 或 `skill`）；`project_ids` 最多支持 5 个，与 `project_id` 互斥。
  - `profile_schema`：触发用户画像抽取的模板 ID，需配合 `messages` 使用（`custom_content` 不支持画像抽取）。
  - `plan_version`：`search` 和 `profile_schema` 创建/更新时可指定 `pro`（支持 `min_score` 过滤、高级抽取）或 `lite`（基础能力），不区分大小写，传入非法值将报错。
- **分页与限流**：列表接口（如 `/memory_nodes`, `/profile_schemas`）支持 `page_num`（默认 1）和 `page_size`（默认 10）；全局限流为 3000 QPM（阿里云账号级），其中 `add` 接口 120 QPM，`search` 接口 300 QPM；详见[长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 使用方式

1. **初始化**：设置环境变量 `MEMORY_SERVICE_ENDPOINT="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory"`（末尾无 `/`）和 `DASHSCOPE_API_KEY`。
2. **写入记忆**：
   - 同步：调用 `POST /add`，传入 `user_id` + `messages`（对话）或 `custom_content`（纯文本）；响应直接返回 `memory_nodes`。
   - 异步：调用 `POST /add-async`，响应返回 `event_id`；随后轮询 `GET /events/{event_id}` 直至 `status=SUCCEEDED`，再解析 `result` 字段。
3. **检索记忆**：调用 `POST /memory_nodes/search`，传入 `user_id` + `messages`（查询语句）+ 可选 `project_ids`/`top_k`/`min_score`。
4. **管理画像**：
   - 创建模板：`POST /profile_schemas`，定义 `attributes`（如年龄、爱好）。
   - 写入画像：在 `AddMemory` 请求中传入 `profile_schema` 和 `messages`。
   - 查询画像：`GET /profile_schemas/{schema_id}/user_profile?user_id=xxx`；首次查询可能为空，需重试（因抽取异步）；详见[获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)。
5. **SDK 调用**：推荐使用 `agentscope-runtime` 工具包（如 `AddMemory`, `SearchMemory`, `GetUserProfile`），封装了请求构造与错误处理逻辑。

## 限制和注意事项

- **商业化时间点**：所有 `Add` 和 `Search` 调用将于 **2026 年 8 月 20 日 10:00（北京时间）** 起正式计费，区分 `Pro` 和 `Lite` 版本；`Pro` 支持 Rerank 和 `min_score` 过滤，`Lite` 仅提供基础能力；详见[长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。
- **关键限制**：
  - `custom_content` 与 `project_ids` 互斥；`custom_content` 与 `skill_name` 等 skill 字段必须同时传入（若需存为 skill）。
  - `GetSkillExport` 仅适用于 `memory_type=skill` 的节点，否则返回 404。
  - 删除操作（`DELETE /memory_nodes/{id}`）为软删除（`status=delete`），不可逆，且历史记录仍可查询。
- **错误处理**：
  - HTTP 429（限流）需按指数退避（1s/2s/4s）重试；5xx 错误最多重试 3 次。
  - 所有响应均含 `request_id`，排查问题时必须提供该字段；错误码详情见[错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)。
- **安全要求**：API Key 必须通过环境变量注入，严禁硬编码或提交至代码仓库；建议为不同应用分配独立 Key 并定期轮转。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
- [记忆管理](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)
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
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)


