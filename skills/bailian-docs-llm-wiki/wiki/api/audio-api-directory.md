# audio api directory

本目录提供非实时音频处理能力的统一接入入口，涵盖语音识别（ASR）、语音合成（TTS）、音频生成和音视频翻译四大核心功能。所有接口均面向离线或长时音频文件设计，支持同步与异步两种调用模式，并兼容 HTTP API 与多语言 SDK。实时音频能力请参见 [Realtime API 概述](raw/model-api-reference/realtime-api-directory/realtime-api-overview.md)。

## 支持的模型/功能

- **语音识别（ASR）**：提供 Qwen-Audio-ASR、Qwen-Audio-ASR-Filetrans、Fun-ASR、Fun-ASR-Flash、Qwen-ASR 和 Paraformer 六类模型。其中 Qwen-Audio-ASR 适用于短音频流式识别；Qwen-Audio-ASR-Filetrans、Fun-ASR 及 Paraformer 专为长音频异步转写优化；Fun-ASR-Flash 和 Qwen-ASR 支持上下文增强与 OpenAI 兼容协议。[语音识别](raw/model-api-reference/audio-api-directory/speech-recognition-api-reference.md) 文档详细列出了各模型能力边界与适用场景。
- **语音合成（TTS）**：支持 Qwen-Audio-TTS 和 CosyVoice 两大模型体系，均提供系统音色、声音复刻音色及声音设计音色三类音色来源。[语音合成](raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference.md) 文档说明了 SSML/LaTeX 输入支持、格式与采样率配置等关键能力。
- **音频生成与音视频翻译**：分别由 [音频生成](raw/model-api-reference/audio-api-directory/audio-generation-api.md) 和 [Qwen3-LiveTranslate-Flash](raw/model-api-reference/audio-api-directory/qwen3-livetranslate-flash-api.md) 接口提供，当前以 HTTP API 形式开放。

> **注意**：Paraformer 模型在文档 36、37、38 中明确要求使用 `X-DashScope-Async: enable` 头提交任务，但文档 42（最佳实践）未提及该强制要求，且未说明其是否适用于预处理后的音频。实际集成时请以 [Paraformer非实时语音识别HTTP API](raw/_short/paraformer-recorded-speech-recognition-restful-a-8b487acdee52d08d.md) 的规范为准。

## 关键参数

- **通用认证与路由**：所有接口均需 `Authorization: Bearer <api_key>` 请求头；服务地址统一采用业务空间专属域名 `https://{WorkspaceId}.{region}.maas.aliyuncs.com`，需将 `{WorkspaceId}` 替换为真实值（[Workspace ID 获取方式](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)）。旧域名 `dashscope.aliyuncs.com` 已不推荐使用。
- **ASR 异步任务控制**：Qwen-Audio-ASR-Filetrans、Fun-ASR、Paraformer 等异步模型必须在提交任务请求头中设置 `X-DashScope-Async: enable`，否则任务创建失败（见 [Qwen-Audio-ASR-Filetrans非实时语音识别HTTP API参考](raw/_short/qwen-audio-asr-filetrans-http-api-e0184f38f9d98459.md)）。
- **TTS 核心输入**：`text`（必填，支持纯文本、SSML 或 LaTeX）、`voice`（必填，音色ID）、`model`（必填，如 `qwen-audio-tts` 或 `cosyvoice-v3.5-plus`）、`format`（可选，默认 `mp3`）和 `sample_rate`（可选，默认 `22050`）。
- **热词定制**：通过独立的 [定制热词HTTP API参考](raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-http-api.md) 管理，需指定 `target_model` 与识别模型严格匹配，且新加坡地域暂不支持。

## 使用方式

- **HTTP 调用**：
  - 同步接口（如 Qwen-Audio-ASR）：单次 POST 请求，响应体直接返回结果。
  - 异步接口（如 Qwen-Audio-ASR-Filetrans）：分两步——先 POST 提交任务获取 `task_id`，再 GET `https://.../api/v1/tasks/{task_id}` 轮询结果。
- **SDK 集成**：
  - Python：`dashscope.Client().audio.asr.jobs.create()`（异步）或 `.audio.tts.http.synthesize()`（同步）。
  - Java：`Transcription.asyncCall()` 或 `HttpSpeechSynthesizer.call()`。
  - 移动端（Android/iOS/HarmonyOS）：统一通过 `initialize` + `startFileTranscriber` / `nui_file_trans_start` 流程启动，支持 `async_request: true/false` 切换同步/异步模式。
- **客户端参数配置**：各 SDK 均需在初始化时传入 `url`（含 WorkspaceId）、`apikey`、`service_mode: "1"`（非实时标识）和 `device_id`（日志追踪用）。

## 限制和注意事项

