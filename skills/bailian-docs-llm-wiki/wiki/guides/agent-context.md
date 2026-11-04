# agent context

`agent context` 是百炼平台中用于增强 Agent 推理能力的上下文注入机制，支持将外部知识、历史记忆、连接器配置等结构化信息动态注入到 LLM 的 prompt 中。它不改变模型本身，而是通过预处理阶段构建高质量上下文片段，提升 Agent 在复杂任务（如多跳问答、状态感知对话）中的准确性和一致性。该机制深度集成于百炼 Agent Runtime，开发者可通过声明式配置或 API 参数控制其行为。

## 支持的模型与功能

当前 `agent context` 仅对百炼平台托管的 **Qwen 系列大模型（Qwen1.5、Qwen2、Qwen2.5）** 及 **Qwen-Agent 系列专用模型** 提供原生支持；其他第三方模型（如 Llama 3、Gemma）虽可接入，但需手动拼接 context 字段，且不保证 memory 或 RAG 的自动截断与重排序逻辑生效。核心功能包括：  
- 基于知识库的 RAG 检索结果注入（见 [Agent 上下文](../../raw/application-user-guide/agent-context.md)）  
- [长期记忆](../concepts/long-term-memory.md)（Memory）的版本化快照加载与时间窗口过滤  
- Connector 配置元数据自动序列化（如数据库 schema、API endpoint 描述）  
- ParseX 解析结果的结构化嵌入（如 PDF 表格转 JSON 后作为 context 片段）

## 关键参数

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `context_type` | string | `"auto"` | 可选 `"rag"`, `"memory"`, `"connector"`, `"parsex"` 或 `"auto"`（由 runtime 自动推断） |
| `context_max_tokens` | int | `2048` | 整体 context 的 token 上限（含分隔符），超出时按优先级截断（RAG > memory > connector） |
| `memory_window` | int | `5` | 仅当 `context_type=memory` 时生效，表示最多回溯最近 N 轮对话历史 |
| `rag_top_k` | int | `3` | RAG 检索返回的最大 chunk 数量（见 [RAG](../../raw/application-user-guide/agent-context/knowledge-base.md)） |

> **注意**：`context_max_tokens` 在 v2.3.0+ 版本中已替代旧版 `max_context_length` 参数；若在 [Memory](../../raw/application-user-guide/agent-context/memory-library-overview.md) 文档中仍看到后者，属过时描述，请以本表为准。

## 使用方式

### 方式一：API 请求体中显式指定
```json
{
  "model": "qwen2.5-72b-instruct",
  "messages": [...],
  "extra_parameters": {
    "agent_context": {
      "context_type": "rag",
      "knowledge_base_id": "kb-xxx",
      "rag_top_k": 5
    }
  }
}
```

### 方式二：在 Agent 编排 YAML 中声明（推荐）
```yaml
steps:
- type: llm
  model: qwen2.5-72b-instruct
  context:
    type: rag
    source: knowledge_base
    id: kb-xxx
    top_k: 3
```
该方式会自动触发 [Connector](../../raw/application-user-guide/agent-context/overview.md) 的元数据同步与 [ParseX](../../raw/application-user-guide/agent-context/getting-started-overview.md) 的预处理流水线。

## 限制和注意事项

- 单次请求中 `agent context` 总 token 数（含原始 prompt）不得超过所选模型的 `max_position_embeddings`，否则触发 400 错误；Qwen2.5-72b 的硬上限为 32768，但建议 `context_max_tokens ≤ 8192` 以保留足够生成空间。  
- RAG context 与 Memory context **不可同时启用**：若两者均配置，runtime 将优先采用 RAG，静默忽略 memory 配置（无 warning 日志）。  
- 所有 context 片段在注入前会进行敏感词过滤与 HTML/XML 标签剥离，因此不建议在 context 中嵌入可执行代码或富文本格式。  
- 当使用 `context_type: "auto"` 时，系统依据 `messages` 中的 `tool_calls` 和 `user_intent` 字段自动匹配 context 类型，该行为依赖于最新版 [Getting Started Overview](../../raw/application-user-guide/agent-context/getting-started-overview.md) 中定义的意图识别规则。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


