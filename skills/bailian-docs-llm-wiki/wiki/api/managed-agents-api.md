# managed agents api

Managed Agents API 是百炼平台提供的用于构建、部署和管理智能体（Agent）的 RESTful 接口集合，支持从环境配置、会话生命周期、技能编排到凭证与内存存储的全栈控制。该 API 采用标准 HTTP 协议，需通过 Bearer [Token](../concepts/token.md) 认证，适用于需要细粒度控制 Agent 行为的中高级开发者场景。详细设计原则与架构约束请参阅 [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)。

## 支持的模型与功能

- **核心能力**：支持创建可复用的 Agent 实例，并通过 Environment 隔离运行上下文；支持 Session 管理多轮对话状态，Event 机制实现异步事件驱动交互。
- **扩展能力**：提供 File API 上传/引用外部文档，Memory Store API 持久化对话记忆，Skills API 注册自定义工具函数，Vault/Credential API 安全托管敏感凭据。
- 当前仅支持百炼平台托管的推理模型（如 `qwen-max`、`qwen-plus`），不支持用户自定义模型后端。具体模型兼容性详见 [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md) 中的 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 和 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md) 子文档。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `agent_id` | string | 是 | Agent 唯一标识符，由 `/agents` 创建接口返回 |
| `session_id` | string | 否（首次调用可省略） | 用于关联多轮会话，若未提供则自动创建新会话 |
| `input` | object | 是 | 用户输入内容，结构为 `{ "text": "..." }` 或 `{ "files": ["file_id1", "..."] }` |
| `stream` | boolean | 否，默认 `false` | 设为 `true` 时启用 Server-Sent Events (SSE) 流式响应 |

> **注意**：`stream=true` 时，响应格式与非流式不同（如无 `output` 字段，而是 `delta` 事件流），该行为在 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md) 文档中有明确定义，但部分旧版 SDK 示例仍按同步格式解析，需以该文档为准。

## 使用方式

1. **认证**：在请求 Header 中携带 `Authorization: Bearer <access_token>`，[Token](../concepts/token.md) 通过 [认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-authentication.md) 流程获取；
2. **发起调用**：向 `POST /v1/agents/{agent_id}/sessions` 发送请求启动会话，后续轮次使用 `POST /v1/sessions/{session_id}/messages`；
3. **处理响应**：同步调用返回 JSON 对象含 `output.text` 和 `output.files`；流式调用需按 SSE 格式解析 `data:` 行。

快速上手示例见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)，其中包含 cURL 与 Python requests 完整代码片段。

## 限制和注意事项

- 单个 Agent 最多关联 100 个 Skill；单个 Session 生命周期最长 24 小时，超时后 `session_id` 失效；
- Memory Store 默认 TTL 为 7 天，不可修改；File API 上传文件大小上限为 100 MB，且仅支持 `pdf`, `txt`, `md`, `csv`, `xlsx` 格式；
- 所有 API 均遵循平台全局速率限制（默认 10 QPS / 租户），超出将返回 `429 Too Many Requests`，错误码详情见 [错误码](../../raw/application-api-reference/managed-agents-api/managed-agents-api-errors.md)。

## 来源文档

- [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)


