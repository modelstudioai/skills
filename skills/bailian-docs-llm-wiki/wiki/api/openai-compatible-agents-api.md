# openai compatible agents api

百炼平台提供的 OpenAI 兼容 Agents API 是一套遵循 OpenAI API 接口规范的智能体服务接口，支持创建、管理与调用具备[长期记忆](../concepts/long-term-memory.md)、工具调用和多轮对话能力的 AI Agent。该 API 与 OpenAI 的 `/v1/agents` 等路径保持语义兼容，便于现有 OpenAI 生态工具链快速迁移。详细设计目标与能力边界请参见 [Agents API](../../raw/application-api-reference/openai-compatible-agents-api.md)。

## 支持的模型与功能

- **模型支持**：当前仅支持 `qwen-plus` 和 `qwen-max` 两类百炼原生大模型作为 Agent 底层推理引擎；不支持第三方模型或自定义模型权重。
- **核心功能**：
  - 创建并持久化 Agent（含 system prompt、tools 列表、memory 配置）
  - 启动 Session 并执行多轮交互（支持流式响应）
  - 通过 Environment 隔离运行时上下文（如沙箱、数据库连接）
  - 使用 Vault 安全存储敏感凭证与结构化知识片段  
  更完整的资源能力矩阵见 [Agents API](../../raw/application-api-reference/openai-compatible-agents-api.md) 中的子文档索引。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 固定为 `qwen-plus` 或 `qwen-max`；传入其他值将返回 400 错误 |
| `tools` | array | 否 | 工具定义列表，格式严格遵循 OpenAI Tool Calling Schema；工具需提前在 Vault 中注册并授权 |
| `tool_choice` | string / object | 否 | 默认 `"auto"`；设为 `"none"` 可禁用工具调用 |
| `max_turns` | integer | 否 | 单次 Session 最大对话轮数，默认 50，上限 200 |
| `session_id` | string | 否 | 复用已有 Session；若未提供则新建；Session 生命周期默认 24 小时 |

> **注意**：`temperature`、`top_p` 等采样参数**暂不生效**，Agent 内部采用固定解码策略以保障确定性行为——此限制与 [Agents API](../../raw/application-api-reference/openai-compatible-agents-api.md) 中“快速开始”示例一致，但与部分旧版 SDK 文档描述存在偏差，请以本页为准。

## 使用方式

1. **认证**：使用 `Authorization: Bearer <api_key>`，API Key 需具备 `agents:read` 和 `agents:write` 权限；
2. **创建 Agent**：`POST /v1/agents`，请求体包含 `model`、`name`、`instructions` 等字段；
3. **启动 Session**：`POST /v1/agents/{agent_id}/sessions`，可指定 `environment_id` 和初始 `messages`；
4. **发送消息**：`POST /v1/sessions/{session_id}/messages`，支持 `stream=true` 流式响应；
5. 所有路径均支持标准 OpenAI 兼容的 HTTP header（如 `X-Stainless-Async: true`）和错误格式。

完整端点说明与请求/响应示例详见 [Agents API](../../raw/application-api-reference/openai-compatible-agents-api.md) 下各子文档，尤其是 `openai-compatible-agents-api-agent.md` 和 `openai-compatible-agents-api-session.md`。

## 限制和注意事项

- 单个 Agent 最多绑定 10 个 tools；单个 Session 最多调用 5 次 tools（防止无限循环）；
- Vault 中存储的凭证仅在 Session 运行时注入 Environment，不会透出至 LLM 上下文；
- 不支持 `parallel_tool_calls`；所有 tool 调用严格串行执行；
- Agent 创建后不可修改 `model` 字段，如需切换模型，须删除重建；
- 错误响应遵循 OpenAI 标准格式（含 `error.type`、`error.message`），具体码表见 [Agents API](../../raw/application-api-reference/openai-compatible-agents-api.md) 中的 errors 子文档。

## 来源文档

- [Agents API](../../raw/application-api-reference/openai-compatible-agents-api.md)


