# audio api directory

本目录提供非实时音频处理能力的 API 参考，涵盖语音识别（ASR）、语音合成（TTS）、音频生成和音视频翻译四大核心功能。所有接口均面向离线/批量场景设计，支持同步响应与异步任务两种调用模式，并兼容 HTTP、Python、Java、Node.js、Android、iOS 和 HarmonyOS 多种接入方式。实时音频能力请参见 [Realtime API 概述](raw/model-api-reference/realtime-api-directory/realtime-api-overview.md)。

## 支持的模型/功能

- **语音识别（ASR）**：提供多模型选择，包括 `Qwen-Audio-ASR`（含 Flash 与 Filetrans 变体）、`Fun-ASR`（含 Flash）、`Qwen-ASR` 和 `Paraformer`。其中 `Qwen-Audio-ASR-Filetrans` 专为长音频文件转写优化，采用“提交-轮询”异步流程；`Qwen-Audio-ASR` 和 `Fun-ASR-Flash` 支持流式 SSE 响应（需音频 ≥1 分钟）[非实时语音识别（Qwen-Audio-ASR）HTTP API](../../raw/_short/qwen-audio-asr-http-api-90b9d62787e911f4.md)。
- **语音合成（TTS）**：支持 `Qwen-Audio-TTS` 和 `CosyVoice` 两大引擎，均提供系统音色、声音复刻及声音设计音色接入能力，并原生支持 SSML 与 LaTeX 格式文本输入 [非实时语音合成Qwen-Audio-TTS HTTP API参考](../../raw/_short/qwen-audio-tts-http-api-ee05f9b13900b687.md)。
- **音频生成与音视频翻译**：分别由 [音频生成](raw/model-api-reference/audio-api-directory/audio-generation-api.md) 和 [音视频翻译](raw/model-api-reference/audio-api-directory/qwen3-livetranslate-flash-api.md) 文档定义，本文档聚焦 ASR/TTS。

> **注意**：`Qwen-ASR` 模型的 OpenAI 兼容模式仅支持华北2（北京）和新加坡地域，且美国地域明确不支持该模式；而 `Qwen-Audio-TTS` 和 `CosyVoice` 的 Java SDK 明确标注“仅在华北2（北京）地域可用”，存在地域能力不一致问题。

## 关键参数

- **通用认证与路由**：
  - `Authorization`: `Bearer <your_api_key>`，必须通过环境变量配置，禁止硬编码。
  - `X-DashScope-SSE`: 控制[流式输出](../concepts/streaming-output.md)（`enable`/`disable`），仅对支持流式的模型（如 `qwen-audio-3.0-asr-flash`）生效。
  - `X-DashScope-Async`: 异步任务必需头（值为 `enable`），用于 `Filetrans` 类接口。
  - `url` 参数中 `{WorkspaceId}` 必须替换为真实业务空间 ID，推荐使用专属域名（如 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）而非旧版 `dashscope.aliyuncs.com`。

- **ASR 输入核心**：
  - `input.file_urls`: 字符串数组，传入公网可访问的音频 URL（`Filetrans` 类）。
  - `input.messages`: 对象数组，用于上下文增强（`Flash` 类），要求 `user`（含 `input_audio`）必须置于末尾，且上下文轮次需严格配对。

- **TTS 输入核心**：
  - `input.text`: 待合成文本，支持纯文本、SSML（需设 `enable_ssml=true`）或 LaTeX。
  - `input.voice`: 音色标识符，可为系统音色 ID、复刻音色 ID 或设计音色 ID。
  - `format` / `sample_rate`: 音频格式（`mp3`, `wav`, `opus` 等）与采样率（8000–48000 Hz），`opus` 格式对采样率有额外限制。

## 使用方式

- **同步调用（短音频/低延迟）**：适用于时长较短（通常 <5 分钟）的音频。直接发送请求，服务端返回最终结果。例如 `Qwen-Audio-ASR` HTTP 接口或 `Qwen-Audio-TTS` 的 `callAndReturnAudio()` 方法。
- **异步调用（长音频/高吞吐）**：适用于大文件或高并发场景。分两步：1) 提交任务获取 `task_id`；2) 轮询 `/api/v1/tasks/{task_id}` 查询状态与结果。`Qwen-Audio-ASR-Filetrans`、`Fun-ASR`、`Paraformer` 均采用此模式 [Qwen-Audio-ASR-Filetrans非实时语音识别HTTP API参考](../../raw/_short/qwen-audio-asr-filetrans-http-api-e0184f38f9d98459.md)。
- **SDK 封装**：各语言 SDK（Python/Java/Node.js/移动端）已封装底层协议细节。Python SDK 的 `client.audio.asr.jobs.create()` + `jobs.wait()` 组合可实现“提交即等待”语义；移动端 SDK（Android/iOS/HarmonyOS）则通过 `async_request` 参数控制同步/异步行为。

