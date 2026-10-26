# agent context

agent context 是百炼平台中用于定义 Agent 运行时环境与外部信息输入的关键机制，它决定了 Agent 在执行任务过程中可访问的知识、历史记忆、数据源及解析能力。通过合理配置上下文，开发者可显著提升 Agent 的准确性、连贯性与领域适应性。其设计遵循模块化原则，各组件（如 RAG、Memory、Connector）可独立启用或组合使用。

## 支持的模型/功能

agent context 本身不依赖特定大模型，但需与支持 `tool calling` 和 `context injection` 能力的模型协同工作，当前已验证兼容的模型包括：Qwen-Max、Qwen-Plus、Qwen-Turbo 及部分第三方接入模型（需开启 `enable_context` 标志）。核心功能模块包括：
- **RAG**：从知识库动态检索相关片段注入上下文，详见 [Agent 上下文](../../raw/application-user-guide/agent-context.md)；
- **Memory**：维护会话级或用户级[长期记忆](../concepts/long-term-memory.md)，支持向量存储与语义检索，参考 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 中的 Memory 模块说明；
- **Connector**：对接外部系统（如数据库、API、文件存储），实现上下文实时拉取，该能力在 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 的 Connector 章节有基础概述。

## 关键参数

配置 agent context 时需在请求 payload 或应用配置中设置以下关键字段：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `context.rag.enabled` | boolean | 否 | 启用 RAG 检索，默认 `false` |
| `context.memory.enabled` | boolean | 否 | 启用记忆回溯，默认 `false`；若启用，需预先配置 memory_id |
| `context.connector.ids` | string[] | 否 | 指定启用的 connector ID 列表，最多 5 个 |
| `context.max_tokens` | number | 否 | 上下文总 token 上限（含 prompt + 注入内容），默认 4096，硬上限由所选模型决定 |

> **注意**：`context.max_tokens` 的实际生效值受模型最大上下文窗口限制，例如 Qwen-Turbo 最大仅支持 8K 输入，超出部分将被截断——此行为与 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 中“[Token](../concepts/token.md) 截断策略”一节描述一致，但文档未明确标注硬上限来源，建议以 `model.supported_context_length` API 返回值为准。

## 使用方式

1. **API 调用**：在 `/v1/chat/completions` 请求体中嵌入 `context` 对象，示例：
   ```json
   {
     "model": "qwen-plus",
     "messages": [...],
     "context": {
       "rag": { "enabled": true, "knowledge_base_id": "kb-xxx" },
       "memory": { "enabled": true, "memory_id": "mem-yyy" }
     }
   }
   ```
2. **低代码平台配置**：在「Agent 编排」界面的「上下文设置」面板中勾选对应模块并填写 ID，配置即时生效；
3. **SDK 封装**：Python SDK 中通过 `AgentConfig(context=...)` 构造，详见 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 的 Getting Started 示例。

## 限制和注意事项

- 单次请求中 RAG 检索结果最多返回 5 片段，每片段最大 1024 字符（经 ParseX 清洗后）；
- Memory 模块仅支持 LRU 最近 100 条交互记录回溯，不支持跨会话关联（除非显式复用同一 `memory_id`）；
- Connector 并发调用数受账户配额限制，免费版默认为 2 并发，超限请求将失败而非排队；
- 所有上下文注入内容均在 LLM 输入前完成拼接与 token 计数，**不会触发额外模型调用**——这一点与旧版文档中“context 预处理可能引入延迟”的描述存在偏差，当前实现在 v2.3+ 已优化为同步注入，详见 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 的版本更新日志。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


