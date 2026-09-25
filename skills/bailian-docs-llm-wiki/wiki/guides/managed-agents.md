# managed agents

managed agents 是百炼平台提供的托管式智能体运行时服务，开发者无需自行部署和运维 Agent 服务，即可通过声明式配置快速创建、调用和管理具备多步推理与工具调用能力的 AI Agent。其核心设计目标是降低 Agent 工程化门槛，统一生命周期管理，并与百炼模型服务、工具市场及上下文存储深度集成。详细背景可参考 [Managed Agents](../../raw/application-user-guide/managed-agents.md)。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台上的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列大模型（v202408 及以上版本），不支持自定义模型或外部模型接入。  
- **核心功能**：  
  - 多轮对话状态自动维护（基于 session ID）  
  - 内置工具调用（支持 HTTP API、数据库查询、知识库检索等预注册工具）  
  - 上下文自动截断与摘要（最大上下文窗口为 32k tokens，超出部分按 LRU + 语义重要性混合策略压缩）  
  - 异步任务委派与结果回调（需显式启用 `enable_async_delegation: true`）  
  更多能力细节见 [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型 ID，仅限 `qwen-max` / `qwen-plus` / `qwen-turbo` |
| `tools` | array[string] | 否 | 工具 ID 列表，须已在工具市场启用并授权给当前项目 |
| `max_iterations` | integer | 否 | 默认 15，单次会话中 Agent 自主决策的最大步骤数（含工具调用） |
| `timeout_ms` | integer | 否 | 默认 30000（30 秒），超时后返回 `STATUS_TIMEOUT` |
| `enable_context_compression` | boolean | 否 | 默认 `true`；设为 `false` 可禁用自动上下文压缩，但可能触发模型输入超限错误 |

> **注意**：`max_iterations` 在 [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md) 中被误标为“最大 token 数”，该描述已过时，以本表为准。

## 使用方式

1. **创建 Agent**：通过控制台或 CLI 提交 YAML 配置（参考 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)）；  
2. **发起会话**：调用 `/v1/agents/{agent_id}/sessions` 创建 session，获取 `session_id`；  
3. **发送消息**：向 `/v1/sessions/{session_id}/messages` POST 用户输入，Agent 自动执行推理与工具调用；  
4. **获取结果**：响应中 `status` 为 `completed` 时，`output.content` 即最终回复；若含 `pending_tools` 字段，表示异步任务进行中，需轮询或监听 Webhook。

CLI 示例（需安装 `bailian-cli>=0.8.0`）：
```bash
bailian agent run --agent-id agt-xxx --input "查一下杭州今天天气"
```

## 限制和注意事项

- 单个 Agent 实例最大并发请求数为 50；超出将返回 `429 Too Many Requests`；  
- Session 生命周期默认 24 小时，超时后上下文自动清除，不可恢复；  
- 工具调用失败时，Agent 默认重试 2 次（间隔 1s），不支持自定义重试策略；  
- 不支持流式响应（`stream: true` 参数被忽略），所有响应均为完整 JSON 结构；  
- 计费按实际调用次数与消耗 token 综合计算，详见 [计费](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)。

## 来源文档

- [Managed Agents](../../raw/application-user-guide/managed-agents.md)


