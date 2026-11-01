# agent context

agent context 是百炼平台中用于定义 Agent 运行时环境与外部信息输入的关键机制，它决定了 Agent 在执行任务过程中可访问的知识、历史记忆、数据源及解析能力。通过合理配置上下文，开发者可显著提升 Agent 的准确性、连贯性与领域适应性。其设计遵循模块化原则，各组件（如 RAG、Memory、Connector）可独立启用或组合使用。

## 支持的模型/功能

agent context 本身不依赖特定大模型，但需与支持 `tool calling` 和 `context injection` 能力的模型协同工作，当前已验证兼容的模型包括：Qwen-Max、Qwen-Plus、Qwen-Turbo 及部分第三方接入模型（需开启 `enable_context` 标志）。核心功能模块包括：
- **RAG**：从知识库动态检索相关片段注入上下文，详见 [Agent 上下文](../../raw/application-user-guide/agent-context.md)；
- **Memory**：维护会话级或用户级[长期记忆](../concepts/long-term-memory.md)，支持向量存储与语义检索，参考 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 中的 Memory 模块说明；
- **Connector**：对接外部系统（如数据库、API、文件存储），实现上下文实时拉取，该能力在 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 的 Connector 章节有基础概述。

## 关键参数

配置 agent context 时需在 `agent_config.yaml` 或 API 请求体中指定以下关键字段：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `rag.enabled` | boolean | 否 | 启用 RAG 检索，默认 `false` |
| `memory.enabled` | boolean | 否 | 启用记忆回溯，默认 `false`；若启用，需同时配置 `memory.type`（`session` / `user`） |
| `connector.ids` | string[] | 否 | 指定启用的 Connector ID 列表，ID 需已在控制台预注册 |
| `context_window_size` | integer | 否 | 上下文总 token 限制（含 prompt + context），默认 8192，最大值依模型而定 |

> **注意**：`context_window_size` 的实际生效上限受所选模型最大上下文长度约束，例如 Qwen-Turbo 最大仅支持 4096 tokens，超出部分将被截断——此限制在 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 中未明确说明，需以 [模型规格文档](../../raw/models/specs/qwen-turbo.md) 为准。

## 使用方式

1. **控制台配置**：在 Agent 编排页 →「上下文设置」Tab 中勾选所需模块，并绑定知识库、记忆库或 Connector 实例；
2. **API 调用**：在 `/v1/agents/{agent_id}/invoke` 请求体中传入 `context` 对象，结构示例如下：
   ```json
   {
     "context": {
       "rag": { "knowledge_base_ids": ["kb-xxx"] },
       "memory": { "session_id": "sess-123" },
       "connector": { "ids": ["conn-db-01"] }
     }
   }
   ```
3. **SDK 调用**：使用 `BailianAgent.invoke()` 时传入 `context` 字典参数，具体字段与 API 一致，详见 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 的 Getting Started 示例。

## 限制和注意事项

- 单次请求中，RAG 检索结果最多返回 5 个 chunk，Memory 回溯最多加载最近 10 轮对话，Connector 并发调用数上限为 3；
- RAG 与 Memory 的检索结果均按 relevance score 排序后截断拼接，不保证严格保序，业务逻辑不应依赖 chunk 的原始位置；
- 若同时启用多个模块，上下文总长度可能快速逼近模型限制，建议监控 `usage.context_tokens` 字段并主动裁剪低优先级内容；
- ParseX 解析能力（如 PDF 表格提取、多模态 OCR）属于 Connector 的子能力，其配置与调用需通过 `connector.ids` 绑定对应 ParseX Connector，而非独立开关——该细节在 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 的 overview.md 中未体现，实际以 [getting-started-overview.md](../../raw/application-user-guide/agent-context/getting-started-overview.md) 为准。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


