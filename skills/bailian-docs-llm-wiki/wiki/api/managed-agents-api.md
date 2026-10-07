# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和运行具备[长期记忆](../concepts/memory.md)、工具调用、多步推理能力的 AI Agent。该 API 将底层基础设施（如环境隔离、状态持久化、凭证管理）抽象为标准化资源，开发者可聚焦于业务逻辑编排。所有操作均通过 RESTful 接口完成，支持细粒度权限控制与异步事件驱动。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款大模型，不支持自定义模型或外部模型接入。  
- **核心功能**：包括 Agent 生命周期管理、Session 状态追踪、Memory Store 持久化存储、Skill 插件注册、Vault 安全凭证管理、Environment 隔离配置，以及 Webhook 事件回调。完整能力列表见 [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)。  
- **扩展能力**：可通过 Skills API 注册自定义工具（如 HTTP 请求、数据库查询），并由 Agent 自动规划调用；Memory Store 支持向量检索与结构化元数据过滤，详见 [Memory Store](../../raw/application-api-reference/managed-agents-api/memory-store-api.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `agent_id` | string | 是 | Agent 唯一标识符，由平台生成或用户指定（需全局唯一） |
| `session_id` | string | 否 | Session 上下文 ID；若未提供，API 自动创建新 Session |
| `input` | object | 是 | 用户输入内容，格式为 `{ "text": "..." }` 或 `{ "files": [...] }` |
| `stream` | boolean | 否 | 是否启用流式响应，默认 `false`；启用后返回 SSE 格式事件流 |
| `max_steps` | integer | 否 | 单次执行最大推理步数，取值范围 `1–50`，默认 `30` |

> **注意**：`max_steps` 的默认值在 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 文档中记为 `25`，但实际 API 行为以 `30` 为准（v2.3.0+ 版本已同步更新）。请以运行时响应头 `X-Default-Max-Steps: 30` 为准。

## 使用方式

1. **初始化 Agent**：调用 `POST /v1/agents` 创建 Agent 实例，传入 `model_id`、`skills` 列表及 `memory_store_id`（可选）；  
2. **启动交互**：使用 `POST /v1/agents/{agent_id}/sessions/{session_id}/chat` 发送用户输入；若省略 `session_id`，将自动创建新 Session；  
3. **事件监听**：配置 Webhook（见 [Webhook](../../raw/application-api-reference/managed-agents-api/webhook-api.md)）接收 `agent.step_completed`、`agent.execution_failed` 等事件；  
4. **文件与凭证**：上传文件前需先调用 Files API 获取预签名 URL；敏感凭证应存入 Vault 并通过 Credential API 绑定至 Agent。

## 限制和注意事项

- 单个 Agent 最多关联 100 个 Skill，单个 Session 内存上下文上限为 10MB（含历史消息与 Memory Store 检索结果）；  
- 所有文件上传需经 Files API 中转，禁止直接 POST 至 Agent 接口；  
- Memory Store 的向量索引更新存在最多 2 秒延迟，高实时性场景需主动调用 `POST /v1/memory_stores/{id}/sync`；  
- Agent 执行超时时间为 120 秒（含模型推理、Tool 调用、网络等待），不可配置；  
- 当前不支持跨 Region 调用，Agent、Environment、Vault 必须位于同一地域。

## 来源文档

- [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)


