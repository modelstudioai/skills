# agent context

`agent context` 是百炼平台中用于定义 Agent 行为边界与知识来源的核心机制，它决定了 Agent 在执行任务时可访问的外部信息、历史记忆及数据连接能力。通过显式配置上下文，开发者可精准控制 Agent 的“认知范围”，避免幻觉并提升任务准确性。该机制并非模型内置能力，而是平台层提供的运行时上下文注入框架。

## 支持的模型/功能

当前 `agent context` 仅对百炼平台托管的 **Agent 模式（非纯 LLM 调用）** 生效，且要求模型版本 ≥ `qwen-max-20240919` 或 `qwen-plus-20240919`。基础 LLM 接口（如 `/v1/chat/completions`）不支持 context 注入；必须通过 `/v1/agents/{agent_id}/run` 等 Agent 专属端点调用。RAG、Memory 和 Connector 均作为 context 的子模块提供，详见 [Agent 上下文](../../raw/application-user-guide/agent-context.md)。

## 关键参数

在 Agent 运行请求体中，context 通过 `context` 字段声明，结构为：

```json
{
  "context": {
    "knowledge_base_ids": ["kb-xxx"],
    "memory_library_ids": ["ml-yyy"],
    "connector_ids": ["conn-zzz"]
  }
}
```

- `knowledge_base_ids`：最多 5 个已发布的知识库 ID（对应 RAG 能力），需确保知识库状态为 `published`  
- `memory_library_ids`：最多 1 个记忆库 ID（支持对话历史回溯与[长期记忆](../concepts/memory.md)），参见 [Memory](../../raw/application-user-guide/agent-context/memory-library-overview.md)  
- `connector_ids`：最多 3 个已授权 Connector ID（用于实时数据源接入），其权限由工作空间策略控制  

> **注意**：文档 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 中列出的 ParseX 入口链接已失效，实际接入应使用 `/v1/connectors/{id}/parse` 接口，而非旧版 `getting-started-overview.md` 所述流程。

## 使用方式

1. 在控制台创建并发布知识库、记忆库或 Connector  
2. 获取对应资源的 ID（格式如 `kb-abc123`）  
3. 发起 Agent 运行请求时，在 `context` 字段中填入 ID 列表  
4. Agent 内部将自动融合这些上下文生成响应——无需修改提示词或[函数调用](../concepts/function-calling.md)逻辑  

完整示例见 [Connector](../../raw/application-user-guide/agent-context/overview.md) 文档中的 `curl` 调用片段。

## 限制和注意事项

- 单次请求中 `context` 总大小（含所有关联数据的索引元信息）不得超过 10 MB，超限将返回 `400 Bad Request`  
- 知识库与记忆库内容更新后，需等待约 30 秒同步延迟才在新 Agent 调用中生效  
- 不支持跨工作空间引用 context 资源；所有 ID 必须属于当前请求所用 Agent 所属工作空间  
- 若同时启用多个知识库，Agent 不保证检索优先级顺序，建议按语义粒度拆分单一知识库以提升召回精度

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


