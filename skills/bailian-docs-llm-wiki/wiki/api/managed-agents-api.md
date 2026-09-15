# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和管理具备[长期记忆](../concepts/long-term-memory.md)、工具调用、多步推理能力的 AI Agent。该 API 以 RESTful 形式提供，支持细粒度的生命周期控制与环境隔离。开发者可通过组合 Agent、Environment、Session、Skill 等资源构建生产级自动化工作流。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三类大模型（详见 [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)）；不支持自定义模型或外部模型接入。
- **核心功能**：包括会话状态持久化（Session）、安全凭证管理（Credential）、私有知识库集成（Vault）、文件上传与解析（File）、可复用技能封装（Skill）、以及 Webhook 事件回调（Webhook）。所有功能均通过独立子资源 API 暴露，例如 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md) 用于定义运行时沙箱，[Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 用于声明行为逻辑。

## 关键参数

- `agent_id`：必填，Agent 实例唯一标识符，由 `/agents` 创建接口返回。
- `session_id`：可选但推荐，用于关联用户会话；若未提供，系统将自动生成临时 session。
- `tool_choice`：指定工具调用策略，可选值为 `"auto"`（默认）、`"none"` 或显式工具名称列表（如 `["search", "calculator"]`）。
- `max_steps`：单次请求最大执行步数，取值范围 `1–50`，超出将被强制终止（参见 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)）。

## 使用方式

1. 调用 `/agents` 创建 Agent，传入 `model`, `instructions`, `skills` 等配置；
2. （可选）调用 `/environments` 创建隔离环境，并在 Agent 创建时通过 `environment_id` 绑定；
3. 发起 `/sessions/{session_id}/messages` 请求，携带用户输入及上下文；
4. 通过 `/webhooks` 配置事件监听，捕获 `agent_step_completed`、`tool_executed` 等生命周期事件。

> **注意**：原始文档中 [Quick Start](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 示例使用了已废弃的 `tools` 字段顶层传参方式；实际应通过 `skills` 数组引用预注册 Skill ID，此差异已在 [Agent API](../../raw/application-api-reference/managed-agents-api/agent-api.md) 中明确修正。

## 限制和注意事项

- 单个 Agent 最多绑定 10 个 Skill，单个 Vault 最多关联 100 个文件；
- Session 默认 TTL 为 24 小时，超时后历史消息不可恢复（除非显式启用 Vault 持久化）；
- 所有文件上传需先通过 `/files` 接口预注册，直接在 message 中附带二进制内容将被拒绝；
- Credential 的 secret 值仅在创建时返回一次，后续无法再次读取，需自行安全存储。

## 来源文档

- [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)


