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
| `session_id` | string | ✗ | 指定已有 Session ID 以复用上下文；首次调用可省略，由服务自动生成 |
| `environment_id` | string | ✗ | 绑定预配置的 Environment（如含特定 Python 包的沙箱），详见 [Environments](../../raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-environment.md) |

## 使用方式

1. **认证**：使用 Bearer Token 方式，在 `Authorization` Header 中传入 `Bearer <api_key>`；密钥需在控制台「API Keys」页面生成，权限需包含 `agents:run`；认证细节见 [认证](../../raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-authentication.md)。
2. **请求示例**（curl）：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/compatible-mode/v1/agents/chat/completions" \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-plus-agent-v1",
           "messages": [{"role": "system", "content": "你是一个天气查询助手，使用 get_weather 工具获取实时天气。"}, {"role": "user", "content": "北京今天气温多少？"}],
           "tools": [{"type": "function", "function": {"name": "get_weather", "parameters": {"type": "object", "properties": {"city": {"type": "string"}}}}}],
           "tool_choice": "auto"
         }'
   ```
3. **响应结构**：与 OpenAI `chat.completions` 基本一致，但新增 `session_id` 字段用于后续续聊；工具调用结果通过 `tool_calls` 返回，需客户端自行执行并提交 `tool_result` 消息完成闭环。

## 限制和注意事项

- 单次请求最大 `messages` 数量为 50 条，总 token 上限为 32768（含 tools 定义）；
- Session 默认 TTL 为 24 小时，超时后历史不可恢复；如需长期状态，请主动调用 `/sessions/{id}/extend` 接口；
- Vault 中存储的凭证**不会自动注入**到所有 Agent 调用中，必须在 `tools` 或 `messages` 中显式引用（如通过 `{{vault.weather_api_key}}` 占位符），具体语法见 [Vaults](../../raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-vault.md)；
- 错误处理应优先依据响应中的 `error.code`（如 `invalid_tool_call`, `session_not_found`），完整错误码列表见 [错误码](../../raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-errors.md)。

## 来源文档

- [Agents API](../../raw/application-api-reference/openai-compatible-agents-api.md)


