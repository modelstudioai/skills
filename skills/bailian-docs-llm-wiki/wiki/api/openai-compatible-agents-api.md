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
| `messages` | array | ✓ | 与 OpenAI 格式一致，首条 `user` 消息触发 Agent 初始化 |
| `tools` | array | ✗ | 工具定义列表，格式同 OpenAI `tools` 字段；若为空则退化为普通 chat |
| `tool_choice` | string / object | ✗ | 控制工具调用策略（`"auto"`/`"none"`/`{"type": "function", "function": {"name": "xxx"}}`） |
| `session_id` | string | ✗ | 指定已有 Session 继续对话；未提供则新建 Session（详见 [Sessions](../../raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-session.md)） |
| `environment_id` | string | ✗ | 指定执行环境，用于隔离资源与权限 |

## 使用方式

1. **认证**：使用 Bearer [Token](../concepts/token.md)，Header 中携带 `Authorization: Bearer <api_key>`；API Key 需在控制台「API 密钥管理」中创建，权限需包含 `agents:run`；认证机制细节见 [认证](../../raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-authentication.md)。
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
3. **响应结构**：与 OpenAI `chat.completions` 一致，但 `choices[0].message` 可能含 `tool_calls` 字段；若 Agent 触发多轮工具调用，需按 `session_id` 轮询或监听流式响应中的 `delta.tool_calls`。

## 限制和注意事项

- 单次请求最大 `messages` 数量为 50 条（含系统、用户、助手、tool 消息）；超出将返回 `400 Bad Request`（错误码参考 [错误码](../../raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-errors.md)）。
- Session 默认 TTL 为 24 小时，超时后关联 history 与 environment 资源自动释放；如需长期会话，请显式调用 `/sessions/{id}/extend`。
- Vault 中存储的密钥**不会**自动注入所有 Agent 调用，必须在 `tools` 或 `environment` 配置中显式声明引用路径（如 `"vault://weather-api-key"`），否则视为未授权访问。
- 流式响应（`stream=true`）下，`tool_calls` 的 `id` 字段可能跨 chunk 分片传输，客户端需按 `index` 合并；此行为与 OpenAI 不完全一致，详见 [Agents](../../raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-agent.md) 文档说明。

## 来源文档

- [Agents API](../../raw/application-api-reference/openai-compatible-agents-api.md)


