# audio api references

百炼平台围绕语音合成（TTS）、语音识别（ASR）和实时音视频翻译三大能力，提供一套 REST / WebSocket 接口以及多语言 SDK（Python、Java、Android、iOS）。所有接口共享同一套 DashScope 鉴权体系（`Authorization: Bearer <API_KEY>`），并按华北2（北京）与新加坡两个地域分别提供端点。

## 一、通用约定

### 1.1 鉴权

所有请求的请求头必须包含：

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| Authorization | string | `Bearer <your_api_key>` |
| Content-Type | string | `application/json`（WebSocket 接口除外） |

### 1.2 地域端点

| 地域 | HTTP / HTTPS | WebSocket |
| --- | --- | --- |
| 华北2（北京） | `https://dashscope.aliyuncs.com/...` | `wss://dashscope.aliyuncs.com/api-ws/v1/realtime` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/...` | `wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime` |

> **注意**：新加坡地域的旧版域名 `dashscope-intl.aliyuncs.com` 即将下线，请迁移到基于 `{WorkspaceId}` 的新版域名。两个地域的 API Key 互不相同，切换地域时需同步更换。

## 二、语音合成（CosyVoice / Qwen-TTS）

### 2.1 实时语音合成（WebSocket 长连接）

实时合成采用 WebSocket 双向流协议，客户端通过三类事件与服务端交互，详见 [CosyVoice客户端事件](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-client-events.md)：

1. **run-task**：建立连接后发送，声明 `model`、`voice`、`format`、`sample_rate`、`volume`、`rate`、`pitch` 等参数；`function` 固定为 `SpeechSynthesizer`。
2. **continue-task**：携带待合成文本（支持 SSML / 普通文本）。
3. **finish-task**：通知服务端结束本次合成。

可用模型：`cosyvoice-v3.5-plus`、`cosyvoice-v3.5-flash`、`cosyvoice-v3-plus`、`cosyvoice-v3-flash`、`cosyvoice-v2`、`cosyvoice-v1`。音频格式支持 `pcm` / `wav` / `mp3` / `opus`（`cosyvoice-v1` 不支持 opus）；采样率可选 8000、16000、22050（默认）、24000、44100、48000 Hz。

官方提供四种语言的 SDK 封装：

- Python：[实时语音合成CosyVoice Python SDK](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-python-sdk.md)
- Java：[实时语音合成CosyVoice Java SDK](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-java-sdk.md)
- Android：[语音合成CosyVoice Android SDK](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-android-sdk.md)
- iOS：[语音合成CosyVoice iOS SDK](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-ios-sdk.md)

### 2.2 非实时语音合成（HTTP）

适合一次性长文本或离线批处理场景，接口为单次 HTTP POST，可选开启 SSE 流式返回。参见 [非实时语音合成CosyVoice HTTP API参考](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/non-realtime-cosyvoice-api/cosyvoice-tts-http-api.md)：

- 端点：`POST /api/v1/services/audio/tts/SpeechSynthesizer`
- 开启流式：请求头加 `X-DashScope-SSE: enable`
- `input.text` 支持 SSML 与 LaTeX 公式转语音；`voice` 可使用系统音色或自定义（复刻 / 设计）音色。

> **注意**：非实时 CosyVoice 合成**目前仅在北京地域可用**，新加坡地域暂不支持。

同样提供 [Python](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/non-realtime-cosyvoice-api/cosyvoice-tts-python-sdk.md) 与 [Java](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/non-realtime-cosyvoice-api/cosyvoice-tts-java-sdk.md) SDK。

### 2.3 声音设计（Voice Design）

通过文本描述生成全新音色，接口为 `POST /api/v1/services/audio/tts/customization`，支持两个模型：

| model | 系列 | `input.action` | 描述长度 | 预览文本语种 |
| --- | --- | --- | --- | --- |
| `voice-enrollment` | CosyVoice | `create_voice` | ≤500 字符 | 中、英 |
| `qwen-voice-design` | Qwen | `create` | ≤2048 字符 | 中/英/德/意/葡/西/日/韩/法/俄 |

详见 [声音设计API参考](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/voice-design-api-references.md)。创建时需要指定 `target_model`（后续合成必须使用同一模型），并可返回一段预览音频用于校验音色效果。除创建外，接口还支持 `list_voices` / `query_voice` / `delete_voice` 等生命周期操作。

### 2.4 声音复刻（Voice Clone）

使用一段参考音频克隆音色。通过 DashScope Java SDK 的 `VoiceEnrollmentService` 类管理，提供 `createVoice` / `listVoice` / `queryVoice` / `updateVoice` / `deleteVoice` 方法。详见 [声音复刻Java SDK参考](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/sound-reengraving/voice-clone-design-java-sdk.md)。

`createVoice` 需要传入：
- `targetModel`：后续合成使用的模型名（必须一致）；
- `prefix`：音色名称前缀（字母数字，≤10 字符）；
- `url`：公网可访问的参考音频 URL。

## 三、语音识别（ASR）

### 3.1 Qwen-ASR（千问录音文件识别）

Qwen-ASR 提供两种接入方式，参见 [录音文件识别（Qwen-ASR）API参考](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference/qwen-asr-api-reference.md)：

| 模型 | 接入方式 |
| --- | --- |
| 千问3-ASR-Flash-Filetrans | 仅 DashScope 异步调用 |
| 千问3-ASR-Flash | OpenAI 兼容 或 DashScope 同步调用 |

- **OpenAI 兼容**：`POST /compatible-mode/v1/chat/completions`，`messages[].content` 通过 `input_audio` 传入音频 URL，支持 `asr_options.enable_itn` 等选项。
- **DashScope 异步**：采用"提交任务 → 轮询 `task_id`"的两步流程，适合长音频。

> **注意**：美国地域不支持 OpenAI 兼容模式。

### 3.2 Fun-ASR（录音文件识别）

Fun-ASR 系列面向更通用场景，提供完整的多语言 SDK，详见 [Fun-ASR录音文件识别HTTP API参考](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/fun-asr-recorded-speech-recognition-http-api.md)。

- 端点：`POST /api/v1/services/audio/asr/transcription`（提交）/ `GET /api/v1/tasks/{task_id}`（查询）
- 请求头必须带 `X-DashScope-Async: enable`
- 可选模型：`fun-asr`、`fun-asr-2025-11-07`、`fun-asr-2025-08-25`、`fun-asr-mtl`、`fun-asr-mtl-2025-08-25`
- `input.file_urls` 支持 HTTP(S) 与 `oss://` 前缀的临时 URL（有效期 48 小时）

