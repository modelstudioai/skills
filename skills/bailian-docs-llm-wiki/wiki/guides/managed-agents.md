# managed agents

managed agents 是百炼平台提供的托管式智能体运行服务，开发者无需自行部署和运维 Agent 服务，只需定义任务逻辑与执行环境，平台即自动完成调度、扩缩容、状态管理与可观测性支持。该能力适用于需要长期运行、多轮交互、上下文感知或事件驱动的自动化工作流场景。详细背景可参见 [Managed Agents](../../raw/application-user-guide/managed-agents.md)。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台已上线的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列大模型（v202409 及之后版本），不支持自定义模型或第三方模型接入。  
- **核心功能**：包括多轮对话上下文自动维护、异步任务委派（session-based delegation）、环境变量隔离、工具调用（function calling）集成、Webhook 事件通知（如 `agent_started`、`task_completed`）等。  
- 所有功能细节均以 [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md) 中的定义为准；若 CLI 行为与该文档描述不一致，请以该文档为权威依据。

## 关键参数

创建或更新 managed agent 时需指定以下必需参数：

| 参数 | 类型 | 说明 |
|------|------|------|
| `name` | string | Agent 唯一标识符（符合 DNS-1123 标准，长度 ≤63 字符） |
| `model_id` | string | 必须为 `qwen-max` / `qwen-plus` / `qwen-turbo` 之一 |
| `system_prompt` | string | 非空，用于初始化 Agent 的角色与行为约束 |
| `tools` | array | 可选，最多 10 个已注册的 tool ID（详见 [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)） |

> **注意**：`temperature` 和 `top_p` 等采样参数**不可在 agent 创建时设置**，仅支持在每次调用 session 时通过 `/v1/agents/{id}/sessions` 接口的 `parameters` 字段传入——此行为与 [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md) 文档中旧版描述存在冲突，应以当前 API 实际行为为准。

## 使用方式

1. **创建 Agent**：通过控制台或 CLI（`bailian agent create --config config.yaml`）提交定义；配置文件结构参考 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)。  
2. **启动会话**：调用 `POST /v1/agents/{id}/sessions` 创建 session，并在请求体中传入 `input` 和可选的 `parameters`。  
3. **处理响应与事件**：监听 Webhook（需提前在 [Webhook 事件订阅](../../raw/application-user-guide/managed-agents/managed-agents-webhook.md) 中配置 endpoint）或轮询 session 状态获取结果。

## 限制和注意事项

- 单个 Agent 最多同时运行 50 个活跃 session；超出将返回 `429 Too Many Requests`。  
- Session 生命周期最长 24 小时，超时后上下文自动清理且不可恢复。  
- Agent 不支持跨 workspace 共享；每个 workspace 需独立创建。  
- 所有环境变量（含 secrets）仅在 session 生命周期内注入内存，不会持久化或透出到日志（符合 [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md) 安全要求）。  
- 计费按实际使用的 token 数与 session 时长叠加计算，详情见 [计费](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)。

## 来源文档

- [Managed Agents](../../raw/application-user-guide/managed-agents.md)


