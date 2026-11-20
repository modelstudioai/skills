# audio api directory

本目录汇总百炼平台提供的非实时音频处理能力，涵盖语音识别（ASR）、语音合成（TTS）、音频生成和音视频翻译四大类 API。所有接口均面向离线或批量音频文件处理场景，支持同步与[异步调用](../concepts/asynchronous-invocation.md)模式，并提供多语言 SDK 封装。实时音频能力请参考 [Realtime API 概述](raw/model-api-reference/realtime-api-directory/realtime-api-overview.md)。

## 支持的模型/功能

- **语音识别（ASR）**：提供 Qwen-Audio-ASR、Qwen-Audio-ASR-Filetrans、Fun-ASR、Fun-ASR-Flash、Qwen-ASR 和 Paraformer 六大模型。其中 Qwen-Audio-ASR 适用于短音频流式识别；Qwen-Audio-ASR-Filetrans 和 Fun-ASR 等专为长音频文件转写设计，采用“提交-轮询”异步流程；Paraformer 支持音轨选择、语气词过滤等精细化控制 [原文标题](../../raw/_short/paraformer-recorded-speech-recognition-api-refer-3f19f98cbb4ce26b.md)。
- **语音合成（TTS）**：包含 Qwen-Audio-TTS 和 CosyVoice 两大引擎，均支持 SSML/LaTeX 输入、多音色（系统音色/复刻音色/设计音色）及多种音频格式（mp3/wav/opus 等）输出 [原文标题](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference.md)。
- **音频生成与音视频翻译**：分别由 [音频生成](../../raw/model-api-reference/audio-api-directory/audio-generation-api.md) 和 [Qwen3-LiveTranslate-Flash](../../raw/model-api-reference/audio-api-directory/qwen3-livetranslate-flash-api.md) 接口提供，文档中未展开细节，需单独查阅对应参考页。

> **注意**：Qwen-ASR 模型同时支持 OpenAI 兼容协议和 DashScope 协议，但千问3-ASR-Flash-Filetrans 仅支持 DashScope [异步调用](../concepts/asynchronous-invocation.md)，不兼容 OpenAI 模式 —— 此限制在 [非实时语音识别（Qwen-ASR）API参考](../../raw/_short/qwen-asr-api-reference-6234af32190b8ba9.md) 中明确说明，而部分 SDK 文档未强调该约束，开发者需以 HTTP API 文档为准。

## 关键参数

- **通用认证与路由**：所有接口均需 `Authorization: Bearer <your_api_key>` 请求头；服务地址统一使用业务空间专属域名（如 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但官方强烈建议迁移以获得更高稳定性与性能。
- **ASR 核心参数**：
  - `model`：必填，指定模型名（如 `qwen-audio-3.1-asr-flash-filetrans`）；
  - `input.file_urls`（Filetrans 类）或 `input.messages`（Flash 类）：必填，分别用于传入公网可访问音频 URL 列表或含 `input_audio` 的消息数组；
  - `X-DashScope-Async: enable`：Filetrans 类异步任务必需请求头；
  - `X-DashScope-SSE: enable`：启用流式响应（仅当音频 ≥1 分钟时生效）。
- **TTS 核心参数**：
  - `text`：必填，支持纯文本、SSML（需设 `enable_ssml=true`）或 LaTeX；
  - `voice`：必填，值为预置音色 ID 或自定义音色 ID；
  - `format` / `sample_rate`：可选，控制输出音频编码与采样率。

## 使用方式

- **HTTP 直调**：按接口文档构造 POST 请求，推荐使用异步模式处理长音频（如 Filetrans 类），避免超时；同步模式适用于 ≤1 分钟音频（如 Qwen-Audio-ASR Flash）。
- **SDK 集成**：各模型均提供 Python/Java/Node.js/Android/iOS/HarmonyOS 多端 SDK。例如：
  - Python：通过 `client.audio.asr.jobs.create()` 提交 Filetrans 任务，再用 `jobs.wait()` 同步阻塞等待结果；
  - Java：使用 `Transcription.asyncCall()` 提交 + `wait()` 查询；
  - 移动端 SDK（Android/iOS/HarmonyOS）：统一通过 `initialize` + `startFileTranscriber` + `onFileTransEventCallback` 三步完成调用。
- **上下文增强**：Qwen-Audio-ASR 和 Fun-ASR-Flash 支持在 `messages` 中传入 `input_text`（user）与 `text`（assistant）上下文对，最多各 5 条，总长度 ≤400 字符，用于提升专业术语识别准确率。

## 限制和注意事项

