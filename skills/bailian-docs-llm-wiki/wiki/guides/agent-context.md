# agent context

`agent context` 是百炼平台中用于增强 Agent 推理能力的核心机制，通过动态注入外部信息（如知识库、历史记忆、连接器数据等）来扩展模型的上下文感知范围。它不改变模型本身参数，而是以结构化方式在推理时注入上下文片段。该机制与 RAG、Memory 和 Connector 等模块深度协同，是构建生产级智能体的关键基础设施。

## 支持的模型与功能

- **模型支持**：当前仅 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三类 Qwen 系列模型原生支持 `agent context` 注入；其他模型（如 `qwen-vl` 或第三方模型）调用时将静默忽略上下文字段 [Agent 上下文](../../raw/application-user-guide/agent-context.md)。
- **功能覆盖**：
  - RAG 检索结果自动注入（需配置 Knowledge Base connector）；
  - Session-level Memory 快照回填（依赖 [Memory](../../raw/application-user-guide/agent-context/memory-library-overview.md) 模块）；
  - 自定义结构化数据（如 JSON Schema 描述的业务实体）通过 ParseX 解析后注入。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `context` | object | 否 | 根对象，包含 `knowledge`、`memory`、`custom` 三个可选子字段 |
| `context.knowledge` | array of object | 否 | 每项含 `content`（string）、`source`（string）、`score`（float）；最大 10 条，总 token ≤ 4096 |
| `context.memory` | object | 否 | 仅支持 `session_id` 字段，由平台自动关联最近 5 轮对话摘要；详见 [Memory](../../raw/application-user-guide/agent-context/memory-library-overview.md) |
| `context.custom` | object | 否 | 用户自定义键值对，需提前在 ParseX 中注册 schema，否则被丢弃 |

> **注意**：文档 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 中提及的 `context.connector` 字段已废弃，实际应使用 `context.knowledge` 配合 connector ID 在 [knowledge base](knowledge-base.md) 配置中绑定——该过时描述未在最新 SDK 中生效。

## 使用方式

1. **API 调用**：在 `/v1/chat/completions` 请求体中直接嵌入 `context` 对象（非 headers 或 query）；
2. **SDK 示例（Python）**：
   ```python
   client.chat.completions.create(
       model="qwen-plus",
       messages=[{"role": "user", "content": "最近订单状态？"}],
       context={
           "knowledge": [{"content": "订单 #12345 已发货，物流单号 SF112233", "source": "order_db"}],
           "memory": {"session_id": "sess_abc789"}
       }
   )
   ```
3. **低代码配置**：在 Agent 编排画布中启用「上下文增强」开关，并关联 Knowledge Base 或 Memory 实例 [ParseX](../../raw/application-user-guide/agent-context/getting-started-overview.md)。

## 限制和注意事项

- 单次请求 `context` 总 token 数不得超过模型 context window 的 30%（例如 `qwen-plus` 最大 8192 token，则 context ≤ 2457 token）；
- `context.knowledge` 中的 `content` 不支持嵌套 Markdown 或 HTML，纯文本将被截断处理；
- `context.memory` 仅在开启 Session Management 且 `session_id` 有效时生效，空或非法 session_id 将导致 memory 字段被完全忽略；
- 所有 context 数据**不参与训练、不落库、不缓存**，仅限本次推理生命周期内使用。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


