# managed agents api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和运行具备长期记忆、工具调用、多步推理能力的自主 Agent。该 API 封装了环境管理、会话生命周期、文件与凭证安全存储等底层复杂性，开发者可通过声明式方式定义 Agent 行为。所有核心资源（如 `Agent`、`Environment`、`Session`）均通过 RESTful 接口暴露，并支持细粒度权限控制。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 系统模型；自定义模型或第三方模型暂不支持接入 Managed Agents 框架。  
- **核心功能**：包括多轮会话管理、结构化 Memory Store（支持向量与键值双模式）、内置 Skill 编排（如 WebSearch、CodeInterpreter）、Vault 加密凭证注入、以及基于 Webhook 的事件回调。详细能力边界请参阅 [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md) 的子模块说明。  
- **扩展能力**：可通过 `Skill` 资源注册自定义函数（需符合 OpenAPI 3.0 规范），但函数执行沙箱仅支持 Python 3.11 运行时，且超时上限为 30 秒 —— 此限制在 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 文档中有明确说明。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 必须为平台预置模型 ID（如 `"qwen-max"`），不接受模型别名或 URL；详见 [概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) |
| `memory_store_type` | string | 否 | 可选 `"vector"` 或 `"kv"`；若未指定，默认为 `"vector"`，但 `kv` 模式不支持语义检索 |
| `enable_webhook` | boolean | 否 | 设为 `true` 时需同步提供 `webhook_url` 和 `webhook_secret`，否则创建失败 |
| `timeout_seconds` | integer | 否 | 单次 Agent 执行最大耗时，范围 `5–300`，默认 `120`；超出将触发 `AGENT_EXECUTION_TIMEOUT` 错误 |

> **注意**：`memory_store_type=kv` 在 [Memory Store](../../raw/application-api-reference/managed-agents-api/memory-store-api.md) 文档中被标记为“实验性”，生产环境不建议启用；而 [概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中未注明该状态，以 Memory Store 文档为准。

## 使用方式

1. **认证**：使用平台颁发的 `X-DashScope-Token` 请求头（非 AccessKey），[Token](../concepts/token.md) 需通过 `/v1/auth/token` 接口获取，有效期 1 小时；认证流程详见 [认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-authentication.md)。  
2. **创建 Agent**：`POST /v1/agents`，传入 JSON body 定义模型、skills、memory 等配置；成功返回 `agent_id`。  
3. **启动会话**：`POST /v1/sessions`，指定 `agent_id` 和初始 `input`，获得 `session_id` 与首条响应。后续消息通过 `POST /v1/sessions/{session_id}/messages` 流式追加。  
4. **调试建议**：首次集成务必查阅 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)，其中包含 cURL 示例与常见 HTTP 状态码对照表。

## 限制和注意事项

- **配额限制**：单个账号默认最多创建 50 个 Agent 实例，每个 Agent 最多关联 100 个 Skill；超出需提交工单申请扩容。  
- **文件限制**：通过 `/files` 上传的文件单个 ≤ 100 MB，总存储空间 ≤ 10 GB（按账号计）；文件元数据不支持自定义标签。  
- **事件可靠性**：Webhook 投递为尽力而为（at-least-once），若目标服务连续 3 次返回非 `2xx` 响应，系统将暂停投递并记录告警 —— 具体重试策略见 [Webhook](../../raw/application-api-reference/managed-agents-api/webhook-api.md)。  
- **错误处理**：所有错误均遵循统一错误格式，含 `error_code`（如 `INVALID_PARAMETER`）与 `request_id`；完整错误码列表请参考 [错误码](../../raw/application-api-reference/managed-agents-api/managed-agents-api-errors.md)。

## 来源文档

- [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)


