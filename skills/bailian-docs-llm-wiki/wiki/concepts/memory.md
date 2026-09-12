# 记忆管理

记忆管理是百炼平台提供的统一状态持久化与上下文复用能力，用于在多轮交互中跨请求、跨会话地存储、检索和关联用户或应用相关的语义化信息。它既支持长期结构化记忆（如用户画像、历史订单），也支持短期会话上下文（如对话历史摘要），是构建具备“认知连续性”的智能体与 LLM 应用的核心基础设施。

## 在百炼平台的不同场景中，这个概念如何使用

- **记忆库（Memory Library）**：作为独立的长期记忆服务，面向开发者提供 `upsert`（写入/覆盖）和 `search`（语义+关键词混合检索）两个原子操作。适用于客服助手、个性化推荐等需跨会话复用用户偏好的场景；数据按 workspace 隔离，不支持跨空间共享。

- **Managed Agents**：通过 `session_id` 自动维护会话级短期记忆，将每轮工具调用结果、中间推理步骤及用户反馈隐式沉淀为上下文向量，供后续 step 检索使用。该层记忆由平台托管，开发者无需显式调用 memory API，但需传入 `session_id` 以启用状态保持。

- **LLM 应用（Application）**：在 `llm-application` 调用中，`session_id` 参数触发平台自动注入最近 N 轮对话历史（含 system/user/assistant 消息），形成轻量级会话记忆；若需更丰富上下文（如用户档案、业务规则），需主动集成记忆库 SDK，在 `input` 中拼接 `memory.search()` 结果。

- **RAG 与 Use Cases**：在 RAG 场景中，“记忆”常与“知识库”协同——知识库承载静态领域知识（如产品文档），而记忆库承载动态用户上下文（如“上一轮我问过退货政策，现在想查物流”）。二者可通过 `metadata` 字段（如 `{"user_id": "u123", "intent": "return"}`）联合过滤，实现个性化检索增强。

- **低代码工作流**：在可视化编排中，「记忆节点」提供拖拽式写入/检索能力，支持绑定变量（如 `${user.profile}` 写入、`${query}` 检索），可与条件分支、循环等节点组合，快速构建带状态的业务流程（如多步表单填写、导购决策树）。

## 关键参数和配置

| 参数名 | 类型 | 说明 | 使用位置 |
|--------|------|------|----------|
| `session_id` | string | 会话唯一标识符，启用上下文隔离与状态保持的必需参数；未提供则生成临时 session，不持久化 | Managed Agents、LLM Application、低代码工作流 |
| `memory_id` | string | 记忆条目唯一 ID，为空时由系统生成 UUIDv4；建议业务侧自定义（如 `user:{id}:profile`）便于精准更新与删除 | Memory Library（upsert/search） |
| `content` | string | 原始文本内容，最大 8192 字符；长文本（≥512 字符）且 `enable_auto_summary: true` 时，平台自动生成不可编辑摘要 | Memory Library |
| `metadata` | object | 键值对标签（≤10 对），用于检索过滤（如 `{"user_id": "u123", "category": "billing"}`）；是连接记忆与业务逻辑的关键桥梁 | Memory Library、Managed Agents（部分 metadata 由平台自动注入） |
| `top_k` | integer | 检索返回条数，默认 10，上限 50；RAG 场景建议设为 3–5，平衡精度与 token 开销 | Memory Library search、RAG 配置 |
| `enable_auto_summary` | boolean | 是否启用自动摘要（仅对 ≥512 字符 content 生效）；摘要结果不可编辑，仅用于检索加速 | Memory Library upsert |

> **注意**：`embedding_model` 参数已废弃，所有 embedding 统一使用 `text-embedding-v3`，传入该字段无效；`session_id` 是跨组件记忆一致性的关键，务必在 Agent、Application、Memory Library 调用中保持相同值以实现上下文贯通。

## 面向开发者，简洁实用

- ✅ **优先用 `session_id`**：只要需要多轮状态，就显式传入稳定 `session_id`（如用户 ID + 会话类型哈希），让平台自动管理短期上下文。
- ✅ **长期记忆走 Memory Library**：用户偏好、历史行为、业务实体等需跨会话复用的数据，用 `memory.upsert()` 写入，`memory.search()` 检索，配合 `metadata` 过滤。
- ✅ **组合使用更强大**：例如在 Agent 中，先用 `memory.search(metadata={"user_id": "u123"})` 获取用户画像，再将其注入 system [prompt](../guides/prompt.md)，最后调用工具完成个性化操作。
- ⚠️ **避免常见陷阱**：
  - 不要依赖未传 `session_id` 的“默认会话”，其状态无法持久；
  - 删除记忆必须按 `memory_id` 逐条调用 `DELETE /v1/memories/{id}`，不支持批量删；
  - 写入后 2–5 秒才可检索（最终一致性），高并发场景需加重试或降级逻辑；
  - 单 workspace 默认配额 10 万条，超限时需清理旧记忆或申请扩容。

- 🛠️ **调试建议**：开启 `enable_tracing`（Managed Agents）或使用 SDK 的 `debug: true` 选项，查看 memory 检索耗时、匹配分数及原始 content，快速定位召回不准问题。

## 关联主题页

- [memory library overview](../guides/memory-library-overview.md)
- [managed agents](../guides/managed-agents.md)
- [llm application](../guides/llm-application.md)
- [application use cases](../guides/application-use-cases.md)
- [use cases](../guides/use-cases.md)


