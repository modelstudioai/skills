# speech synthesis api reference

本文档提供阿里云百炼语音合成（TTS）服务的完整 API 参考，涵盖非实时、实时流式合成及音色定制接口。开发者可根据延迟要求与交互模式选择对应的模型、通信协议与 SDK，快速集成高质量语音生成能力。

## 支持的模型/功能
平台提供多系列语音合成模型，覆盖不同场景需求：
- **CosyVoice 系列**：支持实时双向流式（WebSocket）与 HTTP 非流式调用。内置丰富系统音色，支持 [[SSML标记语言]]、Instruct 指令控制、字级时间戳及多语种合成。可通过 [[声音复刻]] 与 [[声音设计]] 定制专属音色。
- **Qwen-TTS 系列**：包含非实时版与 Realtime 实时版。实时版支持 `server_commit`（服务端智能分段）与 `commit`（客户端手动触发）双模式，内置多语种自动识别，支持指令微调（`qwen3-tts-instruct-flash`）。
- **Sambert 系列**：传统高性能发音人模型，支持单向[[streaming-output|流式输出]]与字/音素级时间戳，适用于对稳定性要求高的播报场景。
- **MiniMax 系列**：第三方模型接入，提供情感控制、多音字注音字典及 SSE [[streaming-output|流式输出]]能力。

## 关键参数
调用合成接口时，需合理配置以下核心参数：
| 参数名 | 类型/必填 | 说明 |
|:---|:---|:---|
| `model` | String/是 | 模型标识，如 `cosyvoice-v3-flash`、`qwen3-tts-flash-realtime`、`sambert-zhichu-v1`。必须与音色绑定。 |
| `voice` | String/是 | 音色 ID。系统音色需匹配对应模型范围；定制音色需传入克隆/设计返回的 `voice_id`。 |
| `text` / `input` | String/是 | 待合成文本。HTTP 非流式需一次性提交完整内容；WebSocket 流式支持分片追加。长度通常 ≤20,000 字符。 |
| `format` | String/否 | 音频编码格式，支持 `pcm`、`wav`、`mp3`（默认）、`opus`。部分旧版模型不支持 `opus`。 |
| `sample_rate` | Integer/否 | 采样率（Hz），常见可选 8000、16000、22050、24000、48000。 |
| 音频控制 | Float/Int/否 | `volume` (0-100)、`rate` (0.5-2.0)、`pitch` (0.5-2.0)、`speech_rate`。用于调节音量、语速与音调。 |
| 模式/开关 | Boolean/否 | `enable_ssml`（开启 SSML 解析）、`word_timestamp_enabled`（字级时间戳）、`mode`（Qwen 实时版交互模式）。 |

## 使用方式
- **HTTP API 调用**：适用于非流式或 SSE 服务端事件流场景。请求地址为 `/api/v1/services/audio/tts/SpeechSynthesizer` 或音色定制端点。通过设置请求头 `X-DashScope-SSE: enable` 可开启流式响应。详细请求体结构请参见 [非实时语音合成（Qwen-TTS）API参考](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-api.md)。
- **WebSocket 协议**：适用于低延迟实时交互场景。建立 `wss://` 长连接后，按标准事件协议交互。CosyVoice 使用 `run-task` → `continue-task`（流式文本） → 接收 `binary` 音频帧 → `finish-task` 流程；Qwen Realtime 采用 `session.update` → `input_text_buffer.append/commit` → `response.audio.delta` 流程。
- **SDK 集成**：官方提供 Python、Java、Android、iOS 多端 SDK。核心封装类（如 `SpeechSynthesizer` 或 `QwenTtsRealtime`）提供同步阻塞 `call()` 与异步回调 `streaming_call()`。SDK 已自动处理鉴权、WebSocket 握手、连接复用及音频流拼接，推荐业务优先使用 SDK 接入。完整调用示例请参见 [实时语音合成CosyVoice Python SDK](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-python-sdk.md)。
- **音色定制流程**：调用定制接口传入提示词或参考音频，获取 `voice_id` 后，在合成请求的 `voice` 参数中传入该 ID 即可生效。接口详情参见 [声音设计API参考](../../raw/model-api-reference/speech-synthesis-api-reference/voice-design-api-references.md)。

