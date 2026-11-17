# openai compatible agents api

百炼平台提供的 OpenAI 兼容 Agents API 是一套遵循 OpenAI API 接口规范的智能体服务接口，支持通过标准 REST 调用创建、管理与执行具备工具调用、多轮记忆和环境隔离能力的 AI Agent。该 API 与 OpenAI 的 `chat.completions` 接口保持高度兼容，便于现有 OpenAI 生态应用快速迁移。详细设计目标与能力边界请参见 [Agents API](../../raw/application-api-reference/openai-compatible-agents-api.md)。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼专属 Agent 模型（如 `qwen-plus-agents-202409`），不支持通用大语言模型（如 `qwen-max`）直接作为 Agent 后端；模型需显式启用 Agent 模式并配置工具集。
- **核心功能**：
  - 多步骤自主规划与工具调用（支持自定义函数、HTTP 工具、数据库连接器等）
  - Session 级别状态持久化（含消息历史、变量上下文、工具执行结果缓存）
  - Environment 隔离运行沙箱（保障多租户间数据与资源隔离）
  - Vault 安全凭证管理（用于工具调用时的密钥注入，避免硬编码）

> **注意**：原始文档中 [概览](../../raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-overview.md) 提到“支持任意 qwen 系列模型”，但该描述已过时；实际接入必须使用带 `-agents-` 后缀的专用模型，详见 [Agents](../../raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-agent.md) 文档的模型约束说明。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | Agent 专用模型 ID（如 `qwen-plus-agents-202409`），不可为通用模型 |
| `tools` | array | 否 | 工具定义列表，格式与 OpenAI `tools` 完全一致；若为空则禁用工具调用 |
| `tool_choice` | string / object | 否 | 控制工具调用策略（`"auto"`/`"required"`/`{"type": "function", "function": {"name": "xxx"}}`） |
| `session_id` | string | 否 | 指定会话 ID；若未提供，API 自动创建新 Session 并返回 `session_id` 字段 |
| `environment_id` | string | 否 | 绑定运行环境 ID；未指定则使用默认环境（每个 workspace 有唯一默认 environment） |

## 使用方式

1. **认证**：使用 Bearer [Token](../concepts/token.md) 方式，在 `Authorization: Bearer <api_key>` 请求头中传入百炼平台生成的 API Key（获取路径见 [认证](../../raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-authentication.md)）；
2. **请求地址**：`POST https://dashscope.aliyuncs.com/api/v1/agents/chat/completions`；
3. **请求体示例**（兼容 OpenAI 格式）：
   ```json
   {
     "model": "qwen-plus-agents-202409",
     "messages": [{"role": "user", "content": "查一下今天北京的天气"}],
     "tools": [...],
     "tool_choice": "auto"
   }
   ```
4. **响应结构**：与 OpenAI `chat.completions` 基本一致，额外包含 `session_id`、`environment_id` 和 `vault_id` 字段（若涉及凭证注入）。

## 限制和注意事项

- 单次请求最大 `messages` 数量为 50 条，总 token 上限为 32768（含工具描述）；
- Session 生命周期默认 24 小时，超时后历史不可恢复（可通过 `session_id` 显式续期）；
- Vault 中存储的密钥仅在工具调用时注入，不会出现在任何日志或响应中；
- 不支持流式响应（`stream: true`）——该限制在 [错误码](../../raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-errors.md) 文档中有明确说明，尝试启用将返回 `400 Bad Request` 与 `invalid_request_error`。

## 来源文档

- [Agents API](../../raw/application-api-reference/openai-compatible-agents-api.md)


