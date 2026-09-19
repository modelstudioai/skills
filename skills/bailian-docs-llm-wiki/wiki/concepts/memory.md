# 长期记忆

长期记忆是百炼平台为大模型应用提供的**跨会话、结构化、语义可检索的持久化记忆能力**，通过自动提取对话中的关键事实与用户属性，并以 `user_id` 为隔离单元进行存储与召回，使智能体具备持续理解用户偏好、历史行为和上下文状态的能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）场景**：在 Managed Agents 中，长期记忆以「记忆库（Memory Store）」形式挂载为沙箱内的持久化文件树，智能体可通过 `read`/`write` 工具直接读写；同时，其对话内容可自动触发记忆库的「事实记忆」与「用户画像」双路提取（需配置规则），实现自然语言交互与结构化记忆的协同演进。  
- **工作流（Workflow）与 LLM 应用场景**：通过 `modelstudio-memory-for-openclaw` 等插件接入，支持 `autoCapture`（对话结束自动提取）与 `autoRecall`（对话开始前自动注入），零侵入式嵌入任意节点流程；记忆检索结果可作为变量直接注入 Prompt 或传递给下游工具。  
- **API 直接集成场景**：开发者调用统一的长期记忆 RESTful API（`/add`, `/memory_nodes/search`, `/profile_schemas/...`），自主控制记忆写入时机、内容来源（`messages` 或 `custom_content`）与检索策略，适用于高代码应用、自定义调度器或第三方系统对接。  
- **RAG 增强场景**：长期记忆与知识库（RAG）正交互补——知识库面向静态文档/外部数据，长期记忆聚焦动态用户事实与个性化画像，二者可并行检索、加权融合后注入大模型上下文，提升个性化与时效性。  

> ✅ 关键区分：长期记忆 ≠ 会话上下文（Session Context），后者仅存活于单次请求链路；也 ≠ 知识库（Knowledge Base），后者不绑定 `user_id`、无用户粒度隔离、不支持语义化事实抽取。

## 关键参数和配置

| 参数 | 说明 | 推荐值/约束 | 备注 |
|------|------|-------------|------|
| `user_id` | 记忆归属唯一标识，所有读写操作的作用域 | 必填，≤64 字符，建议业务侧稳定生成（如登录态 ID） | **不可省略**，缺失将导致写入失败或跨用户污染 |
| `plan_version` | 控制记忆质量与成本的核心策略参数 | `Pro`（默认，启用 Rerank/高质量抽取）或 `Lite`（跳过 Rerank，低延迟） | `AddMemory` 的 `plan_version` 由记忆规则决定；`SearchMemory` 可独立指定（不传默认 `Pro`） |
| `top_k` | 检索返回的最大记忆条数 | `1–100`，默认 `10`；高频轻量场景建议 `3–5`，精准问答建议 `10–20` | 影响 [Token](token.md) 成本与响应延迟，需权衡精度与开销 |
| `min_score` | 相似度阈值，过滤低相关结果 | `0.0–1.0`，建议 `0.5–0.7`；低于 `0.4` 易引入噪声，高于 `0.8` 可能漏召 | 与 `plan_version` 联动：`Pro` 版本得分更可信，可设更高阈值 |
| `profile_schema_id` | 触发用户画像提取的模板 ID | Add 时不传则**不提取画像**；Get 时必须传入 | 用户画像需先调用 `CreateProfileSchema` 创建模板，再在 `AddMemory` 中显式引用 |

## 面向开发者，简洁实用

- **快速验证三步走**：  
  1. `POST /add` 写入：传 `user_id` + `messages`（含至少一条用户陈述，如“我叫张三，30岁，喜欢 hiking”）；  
  2. `GET /profile_schemas/{id}/user_profile?user_id=xxx` 查询画像（等待 ≥3 秒再查）；  
  3. `POST /memory_nodes/search` 检索：传 `user_id` + 当前 `messages`，观察召回的事实记忆。  

- **生产就绪要点**：  
  - ✅ **必配 `user_id`**：所有接口均以此隔离，切勿用随机 UUID 或空字符串；  
  - ✅ **画像提取需显式声明**：`AddMemory` 请求中必须带 `profile_schema_id`，否则仅存事实记忆；  
  - ✅ **异步等待画像**：调用 `AddMemory` 后，`GetUserProfile` 需延迟 ≥3 秒或轮询重试；  
  - ✅ **限流兜底**：账号级总限流 3000 QPM（`Add` ≤120 QPM，`Search` ≤300 QPM），HTTP `429` 错误需指数退避（1s/2s/4s）；  
  - ❌ **禁止硬编码 API Key**：务必通过环境变量 `DASHSCOPE_API_KEY` 注入，严禁提交至代码仓库；  
  - ❌ **删除不可逆**：`DELETE /memory_nodes/{id}` 或 `DELETE /profile_schemas/{id}` 操作立即生效且无法恢复。  

- **调试利器**：所有响应头含 `X-Request-ID`，排查问题时请务必提供该字段。

## 关联主题页

- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)
- [managed agents](../guides/managed-agents.md)
- [llm application](../guides/llm-application.md)
- [application support](../guides/application-support.md)


