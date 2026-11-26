# managed agents api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和运行具备[长期记忆](../concepts/long-term-memory.md)、工具调用、多步推理能力的 AI Agent。该 API 将底层模型调度、状态管理、技能编排等复杂逻辑封装为标准化资源操作（如 `Agent`、`Environment`、`Session`），开发者可通过 RESTful 接口快速集成。所有核心能力均基于百炼统一认证与配额体系，详见 [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列模型；其他模型（如 `qwen2.5-*`）暂未开放 Agent 模式推理通道，具体以 [Agent API](../../raw/application-api-reference/managed-agents-api/agent-api.md) 文档为准。
- **核心功能**：
  - 多轮 Session 管理（含事件流式返回）
  - 内置 Memory Store 实现跨会话上下文持久化
  - Vault + Credential 组合实现安全凭证注入
  - Skills 插件机制支持自定义工具注册与调用
  - Webhook 回调支持异步任务结果通知

> **注意**：原始文档中 [Environment API](../../raw/application-api-reference/managed-agents-api/environment-api.md) 提到支持“自定义 Docker 镜像部署”，但该能力已于 v2.3 版本下线；实际仅支持平台预置的沙箱环境，最新约束请以 [Deployment API](../../raw/application-api-reference/managed-agents-api/deployment-api.md) 为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `agent_id` | string | 是 | 通过 `/v1/agents` 创建后返回的唯一标识 |
| `session_id` | string | 否 | 复用已有会话时传入；不传则新建会话（自动绑定 Memory Store） |
| `input` | object | 是 | 用户输入内容，结构为 `{ "text": "..." }` 或 `{ "files": [...] }` |
| `stream` | boolean | 否 | `true` 时启用 Server-Sent Events 流式响应，默认 `false` |
| `tools` | array | 否 | 显式指定本次调用可使用的 Skill ID 列表，优先级高于 Agent 全局配置 |

## 使用方式

1. **前置准备**：使用平台颁发的 `API Key` 进行 Bearer 认证（参考 [认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-authentication.md)）；
2. **创建 Agent**：`POST /v1/agents`，需指定 `model`, `skills`, `memory_store_id` 等；
3. **发起调用**：`POST /v1/agents/{agent_id}/sessions`，传入 `input` 及可选参数；
4. **获取结果**：同步响应返回 `session_id` 和首条 `output`；若启用 `stream=true`，则通过 SSE 获取 `event: message` 和 `event: tool_call` 等事件。

## 限制和注意事项

- 单次 `input.text` 长度上限为 32,768 字符；文件上传单个不超过 100 MB（见 [Files API](../../raw/application-api-reference/managed-agents-api/files-api.md)）；
- 每个 Agent 默认最多关联 1 个 Memory Store，且不可在运行时动态切换；
- Session 生命周期默认 24 小时，超时后 `session_id` 失效，需重新创建；
- 错误响应遵循统一格式，常见错误码（如 `429 Too Many Requests`、`403 Forbidden`）含义详见 [错误码](../../raw/application-api-reference/managed-agents-api/managed-agents-api-errors.md)。

## 来源文档

- [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)


