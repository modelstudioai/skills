# agent context

`agent context` 是百炼平台中用于增强 Agent 推理能力的核心机制，通过动态注入外部知识、历史记忆和结构化数据源，使 Agent 能在运行时获取上下文相关的补充信息。它不依赖模型自身的参数化知识，而是以轻量、可插拔的方式扩展 Agent 的感知与决策边界。该机制由 RAG、Memory 和 Connector 三大组件协同支撑，适用于对话式应用、智能工作流等场景。

## 支持的模型与功能

- **模型支持**：当前仅 `qwen-max`、`qwen-plus` 和 `qwen-turbo`（v202408 及以上版本）原生支持 `agent context` 的完整上下文注入能力；其他模型（如 `qwen-1.5` 系列）仅支持基础 memory 回溯，不支持 RAG 或 Connector 动态加载 [Agent 上下文](../../raw/application-user-guide/agent-context.md)。
- **核心功能**：
  - **RAG 检索增强**：从知识库实时检索相关文档片段，作为 prompt 上下文拼接；
  - **Memory 管理**：支持会话级短期记忆（session memory）与用户级[长期记忆](../concepts/long-term-memory.md)（user memory），详见 [Memory](../../raw/application-user-guide/agent-context/memory-library-overview.md)；
  - **Connector 集成**：对接数据库、API、文件系统等外部数据源，按需触发上下文提取。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `context_config` | object | 否 | 控制上下文注入策略，含 `rag`、`memory`、`connector` 三个子对象 |
| `rag.enabled` | boolean | 否，默认 `false` | 启用 RAG 检索；启用时需指定 `knowledge_base_id` |
| `memory.enabled` | boolean | 否，默认 `true` | 是否启用会话记忆；设为 `false` 将禁用所有 memory 注入 |
| `connector.ids` | string[] | 否 | 指定要调用的 connector ID 列表，最多 3 个 |

> **注意**：`context_config.memory.enabled = false` 并不会清除已存在的 memory 记录，仅跳过本次请求的注入；该行为与 [RAG](../../raw/application-user-guide/agent-context/knowledge-base.md) 文档中“memory 禁用即清空上下文”的旧描述存在矛盾，以当前 SDK v3.2+ 实现为准。

## 使用方式

1. 在调用 `/v1/chat/completions` 时，于 `messages` 外层传入 `context_config` 对象；
2. RAG 需提前在控制台创建知识库并获取 `knowledge_base_id`；
3. Memory 默认自动启用，无需额外配置，但可通过 `user_id` 和 `session_id` 控制作用域；
4. Connector 需已在平台注册并授权，ID 可在 [Connector](../../raw/application-user-guide/agent-context/overview.md) 页面查看。

示例（精简）：
```json
{
  "model": "qwen-max",
  "messages": [...],
  "context_config": {
    "rag": { "enabled": true, "knowledge_base_id": "kb-xxx" },
    "memory": { "enabled": true },
    "connector": { "ids": ["conn-db-001"] }
  }
}
```

## 限制和注意事项

- 单次请求注入的总上下文 token 数上限为 8192（含原始 prompt），超出部分将被截断；
- RAG 检索结果默认返回 top-3 片段，不可调整数量；
- Memory 的 user-level 存储容量为 1MB/用户，超限时写入失败且不报错，需主动监控 [ParseX](../../raw/application-user-guide/agent-context/getting-started-overview.md) 日志；
- 不支持在流式响应（`stream: true`）中动态更新 context_config —— 配置必须在首次请求时固定。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


