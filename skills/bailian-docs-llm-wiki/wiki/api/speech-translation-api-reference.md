# speech translation api reference

百炼平台「语音/音视频翻译」（Speech Translation）能力由 Qwen-LiveTranslate 模型族提供，覆盖两条调用链路：一是基于 OpenAI 兼容的 `chat.completions` 接口的**非实时**音视频翻译（`qwen3-livetranslate-flash`），二是基于 WebSocket 协议的**实时**流式翻译（`qwen3.5-livetranslate-flash-realtime`），后者额外提供 DashScope Python / Java SDK 封装。本页汇总两类接口的可用模型、关键参数、调用方式与限制，便于开发者按场景选型。

## 支持的模型与调用链路

| 调用方式 | 模型 | 协议 | 适用场景 |
| --- | --- | --- | --- |
| OpenAI 兼容 Chat Completions | `qwen3-livetranslate-flash`、`qwen3-livetranslate-flash-2025-12-01` | HTTPS（流式 SSE） | 一次性翻译已录制的音频文件或视频文件 |
| 原生 WebSocket（客户端/服务端事件） | `qwen3.5-livetranslate-flash-realtime`、`qwen3-livetranslate-flash-realtime`（旧版） | WebSocket | 麦克风/摄像头实时流转译，需毫秒级响应 |
| DashScope Python SDK（`OmniRealtimeConversation`） | 同上 | 封装上述 WebSocket | Python 客户端、桌面 / 服务端集成 |
| DashScope Java SDK（`OmniRealtimeConversation`） | 同上 | 封装上述 WebSocket | JVM 平台集成 |

非实时接口的详细字段定义、地域 base_url 与示例代码见 [音视频翻译-通义千问 API 参考](../../raw/model-api-reference/speech-translation-api-reference/qwen3-livetranslate-flash-api.md)；实时接口的协议事件契约见 [客户端事件](../../raw/model-api-reference/speech-translation-api-reference/live-translator-api/live-translator-client-events.md) 与 [服务端事件](../../raw/model-api-reference/speech-translation-api-reference/live-translator-api/live-translator-server-events.md)。

## 地域与接入端点

接入端点按地域分两套，API Key 不通用：

- **北京（华北 2）**
  - OpenAI 兼容 base_url：`https://dashscope.aliyuncs.com/compatible-mode/v1`
  - 实时 WebSocket：`wss://dashscope.aliyuncs.com/api-ws/v1/realtime`
- **新加坡**
  - OpenAI 兼容 base_url：`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
  - 实时 WebSocket（新版）：`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime`

> **注意**：新加坡地域的旧版 WebSocket 域名 `wss://dashscope-intl.aliyuncs.com` 即将下线，请尽快迁移到带 `WorkspaceId` 的新版域名（详见 [实时音视频翻译（Qwen-LiveTranslate）Python SDK-API参考](../../raw/model-api-reference/speech-translation-api-reference/live-translator-api/qwen-livetranslate-python-sdk.md) 与 [Java SDK-API参考](../../raw/model-api-reference/speech-translation-api-reference/live-translator-api/qwen-livetranslate-java-sdk.md) 的「前提条件」章节）。

> **注意**：本系列模型**不支持** DashScope 原生 `/services/aigc/multimodal-generation/generation` 协议，非实时调用必须走 OpenAI 兼容路径。

## 非实时 API（OpenAI 兼容）

### 请求结构

POST `${base_url}/chat/completions`。关键字段：

- **`model`**（必填）：`qwen3-livetranslate-flash` 或带日期快照的版本号。
- **`messages`**（必填）：仅允许一个 `user` 消息，`content` 数组里放：
  - `type: "input_audio"` + `input_audio.data`（URL 或 Base64 Data URL）+ `input_audio.format`（如 `mp3`、`wav`）。
  - 或 `type: "video_url"` + `video_url.url`（公网 URL 或 Base64 Data URL）。
