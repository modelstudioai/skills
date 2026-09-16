# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和运行具备[长期记忆](../concepts/long-term-memory.md)、工具调用与多步推理能力的 AI Agent。该 API 将底层环境管理、会话状态、文件存储、技能编排等能力封装为标准化资源（如 `Agent`、`Environment`、`Session`、`Vault`），开发者可通过 RESTful 接口按需组合。所有操作均需通过平台认证，并遵循统一的请求/响应结构与错误码规范。

## 支持的模型与功能

Managed Agents API 本身不直接绑定特定大模型，而是通过 `Environment` 资源指定运行时模型（如 `qwen-max`、`qwen-plus` 或自定义微调模型）。核心功能包括：  
- 基于 `Agent` 定义行为逻辑（提示词、工具列表、终止条件）；  
- 通过 `Environment` 配置模型、温度、最大 token 数等推理参数；  
- 利用 `Session` 管理用户级上下文与历史事件流；  
- 使用 `Vault` 和 `Credential` 安全存储敏感数据与外部服务凭据；  
- 通过 `Webhook` 实现异步事件通知（如任务完成、工具调用失败）。  
详细资源能力请参阅 [Managed Agents](../../raw/application-api-reference/managed-agents-api.md) 的子模块文档。

## 关键参数

所有写操作（如 `POST /v1/agents`）需在请求体中提供以下关键字段：  
- `name`: 字符串，长度 ≤ 64，仅支持字母、数字、下划线、短横线；  
- `environment_id`: 必填，指向已创建的 `Environment` 资源 ID；  
- `skills`: 工具列表，每个元素含 `id`（对应 `Skill` 资源 ID）及可选 `config`；  
- `session_ttl_seconds`: `Session` 默认存活时间，范围 300–86400（5 分钟至 24 小时）；  
- `max_iterations`: 单次会话中 Agent 最大推理步数，默认 15，上限 50。  
> **注意**：`max_iterations` 在 [agent-api.md](../../raw/application-api-reference/managed-agents-api/agent-api.md) 中定义为必填，但 [managed-agents-quickstart.md](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 示例中省略且仍可创建成功——实际以 API Schema 校验为准，建议显式设置。

## 使用方式

1. **初始化环境**：先调用 `POST /v1/environments` 创建 `Environment`，指定 `model` 和推理参数；  
2. **注册技能**：通过 `POST /v1/skills` 注册工具（如 HTTP 请求、数据库查询），并关联 `Credential`（若需鉴权）；  
3. **创建 Agent**：`POST /v1/agents`，传入 `environment_id` 和 `skills` 列表；  
4. **启动会话**：`POST /v1/sessions` 获取 `session_id`，再向 `POST /v1/sessions/{id}/messages` 发送用户消息；  
5. **监听结果**：配置 `Webhook` 接收 `session.completed` 或 `tool.error` 事件。  
完整流程示例见 [Managed Agents Quickstart](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)。

## 限制和注意事项

- 单个 `Agent` 最多绑定 20 个 `Skill`；单个 `Vault` 最多存储 100 条密钥；  
- `Session` 生命周期内最多保留 100 条消息（含系统与用户消息），超出部分自动截断；  
- 所有文件上传（`POST /v1/files`）须经 `Vault` 或 `Credential` 授权，禁止明文传递敏感内容；  
- `Deployment` 资源目前仅支持灰度发布，生产环境部署需人工审批，详情见 [Deployment API](../../raw/application-api-reference/managed-agents-api/deployment-api.md)。

## 来源文档

- [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)


