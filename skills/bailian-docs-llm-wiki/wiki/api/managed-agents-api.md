# managed agents api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和管理具备[长期记忆](../concepts/long-term-memory.md)、工具调用、多轮会话与环境隔离能力的 AI Agent。该 API 以 RESTful 形式提供，支持细粒度资源控制（如 Environment、Session、Memory Store）和可扩展能力（如 Skill、Vault、Webhook）。开发者可通过它构建生产级自动化工作流，无需自行维护底层推理与状态管理逻辑。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 等 Qwen 系列模型；不支持用户自定义模型或外部模型接入。  
- **核心功能模块**包括：Agent 生命周期管理、隔离式运行环境（Environment）、有状态会话（Session）、持久化记忆存储（Memory Store）、安全凭证管理（Credential）、技能封装（Skill）、文件处理（File）、密钥保险库（Vault）、部署配置（Deployment）及事件回调（Webhook）。完整能力清单详见 [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md) 的子章节导航。

## 关键参数

- `agent_id`：必填，由 `/agents` 创建后返回的唯一标识符，用于后续所有资源操作。  
- `environment_id`：可选但强烈推荐，指定 Agent 运行的隔离环境；未指定时默认使用 `default` 环境，该行为可能引发资源冲突（见 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md) 文档说明）。  
- `session_id`：会话级状态标识，需在 `/sessions` 中显式创建；重复使用同一 `session_id` 可延续上下文与 Memory Store 数据。  
- `tool_choice`：控制工具调用策略，支持 `"auto"`、`"none"` 或指定 Skill ID 列表；若设为 `"auto"` 但未注册任何 Skill，请求将直接失败（参见 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md) 接口规范）。

## 使用方式

1. **认证**：使用平台颁发的 `API-Key`（非 AccessKey），通过 `Authorization: Bearer <api_key>` 头传递；JWT 认证暂不支持。  
2. **典型流程**：  
   - 调用 `POST /v1/agents` 创建 Agent；  
   - （可选）调用 `POST /v1/environments` 配置专用 Environment；  
   - 调用 `POST /v1/sessions` 初始化会话；  
   - 调用 `POST /v1/sessions/{session_id}/chat` 发起交互，携带 `messages` 与 `tools`（如有）。  
3. 所有路径均以 `/v1/` 为前缀，例如 `/v1/agents`；完整端点列表请参考 [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md) 的目录结构。

## 限制和注意事项

- 单个 Agent 最多绑定 50 个 Skill；单次请求最多调用 5 个工具（含嵌套调用），超出将触发 `400 Bad Request`。  
- Memory Store 默认 TTL 为 7 天，不可修改；若需长期保留，须主动调用 `/memory_store/{id}/export` 导出并另行存档。  
- > **注意**：[快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 文档中示例仍使用 `/api/v1/` 前缀，该路径已废弃；实际应使用 `/v1/`（见 [概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 的版本说明）。  
- 文件上传（`/files`）最大单文件为 100 MB，且仅支持 `text/plain`、`application/json`、`application/pdf` 三种 MIME 类型；其他类型将被静默拒绝，不返回明确错误码（此行为与 [File](../../raw/application-api-reference/managed-agents-api/files-api.md) 文档描述一致）。

## 来源文档

- [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)