- **`stream`**（必填）：必须为 `true`，模型只支持[流式输出](../concepts/streaming.md)。
- **`stream_options.include_usage`**：建议设为 `true`，便于在最后一个 chunk 拿到 Token 用量。
- **`modalities`**：`["text"]` 仅输出文本，或 `["text","audio"]` 同时输出语音。
- **`audio`**：当 `modalities` 含 `audio` 时必填，设置 `voice`（音色）与 `format`（仅支持 `wav`）。
- **`translation_options`**（必填）：
  - `source_lang`（可选，留空则自动检测）。
  - `target_lang`（必填）。
  - 在 Python SDK 中需放入 `extra_body={"translation_options": {...}}`；Node.js / 直接 HTTP 调用作为顶层参数。

非 OpenAI 标准的 `top_k`、`repetition_penalty`、`translation_options` 在 Python SDK 都必须放入 `extra_body`，其余 SDK 直接传顶层。为保证翻译稳定性，**不建议**修改 `temperature`、`top_p`、`top_k`、`presence_penalty`、`repetition_penalty` 的默认值。

### 流式响应 chunk

返回 `chat.completion.chunk` 对象，分三类：

- **文本 chunk**：`choices[0].delta.content` 为增量文本。
- **音频 chunk**：`choices[0].delta.audio.data` 为增量 Base64 音频；`audio.id` 标识本次输出音频。
- **用量 chunk**：仅当 `include_usage=true` 时，最后一个 chunk 的 `choices` 为空数组，`usage` 字段提供 `prompt_tokens` / `completion_tokens` / `total_tokens` 以及音频与文本 token 的细分。

字段级定义参见 [音视频翻译-通义千问 API 参考](../../raw/model-api-reference/speech-translation-api-reference/qwen3-livetranslate-flash-api.md) 的「chat响应chunk对象」小节。

## 实时 API（WebSocket）

实时模型通过 WebSocket 收发 JSON 事件，会话生命周期为：

```
[connect] --> session.created
client --> session.update            <-- server.session.updated
client --> input_audio_buffer.append (循环)
client --> input_image_buffer.append (可选，循环)
                                     <-- response.created
                                     <-- response.audio.delta / response.text.text / response.audio_transcript.text (流式)
                                     <-- response.audio.done / response.text.done / response.audio_transcript.done
                                     <-- conversation.item.input_audio_transcription.text / .completed (可选)
                                     <-- response.done
client --> session.finish            <-- session.finished
[close]
```

### 客户端事件

- **`session.update`**：连接建立后第一个事件，提交完整会话配置；不合法时服务端返回 `error`。`session` 对象主要字段：
  - `modalities`：`["text"]` 或 `["text","audio"]`（默认）。
  - `voice`：系统音色（如 `Tina`、`Cherry`、`Ethan`）。`qwen3.5-livetranslate-flash-realtime` 默认 `Tina`；`qwen3-livetranslate-flash-realtime` 默认 `Cherry`。
  - `enable_voice_clone` + `voice_clone_options.frequency`：开启声音复刻，频率可选 `never`（使用预先复刻的音色 ID）、`once`（会话开始复刻一次，适合单人演讲）、`always`（每次实时复刻，适合多人对话）。
  - `sample_rate`：输入采样率，可选 `8000` / `16000`（默认）。
  - `input_audio_format`：`pcm`（默认）或 `opus`；`output_audio_format` 仅支持 `pcm`。
  - `input_audio_transcription.model = "qwen3-asr-flash-realtime"`：开启原文 ASR 回流。
  - `translation.language`：目标语种代码（默认 `en`）。
  - `translation.corpus.phrases`：源→目标的热词映射，用于稳住专业术语翻译。