## 限制和注意事项
- **地域与鉴权隔离**：北京地域与（国际）新加坡地域使用不同的 API 端点与 API Key，互不通用。初始化 SDK 或构造 HTTP 请求前需显式设置对应的 `base_url`，否则将触发鉴权失败。
- **流式模式差异**：
  > **注意**：Sambert 模型仅支持北京地域，且 **不支持** `duplex` 双向流式输入（`streaming` 固定为 `out`）。所有待合成文本必须在 `run-task` 事件中一次性完整发送，不支持分片续传。
- **SDK 接口演进**：
  > **注意**：最新 Python SDK 已将部分历史独立接口统一收敛至 `MultiModalConversation` 或 `dashscope.audio` 命名空间下。旧版 `SpeechSynthesizer.call()` 直接调用方式可能在新版本中被标记为 Deprecated，请以最新官方文档的参数签名为准。
- **音色与模型强绑定**：通过 [[声音复刻]] 或 [[声音设计]] 生成的专属音色必须与 `target_model` 保持一致。若在合成请求中使用不匹配的 `model`，服务端将拒绝请求或返回异常音频。
- **资源释放与完整性**：WebSocket 双向流式调用结束后，必须显式发送结束指令（如 `finish-task`、`session.finish` 或调用 SDK 的 `streaming_complete()`），否则服务端可能无法输出尾部文本的音频数据。建议复用 WebSocket 连接处理多任务，避免频繁建连增加延迟。

## 来源文档

- [非实时语音合成（Qwen-TTS）API参考](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-api.md)
- [声音设计API参考](../../raw/model-api-reference/speech-synthesis-api-reference/voice-design-api-references.md)
- [CosyVoice WebSocket API参考](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-websocket-api.md)
- [CosyVoice服务端事件](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-server-events.md)
- [CosyVoice客户端事件](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-client-events.md)
- [实时语音合成CosyVoice Java SDK](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-java-sdk.md)
- [语音合成CosyVoice iOS SDK](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-ios-sdk.md)
- [实时语音合成CosyVoice Python SDK](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-python-sdk.md)
- [语音合成CosyVoice Android SDK](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-android-sdk.md)
- [CosyVoice音色列表](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-voice-list.md)
- [客户端事件](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-realtime-api-reference/qwen-tts-realtime-client-events.md)
- [Python SDK](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-realtime-api-reference/qwen-tts-realtime-python-sdk.md)
- [Qwen-TTS-Realtime WebSocket API 参考](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-realtime-api-reference/interactive-process-of-qwen-tts-realtime-synthesis.md)
- [Java SDK](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-realtime-api-reference/qwen-tts-realtime-java-sdk.md)
- [服务端事件](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-realtime-api-reference/qwen-tts-realtime-server-events.md)
- [Sambert WebSocket API 参考](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-websocket-api.md)
- [Sambert客户端事件](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-client-events.md)
- [Sambert服务端事件](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-server-events.md)
- [语音合成Sambert Python SDK](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-python-sdk.md)
- [语音合成Sambert Java SDK](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-java-sdk.md)
- [非实时语音合成CosyVoice HTTP API参考](../../raw/model-api-reference/speech-synthesis-api-reference/non-realtime-cosyvoice-api/cosyvoice-tts-http-api.md)
- [语音合成Sambert Android SDK](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-android-sdk.md)
- [语音合成Sambert iOS SDK](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-ios-sdk.md)
- [非实时语音合成CosyVoice Java SDK参考](../../raw/model-api-reference/speech-synthesis-api-reference/non-realtime-cosyvoice-api/cosyvoice-tts-java-sdk.md)
- [非实时语音合成CosyVoice Python SDK参考](../../raw/model-api-reference/speech-synthesis-api-reference/non-realtime-cosyvoice-api/cosyvoice-tts-python-sdk.md)
- [声音复刻Python SDK参考](../../raw/model-api-reference/speech-synthesis-api-reference/sound-reengraving/voice-clone-design-python-sdk.md)
- [声音复刻Java SDK参考](../../raw/model-api-reference/speech-synthesis-api-reference/sound-reengraving/voice-clone-design-java-sdk.md)
- [声音复刻HTTP API参考](../../raw/model-api-reference/speech-synthesis-api-reference/sound-reengraving/voice-clone-design-http-api.md)
- [MiniMax同步语音合成API参考](../../raw/model-api-reference/speech-synthesis-api-reference/minimax-speech-synthesis/minimax-synchronous-speech-synthesis-api.md)

