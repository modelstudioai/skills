# 流式输出

流式输出（Streaming Output）是指模型服务在生成结果过程中，将响应内容分块、实时、渐进式地返回给客户端，而非等待全部结果生成完毕后一次性返回。这种方式显著降低端到端延迟，提升用户体验，尤其适用于长文本生成、实时语音交互、多模态流式处理等对响应速度和交互感要求高的场景。

## 在百炼平台的不同场景中，这个概念如何使用

流式输出在百炼平台中并非单一功能，而是贯穿多个 API 层级的通用能力，具体体现如下：

- **Model Experience 统一调用层**：通过 `/v1/models/{model_id}/invoke` 接口，设置 `stream: true` 即可启用流式响应。适用于所有支持流式的文本、视觉、语音类模型（如 `qwen2-72b-chat`、`qwen2-vl`），返回格式为标准 Server-Sent Events（SSE），每帧含 `data:` 字段及结构化 `delta` 或 `text` 片段。

- **Qwen API（OpenAI/Anthropic/DashScope 协议）**：
  - [OpenAI 兼容接口](openai-compatible-interface.md)（`/chat/completions`、`/responses`）：通过请求参数 `stream=true` 启用，响应为 SSE 流，支持 `delta.content` 增量文本、`delta.tool_calls` 工具调用片段。
  - Anthropic 兼容接口（`/v1/messages`）：同样使用 `stream=true`，返回 `content_block_delta` 事件，支持 `text_delta` 和 `input_json_delta`。
  - DashScope 原生接口（`/text-generation/generation` 等）：需显式传入 `stream=true`，响应体为 JSON Lines（NDJSON）格式，每行一个 `{ "output": { "text": "..." } }` 对象。

- **Realtime API（WebSocket）**：原生基于双向流式通信设计，无需额外开关。服务端在模型推理过程中持续推送 `event: text`、`event: audio`、`event: input_audio` 等事件帧，天然支持毫秒级低延迟反馈，是 ASR/TTS/Audio Chat 等实时场景的默认工作模式。

- **Audio API（非实时音频处理）**：部分模型明确支持流式能力，例如：
  - `Qwen-Audio-ASR` 和 `Fun-ASR-Flash` 支持 HTTP SSE 流式返回中间识别结果（通过 `enable_interim_results=true` 控制）；
  - `Qwen-Audio-TTS` 在支持的 SDK 中可启用流式音频输出（如分块返回 PCM 数据），但 HTTP 接口本身不直接返回二进制流，需配合 `response_format=audio/wav` + 客户端流式解析。

> ⚠️ 注意：向量模型（embedding/rerank）、异步文件转写类接口（如 `Qwen-Audio-ASR-Filetrans`）**不支持流式输出**；`stream` 参数在这些场景下会被忽略或导致错误。

## 关键参数和配置

| 参数 | 所属层级 | 类型 | 说明 |
|------|----------|------|------|
| `stream` | Model Experience / Qwen API / DashScope | boolean | 必填开关。设为 `true` 启用流式响应；`false` 或未传则为同步阻塞模式。 |
| `enable_interim_results` | Realtime API / Audio API（ASR） | boolean | 控制是否推送中间识别结果（如 ASR 的半句话）。默认 `true`，设为 `false` 仅返回最终结果。 |
| `response_format` | Realtime API / Audio API（TTS） | string | 指定流式输出内容类型，常见值：`text`、`json`、`audio/wav`。影响客户端解析方式。 |
| `max_tokens` | 所有支持流式的文本接口 | integer | 仍生效，用于控制总输出长度上限；流式响应会在达到该限制时自动终止。 |

- **HTTP 流式响应头**：所有流式接口均返回 `Content-Type: text/event-stream; charset=utf-8`，客户端需按 SSE 协议解析（如监听 `data:` 行，忽略 `event:`、`id:`、`retry:` 等可选字段）。
- **WebSocket 流式帧**：Realtime API 使用自定义二进制/JSON 帧协议，不依赖 HTTP 头，由 `event` 字段标识数据类型（如 `event: text`）。
- **错误处理**：流式过程中若发生错误（如鉴权失败、模型中断），服务端会推送 `event: error` 帧并关闭连接，客户端应监听并重试。

## 面向开发者，简洁实用

- ✅ **首选统一入口**：新项目建议优先使用 `Model Experience`（`/v1/models/{model_id}/invoke` + `stream=true`），语义一致、SDK 封装完善、跨模态兼容性好。
- ✅ **实时场景必用 WebSocket**：语音识别、对话、翻译等低延迟需求，请直接接入 `Realtime API`，避免 HTTP 流式带来的额外延迟与连接开销。
- ✅ **流式解析要健壮**：不要假设每帧只含一个 token；需累积 `delta.text` 或拼接 `data:` 内容，并正确处理空格、换行、emoji 等边界情况。
- ❌ **勿混用流式与同步逻辑**：流式响应无 `usage` 字段（token 统计在最后一帧 `done` 事件中），也无完整 `message` 对象，切勿按同步响应结构解析。
- 🛠️ **调试技巧**：用 `curl -N` 或浏览器 DevTools 的 Network → EventStream 查看原始流；Python 开发推荐使用 `httpx.AsyncClient` + `aiter_lines()`，Node.js 推荐 `fetch` + `ReadableStream`。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [realtime api directory](../api/realtime-api-directory.md)
- [model experience](../guides/model-experience.md)
- [audio api directory](../api/audio-api-directory.md)


