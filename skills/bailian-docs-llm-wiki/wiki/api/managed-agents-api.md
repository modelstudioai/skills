# managed agents api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和管理具备[长期记忆](../concepts/long-term-memory.md)、工具调用、多轮会话与环境隔离能力的 AI Agent。该 API 以 RESTful 形式提供，支持细粒度资源控制（如 Environment、Session、Memory Store）和可扩展能力（如 Skill、Vault、Webhook）。开发者可通过它构建生产级自动化工作流，无需自行维护底层推理与状态管理逻辑。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 等 Qwen 系列模型；不支持用户自定义模型或第三方模型接入。  
- **核心功能模块**包括：Agent 生命周期管理、隔离式运行环境（Environment）、带上下文感知的会话（Session）与事件流、持久化记忆存储（Memory Store）、结构化文件处理（Files API）、可复用技能封装（Skill）、密钥与凭证安全托管（Credential/Vault）、部署配置（Deployment）及外部系统集成（Webhook）。完整能力清单见 [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md) 的子章节导航。

## 关键参数

- `agent_id`（必填，路径参数）：Agent 唯一标识符，由平台在创建时生成，不可自定义。  
- `session_id`（可选，Header 或 Query）：显式指定会话上下文；若未提供，API 自动创建新会话（详见 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)）。  
- `enable_memory`（Body 参数，布尔值，默认 `true`）：控制是否启用 Memory Store 关联；设为 `false` 时，本次请求不读写[长期记忆](../concepts/long-term-memory.md)。  
- `tool_choice`（Body 参数，字符串或对象）：指定强制调用的 Skill 名称或 `"auto"`；注意该字段行为与 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 文档中描述一致，但部分旧版示例误写为 `tools_enabled` —— 请以该文档为准。

> **注意**：原始文档中 `raw/application-api-reference/managed-agents-api/agent-api.md` 与 `raw/application-api-reference/managed-agents-api/skills-api.md` 对 `tool_choice` 的枚举值描述存在不一致（前者列出 `"none"`，后者未包含），实际生效值以 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 为准。

## 使用方式

1. **认证**：使用 Bearer Token，通过 `Authorization: Bearer <api_key>` 传入；API Key 需具备 `managed_agents:read` 或 `managed_agents:write` 权限（参见 [认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-authentication.md)）。  
2. **典型流程**：  
   - `POST /v1/agents` 创建 Agent（含默认 Environment 和 Memory Store）  
   - `POST /v1/agents/{agent_id}/sessions` 启动会话  
   - `POST /v1/agents/{agent_id}/sessions/{session_id}/chat` 发送用户消息并流式接收响应  
3. 所有 API 均遵循统一错误格式，常见错误码（如 `400 BAD_REQUEST`、`429 RATE_LIMIT_EXCEEDED`）定义见 [错误码](../../raw/application-api-reference/managed-agents-api/managed-agents-api-errors.md)。

## 限制和注意事项

- 单个 Agent 最多关联 10 个独立 Environment；单个 Environment 下最多运行 100 个并发 Session。  
- Memory Store 默认保留最近 100 条记忆条目，超出后按 LRU 清理；如需更大容量，须在创建时显式设置 `memory_capacity` 参数（见 [Memory Store](../../raw/application-api-reference/managed-agents-api/memory-store-api.md)）。  
- 文件上传（`/files`）最大单文件为 100 MB，且仅支持 `text/plain`、`application/pdf`、`application/vnd.openxmlformats-officedocument.wordprocessingml.document` 等白名单 MIME 类型。  
- Webhook 回调 URL 必须为 HTTPS，且需在 5 秒内返回 `2xx` 响应，否则视为失败并触发重试（最多 3 次）；详细契约见 [Webhook](../../raw/application-api-reference/managed-agents-api/webhook-api.md)。

## 来源文档

- [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)


