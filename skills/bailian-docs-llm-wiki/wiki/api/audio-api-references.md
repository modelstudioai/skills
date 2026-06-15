# audio api references

百炼平台提供了完整的音频处理 API，涵盖语音合成（TTS）、语音识别（ASR）和实时音视频翻译三大类能力。开发者可通过 HTTP API、WebSocket 协议或多平台 SDK（Python、Java、Android、iOS）接入，支持实时流式与非实时批处理两种模式。

## 语音合成（TTS）

### CosyVoice 系列

CosyVoice 是百炼平台的核心语音合成引擎，提供实时和非实时两种调用方式。

**支持的模型**：cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-plus、cosyvoice-v3-flash、cosyvoice-v2。

**调用方式**：

- **实时语音合成**：通过 WebSocket 协议（`wss://dashscope.aliyuncs.com/api-ws/v1/inference`），支持双向流式，适合边生成文本边合成语音的场景。可通过 [实时语音合成CosyVoice Python SDK](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-python-sdk.md) 和 [实时语音合成CosyVoice Java SDK](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-java-sdk.md) 接入。
- **非实时语音合成**：通过 HTTP API（`POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer`），支持非流式和流式两种模式。详见 [非实时语音合成CosyVoice HTTP API参考](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/non-realtime-cosyvoice-api/cosyvoice-tts-http-api.md)。

> **注意**：非实时语音合成 CosyVoice 功能仅在华北2（北京）地域可用。

**关键参数**：

| 参数 | 说明 | 取值范围 |
|------|------|---------|
| `model` | 模型名称 | cosyvoice-v3.5-plus/flash、cosyvoice-v3-plus/flash、cosyvoice-v2 |
| `voice` | 音色（系统音色、复刻音色或声音设计音色） | 参见 CosyVoice 音色列表 |
| `format` | 音频编码格式 | pcm、wav、mp3、opus（cosyvoice-v1 不支持 opus） |
| `sample_rate` | 采样率（Hz） | 8000、16000、22050（默认）、24000、44100、48000 |
| `volume` | 音量 | 0-100，默认 50 |
| `rate` / `speech_rate` | 语速 | 0.5-2.0，默认 1.0 |
| `pitch` / `pitch_rate` | 音调 | 0.5-2.0，默认 1.0 |

**WebSocket 客户端事件协议**：实时合成通过三个客户端事件控制流程——`run-task`（启动任务）、`continue-task`（追加文本）、`finish-task`（结束任务）。详细事件结构参见 [CosyVoice客户端事件](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-client-events.md)。

**移动端 SDK**：Android 和 iOS SDK 基于单例架构和回调驱动模式，支持一次性输入和流式输入两种调用方式。Android 使用 `NativeNui.GetInstance()` 获取实例，iOS 使用 `NeoNui.sharedInstance()`。

**高级功能**：

- **Instruct 指令控制**：cosyvoice-v3.5-flash/plus 和部分系统音色支持通过 `instruction` 参数控制方言、情感或角色等合成效果，最大长度 100 字符。
- **字级别时间戳**：设置 `word_timestamp_enabled` 为 true 可获取字级别时间戳，仅在[流式输出](../concepts/streaming.md)模式下可用。
- **SSML 支持**：设置 `enable_ssml` 为 true 后可使用 SSML 标记语言控制合成细节。
- **随机种子**：`seed` 参数（0-65535）可使合成效果可复现。
- **语言提示**：`language_hints` 可指定目标语言，提升小语种和数字符号的合成效果。

### 声音定制

**声音设计**：通过 `POST .../api/v1/services/audio/tts/customization` 接口，基于文本描述生成自定义音色。支持两种引擎：

- **CosyVoice 声音设计**（model: `voice-enrollment`）：`voice_prompt` 最大 500 字符，支持中英文。
- **Qwen 声音设计**（model: `qwen-voice-design`）：`voice_prompt` 最大 2048 字符，支持 10 种语言。

详见 [声音设计API参考](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/voice-design-api-references.md)。

**声音复刻**：通过上传音频文件复制真人音色。Java SDK 提供 `VoiceEnrollmentService` 类管理音色的完整生命周期（创建、查询、更新、删除）。参见 [声音复刻Java SDK参考](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/sound-reengraving/voice-clone-design-java-sdk.md)。

### MiniMax 语音合成

百炼平台同时集成了 MiniMax 语音合成模型，支持 speech-2.8-hd、speech-02-hd、speech-2.8-turbo、speech-02-turbo 四个模型。

**调用端点**：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

MiniMax 模型具有独立的参数体系：

- 通过 `voice_setting` 设置音色、语速、音量、音高和情感。
- 通过 `audio_setting` 设置采样率、码率、格式和声道。
- 支持 `pronunciation_dict` 设置发音词典。
- 支持 `emotion` 参数直接设置情感（happy、sad、angry 等 8 种）。

> **注意**：MiniMax 的音量参数 `vol` 取值范围为 (0.0, 10.0]，与 CosyVoice 的 [0, 100] 不同，集成时需注意区分。

详见 [MiniMax同步语音合成API参考](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/minimax-speech-synthesis/minimax-synchronous-speech-synthesis-api.md)。

