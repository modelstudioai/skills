# 长期记忆

长期记忆（Long Term Memory）是百炼平台提供的**结构化、用户级、可检索的持久化记忆服务**，用于跨会话、跨请求地存储和复用关键业务事实与用户画像信息。它独立于对话 session 生命周期，以 `user_id` 为隔离核心，支持语义检索、异步抽取与模板驱动的结构化建模。

## 在百炼平台的不同场景中，这个概念如何使用

- **Agent 运行时上下文注入**：在 `agent context` 中配置 `"memory_type": "user"` 并传入 `user_id`，平台将自动从长期记忆中检索匹配该用户的最新事实节点（`observation`/`skill`）和画像数据（`profile`），注入到当前推理上下文中，提升响应一致性与个性化能力。
  
- **智能体应用开发（Flow Agent）**：通过组件类 API（如 `/add-async`、`/memory_nodes/search`）直接管理记忆生命周期；旧版 `Memory`/`MemoryNode` 接口已标记为遗留，新项目应统一使用 `long-term-memory-new` 体系。

- **RAG 增强与行为建模**：长期记忆中的 `skill` 类型记忆可作为可复用的工具行为（如“用户习惯用语音下单”“偏好夜间客服”），被 Agent 主动调用或由 RAG 检索结果触发；`observation` 则沉淀关键事件（如“用户投诉物流延迟”），支撑后续风险识别与服务干预。

- **治理与可观测性闭环**：记忆写入与检索行为自动上报至 `Agent Governance` 的 Trace 数据流，可用于分析记忆命中率、画像更新时效性、抽取准确率等质量指标，支撑评测集构建与优化迭代。

> ⚠️ 注意：同步 `/add` 接口仅适用于 `extract_scene=efficient` 场景；若需 `intelligent` 抽取（含技能识别、多轮意图聚合、深度画像生成），必须使用 `/add-async` + 轮询事件状态，否则可能超时失败。

## 关键参数和配置

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `user_id` | Body / Query | string | ✅ | 记忆隔离主键，所有读写操作必需；需符合正则 `^[a-zA-Z0-9_-]{4,64}$` |
| `extract_scene` | Body | string | ❌ | `efficient`（默认，低延迟）或 `intelligent`（高精度，需异步）；决定抽取能力边界 |
| `profile_schema` | Body | string | ❌ | 指定已创建的用户画像模板 ID，传入后触发结构化属性抽取（如年龄、职业） |
| `plan_version` | Body / Query | string | ❌ | `pro`（默认，支持 `min_score` 过滤、高级 Rerank、深度画像）或 `lite`（基础能力） |
| `top_k` / `min_score` | Body | integer / number | ❌ | 仅 `SearchMemory` 接口有效：`top_k` 控制召回数量（默认 10）；`min_score` 仅 `plan_version=pro` 时生效（默认 0.3） |
| `project_ids` | Body | array of string | ❌ | 最多 5 个，用于二级业务隔离（如区分 App/小程序/客服系统）；与 `project_id` 互斥 |

## 面向开发者，简洁实用

- ✅ **首选异步写入**：批量导入、含图片/多轮消息、需 `intelligent` 抽取时，务必用 `/add-async` → 获取 `event_id` → 轮询 `/events/{event_id}` 直到 `status=success`。
- ✅ **画像模板先行**：先调用 `/profile_schemas` 创建 schema，再在 `AddMemory` 请求中传 `profile_schema`，否则画像抽取不生效。
- ✅ **检索即用**：`/memory_nodes/search` 传 `user_id` + 查询文本（`messages`），无需预加载或初始化，返回结构化 JSON 节点数组。
- ❌ **勿混用旧接口**：`flow-agent-api` 中的 `CreateMemory` 等旧版记忆接口已废弃，新项目禁止使用。
- 🔑 **鉴权与 Endpoint**：使用业务空间专属域名（`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory`）+ `DASHSCOPE_API_KEY`，非通用 DashScope 网关地址。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [agent context](../guides/agent-context.md)
- [flow agent api](../api/flow-agent-api.md)
- [agent governance](../guides/agent-governance.md)


