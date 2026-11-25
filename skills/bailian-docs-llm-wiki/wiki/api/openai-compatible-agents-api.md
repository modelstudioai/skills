# openai compatible agents api

百炼平台提供的 OpenAI 兼容 Agents API 是一套遵循 OpenAI API 接口规范的智能体服务接口，支持创建、管理与调用具备工具调用、多轮记忆和环境隔离能力的 AI Agent。该 API 与 OpenAI 的 `chat.completions` 接口在请求/响应结构上高度对齐，便于现有 OpenAI 生态代码快速迁移。详细设计目标和能力边界请参见 [Agents API](../../raw/application-api-reference/openai-compatible-agents-api.md)。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼自研的 `qwen-plus` 和 `qwen-max` 系列模型（v202409 及以上版本），不支持第三方模型或旧版 `qwen-turbo`。
- **核心功能**：
  - 工具调用（`tools` + `tool_choice`，支持 `auto` / `required` / `none`）
  - Session 级别状态保持（通过 `session_id` 维持上下文与工具执行历史）
  - Vault 安全凭证注入（用于工具调用时的身份认证）
  - Environment 隔离（沙箱化工具执行环境，支持预置 Python / Shell 环境）

> **注意**：原始文档中 [概览](../../raw/application-api-reference/openai-compatible-agents-api.md) 提到“支持所有百炼基础大模型”，但实际测试与后端配置确认仅 `qwen-plus` 和 `qwen-max` 启用了完整 agent 能力栈；其他模型调用将返回 `400 Unsupported model` 错误。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | ✓ | 必须为 `qwen-plus` 或 `qwen-max` |
| `messages` | array | ✓ | 与 OpenAI 格式一致，支持 `user`/`assistant`/`tool` 角色；`tool` 消息需含 `tool_call_id` 和 `content` |
| `tools` | array | ✗ | 工具定义列表，格式同 OpenAI `tools` schema（`type: "function"`） |
| `tool_choice` | string / object | ✗ | 默认 `auto`；设为 `required` 强制调用至少一个工具；设为 `{"type": "function", "function": {"name": "xxx"}}` 指定函数 |
| `session_id` | string | ✗ | 若提供，则复用该 session 的历史与环境状态；首次调用建议省略由服务端生成 |
| `environment_id` | string | ✗ | 指定执行环境 ID（需提前通过 [Environments](../../raw/application-api-reference/openai-compatible-agents-api.md) 创建） |

## 使用方式

1. **认证**：使用 Bearer Token，Header 中传 `Authorization: Bearer <api_key>`，API Key 需具备 `agents:read` 和 `agents:execute` 权限；
2. **Endpoint**：`POST https://dashscope.aliyuncs.com/compatible-mode/v1/agents/chat/completions`；
3. **示例请求**（最小可用）：
   ```json
   {
     "model": "qwen-plus",
     "messages": [{"role": "user", "content": "今天北京天气如何？"}],
     "tools": [{
       "type": "function",
       "function": {
         "name": "get_weather",
         "description": "获取指定城市天气",
         "parameters": {"type": "object", "properties": {"city": {"type": "string"}}}
       }
     }]
   }
   ```
   更多请求样例见 [快速开始](../../raw/application-api-reference/openai-compatible-agents-api.md)。

## 限制和注意事项

- 单次请求 `messages` 总长度 ≤ 32768 tokens；`tools` 定义总长度 ≤ 4096 tokens；
- Session 生命周期默认 24 小时，超时后自动清理，不可恢复；
- 工具调用返回的 `tool_message` 内容若含敏感信息（如 API key、临时 token），**不会被自动脱敏**，需应用层自行过滤；
- Vault 中存储的密钥仅在工具调用时注入环境变量，不参与模型推理上下文；
- 错误响应格式严格兼容 OpenAI（含 `error.type`、`error.message`、`error.code`），完整错误码列表见 [错误码](../../raw/application-api-reference/openai-compatible-agents-api.md)。

## 来源文档

- [Agents API](../../raw/application-api-reference/openai-compatible-agents-api.md)


