# 长期记忆

长期记忆（Long Term Memory）是百炼平台提供的结构化、可检索、跨会话持久化的记忆管理服务，用于将用户交互、业务事件或自定义内容沉淀为事实（`observation`）、技能（`skill`）和用户画像（`user_profile`）三类语义化记忆节点，支撑智能体具备持续学习与上下文感知能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **Agent 开发（Sandbox/Flow Agent）**：开发者可在 `main.py` 或 Flow 节点中主动调用长期记忆 API，将关键对话片段、用户偏好、操作结果写入记忆库；后续请求可通过 `context.memory.session_id` 自动加载关联记忆，实现多轮对话状态延续与个性化响应。  
- **Agent 上下文（`agent context`）**：当请求中携带 `context.memory.session_id` 时，平台自动从长期记忆中检索匹配的 `observation` 和 `skill` 类型节点，并按相关性注入 prompt，无需手动拼接——该机制是 RAG 之外另一条核心上下文增强通路。  
- **用户画像构建**：配合预定义的 `profile_schema`，长期记忆可从对话中自动抽取结构化用户属性（如“职业=产品经理”“偏好=简洁回复”），供后续决策、推荐或风控策略调用。  
- **技能沉淀与复用**：通过写入 `skill` 类型记忆（含 `skill_name`、`skill_description`、`skill_tags`），团队可将高频操作流程（如“重置密码五步法”）沉淀为可被 LLM 理解与调用的原子能力，降低 Prompt 工程维护成本。  
- **应用治理与可观测性**：所有长期记忆的写入/检索行为均被记录在全链路 Trace 中（`memory.write` / `memory.search` 事件），支持在「应用观测」中分析记忆使用频次、命中率与耗时，辅助优化记忆策略。

## 关键参数和配置

| 参数 | 说明 | 开发建议 |
|------|------|----------|
| `user_id` | **必填**。子用户唯一标识，用于严格隔离不同用户的记忆数据。 | 建议与业务系统用户 ID 对齐，避免使用临时 UUID。 |
| `project_id` 或 `project_ids` | **推荐设置**。项目级逻辑分组标识（最多 5 个），用于区分同一用户在不同业务场景下的记忆（如“客服项目” vs “营销项目”）。 | 若不传，记忆将默认归属全局项目，不利于后期清理与权限管控。 |
| `profile_schema` | **仅需画像时必填**。指定画像模板 ID，触发结构化用户属性抽取。未传则跳过画像生成。 | 模板需提前在控制台创建并发布；建议为每个业务线定义专属 schema。 |
| `plan_version` | **检索时显式指定**。`"pro"` 启用 `min_score` 过滤、Rerank 等高级能力；`"lite"` 仅基础向量搜索。默认为 `"pro"`，但 `search` 接口需显式传入才生效。 | 生产环境务必设为 `"pro"` 并配合 `min_score: 0.3`（典型阈值）过滤低质结果。 |
| `memory_types` | **检索时可选**。限制返回的记忆类型，默认 `["observation"]`；如需技能+事实联合检索，设为 `["observation", "skill"]`。 | 避免无意义全量检索，明确业务意图后精准限定类型。 |
| `extract_mode`（写入时） | 取值 `"efficient"`（毫秒级延迟，适合实时反馈）或 `"intelligent"`（高精度抽取，需异步）。同步接口在 `"intelligent"` 下**可能超时**，必须改用 `/add-async`。 | 实时场景（如聊天输入框即时记忆）用 `"efficient"`；后台批量处理、画像/技能联合抽取用 `"intelligent"` + 异步。 |

## 面向开发者，简洁实用

- ✅ **写入优先选异步**：除极简场景外，一律使用 `/add-async` 写入，立即获得 `event_id`，再轮询 `/events/{event_id}` 获取结果（含抽取详情与错误码）。  
- ✅ **检索必带过滤**：`search` 请求务必指定 `plan_version: "pro"` + `min_score`（建议 0.25–0.4），避免噪声干扰。  
- ✅ **画像需两步走**：先调用 `/profile_schemas` 创建模板 → 写入时传 `profile_schema` → 最后调用 `/profile_schemas/{id}/user_profile?user_id=xxx` 获取结构化结果。  
- ⚠️ **无自动过期**：长期记忆**永不过期**，请自行设计清理策略（如按 `created_at` 定期调用 `/memory_nodes?user_id=xxx&project_id=yyy` 分页删除）。  
- ⚠️ **限流要兜底**：`/add` 接口限 120 QPM，`/search` 限 300 QPM；超时（HTTP 429）需实现指数退避重试（1s → 2s → 4s）。  
- 🚀 **调试技巧**：在请求头加 `X-Debug-Context: true`，响应中 `debug.context_summary` 会显示本次加载了哪些记忆节点及其来源。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [agent development](../guides/agent-development.md)
- [agent context](../guides/agent-context.md)
- [agent governance](../guides/agent-governance.md)
- [application use cases](../guides/application-use-cases.md)


