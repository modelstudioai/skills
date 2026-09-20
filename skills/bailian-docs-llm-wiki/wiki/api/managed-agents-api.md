# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和运行具备[长期记忆](../concepts/long-term-memory.md)、工具调用、多步推理能力的自主 Agent。该 API 将底层模型调度、状态管理、环境隔离与安全凭证等复杂性封装为声明式资源（如 `Agent`、`Environment`、`Memory Store`），开发者可通过 RESTful 接口组合构建生产级 AI 应用。详细设计原则与架构约束请参见 [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三类大模型，不支持 BYOM（Bring Your Own Model）或外部模型接入；模型选择通过 `agent.model_id` 字段指定。
- **核心功能**：
  - 多轮会话状态自动持久化（基于 `Session` 资源）
  - 工具调用（Skills）的声明式注册与权限控制（见 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)）
  - 安全敏感数据隔离存储（`Vault` + `Credential` 组合机制）
  - 运行时环境沙箱（`Environment` 配置 CPU/GPU/内存规格及网络策略）

> **注意**：文档中提及的 `qwen-vl` 模型支持已在 v2.3.0 版本中移除，实际调用将返回 `400 UnsupportedModel` 错误；请以 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 文档中 `model_id` 枚举值为准。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `agent_id` | Path | string | 是 | Agent 唯一标识符，由平台生成或用户指定（需符合 `[a-z0-9-]{3,63}` 正则） |
| `session_id` | Query 或 Body | string | 否（首次调用可省略） | 显式指定会话 ID，用于跨请求状态复用；若未提供，平台自动生成 |
| `stream` | Query | boolean | 否，默认 `false` | 设为 `true` 时启用 SSE 流式响应（仅 `/v1/agents/{agent_id}/run` 支持） |
| `memory_store_id` | Body（`run` 请求） | string | 否 | 指定本次运行使用的 Memory Store 实例，覆盖 Agent 默认配置 |

## 使用方式

1. **初始化 Agent**：先通过 `POST /v1/agents` 创建 Agent 资源，需指定 `model_id`、`skills` 列表及 `memory_store_id`；
2. **启动会话**：调用 `POST /v1/agents/{agent_id}/run` 提交用户输入，平台自动关联 Session 并返回 `event_stream` 或完整响应；
3. **状态查询**：使用 `GET /v1/sessions/{session_id}` 获取历史消息与执行轨迹（含 tool calls 详情）；
4. **文件与凭证集成**：上传文件至 `File` 资源后，通过 `Vault` 引用其 `file_id`；`Credential` 资源须绑定至 `Environment` 才可在 Skill 中访问。

所有操作均需携带 `Authorization: Bearer <api_key>`，且请求体必须为 `application/json`。完整端点列表与示例见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 限制和注意事项

- 单次 `run` 请求最大输入长度为 32768 token（含 system [prompt](../guides/prompt.md) + history + user input）；
- `Memory Store` 默认保留最近 100 条消息，TTL 可配置但不可超过 30 天；
- Webhook 回调地址必须为 HTTPS，且需在 `Webhook` 资源中显式启用 `verify_ssl: true`（默认开启）；
- Agent 创建后不可修改 `model_id` 或 `environment_id`，如需变更，须重建 Agent 并迁移 `Memory Store` 数据；
- 文件上传大小上限为 512 MB，但 `File` 资源仅支持文本类 MIME 类型（`text/*`, `application/json`, `application/pdf`），不支持视频/音频解析——该限制在 [File](../../raw/application-api-reference/managed-agents-api/files-api.md) 文档中有明确说明。

## 来源文档

- [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)


