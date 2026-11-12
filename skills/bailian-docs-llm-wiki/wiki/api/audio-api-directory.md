# audio api directory

本目录汇总百炼平台提供的非实时音频处理能力，涵盖语音识别（ASR）、语音合成（TTS）、音频生成和音视频翻译四大类 API。所有接口均面向离线或批量音频文件处理场景，支持同步与异步调用模式，并提供多语言 SDK 封装。实时音频能力请参见 [Realtime API 概述](raw/model-api-reference/realtime-api-directory/realtime-api-overview.md)。

## 支持的模型/功能

- **语音识别（ASR）**：提供 Qwen-Audio-ASR、Qwen-Audio-ASR-Filetrans、Fun-ASR、Fun-ASR-Flash、Qwen-ASR 和 Paraformer 六大模型。其中 Qwen-Audio-ASR 与 Fun-ASR-Flash 支持上下文增强和 SSE 流式返回；Qwen-Audio-ASR-Filetrans、Fun-ASR、Paraformer 采用“提交-轮询”异步范式，适用于长音频（>10 分钟）；Qwen-ASR 同时支持 OpenAI 兼容协议与 DashScope 协议 [非实时语音识别（Qwen-ASR）API参考](../../raw/_short/qwen-asr-api-reference-6234af32190b8ba9.md)。
- **语音合成（TTS）**：提供 Qwen-Audio-TTS 和 CosyVoice 两大模型系列，均支持 SSML/LaTeX 输入、多音色（系统音色/复刻音色/设计音色）、多种音频格式（mp3/wav/opus/pcm）及采样率配置 [非实时语音合成Qwen-Audio-TTS HTTP API参考](../../raw/_short/qwen-audio-tts-http-api-ee05f9b13900b687.md)。
- **音频生成与音视频翻译**：分别由 [音频生成](raw/model-api-reference/audio-api-directory/audio-generation-api.md) 和 [音视频翻译](raw/model-api-reference/audio-api-directory/qwen3-livetranslate-flash-api.md) 文档定义，本文档不展开细节。