官方 SDK 覆盖 [Python](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/funauidio-asr-recorded-speech-recognition-python-sdk.md)、[Java](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/fun-asr-recorded-speech-recognition-java-sdk.md)、[Android](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/fun-asr-recorded-speech-recognition-android-sdk.md)、[iOS](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/fun-asr-recorded-speech-recognition-ios-sdk.md) 四端。

> **注意**：使用新加坡新版域名提交任务时，请求体中**必须包含 `parameters` 对象**（即使为空 `{}`），否则识别会失败。

### 3.3 定制热词

通过热词列表提升特定术语的识别准确率。使用 Java SDK 的 `VocabularyService` 管理，详见 [定制热词Java SDK参考](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference/custom-hot-words/vocabulary-java-sdk.md)。

- 创建热词时需指定 `targetModel`（必须与后续识别使用的模型一致）和 `prefix`；
- 热词对象包含 `text`、`weight`、`lang` 字段；
- 当前新加坡地域的**子[业务空间](../concepts/workspace.md)暂不支持**热词功能。

## 四、实时音视频翻译（Qwen-LiveTranslate）

基于 `qwen3.5-livetranslate-flash-realtime`（旧版 `qwen3-livetranslate-flash-realtime`）模型，通过 WebSocket 实时接收音频并返回翻译结果（文本 + 合成音频），参见 [Python SDK](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference/live-translator-api/qwen-livetranslate-python-sdk.md) 与 [Java SDK](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference/live-translator-api/qwen-livetranslate-java-sdk.md)。

核心参数通过 `update_session` / `updateSession` 设置：

| 参数 | 说明 |
| --- | --- |
| `output_modalities` | `[TEXT]` 仅文本；`[TEXT, AUDIO]` 文本+音频（默认） |
| `voice` | 合成音频的音色（Qwen3.5 默认 `Tina`，Qwen3 默认 `Cherry`） |
| `translation_params.language` | 目标翻译语言（如 `en`） |
| `translation_params.corpus.phrases` | 术语表，用于纠正领域专有名词 |
| `input_audio_format` / `output_audio_format` | 音频编码格式（如 PCM 16000/24000 Hz） |
| `InputAudioTranscription` | 可选，指定一个 ASR 模型同时输出源语言转写 |