- **`input_audio_buffer.append`**：`audio` 字段为 Base64 编码音频片段，服务端基于此缓冲做 VAD 与翻译触发。
- **`input_image_buffer.append`**：`image` 字段为 Base64 JPG/JPEG。约束：分辨率建议 480p–720p（不超过 1080p）、Base64 前单图 ≤ 500 KB、频率 ≤ 2 张/秒、且必须在已发过至少一次 `input_audio_buffer.append` 之后再发图像。
- **`session.finish`**：通知服务端结束会话；服务端完成残留语音的识别后返回 `session.finished`，客户端再主动断开。

事件载荷示例与逐字段说明见 [客户端事件](../../raw/model-api-reference/speech-translation-api-reference/live-translator-api/live-translator-client-events.md)。

### 服务端事件

- **`error`**：参数校验失败或运行时错误，`error.type` / `code` / `message` / `param` 指明出错字段。
- **`session.created`** / **`session.updated`**：连接初始默认配置 / 收到 `session.update` 后的最新会话快照。注意 `session.created` 给出的格式字段是 `pcm16` / `pcm24`，而 `session.updated` 改回 `pcm`。
- **`session.finished`**：会话结束（仅在客户端发送 `session.finish` 后触发）。
- **`response.created`** / **`response.done`**：模型一次响应的起止；`response.done` 携带完整 `output[]`（除原始音频外）以及 `usage`（细分文本/音频 token）。
- **`response.text.text`** / **`response.text.done`**：仅文本模态下的增量与最终文本。`response.text.text` 同时给出 `text`（已确认）和 `stash`（临时拼接片段），最终以 `response.text.done` 的 `text` 字段为准。
- **`response.audio.delta`** / **`response.audio.done`**：含音频模态时的 Base64 音频增量与完结信号；`done` 不会再带音频数据。
- **`response.audio_transcript.text`** / **`response.audio_transcript.done`**：音频模态下同步推送的翻译文本（用于字幕），与 `text` / `stash` 模式一致。
- **`conversation.item.input_audio_transcription.text`** / **`.completed`**：仅当配置了 `input_audio_transcription.model` 时返回源语言 ASR 结果，`.completed.transcript` 为最终原文。

> **注意**：服务端事件中的 `session.created` 把音频格式记为 `pcm16` / `pcm24`，而客户端通过 `session.update` 传入及 `session.updated` 返回的字段名是 `pcm`。两者描述的是同一编码族（PCM 16-bit），命名差异源于事件版本不同，集成时不要据此判断格式变化。事件契约请以 [服务端事件](../../raw/model-api-reference/speech-translation-api-reference/live-translator-api/live-translator-server-events.md) 为准。

## DashScope SDK 封装

SDK 把上述 WebSocket 收发包装成方法 + 回调，避免手写事件路由。两套 SDK 形状对称：

| 关注点 | Python | Java |
| --- | --- | --- |
| 最低版本 | DashScope SDK ≥ `1.25.6` | DashScope SDK ≥ `2.22.5` |
| 连接配置 | `OmniRealtimeConversation(model, url, callback)` | `OmniRealtimeParam.builder().model().url().apikey().build()` |
| 会话配置 | `conversation.update_session(output_modalities, voice, input_audio_transcription_model, translation_params)` | `OmniRealtimeConfig.builder().modalities().voice().inputAudioFormat().outputAudioFormat().InputAudioTranscription().translationConfig().build()` + `conversation.updateSession(config)` |
| 翻译参数 | `TranslationParams(language, corpus=Corpus(phrases={...}))` | `OmniRealtimeTranslationParam.builder().language().corpus(...).build()` |
| 发送音频 | `append_audio(audio_b64)` | `appendAudio(audioBase64)` |
| 结束会话 | `end_session(timeout=20)` → 等待 `session.finished` → `close()` | `endSession()` → `close(code, reason)` |
| 工具方法 | `get_session_id()`、`get_last_response_id()` | `getSessionId()`、`getResponseId()`、`getFirstTextDelay()`、`getFirstAudioDelay()` |
| 回调基类 | `OmniRealtimeCallback`：`on_open` / `on_event(response: dict)` / `on_close(code, msg)` | `OmniRealtimeCallback`：`onOpen` / `onEvent(JsonObject message)` / `onClose(int code, String reason)` |

