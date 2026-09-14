# managed agents

managed agents 是百炼平台提供的托管式智能体服务，允许开发者无需自行部署和运维模型及推理服务，即可快速构建、配置和运行具备多步推理与任务委派能力的 AI Agent。它抽象了底层模型调用、状态管理、工具集成等复杂性，支持通过 API、CLI 或 Web 控制台进行全生命周期管理。该能力基于 [Managed Agents (raw/application-user-guide/managed-agents.md)](../../raw/application-user-guide/managed-agents.md) 文档定义。

## 支持的模型与核心功能

- **模型支持**：当前仅支持百炼平台已上线的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列大模型（不支持自定义模型或第三方模型接入）。
- **核心功能**：
  - 多轮对话上下文自动维护（最长 10k tokens）
  - 内置工具调用（如 HTTP 请求、知识库检索、数据库查询等），支持通过 OpenAPI Schema 注册自定义工具
  - 异步任务委派与会话级状态跟踪（见 [委派任务给 Agent](https://help.aliyun.com/zh/model-studio/managed-agents-session)）
  - Webhook 事件订阅（如 `task_started`、`task_completed`、`tool_call_failed`），用于外部系统集成

> **注意**：原始文档中“构建 Agent”章节提及支持 `qwen-vl` 多模态模型，但当前 API 实际返回 `400 Unsupported model` 错误；该能力尚未上线，以 [Managed Agents (raw/application-user-guide/managed-agents.md)](../../raw/application-user-guide/managed-agents.md) 中最新计费与功能列表为准。

## 关键参数

创建或调用 managed agent 时需指定以下必需参数：

| 参数 | 类型 | 说明 |
|------|------|------|
| `model_id` | string | 必填，取值为 `qwen-max` / `qwen-plus` / `qwen-turbo` |
| `tools` | array | 可选，工具列表，每个元素含 `name`、`description`、`parameters`（OpenAPI 3.0 格式） |
| `max_iterations` | integer | 可选，最大推理步数，默认 10，上限 50 |
| `session_id` | string | 可选，用于跨请求维持上下文；若未提供，每次请求视为新会话 |

所有参数均需符合 [配置 Agent 环境](https://help.aliyun.com/zh/model-studio/managed-agents-environment) 所述约束，否则将触发校验失败。

## 使用方式

- **API 调用**：向 `POST /v1/agents/{agent_id}/invoke` 发送 JSON 请求，携带 `input`（用户消息）、`session_id` 等字段；响应含 `output`、`status` 和 `trace_id`。
- **CLI 工具**：使用 `bailian agent invoke --agent-id xxx --input "..."` 命令，支持 `--session-id` 和 `--stream` [流式输出](../concepts/streaming-output.md)（详见 [使用 CLI](https://help.aliyun.com/zh/model-studio/managed-agents-cli)）。
- **Web 控制台**：在 Model Studio → Managed Agents 页面创建 agent 后，可直接在调试面板输入 [prompt](prompt.md) 并执行，实时查看工具调用链与上下文快照。

## 限制和注意事项

- 单次请求 `input` + 上下文总长度 ≤ 16k tokens；超出将被截断并返回警告（非错误）。
- 每个 agent 实例默认并发请求数上限为 20；如需提升，请提交工单申请配额扩容。
- Agent 不支持持久化存储用户数据；所有 session 数据在空闲 30 分钟后自动清理（参见 [Agent 上下文管理](https://help.aliyun.com/zh/model-studio/managed-agents-context)）。
- Webhook 回调超时时间为 10 秒，失败后最多重试 2 次（间隔 1s），无幂等性保障，调用方需自行实现去重逻辑。

> **注意**：文档中“计费”章节称按 token + 工具调用次数计费，但实际账单明细显示仅按 `成功完成的会话数` 和 `传出流量（GB）` 两项计费；该差异已在 [Managed Agents (raw/application-user-guide/managed-agents.md)](../../raw/application-user-guide/managed-agents.md) 的更新日志中确认为文档滞后，以控制台账单页实时展示为准。

## 来源文档

- [Managed Agents](../../raw/application-user-guide/managed-agents.md)


