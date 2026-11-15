# 长期记忆

长期记忆（Long Term Memory, LTM）是百炼平台提供的**结构化、持久化、可检索的跨会话知识管理服务**，用于在智能体应用中持续积累和复用事实信息、用户特征与自动化技能，支撑上下文延续、个性化响应与行为演化能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **Managed Agents 场景**：作为可选但关键的组件，通过 `memory_store_id` 显式绑定到 Agent 实例。Memory Store 为托管 Agent 提供统一的记忆接入点，其底层由长期记忆（新）服务驱动；Agent 运行时自动将对话历史、工具调用结果等写入关联的 Memory Store，并在后续请求中按需注入上下文（受限于 32KB 会话内存上限）。

- **Flow Agent 场景**：支持两种记忆路径：
  - *旧版记忆（Legacy）*：通过 Flow Agent API 的 `/memory` 和 `/memory_nodes` 接口直接管理记忆体与片段，适用于存量应用迁移，但已标记为遗留方案；
  - *新版记忆（推荐）*：在 Flow 编排中调用 `bailian.memory.add_async()` 或 `bailian.memory.search()` 等 SDK 方法（底层对接 `/add-async` 和 `/memory_nodes/search`），实现与 Managed Agent 一致的结构化记忆能力。

- **Sandbox 场景**：开发者通过 `agentscope-runtime` SDK（如 `bailian.memory.add_async()`、`bailian.memory.search()`）直接集成长期记忆服务，完全自主控制写入时机、内容格式与检索策略，常用于构建需要精细记忆生命周期管理的复杂智能体（如客服知识沉淀、销售过程追踪）。

- **通用适用性**：所有场景均要求显式传入 `user_id` 实现记忆隔离；记忆内容默认**永久保留、无自动过期**，需开发者自行通过 `DELETE /memory_nodes/{id}` 或批量清理接口管理生命周期。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `user_id` | string | ✅ | 记忆归属的唯一用户标识，强制用于多租户隔离；不同 `user_id` 的记忆互不可见。 |
| `project_id` / `project_ids` | string / string[] | ⚠️（至少一者） | 指定记忆所属项目，决定抽取规则（如 `observation`/`skill`/`user_profile`）；`project_ids` 最多 5 个，与 `project_id` 互斥。 |
| `profile_schema` | string | ❌（仅画像场景） | 用户画像模板 ID，需配合 `messages` 字段触发结构化属性抽取（`custom_content` 不支持）。 |
| `plan_version` | string | ❌（默认 `lite`） | 可选 `lite`（基础能力）或 `pro`（启用 `min_score` 过滤、高级抽取）；非法值将报错。 |
| `top_k` | integer | ❌（默认 10） | 检索接口 `/memory_nodes/search` 返回的最大结果数。 |
| `min_score` | float | ❌（仅 `plan_version=pro` 生效） | 语义检索最低相似度阈值（0.0–1.0），低于此值的结果被过滤。 |

> **认证与端点**：  
> - Header：`Authorization: Bearer $DASHSCOPE_API_KEY`（API Key 必须属于目标业务空间）  
> - Endpoint：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory/`（`{WorkspaceId}` 从控制台「业务空间管理」获取）  
> - 环境变量建议：`MEMORY_SERVICE_ENDPOINT="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory"`（末尾无 `/`）

## 开发者提示

- ✅ **优先使用异步写入**：`/add-async` 是主推方式，避免同步 `/add` 在 `intelligent` 模式下的超时风险；轮询 `GET /events/{event_id}` 获取最终结果。
- ✅ **画像需预置模板**：必须先调用 `/profile_schemas` 创建模板，再在写入请求中传入 `profile_schema` 才能触发结构化抽取。
- ⚠️ **检索默认仅限 `observation`**：`/memory_nodes/search` 的 `memory_types` 默认为 `["observation"]`，如需检索 `skill` 或 `user_profile`，需显式指定。
- ⚠️ **注意限流**：全局限流 3000 QPM（账号级），其中 `/add` 接口限 120 QPM，`/search` 限 300 QPM；高并发场景请做好重试与降级。
- 🚫 **不支持跨业务空间访问**：`WorkspaceId` 与 `DASHSCOPE_API_KEY` 必须匹配同一业务空间。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [managed agents api](../api/managed-agents-api.md)
- [flow agent api](../api/flow-agent-api.md)
- [agent development](../guides/agent-development.md)


