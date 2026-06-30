# 流式输出

流式输出（Streaming Output）是百炼平台模型推理与应用调用的一种返回模式：服务端在生成过程中按增量块（chunk）逐步把结果推送给客户端，而不是等整个响应生成完毕再一次性返回。它能显著降低首字延迟、改善交互体验，并允许开发者在长任务进行中实时处理与中断。

## 在百炼平台的使用场景

百炼的多类接口都支持流式输出，但启用方式和事件结构因协议族而异：

### 文本生成模型（Qwen 系列）

无论是 OpenAI 兼容 Chat Completions、Anthropic 兼容 Messages，还是 DashScope 原生接口，均通过请求体中的 `stream` 参数（布尔值）开启流式。开启后服务端按增量返回文本片段，调用方可逐块拼装最终回答。在选型迁移时需注意：兼容接口为保持协议一致可能不暴露全部原生采样参数，但 `stream`、`temperature`、`tools` 等核心参数在三种协议下均可使用。

### 专用模型（翻译、深度研究、OCR、GUI 等）

- **qwen-mt-plus（翻译）**：通过 `stream` 控制是否流式返回译文。
- **qwen-deep-research（深度研究）**：两阶段流程，第一步「反问确认」阶段必须将 `stream` 设为 `true`，以流式获取模型的澄清问题。
- **qwen3.5-ocr / gui-plus**：同样支持 OpenAI 兼容或 DashScope 协议下的流式输出。

### 应用调用（智能体 / 工作流）

通过 OpenAI 兼容 Responses API 调用百炼应用时，`stream` 参数可选，开启后响应以 SSE（Server-Sent Events）方式增量推送，包含文本增量、工具调用增量与状态事件。DashScope 原生 `/completion` 接口同样支持流式返回，便于在工作流长链路中实时展示中间步骤。

### 实时多模态交互（Qwen-Omni-Realtime）

实时 API 基于 WebSocket 长连接，本质上就是一种流式交互：音频通过 `input_audio_buffer.append` 增量上行，模型响应通过 `response.delta`、`response.output_audio.delta` 等事件增量下行。这里「流式」不再是请求级开关，而是会话级协议——VAD 模式下语音结束即自动触发流式响应，Manual 模式下由 `response.create` 显式触发。

## 关键参数与配置

| 参数 | 类型 | 适用接口 | 说明 |
| --- | --- | --- | --- |
| `stream` | bool | Qwen 文本 / 专用模型 / 应用 Responses | 是否开启流式输出，默认 `false` |
| `stream_options.include_usage` | object | OpenAI 兼容接口 | 流式末块附带 token 用量统计 |
| 增量事件 | SSE/WebSocket | Responses API / Omni Realtime | 通过事件类型区分文本增量、音频增量、工具调用增量与终止事件 |

注意事项：

- **拼装顺序**：流式块按服务端发送顺序到达，需按 `delta` 顺序累加文本与工具调用参数；丢弃或乱序处理会导致内容错乱。
- **终止判定**：收到 `finish_reason`（HTTP SSE）或 `response.done`（WebSocket）后才视为响应结束，不应依赖连接关闭判断。
- **中断与取消**：Omni Realtime 用 `response.cancel` 取消进行中的流式响应；HTTP 流式可由客户端主动断开连接，但服务端可能继续计费直至生成完成，建议优先用协议级取消。
- **工具调用**：流式返回工具调用时，函数名与参数也是增量拼接的，需在终止事件后整体执行，避免对半截 JSON 解析。
- **错误处理**：流式中途出错通常以 `error` 事件或异常 HTTP 状态返回，调用方应保留已收到的增量并据此决定重试策略。
- **token 用量**：OpenAI 兼容接口需显式设置 `stream_options.include_usage`，否则流式响应不会附带 usage 统计。

## 选型建议

面向终端用户的对话、实时问答、长文本生成场景应默认开启流式以优化体验；后台批处理、需要完整结构化结果再处理的场景可关闭流式以简化拼装逻辑。实时多模态场景则必须使用 WebSocket 流式协议。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [image generation](../api/image-generation.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [application call](../api/application-call.md)
- [more models](../api/more-models.md)