回调内通过 `response['type']`（Python）或 `message.get("type").getAsString()`（Java）路由到对应服务端事件。完整的麦克风采集 → 翻译播放示例可直接复用文档中的 `pyaudio` / `javax.sound.sampled` 示例代码（详见 [Python SDK-API参考](../../raw/model-api-reference/speech-translation-api-reference/live-translator-api/qwen-livetranslate-python-sdk.md) 与 [Java SDK-API参考](../../raw/model-api-reference/speech-translation-api-reference/live-translator-api/qwen-livetranslate-java-sdk.md)）。

> **注意**：Java SDK 的方法名 `InputAudioTranscription` 首字母大写，与字段语义不一致但属当前版本的真实签名；Python SDK 对应字段为 `input_audio_transcription_model`。集成时按各自 SDK 的精确拼写传入。

## 关键参数速查

- **音色**：实时模型默认 `Tina`（3.5）/ `Cherry`（3）；启用声音复刻时 `voice` 取值依 `frequency` 变化（`once`/`always` 必须为 `default`，`never` 必须为预先复刻的音色 ID），否则服务端返回错误。
- **语种**：源语种 `source_lang` / `language` 可留空让模型自动识别；目标语种在非实时接口为必填，在实时接口默认 `en`。
- **热词**：`translation_options` 或 `translation.corpus.phrases` 的 key 为源语言原文，value 为期望的目标语言翻译，对专有名词、品牌词稳定性提升明显。
- **图像帧**：仅实时 API 支持；JPG/JPEG、单图 ≤ 500 KB（Base64 前）、≤ 2 fps、必须在已开始送音频之后才能送图。
- **多模态输出**：`["text"]` 时只走 `response.text.*` 事件；`["text","audio"]` 时同时走 `response.audio.*` 与 `response.audio_transcript.*` 事件。
- **Token 计量**：非实时接口在最后一个 chunk 的 `usage` 中拆分 `text_tokens` / `audio_tokens`；实时接口在 `response.done.usage` 中给出 `input_tokens_details` / `output_tokens_details`。

## 限制与注意事项

- [流式输出](../concepts/streaming.md)是硬性要求，非实时 API 设置 `stream=false` 会被拒绝。
- 实时 API 必须先 `session.update` 再 `input_audio_buffer.append`；图像帧必须在首个音频帧之后再发。
- 客户端必须监听 `session.finished` 后再主动断开 WebSocket，否则可能丢失尾音段的翻译结果。
- 不同地域使用不同的 API Key 与 base URL；新加坡地域请按上文「地域与接入端点」迁移到新版域名。
- `qwen3-livetranslate-flash-realtime` 已标记为旧版模型，新接入请使用 `qwen3.5-livetranslate-flash-realtime`。

## 来源文档

- [音视频翻译-通义千问 API 参考](../../raw/model-api-reference/speech-translation-api-reference/qwen3-livetranslate-flash-api.md)
- [客户端事件](../../raw/model-api-reference/speech-translation-api-reference/live-translator-api/live-translator-client-events.md)
- [服务端事件](../../raw/model-api-reference/speech-translation-api-reference/live-translator-api/live-translator-server-events.md)
- [实时音视频翻译（Qwen-LiveTranslate）Python SDK-API参考](../../raw/model-api-reference/speech-translation-api-reference/live-translator-api/qwen-livetranslate-python-sdk.md)
- [实时音视频翻译（Qwen-LiveTranslate）Java SDK-API参考](../../raw/model-api-reference/speech-translation-api-reference/live-translator-api/qwen-livetranslate-java-sdk.md)



