# 流式输出

流式输出（Streaming）是指模型在生成过程中逐段返回内容，而非等待完整结果一次性返回的调用方式。在百炼平台中，流式输出广泛用于文本生成、实时多模态交互、应用调用与图像生成等场景，以降低首字延迟、提升用户体验。

## 在百炼平台中的使用场景

### 文本生成模型（Qwen 系列）

Qwen 系列模型支持通过 OpenAI 兼容 Chat Completions、Anthropic 兼容 Messages、DashScope 原生接口调用，均可启用流式输出。OpenAI 兼容 Responses 接口同样支持流式。开发者只需在请求中将 `stream` 参数设为 `true`，响应即以 Server-Sent Events（SSE）增量片段形式逐块返回。

### 实时多模态交互（Qwen-Omni-Realtime）

Qwen-Omni-Realtime API 基于 WebSocket 长连接，本质即为流式双向通信。会话由客户端事件与服务端事件驱动：

- 客户端通过 `input_audio_buffer.append` 流式追加音频字节到缓冲区，建议以较小数据块发送以提升 VAD 响应速度。
- 服务端在生成响应时通过 `response.delta` 等事件增量输出文本与音频片段，客户端实时渲染。
- Manual 模式下，关闭 `turn_detection` 时每个事件最多放置 15 MiB 音频；通过 SDK 的 `append_audio` 流式发送较小块可让 VAD 更迅速。

### 应用调用

百炼应用（智能体、工作流、Agent 2.0）通过 OpenAI 兼容 Responses API 或 DashScope 原生 `/completion` 接口调用时，均支持流式返回。 Responses API 在 `stream` 为 `true` 时按 SSE 增量推送应用输出与中间步骤；DashScope 原生接口在 `stream` 为 `true` 时通过 `X-DashScope-Streaming` 头声明，并以增量方式返回对话与工具调用结果。

### 图像生成

图像生成类接口以异步任务为主：提交请求获得 `task_id`，再轮询 `GET /api/v1/tasks/{task_id}` 取结果。部分接口（如千问-文生图、文生图 V2 兼容模式）提供同步调用，少数能力支持流式。流式与异步的差异在于：流式为增量推送生成过程，异步为提交-轮询模型，二者不应混淆。

## 关键参数与配置

- **`stream`**：是否启用流式输出，布尔值，默认 `false`。文本生成与应用调用接口通用。
- **SSE 格式**：OpenAI 兼容接口遵循 `data: {...}\n\n` 格式，结尾以 `data: [DONE]` 标记完成；DashScope 原生接口的增量结构以 `output` 字段逐步累加。
- **`X-DashScope-Streaming`**：DashScope 原生接口启用流式时需在请求头声明 `enable`。
- **WebSocket 事件流**：实时多模态接口中，音频与文本以事件为粒度流式传输，无需显式 `stream` 参数。
- **流式与工具调用**：当响应包含工具调用（Function Calling）时，流式输出会将工具参数以增量片段返回，开发者需在事件回调中累积拼接。

## 注意事项

- 流式输出要求客户端正确处理增量片段的累积与拼接，避免漏字段或顺序错乱。
- 实时多模态场景下，音频流式块的发送速率与大小会影响 VAD 灵敏度与首字延迟，建议按 SDK 推荐块大小发送。
- 异步图像生成接口不等于流式，需通过轮询获取最终结果；只有显式声明 `stream` 的接口才提供增量推送。
- 迁移自 OpenAI / Anthropic 客户端时，应先确认目标 Qwen 模型在对应兼容接口下对 `stream` 参数的支持情况。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [application call](../api/application-call.md)
- [image generation](../api/image-generation.md)


