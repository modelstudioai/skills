# agent context

agent context 是 Agent 运行时所依赖的动态上下文环境，用于支撑其感知、推理与执行能力。它由知识库（RAG）、记忆（Memory）、外部连接器（Connector）及结构化解析组件（ParseX）共同构成，决定了 Agent 对用户意图的理解深度与响应质量。该机制在百炼平台中通过统一上下文管理接口暴露给开发者调用。

## 支持的模型与功能

当前 agent context 仅在 `qwen-plus`、`qwen-max` 及 `qwen2.5-72b-instruct` 等支持完整 Agent 框架的模型上启用；基础语言模型（如 `qwen-turbo`）不支持 context 注入。核心功能包括：  
- RAG：从向量库实时检索相关文档片段，注入 prompt 上下文；  
- Memory：维护会话级短期记忆（Session Memory）与用户级[长期记忆](../concepts/long-term-memory.md)（User Memory），详见 [Agent 上下文](../../raw/application-user-guide/agent-context.md)；  
- Connector：对接第三方系统（如 CRM、数据库、API），实现上下文驱动的动作触发；  
- ParseX：对非结构化输入（PDF、表格、邮件等）进行语义解析并提取结构化字段，作为 context 的补充输入源。

## 关键参数

在创建或调用 Agent 时，需通过 `context_config` 字段显式声明上下文配置：

```json
{
  "context_config": {
    "rag": { "enabled": true, "top_k": 3 },
    "memory": { "enabled": true, "type": "session" },
    "connector": { "ids": ["conn-crm-001"] },
    "parsex": { "enabled": true, "max_pages": 10 }
  }
}
```

所有子模块均为可选，默认全禁用。`top_k` 最大支持 10；`max_pages` 超过 20 将被截断。更多细节请参考 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 中的配置说明。

## 使用方式

1. 在控制台「Agent 配置 → 上下文设置」中勾选启用模块，并绑定对应资源（如知识库 ID、Connector 实例）；  
2. 或通过 OpenAPI 的 `/v1/agents/{id}/invoke` 接口，在请求体中传入 `context_config`；  
3. 若使用 SDK，调用 `Agent.invoke(input, context_config=...)` 即可。注意：RAG 检索结果与 Memory 内容将自动拼接至 system prompt 末尾，无需手动构造。具体集成示例见 [Agent 上下文](../../raw/application-user-guide/agent-context.md)。

## 限制和注意事项

- 单次请求总 context 长度（含 RAG 片段 + Memory + ParseX 输出）不得超过模型最大上下文窗口的 80%，否则触发截断且不报错；  
- Memory 的 User Memory 依赖用户唯一标识（`user_id`）进行隔离，若未传 `user_id`，则退化为 session-only 模式；  
- Connector 调用受配额与超时限制（默认 5s），失败时不中断主流程，但对应 context 字段为空；  
> **注意**：原始文档中提到的 `ParseX` 入口路径 [getting-started-overview.md](../../raw/application-user-guide/agent-context/getting-started-overview.md) 已于 v2.3 版本废弃，实际应使用 `/v1/parsex/extract` 新接口，详见最新 [knowledge-base.md](../../raw/application-user-guide/agent-context/knowledge-base.md) 中的兼容性说明。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