## 语音识别（ASR）

### Qwen-ASR

Qwen-ASR 支持录音文件识别，可通过 OpenAI 兼容和 DashScope 两种协议调用。

- **千问3-ASR-Flash-Filetrans**：仅支持 DashScope 异步调用方式。
- **千问3-ASR-Flash**：支持 OpenAI 兼容和 DashScope 同步调用两种方式。

OpenAI 兼容模式使用 `POST .../compatible-mode/v1/chat/completions`，通过 `input_audio` 类型的 content 传入音频 URL 或 Base64 数据。可通过 `asr_options` 设置语言和 ITN（逆文本正则化）选项。详见 [录音文件识别（Qwen-ASR）API参考](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference/qwen-asr-api-reference.md)。

> **注意**：美国地域不支持 OpenAI 兼容模式。

### Fun-ASR

Fun-ASR 专用于录音文件转写，采用异步"提交-轮询"模式：

1. **提交任务**：`POST .../api/v1/services/audio/asr/transcription`（需设置 `X-DashScope-Async: enable` 请求头）
2. **查询结果**：`GET .../api/v1/tasks/{task_id}`

**支持的模型**：fun-asr、fun-asr-2025-11-07、fun-asr-2025-08-25、fun-asr-mtl、fun-asr-mtl-2025-08-25。

**关键特性**：

- 支持多音轨识别（通过 `channel_id` 指定）
- 支持说话人分离（`diarization_enabled`）
- 支持定制热词（`vocabulary_id`）
- 支持敏感词过滤（`special_word_filter`）

**SDK 支持**：提供 [Fun-ASR录音文件识别Python SDK](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/funauidio-asr-recorded-speech-recognition-python-sdk.md)、[Fun-ASR录音文件识别Java SDK](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/fun-asr-recorded-speech-recognition-java-sdk.md)、Android SDK 和 iOS SDK 四种客户端。

### 定制热词

通过 `VocabularyService` 类（Java SDK）管理热词列表，支持创建、查询、更新、删除操作。热词可提升专业术语、人名、产品名等的识别准确率。参见 [定制热词Java SDK参考](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference/custom-hot-words/vocabulary-java-sdk.md)。

> **注意**：新加坡地域的子[业务空间](../concepts/workspace.md)暂不支持热词功能。

## 实时音视频翻译

### Qwen-LiveTranslate

基于 WebSocket 实时翻译服务，支持语音输入的实时翻译并输出文本和/或音频。

**推荐模型**：`qwen3.5-livetranslate-flash-realtime`（旧版 `qwen3-livetranslate-flash-realtime` 仍可用）。

**服务端点**：`wss://dashscope.aliyuncs.com/api-ws/v1/realtime`

**关键配置**：

- `output_modalities`：输出模态，可选仅文本或文本+音频。
- `voice`：输出音色，Qwen3.5 默认 Tina，Qwen3 默认 Cherry。
- `translation_params.language`：目标语言。
- `translation_params.corpus.phrases`：翻译热词词典，指定专业术语的翻译对照。

提供 [Python SDK](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference/live-translator-api/qwen-livetranslate-python-sdk.md) 和 [Java SDK](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference/live-translator-api/qwen-livetranslate-java-sdk.md) 两种接入方式。

## 地域与鉴权

所有音频 API 统一使用 `Authorization: Bearer <API_KEY>` 方式鉴权。支持的部署地域：

| 地域 | HTTP 端点 | WebSocket 端点 |
|------|-----------|---------------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/api/v1` | `wss://dashscope.aliyuncs.com/api-ws/v1/inference` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1` | `wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference` |

> **注意**：新加坡地域的旧版域名 `https://dashscope-intl.aliyuncs.com` 即将下线，请及时迁移到新版域名。不同地域的 API Key 不同，请确保使用对应地域的 Key。移动端 SDK（Android/iOS）建议使用临时 API Key 以降低泄露风险。

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
- [MiniMax同步语音合成API参考](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/minimax-speech-synthesis/minimax-synchronous-speech-synthesis-api.md)
- [声音复刻Java SDK参考](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/sound-reengraving/voice-clone-design-java-sdk.md)
- [Fun-ASR录音文件识别Python SDK](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/funauidio-asr-recorded-speech-recognition-python-sdk.md)
- [Fun-ASR录音文件识别HTTP API参考](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/fun-asr-recorded-speech-recognition-http-api.md)
- [Fun-ASR录音文件识别Android SDK](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/fun-asr-recorded-speech-recognition-android-sdk.md)
- [Fun-ASR录音文件识别iOS SDK](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/fun-asr-recorded-speech-recognition-ios-sdk.md)
- [Fun-ASR录音文件识别Java SDK](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/fun-asr-recorded-speech-recognition-java-sdk.md)
- [定制热词Java SDK参考](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference/custom-hot-words/vocabulary-java-sdk.md)
- [实时音视频翻译（Qwen-LiveTranslate）Python SDK-API参考](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference/live-translator-api/qwen-livetranslate-python-sdk.md)
- [实时音视频翻译（Qwen-LiveTranslate）Java SDK-API参考](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference/live-translator-api/qwen-livetranslate-java-sdk.md)





