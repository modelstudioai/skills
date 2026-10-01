# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和管理具备[长期记忆](../concepts/memory.md)、工具调用、多步推理能力的 AI Agent。该 API 以 RESTful 形式提供，支持细粒度的生命周期控制与环境隔离。开发者可通过组合 Agent、Environment、Session、Memory Store 等核心资源构建生产级智能体应用。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三类大模型（详见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)）；不支持自定义模型或外部模型接入。
- **核心功能**：包括会话状态管理（Session）、持久化记忆存储（Memory Store）、安全凭证管理（Credential）、技能封装（Skill）、文件上传与引用（File）、环境沙箱隔离（Environment）及 Webhook 事件回调。所有功能均通过独立子资源 API 暴露，例如 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md) 提供运行时依赖注入能力。

## 关键参数

- `agent_id`（路径参数）：Agent 唯一标识，由平台在创建后返回，不可自定义。
- `session_id`（请求体/查询参数）：用于关联用户会话，若未提供则自动创建新会话；建议前端传入稳定用户 ID 以启用跨设备记忆同步。
- `memory_store_id`（可选）：指定绑定的记忆存储实例，若为空则使用 Agent 默认 Memory Store；注意该字段在 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md) 中为必填项，与 [Memory Store](../../raw/application-api-reference/managed-agents-api/memory-store-api.md) 文档描述存在不一致。
> **注意**：`memory_store_id` 在 Session 创建时是否强制要求，[Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md) 与 [Memory Store](../../raw/application-api-reference/managed-agents-api/memory-store-api.md) 的约束说明冲突，建议以 Session API 文档为准并显式传入。

## 使用方式

1. **初始化 Agent**：先调用 `/v1/agents` 创建 Agent 实例，指定 `model_id` 和基础配置；
2. **配置依赖**：按需创建 Environment、Memory Store、Skill 等资源，并通过 `POST /v1/agents/{agent_id}/bindings` 关联；
3. **启动交互**：使用 `POST /v1/agents/{agent_id}/sessions/{session_id}/chat` 发起对话，请求体中可携带 `files`、`tool_choice` 等上下文参数；
4. 参考完整流程见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)。

## 限制和注意事项

- 单个 Agent 最多绑定 10 个 Skill、5 个 Environment 和 1 个 Memory Store；
- Session 生命周期默认 7 天，超时后关联 Memory Store 中的历史记录仍保留，但会话状态不可恢复；
- 文件上传大小上限为 100 MB，且仅支持 `pdf`, `txt`, `md`, `csv`, `xlsx` 格式（参见 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)）；
- 所有 API 均需通过 Bearer Token 认证，Token 权限须包含 `managed_agents:full_access`，具体鉴权规则见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 来源文档

- [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)


