# agent context

`agent context` 是百炼平台中用于增强 Agent 推理能力的上下文注入机制，支持将外部知识、历史记忆、结构化数据源等动态注入到 LLM 的 prompt 中。它不依赖模型微调，而是通过运行时上下文拼接与策略编排实现上下文感知的智能体行为。该机制是构建生产级 RAG、多轮对话记忆、跨系统数据联动等场景的核心基础设施。

## 支持的模型与功能

- **模型支持**：当前仅 `qwen-plus`、`qwen-max` 和 `qwen-turbo`（v202408 及之后版本）原生支持 `agent context` 的完整上下文解析与优先级调度；其他模型（如 `qwen-1.5-7b-chat`）仅支持基础 context 字段透传，不触发自动检索或记忆融合逻辑。  
- **核心功能**：  
  - RAG 检索结果自动注入（基于 [RAG](../../raw/application-user-guide/agent-context/knowledge-base.md) 配置）  
  - 对话级 Memory 自动加载与更新（详见 [Memory](../../raw/application-user-guide/agent-context/memory-library-overview.md)）  
  - 外部系统 Connector 数据实时拉取（参见 [Connector](../../raw/application-user-guide/agent-context/overview.md)）  
  - 结构化文档解析与语义切片（通过 ParseX 引擎，见 [ParseX](../../raw/application-user-guide/agent-context/getting-started-overview.md)）

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `context` | object | 否 | 顶层上下文容器，结构为 `{ knowledge_base: [...], memory: {...}, connector: [...] }` |
| `context.knowledge_base.ids` | string[] | 否 | 指定知识库 ID 列表，触发对应 RAG 检索（需提前在控制台启用） |
| `context.memory.session_id` | string | 否 | 会话级记忆标识符；若未提供，则使用请求级 `trace_id` 作为 fallback |
| `context.connector.ids` | string[] | 否 | Connector 实例 ID 列表，按声明顺序执行同步调用 |

> **注意**：`context.memory.ttl_seconds` 在 [Memory](../../raw/application-user-guide/agent-context/memory-library-overview.md) 文档中标注为支持，但实测 v202409 版本 SDK 中该字段被忽略，实际 TTL 由服务端统一配置（默认 7200 秒），请勿在请求中设置。

## 使用方式

1. 在调用 `/v1/chat/completions` 或 `/v1/agents/run` 接口时，在 `messages` 数组前添加 `context` 字段（非 `messages` 内容）；  
2. 确保所引用的 `knowledge_base.id`、`connector.id` 已在控制台完成授权与发布；  
3. 若需调试上下文注入效果，可在请求头添加 `X-Debug-Context: true`，响应中将返回 `debug.context_summary` 字段说明各模块是否命中及 token 占用。

## 限制和注意事项

- 单次请求总 context token 不得超过模型 `max_context_length` 的 60%（例如 `qwen-max` 为 32768，则 context 上限约 19660 tokens），超限将触发截断并返回警告 `context_truncated: true`；  
- `knowledge_base` 与 `connector` 并发调用上限为 3 个实例，超出部分将排队等待（最大等待 5s，超时则跳过）；  
- Memory 模块仅对 `role: "user"` 和 `role: "assistant"` 的 message 生效，`role: "system"` 中的 context 不参与记忆写入；  
- 所有 context 注入内容均在 LLM 输入前完成拼接，**不经过模型内部 tokenizer 重分词**，因此需确保原始文本已做基础清洗（如去除不可见控制字符）。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


