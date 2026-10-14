# agent context

agent context 是百炼平台中用于定义 Agent 运行时环境与外部信息交互能力的核心机制，它决定了 Agent 能够感知哪些知识、记住哪些历史、接入哪些数据源。该机制通过结构化配置实现上下文的动态注入与生命周期管理，直接影响 Agent 的推理准确性与任务执行能力。其设计遵循“按需加载、显式声明、隔离可控”原则。

## 支持的模型与功能

当前仅 `qwen-plus`、`qwen-max` 和 `qwen2.5-72b-instruct` 三类模型原生支持完整的 agent context 功能（含 memory、knowledge base、connector 集成）。其他模型调用时若传入 `context` 字段，将被静默忽略——此行为已在 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 中明确说明。RAG 检索增强、长期记忆回溯、第三方系统连接器（如飞书、钉钉）均依赖该上下文框架驱动。

## 关键参数

在 `messages` 数组外，需通过顶层 `context` 对象声明上下文组件：

```json
{
  "context": {
    "memory": { "id": "mem_abc123" },
    "knowledge_base": { "id": "kb_xyz789", "top_k": 3 },
    "connector": { "id": "conn_lmn456", "timeout_ms": 5000 }
  }
}
```

所有子字段均为可选；若未提供 `memory.id`，则本次调用不启用记忆；若 `knowledge_base.id` 不存在或权限不足，请求将直接失败（非降级）。详细字段语义见 [Agent 上下文](../../raw/application-user-guide/agent-context.md)。

## 使用方式

1. **初始化 Memory**：首次调用前需通过 `/v1/memories` 创建 memory 实例，并在后续请求中复用其 `id`；  
2. **绑定 Knowledge Base**：确保 knowledge base 已发布且 `id` 在当前项目可见，详见 [RAG](../../raw/application-user-guide/agent-context/knowledge-base.md)；  
3. **配置 Connector**：connector 必须已完成 OAuth 授权并处于启用状态，否则 `context.connector` 将触发 403 错误；  
4. 所有上下文组件 ID 均为字符串类型，**不支持变量插值或表达式**（如 `${kb_id}`），该限制在 [ParseX](../../raw/application-user-guide/agent-context/getting-started-overview.md) 文档中被强调。

> **注意**：`context.memory.id` 若指向一个已过期（`expired_at < now`）的 memory，API 不返回错误，但实际不加载任何历史——这与 [Memory](../../raw/application-user-guide/agent-context/memory-library-overview.md) 文档中“自动清理后返回空上下文”的描述一致，但不同于早期文档声称的“抛出 404”。

## 限制和注意事项

- 单次请求中 `context` 总大小（JSON 序列化后）不得超过 2MB；  
- `knowledge_base.top_k` 最大值为 10，超出将被截断（非报错），该限制未在 [RAG](../../raw/application-user-guide/agent-context/knowledge-base.md) 中体现，属平台隐式约束；  
- connector 调用超时独立于主模型推理超时，且不可在 `context.connector.timeout_ms` 外覆盖；  
- 同一 `memory.id` 在并发请求中共享状态，无读写锁，高并发写入可能导致历史覆盖——此风险在 [Memory](../../raw/application-user-guide/agent-context/memory-library-overview.md) 中未警示，需开发者自行规避。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


