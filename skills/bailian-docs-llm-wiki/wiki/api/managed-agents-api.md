# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和管理具备[长期记忆](../concepts/memory.md)、工具调用、多步推理能力的自主运行 Agent。该 API 以 RESTful 形式提供，支持细粒度的环境隔离、会话生命周期控制与外部系统集成。开发者可通过它快速构建面向业务场景的自动化工作流，无需自行维护底层推理调度与状态管理。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 等 Qwen 系列大模型；不支持用户自定义模型或第三方模型接入（参见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)）。
- **核心功能**：包括 Agent 定义与部署、动态 Environment 配置、Session 生命周期管理、结构化 Memory Store 持久化、Skill 编排、Vault 安全凭证注入、以及 Webhook 事件回调。完整能力矩阵详见 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 和 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md) 文档。

## 关键参数

- `agent_id`（路径参数）：Agent 唯一标识符，由平台分配或用户指定（需符合 `[a-z0-9]([-a-z0-9]*[a-z0-9])?` 正则规则）。
- `session_id`（请求头或 query 参数）：用于关联会话上下文；若未提供，API 将自动创建新会话（见 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)）。
- `tool_choice`（body 字段）：控制工具调用策略，可选 `"auto"`、`"none"` 或指定 Skill ID；默认为 `"auto"`，但部分旧版 SDK 默认行为不一致（> **注意**：[Quickstart](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 中示例仍使用 `"required"`，该值已废弃，请以 [Agent API](../../raw/application-api-reference/managed-agents-api/agent-api.md) 为准）。

## 使用方式

1. **认证**：所有请求需携带 `Authorization: Bearer <api_key>`，且 `X-Region` 请求头指定地域（如 `cn-beijing`）；
2. **创建 Agent**：`POST /v1/agents`，传入 `name`、`model_id`、`skills` 数组及可选 `memory_store_id`；
3. **发起调用**：`POST /v1/agents/{agent_id}/chat`，body 包含 `messages`（遵循 OpenAI 格式）及 `session_id`；
4. **文件上传与引用**：通过 `/v1/files` 上传后，可在 `messages` 中以 `file://<file_id>` 形式引用（详见 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)）。

## 限制和注意事项

- 单次请求最大 token 数为 32768（含 [prompt](../guides/prompt.md) + completion），超限将返回 `400 Bad Request`；
- Memory Store 默认保留最近 100 条交互记录，可通过 `max_history` 参数调整（上限 500）；
- Vault 中的凭证仅在运行时注入 Environment，不会出现在日志或调试响应中；
- > **注意**：[Credential API](../../raw/application-api-reference/managed-agents-api/credential-api.md) 文档中提及的 `GET /v1/credentials/{id}/value` 接口已于 v2.3 版本下线，当前仅支持通过 Environment 绑定方式间接使用凭证。

## 来源文档

- [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)


