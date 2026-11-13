# managed agents api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和管理具备[长期记忆](../concepts/long-term-memory.md)、工具调用、多轮会话与环境隔离能力的 AI Agent。该 API 以 RESTful 形式提供，支持细粒度资源控制（如 Environment、Session、Memory Store）和可扩展能力（如 Skill、Vault、Webhook）。开发者可通过它构建生产级自动化工作流，无需自行维护底层推理与状态管理逻辑。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 系统模型；自定义模型暂不支持接入 Managed Agents。  
- **核心功能**：包括会话生命周期管理（Session）、持久化记忆存储（Memory Store）、安全凭证管理（Credential）、外部工具集成（Skill）、文件上传与引用（File）、环境隔离（Environment）、部署配置（Deployment）及事件回调（Webhook）。完整能力列表见 [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md) 的子模块索引。

## 关键参数

- `agent_id`：必填，通过 `/agents` 创建后返回的唯一标识符。  
- `session_id`：可选但推荐，用于关联同一用户上下文；若未提供，系统将自动生成临时 session。  
- `memory_store_id`：指定会话级记忆存储实例，必须已通过 `/memory-stores` 创建并处于 `active` 状态。  
- `tool_choice`：控制工具调用策略，支持 `"auto"`、`"none"` 或显式指定 Skill ID；默认为 `"auto"`。  
- `stream`：布尔值，启用流式响应时设为 `true`，此时需按 SSE 协议解析事件（详见 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)）。

## 使用方式

1. **认证**：使用 Bearer Token 方式，在 `Authorization` 请求头中传入平台颁发的 API Key（格式：`Bearer <api_key>`），认证流程详见 [认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-authentication.md)。  
2. **快速启动**：建议从 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 文档入手，其中包含 cURL 示例与最小可行请求体结构。  
3. **典型调用链**：先创建 Agent → 创建 Environment → 创建 Memory Store → 启动 Session → 发送用户消息（POST `/sessions/{session_id}/messages`）。所有资源路径均遵循 REST 规范，具体字段定义参见各子 API 文档，例如 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 和 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)。

## 限制和注意事项

- 单个 Agent 最多关联 100 个 Environment；单个 Environment 下最多运行 50 个并发 Session。  
- Memory Store 默认 TTL 为 7 天，不可修改；如需长期保留，请定期调用 `PATCH /memory-stores/{id}` 更新 `expires_at`（仅限企业版）。  
- > **注意**：[概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中提及“支持任意 HuggingFace 模型”，该描述已过时；实际仅支持百炼托管模型，以本页及 [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md) 主文档为准。  
- 文件上传大小上限为 100 MB，且仅支持 `text/plain`、`application/pdf`、`text/csv`、`application/json` 四类 MIME 类型。  
- 所有 Webhook 回调必须在 5 秒内返回 HTTP 2xx 响应，超时将触发重试（最多 3 次），详情见 [Webhook](../../raw/application-api-reference/managed-agents-api/webhook-api.md)。

## 来源文档

- [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)


