# audio api directory

本目录汇总百炼平台提供的非实时音频处理能力，涵盖语音识别（ASR）、语音合成（TTS）、音频生成和音视频翻译四大类 API。所有接口均面向离线或批量音频文件处理场景，支持同步、异步及流式响应模式，并提供多语言 SDK 封装。实时音频能力（如实时 ASR/TTS）请参考 [Realtime API 概述](raw/model-api-reference/realtime-api-directory/realtime-api-overview.md)。

## 支持的模型/功能

### 语音识别（ASR）
- **Qwen-Audio-ASR**：通用高精度识别，支持上下文增强与 SSE 流式返回（[Qwen-Audio-ASR](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/qwen-audio-asr-api.md)）。
- **Qwen-Audio-ASR-Filetrans**：专为长音频文件设计的异步转写服务，采用“提交-轮询”流程，结果有效期 24 小时（[Qwen-Audio-ASR-Filetrans](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/qwen-audio-asr-filetrans-api.md)）。
- **Fun-ASR / Fun-ASR-Flash**：轻量级模型，适用于低延迟中短音频识别；Fun-ASR-Flash 支持上下文与流式（[Fun-ASR-Flash](../../raw/_short/non-real-time-speech-recognition-for-fun-asr-fla-650fa37d535f17b4.md)）。
- **Paraformer**：高性能开源模型，推荐用于录音文件识别；最佳实践建议预处理视频为 16kHz Opus 音频以提升吞吐（[Paraformer](../../raw/_short/paraformer-recorded-speech-recognition-api-refer-3f19f98cbb4ce26b.md)）。
- **定制热词**：通过 `speech-biasing` 模型提升专有词汇识别准确率，但新加坡地域暂不支持（[定制热词](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words.md)）。

### 语音合成（TTS）
- **Qwen-Audio-TTS**：支持 SSML/LaTeX 输入、多音色（含复刻/设计音色）、多种格式（mp3/wav/opus）与采样率（[Qwen-Audio-TTS](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-qwen-audio-tts-api.md)）。
- **CosyVoice**：多版本模型（v3.5-plus/v3-flash 等），参数与 Qwen-Audio-TTS 高度一致，但仅限华北2（北京）地域（[CosyVoice](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-cosyvoice-api.md)）。
- **其他模型**：包括 Qwen-TTS、MiniMax 等第三方集成方案（[其他模型](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-tts-other-models.md)）。

> **注意**：CosyVoice 和 Qwen-Audio-TTS 的 Java/Python SDK 均明确标注“仅在华北2（北京）地域可用”，而其 HTTP API 文档未限定地域；实际调用时需严格匹配地域配置，否则可能失败。

## 关键参数

### 通用参数
- **`Authorization`**：必填，格式 `Bearer <your_api_key>`，需与 Workspace 所在地域匹配。
- **`Content-Type`**：必填，固定为 `application/json`（HTTP）或 `application/octet-stream`（部分文件上传场景）。
- **`X-DashScope-SSE`**：控制流式响应，设为 `enable` 启用 SSE；仅对 `qwen-audio-3.0-asr-flash` 要求音频 ≥1 分钟才分片返回（[Qwen-Audio-ASR HTTP API](../../raw/_short/qwen-audio-asr-http-api-90b9d62787e911f4.md)）。
- **`X-DashScope-Async`**：异步任务必需，设为 `enable`（如 Filetrans、Fun-ASR 提交接口）。

### 模型特有参数
- **ASR `input.messages`**：`user`（含 `input_audio`）必须置于数组末尾；上下文消息（`input_text`/`text`）各限 5 条，每轮总长 ≤400 字符（[Qwen-Audio-ASR HTTP API](../../raw/_short/qwen-audio-asr-http-api-90b9d62787e911f4.md)）。
- **TTS `input.text`**：支持 SSML（需 `enable_ssml=true`）和 LaTeX 格式（无需额外配置）。
- **TTS `format` & `sample_rate`**：`opus` 格式下 `sample_rate` 仅支持 8000/12000/16000/24000/48000（[CosyVoice HTTP API](../../raw/_short/cosyvoice-tts-http-api-63e05680db50f996.md)）。

## 使用方式

### 接口调用模式
- **同步调用**：适用于 ≤1 分钟音频，一次请求立即返回结果（如 Qwen-Audio-ASR、Qwen-Audio-TTS）。
- **异步调用（提交-轮询）**：适用于长音频，先调用提交接口获 `task_id`，再轮询 `GET /api/v1/tasks/{task_id}` 查询状态（如 Qwen-Audio-ASR-Filetrans、Paraformer）。
- **流式调用（SSE）**：通过 `X-DashScope-SSE: enable` 启用，服务端分片推送中间结果（ASR）或音频数据（TTS）。

