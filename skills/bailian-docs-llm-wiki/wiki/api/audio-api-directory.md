# audio api directory

`audio api directory` 是百炼平台提供的非实时音频处理能力的统一入口，涵盖语音识别（ASR）、语音合成（TTS）、音频生成和音视频翻译四大核心功能。所有接口均面向离线或批量音频文件设计，支持同步与异步调用模式，并提供多语言 SDK 封装。实时音频能力（如实时 ASR/TTS）请参考 [Realtime API 概述](raw/model-api-reference/realtime-api-directory/realtime-api-overview.md)。

## 支持的模型/功能

本目录覆盖以下主要模型与能力：

- **语音识别（ASR）**：  
  - `Qwen-Audio-ASR`：支持 HTTP 和多端 SDK（Android/iOS/HarmonyOS），适用于中短音频（<10 分钟），支持上下文增强与 SSE 流式返回（[Qwen-Audio-ASR](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/qwen-audio-asr-api.md)）。  
  - `Qwen-Audio-ASR-Filetrans`：专为长音频（>10 分钟）设计的异步任务型接口，支持批量 URL 提交与轮询查询（[Qwen-Audio-ASR-Filetrans](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/qwen-audio-asr-filetrans-api.md)）。  
  - `Fun-ASR` / `Fun-ASR-Flash`：轻量级高性价比模型，分别适配通用录音与低延迟场景（[其他模型](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/non-realtime-asr-other-models.md)）。  
  - `Paraformer`：高性能开源模型，推荐用于高精度、长时语音转写，支持音轨选择与语气词过滤（[Paraformer非实时语音识别HTTP API](../../raw/_short/paraformer-recorded-speech-recognition-restful-a-8b487acdee52d08d.md)）。  
  - **定制热词**：通过独立接口管理热词列表，提升领域专有词汇识别准确率（[定制热词](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words.md)）。

- **语音合成（TTS）**：  
  - `Qwen-Audio-TTS`：支持 SSML/LaTeX、多音色、多采样率与编码格式（[Qwen-Audio-TTS](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-qwen-audio-tts-api.md)）。  
  - `CosyVoice`：强调自然度与情感表达，提供多个版本模型（v2/v3/v3.5 系列）（[CosyVoice](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-cosyvoice-api.md)）。

- **其他**：  
  - 音频生成、音视频翻译等功能详见 [音频（非实时）](../../raw/model-api-reference/audio-api-directory/audio-api-references.md) 主目录。

> **注意**：`Qwen-ASR` 模型文档（文档 32–33）明确指出其仅支持 DashScope 异步调用（Filetrans 类型）或 OpenAI 兼容模式，但未提供独立的同步 HTTP 接口；而 `Qwen-Audio-ASR`（文档 2–7）和 `Fun-ASR-Flash`（文档 27–31）均支持同步流式调用。开发者应根据实际延迟与音频长度需求选择对应模型，避免误用不支持的调用方式。

## 关键参数

所有音频 API 的关键参数具有高度一致性，主要包括：

- **`model`**（必选 `string`）：指定模型 ID，如 `"qwen-audio-3.1-asr-flash-filetrans"` 或 `"cosyvoice-v3.5-plus"`。  
- **`input`**（必选 `object`）：  
  - ASR：含 `file_urls`（异步）或 `messages` 中 `input_audio`（同步）；  
  - TTS：含 `text`（支持 SSML/LaTeX）、`voice`（音色 ID）、`format`（`mp3`/`wav`/`opus` 等）、`sample_rate`（如 `16000`, `22050`, `48000`）。  
- **`url`（服务地址）**：必须使用业务空间专属域名（如 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名 `dashscope.aliyuncs.com` 已不推荐（[Qwen-Audio-ASR-Filetrans非实时语音识别HTTP API参考](../../raw/_short/qwen-audio-asr-filetrans-http-api-e0184f38f9d98459.md)）。  
- **`Authorization` 请求头**：固定为 `Bearer <your_api_key>`，API Key 需与 Workspace ID 所在地域匹配（北京/新加坡等）。  
- **`X-DashScope-Async`**（ASR 异步任务）：必须设为 `"enable"`，否则提交失败（[Fun-ASR非实时语音识别HTTP API参考](../../raw/_short/fun-asr-recorded-speech-recognition-http-api-0e04e08da4894bf2.md)）。  
- **`X-DashScope-SSE`**（流式返回）：设为 `"enable"` 启用 SSE 流式响应（仅部分 ASR/TTS 模型支持，且对音频时长有最低要求，如 Qwen-Audio-ASR 要求 ≥1 分钟）。

## 使用方式

- **同步调用（适合 ≤10 分钟音频）**：  
  直接发送 POST 请求至 `/generation` 端点（如 `.../multimodal-generation/generation`），等待完整响应。支持 `X-DashScope-SSE: enable` 获取中间结果流。SDK 中对应 `startFileTranscriber`（Android/iOS/HarmonyOS）或 `client.audio.asr.jobs.create` + `wait`（Python/Java）。

