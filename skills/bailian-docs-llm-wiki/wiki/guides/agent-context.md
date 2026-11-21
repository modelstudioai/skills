# agent context

agent context 是百炼平台中用于定义 Agent 运行时环境与外部信息输入的关键机制，它决定了 Agent 在执行任务过程中可访问的知识、历史记忆、数据源及解析能力。通过合理配置上下文，开发者可显著提升 Agent 的准确性、连贯性与领域适应性。其设计遵循模块化原则，各组件（如 RAG、Memory、Connector）可独立启用或组合使用。

## 支持的模型/功能

agent context 本身不依赖特定大模型，但需与支持 `tool calling` 和 `context injection` 能力的模型协同工作，当前已验证兼容的模型包括：Qwen-Max、Qwen-Plus、Qwen-Turbo 及部分第三方接入模型（需开启 `enable_context` 标志）。核心功能模块包括：
- **RAG**：支持从知识库动态检索并注入上下文片段，详见 [Agent 上下文](../../raw/application-user-guide/agent-context.md)；
- **Memory**：提供短期对话记忆（session-level）与长期用户画像记忆（user-level），其能力边界在 [Memory](../../raw/application-user-guide/agent-context/memory-library-overview.md) 中明确定义；
- **Connector**：用于对接外部系统（如 CRM、数据库），其协议适配与认证方式参考 [Connector](../../raw/application-user-guide/agent-context/overview.md)；
- **ParseX**：专用于非结构化文档（PDF/Word/Excel）的内容提取与语义切分，是 RAG 前置必备环节，用法见 [ParseX](../../raw/application-user-guide/agent-context/getting-started-overview.md)。

> **注意**：部分旧版 SDK 示例中将 `memory` 配置为布尔开关（`true/false`），但自 v2.3.0 起已改为对象结构（含 `type`, `ttl`, `max_length` 字段），实际行为以 [Memory](../../raw/application-user-guide/agent-context/memory-library-overview.md) 文档为准。

## 关键参数

所有上下文模块均通过 `context` 字段统一配置，典型结构如下：

```json
{
  "context": {
    "rag": { "knowledge_base_id": "kb-xxx", "top_k": 3 },
    "memory": { "type": "session", "ttl": 3600 },
    "connector": { "id": "conn-yyy", "params": { "timeout": 5000 } },
    "parsex": { "mode": "semantic", "chunk_size": 512 }
  }
}
```

- `rag.knowledge_base_id`：必填，对应知识库唯一标识；
- `memory.type`：仅支持 `"session"` 或 `"user"`，不支持 `"global"`（该值已在 [Connector](../../raw/application-user-guide/agent-context/overview.md) 的附录中明确废弃）；
- `parsex.mode`：推荐 `"semantic"`，`"fixed"` 模式在长文档中易导致语义断裂。

## 使用方式

1. 在创建 Agent 时，于请求体 `POST /v1/agents` 的 `context` 字段中传入完整配置；
2. 若使用 SDK，调用 `AgentBuilder.withContext(...)` 方法链式设置；
3. RAG 与 ParseX 需预先完成知识库构建与文档解析任务（异步），否则首次调用将返回 `400 Bad Request`；
4. Memory 的生命周期由会话 ID（`session_id`）或用户 ID（`user_id`）自动绑定，无需手动管理。

## 限制和注意事项

- 单次请求注入的上下文总 token 数上限为 8192（含 prompt + context），超出将被截断且不报错；
- RAG 与 Memory 的检索结果默认按相关性降序合并，但 **不保证时间顺序**，若需严格保序，须在应用层对 `context.rag.results` 与 `context.memory.items` 手动排序；
- Connector 调用失败时，Agent 默认跳过该模块继续执行，不会中断流程——此行为与 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 中“fail-fast”描述存在矛盾，实际以运行时行为为准；
- ParseX 对扫描版 PDF 不支持 OCR，需预处理为文本型 PDF，该限制未在 [ParseX](../../raw/application-user-guide/agent-context/getting-started-overview.md) 中明确说明，属隐含约束。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


