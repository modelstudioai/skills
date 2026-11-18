# managed agents api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和管理具备[长期记忆](../concepts/long-term-memory.md)、工具调用、多轮会话与环境隔离能力的 AI Agent。该 API 以 RESTful 形式提供，支持细粒度资源控制（如 Environment、Session、Memory Store）和可扩展能力（如 Skill、Vault、Webhook）。开发者可通过它构建生产级自动化工作流，无需自行维护底层推理与状态管理逻辑。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 等 Qwen 系列模型；不支持用户自定义模型或外部模型接入。  
- **核心功能模块**包括：Agent 生命周期管理、隔离式运行环境（Environment）、有状态会话（Session）、持久化记忆存储（Memory Store）、安全凭证管理（Credential）、技能封装（Skill）、文件处理（File）、密钥保险库（Vault）、部署配置（Deployment）及事件回调（Webhook）。完整能力清单详见 [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md) 的子模块索引。

## 关键参数

- `agent_id`：必填，由 `/agents` 创建后返回的唯一标识符，用于后续所有资源操作。  
- `environment_id`：可选但推荐，指定 Agent 运行的隔离环境；若未指定，则使用默认环境（可能影响多租户安全性）。  
- `session_id`：会话级状态标识，需在 `/sessions` 中显式创建，用于跨请求维持上下文与 Memory Store 绑定。  
- `memory_store_id`：若启用[长期记忆](../concepts/long-term-memory.md)，必须关联已创建的 Memory Store 实例，其 TTL 和访问策略需提前配置。  
- `webhook_url`：仅在注册 Webhook 时生效，须为 HTTPS 端点且响应超时 ≤3s；详细约束见 [Webhook](../../raw/application-api-reference/managed-agents-api/webhook-api.md) 文档。

## 使用方式

1. **认证**：使用平台颁发的 `API Key`，通过 `Authorization: Bearer <api_key>` 请求头传递；JWT Token 方式暂不支持（参见 [认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-authentication.md)）。  
2. **快速启动**：按顺序调用：`POST /agents` → `POST /environments` → `POST /sessions` → `POST /sessions/{session_id}/messages`；完整流程见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)。  
3. **调试建议**：首次集成时务必启用 `X-Bailian-Debug: true` 请求头，以获取详细的执行链路日志（含 Skill 调用、Memory 读写、Tool 执行等）。

## 限制和注意事项

- 单个 Agent 最多绑定 10 个 Skill，单个 Environment 最多承载 50 个并发 Session；超出将返回 `429 Too Many Requests`。  
- Memory Store 默认保留 7 天，不可修改 TTL；若需更长周期，请改用外部数据库 + 自定义 Skill 同步（[Memory Store](../../raw/application-api-reference/managed-agents-api/memory-store-api.md) 明确说明无 `expire_at` 字段）。  
> **注意**：原始文档中 [Deployment](../../raw/application-api-reference/managed-agents-api/deployment-api.md) 提到支持 `autoscale: true` 参数，但实测该字段已被忽略，当前所有 Deployment 均为固定规格（vCPU=2, RAM=4GB），该描述已过时。  
- 文件上传最大单文件为 100MB，且仅支持 `application/pdf`, `text/plain`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document` 三种 MIME 类型；其他格式将被静默拒绝（[File](../../raw/application-api-reference/managed-agents-api/files-api.md) 未明确列出全部限制，需以实际 API 响应为准）。

## 来源文档

- [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)


