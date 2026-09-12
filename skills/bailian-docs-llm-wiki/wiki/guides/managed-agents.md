# managed agents

managed agents 是百炼平台提供的托管式智能体运行服务，开发者无需自行部署和运维 Agent 服务，即可通过 API 或 CLI 快速创建、配置并调用具备多步推理与工具调用能力的 Agent。其核心能力基于大模型驱动的任务分解与外部系统集成，适用于客服对话、自动化工作流、数据查询等场景。详细背景可参考 [Managed Agents](../../raw/application-user-guide/managed-agents.md)。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台已接入的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列模型（不支持自定义模型或第三方模型接入）。
- **核心功能**：
  - 多轮任务分解与自主规划（Plan-and-Execute）
  - 内置工具调用（如 HTTP 请求、数据库查询、知识库检索）
  - 支持用户自定义工具（需符合 OpenAPI 3.0 规范并完成鉴权配置）
  - Agent 级别上下文隔离与生命周期管理
  - Webhook 事件订阅（如 `task_started`、`tool_called`、`session_completed`）

> **注意**：原始文档中“构建 Agent”章节提及支持 `qwen2-72b`，但该模型尚未在生产环境开放 Agent 模式调用，实际使用时将返回 `400 UnsupportedModel` 错误；请以控制台模型列表或 [Managed Agents](../../raw/application-user-guide/managed-agents.md) 中“快速开始”章节的可用模型为准。

## 关键参数

创建或调用 Agent 时需指定以下关键参数：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 模型 ID，如 `"qwen-plus"`；必须为平台当前支持的 Agent 模型 |
| `tools` | array | 否 | 工具列表，每个元素含 `name`、`description`、`parameters`（JSON Schema）及 `type: "function"` |
| `max_iterations` | integer | 否 | 默认 15，最大 50；单次会话中 Agent 自主调用工具+生成响应的总步数上限 |
| `enable_webhook` | boolean | 否 | 默认 `false`；设为 `true` 时需同步提供 `webhook_url` |
| `session_id` | string | 否 | 用于上下文延续；若未提供则新建会话（详见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents.md)）|

## 使用方式

1. **通过 API 创建 Agent**：  
   向 `POST /v1/agents` 提交 JSON 配置（含 `model_id`、`tools` 等），获取 `agent_id`；后续调用均基于该 ID。

2. **启动会话并执行任务**：  
   调用 `POST /v1/agents/{agent_id}/sessions`，传入 `input` 字符串（如 `"查一下杭州今天天气"`）及可选 `session_id`。

3. **通过 CLI 快速验证**（推荐开发调试）：  
   ```bash
   baiLian agent create --model qwen-plus --tools tools.json
   baiLian agent run --agent-id agt-xxx --input "列出我上月订单"
   ```
   具体命令与选项见 [Managed Agents](../../raw/application-user-guide/managed-agents.md) 的“使用 CLI”章节。

## 限制和注意事项

- **并发与配额**：免费试用期默认限 5 个并发会话；企业版按 license 绑定并发数（最高 100），超出请求将被限流（HTTP 429）。
- **上下文长度**：单次会话输入 + 历史消息 + 工具返回内容总 token 数不得超过模型 context window 的 80%（例如 `qwen-plus` 为 8192，则上限约 6550 tokens）。
- **工具返回限制**：单次工具调用响应体大小不可超过 2MB；超长响应将被截断并记录警告日志。
- **会话有效期**：空闲会话（无新消息）30 分钟后自动清理，`session_id` 失效；如需长期状态，请自行持久化关键上下文。
- **调试建议**：首次集成时务必启用 `enable_webhook` 并监听事件流，便于定位工具调用失败或规划异常问题——详情参见 [Managed Agents](../../raw/application-user-guide/managed-agents.md) 的“Webhook 事件订阅”部分。

## 来源文档

- [Managed Agents](../../raw/application-user-guide/managed-agents.md)


