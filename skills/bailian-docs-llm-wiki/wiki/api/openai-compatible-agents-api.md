# openai compatible agents api

百炼平台提供的 OpenAI 兼容 Agents API 是一套遵循 OpenAI API 设计规范的智能体（Agent）调用接口，支持通过标准 REST 请求创建、管理及运行具备工具调用、多步推理能力的 Agent 实例。该 API 与 OpenAI 的 `/v1/chat/completions` 接口保持高度兼容，便于现有 OpenAI 生态应用快速迁移。详细设计目标和适用场景见 [Agents API](../../raw/application-api-reference/openai-compatible-agents-api.md)。

## 支持的模型与功能

- **模型支持**：当前仅支持 `qwen-plus` 和 `qwen-max` 两款百炼专属大模型；不支持 `qwen-turbo` 或第三方模型（如 `gpt-4o`）。  
- **核心功能**：  
  - 基于 `tools` 定义的[函数调用](../concepts/function-calling.md)（function calling），支持并行/串行工具执行；  
  - Session 状态持久化（需显式启用 `enable_session`）；  
  - 自定义 Environment（沙箱环境）与 Vault（安全凭证存储）集成；  
  - 流式响应（`stream: true`）与非流式响应均支持。  
更多能力边界说明请参考 [概览](../../raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-overview.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 固定为 `qwen-plus` 或 `qwen-max`；传入其他值将返回 400 错误 |
| `messages` | array | 是 | 与 OpenAI 格式一致，首条消息建议为 `user` 角色；系统提示词应置于 `system` 消息中 |
| `tools` | array | 否 | 工具定义列表，格式同 OpenAI `tools` schema；若未提供则退化为普通 chat 接口 |
| `tool_choice` | string / object | 否 | 可选 `"auto"`（默认）、`"none"` 或 `{"type": "function", "function": {"name": "xxx"}}` |
| `enable_session` | boolean | 否 | 设为 `true` 时启用会话状态跟踪（需配合 `session_id` 使用）；详见 [Sessions](../../raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-session.md) |

> **注意**：`temperature`、`top_p` 等采样参数虽可传入，但当前版本中仅 `qwen-max` 对其生效；`qwen-plus` 固定使用服务端预设参数，此行为与 [概览](../../raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-overview.md) 中“模型行为一致性”描述存在偏差，以实际调用结果为准。

## 使用方式

1. **认证**：使用 Bearer Token 方式，在 `Authorization` Header 中传入 `Bearer <api_key>`；API Key 需在百炼控制台「API 密钥」中创建，且需具备 `agents:read` 和 `agents:invoke` 权限。认证机制细节见 [认证](../../raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-authentication.md)。  
2. **请求示例（cURL）**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-max",
           "messages": [{"role": "user", "content": "今天北京天气如何？"}],
           "tools": [...],
           "tool_choice": "auto"
         }'
   ```
3. **响应结构**：与 OpenAI 完全兼容，含 `id`、`choices[0].message`、`choices[0].finish_reason`（可能为 `"tool_calls"` 或 `"stop"`）等字段；工具调用结果以 `choices[0].message.tool_calls` 返回。

## 限制和注意事项

- 单次请求最大 `messages` 数量为 50，总 token 数上限为 32768（含 tools schema）；超出将返回 `400 Bad Request`。  
- `session_id` 若未显式传入且 `enable_session=true`，服务端将自动生成并返回于响应头 `X-Session-ID` 中；客户端需自行维护该 ID 用于后续请求。  
- 不支持 `response_format`（如 `{"type": "json_object"}`）参数，传入将被忽略。  
- 错误码统一遵循 OpenAI 兼容格式，但部分业务错误（如 Vault 权限不足）映射为 `500 Internal Server Error`，完整列表见 [错误码](../../raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-errors.md)。

## 来源文档

- [Agents API](../../raw/application-api-reference/openai-compatible-agents-api.md)


