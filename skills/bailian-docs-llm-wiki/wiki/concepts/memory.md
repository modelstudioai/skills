# 记忆管理

记忆管理是百炼平台提供的统一、结构化、跨会话的长期记忆能力，用于在智能体与工作流中持续沉淀和复用用户事实性信息（如临时意图、事件承诺）与稳定属性（如身份、偏好），实现上下文感知的个性化交互。它不绑定特定大模型，而是作为独立中间件，通过语义向量化、规则驱动提取与精准检索，将对话历史自动转化为可查询、可更新、可编排的记忆资产。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）应用**：通过 `application call` 接口的 `memory_id` 参数显式关联记忆库，或在 Agent 2.0 配置中启用「长期记忆」开关，系统自动在每次调用前后执行 `autoCapture`（写入）与 `autoRecall`（注入）。记忆内容经语义检索后，以结构化片段形式注入模型上下文，无需手动拼接提示词。
  
- **OpenClaw 工作流**：通过「长期记忆[插件](plugin.md)」节点接入，支持零代码启用 `autoCapture`/`autoRecall` 生命周期钩子。[插件](plugin.md)自动识别消息中的关键事实（如“明天下午三点开会”）并提取为事实记忆；若配置了 `profile_schema`，则同步触发用户画像字段（如“会议常驻地点”）的结构化填充。

- **Memory Library（记忆库）原生集成**：开发者可直接调用 RESTful API（如 `POST /add`, `POST /memory_nodes/search`）进行全生命周期控制。适用于需精细调度记忆行为的场景，例如：在 RAG 检索前预加载用户历史偏好、在工具调用后主动归档执行结果、或在会话结束时批量清理临时记忆。

- **Managed Agents 托管服务**：通过 `context_id` 关联预注册的上下文配置，底层自动绑定记忆库实例。平台在会话状态持久化过程中，将 `session_id` 与 `user_id` 映射，确保多轮对话中记忆按用户隔离、跨会话延续。

- **高代码应用（Python）**：使用 `agentscope_runtime.tools.modelstudio_memory` 封装类（如 `AddMemory`, `SearchMemory`），在自定义逻辑中同步写入业务事件（如订单创建、投诉提交）或动态检索用户历史行为（如“最近三次退货原因”），实现记忆与业务流程深度耦合。

## 关键参数和配置

| 参数 | 说明 | 推荐值 | 注意事项 |
|------|------|--------|----------|
| `user_id` | 记忆归属的唯一实体标识，用于跨会话、跨应用隔离 | 业务系统用户 ID（如 `uid_123456`） | 必填；长度 ≤64 字符；避免使用会话 ID 或临时 token |
| `plan_version` | 控制记忆处理精度与性能：`Pro` 启用重排（Rerank）、高精度提取与查询改写；`Lite` 仅基础向量检索，延迟更低 | `Pro`（默认，推荐调试与生产）；`Lite`（高吞吐低延迟场景） | 大小写不敏感，但建议统一用大写；`AddMemory` 和 `SearchMemory` 可独立设置 |
| `min_score` | 检索相似度阈值，低于此值的结果被过滤 | `0.5–0.7`（生产环境）；`0.3`（API 默认，调试时可降低） | 过低易引入噪声；过高可能导致漏召；建议结合业务场景 A/B 测试 |
| `top_k` | 单次检索返回的最大记忆条数 | `5`（OpenClaw [插件](plugin.md)默认）；`10`（API 示例）；最大 `100` | 值越大，上下文越丰富但 token 开销越高；需与模型上下文窗口协同配置 |
| `profile_schema_id` | 用户画像模板 ID，显式传入才触发画像提取 | 由控制台创建后获取的字符串 ID | 不传则仅生成事实记忆；画像提取为异步，需等待约 3 秒再调用 `GetUserProfile` |
| `memory_library_id` | 指定目标记忆库（用于业务隔离，如电商/客服分库） | 自定义库 ID；不传则使用账号默认库 | 默认库不可删除；自定义库支持最多 50 条事实规则 + 50 条画像规则 |

> ⚠️ **重要限制**：  
> - 账号级总 QPM 限流 3000；`AddMemory` 单独限 120 QPM，`SearchMemory` 限 300 QPM；超限返回 `429`，需实现指数退避重试（1s → 2s → 4s）。  
> - 用户画像提取为异步，`AddMemory` 返回后约 3 秒 `GetUserProfile` 才可获取结果。  
> - 删除记忆或画像模板为**不可逆操作**，数据无法恢复。  

## 面向开发者，简洁实用

- ✅ **快速起步**：只需 `user_id` + `messages` 调用 `AddMemory`，系统自动提取事实记忆；加 `profile_schema_id` 即激活画像。  
- ✅ **即插即用**：OpenClaw 插件、Agent 2.0 内置开关、Managed Agents `context_id` 均支持零配置启用，无需修改业务逻辑。  
- ✅ **精准可控**：`min_score` 和 `top_k` 直接调控召回质量与成本；`plan_version` 在精度与延迟间灵活权衡。  
- ✅ **生产就绪**：支持自定义记忆库隔离、规则过期策略（7/30/180天/永不过期）、完整 API 与控制台可视化运维。  
- ❌ **避免踩坑**：勿使用已废弃的“记忆变量”“MemoryNode”等旧术语；所有新开发请严格使用「事实记忆」与「用户画像」两类标准概念。

## 关联主题页

- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)
- [application call](../api/application-call.md)
- [managed agents](../guides/managed-agents.md)
- [llm application](../guides/llm-application.md)


