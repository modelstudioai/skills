# agent context

`agent context` 是百炼平台中用于为 Agent 提供外部信息输入与状态记忆能力的核心机制，它决定了 Agent 在执行任务时可感知和利用的上下文范围。该机制通过 Knowledge、Memory、Connector 和 ParseX 四类组件协同构建动态、可扩展的上下文环境。开发者需根据模型能力与业务需求合理配置，否则可能导致上下文截断或推理偏差。

## 支持的模型与功能

当前 `agent context` 功能在百炼平台全量支持 Qwen 系列大模型（包括 Qwen1.5、Qwen2、Qwen2.5 及 Qwen3），但对非 Qwen 模型（如 Llama 3 或 GLM 系列）的支持仍处于实验阶段，部分 context 注入方式可能被静默忽略。所有 context 组件均依赖模型的 `tool_call` 与 `context_window` 能力，因此仅当模型具备完整工具调用协议及 ≥32k token 上下文窗口时，才能启用 Memory 与 Knowledge 的联合检索 [Agent 上下文](../../raw/application-user-guide/agent-context.md)。

## 关键参数

- `context_type`: 必填，取值为 `"knowledge"`、`"memory"`、`"connector"` 或 `"parsex"`，决定上下文来源类型  
- `context_id`: 对应资源的唯一标识（如 Knowledge 库 ID、Memory session ID）  
- `max_context_tokens`: 可选，显式控制注入上下文的最大 token 数，默认为模型 context window 的 30%，但不得超过 8192；该参数在 [Knowledge（原RAG）](../../raw/application-user-guide/agent-context/knowledge-base.md) 中被明确要求用于防止 prompt 溢出  
- `enable_fallback`: 布尔值，仅对 Connector 有效，启用后在连接失败时自动降级为无 context 执行  

> **注意**：`max_context_tokens` 在 [Memory](../../raw/application-user-guide/agent-context/memory-library-overview.md) 文档中被描述为“建议设为 4096”，但该值与实际模型窗口不匹配，已确认为过时建议；请以 `context_window × 0.3` 为准。

## 使用方式

通过 API 请求体中的 `context` 字段传入结构化对象：

```json
{
  "context": {
    "type": "knowledge",
    "id": "kb_abc123",
    "max_context_tokens": 6144
  }
}
```

若需组合多源 context（如同时注入 Knowledge 与 Memory），须使用 `context_list` 数组（非 `context` 单对象），且各条目 `context_type` 不可重复。此行为在 [Connector](../../raw/application-user-guide/agent-context/overview.md) 的高级用法章节中有示例说明。

## 限制和注意事项

- 单次请求最多支持 3 个 context 条目（即 `context_list` 长度 ≤ 3）  
- Knowledge 与 ParseX context 不支持实时增量更新，变更后需重新触发索引构建（参见 [ParseX](../../raw/application-user-guide/agent-context/getting-started-overview.md) 初始化流程）  
- Memory context 仅对同一 `session_id` 有效，跨 session 不共享；且默认 TTL 为 2 小时，不可配置  
- 所有 context 内容在进入 LLM 输入前会经统一 tokenizer 截断，**不会**触发模型侧的 sliding window 或 long-context 推理优化，因此超长 context 仍可能丢失尾部信息

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


