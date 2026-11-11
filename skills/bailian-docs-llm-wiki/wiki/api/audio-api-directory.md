# audio api directory

本目录汇总百炼平台提供的非实时音频处理能力，涵盖语音识别（ASR）、语音合成（TTS）、音频生成及音视频翻译四大类 API。所有接口均面向离线或长时音频文件场景设计，支持同步与异步调用模式，并提供多语言 SDK 封装。实时音频能力请参见 [Realtime API 概述](raw/model-api-reference/realtime-api-directory/realtime-api-overview.md)。

## 支持的模型/功能

- **语音识别（ASR）**：提供 Qwen-Audio-ASR、Qwen-Audio-ASR-Filetrans、Fun-ASR、Fun-ASR-Flash、Paraformer、Qwen-ASR 等多模型选择。其中：
  - `Qwen-Audio-ASR` 和 `Fun-ASR-Flash` 支持**同步 HTTP 调用 + SSE 流式返回**（需音频 ≥1 分钟），适用于低延迟短音频识别；
  - `Qwen-Audio-ASR-Filetrans`、`Fun-ASR`、`Paraformer` 等采用**异步“提交-轮询”模式**，专为长音频（如会议录音、播客）设计，任务提交后返回 `task_id`，需调用查询接口获取结果；
  - 所有 ASR 模型均支持定制热词，通过 [定制热词HTTP API参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-http-api.md) 创建、绑定并生效于指定模型。
- **语音合成（TTS）**：覆盖 `Qwen-Audio-TTS`、`CosyVoice`、`Qwen-TTS`、`MiniMax` 四大引擎，均支持 SSML/LaTeX 格式输入、多音色（含系统音色、复刻音色、设计音色）及多种音频格式（mp3/wav/pcm/opus）与采样率配置。
- **音频生成**：通过 `qwen-audio-3.1-tts-next` 等模型，支持文本提示词 + 参考音频联合驱动的高质量音频生成，适用于音效创作、AI 配音等场景。
- **音视频翻译**：由 `qwen3-livetranslate-flash-api` 提供，支持端到端音视频内容跨语言转译。

> **注意**：文档中 `Qwen-ASR` 的接入方式描述存在矛盾——[非实时语音识别（Qwen-ASR）API参考](../../raw/_short/qwen-asr-api-reference-6234af32190b8ba9.md) 明确指出“千问3-ASR-Flash-Filetrans 仅支持 DashScope 异步调用”，但同文档又列出其支持 OpenAI 兼容模式；而其他 ASR 模型（如 Fun-ASR-Flash）在 HTTP 接口定义中未体现 OpenAI 兼容路径。实际开发应以各模型独立文档为准，避免混用协议。

## 关键参数

- **通用认证与路由**：
  - `Authorization`: `Bearer <your_api_key>`，必须使用与业务空间地域匹配的 API Key（北京/新加坡 Key 不互通）；
  - `url` 域名：**强烈建议迁移至业务空间专属域名**，例如华北2（北京）使用 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，而非旧版 `dashscope.aliyuncs.com`（详见 [Qwen-Audio-ASR-Filetrans非实时语音识别HTTP API参考](../../raw/_short/qwen-audio-asr-filetrans-http-api-e0184f38f9d98459.md)）；
  - `X-DashScope-Async`: ASR 异步任务提交时**必须设置为 `enable`**，否则请求失败；
  - `X-DashScope-SSE`: TTS 或部分 ASR 接口启用流式响应时设为 `enable`。
- **ASR 核心参数**：
  - `model`: 必填，如 `"qwen-audio-3.1-asr-flash-filetrans"`；
  - `input.file_urls`: 异步模式下必填数组（单次仅支持 1 个 URL）；
  - `input.messages`: 同步模式下必填，含 `role: "user"` + `type: "input_audio"` 的音频消息，且必须置于 `messages` 数组末尾；
  - `parameters`: Paraformer 等模型要求显式传入空对象 `{}`（见 [Paraformer非实时语音识别HTTP API](../../raw/_short/paraformer-recorded-speech-recognition-restful-a-8b487acdee52d08d.md)）。
- **TTS 核心参数**：
  - `text`: 待合成文本，支持 SSML（需 `enable_ssml: true`）和 LaTeX；
  - `voice`: 音色 ID，可为系统音色、复刻音色或设计音色；
  - `format` / `sample_rate`: 控制输出音频编码与质量，默认 `mp3` / `22050`。

## 使用方式

- **HTTP 直调**：按接口文档构造 POST 请求，设置正确 `Content-Type` 与请求头，JSON body 包含 `model` 和 `input` 对象。异步任务需额外实现轮询逻辑（如定时 GET `/api/v1/tasks/{task_id}`）。
- **SDK 调用**：
  - Python：统一使用 `dashscope.Client` 实例的 `client.audio.asr.jobs`（ASR）、`client.audio.tts.http`（TTS）等资源入口；
  - Java：通过 `Transcription`（ASR）或 `HttpSpeechSynthesizer`（TTS）类封装调用；
  - 移动端（Android/iOS/HarmonyOS）：初始化 SDK 时传入 `url`、`apikey`、`service_mode: "1"` 等必要参数，再调用 `startFileTranscriber` 或 `nui_file_trans_start` 等方法。
- **流式处理**：对低首包延迟敏感场景，优先选用 `X-DashScope-SSE: enable` 的 HTTP 接口，或 SDK 中 `stream()` / `streamCall()` 方法，接收分片音频数据。

## 限制和注意事项

