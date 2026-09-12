# managed agents

managed agents 是百炼平台提供的托管式智能体运行与编排服务，开发者无需自行部署和运维 Agent 服务，即可通过声明式配置快速创建、调用和管理具备多步推理、工具调用、状态保持能力的 AI Agent。其核心设计面向生产级集成，支持事件驱动、会话上下文隔离及 Webhook 回调等关键能力。详细背景和设计目标参见 [Managed Agents](../../raw/application-user-guide/managed-agents.md)。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台已上线的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列大模型（不支持自定义模型或第三方模型接入）；模型选择直接影响 Agent 的推理深度与工具调用稳定性。
- **核心功能**：
  - 多轮会话上下文自动管理（基于 session_id 隔离）
  - 内置工具调用（如 HTTP 请求、数据库查询插件需在 [配置 Agent 环境](../../raw/application-user-guide/managed-agents.md) 中显式声明）
  - 异步任务委派与结果轮询（见 [委派任务给 Agent](../../raw/application-user-guide/managed-agents.md)）
  - Webhook 事件订阅（支持 `agent_started`、`tool_called`、`session_completed` 等事件类型）

> **注意**：原始文档中“构建 Agent”章节提及支持 YAML 定义 workflow，但该能力已在 v2.3.0 后移除，现仅支持 JSON Schema 格式的 `agent_definition` 参数；请以 [构建 Agent](../../raw/application-user-guide/managed-agents.md) 的最新版本说明为准。

## 关键参数

调用 managed agents 时需提供以下必需参数（均通过 API 或 CLI 传入）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `agent_id` | string | 是 | 在控制台创建 Agent 后分配的唯一标识符 |
| `session_id` | string | 否（推荐必设） | 用于隔离会话上下文；若未提供，系统将生成临时 session，不保留历史状态 |
| `input` | object | 是 | 用户输入内容，结构由 Agent 定义中的 `input_schema` 约束 |
| `timeout` | integer | 否 | 最大执行时长（秒），范围 30–600，默认 300 |

其他可选参数（如 `enable_tracing`、`webhook_url`）详见 [配置 Agent 环境](../../raw/application-user-guide/managed-agents.md)。

## 使用方式

1. **创建 Agent**：在控制台「Agent 管理」页点击「新建」，填写名称、描述，并上传符合规范的 agent_definition.json（参考 [构建 Agent](../../raw/application-user-guide/managed-agents.md)）；
2. **调用 Agent**：
   - **API 方式**：向 `POST /v1/agents/{agent_id}/sessions` 发送请求，携带 `session_id` 和 `input`；
   - **CLI 方式**：使用 `bailian agent run --agent-id <id> --session-id <sid> --input '{"query":"..."}'`（详见 [使用 CLI](../../raw/application-user-guide/managed-agents.md)）；
3. **获取结果**：同步返回 `status: "completed"` 或 `"failed"`；异步场景下需轮询 `GET /v1/agents/{agent_id}/sessions/{session_id}` 或监听 Webhook。

## 限制和注意事项

- 单次会话最大 token 数为 32768（含 input + model context + tool responses），超限将触发截断并报错 `context_length_exceeded`；
- 每个 `agent_id` 默认并发上限为 50 路会话，如需提升，请提交工单申请；
- Agent 定义中声明的工具必须已在当前工作空间完成授权与配置，否则调用时返回 `tool_not_authorized` 错误；
- 所有日志与 trace 数据默认保留 7 天，如需长期审计，须主动通过 Webhook 接收并落库 —— 此行为在 [Agent 上下文管理](../../raw/application-user-guide/managed-agents.md) 中有明确说明。

## 来源文档

- [Managed Agents](../../raw/application-user-guide/managed-agents.md)


