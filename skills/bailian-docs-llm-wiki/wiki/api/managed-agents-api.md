# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和管理具备[长期记忆](../concepts/memory.md)、工具调用、多会话支持等能力的 AI Agent。该 API 以 RESTful 形式提供，支持细粒度资源控制（如 Environment、Session、Memory Store）和安全凭证管理（Vault/Credential）。开发者可通过组合基础模块快速构建生产级自动化工作流。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 等 Qwen 系列大模型；不支持用户自定义模型或外部模型接入。  
- **核心功能**：包括 Agent 生命周期管理、带状态的 Session 控制、结构化 Memory Store 持久化、文件上传/引用（支持 PDF/DOCX/TXT）、内置 Skill 编排（如 WebSearch、CodeInterpreter）、环境隔离（Environment）、密钥安全存储（Vault）及事件驱动 Webhook 回调。详细能力请参阅 [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)。

## 关键参数

- `agent_id`（必填）：Agent 实例唯一标识，由 `/agents` 创建接口返回。  
- `session_id`（可选但推荐）：用于关联上下文，若未提供则自动创建新会话；同一 `session_id` 下的请求共享 Memory Store 和历史事件。  
- `stream`（布尔，默认 `false`）：启用流式响应时设为 `true`，此时需按 SSE 格式解析；注意 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md) 文档明确要求流式请求必须携带 `Accept: text/event-stream` 头。  
- `memory_store_id`（可选）：指定挂载的 Memory Store，否则使用 Agent 默认存储；该参数在 [Memory Store](../../raw/application-api-reference/managed-agents-api/memory-store-api.md) 中定义了 TTL 和容量限制。

## 使用方式

1. **初始化 Agent**：先通过 `POST /v1/agents` 创建 Agent 实例，可绑定 Environment、Skill 和默认 Vault。  
2. **发起调用**：向 `POST /v1/agents/{agent_id}/chat` 提交消息，附带 `session_id` 和可选 `files`（需提前通过 `/files` 上传并获取 `file_id`）。  
3. **管理状态**：使用 `/sessions/{session_id}/events` 查询执行轨迹，或通过 `/memory-stores/{id}/entries` 直接读写记忆条目。  
> **注意**：[Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 文档中示例使用的 `POST /agents/{id}/run` 路径已废弃，当前统一使用 `/chat` 接口；请以 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中的最新路由为准。

## 限制和注意事项

- 单次请求最大输入长度为 32768 token（含 system prompt + history + user input），超限将返回 `400 Bad Request`。  
- Memory Store 单条记录最大 8KB，总容量默认 1MB/Agent（可申请扩容）；超过 TTL（默认 7 天）自动清理。  
- 文件上传后有效期为 24 小时，且仅可在同 Environment 内的 Session 中引用；跨 Environment 使用需重新上传。  
- 所有敏感操作（如 Credential 创建、Vault 更新）需显式声明 `X-Bailian-Permission: manage-vaults` 请求头，否则拒绝执行——该权限要求在 [Credential](../../raw/application-api-reference/managed-agents-api/credential-api.md) 文档中有明确说明。

## 来源文档

- [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)


