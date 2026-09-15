# managed agents

managed agents 是百炼平台提供的托管式智能体运行服务，开发者无需自行部署和运维 Agent 运行时环境，只需定义任务逻辑与交互协议，平台即自动完成调度、扩缩容、状态管理与可观测性集成。该能力适用于需长期运行、多轮对话、跨会话状态保持或事件驱动响应的 Agent 场景。详细背景可参考 [Managed Agents](../../raw/application-user-guide/managed-agents.md)。

## 支持的模型与功能

- **模型支持**：当前仅支持 Qwen 系列大模型（如 `qwen-max`、`qwen-plus`），不支持自定义模型或第三方模型接入；模型版本由平台统一维护，用户不可指定 patch 版本。
- **核心功能**：
  - 多轮会话上下文自动持久化（基于 session_id）
  - 内置工具调用框架（支持 HTTP 工具、函数工具、知识库检索）
  - Webhook 事件订阅（如 `agent_started`、`task_completed`、`error_occurred`）
  - 环境变量隔离与 Secret 注入（通过 `environment` 和 `secrets` 参数配置）

> **注意**：原始文档中 [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md) 提到支持“任意 Python 函数作为 tool”，但实际 API 校验仅接受符合 OpenAPI Schema 描述的 HTTP 工具或平台预注册函数工具；该描述已过时，请以 [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md) 中的工具注册流程为准。

## 关键参数

创建 managed agent 时需在 `POST /v1/agents` 请求体中指定以下必需参数：

| 参数 | 类型 | 说明 |
|------|------|------|
| `name` | string | Agent 唯一标识符（仅限小写字母、数字、连字符） |
| `model` | string | 必须为平台支持的模型 ID，如 `"qwen-max"` |
| `prompt` | string | 系统提示词（支持 Jinja2 变量，如 `{{ user_input }}`） |
| `tools` | array | 工具列表，每个元素含 `type`（`http`/`function`）、`name`、`description` 及对应 schema |
| `environment` | object | 键值对形式的环境变量（非敏感信息） |

`timeout_seconds`（默认 300）、`max_iterations`（默认 15）等运行时参数亦需显式声明，否则使用平台默认值。完整参数定义见 [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)。

## 使用方式

1. **创建 Agent**：调用 `POST /v1/agents`，传入上述参数，返回 `agent_id`；
2. **启动会话**：调用 `POST /v1/agents/{agent_id}/sessions`，传入 `user_input` 和可选 `session_id`；
3. **流式获取响应**：响应头含 `Content-Type: text/event-stream`，按 SSE 协议解析 `data:` 事件；
4. **事件监听（可选）**：在创建时配置 `webhook_url`，平台将推送生命周期事件（详见 [Webhook 事件订阅](../../raw/application-user-guide/managed-agents/managed-agents-webhook.md)）。

CLI 方式可通过 `bailian-cli agent create --config agent.yaml` 快速部署，配置文件结构与 API 一致，详见 [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)。

## 限制和注意事项

- 单个 Agent 实例最大并发会话数为 100；超出时新请求将被拒绝（HTTP 429）；
- `prompt` 长度上限为 8192 字符；工具描述总长度（含所有 `description` 字段）不得超过 4096 字符；
- Agent 生命周期内不可修改 `model` 或 `tools` 列表，如需变更，必须删除后重建；
- 所有会话状态默认保留 7 天，超期后自动清理；如需延长，请在创建时设置 `retention_days`（最大 30）；
- 计费按实际执行时长（秒级）与 token 消耗双重计量，空闲等待时间不计费——具体规则参见 [计费](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)。

## 来源文档

- [Managed Agents](../../raw/application-user-guide/managed-agents.md)


