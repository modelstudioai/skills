# get started with agents

Agent 是百炼平台提供的可编程智能体服务，支持开发者快速构建具备规划、工具调用和多轮推理能力的应用。本文档指导你完成 Agent 的初始化配置、核心参数设置及基础调用流程。所有操作均基于百炼 API v3 接口，需配合有效的 API Key 和模型授权。

## 支持的模型与功能

当前 Agent 服务仅支持 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列模型（详见 [开始使用](../../raw/application-user-guide/get-started-with-agents.md)）。不支持第三方模型或自定义 LLM 后端。Agent 内置以下关键能力：  
- 自动化工具选择与调用（需提前注册 Tool Schema）  
- 多轮对话状态维护（最长支持 10 轮历史上下文）  
- 结构化输出约束（通过 `response_format` 参数启用 JSON Schema 校验）  

> **注意**：原始文档中提及的 `qwen-72b-chat` 已于 2024-06 版本下线，实际调用将返回 `model_not_found` 错误；请以控制台「模型列表」实时状态为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 必须为 `qwen-max`/`qwen-plus`/`qwen-turbo` 之一，大小写敏感 |
| `tools` | array | 否 | 工具定义数组，每个元素需包含 `name`、`description` 和 `parameters`（遵循 OpenAPI 3.0 Schema） |
| `tool_choice` | string \| object | 否 | 可选 `"auto"`（默认）、`"none"` 或 `{ "type": "function", "function": { "name": "xxx" } }`；详见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) |
| `max_iterations` | integer | 否 | 最大推理步数，默认 5，取值范围 1–15 |

## 使用方式

1. **准备工具定义**：按 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中的 Schema 规范编写工具描述；  
2. **发起请求**：向 `/v3/agents/run` 发送 POST 请求，携带 `model`、`messages`（含用户初始 query）及可选 `tools`；  
3. **处理响应**：检查 `status` 字段（`success` / `tool_calls` / `failed`），对 `tool_calls` 类型响应需同步执行工具并提交结果至 `/v3/agents/continue`。

## 限制和注意事项

- 单次请求最大输入 tokens 为 32768（含 system prompt、messages 和 tools 描述），超限将返回 `400 Bad Request`；  
- `tools` 数量上限为 20 个，单个 tool 的 `parameters` Schema 深度不得超过 5 层；  
- Agent 不支持流式响应（`stream: true` 将被忽略），所有输出均为完整 JSON 对象；  
- 若在调试中遇到 `invalid_tool_call` 错误，请确认工具名拼写与 `tool_choice.name` 严格一致——该行为与 [开始使用](../../raw/application-user-guide/get-started-with-agents.md) 文档描述一致，但与旧版 SDK 示例存在差异，建议以 API 实际返回为准。

## 来源文档

- [开始使用](../../raw/application-user-guide/get-started-with-agents.md)


