# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于构建、部署和管理具备[长期记忆](../concepts/memory.md)、多工具调用与环境隔离能力的 AI 应用。它将 Agent 生命周期（创建、执行、状态管理）、运行时上下文（Environment、Session、Memory Store）、资源管控（File、Vault、Credential）及集成能力（Webhook、Skill、Deployment）统一抽象为 RESTful 接口。开发者无需自行维护推理服务或状态同步逻辑，可专注于业务逻辑编排 —— 详见 [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 系统预置模型；自定义模型暂不支持接入 Managed Agents 流程。
- **核心功能模块**：
  - `Agent`：定义智能体行为逻辑（[prompt](../guides/prompt.md)、tools、memory 配置等）；
  - `Environment`：隔离运行时依赖（如 Python 版本、第三方库）；
  - `Session` 与 `Event`：支持会话级状态追踪与事件驱动响应；
  - `Memory Store`：提供结构化[长期记忆](../concepts/memory.md)存储（支持向量检索与元数据过滤）；
  - `Skill`：封装可复用的原子能力（如查天气、发邮件），支持跨 Agent 复用；
  - `Vault` 与 `Credential`：安全托管敏感凭证，按需注入至 Skill 或 Environment；
  - `File`：上传/引用外部文件（PDF、CSV、JSON 等），自动触发解析与嵌入；
  - `Deployment`：一键发布 Agent 至生产环境，支持灰度与版本回滚；
  - `Webhook`：接收外部系统事件（如企业微信消息、CRM 更新），触发 Agent 执行。

> **注意**：[Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 文档中提及的 `model_id` 字段允许传入任意模型 ID，但实际调用时若非上述三款预置模型，将返回 `400 Bad Request`。该不一致已在 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 的“模型兼容性”章节中明确修正，请以该文档为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `agent_id` | string | 是 | Agent 唯一标识，由 `/v1/agents` 创建后返回 |
| `session_id` | string | 否 | 会话 ID；未提供时自动创建新会话；同一 `session_id` 下共享 Memory Store 与 Session State |
| `input` | object | 是 | 用户输入内容，格式为 `{ "text": "..." }` 或 `{ "files": ["file-xxx"] }` |
| `stream` | boolean | 否 | `true` 时启用 SSE 流式响应（推荐用于前端实时渲染） |
| `tool_choice` | string \| object | 否 | 控制工具调用策略，可选 `"auto"`、`"none"` 或指定 tool name；默认 `"auto"` |

所有请求需携带 `Authorization: Bearer <api_key>` 及 `Content-Type: application/json`。更多参数细节参见 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)。

## 使用方式

1. **创建 Agent**：调用 `POST /v1/agents`，传入 `name`、`description`、`model_id`、`tools` 列表及 `memory_store_id`（可选）；
2. **启动会话**：调用 `POST /v1/agents/{agent_id}/sessions`，获取 `session_id`；
3. **发送消息**：调用 `POST /v1/agents/{agent_id}/sessions/{session_id}/messages`，传入 `input`；
4. **（可选）监听事件**：配置 Webhook 订阅 `agent.session.completed` 等事件，实现异步通知；
5. **（可选）部署上线**：调用 `POST /v1/deployments` 绑定 Agent 与 Environment，生成可调用 endpoint。

完整流程示例见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)。

## 限制和注意事项

- 单次 `input.text` 长度上限为 32768 字符；单次 `input.files` 最多 10 个；
- Memory Store 单条记录最大 1MB，总容量受项目配额限制（默认 1GB）；
- Session 默认 TTL 为 7 天，超时后自动清理关联 Memory、Events 与临时 Files；
- Agent 创建后不可修改 `model_id`，如需更换模型，须新建 Agent 并迁移 Skill/Vault 配置；
- 所有文件上传均通过 `/v1/files` 接口先行处理，直接在 `input.files` 中引用未上传的 file ID 将导致 `404 Not Found`。

## 来源文档

- [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)


