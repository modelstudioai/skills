# openai compatible agents api

OpenAI Compatible Agents API 是百炼平台提供的标准化接口，兼容 OpenAI 的 Agents 协议规范，支持构建具备工具调用、多步推理和状态管理能力的智能体应用。该 API 采用 RESTful 设计，与 OpenAI 的 `/v1/agents` 等路径保持语义对齐，便于迁移现有基于 OpenAI Agents SDK 的代码。详细设计目标和协议映射见 [Agents API](../../raw/application-api-reference/openai-compatible-agents-api.md)。

## 支持的模型与功能

- 当前仅支持 `qwen-plus` 和 `qwen-max` 两款模型作为 agent 的底层执行引擎（不支持 `qwen-turbo` 或历史旧版模型）；
- 支持完整 OpenAI Agents 功能集：tool calling（含自定义 function tools）、session-aware state persistence、environment sandboxing（通过 `environment_id` 隔离执行上下文）、vault-backed secrets 注入；
- 不支持 streaming 响应（`stream: true` 将被忽略），所有响应均为完整 JSON object；此限制在 [Agents API](../../raw/application-api-reference/openai-compatible-agents-api.md) 的“限制”小节中有明确说明。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 必须为 `qwen-plus` 或 `qwen-max`；其他值将返回 400 错误 |
| `tools` | array | 否 | OpenAI-style tool definition 列表；每个 tool 必须包含 `type: "function"` 和 `function` 字段；详见 [Agents API](../../raw/application-api-reference/openai-compatible-agents-api.md) 中的 tool schema 示例 |
| `tool_choice` | string / object | 否 | 可选 `"auto"`、`"none"` 或 `{ "type": "function", "function": { "name": "xxx" } }`；默认为 `"auto"` |
| `session_id` | string | 否 | 指定已有 session；若未提供则自动创建新 session；session 生命周期为 24 小时（不可配置） |
| `environment_id` | string | 否 | 绑定预置 environment（如 `"prod-db"`），用于控制 tool 执行权限边界 |

> **注意**：原始文档中 `openai-compatible-agents-api-session.md` 提到 session 默认 TTL 为 72 小时，但实际服务端强制设为 24 小时且不可覆盖——请以运行时行为为准，该差异已在 [Agents API](../../raw/application-api-reference/openai-compatible-agents-api.md) 的错误码文档中补充说明。

## 使用方式

1. **认证**：使用 Bearer Token，Header 中携带 `Authorization: Bearer <api_key>`；API Key 需具备 `agents:read` 和 `agents:execute` 权限；
2. **创建 Agent**：`POST https://dashscope.aliyuncs.com/v1/agents`，传入 `model`、`tools` 等参数，返回 `agent_id`；
3. **运行 Agent**：`POST https://dashscope.aliyuncs.com/v1/agents/{agent_id}/runs`，可指定 `session_id` 复用上下文；
4. **轮询结果**：通过 `GET /v1/agents/{agent_id}/runs/{run_id}` 获取 status（`queued` → `in_progress` → `completed`/`failed`）；不支持 webhook 回调。

## 限制和注意事项

- 单次 run 最大 token 数为 32768（输入 + 输出），超限将返回 `400 invalid_request_error`；
- tool 函数名（`function.name`）必须符合 Python 标识符规则（字母/数字/下划线，不以数字开头），否则触发 `invalid_tool_name` 错误；
- Vault 中 secret 的 key 名需与 tool 函数签名中的参数名严格一致，大小写敏感；
- 所有请求必须在 60 秒内完成，超时将中断执行并返回 `504 gateway_timeout`；该行为与 [Agents API](../../raw/application-api-reference/openai-compatible-agents-api.md) 文档一致。

## 来源文档

- [Agents API](../../raw/application-api-reference/openai-compatible-agents-api.md)


