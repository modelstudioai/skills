# managed agents

managed agents 是百炼平台提供的托管式智能体运行服务，开发者无需自行部署和运维 Agent 服务，即可通过 API 或 CLI 快速创建、配置并调用具备多步推理与工具调用能力的 Agent。其核心能力基于大模型驱动的任务分解与外部系统集成，适用于客服对话、自动化工作流、数据查询等场景。详细背景可参考 [Managed Agents](../../raw/application-user-guide/managed-agents.md)。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台已接入的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列模型（不支持自定义模型或第三方模型接入）。
- **核心功能**：
  - 多轮任务分解与自主规划（Plan-and-Execute）
  - 内置工具调用（如 HTTP 请求、数据库查询、知识库检索）
  - 支持用户自定义工具（需符合 OpenAPI 3.0 规范并完成鉴权配置）
  - 异步会话管理与长上下文保持（最大 context window 为 32k tokens）
  - Webhook 事件回调（支持 `agent_started`、`tool_called`、`agent_finished` 等生命周期事件）

> **注意**：文档 [Managed Agents](../../raw/application-user-guide/managed-agents.md) 中“构建 Agent”章节提及支持 `qwen-vl` [多模态](../concepts/multi-modal.md)模型，但该能力尚未上线，实际调用将返回 `model_not_supported` 错误；请以控制台模型下拉列表或 `/v1/models` API 返回结果为准。

## 关键参数

创建或调用 Agent 时需关注以下必需或常用参数：

| 参数名 | 类型 | 是否必需 | 说明 |
|--------|------|----------|------|
| `model_id` | string | 是 | 模型 ID，如 `"qwen-plus"`；必须为平台当前启用的模型 |
| `tools` | array | 否 | 工具列表，每个工具需包含 `name`、`description` 和 `spec`（OpenAPI 3.0 JSON Schema） |
| `max_iterations` | integer | 否 | 最大推理步数，默认 15，上限 50 |
| `enable_webhook` | boolean | 否 | 是否启用 Webhook 回调，默认 `false`；启用后需同时提供 `webhook_url` |
| `session_id` | string | 否（会话续写必需） | 用于关联上下文的唯一标识，建议由客户端生成 UUID |

完整参数说明见 [配置 Agent 环境](../../raw/application-user-guide/managed-agents.md)。

## 使用方式

1. **创建 Agent**：通过 `POST /v1/agents` 提交配置（含模型、工具、超参），获取 `agent_id`；
2. **启动会话**：调用 `POST /v1/agents/{agent_id}/sessions`，传入初始 `input` 和可选 `session_id`；
3. **轮询或监听结果**：
   - 同步模式：等待响应体中 `status: "completed"`，返回最终输出；
   - 异步模式：配合 Webhook 订阅事件，或轮询 `GET /v1/sessions/{session_id}`；
4. **CLI 快速验证**（推荐开发调试）：
   ```bash
   aliyun baiLian CreateAgent --ModelId qwen-plus --Tools '[{"name":"search","spec":{...}}]'
   ```

更多操作示例详见 [使用 CLI](../../raw/application-user-guide/managed-agents.md)。

## 限制和注意事项

- **配额限制**：单个账号默认最多创建 100 个 Agent；单次会话最长执行时间 300 秒，超时自动终止；
- **工具调用安全**：所有自定义工具 endpoint 必须使用 HTTPS，且需在控制台完成域名白名单备案；
- **上下文隔离**：不同 `session_id` 之间完全隔离；同一 session 内工具调用返回内容默认进入 LLM 上下文，敏感字段（如 token、密码）需在 `spec` 中显式标记 `"x-sensitive": true` 以触发自动脱敏；
- **计费说明**：按 Agent 实例运行时长（秒） + 工具调用次数 + 模型 [Token](../concepts/token.md) 数三者叠加计费，非活跃会话（无新消息 10 分钟）自动释放资源；详情见 [计费](../../raw/application-user-guide/managed-agents.md)。

## 来源文档

- [Managed Agents](../../raw/application-user-guide/managed-agents.md)



