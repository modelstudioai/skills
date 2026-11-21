# openai compatible agents api

百炼平台提供的 OpenAI 兼容 Agents API 是一套遵循 OpenAI API 接口规范的智能体服务接口，支持通过标准 REST 调用创建、管理及运行具备工具调用、多轮记忆与环境隔离能力的 AI Agent。该 API 与 OpenAI 的 `chat.completions` 接口保持高度兼容，便于现有应用无缝迁移。详细设计目标和能力边界请参见 [Agents API](../../raw/application-api-reference/openai-compatible-agents-api.md)。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼自研的 `qwen-plus` 和 `qwen-max` 系列模型（v202408 及以上版本），不支持第三方模型或旧版 `qwen-turbo`。
- **核心功能**：
  - 多轮会话状态自动维护（基于 Session ID）
  - 工具调用（function calling）：支持 `tools` 字段声明函数列表，`tool_choice` 控制调用策略
  - 环境隔离（Environment）：可为不同 Agent 实例绑定独立的 Vault（知识库）与执行上下文
  - 流式响应（`stream: true`）与非流式响应均支持，格式与 OpenAI 完全一致

> **注意**：原始文档中提及的 `qwen-turbo` 在 [Agents API](../../raw/application-api-reference/openai-compatible-agents-api.md) 的快速开始示例中曾出现，但该模型实际已下线支持；最新兼容模型列表以 [概览](../../raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-overview.md) 为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | ✓ | 必须为 `qwen-plus` 或 `qwen-max`，其他值将返回 400 错误 |
| `messages` | array | ✓ | 消息数组，格式同 OpenAI；首条 `system` 消息可包含 agent description 和 tool schema |
| `tools` | array | ✗ | 工具定义列表，每个元素含 `type: "function"` 和 `function` 描述（OpenAI 格式） |
| `tool_choice` | string / object | ✗ | 可选 `"auto"`、`"none"` 或 `{"type": "function", "function": {"name": "xxx"}}` |
| `session_id` | string | ✗ | 若提供，则复用已有会话上下文；否则新建会话（推荐显式传入） |
| `environment_id` | string | ✗ | 绑定指定 Environment，用于隔离 Vault 访问权限与工具执行沙箱 |

## 使用方式

1. **认证**：使用 Bearer Token，Header 中携带 `Authorization: Bearer <api_key>`，密钥需在百炼控制台「API 密钥」中生成  
2. **请求地址**：`POST https://dashscope.aliyuncs.com/api/v1/agents/chat/completions`  
3. **示例调用**（curl）：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/agents/chat/completions" \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-plus",
           "session_id": "sess_abc123",
           "messages": [{"role": "user", "content": "今天北京天气如何？"}],
           "tools": [...]
         }'
   ```
   更多完整示例见 [快速开始](../../raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-quickstart.md)。

## 限制和注意事项

- 单次请求 `messages` 总长度上限为 32768 tokens（含 system message 和 tools 描述）  
- `session_id` 生命周期默认 24 小时，超时后上下文自动清理；如需长期保留，请调用 `/sessions/{id}/extend`  
- 不支持 `response_format`（如 `{"type": "json_object"}`）参数，该字段将被忽略  
- 错误响应结构与 OpenAI 一致，但错误码含义详见 [错误码](../../raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-errors.md) 文档  
- 所有 Agent 调用均计入百炼平台「Agent 调用量」配额，不计入普通 LLM 调用量 quota

## 来源文档

- [Agents API](../../raw/application-api-reference/openai-compatible-agents-api.md)


