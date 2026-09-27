# managed agents

managed agents 是百炼平台提供的托管式智能体运行服务，开发者无需自行部署和运维 Agent 运行时环境，只需定义任务逻辑与交互协议，平台自动完成调度、扩缩容、上下文隔离与生命周期管理。该能力适用于需长期运行、多会话并发、强状态一致性要求的生产级 Agent 场景。详细背景可参见 [Managed Agents](../../raw/application-user-guide/managed-agents.md)。

## 支持的模型与功能

- **模型支持**：当前仅支持 Qwen 系列大模型（`qwen-max`、`qwen-plus`、`qwen-turbo`），不支持第三方模型或自定义模型权重；模型版本由平台统一维护，用户不可指定 patch 版本号。
- **核心功能**：
  - 多轮会话上下文自动持久化与隔离（基于 session_id）
  - 内置工具调用框架（支持 HTTP 工具、知识库检索、[函数调用](../concepts/function-calling.md)等）
  - 异步任务委派与结果回调（通过 `delegate_task` 接口）
  - 运行时环境变量注入与 Secrets 安全挂载（详见 [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)）

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `agent_id` | string | 是 | 平台分配的唯一 Agent 标识，创建后不可修改 |
| `session_id` | string | 是 | 每次会话的唯一 ID，用于上下文隔离；建议由客户端生成 UUIDv4 |
| `input` | object | 是 | 用户输入消息对象，格式为 `{ "content": "..." }`，暂不支持多模态输入 |
| `timeout_ms` | integer | 否 | 单次请求最大执行时长，默认 30000（30 秒），上限 120000（2 分钟） |
| `max_steps` | integer | 否 | Agent 自主推理的最大步骤数，默认 15，硬上限 50 |

> **注意**：`max_steps` 在 [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md) 文档中标注为“默认 20”，但实测及最新 API 响应头中确认默认值为 15，以实际接口行为为准。

## 使用方式

1. **创建 Agent**：通过控制台或 CLI 提交 YAML 配置（含 [prompt](prompt.md)、tools、runtime 等），平台返回 `agent_id`  
2. **发起会话**：调用 `/v1/agents/{agent_id}/sessions` POST 接口，传入 `session_id` 和 `input`  
3. **流式响应**：响应体为 Server-Sent Events（SSE），包含 `thought`、`tool_use`、`output` 等事件类型  
4. **委派任务**：在 Agent 执行中调用 `delegate_task(tool_name, parameters)`，结果将自动注入后续上下文（参考 [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)）

## 限制和注意事项

- 单个 Agent 实例最大并发会话数为 100，超出请求将被限流（HTTP 429）  
- 上下文窗口总长度（含历史消息+当前输入）不得超过 32768 token，超长部分将被截断且**不触发警告**  
- Agent 不支持热重载配置；更新 [prompt](prompt.md) 或 tools 需重建 agent_id（旧 ID 会话仍可继续，但新会话生效新配置）  
- 计费按实际 token 数与执行时长计费，空闲会话（无新消息超过 10 分钟）自动终止并释放资源（见 [计费](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)）

## 来源文档

- [Managed Agents](../../raw/application-user-guide/managed-agents.md)


