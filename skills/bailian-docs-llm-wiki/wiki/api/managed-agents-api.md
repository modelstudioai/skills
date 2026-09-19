# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和运行具备[长期记忆](../concepts/memory.md)、工具调用、多步推理能力的 AI Agent。该 API 将底层基础设施（如环境隔离、状态持久化、凭证管理）抽象为标准化资源，开发者可聚焦于业务逻辑编排。所有操作均通过 RESTful 接口完成，支持细粒度权限控制与异步事件驱动。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款大模型，不支持自定义模型或外部模型接入。  
- **核心功能**：包括 Agent 生命周期管理、Session 状态追踪、Memory Store 持久化存储、Skill 插件注册、Vault 安全凭证管理、Environment 隔离运行时、File 上传/引用、Webhook 事件回调等。完整能力列表见 [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)。  
- **扩展能力**：可通过 Skill 接口集成自定义工具（如 HTTP 请求、数据库查询），并通过 Memory Store 实现跨 Session 的上下文继承；相关实现细节参见 [Memory Store](../../raw/application-api-reference/managed-agents-api/memory-store-api.md) 和 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `agent_id` | string | 是 | Agent 唯一标识符，由平台生成或用户指定（需全局唯一） |
| `session_id` | string | 否 | Session 上下文 ID；未提供时自动创建新 Session |
| `input` | object | 是 | 用户输入内容，格式为 `{ "text": "..." }` 或 `{ "files": [...] }` |
| `stream` | boolean | 否 | 是否启用流式响应，默认 `false`；启用后返回 SSE 格式事件流 |
| `max_steps` | integer | 否 | 单次执行最大推理步数，取值范围 1–50，默认 20 |

> **注意**：`max_steps` 在 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 文档中定义为必填项，但实际 API 允许省略（使用默认值），此为文档过时描述，请以实际接口行为为准。

## 使用方式

1. **认证**：使用 `X-DashScope-Access-Token` 请求头传递 API Key（非 Bearer [Token](../concepts/token.md)）；认证机制详见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。  
2. **发起调用**：向 `POST /v1/agents/{agent_id}/sessions/{session_id}/run` 发送请求（若未指定 `session_id`，则先调用 `/v1/agents/{agent_id}/sessions` 创建）。  
3. **处理响应**：同步模式返回 JSON 对象；流式模式需按 `data:` 行解析事件，关键事件类型包括 `agent_message`、`tool_call`、`tool_result`、`session_end`。

## 限制和注意事项

- **速率限制**：单个 `agent_id` 最高 10 QPS，突发流量触发 429 响应；企业版客户可申请提升配额。  
- **Session 生命周期**：空闲超时时间为 30 分钟，超时后关联 Memory Store 数据仍保留（受 TTL 策略约束），但 Session 不可恢复。  
- **文件限制**：单次上传文件总大小 ≤ 100 MB，支持格式包括 PDF、TXT、DOCX、XLSX、PNG、JPEG；文件元数据通过 `/files` 接口预注册后，在 `input.files` 中引用。  
- **调试建议**：首次集成推荐从 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 入手，该文档包含可直接运行的 cURL 示例与错误码速查表。

## 来源文档

- [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)


