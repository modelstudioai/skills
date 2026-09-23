# 长期记忆

长期记忆（Long Term Memory, LTM）是百炼平台提供的结构化、跨会话持久化记忆管理服务，用于突破大模型单次对话的上下文窗口限制，实现用户状态、行为模式、关键事件和结构化属性的自动沉淀与语义化召回。它不是简单的缓存或日志存储，而是通过模型驱动的信息抽取、向量化索引与策略化检索，构建可演进、可治理、可复用的用户认知基座。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）应用**：在 Agent 1.0/2.0 中，长期记忆作为“隐式上下文增强层”自动启用（需开通记忆库并配置 `autoRecall=true`）。系统在每次推理前自动调用 `SearchMemory`，将匹配的事实记忆（如“用户过敏花生”）和用户画像（如“职业=医生，偏好=简洁回复”）注入 [prompt](../guides/prompt.md)，无需开发者手动拼接上下文。
  
- **工作流（Workflow）系统**：通过「长期记忆插件」嵌入任意节点（如智能体群组、大模型节点前），支持 `autoCapture`（自动从输入消息提取记忆）与 `autoRecall`（自动检索并注入当前上下文），实现记忆能力与业务逻辑解耦。适用于客服工单流转、销售跟进等需跨步骤维持用户意图的场景。

- **高代码应用（Serverless/K8s）**：开发者直接调用记忆库 REST API（如 `/add-async`、`/memory_nodes/search`），将记忆写入与检索深度集成至自定义业务逻辑中。例如，在订单履约服务中，将用户历史退换货原因作为 `observation` 类型事实记忆写入，并在新订单咨询时优先召回相似案例辅助决策。

- **Managed Agents 托管服务**：通过 `context_id` 参数关联预存的长期记忆快照（由记忆库生成），使托管智能体在无 session 状态下仍能复用用户长期特征，适用于异步任务、Webhook 回调等非连续交互场景。

- **RAG 增强场景**：与知识库检索正交协同——知识库解决“通用领域知识”，长期记忆解决“专属用户事实”。二者可并行检索后融合排序（如加权合并 score），显著提升个性化回答准确率（例如：“根据您的过往投诉记录（LTM）和《售后服务条例》（知识库），本次可全额退款”）。

## 关键参数和配置

| 参数 | 作用域 | 说明 | 推荐值 | 注意事项 |
|------|--------|------|--------|----------|
| `user_id` | 全局必填 | 记忆隔离主键，必须唯一标识终端用户（如手机号哈希、OpenID）。同一 `user_id` 下所有记忆自动聚合、跨应用共享。 | 业务侧稳定 ID，避免使用临时 token | 不传或为空将导致写入失败；不同 `user_id` 的记忆完全隔离，不可交叉检索 |
| `top_k` | `SearchMemory` 请求体 | 检索返回的最大记忆条数 | `5–10`（平衡效果与 token 开销） | 超过 100 将被截断；值过大易引入噪声，建议结合业务场景压测确定 |
| `min_score` | `SearchMemory`（仅 `plan_version=pro` 生效） | 相似度阈值（0.0–1.0），低于此值的记忆不返回 | `0.5–0.7`（查准率优先）或 `0.3–0.5`（查全率优先） | `Lite` 版本忽略该参数；默认 `0.3`，生产环境务必显式设置以规避低质召回 |
| `plan_version` | `SearchMemory` / `CreateProfileSchema` / `AddMemoryAsync` 路径 | 控制策略版本：`pro` 启用高级重排（Rerank）与高精度抽取；`lite` 为轻量级低延迟版本 | `pro`（默认，推荐） | `AddMemory` 同步接口**不支持**该参数；切换版本仅影响新写入/新检索行为，已存记忆不受影响 |
| `profile_schema` | `AddMemoryAsync` 请求体 | 用户画像模板 ID，指定结构化属性提取规则（如 `schema_abc123`） | 模板创建后获取的实际 ID | 缺失则跳过画像抽取；一个 `user_id` 可绑定多个 schema，但单次调用仅支持一个 |
| `memory_library_id` | 全局可选 | 自定义记忆库 ID，用于多租户、多业务线隔离 | 由控制台创建后分配 | 不传则使用账号默认记忆库；默认库不可删除，仅可编辑元信息 |

> ⚠️ 重要提示：`extract_mode`（如 `profile_only`）仅在 `AddMemoryAsync` 中有效；`AddMemory` 同步接口不支持该参数，也不支持 `plan_version`。所有参数均区分大小写，且 `user_id` 是强制维度，缺失将返回 `400` 错误。

## 面向开发者，简洁实用

- **快速上手三步走**：  
  1. 控制台开通记忆库 → 获取 `DASHSCOPE_API_KEY`；  
  2. 调用 `POST /add-async` 写入对话（带 `user_id` + `messages`），若需画像同步传 `profile_schema`；  
  3. 调用 `POST /memory_nodes/search` 检索（带 `user_id` + 当前 `messages`），将 `result.memory_nodes` 注入 [prompt](../guides/prompt.md) 即可。

- **调试黄金法则**：  
  - 在控制台「记忆检索」标签页实时调整 `top_k`/`min_score`，观察召回内容变化；  
  - 使用 `ListMemory?user_id=xxx` 查看已写入记忆，确认抽取是否符合预期；  
  - 用户画像首次查询可能为空 → 实现指数退避重试（建议 1s/2s/4s 三次）。

- **避坑指南**：  
  - ❌ 不要混用旧版术语（如 “MemoryNode”、“记忆变量”），统一使用 **事实记忆**（动态事件）和 **用户画像**（结构化属性）；  
  - ❌ 不要在 `AddMemory` 中传 `plan_version` 或 `profile_schema`（无效且可能报错）；  
  - ✅ 异步写入（`/add-async`）是生产环境首选——支持 [skill](../guides/skill.md) + profile 混合提取，吞吐更高；  
  - ✅ 记忆库 QPM 限流严格（`Add` ≤120 QPM，`Search` ≤300 QPM），高频场景务必加本地缓存或批量聚合请求。

## 关联主题页

- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)
- [llm application](../guides/llm-application.md)
- [managed agents](../guides/managed-agents.md)
- [application support](../guides/application-support.md)


