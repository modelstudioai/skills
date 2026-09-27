# application call

`application call` 是百炼平台提供的核心能力，允许开发者通过 API 方式调用已部署的 AI 应用（App），将用户输入传递给应用工作流并获取结构化响应。该接口统一抽象了底层模型执行、上下文管理与工具调用等细节，支持同步/流式两种调用模式。其设计目标是让业务系统快速集成定制化 AI 能力，无需关心模型部署与编排逻辑。

## 支持的模型/功能

- 支持所有已在百炼控制台成功发布（Published）的应用，无论其内部使用 Qwen 系列、GLM 系列或其他兼容模型；
- 支持多轮对话状态保持（需传入 `conversation_id`）、文件上传（通过 `files` 参数）、自定义元数据透传（`metadata` 字段）；
- 支持[函数调用](../concepts/function-calling.md)（Function Calling）能力，当应用配置了工具节点时，API 会返回 `tool_calls` 结构；该行为与 [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md) 定义一致。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，需通过 [获取APP ID 和 Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 获取 |
| `input` | object | 是 | 用户输入内容，格式为 `{ "text": "..." }` 或含多模态字段的对象 |
| `user_id` | string | 否 | 用于会话隔离与审计，建议传入业务侧用户标识 |
| `stream` | boolean | 否 | `true` 时启用 SSE 流式响应；注意流式响应中 `tool_calls` 仅在最终 `done` 事件中完整返回 |
| `parameters` | object | 否 | 覆盖应用默认参数（如 `temperature`, `top_p`），详见 [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md) 的参数映射规则 |

> **注意**：`parameters` 中的 `max_tokens` 在部分旧版应用中可能被忽略，实际受应用配置的 `output_max_length` 限制——请以 [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md) 文档中 `max_output_tokens` 字段为准。

## 使用方式

1. 确保应用状态为 **Published**（非 Draft 或 Testing）；
2. 构造 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/call`；
3. 设置 Header：`Authorization: Bearer <api_key>`，`Content-Type: application/json`；
4. 发送 JSON Body（示例）：
```json
{
  "input": { "text": "总结这篇文档的核心要点" },
  "user_id": "u_123456",
  "stream": false,
  "parameters": { "temperature": 0.3 }
}
```

## 限制和注意事项

- 单次请求 `input.text` 长度上限为 100,000 字符；文件总大小不超过 50MB；
- `conversation_id` 若未提供，系统将自动生成新会话；同一 `conversation_id` 下的历史消息默认保留 30 天（可配置）；
- 流式响应中，中间 chunk 不包含 `tool_calls` 字段，仅最终 `{"event": "done", ...}` 消息携带完整工具调用结果——此行为与 [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md) 兼容，但与早期文档描述存在差异；
- 调用失败时，HTTP 状态码非 2xx，响应体含 `code` 与 `message` 字段，常见错误见 [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md) 错误码表。

## 来源文档

- [应用调用](../../raw/application-api-reference/application-call.md)