- **异步调用（适合长音频或高并发）**：  
  1. **提交任务**：POST 至 `/transcription` 端点，携带 `X-DashScope-Async: enable`，获取 `task_id`；  
  2. **轮询结果**：GET `/tasks/{task_id}`，直至状态为 `SUCCEEDED`；  
  3. **下载结果**：从响应中提取 `transcription_url`（24 小时有效）或 `audio_info.url`（TTS）。  
  Python/Java SDK 提供 `jobs.create` + `jobs.wait` 封装，简化轮询逻辑。

- **SDK 初始化共性**：  
  所有移动端 SDK（Android/iOS/HarmonyOS）均需在 `initialize`/`nui_initialize`/`initializeFileTrans` 中传入 JSON 参数，包含 `url`、`apikey`、`service_mode: "1"`（非实时标识）及 `device_id`（用于日志追踪）。

## 限制和注意事项

- **地域与域名强绑定**：北京/新加坡 Workspace ID 必须搭配对应地域专属域名（如 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），且 API Key 需与地域一致。跨地域混用将导致鉴权失败（[定制热词HTTP API参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-http-api.md)）。
- **热词功能地域限制**：定制热词目前**仅支持华北2（北京）地域**，新加坡子业务空间明确不支持（文档 16、18、22）。
- **音频预处理建议**：Paraformer 等模型虽支持视频文件，但强烈建议预处理为纯音频（如用 `ffmpeg -i input.mp4 -ac 1 -ar 16000 -acodec libopus output.opus`），可显著降低传输耗时与识别延迟（[最佳实践](../../raw/_short/paraformer-best-practices-b5bb2777c9abaf3c.md)）。
- **临时 API Key 推荐**：涉及客户端直连（如移动端 SDK）时，务必使用时效短（默认 60 秒）、权限受限的 [临时 API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)，而非长期有效 Key，以降低泄露风险（文档 7、17、34、35、36、37、38、39、44、45、48）。
- **异步任务有效期**：所有异步任务的识别结果与下载 URL 有效期为 **24 小时**，超时后无法查询或下载（文档 10、12、21、46）。

## 来源文档

