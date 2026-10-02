# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和运行具备[长期记忆](../concepts/long-term-memory.md)、工具调用、多步推理能力的自主 Agent。该 API 封装了环境管理、会话生命周期、文件与凭证安全存储、技能编排等底层能力，开发者无需自行维护基础设施即可构建生产级 Agent 应用。详细设计与行为规范请参考 [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列大模型；其他模型（如 `qwen2.5`）暂未开放 Agent 模式调用，具体以 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 文档为准。
- **核心功能**：
  - 基于 `Environment` 的隔离[沙箱](../concepts/sandbox.md)执行上下文；
  - `Session` 管理带状态的多轮交互与事件流（含 `on_tool_call`、`on_memory_update` 等钩子）；
  - `Memory Store` 提供向量+结构化混合记忆检索；
  - `Skill` 机制支持声明式工具注册与自动路由；
  - `Vault` + `Credential` 实现敏感凭据的加密托管与按需注入。

> **注意**：原始文档中 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md) 描述其支持自定义 Docker 镜像，但该能力已于 v2.3 版本下线；实际仅支持平台预置的 Python 3.11 运行时环境，请以 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md) 中的 runtime 兼容性说明为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `agent_id` | string | 是 | 通过 `/v1/agents` 创建后返回的唯一标识符 |
| `session_id` | string | 否 | 复用已有会话时传入；不传则新建会话（自动持久化） |
| `input` | object | 是 | 用户输入，格式为 `{ "text": "..." }` 或 `{ "files": ["file_id_1", "..."] }` |
| `stream` | boolean | 否 | `true` 时返回 Server-Sent Events 流；默认 `false`（JSON 响应） |
| `max_steps` | integer | 否 | 单次请求最大执行步数，范围 1–50，默认 20 |

## 使用方式

1. **创建 Agent**：调用 `POST /v1/agents`，传入 `name`、`description`、启用的 `skills` 列表及 `memory_store_id`（可选）；
2. **发起调用**：`POST /v1/agents/{agent_id}/chat`，携带 `input` 与可选 `session_id`；
3. **管理资源**：通过 `/v1/environments`、`/v1/skills`、`/v1/vaults` 等子路径独立配置依赖组件；
4. **调试与监控**：所有会话事件可通过 `/v1/sessions/{session_id}/events` 查询，详见 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)。

## 限制和注意事项

- 单次 `chat` 请求最大 `input.text` 长度为 32768 字符；文件总大小不超过 100 MB；
- `Memory Store` 默认保留最近 100 条记忆条目，超出部分按 LRU 自动淘汰；
- Agent 不支持跨 `Environment` 共享 `Vault` 凭据——每个 Environment 必须显式绑定 Vault，此约束在 [Vault](../../raw/application-api-reference/managed-agents-api/vault-api.md) 中有明确说明；
- 所有 API 均需使用 `Authorization: Bearer <api_key>` 认证，且 `api_key` 必须具备 `managed_agents:write` 权限。

## 来源文档

- [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)


