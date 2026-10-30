# agent context

agent context 是 Agent 执行过程中用于支撑决策与响应的关键信息集合，包括知识库检索结果（RAG）、历史对话记忆（Memory）、外部系统连接器（Connector）及结构化内容解析（ParseX）等模块。它决定了 Agent 能“知道什么”和“记住什么”，直接影响响应准确性与上下文连贯性。该机制通过统一上下文管理框架实现多源信息的动态注入与生命周期控制。

## 支持的模型/功能

当前 agent context 仅在 `qwen-plus`、`qwen-max` 和 `qwen-turbo` 等 Qwen 系列大模型上完整支持；其他模型（如 `qwen-14b-chat`）虽可接收 context 字段，但不保证对 RAG 或 Memory 的语义理解与协同调用。核心功能模块包括：
- **RAG**：从知识库实时检索并注入相关文档片段，详见 [Agent 上下文](../../raw/application-user-guide/agent-context.md)；
- **Memory**：维护跨轮次对话状态，支持短期会话记忆与长期用户画像缓存，其行为受 `memory_type` 参数约束；
- **Connector**：对接 CRM、数据库等外部系统，需在 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 中配置白名单 endpoint；
- **ParseX**：对上传文件（PDF/Excel/Word）进行结构化解析并注入上下文，能力依赖于 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 中声明的 `parsex_enabled: true`。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `context.rag` | object | 否 | 启用 RAG 时必填，含 `knowledge_base_id` 和 `top_k`（默认 3）；参见 [Agent 上下文](../../raw/application-user-guide/agent-context.md) |
| `context.memory` | object | 否 | 控制记忆读写策略，`read_only: true` 禁止更新记忆，`ttl_seconds` 设置过期时间（最小 60） |
| `context.connector` | array | 否 | 每项为 `{id: string, params: object}`，connector id 需预先在平台注册 |
| `context.parsex` | object | 否 | 含 `file_ids: string[]` 和 `chunk_size: number`（默认 512），仅当 `parsex_enabled` 为 true 时生效 |

> **注意**：原始文档中 `context.parsex.chunk_size` 标注范围为 “128–1024”，但实测超过 768 将触发截断警告；请以 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 中最新运行时日志为准。

## 使用方式

1. 在调用 `/v1/agents/{agent_id}/chat` 接口时，将 context 对象作为请求体顶层字段传入（非 `messages` 内部）；
2. RAG 与 Memory 可同时启用，但若 `context.rag.knowledge_base_id` 与 `context.memory.read_only: false` 共存，Memory 会自动将本轮 RAG 结果摘要写入[长期记忆](../concepts/long-term-memory.md)（需开启 `auto_memory_summary`）；
3. Connector 调用结果默认不透出给 LLM，如需注入上下文，须显式设置 `inject_to_context: true` —— 此行为未在 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 中明确说明，属隐式约定。

## 限制和注意事项

- 单次请求总 context 大小（含所有模块序列化后）不得超过 128 KB，超限将返回 `400 Bad Request`；
- Memory 模块在流式响应（`stream: true`）下仅支持读取，写入操作必须在非流式调用中完成；
- RAG 检索结果按 `score` 降序排列，但 LLM 实际可见顺序取决于 `context.rag.reorder` 参数（默认 `false`，即保持原始排序）；
- ParseX 解析后的文本不参与 token 计费，但计入上下文长度限制。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


