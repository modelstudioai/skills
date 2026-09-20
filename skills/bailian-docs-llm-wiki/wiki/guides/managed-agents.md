# managed agents

managed agents 是百炼平台提供的托管式智能体运行服务，开发者无需自行部署和运维 Agent 运行时环境，只需定义任务逻辑与交互协议，平台自动完成调度、扩缩容、状态持久化与上下文管理。该能力适用于需长期运行、多轮交互、跨会话状态保持的自动化工作流场景。详细背景可参见 [Managed Agents](../../raw/application-user-guide/managed-agents.md)。

## 支持的模型与功能

- **模型支持**：当前仅支持 Qwen 系列大模型（Qwen2.5-72B-Instruct、Qwen2.5-32B-Instruct 等），不支持第三方模型或自定义推理后端；模型版本由平台统一维护，用户不可指定 patch 版本号。
- **核心功能**：
  - 自动会话生命周期管理（创建、恢复、超时终止）
  - 内置工具调用框架（支持 HTTP 工具、数据库连接器、百炼内置插件）
  - 多轮对话上下文自动截断与压缩（基于 token 预估，非精确计数）
  - 异步任务委派与结果回调（通过 `session_id` 关联）

> **注意**：[managed-agents-agent.md](../../raw/application-user-guide/managed-agents/managed-agents-agent.md) 中提及的“支持任意 HuggingFace 模型”已过时，该描述未同步更新，实际以控制台模型下拉列表为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `agent_id` | string | 是 | 平台分配的唯一 Agent 标识符，创建后不可修改 |
| `session_id` | string | 否 | 显式指定会话 ID；若为空，平台自动生成；用于跨请求恢复上下文 |
| `max_steps` | integer | 否 | 单次会话最大执行步数，默认 15，上限 50 |
| `timeout_ms` | integer | 否 | 单步执行超时毫秒数，默认 30000（30 秒），最小 5000 |
| `enable_context_compression` | boolean | 否 | 是否启用上下文压缩，默认 `true`；设为 `false` 时可能触发 token 超限错误 |

完整参数说明请参考 [managed-agents-session.md](../../raw/application-user-guide/managed-agents/managed-agents-session.md)。

## 使用方式

1. **创建 Agent**：通过控制台或 OpenAPI 提交 Agent 定义（含 [prompt](prompt.md) 模板、工具列表、默认参数），获取 `agent_id`；
2. **发起会话**：调用 `/v1/agents/{agent_id}/sessions` 接口，传入初始输入（`input` 字段）及可选参数；
3. **持续交互**：使用返回的 `session_id` 调用 `/v1/agents/{agent_id}/sessions/{session_id}/chat` 发起后续消息；
4. **CLI 辅助**（可选）：`bailian-cli agent run --agent-id xxx --input "..."` 可快速验证基础流程，详见 [managed-agents-cli.md](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)。

## 限制和注意事项

- 单个 Agent 实例最大并发会话数为 100；超出时新请求将被拒绝（HTTP 429）；
- 会话空闲超时时间为 10 分钟（自最后一条消息起），超时后上下文自动释放，不可恢复；
- 不支持在运行时动态修改 Agent 的 [prompt](prompt.md) 或工具配置；如需变更，必须新建 Agent 并迁移会话逻辑；
- 计费按实际执行步数（step）计费，每步包含模型推理 + 工具调用 + 上下文管理开销，详情见 [managed-agents-billing.md](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)。

## 来源文档

- [Managed Agents](../../raw/application-user-guide/managed-agents.md)


