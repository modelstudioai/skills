# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和管理具备[长期记忆](../concepts/long-term-memory.md)、工具调用与多步推理能力的 AI Agent。该 API 以 RESTful 形式提供，支持细粒度的环境隔离、会话生命周期控制及安全凭证管理。开发者可通过组合 Agent、Environment、Session、Skill 等核心资源构建生产级自动化工作流。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列模型（详见 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 文档中 `model_id` 字段说明）。
- **核心功能**：
  - 基于 Environment 的沙箱化执行环境（含网络策略、超时与资源配额控制）
  - Session 级持久化上下文与事件流（支持 `event_type: "tool_call"` / `"tool_result"` 回调）
  - 内置 Skill 注册与调用（如 `web_search`、`code_interpreter`、`file_read`），技能行为由 Vault 中的 Credential 驱动
  - 文件上传与引用（通过 `/files` 接口上传后，可在 Session 中以 `file://<file_id>` 方式传入）

> **注意**：原始文档中 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md) 提到支持自定义 Docker 镜像，但该能力已在 v2.3.0 后下线；实际仅支持平台预置的 runtime（Python 3.11 + 工具 SDK），请以 [Deployment](../../raw/application-api-reference/managed-agents-api/deployment-api.md) 中的 `runtime_type` 字段为准。

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `agent_id` | Path | 是 | 通过 POST `/agents` 创建后返回的唯一标识 |
| `environment_id` | Body (Agent creation) | 否 | 若不指定，将自动绑定默认环境；建议显式传入以保障一致性（见 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)） |
| `session_id` | Header (`X-Session-ID`) 或 Body | 否（首次请求可省略） | 用于关联会话状态；若缺失，API 将自动生成新 session 并返回 `X-Session-ID` 响应头 |
| `tools` | Body (Session create) | 否 | 显式声明本次会话可用的 Skill 列表，格式为 `["web_search", "file_read"]`；未声明则仅启用 Agent 默认启用的工具 |

## 使用方式

1. **创建 Agent**：`POST /agents`，指定 `model_id`、`name` 及可选 `environment_id`
2. **启动会话**：`POST /agents/{agent_id}/sessions`，携带用户输入 `input` 和可选 `tools`
3. **流式响应处理**：响应为 Server-Sent Events（SSE），需监听 `event: message`、`event: tool_call` 等类型，并按需调用对应 Skill 接口（如 `/skills/web_search`）
4. **文件上传与引用**：先 `POST /files` 上传二进制文件，获取 `file_id` 后，在 `input` 中以 `file://<file_id>` 形式引用（参见 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)）

## 限制和注意事项

- 单次 Session 最大 token 数为 32768（含 [prompt](../guides/prompt.md) + completion），超出将触发 `400 Bad Request`
- 每个 Agent 最多关联 100 个活跃 Session；超过后需显式 `DELETE /sessions/{id}` 清理
- Skill 调用结果必须在 60 秒内通过 `POST /sessions/{session_id}/tool_results` 回传，超时将导致会话中断
- 所有 Credential（如 API Key）必须预先存入 Vault 并授权给对应 Environment，否则 Skill 调用将返回 `403 Forbidden`（详见 [Credential](../../raw/application-api-reference/managed-agents-api/credential-api.md)）

## 来源文档

- [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)


