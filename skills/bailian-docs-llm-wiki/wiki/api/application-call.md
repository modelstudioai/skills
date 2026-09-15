# application call

`application call` 是百炼平台提供的核心 API 接口，用于以编程方式触发已部署应用的执行流程，支持同步响应与[流式输出](../concepts/streaming-output.md)。该接口统一抽象了底层模型推理、工具调用、上下文管理等能力，开发者无需关心具体模型细节即可集成业务逻辑。其设计兼容 OpenAI 兼容层与 DashScope 原生协议，适用于对话、单次生成、多步骤工作流等多种场景。

## 支持的模型/功能

- 支持所有已在百炼控制台成功发布（Published）的应用，无论其底层使用 Qwen 系列、GLM、Llama 还是自定义微调模型；
- 内置支持[函数调用](../concepts/function-calling.md)（Function Calling）、RAG 检索增强、多轮会话状态维护（需传入 `conversation_id`）；
- 同时提供 OpenAI 兼容的 `/v1/chat/completions` 接口和 DashScope 原生 `/api/v1/applications/{app_id}/call` 接口，二者语义一致但鉴权与参数命名略有差异。详见 [application-dashscope-api-reference.md](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md) 和 [openai-responses-api.md](../../raw/application-api-reference/application-call/openai-responses-api.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，需通过 [obtain-the-app-id-and-workspace-id.md](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 获取 |
| `input` | object | 是 | 用户输入内容，结构为 `{ "text": "..." }` 或含 `files` 字段的富媒体输入 |
| `parameters` | object | 否 | 覆盖应用默认配置，如 `temperature`, `max_output_tokens` 等 |
| `enable_stream` | boolean | 否 | 设为 `true` 启用 SSE 流式响应（仅 DashScope 原生接口支持） |

> **注意**：[OpenAI 兼容接口](../concepts/openai-compatible-api.md)中 `stream` 参数为布尔值，而 DashScope 原生接口中对应字段名为 `enable_stream` 且必须为字符串 `"true"` 或 `"false"` —— 此处行为不一致，请严格按 [application-dashscope-api-reference.md](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md) 的类型要求传参。

## 使用方式

1. 获取 `app_id` 和 `workspace_id`（后者用于部分鉴权场景），参考 [obtain-the-app-id-and-workspace-id.md](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)；
2. 构造 HTTP POST 请求，Header 中携带 `Authorization: Bearer <api_key>` 和 `Content-Type: application/json`；
3. Body 示例（DashScope 原生）：
   ```json
   {
     "app_id": "app-xxx",
     "input": { "text": "你好" },
     "parameters": { "temperature": 0.5 }
   }
   ```

## 限制和注意事项

- 单次请求 `input.text` 长度上限为 32768 字符；含附件时总 payload 不得超过 10MB；
- 同步调用超时时间为 60 秒，流式调用连接空闲超时为 90 秒；
- `conversation_id` 若未显式传入，平台将为每次请求生成新会话，历史上下文不保留；
- 应用若配置了敏感信息过滤或合规拦截策略，响应中可能返回 `status_code: 400` 并附带 `error.code: "CONTENT_FILTERED"`。

## 来源文档

- [应用调用](../../raw/application-api-reference/application-call.md)


