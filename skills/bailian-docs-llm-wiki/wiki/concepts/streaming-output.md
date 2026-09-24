# 流式输出

流式输出（Streaming Output）是指模型推理结果以增量、分块的方式持续返回，而非等待整个响应生成完毕后一次性返回。它通过事件驱动机制（如 Server-Sent Events 或 WebSocket 消息）将文本 token、音频帧、结构化字段等按生成顺序实时推送至客户端，显著降低端到端延迟，提升交互自然度与用户体验。

## 在百炼平台的不同场景中如何使用

流式输出是百炼平台实时性关键能力的底层支撑，在以下场景中被统一支持并差异化实现：

- **Realtime API（语音/多模态实时交互）**：  
  基于 WebSocket 协议，强制启用流式（`stream: true` 固定），支持 `output.text.delta`（逐 token 文本）、`output.audio.delta`（PCM/Opus 音频帧）、`output.video.frame`（视频帧）等细粒度事件。适用于语音助手、会议实时转写、VAD 驱动的语音轮转等低延迟场景。

- **Application Call（智能体/工作流调用）**：  
  通过 `stream: true` 参数启用，支持两种模式：  
  - DashScope 原生协议：可选 `incremental_output: true`（返回 delta）或 `false`（返回全量追加内容）；  
  - Responses（OpenAI 兼容）协议：默认返回 `data: {...}` SSE 格式，兼容标准 OpenAI SDK 的 `stream=True` 行为。  
  工作流应用还可通过 `flow_stream_mode` 控制推送粒度（如 `message_format_plus` 支持节点级流式）。

- **Qwen 系列通用 API（OpenAI/Anthropic/DashScope 协议）**：  
  所有协议均支持 `stream: true` 参数。[OpenAI 兼容接口](openai-compatible-api.md)返回标准 SSE `data:` 块；Anthropic Messages 返回 `content_block_delta` 事件；DashScope 原生接口返回 `output.text.delta` 等结构化事件。注意：`qwen3.8-audio` 等专用模型仅在 DashScope 协议下支持流式音频输出。

- **[test 1](../guides/test-1.md)（基础同步推理服务）**：  
  虽未在文档中明确定义为“流式接口”，但实测 `/v1/chat/completions` 支持 `stream: true` 并返回符合 OpenAI SSE 规范的 `data:` 块，可用于轻量级流式体验，但不支持中断、动态追加等高级控制。

> ⚠️ 注意：`omni realtime api` 中 `qwen-omni-turbo-realtime` 等部分模型系列**禁止覆盖** `temperature`/`top_p` 等参数，但流式能力本身不受影响；`realtime api user guide` 明确声明该接口**不支持非流式模式**（`stream` 必须为 `true`）。

## 关键参数和配置

| 参数 | 类型 | 作用 | 是否必需 | 备注 |
|------|------|------|----------|------|
| `stream` | `boolean` | 启用流式输出开关 | 大多数场景为必填（Realtime API 强制 `true`） | 所有协议通用，设为 `false` 将退化为同步响应 |
| `incremental_output` | `boolean` | （DashScope Application Call）控制流式内容是否为增量 delta | 否 | `true`：返回 `delta` 字段；`false`：返回 `text` 全量追加值 |
| `flow_stream_mode` | `string` | （工作流应用）指定流式推送格式 | 否 | 推荐 `message_format_plus`，支持节点级事件透出 |
| `modalities` | `array` | （Omni Realtime）声明输出模态组合 | 是（Omni Realtime） | 仅支持 `["text"]` 或 `["text","audio"]`，决定是否推送音频流 |

- **事件格式统一约定**：  
  - 文本流：`output.text.delta`（Realtime/Omni）或 `delta.content`（OpenAI SSE）；  
  - 音频流：`output.audio.delta`（base64 编码 PCM/Opus 帧，含 `sample_rate` 和 `format` 元信息）；  
  - 结束标识：`output_finished`（Realtime）、`[DONE]`（OpenAI SSE）、`content_block_stop`（Anthropic）。

- **客户端处理建议**：  
  - 使用 `EventSource`（SSE）或 WebSocket 客户端监听事件，避免阻塞解析；  
  - 对 `delta` 内容做累积拼接（尤其 `incremental_output: false` 时需自行合并）；  
  - 监听 `output_finished` 或 `error` 事件及时终止渲染，防止 stale state。

面向开发者，请始终以实际接口返回的事件结构为准，并参考对应协议的 [AOQ 客户端 SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md) 或 [OpenAI 兼容规范](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md) 进行解析。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [application call](../api/application-call.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [test 1](../guides/test-1.md)


