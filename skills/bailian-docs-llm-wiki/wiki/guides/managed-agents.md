# managed agents

managed agents 是百炼平台提供的托管式智能体运行服务，开发者无需自行部署和运维 Agent 运行时环境，只需定义任务逻辑与交互协议，平台自动完成调度、扩缩容、状态持久化与上下文管理。该能力适用于需长期运行、多轮交互、跨会话状态保持的自动化工作流场景。详细背景可参见 [Managed Agents](../../raw/application-user-guide/managed-agents.md)。

## 支持的模型与功能

- **模型支持**：当前仅支持 Qwen 系列大模型（如 `qwen-max`、`qwen-plus`），不支持第三方模型或自定义模型权重；模型版本由平台统一维护，不可降级。
- **核心功能**：
  - 多轮会话上下文自动管理（基于 session ID 的隔离存储）
  - 内置工具调用框架（支持 HTTP 工具、数据库连接器、百炼内置插件）
  - 异步任务委派与结果回调（通过 `delegate_task` 接口触发子 Agent）
  - 环境变量与 secrets 安全注入（通过 `environment` 字段配置）

> **注意**：文档 [Managed Agents](../../raw/application-user-guide/managed-agents.md) 中列出的“支持 Llama 系列模型”为历史遗留描述，已于 v2.3.0 版本移除，实际不支持，请以控制台模型下拉列表为准。

## 关键参数

创建或更新 managed agent 时需在请求体中指定以下必选/常用字段：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | Agent 唯一标识符（仅限小写字母、数字、短横线，长度 3–32） |
| `model` | string | 是 | 模型 ID，如 `"qwen-max"`；必须来自 [支持的模型列表](../../raw/application-user-guide/managed-agents/managed-agents-agent.md) |
| `prompt` | string | 否 | 系统提示词（若未提供，则使用平台默认 prompt） |
| `tools` | array | 否 | 工具定义数组，每个元素含 `type`（如 `"http"`）、`name`、`description` 和 `spec` |
| `session_ttl_seconds` | integer | 否 | 会话空闲超时时间，默认 3600（1 小时），范围 300–86400 |

## 使用方式

1. **创建 Agent**：通过 API（`POST /v1/agents`）或 CLI（`bailian agent create --config agent.yaml`）提交配置；
2. **启动会话**：调用 `POST /v1/agents/{agent_id}/sessions` 获取 `session_id`；
3. **交互调用**：向 `POST /v1/agents/{agent_id}/sessions/{session_id}/chat` 发送用户消息，平台自动维护上下文与工具执行；
4. **委派子任务**：在 prompt 或 tool response 中返回 `{"delegate": {"agent_id": "...", "input": {...}}}` 触发嵌套 Agent 调用。

完整流程示例见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)。

## 限制和注意事项

- 单次请求最大 token 数：输入 + 输出总和 ≤ 32768（受底层模型限制）；
- 单个 Agent 最大会话数：10,000（超出后需归档旧会话）；
- 不支持动态加载外部 Python 模块或自定义 runtime；
- 所有工具调用均经平台沙箱拦截，禁止访问本地文件系统、`os.system`、`subprocess` 等高危操作；
- Agent 配置更新后，**已有会话不自动继承新配置**，需显式调用 `/reinit` 或新建会话。

> **注意**：[配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md) 文档中提及的 `LD_PRELOAD` 环境变量注入方式已废弃，v2.4.0 起不再生效，应改用 `secrets` 字段安全传入凭证。

## 来源文档

- [Managed Agents](../../raw/application-user-guide/managed-agents.md)


