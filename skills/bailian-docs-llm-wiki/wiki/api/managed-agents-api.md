# managed agents api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和运行具备[长期记忆](../concepts/long-term-memory.md)、工具调用、多步推理能力的 AI Agent。该 API 封装了环境管理、会话生命周期、文件与凭证存储、技能编排等底层复杂性，开发者可通过 RESTful 接口快速集成。详细设计目标与架构约束可参见 [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列大模型；不支持第三方模型或自定义模型权重上传。
- **核心功能**：
  - 基于 `Agent` 资源定义行为逻辑（含 system prompt、tool schema、memory policy）；
  - 通过 `Environment` 隔离运行上下文（如开发/生产环境）；
  - 利用 `Memory Store` 实现跨会话持久化记忆，支持向量检索与结构化元数据过滤；
  - 通过 `Skill` 注册并复用预置或自定义工具（如 HTTP 请求、数据库查询、文件解析），详见 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md) 文档。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `agent_id` | string | 是 | Agent 实例唯一标识，由 `/agents` 创建后返回，后续所有资源操作均需携带 |
| `session_id` | string | 否（首次调用可省略） | 指定会话上下文；若未提供，API 自动创建新会话并返回 ID；会话默认 TTL 为 24 小时 |
| `stream` | boolean | 否，默认 `false` | 设为 `true` 时启用 SSE 流式响应，适用于长任务或实时交互场景 |
| `max_steps` | integer | 否，默认 `15` | 单次请求中 Agent 允许执行的最大推理+工具调用步数，超限将终止并返回 `error_code: STEP_LIMIT_EXCEEDED` |

> **注意**：原始文档中 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 的 `model` 字段描述为“支持任意百炼已上线模型”，但实际调用时若传入 `qwen-vl` 或 `qwen-audio` 将返回 `MODEL_NOT_SUPPORTED` 错误——该字段说明已过时，请以本节为准。

## 使用方式

1. **认证**：使用平台颁发的 `API Key`，通过 `Authorization: Bearer <api_key>` 请求头传递；密钥需具备 `managed_agents:read` 和 `managed_agents:write` 权限。
2. **创建 Agent**：`POST /v1/agents`，传入 JSON body 定义基础配置（name、description、model、tools）。
3. **启动会话并运行**：`POST /v1/agents/{agent_id}/sessions`（可选带 `session_id` 复用），随后 `POST /v1/sessions/{session_id}/run` 提交用户输入。
4. **状态轮询或 Webhook 回调**：非流式调用需轮询 `GET /v1/sessions/{session_id}`；也可配置 [Webhook](../../raw/application-api-reference/managed-agents-api/webhook-api.md) 实现事件驱动。

## 限制和注意事项

- 单个 Agent 最多绑定 50 个 `Skill`；单次 `run` 请求最大输入长度为 32768 token（含 system prompt + history + user input）。
- `Memory Store` 中单条记忆最大 size 为 4096 字符，且仅对 `text` 类型字段建立向量索引；`metadata` 字段不参与语义检索。
- 所有文件上传（通过 `/files`）必须先关联到 `Vault`，且 Vault 必须已绑定至目标 `Environment`——此依赖关系在 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md) 文档中有明确定义，但部分旧版示例代码遗漏了该步骤，易导致 `VAULT_NOT_BOUND` 错误。

## 来源文档

- [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)


