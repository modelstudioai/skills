# agent context

`agent context` 是百炼平台中用于定义 Agent 行为边界与知识来源的核心机制，它决定了 Agent 在执行任务时可访问的外部信息、历史记忆及数据连接能力。通过显式配置上下文，开发者可精准控制 Agent 的“所知”与“所见”，避免信息过载或知识泄露。该机制并非模型内置能力，而是平台层提供的运行时上下文注入框架。

## 支持的模型/功能

当前仅 `qwen-max`、`qwen-plus` 及 `qwen-turbo`（v20240915 及之后版本）原生支持完整的 `agent context` 注入能力；其他模型（如 `qwen-1.5` 系列旧版）虽可接收 context 字段，但实际不解析或忽略其中的 memory/knowledge 结构。RAG、Memory 和 Connector 三大能力均依赖此上下文框架实现 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 中定义的语义绑定。

## 关键参数

调用 `/v1/chat/completions` 时需在 `messages` 后追加 `context` 对象（非 `extra_body`），结构如下：
```json
"context": {
  "knowledge_base_ids": ["kb-xxx"],
  "memory_session_id": "sess-yyy",
  "connector_ids": ["conn-zzz"]
}
```
所有 ID 均需提前通过对应 API 创建并授权；`knowledge_base_ids` 支持最多 3 个知识库，`memory_session_id` 必须关联已启用[长期记忆](../concepts/long-term-memory.md)的 App。详见 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 的参数说明章节。

## 使用方式

1. 初始化：调用 `POST /v1/applications/{app_id}/contexts` 创建上下文实例（返回 `context_id`）  
2. 绑定：在 Chat 请求中将 `context_id` 传入 `context.context_id` 字段（注意不是顶层 `context`）  
3. 动态更新：通过 `PATCH /v1/contexts/{context_id}` 可实时增删 knowledge_base_ids 或 connector_ids  
> **注意**：文档 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 中描述的 `context` 直接嵌入 `messages` 的旧用法已废弃，新接口强制要求 `context_id` 引用，否则返回 `400 Invalid context format`。

## 限制和注意事项

- 单次请求 `context.knowledge_base_ids` 总文档切片数上限为 500，超限将截断并触发告警日志  
- Memory 会话若超过 7 天无访问，自动进入冷存档状态，首次唤醒需额外 2–3s 解冻延迟  
- ParseX 不再作为独立 context 类型存在，其能力已整合进 `knowledge_base_ids` 的解析流程，旧文档 [ParseX](../../raw/application-user-guide/agent-context/getting-started-overview.md) 中的独立配置方式已失效，请以 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 的最新结构为准

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