- [音频（非实时）](../../raw/model-api-reference/audio-api-directory/audio-api-references.md)
- [Qwen-Audio-ASR](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/qwen-audio-asr-api.md)
- [语音识别](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference.md)
- [非实时语音识别（Qwen-Audio-ASR）Android SDK](../../raw/_short/qwen-audio-asr-android-sdk-1e97f1d8b5e9135c.md)
- [非实时语音识别（Qwen-Audio-ASR）HTTP API](../../raw/_short/qwen-audio-asr-http-api-90b9d62787e911f4.md)
- [非实时语音识别（Qwen-Audio-ASR）iOS SDK](../../raw/_short/qwen-audio-asr-ios-sdk-fc08c802d4ff7f08.md)
- [非实时语音识别（Qwen-Audio-ASR）HarmonyOS SDK](../../raw/_short/qwen-audio-asr-harmonyos-sdk-b1335f47a12054cd.md)
- [Qwen-Audio-ASR-Filetrans](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/qwen-audio-asr-filetrans-api.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别HTTP API参考](../../raw/_short/qwen-audio-asr-filetrans-http-api-e0184f38f9d98459.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别Python SDK](../../raw/_short/qwen-audio-asr-filetrans-python-sdk-e244defb9b1288ee.md)
- [Qwen-Audio-ASR-Filetrans Node.js SDK](../../raw/_short/qwen-audio-asr-filetrans-nodejs-sdk-6457111def74455c.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别Java SDK](../../raw/_short/qwen-audio-asr-filetrans-java-sdk-e33c81cb99967d86.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别iOS SDK](../../raw/_short/qwen-audio-asr-filetrans-ios-sdk-ac5cc79341721cdd.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别Android SDK](../../raw/_short/qwen-audio-asr-filetrans-android-sdk-a3c0fbd842a710b1.md)
- [定制热词](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words.md)
- [定制热词HTTP API参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-http-api.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别HarmonyOS SDK](../../raw/_short/qwen-audio-asr-filetrans-harmonyos-sdk-bca7ed5502ce3fcf.md)
- [定制热词Java SDK参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-java-sdk.md)
- [其他模型](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/non-realtime-asr-other-models.md)
- [Fun-ASR](../../raw/_short/fun-asr-recorded-speech-recognition-api-referenc-b0273c90bb44d4cc.md)
- [Fun-ASR非实时语音识别Python SDK](../../raw/_short/funauidio-asr-recorded-speech-recognition-python-d69dda8f4675042c.md)
- [定制热词Python SDK参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-python-sdk.md)
- [Fun-ASR非实时语音识别Android SDK](../../raw/_short/fun-asr-recorded-speech-recognition-android-sdk-f828ab21cfa96d66.md)
- [Fun-ASR非实时语音识别iOS SDK](../../raw/_short/fun-asr-recorded-speech-recognition-ios-sdk-e6f16b9236096238.md)
- [Fun-ASR非实时语音识别HTTP API参考](../../raw/_short/fun-asr-recorded-speech-recognition-http-api-0e04e08da4894bf2.md)
- [Fun-ASR非实时语音识别HarmonyOS SDK](../../raw/_short/fun-asr-recorded-speech-recognition-harmonyos-sd-f2337ad439819fc6.md)
- [Fun-ASR-Flash](../../raw/_short/non-real-time-speech-recognition-for-fun-asr-fla-650fa37d535f17b4.md)
- [非实时语音识别（Fun-ASR-Flash）HTTP API](../../raw/_short/fun-asr-flash-recorded-speech-recognition-http-a-7716e5d27dfd9a7b.md)
- [非实时语音识别（Fun-ASR-Flash）Android SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-androi-5c29202b31b7bc7c.md)
- [非实时语音识别（Fun-ASR-Flash）iOS SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-ios-sd-ebb52f47ee469aa4.md)
- [非实时语音识别（Fun-ASR-Flash）HarmonyOS SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-harmon-eee2d6e9b92ea2cc.md)
- [Qwen-ASR](../../raw/_short/qwen-asr-non-realtime-api-da664e843d2e7fef.md)
- [非实时语音识别（Qwen-ASR）API参考](../../raw/_short/qwen-asr-api-reference-6234af32190b8ba9.md)
- [Paraformer非实时语音识别HTTP API](../../raw/_short/paraformer-recorded-speech-recognition-restful-a-8b487acdee52d08d.md)
- [Paraformer非实时语音识别Python SDK](../../raw/_short/paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md)
- [Paraformer非实时语音识别Java SDK](../../raw/_short/paraformer-recorded-speech-recognition-java-sdk-915d733e99a3db9b.md)
- [Paraformer非实时语音识别Android SDK](../../raw/_short/paraformer-recorded-speech-recognition-android-s-13e83d144d148a4f.md)
- [Paraformer非实时语音识别iOS SDK](../../raw/_short/paraformer-recorded-speech-recognition-ios-sdk-137ff6eb176e867a.md)
- [Paraformer非实时语音识别HarmonyOS SDK](../../raw/_short/paraformer-recorded-speech-recognition-harmonyos-71907f3ccc6c91c4.md)
- [最佳实践](../../raw/_short/paraformer-best-practices-b5bb2777c9abaf3c.md)
- [语音合成](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference.md)
- [Qwen-Audio-TTS](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-qwen-audio-tts-api.md)
- [非实时语音合成Qwen-Audio-TTS HTTP API参考](../../raw/_short/qwen-audio-tts-http-api-ee05f9b13900b687.md)
- [非实时语音合成Qwen-Audio-TTS Java SDK参考](../../raw/_short/qwen-audio-tts-http-java-sdk-e802adc41b79b00c.md)
- [非实时语音合成Qwen-Audio-TTS Python SDK参考](../../raw/_short/qwen-audio-tts-http-python-sdk-5de04c79426618ab.md)
- [Fun-ASR非实时语音识别Java SDK](../../raw/_short/fun-asr-recorded-speech-recognition-java-sdk-b2ce5e0f37e9003f.md)
- [CosyVoice](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-cosyvoice-api.md)
- [非实时语音合成CosyVoice Java SDK参考](../../raw/_short/cosyvoice-tts-java-sdk-b4e23dd3f27b95e0.md)
- [非实时语音合成CosyVoice HTTP API参考](../../raw/_short/cosyvoice-tts-http-api-63e05680db50f996.md)
- [非实时语音合成CosyVoice Python SDK参考](../../raw/_short/cosyvoice-tts-python-sdk-01187ba238f52941.md)
- [其他模型](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-tts-other-models.md)
- [Qwen-TTS](../../raw/_short/qwen-tts-non-realtime-api-1c364eb278c0a2e2.md)
- [非实时语音合成（Qwen-TTS）API参考](../../raw/_short/qwen-tts-api-3dac64d546223453.md)
- [MiniMax](../../raw/_short/minimax-speech-synthesis-9ac5812df734fd8c.md)
- [MiniMax同步语音合成API参考](../../raw/_short/minimax-synchronous-speech-synthesis-api-cddb40af595ff320.md)
- [音频生成 API参考](../../raw/model-api-reference/audio-api-directory/audio-generation-api.md)
- [音视频翻译](../../raw/model-api-reference/audio-api-directory/qwen3-livetranslate-flash-api.md)
- [Paraformer](../../raw/_short/paraformer-recorded-speech-recognition-api-refer-3f19f98cbb4ce26b.md)


