# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和运行具备长期[记忆](../concepts/memory.md)、工具调用、多步推理能力的 AI Agent。该 API 封装了环境管理、会话状态、文件处理、技能编排等核心能力，开发者无需自行维护底层基础设施即可构建生产级 Agent 应用。详细设计与行为规范请参阅 [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列模型；不支持第三方模型或自定义模型接入。
- **核心功能**：
  - 基于 `Environment` 的隔离运行时上下文；
  - `Session` 级别的状态持久化与事件流（含 `on_tool_call`、`on_message` 等生命周期钩子）；
  - `Memory Store` 提供结构化长期[记忆](../concepts/memory.md)（支持向量检索与元数据过滤）；
  - `Skill` 机制支持声明式工具注册与自动编排；
  - `Vault` + `Credential` 实现安全凭证管理与动态注入。

> **注意**：[Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 文档中提及的“支持任意 HuggingFace 模型”为历史遗留描述，已过时；实际仅限平台白名单模型，以 [Deployment](../../raw/application-api-reference/managed-agents-api/deployment-api.md) 中的 `model_id` 枚举值为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `agent_id` | string | 是 | 通过 `/v1/agents` 创建后返回的唯一标识符 |
| `session_id` | string | 否 | 若未提供，API 自动创建新会话；复用可延续上下文与 memory |
| `input` | object | 是 | 用户输入，格式为 `{ "text": "..." }` 或 `{ "files": [...] }` |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时返回 Server-Sent Events 流式响应 |
| `tools` | array | 否 | 运行时临时覆盖 Agent 配置的工具列表（仅限已授权 `Skill`） |

所有请求需携带 `Authorization: Bearer <api_key>`，且 `Content-Type: application/json`。更多参数细节见 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)。

## 使用方式

1. **初始化 Agent**：调用 `POST /v1/agents` 创建 Agent 实例，指定 `environment_id`、`skills`、`memory_store_id` 等；
2. **发起调用**：向 `POST /v1/agents/{agent_id}/chat` 提交请求，传入 `input` 与可选 `session_id`；
3. **处理响应**：同步响应含 `output`（文本/结构化结果）、`event_trace`（执行路径）；流式响应按 `data:` 行解析；
4. **管理资源**：通过 `/environments`、`/memory-stores`、`/skills` 等子资源独立配置与复用组件。

完整端到端示例见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)。

## 限制与注意事项

- 单次请求 `input.text` 最长 32768 字符；`files` 总大小不超过 100 MB；
- 每个 `session_id` 最多保留 7 天活跃状态，超期后 `Memory Store` 中关联记录仍保留但不可被新会话自动继承；
- `File` API 上传的临时文件在会话结束后 24 小时自动清理，如需长期存储须显式调用 `POST /v1/files/persist`；
- Agent 执行超时默认为 120 秒，不可修改；若需更长任务周期，应拆分为多个 `session` 并手动传递中间状态。

> **注意**：[File](../../raw/application-api-reference/managed-agents-api/files-api.md) 文档中“临时文件永久保留”为错误描述，正确行为以本节及 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md) 中的生命周期说明为准。

## 来源文档

- [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)


