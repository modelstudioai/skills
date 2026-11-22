# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory）是百炼平台提供的结构化记忆管理服务，支持事实记忆（observation）、技能记忆（skill）和用户画像（user profile）三类记忆的写入、检索、更新与生命周期管理。所有操作均通过 RESTful API 或 `agentscope-runtime` SDK 实现，具备多项目隔离、[多模态](../concepts/multi-modal.md)内容支持、异步抽取与语义搜索能力。服务基于业务空间专属域名提供，需使用对应 Workspace 的 API Key 鉴权。

## 支持的模型/功能

- **记忆类型**：支持 `observation`（事实记忆，如“用户明天10点开会”）、`skill`（技能记忆，如“会议纪要整理”流程）和 `user_profile`（结构化用户画像，需先定义模板）三类记忆节点，类型由 `project_id` 对应的记忆规则或显式传入的 `profile_schema` 决定。
- **抽取模式**：同步接口（`/add`）适用于实时性要求高的 `efficient` 场景；异步接口（`/add-async`）支持多项目并行、技能抽取及画像联合提取，推荐用于生产环境 —— 详见 [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)。
- **搜索能力**：`/memory_nodes/search` 支持语义相似度检索，默认仅返回 `observation` 类型，可通过 `memory_types` 参数扩展为 `["observation", "skill"]`；`pro` 计划支持 `min_score` 过滤与 Rerank，`lite` 计划仅基础向量召回。
- **用户画像**：需先调用 [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md) 定义字段（如“年龄”“爱好”），再在 `AddMemory` 或 `AddMemoryAsync` 中传入 `profile_schema` 触发抽取，最终通过 [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md) 查询结果。

> **注意**：文档 6（[添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)）称同步接口“在 `intelligent` 模式下可能超时”，而文档 7（[异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)）明确指出异步接口“支持多项目并行抽取、技能抽取和用户画像抽取”。二者功能边界清晰，但文档 6 未说明 `intelligent` 模式是否被同步接口实际支持；实践中应以异步接口为准，避免在复杂抽取场景下依赖同步调用。

## 关键参数

- **必填认证参数**：`Authorization: Bearer $DASHSCOPE_API_KEY`（Header）、`user_id`（Query 或 Body），且 API Key 必须属于请求地址中 `{WorkspaceId}` 对应的业务空间 —— 参见 [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)。
- **记忆写入核心参数**：
  - `messages`（array）或 `custom_content`（string）：二选一，前者触发智能抽取，后者直接存为原始内容；
  - `project_id` / `project_ids`：指定记忆归属项目，决定抽取规则（如 `observation` 或 `skill`）；
  - `profile_schema`（string）：启用用户画像抽取时必需；
  - `extract_mode="profile_only"`：仅抽取画像，不生成 observation/skill 节点。
- **搜索关键参数**：
  - `top_k`（integer，默认 10）：最大召回数；
  - `min_score`（number，默认 0.3）：仅 `plan_version="pro"` 时生效，用于过滤低置信度结果；
  - `memory_types`（array，默认 `["observation"]`）：显式指定检索类型，`skill` 类型需单独声明。
- **分页通用参数**：`page_num`（从 1 开始）、`page_size`（默认 10），适用于 `ListMemory`、`ListProfileSchemas` 等列表接口。

## 使用方式

1. **初始化**：设置环境变量 `MEMORY_SERVICE_ENDPOINT="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory"` 和 `DASHSCOPE_API_KEY`，其中 `{WorkspaceId}` 从[业务空间管理](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)页面复制。
2. **写入记忆**：
   - 同步：调用 `POST /add`，适合轻量、实时场景（如单轮对话摘要）；
   - 异步：调用 `POST /add-async` 获取 `event_id`，再轮询 `GET /events/{event_id}` 查询状态与结果，适合批量、多项目或含技能/画像的复杂写入。
3. **检索记忆**：调用 `POST /memory_nodes/search`，传入查询 `messages` 和 `user_id`，按需配置 `top_k`、`memory_types` 等参数。
4. **管理画像**：先用 `POST /profile_schemas` 创建模板，再在写入时传 `profile_schema`，最后用 `GET /profile_schemas/{id}/user_profile?user_id=xxx` 获取结果。
5. **SDK 快速接入**：推荐使用 `agentscope-runtime`，各接口均有对应工具类（如 `AddMemory`, `SearchMemory`, `GetUserProfile`），封装了 endpoint、鉴权与序列化逻辑。

## 限制和注意事项

- **限流策略**：阿里云账号级别总计 3000 QPM；`/add` 接口限 120 QPM，`/memory_nodes/search` 限 300 QPM。超限返回 HTTP 429，需按指数退避（1s/2s/4s）重试 —— 具体规则见 [限流说明](raw/application-user-guide/agent-context/memory-library-overview/integration-overview/limits.md)。
- **商业化时间点**：所有 `Add` 和 `Search` 调用自 **2026 年 8 月 20 日 10:00（北京时间）** 起正式计费，区分 `pro` 与 `lite` 版本，影响抽取质量与搜索能力 —— 详见 [计费说明](raw/application-user-guide/agent-billing/billing.md)。
- **数据持久性**：当前生成的记忆片段与用户画像无自动失效机制，长期有效；但软删除（`status="delete"`）的记忆节点仍可被 `GetMemoryNode` 查询到。
- **安全要求**：API Key 具有账号级权限，严禁硬编码或提交至公开仓库；建议为不同应用分配独立 Key 并定期轮转。
- **错误处理**：所有响应均含 `request_id`，排查问题时必须提供该字段；常见错误码包括 400（参数错误）、401（鉴权失败）、403（权限不足）、404（ID 不存在）、429（限流）和 500（服务异常）—— 错误详情参见 [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)
- [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
- [记忆管理](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)
- [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
- [查询记忆节点](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-memory-node.md)
- [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)