## 限制和注意事项

- **音频规格**：所有 ASR 模型均遵循统一的[音频规格](https://help.aliyun.com/zh/model-studio/asr-model#asr_audio_spec02)，包括格式（WAV/MP3/OPUS 等）、采样率（≥8kHz）、单文件大小（≤200MB）与时长（≤6 小时）限制。
- **地域与功能约束**：
  - 定制热词功能在新加坡地域子业务空间不可用。
  - `Paraformer` 的 Android/iOS SDK 使用旧版 WebSocket 地址 `wss://dashscope.aliyuncs.com/api-ws/v1/inference`，与其他模型的 `.../multimodal-generation/generation` 或 `.../audio/asr/transcription` 不一致，需单独适配。
- **安全实践**：
  - API Key 必须配置于环境变量，严禁硬编码。
  - 敏感场景（如第三方调用）应使用时效仅 60 秒的[临时 API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。
- **结果有效期**：异步任务生成的识别结果下载 URL 或音频 URL 有效期为 24 小时，超时后失效。

## 来源文档

- [音频（非实时）](../../raw/model-api-reference/audio-api-directory/audio-api-references.md)
- [Qwen-Audio-ASR](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/qwen-audio-asr-api.md)
- [语音识别](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference.md)
- [非实时语音识别（Qwen-Audio-ASR）HTTP API](../../raw/_short/qwen-audio-asr-http-api-90b9d62787e911f4.md)
- [非实时语音识别（Qwen-Audio-ASR）Android SDK](../../raw/_short/qwen-audio-asr-android-sdk-1e97f1d8b5e9135c.md)
- [非实时语音识别（Qwen-Audio-ASR）iOS SDK](../../raw/_short/qwen-audio-asr-ios-sdk-fc08c802d4ff7f08.md)
- [Qwen-Audio-ASR-Filetrans](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/qwen-audio-asr-filetrans-api.md)
- [非实时语音识别（Qwen-Audio-ASR）HarmonyOS SDK](../../raw/_short/qwen-audio-asr-harmonyos-sdk-b1335f47a12054cd.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别HTTP API参考](../../raw/_short/qwen-audio-asr-filetrans-http-api-e0184f38f9d98459.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别Python SDK](../../raw/_short/qwen-audio-asr-filetrans-python-sdk-e244defb9b1288ee.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别Java SDK](../../raw/_short/qwen-audio-asr-filetrans-java-sdk-e33c81cb99967d86.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别Android SDK](../../raw/_short/qwen-audio-asr-filetrans-android-sdk-a3c0fbd842a710b1.md)
- [Qwen-Audio-ASR-Filetrans Node.js SDK](../../raw/_short/qwen-audio-asr-filetrans-nodejs-sdk-6457111def74455c.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别iOS SDK](../../raw/_short/qwen-audio-asr-filetrans-ios-sdk-ac5cc79341721cdd.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别HarmonyOS SDK](../../raw/_short/qwen-audio-asr-filetrans-harmonyos-sdk-bca7ed5502ce3fcf.md)
- [定制热词](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words.md)
- [定制热词Python SDK参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-python-sdk.md)
- [定制热词HTTP API参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-http-api.md)
- [其他模型](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/non-realtime-asr-other-models.md)
- [定制热词Java SDK参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-java-sdk.md)
- [Fun-ASR非实时语音识别HTTP API参考](../../raw/_short/fun-asr-recorded-speech-recognition-http-api-0e04e08da4894bf2.md)
- [Fun-ASR](../../raw/_short/fun-asr-recorded-speech-recognition-api-referenc-b0273c90bb44d4cc.md)
- [Fun-ASR非实时语音识别Java SDK](../../raw/_short/fun-asr-recorded-speech-recognition-java-sdk-b2ce5e0f37e9003f.md)
- [Fun-ASR非实时语音识别Android SDK](../../raw/_short/fun-asr-recorded-speech-recognition-android-sdk-f828ab21cfa96d66.md)
- [Fun-ASR非实时语音识别HarmonyOS SDK](../../raw/_short/fun-asr-recorded-speech-recognition-harmonyos-sd-f2337ad439819fc6.md)
- [Fun-ASR-Flash](../../raw/_short/non-real-time-speech-recognition-for-fun-asr-fla-650fa37d535f17b4.md)
- [非实时语音识别（Fun-ASR-Flash）HTTP API](../../raw/_short/fun-asr-flash-recorded-speech-recognition-http-a-7716e5d27dfd9a7b.md)
- [非实时语音识别（Fun-ASR-Flash）Android SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-androi-5c29202b31b7bc7c.md)
- [非实时语音识别（Fun-ASR-Flash）iOS SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-ios-sd-ebb52f47ee469aa4.md)
- [非实时语音识别（Fun-ASR-Flash）HarmonyOS SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-harmon-eee2d6e9b92ea2cc.md)
- [Qwen-ASR](../../raw/_short/qwen-asr-non-realtime-api-da664e843d2e7fef.md)
- [非实时语音识别（Qwen-ASR）API参考](../../raw/_short/qwen-asr-api-reference-6234af32190b8ba9.md)
- [Paraformer](../../raw/_short/paraformer-recorded-speech-recognition-api-refer-3f19f98cbb4ce26b.md)
- [Paraformer非实时语音识别HTTP API](../../raw/_short/paraformer-recorded-speech-recognition-restful-a-8b487acdee52d08d.md)
- [Fun-ASR非实时语音识别Python SDK](../../raw/_short/funauidio-asr-recorded-speech-recognition-python-d69dda8f4675042c.md)
- [Fun-ASR非实时语音识别iOS SDK](../../raw/_short/fun-asr-recorded-speech-recognition-ios-sdk-e6f16b9236096238.md)
- [Paraformer非实时语音识别Android SDK](../../raw/_short/paraformer-recorded-speech-recognition-android-s-13e83d144d148a4f.md)
- [Paraformer非实时语音识别iOS SDK](../../raw/_short/paraformer-recorded-speech-recognition-ios-sdk-137ff6eb176e867a.md)
- [Paraformer非实时语音识别HarmonyOS SDK](../../raw/_short/paraformer-recorded-speech-recognition-harmonyos-71907f3ccc6c91c4.md)
- [最佳实践](../../raw/_short/paraformer-best-practices-b5bb2777c9abaf3c.md)
- [语音合成](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference.md)
- [Qwen-Audio-TTS](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-qwen-audio-tts-api.md)
- [非实时语音合成Qwen-Audio-TTS HTTP API参考](../../raw/_short/qwen-audio-tts-http-api-ee05f9b13900b687.md)
- [非实时语音合成Qwen-Audio-TTS Java SDK参考](../../raw/_short/qwen-audio-tts-http-java-sdk-e802adc41b79b00c.md)
- [Paraformer非实时语音识别Python SDK](../../raw/_short/paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md)
- [非实时语音合成Qwen-Audio-TTS Python SDK参考](../../raw/_short/qwen-audio-tts-http-python-sdk-5de04c79426618ab.md)
- [CosyVoice](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-cosyvoice-api.md)
- [Paraformer非实时语音识别Java SDK](../../raw/_short/paraformer-recorded-speech-recognition-java-sdk-915d733e99a3db9b.md)
- [非实时语音合成CosyVoice HTTP API参考](../../raw/_short/cosyvoice-tts-http-api-63e05680db50f996.md)
- [非实时语音合成CosyVoice Java SDK参考](../../raw/_short/cosyvoice-tts-java-sdk-b4e23dd3f27b95e0.md)
- [非实时语音合成CosyVoice Python SDK参考](../../raw/_short/cosyvoice-tts-python-sdk-01187ba238f52941.md)
- [Qwen-TTS](../../raw/_short/qwen-tts-non-realtime-api-1c364eb278c0a2e2.md)
- [其他模型](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-tts-other-models.md)
- [非实时语音合成（Qwen-TTS）API参考](../../raw/_short/qwen-tts-api-3dac64d546223453.md)
- [MiniMax](../../raw/_short/minimax-speech-synthesis-9ac5812df734fd8c.md)
- [MiniMax同步语音合成API参考](../../raw/_short/minimax-synchronous-speech-synthesis-api-cddb40af595ff320.md)
- [音频生成 API参考](../../raw/model-api-reference/audio-api-directory/audio-generation-api.md)
- [音视频翻译](../../raw/model-api-reference/audio-api-directory/qwen3-livetranslate-flash-api.md)