- **地域与功能限制**：定制热词功能仅在北京地域可用，新加坡地域明确不支持（见 [定制热词HTTP API参考](raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-http-api.md)）；CosyVoice 和 Qwen-Audio-TTS 的 Java/Python SDK 当前仅限华北2（北京）地域（文档 46、47、49、50 多次强调）。
- **音频输入规范**：所有 ASR/TTS 接口对音频格式、大小、时长有统一要求，详见 [音频规格](https://help.aliyun.com/zh/model-studio/asr-model#asr_audio_spec02)。Paraformer 强烈建议对视频文件预处理为 OPUS 格式以提升效率（见 [最佳实践](raw/_short/paraformer-best-practices-b5bb2777c9abaf3c.md)）。
- **安全实践**：API Key 必须配置于环境变量而非硬编码；高敏感场景应优先使用 [临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)（有效期60秒），尤其在移动端 SDK 中（文档 7、15、35、38、40、41 均明确建议）。
- **异步任务生命周期**：Qwen-Audio-ASR-Filetrans、Fun-ASR 等异步任务的结果 URL 有效期为 24 小时，超时后无法下载（见文档 10、11、39）。

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
- [Fun-ASR非实时语音识别HTTP API参考](../../raw/_short/fun-asr-recorded-speech-recognition-http-api-0e04e08da4894bf2.md)
- [Fun-ASR非实时语音识别Java SDK](../../raw/_short/fun-asr-recorded-speech-recognition-java-sdk-b2ce5e0f37e9003f.md)
- [Fun-ASR](../../raw/_short/fun-asr-recorded-speech-recognition-api-referenc-b0273c90bb44d4cc.md)
- [Fun-ASR非实时语音识别iOS SDK](../../raw/_short/fun-asr-recorded-speech-recognition-ios-sdk-e6f16b9236096238.md)
- [Fun-ASR非实时语音识别Android SDK](../../raw/_short/fun-asr-recorded-speech-recognition-android-sdk-f828ab21cfa96d66.md)
- [Fun-ASR非实时语音识别HarmonyOS SDK](../../raw/_short/fun-asr-recorded-speech-recognition-harmonyos-sd-f2337ad439819fc6.md)
- [Fun-ASR-Flash](../../raw/_short/non-real-time-speech-recognition-for-fun-asr-fla-650fa37d535f17b4.md)
- [非实时语音识别（Fun-ASR-Flash）Android SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-androi-5c29202b31b7bc7c.md)
- [非实时语音识别（Fun-ASR-Flash）HTTP API](../../raw/_short/fun-asr-flash-recorded-speech-recognition-http-a-7716e5d27dfd9a7b.md)
- [非实时语音识别（Fun-ASR-Flash）iOS SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-ios-sd-ebb52f47ee469aa4.md)
- [非实时语音识别（Fun-ASR-Flash）HarmonyOS SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-harmon-eee2d6e9b92ea2cc.md)
- [Qwen-ASR](../../raw/_short/qwen-asr-non-realtime-api-da664e843d2e7fef.md)
- [非实时语音识别（Qwen-ASR）API参考](../../raw/_short/qwen-asr-api-reference-6234af32190b8ba9.md)
- [Paraformer](../../raw/_short/paraformer-recorded-speech-recognition-api-refer-3f19f98cbb4ce26b.md)
- [Paraformer非实时语音识别Python SDK](../../raw/_short/paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md)
- [Paraformer非实时语音识别HTTP API](../../raw/_short/paraformer-recorded-speech-recognition-restful-a-8b487acdee52d08d.md)
- [Paraformer非实时语音识别Java SDK](../../raw/_short/paraformer-recorded-speech-recognition-java-sdk-915d733e99a3db9b.md)
- [Paraformer非实时语音识别Android SDK](../../raw/_short/paraformer-recorded-speech-recognition-android-s-13e83d144d148a4f.md)
- [Fun-ASR非实时语音识别Python SDK](../../raw/_short/funauidio-asr-recorded-speech-recognition-python-d69dda8f4675042c.md)
- [Paraformer非实时语音识别HarmonyOS SDK](../../raw/_short/paraformer-recorded-speech-recognition-harmonyos-71907f3ccc6c91c4.md)
- [Paraformer非实时语音识别iOS SDK](../../raw/_short/paraformer-recorded-speech-recognition-ios-sdk-137ff6eb176e867a.md)
- [最佳实践](../../raw/_short/paraformer-best-practices-b5bb2777c9abaf3c.md)
- [语音合成](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference.md)
- [Qwen-Audio-TTS](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-qwen-audio-tts-api.md)
- [非实时语音合成Qwen-Audio-TTS HTTP API参考](../../raw/_short/qwen-audio-tts-http-api-ee05f9b13900b687.md)
- [非实时语音合成Qwen-Audio-TTS Python SDK参考](../../raw/_short/qwen-audio-tts-http-python-sdk-5de04c79426618ab.md)
- [非实时语音合成Qwen-Audio-TTS Java SDK参考](../../raw/_short/qwen-audio-tts-http-java-sdk-e802adc41b79b00c.md)
- [CosyVoice](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-cosyvoice-api.md)
- [非实时语音合成CosyVoice HTTP API参考](../../raw/_short/cosyvoice-tts-http-api-63e05680db50f996.md)
- [非实时语音合成CosyVoice Java SDK参考](../../raw/_short/cosyvoice-tts-java-sdk-b4e23dd3f27b95e0.md)
- [非实时语音合成CosyVoice Python SDK参考](../../raw/_short/cosyvoice-tts-python-sdk-01187ba238f52941.md)
- [非实时语音合成（Qwen-TTS）API参考](../../raw/_short/qwen-tts-api-3dac64d546223453.md)
- [Qwen-TTS](../../raw/_short/qwen-tts-non-realtime-api-1c364eb278c0a2e2.md)
- [其他模型](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-tts-other-models.md)
- [音频生成 API参考](../../raw/model-api-reference/audio-api-directory/audio-generation-api.md)
- [MiniMax同步语音合成API参考](../../raw/_short/minimax-synchronous-speech-synthesis-api-cddb40af595ff320.md)
- [MiniMax](../../raw/_short/minimax-speech-synthesis-9ac5812df734fd8c.md)
- [音视频翻译](../../raw/model-api-reference/audio-api-directory/qwen3-livetranslate-flash-api.md)


