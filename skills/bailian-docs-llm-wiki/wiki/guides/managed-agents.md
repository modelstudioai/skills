# managed agents

managed agents 是百炼平台提供的托管式智能体运行服务，开发者无需自行部署和运维 Agent 运行时环境，只需定义任务逻辑与交互协议，平台即自动完成调度、扩缩容、状态持久化与可观测性集成。该能力适用于需长期运行、多轮对话、跨会话上下文保持或事件驱动响应的 Agent 场景。详细背景可参考 [Managed Agents](../../raw/application-user-guide/managed-agents.md)。

## 支持的模型与功能

- **模型支持**：当前仅支持 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款通义千问系列模型；其他模型（如 `qwen2.5-*` 系列）暂未开放接入，调用将返回 `400 UnsupportedModel` 错误。
- **核心功能**：
  - 多轮会话状态自动管理（基于 session_id）
  - 工具调用（function calling）与[插件](../concepts/plugin.md)集成（需在 `tools` 字段中显式声明）
  - 上下文窗口自动分片与长期记忆（通过 `context_id` 关联外部向量库）
  - Webhook 事件订阅（支持 `agent_started`、`task_completed`、`tool_call_failed` 等 8 类事件）

> **注意**：[概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md) 中提及“支持任意百炼已上线模型”，该描述已过时；以本节及 [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md) 中的模型白名单为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 必须为 `qwen-max` / `qwen-plus` / `qwen-turbo` 之一 |
| `session_id` | string | 否 | 用于关联同一会话的多次请求；不传则由平台生成新会话 |
| `context_id` | string | 否 | 指向预注册的上下文配置 ID，启用长期记忆需提前调用 `/v1/contexts` 创建 |
| `tools` | array | 否 | 工具定义列表，格式与 OpenAI Function Calling 兼容；未声明则禁用工具调用 |

## 使用方式

1. **创建 Agent**：通过 `POST /v1/agents` 提交配置（含 [prompt](prompt.md)、tools、model 等），获取 `agent_id`；
2. **发起会话**：调用 `POST /v1/agents/{agent_id}/sessions`，传入用户输入与可选 `session_id`；
3. **流式响应处理**：响应体为 Server-Sent Events（SSE），每条事件含 `type`（如 `message`, `tool_call`, `done`）与对应 payload；
4. **事件监听（可选）**：在创建 Agent 时配置 `webhook_url`，平台将异步推送关键生命周期事件 —— 具体事件类型详见 [Webhook 事件订阅](../../raw/application-user-guide/managed-agents/managed-agents-webhook.md)。

## 限制和注意事项

- 单次会话最大 token 数：`qwen-max` 为 32768，其余模型为 8192；超限请求将被截断并返回警告头 `X-Warning: truncated`;
- `session_id` 生命周期为 7 天，过期后关联上下文不可恢复；
- 不支持自定义模型权重、LoRA 微调加载或系统级容器挂载；
- Agent 实例默认无公网出向访问权限；如需调用外部 API，必须通过百炼内置的 [安全网关代理](../../raw/application-user-guide/managed-agents/managed-agents-environment.md) 配置白名单域名。

## 来源文档

- [Managed Agents](../../raw/application-user-guide/managed-agents.md)