- **地域限制**：定制热词功能仅在北京地域可用，新加坡子业务空间暂不支持 [原文标题](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words.md)。
- **音频规格**：所有 ASR/TTS 接口对输入音频格式、大小、时长有统一要求，详见 [音频规格](https://help.aliyun.com/zh/model-studio/asr-model#asr_audio_spec02)（外部链接），未满足将直接报错。
- **异步任务时效性**：Filetrans 类任务结果及下载 URL 有效期为 24 小时，超时后无法查询或下载。
- **SDK 地域配置差异**：Python SDK 通过 `Client(region=...)` 设置地域；Java SDK 需全局修改 `Constants.baseHttpApiUrl`；移动端 SDK 则在初始化 `parameters.url` 中显式指定，三者配置方式不一致，需按 SDK 文档严格操作。
- **安全实践**：生产环境务必使用环境变量管理 API Key；高敏感场景推荐使用 [临时 API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)，其默认有效期仅 60 秒，可显著降低泄露风险。

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
- [Qwen-Audio-ASR-Filetrans Node.js SDK](../../raw/_short/qwen-audio-asr-filetrans-nodejs-sdk-6457111def74455c.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别iOS SDK](../../raw/_short/qwen-audio-asr-filetrans-ios-sdk-ac5cc79341721cdd.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别HarmonyOS SDK](../../raw/_short/qwen-audio-asr-filetrans-harmonyos-sdk-bca7ed5502ce3fcf.md)
- [定制热词](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words.md)
- [定制热词HTTP API参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-http-api.md)
- [定制热词Python SDK参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-python-sdk.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别Java SDK](../../raw/_short/qwen-audio-asr-filetrans-java-sdk-e33c81cb99967d86.md)
- [其他模型](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/non-realtime-asr-other-models.md)
- [定制热词Java SDK参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-java-sdk.md)
- [Fun-ASR非实时语音识别HTTP API参考](../../raw/_short/fun-asr-recorded-speech-recognition-http-api-0e04e08da4894bf2.md)
- [Fun-ASR](../../raw/_short/fun-asr-recorded-speech-recognition-api-referenc-b0273c90bb44d4cc.md)
- [Fun-ASR非实时语音识别Python SDK](../../raw/_short/funauidio-asr-recorded-speech-recognition-python-d69dda8f4675042c.md)
- [Fun-ASR非实时语音识别Java SDK](../../raw/_short/fun-asr-recorded-speech-recognition-java-sdk-b2ce5e0f37e9003f.md)
- [Fun-ASR非实时语音识别iOS SDK](../../raw/_short/fun-asr-recorded-speech-recognition-ios-sdk-e6f16b9236096238.md)
- [Fun-ASR非实时语音识别Android SDK](../../raw/_short/fun-asr-recorded-speech-recognition-android-sdk-f828ab21cfa96d66.md)
- [Fun-ASR非实时语音识别HarmonyOS SDK](../../raw/_short/fun-asr-recorded-speech-recognition-harmonyos-sd-f2337ad439819fc6.md)
- [Fun-ASR-Flash](../../raw/_short/non-real-time-speech-recognition-for-fun-asr-fla-650fa37d535f17b4.md)
- [非实时语音识别（Fun-ASR-Flash）Android SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-androi-5c29202b31b7bc7c.md)
- [非实时语音识别（Fun-ASR-Flash）HTTP API](../../raw/_short/fun-asr-flash-recorded-speech-recognition-http-a-7716e5d27dfd9a7b.md)
- [非实时语音识别（Fun-ASR-Flash）HarmonyOS SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-harmon-eee2d6e9b92ea2cc.md)
- [非实时语音识别（Fun-ASR-Flash）iOS SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-ios-sd-ebb52f47ee469aa4.md)
- [Qwen-ASR](../../raw/_short/qwen-asr-non-realtime-api-da664e843d2e7fef.md)
- [Paraformer](../../raw/_short/paraformer-recorded-speech-recognition-api-refer-3f19f98cbb4ce26b.md)
- [非实时语音识别（Qwen-ASR）API参考](../../raw/_short/qwen-asr-api-reference-6234af32190b8ba9.md)
- [Paraformer非实时语音识别HTTP API](../../raw/_short/paraformer-recorded-speech-recognition-restful-a-8b487acdee52d08d.md)
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
- [CosyVoice](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-cosyvoice-api.md)
- [非实时语音合成CosyVoice HTTP API参考](../../raw/_short/cosyvoice-tts-http-api-63e05680db50f996.md)
- [非实时语音合成CosyVoice Java SDK参考](../../raw/_short/cosyvoice-tts-java-sdk-b4e23dd3f27b95e0.md)
- [非实时语音合成CosyVoice Python SDK参考](../../raw/_short/cosyvoice-tts-python-sdk-01187ba238f52941.md)
- [其他模型](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-tts-other-models.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别Android SDK](../../raw/_short/qwen-audio-asr-filetrans-android-sdk-a3c0fbd842a710b1.md)
- [非实时语音合成（Qwen-TTS）API参考](../../raw/_short/qwen-tts-api-3dac64d546223453.md)
- [Paraformer非实时语音识别Python SDK](../../raw/_short/paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md)
- [MiniMax同步语音合成API参考](../../raw/_short/minimax-synchronous-speech-synthesis-api-cddb40af595ff320.md)
- [MiniMax](../../raw/_short/minimax-speech-synthesis-9ac5812df734fd8c.md)
- [音频生成 API参考](../../raw/model-api-reference/audio-api-directory/audio-generation-api.md)
- [Qwen-TTS](../../raw/_short/qwen-tts-non-realtime-api-1c364eb278c0a2e2.md)
- [音视频翻译](../../raw/model-api-reference/audio-api-directory/qwen3-livetranslate-flash-api.md)


