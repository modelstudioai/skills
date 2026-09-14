# omni realtime api

omni realtime api 是百炼平台提供的低延迟、流式多模态交互接口，支持语音输入/输出、文本生成与实时音视频流处理的端到端协同。该 API 采用事件驱动架构，通过客户端与服务端双向事件流（如 `input_audio_buffer`、`response_text_delta`、`audio_chunk`）实现毫秒级响应。适用于智能座舱、实时会议助手、无障碍交互等对时延敏感的场景。

## 支持的模型与功能

- 当前仅支持 `qwen-omni-realtime` 模型（v1.0+），不兼容旧版 `qwen-omni` 非实时推理模型。
- 核心能力包括：实时语音识别（ASR）、流式文本生成（LLM）、语音合成（TTS）及可选的声音复刻（Voice Cloning）[实时多模态](../../raw/model-api-reference/omni-realtime-api.md)。  
- 支持全双工交互：客户端可在服务端响应过程中持续推送音频流，无需等待上一轮结束 [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 固定为 `"qwen-omni-realtime"`，其他值将返回 400 错误 |
| `input_audio_format` | string | 否 | 默认 `"pcm16"`, 支持 `"pcm16"` / `"opus"`；需与实际音频编码一致 |
| `output_audio_format` | string | 否 | 默认 `"pcm16"`，若启用声音复刻则必须设为 `"pcm16"` |
| `voice_clone` | object | 否 | 启用声音复刻时必填，结构见 [qwen-omni-voice-cloning](../../raw/model-api-reference/omni-realtime-api.md) |

> **注意**：原始文档中部分 SDK 示例（如 Java SDK）仍引用已废弃的 `qwen-omni-stream` 模型标识，实际调用必须使用 `qwen-omni-realtime`，否则触发模型不可用错误。

## 使用方式

1. 建立 WebSocket 连接至 `wss://dashscope.aliyuncs.com/realtime/v1/omni`（鉴权通过 `Authorization: Bearer <api_key>`）；
2. 发送 `session.update` 事件初始化会话（含 `model`、`voice_clone` 等配置）；
3. 通过 `input_audio_buffer` 事件持续上传音频帧（建议单帧 ≤ 200ms）；
4. 监听 `response_text_delta`（文本流）、`audio_chunk`（合成音频）等服务端事件；
5. 客户端可随时发送 `input_text` 或 `cancel_response` 控制交互流。

参考实现请查阅 [Python SDK](../../raw/model-api-reference/omni-realtime-api.md) 和 [Java SDK](../../raw/model-api-reference/omni-realtime-api.md) 文档。

## 限制和注意事项

- 单次会话最长 300 秒，超时后连接自动关闭；
- 音频输入采样率必须为 16kHz（`pcm16`）或 48kHz（`opus`），不支持自动重采样；
- 声音复刻需提前上传参考音频并获取 `voice_id`，且仅支持中文普通话参考音；
- 服务端事件类型与语义以 [服务端事件](../../raw/model-api-reference/omni-realtime-api.md) 文档为准，客户端须健壮处理未知事件类型；
- 不支持 HTTP 轮询方式，仅限 WebSocket 协议。

## 来源文档

- [实时多模态](../../raw/model-api-reference/omni-realtime-api.md)


