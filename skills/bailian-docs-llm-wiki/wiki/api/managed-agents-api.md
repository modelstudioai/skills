# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和运行具备[长期记忆](../concepts/memory.md)、工具调用、多步推理能力的 AI Agent。该 API 抽象了底层执行环境与状态管理，开发者只需关注业务逻辑与技能编排。所有资源（如 Environment、Session、Memory Store）均通过 RESTful 接口统一管理，支持细粒度权限控制与异步事件驱动交互。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三类大模型，不支持自定义模型或外部模型接入；模型绑定在 Agent 创建时指定，不可动态切换。  
- **核心功能**：包括会话生命周期管理（Session）、上下文感知的记忆存储（Memory Store）、安全凭证管理（Credential）、外部工具集成（Skill）、文件上传与引用（File）、环境隔离（Environment）以及 Webhook 事件回调。完整能力清单详见 [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)。  
- **扩展能力**：可通过 Skill API 注册自定义函数（HTTP 或内部服务），并由 Agent 在推理过程中自动调用；Vault 用于加密存储敏感配置，供 Skill 安全读取。这些模块的详细契约请参考 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md) 和 [Vault](../../raw/application-api-reference/managed-agents-api/vault-api.md) 文档。

## 关键参数

- `agent_id`：Agent 唯一标识，创建后不可修改，用于所有子资源路径（如 `/agents/{agent_id}/sessions`）。  
- `session_id`：会话 ID，建议由客户端生成 UUIDv4，避免重复；若未提供，API 将自动生成。  
- `memory_store_id`：指定会话级记忆存储实例，必须提前通过 Memory Store API 创建；若留空，则使用 Agent 默认 memory store。  
- `tool_choice`：控制工具调用策略，可选 `"auto"`（默认）、`"none"` 或指定 Skill ID 字符串；该参数行为与 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md) 中定义一致。

## 使用方式

1. **初始化 Agent**：先调用 `POST /agents` 创建 Agent 实例，指定 `model_id`、`system_prompt` 及默认 `memory_store_id`。  
2. **启动会话**：对目标 Agent 发起 `POST /agents/{agent_id}/sessions`，可携带初始 `input` 和 `files`（需先通过 File API 上传并获取 `file_id`）。  
3. **流式交互**：使用 `POST /agents/{agent_id}/sessions/{session_id}/messages` 提交用户消息，响应为 Server-Sent Events（SSE），含 `content`、`tool_calls`、`events` 等字段。  
4. **事件监听**：注册 Webhook 后，Agent 执行中的关键事件（如 `tool_call_started`、`memory_updated`）将推送至指定 endpoint。Webhook 配置细节见 [Webhook](../../raw/application-api-reference/managed-agents-api/webhook-api.md)。

## 限制和注意事项

- 单次请求最大输入长度为 32768 token（含 system [prompt](../guides/prompt.md) + history + user input）；超出将返回 `400 Bad Request`。  
- Session 生命周期默认 24 小时，超时后自动归档，不可恢复；如需长期会话，请主动调用 `PATCH /sessions/{session_id}` 延长 `expires_at`。  
- > **注意**：[Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md) 文档中提及“支持跨 Region 环境复用”，但实际 API 当前仅允许同一 Region 内的 Environment 与 Agent 绑定，跨 Region 调用将返回 `403 Forbidden` —— 此为文档过时，以实际接口行为为准。  
- 文件上传大小上限为 100 MB，且仅支持 `text/plain`、`application/json`、`application/pdf`、`image/*` 类型；不支持 ZIP 解压或嵌套解析。  
- Credential 的 `access_key` 和 `secret_key` 仅在创建响应中明文返回一次，后续无法再次获取，务必妥善保存。

## 来源文档

- [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)