事件回调包含 `session.created`、`response.audio_transcript.done`、`response.audio.delta`、`input_audio_buffer.speech_started` / `speech_stopped` 等。

## 五、SDK 与语言覆盖速查

| 能力 | Python | Java | Android | iOS | HTTP/WS |
| --- | --- | --- | --- | --- | --- |
| 实时 TTS（CosyVoice） | ✅ | ✅ | ✅ | ✅ | WebSocket |
| 非实时 TTS（CosyVoice） | ✅ | ✅ | — | — | HTTP / SSE |
| 声音设计 | — | — | — | — | HTTP |
| 声音复刻 | — | ✅ | — | — | HTTP |
| Qwen-ASR | ✅ | ✅ | — | — | OpenAI 兼容 / DashScope |
| Fun-ASR | ✅ | ✅ | ✅ | ✅ | HTTP 异步 |
| 定制热词 | — | ✅ | — | — | HTTP |
| 实时翻译 | ✅ | ✅ | — | — | WebSocket |

## 六、常见注意事项

- **模型一致性**：声音设计 / 声音复刻 / 热词创建时指定的 `target_model`，必须与后续实际调用合成或识别时使用的模型完全一致，否则调用会失败。
- **音频 URL 可访问性**：复刻 / 设计接口要求音频 URL 公网可达；OSS 临时 URL 有效期 48 小时。
- **格式与采样率**：`opus` 格式与 `bit_rate` 参数仅在 `cosyvoice-v2` 及以上版本支持；`cosyvoice-v1` 不支持。
- **SSML / LaTeX**：CosyVoice 合成支持 SSML（需 `enable_ssml=true`）与 LaTeX 公式直读。
- **字级别时间戳**：仅流式合成可用，且仅 `cosyvoice-v3-flash` / `cosyvoice-v3-plus` 及部分 v2 复刻音色支持。
- **流式 vs 非流式**：实时场景一律走 WebSocket；离线 / 长文本走 HTTP（非实时 TTS 用 SSE 可选流式，ASR 长音频用 DashScope 异步）。

## 来源文档

- [声音设计API参考](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/voice-design-api-references.md)
- [录音文件识别（Qwen-ASR）API参考](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference/qwen-asr-api-reference.md)
- [CosyVoice客户端事件](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-client-events.md)
- [实时语音合成CosyVoice Java SDK](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-java-sdk.md)
- [实时语音合成CosyVoice Python SDK](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-python-sdk.md)
- [语音合成CosyVoice Android SDK](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-android-sdk.md)
- [语音合成CosyVoice iOS SDK](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-ios-sdk.md)
- [非实时语音合成CosyVoice HTTP API参考](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/non-realtime-cosyvoice-api/cosyvoice-tts-http-api.md)
- [非实时语音合成CosyVoice Java SDK参考](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/non-realtime-cosyvoice-api/cosyvoice-tts-java-sdk.md)
- [非实时语音合成CosyVoice Python SDK参考](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/non-realtime-cosyvoice-api/cosyvoice-tts-python-sdk.md)
- [声音复刻Java SDK参考](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/sound-reengraving/voice-clone-design-java-sdk.md)
- [Fun-ASR录音文件识别Python SDK](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/funauidio-asr-recorded-speech-recognition-python-sdk.md)
- [Fun-ASR录音文件识别HTTP API参考](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/fun-asr-recorded-speech-recognition-http-api.md)
- [Fun-ASR录音文件识别Android SDK](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/fun-asr-recorded-speech-recognition-android-sdk.md)
- [Fun-ASR录音文件识别iOS SDK](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/fun-asr-recorded-speech-recognition-ios-sdk.md)
- [Fun-ASR录音文件识别Java SDK](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/fun-asr-recorded-speech-recognition-java-sdk.md)
- [定制热词Java SDK参考](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference/custom-hot-words/vocabulary-java-sdk.md)
- [实时音视频翻译（Qwen-LiveTranslate）Python SDK-API参考](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference/live-translator-api/qwen-livetranslate-python-sdk.md)
- [实时音视频翻译（Qwen-LiveTranslate）Java SDK-API参考](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference/live-translator-api/qwen-livetranslate-java-sdk.md)



