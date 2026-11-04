# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种实时、增量式响应机制，服务端在模型推理过程中持续生成并分块推送结果（如 token、音频帧、文本片段），而非等待全部计算完成后再返回完整响应。该机制显著降低端到端延迟，提升交互自然度，是构建低延迟对话、语音助手、实时音视频应用的核心能力。

## 在百炼平台的不同场景中如何使用

流式输出并非统一接口，而是根据调用协议与业务场景，通过不同技术路径实现：

- **Model Experience（RESTful /v1/models/{model_id}/invoke）**  
  适用于文本生成、部分全模态及 TTS 模型。启用方式：在请求 `body` 中设置 `"enable_streaming": true`。响应为标准 SSE（Server-Sent Events）格式，`Content-Type: text/event-stream`，每行以 `data:` 开头，需按 SSE 协议解析（如 `data: {"output": {"text": "Hello"}}`）。支持模型包括 `qwen-max`、`qwen-plus`、`wanx-v1`（TTS）、`qwen3-omni-flash-realtime`（部分能力）等。

- **Realtime API（WebSocket）**  
  面向强实时交互场景（如语音对话、多轮上下文感知），**强制流式**（`stream: true` 固定开启）。客户端通过 WebSocket 连接，接收结构化事件（如 `output.text.delta`、`output.audio.chunk`、`tool_calls`），支持输入流式注入（`input.audio`/`input.text` 分片）、运行时中断（`input.interrupt`）和会话状态保持。典型模型：`qwen-audio-realtime-v1`、`qwen2.5-7b-instruct-realtime`、`qwen-vl-realtime-v1`。

- **Omni Realtime API（WebSocket/AOQ/WebRTC）**  
  多模态流式交互的增强形态，专为音视频同步生成设计。通过 `session.update` 配置 `modalities: ["text", "audio"]` 启用双模态流式输出；服务端逐帧返回 `response.text.delta` 和 `response.audio.chunk`，并支持语义 VAD、平滑输出（`smooth_output`）等高级控制。仅限 `qwen3.8-omni-flash-realtime` 等指定模型。

- **Audio API（RESTful）**  
  音频类模型（ASR、TTS、Audio Generation）支持可选流式。TTS 和 ASR 接口在请求中设置 `stream: true`（注意：此字段名与 Model Experience 的 `enable_streaming` 不同），响应体为 `application/octet-stream` 二进制流（如 PCM 音频流或识别文本流），需按 chunk 边接收边处理。不支持流式的模型（如部分语音翻译）将返回完整 JSON。

- **Qwen 兼容协议（OpenAI/Anthropic/DashScope）**  
  OpenAI 兼容 `/chat/completions` 接口通过 `stream: true` 启用流式；DashScope 原生协议对应 `enable_streaming: true`；Anthropic 兼容 Messages API 则原生支持流式（无需额外参数）。所有协议下，流式响应均为 SSE 格式，结构与 Model Experience 一致，便于 SDK 统一适配。

> ⚠️ 注意：向量模型（embedding/rerank）和部分旧版视觉生成模型**不支持流式输出**，请求中传入流式参数将被忽略或报错。

## 关键参数和配置

| 参数 | 所属协议 | 类型 | 说明 | 是否必需 |
|------|----------|------|------|-----------|
| `enable_streaming` | Model Experience, DashScope 原生 | boolean | 启用 SSE 流式响应 | 否（默认 `false`） |
| `stream` | Realtime API, Audio API, OpenAI 兼容 | boolean | 启用流式（Realtime API 中固定为 `true`） | 是（Realtime）/ 否（Audio/OpenAI） |
| `modalities` | Omni Realtime API | string[] | 指定输出模态，`["text"]` 或 `["text","audio"]` | 是（决定是否输出音频流） |
| `audio.output.format.sample_rate` | Omni Realtime API | integer | 输出音频采样率（8000–48000 Hz），影响流式音频 chunk 质量 | 否（有默认值） |

- **超时设置**：所有流式请求需客户端显式配置长超时（建议 ≥ 300 秒），避免连接被中间代理或 SDK 默认策略中断。
- **错误处理**：流式响应中可能夹杂 `event: error` 事件（SSE）或 `error` 字段（WebSocket），需监听并终止当前流。
- **Token 边界**：文本流中 `text.delta` 为 UTF-8 字符串，**不保证按词/字粒度切分**，应用层需自行累积拼接；音频流为原始 PCM/WAV 帧，需按 `sample_rate`/`channels` 解码。

## 面向开发者：简洁实用提示

- ✅ **首选 SSE 解析库**：Node.js 用 `eventsource-parser`，Python 用 `sseclient-py`，浏览器用原生 `EventSource`，避免手动解析 `data:` 行。
- ✅ **WebSocket 流务必处理重连**：Realtime/Omni Realtime 连接有 300 秒生命周期限制，建议结合 `session_id` 或 `sequence_id` 实现断点续传。
- ✅ **TTS/ASR 流式响应无 JSON 封装**：直接接收二进制数据，勿尝试 `JSON.parse()`；可用 `Uint8Array` 或 `Blob` 处理。
- ❌ **勿混用流式与非流式参数**：如在 Model Experience 中同时传 `enable_streaming=true` 和 `max_tokens=1`（过小），可能导致流提前终止。
- 📌 **调试技巧**：用 `curl -N` 查看原始 SSE 流；WebSocket 场景使用 [AOQ 客户端 SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md) 可自动处理序列号、buffer 和重试。

## 关联主题页

- [model experience](../guides/model-experience.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [audio api references](../api/audio-api-references.md)
- [qwen api reference](../api/qwen-api-reference.md)


