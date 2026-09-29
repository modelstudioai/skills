# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和运行具备[长期记忆](../concepts/long-term-memory.md)、工具调用、多步推理能力的 AI Agent。该 API 将底层基础设施（如环境隔离、状态持久化、技能编排）抽象为标准 REST 接口，开发者可聚焦于业务逻辑而非运维细节。所有资源均通过统一的 `POST /v1/agents/{agent_id}/run` 等端点驱动，支持异步会话与事件流式响应。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款大模型，不支持自定义模型或外部模型接入；模型选择通过 `model` 参数在 Agent 创建时指定。
- **核心功能**：包括会话管理（Session）、文件上传与引用（Files API）、结构化记忆存储（Memory Store）、技能注册与调用（Skills API）、凭证安全托管（Credential API）、环境变量隔离（Environment API）及 Webhook 事件通知。完整能力矩阵详见 [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)。
- **扩展能力**：Vault 提供密钥安全分发，Deployment 支持灰度发布与版本回滚，这些高级特性需配合企业版 License 使用 —— 具体权限约束参见 [Deployment](../../raw/application-api-reference/managed-agents-api/deployment-api.md) 文档。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `agent_id` | string | 是 | Agent 实例唯一标识，由 `/v1/agents` 创建后返回 |
| `input` | object | 是 | 用户输入内容，支持 `text` 字段（字符串）或 `files` 数组（含 `file_id`） |
| `session_id` | string | 否 | 指定会话上下文；若未提供则新建会话；会话状态默认保留 7 天 |
| `stream` | boolean | 否 | 设为 `true` 时启用 Server-Sent Events（SSE）流式响应，推荐用于长任务 |
| `max_steps` | integer | 否 | 限制 Agent 单次执行的最大推理步数，默认 20，上限 100 |

> **注意**：`max_steps` 的默认值在 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md) 中标注为 15，但实际 API 行为以最新 OpenAPI Schema（v2024.06）为准，即默认 20。请以运行时响应头 `X-Default-Max-Steps: 20` 为准。

## 使用方式

1. **创建 Agent**：调用 `POST /v1/agents`，传入 `name`、`model`、`skills`（数组）、`memory_store_id` 等配置；
2. **启动执行**：向 `POST /v1/agents/{agent_id}/run` 发送请求，携带 `input` 与可选 `session_id`；
3. **处理响应**：同步模式返回 JSON 结构体（含 `output`、`events`、`session_id`）；流式模式下按 `event: step`、`event: final_output` 分类接收数据块；
4. **调试与监控**：通过 `/v1/sessions/{session_id}/events` 查询历史事件，或订阅 `/v1/webhooks` 接收 `agent.run.completed` 等事件。

快速上手示例见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)，其中包含 cURL 与 Python SDK 调用片段。

## 限制和注意事项

- 单次 `input.text` 长度上限为 32,768 字符；单个 `files` 数组最多 10 个文件，总大小不超过 100 MB；
- Memory Store 写入单条记录最大 1 MB，Key 长度限 256 字符，且不支持嵌套对象序列化（需客户端预扁平化）；
- 所有 Agent 默认启用速率限制：每秒最多 5 次 `/run` 请求（按 `agent_id` 维度计费），超出将返回 `429 Too Many Requests`；
- Vault 与 Credential 资源的读写权限严格绑定至所属 Agent，跨 Agent 引用将触发 `403 Forbidden` —— 此行为与 [Vault](../../raw/application-api-reference/managed-agents-api/vault-api.md) 文档描述一致，但 [Credential](../../raw/application-api-reference/managed-agents-api/credential-api.md) 中未明确强调，建议始终遵循最小权限原则。

## 来源文档

- [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)