### SDK 集成要点
- **URL 配置**：所有 SDK 均需显式设置 Workspace ID 和地域（如 `cn-beijing` 或 `ap-southeast-1`），优先使用业务空间专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）而非旧域名（`dashscope.aliyuncs.com`）。
- **API Key 安全**：强烈建议配置到环境变量（如 `DASHSCOPE_API_KEY`），避免硬编码；敏感场景应使用临时 Token（60 秒有效期）（[临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)）。
- **客户端初始化**：Android/iOS/HarmonyOS SDK 均需在 `initialize`/`nui_initialize` 中传入 JSON 参数（含 `url`, `apikey`, `service_mode="1"`）。

## 限制和注意事项

- **地域限制**：CosyVoice 及其 SDK 仅支持华北2（北京）；Fun-ASR-Flash 的 OpenAI 兼容模式美国地域不可用；定制热词在新加坡地域不可用（[定制热词HTTP API参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-http-api.md)）。
- **音频规格**：所有 ASR/TTS 接口均遵循统一[音频规格](https://help.aliyun.com/zh/model-studio/asr-model#asr_audio_spec02)，包括格式（WAV/MP3/OPUS 等）、大小（通常 ≤100 MB）、时长（单文件 ≤2 小时）等硬性约束。
- **异步任务生命周期**：Filetrans 类任务结果 URL 有效期为 24 小时，超时后无法下载；Paraformer 等任务排队时间取决于队列长度，通常数分钟内开始处理（[Qwen-Audio-ASR-Filetrans Python SDK](../../raw/_short/qwen-audio-asr-filetrans-python-sdk-e244defb9b1288ee.md)）。
- **SDK 兼容性**：HarmonyOS SDK 的 `url` 参数在不同模型间存在差异——Qwen-Audio-ASR 固定为 `/api/v1/services/aigc/multimodal-generation/generation`，而 Paraformer 固定为 `/api/v1/services/audio/asr/transcription`；务必按模型文档配置，否则初始化失败。

## 来源文档

- [音频（非实时）](../../raw/model-api-reference/audio-api-directory/audio-api-references.md)
- [语音识别](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference.md)
- [Qwen-Audio-ASR](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/qwen-audio-asr-api.md)
- [非实时语音识别（Qwen-Audio-ASR）HTTP API](../../raw/_short/qwen-audio-asr-http-api-90b9d62787e911f4.md)
- [非实时语音识别（Qwen-Audio-ASR）iOS SDK](../../raw/_short/qwen-audio-asr-ios-sdk-fc08c802d4ff7f08.md)
- [非实时语音识别（Qwen-Audio-ASR）Android SDK](../../raw/_short/qwen-audio-asr-android-sdk-1e97f1d8b5e9135c.md)
- [非实时语音识别（Qwen-Audio-ASR）HarmonyOS SDK](../../raw/_short/qwen-audio-asr-harmonyos-sdk-b1335f47a12054cd.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别HTTP API参考](../../raw/_short/qwen-audio-asr-filetrans-http-api-e0184f38f9d98459.md)
- [Qwen-Audio-ASR-Filetrans](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/qwen-audio-asr-filetrans-api.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别Python SDK](../../raw/_short/qwen-audio-asr-filetrans-python-sdk-e244defb9b1288ee.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别Java SDK](../../raw/_short/qwen-audio-asr-filetrans-java-sdk-e33c81cb99967d86.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别iOS SDK](../../raw/_short/qwen-audio-asr-filetrans-ios-sdk-ac5cc79341721cdd.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别Android SDK](../../raw/_short/qwen-audio-asr-filetrans-android-sdk-a3c0fbd842a710b1.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别HarmonyOS SDK](../../raw/_short/qwen-audio-asr-filetrans-harmonyos-sdk-bca7ed5502ce3fcf.md)
- [定制热词Python SDK参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-python-sdk.md)
- [定制热词](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words.md)
- [定制热词HTTP API参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-http-api.md)
- [其他模型](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/non-realtime-asr-other-models.md)
- [Fun-ASR非实时语音识别HTTP API参考](../../raw/_short/fun-asr-recorded-speech-recognition-http-api-0e04e08da4894bf2.md)
- [Fun-ASR非实时语音识别Python SDK](../../raw/_short/funauidio-asr-recorded-speech-recognition-python-d69dda8f4675042c.md)
- [Fun-ASR非实时语音识别Java SDK](../../raw/_short/fun-asr-recorded-speech-recognition-java-sdk-b2ce5e0f37e9003f.md)
- [Fun-ASR非实时语音识别Android SDK](../../raw/_short/fun-asr-recorded-speech-recognition-android-sdk-f828ab21cfa96d66.md)
- [Fun-ASR非实时语音识别iOS SDK](../../raw/_short/fun-asr-recorded-speech-recognition-ios-sdk-e6f16b9236096238.md)
- [Fun-ASR非实时语音识别HarmonyOS SDK](../../raw/_short/fun-asr-recorded-speech-recognition-harmonyos-sd-f2337ad439819fc6.md)
- [Fun-ASR-Flash](../../raw/_short/non-real-time-speech-recognition-for-fun-asr-fla-650fa37d535f17b4.md)
- [非实时语音识别（Fun-ASR-Flash）HTTP API](../../raw/_short/fun-asr-flash-recorded-speech-recognition-http-a-7716e5d27dfd9a7b.md)
- [非实时语音识别（Fun-ASR-Flash）Android SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-androi-5c29202b31b7bc7c.md)
- [非实时语音识别（Fun-ASR-Flash）iOS SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-ios-sd-ebb52f47ee469aa4.md)
- [非实时语音识别（Fun-ASR-Flash）HarmonyOS SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-harmon-eee2d6e9b92ea2cc.md)
- [Qwen-ASR](../../raw/_short/qwen-asr-non-realtime-api-da664e843d2e7fef.md)
- [Fun-ASR](../../raw/_short/fun-asr-recorded-speech-recognition-api-referenc-b0273c90bb44d4cc.md)
- [非实时语音识别（Qwen-ASR）API参考](../../raw/_short/qwen-asr-api-reference-6234af32190b8ba9.md)
- [Paraformer](../../raw/_short/paraformer-recorded-speech-recognition-api-refer-3f19f98cbb4ce26b.md)
- [Paraformer非实时语音识别HTTP API](../../raw/_short/paraformer-recorded-speech-recognition-restful-a-8b487acdee52d08d.md)
- [Paraformer非实时语音识别Python SDK](../../raw/_short/paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md)
- [Paraformer非实时语音识别Java SDK](../../raw/_short/paraformer-recorded-speech-recognition-java-sdk-915d733e99a3db9b.md)
- [Paraformer非实时语音识别Android SDK](../../raw/_short/paraformer-recorded-speech-recognition-android-s-13e83d144d148a4f.md)
- [Paraformer非实时语音识别iOS SDK](../../raw/_short/paraformer-recorded-speech-recognition-ios-sdk-137ff6eb176e867a.md)
- [最佳实践](../../raw/_short/paraformer-best-practices-b5bb2777c9abaf3c.md)
- [Paraformer非实时语音识别HarmonyOS SDK](../../raw/_short/paraformer-recorded-speech-recognition-harmonyos-71907f3ccc6c91c4.md)
- [语音合成](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference.md)
- [Qwen-Audio-TTS](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-qwen-audio-tts-api.md)
- [非实时语音合成Qwen-Audio-TTS HTTP API参考](../../raw/_short/qwen-audio-tts-http-api-ee05f9b13900b687.md)
- [非实时语音合成Qwen-Audio-TTS Java SDK参考](../../raw/_short/qwen-audio-tts-http-java-sdk-e802adc41b79b00c.md)
- [非实时语音合成Qwen-Audio-TTS Python SDK参考](../../raw/_short/qwen-audio-tts-http-python-sdk-5de04c79426618ab.md)
- [CosyVoice](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-cosyvoice-api.md)
- [非实时语音合成CosyVoice HTTP API参考](../../raw/_short/cosyvoice-tts-http-api-63e05680db50f996.md)
- [非实时语音合成CosyVoice Java SDK参考](../../raw/_short/cosyvoice-tts-java-sdk-b4e23dd3f27b95e0.md)
- [非实时语音合成CosyVoice Python SDK参考](../../raw/_short/cosyvoice-tts-python-sdk-01187ba238f52941.md)
- [其他模型](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-tts-other-models.md)
- [Qwen-TTS](../../raw/_short/qwen-tts-non-realtime-api-1c364eb278c0a2e2.md)
- [非实时语音合成（Qwen-TTS）API参考](../../raw/_short/qwen-tts-api-3dac64d546223453.md)
- [MiniMax同步语音合成API参考](../../raw/_short/minimax-synchronous-speech-synthesis-api-cddb40af595ff320.md)
- [音频生成 API参考](../../raw/model-api-reference/audio-api-directory/audio-generation-api.md)
- [音视频翻译](../../raw/model-api-reference/audio-api-directory/qwen3-livetranslate-flash-api.md)
- [MiniMax](../../raw/_short/minimax-speech-synthesis-9ac5812df734fd8c.md)
- [定制热词Java SDK参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-java-sdk.md)