> **注意**：Paraformer 在文档 35–40 中明确要求仅支持华北2（北京）地域，但文档 37（Android SDK）示例 URL 仍使用 `wss://dashscope.aliyuncs.com/api-ws/v1/inference`（旧域名），而文档 40（HarmonyOS SDK）已更新为 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/...`。建议统一采用业务空间专属域名，避免兼容性风险。

## 关键参数

- **通用认证与路由**：所有 HTTP 接口均需 `Authorization: Bearer <api_key>` 请求头；`Content-Type: application/json` 为必填；服务地址必须替换 `{WorkspaceId}` 并匹配地域（如 `cn-beijing` 或 `ap-southeast-1`）。强烈建议迁移至业务空间专属域名（如 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），详见各文档中的“重要”提示。
- **ASR 异步任务**：`X-DashScope-Async: enable` 为提交任务必需头；`file_urls`（数组）为必填输入字段，指向公网可访问的音频资源；任务结果有效期为 24 小时。
- **ASR 同步/流式识别**：`X-DashScope-SSE: enable` 控制 SSE 流式返回，但仅当音频时长 ≥1 分钟时生效（[非实时语音识别（Qwen-Audio-ASR）HTTP API](../../raw/_short/qwen-audio-asr-http-api-90b9d62787e911f4.md)）。
- **TTS 核心参数**：`text`（必填，支持 SSML/LaTeX）、`voice`（必填，音色 ID）、`model`（必填）、`format`（默认 mp3）、`sample_rate`（默认 22050 Hz）；流式调用需额外设置 `X-DashScope-SSE: enable`。
- **定制热词**：通过独立接口管理，`target_model` 必须与后续 ASR 调用的 `model` 完全一致；新加坡地域暂不支持该功能 [定制热词HTTP API参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-http-api.md)。

## 使用方式

- **HTTP 直调**：按接口文档构造 POST/GET 请求，注意区分同步（单次请求返回）与异步（提交+轮询）流程。ASR 异步任务需轮询 `GET /api/v1/tasks/{task_id}`；TTS 流式调用需处理 SSE EventStream 响应。
- **SDK 集成**：
  - Python：使用 `dashscope.Client().audio.asr.jobs.create()`（ASR 异步）、`client.audio.tts.http.synthesize()`（TTS 非流式）等高层封装；
  - Java：通过 `Transcription.asyncCall()`（ASR）或 `HttpSpeechSynthesizer.call()`（TTS）调用；
  - 移动端（Android/iOS/HarmonyOS）：初始化 SDK 时传入 `url`、`apikey`、`service_mode="1"` 等 JSON 参数，再调用 `startFileTranscriber` 或 `nui_file_trans_start`。
- **跨平台一致性**：所有 SDK 均遵循相同参数语义（如 `file_urls`、`voice`、`model`），便于多端代码复用。

## 限制和注意事项

- **地域与功能约束**：定制热词功能在新加坡地域不可用；Paraformer 仅支持华北2（北京）地域；Qwen-ASR 的 OpenAI 兼容模式在美国地域不可用。
- **音频规格**：所有 ASR/TTS 接口对输入音频格式、大小、时长有统一要求，详见 [音频规格](https://help.aliyun.com/zh/model-studio/asr-model#asr_audio_spec02)（外部链接），开发者需预处理（如用 ffmpeg 提取音轨并转为 opus）以提升效率 [最佳实践](raw/_short/paraformer-best-practices-b5bb2777c9abaf3c.md)。
- **安全实践**：禁止硬编码 API Key，务必配置到环境变量；高风险场景（如第三方调用）应使用时效短（60秒）的临时 API Key [生成临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。
- **错误处理**：异步任务失败后，`task_id` 无法重试，需重新提交；TTS 流式调用中断需重连并重新发起请求。

## 来源文档

- [音频（非实时）](../../raw/model-api-reference/audio-api-directory/audio-api-references.md)
- [语音识别](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference.md)
- [Qwen-Audio-ASR](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/qwen-audio-asr-api.md)
- [非实时语音识别（Qwen-Audio-ASR）HTTP API](../../raw/_short/qwen-audio-asr-http-api-90b9d62787e911f4.md)
- [非实时语音识别（Qwen-Audio-ASR）Android SDK](../../raw/_short/qwen-audio-asr-android-sdk-1e97f1d8b5e9135c.md)
- [非实时语音识别（Qwen-Audio-ASR）iOS SDK](../../raw/_short/qwen-audio-asr-ios-sdk-fc08c802d4ff7f08.md)
- [非实时语音识别（Qwen-Audio-ASR）HarmonyOS SDK](../../raw/_short/qwen-audio-asr-harmonyos-sdk-b1335f47a12054cd.md)
- [Qwen-Audio-ASR-Filetrans](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/qwen-audio-asr-filetrans-api.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别HTTP API参考](../../raw/_short/qwen-audio-asr-filetrans-http-api-e0184f38f9d98459.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别Python SDK](../../raw/_short/qwen-audio-asr-filetrans-python-sdk-e244defb9b1288ee.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别Java SDK](../../raw/_short/qwen-audio-asr-filetrans-java-sdk-e33c81cb99967d86.md)
- [Qwen-Audio-ASR-Filetrans Node.js SDK](../../raw/_short/qwen-audio-asr-filetrans-nodejs-sdk-6457111def74455c.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别Android SDK](../../raw/_short/qwen-audio-asr-filetrans-android-sdk-a3c0fbd842a710b1.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别iOS SDK](../../raw/_short/qwen-audio-asr-filetrans-ios-sdk-ac5cc79341721cdd.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别HarmonyOS SDK](../../raw/_short/qwen-audio-asr-filetrans-harmonyos-sdk-bca7ed5502ce3fcf.md)
- [定制热词](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words.md)
- [定制热词HTTP API参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-http-api.md)
- [定制热词Python SDK参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-python-sdk.md)
- [定制热词Java SDK参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-java-sdk.md)
- [其他模型](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/non-realtime-asr-other-models.md)
- [Fun-ASR](../../raw/_short/fun-asr-recorded-speech-recognition-api-referenc-b0273c90bb44d4cc.md)
- [Fun-ASR非实时语音识别HTTP API参考](../../raw/_short/fun-asr-recorded-speech-recognition-http-api-0e04e08da4894bf2.md)
- [Fun-ASR非实时语音识别Python SDK](../../raw/_short/funauidio-asr-recorded-speech-recognition-python-d69dda8f4675042c.md)
- [Fun-ASR非实时语音识别Java SDK](../../raw/_short/fun-asr-recorded-speech-recognition-java-sdk-b2ce5e0f37e9003f.md)
- [Fun-ASR非实时语音识别Android SDK](../../raw/_short/fun-asr-recorded-speech-recognition-android-sdk-f828ab21cfa96d66.md)
- [Fun-ASR非实时语音识别iOS SDK](../../raw/_short/fun-asr-recorded-speech-recognition-ios-sdk-e6f16b9236096238.md)
- [Fun-ASR非实时语音识别HarmonyOS SDK](../../raw/_short/fun-asr-recorded-speech-recognition-harmonyos-sd-f2337ad439819fc6.md)
- [Fun-ASR-Flash](../../raw/_short/non-real-time-speech-recognition-for-fun-asr-fla-650fa37d535f17b4.md)
- [非实时语音识别（Fun-ASR-Flash）Android SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-androi-5c29202b31b7bc7c.md)
- [非实时语音识别（Fun-ASR-Flash）HTTP API](../../raw/_short/fun-asr-flash-recorded-speech-recognition-http-a-7716e5d27dfd9a7b.md)
- [非实时语音识别（Fun-ASR-Flash）HarmonyOS SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-harmon-eee2d6e9b92ea2cc.md)
- [Qwen-ASR](../../raw/_short/qwen-asr-non-realtime-api-da664e843d2e7fef.md)
- [非实时语音识别（Qwen-ASR）API参考](../../raw/_short/qwen-asr-api-reference-6234af32190b8ba9.md)
- [Paraformer](../../raw/_short/paraformer-recorded-speech-recognition-api-refer-3f19f98cbb4ce26b.md)
- [Paraformer非实时语音识别HTTP API](../../raw/_short/paraformer-recorded-speech-recognition-restful-a-8b487acdee52d08d.md)
- [Paraformer非实时语音识别Python SDK](../../raw/_short/paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md)
- [Paraformer非实时语音识别Android SDK](../../raw/_short/paraformer-recorded-speech-recognition-android-s-13e83d144d148a4f.md)
- [Paraformer非实时语音识别Java SDK](../../raw/_short/paraformer-recorded-speech-recognition-java-sdk-915d733e99a3db9b.md)
- [Paraformer非实时语音识别iOS SDK](../../raw/_short/paraformer-recorded-speech-recognition-ios-sdk-137ff6eb176e867a.md)
- [Paraformer非实时语音识别HarmonyOS SDK](../../raw/_short/paraformer-recorded-speech-recognition-harmonyos-71907f3ccc6c91c4.md)
- [最佳实践](../../raw/_short/paraformer-best-practices-b5bb2777c9abaf3c.md)
- [语音合成](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference.md)
- [Qwen-Audio-TTS](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-qwen-audio-tts-api.md)
- [非实时语音合成Qwen-Audio-TTS HTTP API参考](../../raw/_short/qwen-audio-tts-http-api-ee05f9b13900b687.md)
- [非实时语音合成Qwen-Audio-TTS Java SDK参考](../../raw/_short/qwen-audio-tts-http-java-sdk-e802adc41b79b00c.md)
- [非实时语音合成Qwen-Audio-TTS Python SDK参考](../../raw/_short/qwen-audio-tts-http-python-sdk-5de04c79426618ab.md)
- [CosyVoice](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-cosyvoice-api.md)
- [非实时语音合成CosyVoice Java SDK参考](../../raw/_short/cosyvoice-tts-java-sdk-b4e23dd3f27b95e0.md)
- [非实时语音合成CosyVoice HTTP API参考](../../raw/_short/cosyvoice-tts-http-api-63e05680db50f996.md)
- [非实时语音合成CosyVoice Python SDK参考](../../raw/_short/cosyvoice-tts-python-sdk-01187ba238f52941.md)
- [其他模型](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-tts-other-models.md)
- [Qwen-TTS](../../raw/_short/qwen-tts-non-realtime-api-1c364eb278c0a2e2.md)
- [非实时语音识别（Fun-ASR-Flash）iOS SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-ios-sd-ebb52f47ee469aa4.md)
- [非实时语音合成（Qwen-TTS）API参考](../../raw/_short/qwen-tts-api-3dac64d546223453.md)
- [MiniMax](../../raw/_short/minimax-speech-synthesis-9ac5812df734fd8c.md)
- [MiniMax同步语音合成API参考](../../raw/_short/minimax-synchronous-speech-synthesis-api-cddb40af595ff320.md)
- [音频生成 API参考](../../raw/model-api-reference/audio-api-directory/audio-generation-api.md)
- [音视频翻译](../../raw/model-api-reference/audio-api-directory/qwen3-livetranslate-flash-api.md)


