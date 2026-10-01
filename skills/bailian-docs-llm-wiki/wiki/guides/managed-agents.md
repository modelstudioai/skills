# managed agents

managed agents 是百炼平台提供的托管式智能体运行时服务，允许开发者无需自行维护基础设施即可部署、调用和管理基于大模型的自主智能体。它抽象了底层推理调度、状态持久化与会话生命周期管理，支持通过 API 或 CLI 快速集成。该能力适用于需要长期运行、多轮交互或任务委派的复杂场景，如自动化客服、数据分析师代理等。

## 支持的模型与功能

- 支持 Qwen 系列（Qwen2.5-72B、Qwen2.5-32B）、Baichuan2、GLM4 等平台已上线的推理模型，具体以 [Managed Agents (raw/application-user-guide/managed-agents.md)](../../raw/application-user-guide/managed-agents.md) 中“构建 Agent”章节列出的模型列表为准。
- 核心功能包括：自动会话状态管理、工具调用（function calling）编排、多 step 任务委派、上下文窗口动态扩展（最大 128K tokens），以及内置的异步任务队列。
- > **注意**：文档 [managed-agents-agent.md](../../raw/application-user-guide/managed-agents/managed-agents-agent.md) 中提及的“自定义 LLM adapter 插件机制”目前仅限白名单客户使用，公测版暂未开放，实际配置时请以 [managed-agents-environment.md](../../raw/application-user-guide/managed-agents/managed-agents-environment.md) 的环境变量约束为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型 ID，必须为平台支持的托管模型，例如 `"qwen2.5-32b"`；不支持自定义模型路径。 |
| `tools` | array | 否 | 工具定义列表，每个工具需包含 `name`、`description` 和 OpenAPI 格式的 `parameters`；详见 [managed-agents-agent.md](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)。 |
| `max_steps` | integer | 否 | 单次会话最大执行步数，默认 10，上限 50。超过将终止并返回 `stopped_by_max_steps`。 |
| `timeout_ms` | integer | 否 | 单步执行超时毫秒数，默认 30000（30 秒），最小 5000。 |

## 使用方式

1. **创建 Agent**：通过 `POST /v1/agents` 提交配置（含 model、tools 等），获取唯一 `agent_id`；
2. **启动会话**：调用 `POST /v1/agents/{agent_id}/sessions` 初始化会话，可传入初始 `input` 和 `context`；
3. **交互与委派**：向 `POST /v1/agents/{agent_id}/sessions/{session_id}/messages` 发送用户消息，Agent 自动处理 tool call 并返回结果或中间状态；
4. CLI 方式支持快速调试：`bailian agent run --agent-id xxx --input "分析销售数据"`，完整命令参考 [managed-agents-cli.md](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)。

## 限制和注意事项

- 单个 Agent 实例最多并发 20 个活跃会话；超出请求将被限流（HTTP 429）；
- 上下文管理依赖显式传入 `context_id` 或复用 session ID；跨 session 的上下文不自动继承，需手动注入，详见 [managed-agents-context.md](../../raw/application-user-guide/managed-agents/managed-agents-context.md)；
- 不支持在运行时热更新 tools 列表或 model 配置，变更需重建 Agent；
- 计费按实际 token 消耗 + 执行步数计费，空闲会话（>15 分钟无新消息）自动释放资源，详情见 [managed-agents-billing.md](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)。

## 来源文档

- [Managed Agents](../../raw/application-user-guide/managed-agents.md)


