# managed agents api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和管理具备[长期记忆](../concepts/long-term-memory.md)、工具调用、多轮会话与环境隔离能力的 AI Agent。该 API 以 RESTful 形式提供，支持细粒度资源控制（如 Environment、Session、Memory Store）和可扩展能力（如 Skill、Vault、Webhook）。开发者可通过它构建生产级自动化工作流，无需自行维护底层推理与状态管理逻辑。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 等 Qwen 系列模型；不支持用户自定义模型或第三方模型接入。  
- **核心功能模块**包括：Agent 生命周期管理、隔离式运行环境（Environment）、带上下文感知的会话（Session）、持久化记忆存储（Memory Store）、结构化文件处理（Files API）、可复用技能封装（Skill）、安全凭证管理（Credential）、密钥保险库（Vault）、部署配置（Deployment）及事件通知（Webhook）。完整能力清单详见 [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md) 的子章节导航。

## 关键参数

- `agent_id`：必填，Agent 唯一标识符，由 `/agents` 创建接口返回；  
- `session_id`：会话级状态隔离关键字段，首次调用 `/sessions` 时生成，后续请求需显式携带；  
- `memory_store_id`：若启用[长期记忆](../concepts/long-term-memory.md)，必须关联已创建的 Memory Store 实例；  
- `tool_choice`：控制工具调用策略，支持 `"auto"`、`"none"` 或指定 Skill ID 列表；  
- `max_iterations`：默认为 `15`，防止无限循环，可在 `/agents/{id}/deploy` 中覆盖。  
更多参数语义与约束请参考 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 和 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md) 的原始定义。

## 使用方式

1. **认证**：使用平台颁发的 `X-DashScope-Access-Token` 请求头（非 Bearer Token），有效期 24 小时；  
2. **快速启动**：按 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 文档顺序调用：`POST /environments` → `POST /agents` → `POST /sessions` → `POST /sessions/{id}/messages`；  
3. **调试建议**：首次集成时务必启用 `debug: true` 参数，并检查 `/usage` 接口返回的 token 消耗与调用链路追踪 ID。

## 限制和注意事项

- 单个 Agent 最多绑定 10 个 Skill，单个 Session 内存上下文上限为 32KB（含历史消息与 Memory Store 合并结果）；  
- Environment 不支持跨区域复制，且一旦绑定 Agent 后不可迁移；  
- > **注意**：[概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中提及的 “支持异步批量会话提交” 功能尚未上线，实际行为仍为同步响应，该描述已过时，请以 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md) 的最新说明为准；  
- 所有文件上传（`/files`）必须通过预签名 URL 完成，直接 POST 文件体将返回 `400 Bad Request`；  
- Vault 中存储的敏感值在 Agent 运行时自动注入环境变量，但不会出现在日志或调试输出中——此行为由 [Vault](../../raw/application-api-reference/managed-agents-api/vault-api.md) 和 [Credential](../../raw/application-api-reference/managed-agents-api/credential-api.md) 双文档共同约定。

## 来源文档

- [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)


