# openai compatible agents api

百炼平台提供的 OpenAI 兼容 Agents API 是一套遵循 OpenAI API 接口规范的智能体服务接口，支持通过标准 REST 调用创建、管理及运行具备工具调用、多步推理和状态保持能力的 AI Agent。该 API 与 OpenAI 的 `chat.completions` 接口高度对齐，同时扩展了 Agent 生命周期管理（如 Session、Environment、Vault）等关键能力。详细设计目标和适用场景见 [Agents API](../../raw/application-api-reference/openai-compatible-agents-api.md)。

## 支持的模型/功能

- **模型兼容性**：当前仅支持百炼专属 Agent 模型（如 `qwen-plus-agent-v1`, `qwen-max-agent-v1`），不支持通用大模型（如 `qwen-max`）直接作为 Agent 后端；模型列表以 [概览](../../raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-overview.md) 中的「Supported Models」章节为准。
- **核心功能**：
  - 基于 `tools` 定义的自动工具选择与调用（支持 `function` 和 `code_interpreter` 类型）
  - 多轮 Session 状态持久化（含 message history、tool call 结果缓存）
  - Environment 隔离执行上下文（如沙箱、数据库连接池）
  - Vault 安全存储敏感凭证（API keys、OAuth tokens），供 Agent 运行时按需注入

> **注意**：原始文档中 [快速开始](../../raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-quickstart.md) 示例默认使用 `qwen-max-agent-v1`，但该模型已于 v2024.07 版本起标记为 deprecated；实际生产环境请优先选用 `qwen-plus-agent-v1`，具体变更说明参见 [概览](../../raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-overview.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | ✓ | Agent 模型 ID，必须为平台支持的 Agent 专用模型 |
| `messages` | array | ✓ | 与 OpenAI 格式一致，首条消息建议为 `role: "system"` 描述 Agent 行为约束 |
| `tools` | array | ✗ | 工具定义列表，格式同 OpenAI `tools` 字段；若未提供则禁用工具调用 |
| `tool_choice` | string / object | ✗ | 控制工具调用策略，支持 `"auto"`、`"none"` 或 `{"type": "function", "function": {"name": "xxx"}}` |
| `session_id` | string | ✗ | 指定已有 Session ID 以复用上下文；首次调用可省略，服务端自动生成 |
| `environment_id` | string | ✗ | 绑定预配置的 Environment（如 Python 沙箱、RAG 索引），详见 [Environments](../../raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-environment.md) |

## 使用方式

1. **认证**：使用 Bearer [Token](../concepts/token.md) 方式，在 `Authorization` Header 中传入 `Bearer <api_key>`；API Key 需在百炼控制台「API 密钥管理」中创建，权限需包含 `agents:run`；认证细节见 [认证](../../raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-authentication.md)。
2. **请求示例**（curl）：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/agents/chat/completions \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-plus-agent-v1",
           "messages": [{"role": "user", "content": "查一下今天北京的天气"}],
           "tools": [{"type": "function", "function": {"name": "get_weather", "parameters": {...}}}]
         }'
   ```
3. **响应结构**：与 OpenAI `chat.completions` 一致，含 `choices[0].message` 和 `choices[0].delta` 流式响应支持；当触发工具调用时，`message.tool_calls` 字段返回待执行的工具列表。

## 限制和注意事项

- 单次请求最大 `messages` 数量为 50 条（含 system、user、assistant、tool 四类角色）；
- Session 生命周期默认 24 小时，超时后关联 history 自动清理；如需长期会话，请自行维护 `session_id` 并定期调用 `/sessions/{id}/extend`；
- Vault 中存储的密钥**不会自动注入到所有工具调用中**，必须在 tool function definition 的 `description` 中显式声明依赖（例如 `"Requires vault key 'weather_api_key'"`），否则 Agent 不会加载；
- 错误处理应基于 [错误码](../../raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-errors.md) 文档中的 `error.code` 字段做分支判断，而非仅依赖 HTTP 状态码。

## 来源文档

- [Agents API](../../raw/application-api-reference/openai-compatible-agents-api.md)


