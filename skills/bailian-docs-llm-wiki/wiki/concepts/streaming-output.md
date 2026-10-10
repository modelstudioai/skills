# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种实时增量响应机制，允许模型在推理过程中将结果分块、逐步返回，而非等待全部计算完成后再一次性返回完整结果。该机制显著降低端到端延迟，提升用户体验，尤其适用于语音交互、实时对话、长文本生成等对响应速度敏感的场景。

## 在百炼平台的不同场景中，这个概念如何使用

流式输出在百炼平台中并非统一协议，而是根据接口类型和通信方式适配不同实现：

- **RESTful 音频 API（TTS/ASR/语音对话等）**：通过 `stream=true` 参数启用，服务端以 Server-Sent Events（SSE）格式返回事件流，每帧包含音频片段（base64 编码的 PCM/WAV）、识别文本片段或状态更新（如 `{"event": "started"}`）。适用于低集成复杂度的 Web 或后端调用。

- **Realtime API（WebSocket）**：原生支持双向流式交互。客户端发送 `input_audio` 或 `input_text` 后，服务端立即推送 `output_text_delta`、`output_audio_delta` 等增量事件，支持毫秒级响应与实时中断（`cancel` 事件）。适用于智能硬件、语音助手等强实时性场景。

- **Omni Realtime API（多模态 WebSocket）**：在 `stream=true` 强制要求下，统一处理语音、文本、图像输入，并流式返回混合模态输出（如 ASR 文本流 + TTS 音频流 + 图像理解摘要），所有事件均按时间戳对齐，保障多模态同步体验。

- **Application Call（智能体/工作流调用）**：支持两种流式模式：  
  - DashScope 原生方式：设置 Header `X-DashScope-SSE: enable`，响应为标准 SSE；  
  - OpenAI 兼容 Responses API：在请求体中设 `"stream": true`，格式与 OpenAI 保持一致。  
  推荐启用 `incremental_output=true`，确保 `delta.content` 为纯增量文本（非全量累积），便于前端逐字渲染。

- **应用组件 API（基础模型调用）**：通过 `stream=true` 参数触发 SSE 流式响应，返回结构化 `delta` 对象（含 `content`、`tool_calls` 等字段），适用于构建自定义 Agent 或轻量级 RAG 应用。

> ✅ **最佳实践**：所有支持流式的接口，均应优先启用流式输出——它可降低首字节延迟（Time to First [Token](token.md), TTFT）达 50% 以上，并支持自然的“边说边听”“边打边显”交互范式。

## 关键参数和配置

| 接口类型 | 启用方式 | 必填参数 | 推荐配套配置 | 协议/格式 |
|----------|----------|-----------|----------------|------------|
| RESTful 音频 API | `parameters.stream = true`（或顶层 `stream: true`） | `model`, `input` | `parameters.sample_rate`（按模型要求指定） | SSE（`data: {...}\n\n`） |
| Realtime API / Omni Realtime API | URL query 中 `stream=true`（强制） | `model`, `api_key` | `session_id`（维持上下文）、`max_output_tokens`（控长） | WebSocket 事件（JSON） |
| Application Call（DashScope） | Header `X-DashScope-SSE: enable` | `app_id`, `input` | `incremental_output=true`（确保 delta 为增量） | SSE |
| Application Call（OpenAI 兼容） | 请求体 `"stream": true` | `app_id`, `input` | `"stream_options": {"include_usage": false}`（减小开销） | SSE（OpenAI 格式） |
| 应用组件 API | `stream=true`（顶层布尔参数） | `model`, `input.messages` | `parameters.temperature=0.3`（降低随机性，提升流式稳定性） | SSE |

⚠️ 注意：  
- `stream=true` 仅在明确标注“支持流式”的模型和接口中生效，对不支持的模型（如部分旧版 `qwen-max` 直接调用）将被忽略或返回错误；  
- 所有流式响应必须按对应协议解析（不可直接 JSON.parse 整个响应体）；  
- 客户端需主动处理连接中断、重连、超时（如 Realtime API 单连接最长 30 分钟）。

## 面向开发者，简洁实用

- **快速验证**：用 `curl` 调用任意支持流式的 RESTful 接口时，添加 `-N`（no-buffer）参数并配合 `grep data:` 查看实时数据流；  
- **前端渲染**：监听 SSE 的 `message` 事件，对 `event.data` 做 `JSON.parse()`，拼接 `delta.content` 即可实现打字机效果；  
- **音频流处理**：TTS 流式响应中的 `output.audio` 字段为 base64 PCM 音频分片，建议使用 Web Audio API 动态解码播放，避免内存堆积；  
- **错误防御**：始终监听 `error` 事件（WebSocket）或 `event: error`（SSE），并检查 `data:` 行是否含 `{"code":"..."}` 错误对象；  
- **性能提示**：流式不降低总计算耗时，但极大改善感知延迟；若需极致低延迟，请优先选用 Realtime API 或 Omni Realtime API。

## 关联主题页

- [audio api references](../api/audio-api-references.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [application call](../api/application-call.md)
- [application component api reference](../api/application-component-api-reference.md)


