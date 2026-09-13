# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式响应的模型调用接口，适用于对话交互、实时语音转写、代码补全等对响应时延敏感的场景。它支持 SSE（Server-Sent Events）和 WebSocket 两种传输协议，并提供完整的流式 token 输出与事件状态通知。该接口不替代标准 RESTful `/v1/chat/completions`，而是作为其补充，专为实时性要求高的用例设计。

## 支持的模型与功能

- 当前支持的模型包括 `qwen-max`、`qwen-plus`、`qwen-turbo` 及部分语音模型（如 `paraformer-realtime-v1`），具体以控制台「模型服务」页的「实时 API 可用模型」列表为准；  
- 功能上支持：流式文本生成（`text/event-stream`）、多轮上下文保持（需显式传入 `conversation_id`）、中断恢复（通过 `continue_from` 参数）、以及结构化输出（启用 `response_format = {"type": "json_object"}` 时需配合 `qwen-max` 等支持 JSON Schema 的模型）。  
- 不支持图像输入、文件上传或[函数调用](../concepts/function-calling.md)（function calling）——这些能力仅在 [标准 Chat API](../../raw/model-api-reference/chat-completion-api.md) 中提供。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型 ID，必须为实时 API 明确支持的型号，详见 [Realtime API (raw/model-api-reference/realtime-api-user-guide.md)](../../raw/model-api-reference/realtime-api-user-guide.md) 文档中的模型列表 |
| `messages` | array | 是 | 消息数组，格式同标准 Chat API，但 `role: "system"` 不被忽略（与标准 API 行为不同） |
| `stream` | boolean | 是 | 必须为 `true`；设为 `false` 将返回 400 错误 |
| `max_tokens` | integer | 否 | 最大生成 token 数，默认 2048，硬上限为 4096 |
| `temperature` | number | 否 | 采样温度，范围 `[0.0, 2.0]`，默认 `0.8`；注意该参数在流式响应中**不可动态调整**，需在首次请求中固定 |

> **注意**：原始文档中提到的 `top_p` 参数在 v2024.07+ 版本已弃用，实际请求中传入将被静默忽略；请参考 [Realtime API (raw/model-api-reference/realtime-api-user-guide.md)](../../raw/model-api-reference/realtime-api-user-guide.md) 的最新参数说明，或使用 `presence_penalty` / `frequency_penalty` 替代。

## 使用方式

1. **认证**：使用 `Authorization: Bearer <api_key>`，API Key 需具备 `model:realtime:invoke` 权限；  
2. **Endpoint**：`POST https://dashscope.aliyuncs.com/api/v1/realtime/chat/completions`；  
3. **请求头**：必须设置 `Content-Type: application/json` 和 `Accept: text/event-stream`（SSE）或 `Connection: upgrade` + `Upgrade: websocket`（WebSocket）；  
4. **响应解析**：SSE 响应按 `data:` 行分隔，每行是一个 JSON 对象；需按 `event` 字段区分 `message`、`error`、`done` 等类型；完整解析逻辑可参考 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide.md) 提供的 reference implementation。

## 限制和注意事项

- 单连接最大持续时间：15 分钟（超时后连接关闭，需重连）；  
- 并发连接数限制：免费版 ≤ 5，企业版按配额配置，超出返回 `429 Too Many Requests`；  
- 流式响应中 `delta.content` 可能为空字符串（例如模型正在思考或生成非文本内容），客户端需容错处理；  
- 不支持 `logprobs`、`n > 1`、`stop` 字符串数组等高级采样参数；  
- 所有请求日志默认保留 7 天，审计与调试请优先使用 `trace_id` 字段关联上下游调用。  

> **注意**：[概述](https://help.aliyun.com/zh/model-studio/realtime-api-overview) 页面中提及的“自动重连机制”在当前 SDK v1.3.0 中尚未实现，需开发者自行实现指数退避重连逻辑；该差异已在 [Realtime API (raw/model-api-reference/realtime-api-user-guide.md)](../../raw/model-api-reference/realtime-api-user-guide.md) 的「客户端集成」章节中标注为待办（TODO）。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


