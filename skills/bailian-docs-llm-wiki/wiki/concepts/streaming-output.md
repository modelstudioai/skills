# 流式输出

流式输出（Streaming Output）是指模型服务在生成结果过程中，将响应内容分块、实时、渐进式地返回给客户端，而非等待全部结果生成完毕后一次性返回。这种方式显著降低端到端延迟，提升用户感知的响应速度与交互自然度，是构建实时对话、语音合成、长文本生成等体验的关键能力。

## 在百炼平台的不同场景中，这个概念如何使用

流式输出在百炼平台中按调用协议和业务场景分为两类实现方式，适用范围明确，不可混用：

- **HTTP 流式（`stream=true`）**：适用于 `model experience` 和 `get started with models` 等 RESTful 接口。启用后，API 返回 `Content-Type: text/event-stream` 的 SSE（Server-Sent Events）响应，每生成一个 token（文本）或部分结构化片段（如[函数调用](function-calling.md)参数），即推送一条 `data: {...}` 事件。适用于 Web 前端、CLI 工具等需低门槛接入流式能力的场景。当前仅支持**文本生成类模型**（如 `qwen-max`、`qwen2.5-7b-chat`）及**部分语音模型**（ASR/TTS，需查阅具体模型文档确认支持状态）；视觉、向量、视频生成等模态不支持。

- **WebSocket 流式（Realtime API）**：专为超低延迟、双向实时交互设计，是 `realtime api directory` 的唯一通信模式。所有 Realtime 接口（如 `asr`、`tts`、`omni`）**强制启用流式**（`stream` 参数必须为 `true`），基于 WebSocket 协议传输二进制音频帧、文本增量（`output.text.delta`）、状态事件（`session.ended`）等细粒度消息。适用于智能座舱、实时翻译、多模态对话机器人等对端到端延迟敏感（毫秒级）的生产级应用。

> ⚠️ 注意：两种流式机制互不兼容——HTTP 流式无法传输原始音频流，WebSocket 流式不支持 HTTP 轮询或 SSE 格式。请根据延迟要求、数据类型（纯文本 vs 音频/图像帧）和客户端环境（浏览器 SSE 支持 vs 移动端 WebSocket 封装）选择对应路径。

## 关键参数和配置

| 参数名 | 所属协议 | 类型 | 必填 | 说明 |
|--------|----------|------|------|------|
| `stream` | 全部 HTTP 接口（`model experience` / `get started` / `Qwen API`） | boolean | 否（默认 `false`） | 启用流式响应。设为 `true` 后，响应头为 `Content-Type: text/event-stream`，响应体为 SSE 格式。仅对支持流式的模型生效。 |
| `stream` | Realtime API（WebSocket） | boolean | 是（必须为 `true`） | Realtime 接口强制流式，该参数用于会话初始化时显式声明，不可省略或设为 `false`。 |
| `response_format` | Realtime API | string | 否（默认 `"json"`） | 控制输出格式：`"json"`（结构化事件，含 `type`/`delta`/`final` 字段）或 `"binary"`（原始 PCM 音频流，仅 TTS/LiveTranslate 支持）。 |
| `output_config.effort`（Anthropic） / `reasoning.effort`（Responses） | Qwen API（OpenAI/Anthropic 兼容） | string | 否 | 影响流式输出节奏：高推理强度（如 `"high"`）可能导致首 token 延迟增加，但后续 token 更连贯；低强度（如 `"none"`）则优先降低首 token 延迟。 |

- **HTTP 流式响应解析要点**：  
  - 每行以 `data:` 开头，JSON 内容需手动去除前缀并 `JSON.parse()`；  
  - 完整响应以 `data: [DONE]` 结束；  
  - 错误仍通过 HTTP 状态码（如 `400`）返回，不走 `data:` 流。

- **Realtime 流式连接要点**：  
  - 必须先发送 `session.update` 消息完成鉴权与参数协商；  
  - 文本流事件为 `output.text.delta`（增量）和 `output.text.final`（终稿）；  
  - 音频流事件为 `output.audio.chunk`（二进制 PCM 数据块），需客户端拼接播放。

## 面向开发者，简洁实用

- ✅ **快速启用 HTTP 流式**：在请求 body 中添加 `"stream": true`，用 `curl -N` 或前端 `EventSource` 直接消费；检查模型文档确认支持状态（如 `qwen2.5-7b-chat` 支持，`qwen-vl-plus` 不支持）。
- ✅ **Realtime 必须用 WebSocket**：不要尝试用 HTTP 请求 Realtime 接口；使用官方 AOQ SDK 或标准 WebSocket 库，严格遵循 [Realtime API 概述](../../raw/model-api-reference/realtime-api-directory/realtime-api-overview.md) 的消息协议。
- ❌ **避免常见错误**：  
  - 对向量模型（embedding/rerank）传 `stream=true` → 无效且可能报错；  
  - 在 Realtime 连接中发送 `stream=false` → 连接被拒绝；  
  - 解析 HTTP 流式响应时未处理 `data:` 前缀或 `[DONE]` → JSON 解析失败。
- 🛠️ **调试建议**：  
  - HTTP 流式：用 `curl -v -N -d '{"stream":true,...}' <url>` 查看原始响应流；  
  - Realtime：使用 `wscat -c "wss://..."` 手动发送 `session.update` 并观察事件流；  
  - 所有流式调用均需设置合理超时（HTTP 流式建议 120s+，Realtime 单连接上限 30 分钟）。

## 关联主题页

- [model experience](../guides/model-experience.md)
- [realtime api directory](../api/realtime-api-directory.md)
- [get started with models](../guides/get-started-with-models.md)
- [qwen api reference](../api/qwen-api-reference.md)