- **地域与域名兼容性**：新加坡地域**不支持定制热词功能**（见 [定制热词HTTP API参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-http-api.md)），且部分模型（如 Fun-ASR-Flash）的 HTTP 接口文档未明确标注新加坡支持状态，调用前需验证。
- **音频输入规范**：所有 ASR/TTS 接口均遵循统一 [音频规格](https://help.aliyun.com/zh/model-studio/asr-model#asr_audio_spec02)，包括格式（WAV/MP3/OPUS 等）、采样率、声道数、文件大小与时长上限，超限将直接报错。
- **异步任务生命周期**：ASR Filetrans 类任务结果 URL 有效期为 **24 小时**，过期后无法下载；Paraformer 等模型任务排队时间取决于队列负载，“尽力服务”，无确定性 SLA。
- **安全实践**：禁止硬编码 API Key，务必配置为环境变量；高风险场景（如第三方调用）应使用 [临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)（60秒有效期）替代长期 Key。

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
- [Qwen-Audio-ASR-Filetrans非实时语音识别iOS SDK](../../raw/_short/qwen-audio-asr-filetrans-ios-sdk-ac5cc79341721cdd.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别HarmonyOS SDK](../../raw/_short/qwen-audio-asr-filetrans-harmonyos-sdk-bca7ed5502ce3fcf.md)
- [定制热词](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words.md)
- [定制热词HTTP API参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-http-api.md)
- [定制热词Python SDK参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-python-sdk.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别Android SDK](../../raw/_short/qwen-audio-asr-filetrans-android-sdk-a3c0fbd842a710b1.md)
- [Fun-ASR](../../raw/_short/fun-asr-recorded-speech-recognition-api-referenc-b0273c90bb44d4cc.md)
- [Fun-ASR非实时语音识别HTTP API参考](../../raw/_short/fun-asr-recorded-speech-recognition-http-api-0e04e08da4894bf2.md)
- [Fun-ASR非实时语音识别Python SDK](../../raw/_short/funauidio-asr-recorded-speech-recognition-python-d69dda8f4675042c.md)
- [Fun-ASR非实时语音识别Java SDK](../../raw/_short/fun-asr-recorded-speech-recognition-java-sdk-b2ce5e0f37e9003f.md)
- [Fun-ASR非实时语音识别HarmonyOS SDK](../../raw/_short/fun-asr-recorded-speech-recognition-harmonyos-sd-f2337ad439819fc6.md)
- [Fun-ASR-Flash](../../raw/_short/non-real-time-speech-recognition-for-fun-asr-fla-650fa37d535f17b4.md)
- [非实时语音识别（Fun-ASR-Flash）HTTP API](../../raw/_short/fun-asr-flash-recorded-speech-recognition-http-a-7716e5d27dfd9a7b.md)
- [Fun-ASR非实时语音识别iOS SDK](../../raw/_short/fun-asr-recorded-speech-recognition-ios-sdk-e6f16b9236096238.md)
- [非实时语音识别（Fun-ASR-Flash）iOS SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-ios-sd-ebb52f47ee469aa4.md)
- [非实时语音识别（Fun-ASR-Flash）HarmonyOS SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-harmon-eee2d6e9b92ea2cc.md)
- [Qwen-ASR](../../raw/_short/qwen-asr-non-realtime-api-da664e843d2e7fef.md)
- [非实时语音识别（Qwen-ASR）API参考](../../raw/_short/qwen-asr-api-reference-6234af32190b8ba9.md)
- [Paraformer](../../raw/_short/paraformer-recorded-speech-recognition-api-refer-3f19f98cbb4ce26b.md)
- [Paraformer非实时语音识别HTTP API](../../raw/_short/paraformer-recorded-speech-recognition-restful-a-8b487acdee52d08d.md)
- [Paraformer非实时语音识别Python SDK](../../raw/_short/paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md)
- [Paraformer非实时语音识别Java SDK](../../raw/_short/paraformer-recorded-speech-recognition-java-sdk-915d733e99a3db9b.md)
- [Paraformer非实时语音识别Android SDK](../../raw/_short/paraformer-recorded-speech-recognition-android-s-13e83d144d148a4f.md)
- [Paraformer非实时语音识别HarmonyOS SDK](../../raw/_short/paraformer-recorded-speech-recognition-harmonyos-71907f3ccc6c91c4.md)
- [非实时语音识别（Fun-ASR-Flash）Android SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-androi-5c29202b31b7bc7c.md)
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
- [最佳实践](../../raw/_short/paraformer-best-practices-b5bb2777c9abaf3c.md)
- [MiniMax](../../raw/_short/minimax-speech-synthesis-9ac5812df734fd8c.md)
- [音频生成 API参考](../../raw/model-api-reference/audio-api-directory/audio-generation-api.md)
- [MiniMax同步语音合成API参考](../../raw/_short/minimax-synchronous-speech-synthesis-api-cddb40af595ff320.md)
- [音视频翻译](../../raw/model-api-reference/audio-api-directory/qwen3-livetranslate-flash-api.md)
- [Paraformer非实时语音识别iOS SDK](../../raw/_short/paraformer-recorded-speech-recognition-ios-sdk-137ff6eb176e867a.md)
- [定制热词Java SDK参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-java-sdk.md)
- [其他模型](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/non-realtime-asr-other-models.md)
- [Fun-ASR非实时语音识别Android SDK](../../raw/_short/fun-asr-recorded-speech-recognition-android-sdk-f828ab21cfa96d66.md)


