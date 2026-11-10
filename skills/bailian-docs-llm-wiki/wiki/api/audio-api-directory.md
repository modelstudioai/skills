# audio api directory

本目录提供非实时音频处理能力的统一入口，涵盖语音识别（ASR）、语音合成（TTS）、音频生成和音视频翻译四大核心功能。所有接口均基于统一的多模态推理服务框架，支持同步、异步及流式调用模式，并与百炼业务空间（Workspace）深度集成。实时音频能力请参见 [Realtime API 概述](raw/model-api-reference/realtime-api-directory/realtime-api-overview.md)。

## 支持的模型/功能

- **语音识别（ASR）**：提供多模型选择，包括 `qwen-audio-3.1-asr-flash`（低延迟流式）、`qwen-audio-3.1-asr-flash-filetrans`（长文件异步转写）、`fun-asr`、`fun-asr-flash`、`qwen-asr` 和 `paraformer-v2`。其中 `Qwen-Audio-ASR` 和 `Qwen-Audio-ASR-Filetrans` 是主力推荐模型，前者适用于短音频实时响应场景，后者专为长音频（>5分钟）异步批量处理设计。  
- **语音合成（TTS）**：支持 `qwen-audio-tts` 和 `cosyvoice` 两大系列，覆盖通用播报、情感化表达、数学公式朗读（LaTeX/SSML）等场景。`cosyvoice` 系列提供 `v3.5-plus`、`v3.5-flash` 等多个版本，侧重自然度与实时性平衡。  
- **音频生成与音视频翻译**：详见 [音频生成](raw/model-api-reference/audio-api-directory/audio-generation-api.md) 和 [Qwen3-LiveTranslate-Flash](raw/model-api-reference/audio-api-directory/qwen3-livetranslate-flash-api.md) 文档。  
- **增强能力**：支持定制热词（[定制热词](raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words.md)），用于提升专业领域词汇识别准确率；上下文增强（如 `qwen-audio-asr-flash` 的 `messages` 中嵌入 `input_text`）可优化连续对话识别效果。

## 关键参数

- **通用认证与路由**：所有 HTTP 接口均需 `Authorization: Bearer <api_key>` 请求头；必须指定业务空间专属域名（如 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名 `dashscope.aliyuncs.com` 已不推荐使用。  
- **ASR [异步任务](../concepts/asynchronous-task.md)**：提交接口需携带 `X-DashScope-Async: enable` 头；任务 ID 通过 `POST /api/v1/services/audio/asr/transcription` 返回，结果通过 `GET /api/v1/tasks/{task_id}` 轮询获取。  
- **TTS 流式控制**：启用流式返回需设置 `X-DashScope-SSE: enable` 请求头（HTTP）或 `stream=True` 参数（SDK）。  
- **输入格式**：ASR 支持上传音频 URL（`file_urls` 数组）或 Base64 内联数据；TTS `text` 字段支持纯文本、SSML（需 `enable_ssml=true`）及 LaTeX 格式。  
- **音色与编码**：TTS 必须指定 `voice`（系统音色、复刻音色或设计音色）和 `format`（默认 `mp3`）；`sample_rate` 取值范围为 `8000–48000`，但 `opus` 格式仅支持 `8000` 或 `16000`（[非实时语音合成CosyVoice HTTP API参考](../../raw/_short/cosyvoice-tts-http-api-63e05680db50f996.md)）。

## 使用方式

- **HTTP 直接调用**：适用于后端服务集成。ASR 同步调用（如 `qwen-audio-asr-flash`）使用 `/api/v1/services/aigc/multimodal-generation/generation`；ASR/TTS 异步调用统一使用 `/api/v1/services/audio/{asr|tts}/...` 路径。  
- **SDK 集成**：官方提供 Python、Java、Android、iOS、HarmonyOS 多语言 SDK。Python SDK 统一通过 `client.audio.asr.jobs.create()`（ASR）或 `client.audio.tts.http.synthesize()`（TTS）发起请求；Java SDK 对应 `Transcription.asyncCall()` 或 `HttpSpeechSynthesizer.call()`。  
- **异步工作流**：对长音频（>10分钟），强烈推荐 `Filetrans` 类模型（如 `qwen-audio-3.1-asr-flash-filetrans`），其采用“提交-轮询”模式，避免连接超时。任务结果有效期为 24 小时（[Qwen-Audio-ASR-Filetrans非实时语音识别Python SDK](../../raw/_short/qwen-audio-asr-filetrans-python-sdk-e244defb9b1288ee.md)）。  
- **客户端部署**：移动端（Android/iOS/HarmonyOS）SDK 均需在初始化时传入 `url`（含 WorkspaceId）、`apikey` 和 `service_mode="1"`；HarmonyOS SDK 明确要求使用临时 API Key 以提升安全性（[非实时语音识别（Qwen-Audio-ASR）HarmonyOS SDK](../../raw/_short/qwen-audio-asr-harmonyos-sdk-b1335f47a12054cd.md)）。

## 限制和注意事项

- **地域与功能约束**：定制热词功能**不支持新加坡地域**子业务空间（[定制热词HTTP API参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-http-api.md)）；`cosyvoice` 和 `qwen-audio-tts` 的 Java/Python SDK 当前**仅限华北2（北京）地域**可用（[非实时语音合成Qwen-Audio-TTS Java SDK参考](../../raw/_short/qwen-audio-tts-http-java-sdk-e802adc41b79b00c.md)）。  
- **模型兼容性差异**：`fun-asr` 和 `paraformer` 的异步提交接口要求 `parameters` 字段**即使为空也必须显式传入 `{}`**，否则识别失败（[Fun-ASR非实时语音识别HTTP API参考](../../raw/_short/fun-asr-recorded-speech-recognition-http-api-0e04e08da4894bf2.md)）；而 `qwen-audio-asr-flash` 的同步接口无此要求。  
- > **注意**：`paraformer` Android/iOS SDK 的默认服务地址为 `wss://dashscope.aliyuncs.com/api-ws/v1/inference`（[Paraformer非实时语音识别Android SDK](../../raw/_short/paraformer-recorded-speech-recognition-android-s-13e83d144d148a4f.md)），与其他 ASR 模型（如 `qwen-audio-asr-filetrans`）使用的 `.../services/audio/asr/transcription` 路径不一致，且未强制要求 WorkspaceId 域名，存在兼容性风险，建议优先使用统一的 Workspace 域名。  
- **音频预处理建议**：为提升 `paraformer` 识别效率，推荐对视频源文件预处理——提取单声道、降采样至 16kHz、编码为 opus 格式（[最佳实践](../../raw/_short/paraformer-best-practices-b5bb2777c9abaf3c.md)）。  
- **安全实践**：生产环境务必配置环境变量管理 API Key；涉及敏感场景（如第三方调用）时，应使用时效性仅 60 秒的临时 [Token](../concepts/token.md)（[生成临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)）。

## 来源文档

- [音频（非实时）](../../raw/model-api-reference/audio-api-directory/audio-api-references.md)
- [非实时语音识别（Qwen-Audio-ASR）HTTP API](../../raw/_short/qwen-audio-asr-http-api-90b9d62787e911f4.md)
- [非实时语音识别（Qwen-Audio-ASR）Android SDK](../../raw/_short/qwen-audio-asr-android-sdk-1e97f1d8b5e9135c.md)
- [非实时语音识别（Qwen-Audio-ASR）iOS SDK](../../raw/_short/qwen-audio-asr-ios-sdk-fc08c802d4ff7f08.md)
- [非实时语音识别（Qwen-Audio-ASR）HarmonyOS SDK](../../raw/_short/qwen-audio-asr-harmonyos-sdk-b1335f47a12054cd.md)
- [Qwen-Audio-ASR-Filetrans](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/qwen-audio-asr-filetrans-api.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别HTTP API参考](../../raw/_short/qwen-audio-asr-filetrans-http-api-e0184f38f9d98459.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别Python SDK](../../raw/_short/qwen-audio-asr-filetrans-python-sdk-e244defb9b1288ee.md)
- [Qwen-Audio-ASR](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/qwen-audio-asr-api.md)
- [语音识别](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别Android SDK](../../raw/_short/qwen-audio-asr-filetrans-android-sdk-a3c0fbd842a710b1.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别Java SDK](../../raw/_short/qwen-audio-asr-filetrans-java-sdk-e33c81cb99967d86.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别iOS SDK](../../raw/_short/qwen-audio-asr-filetrans-ios-sdk-ac5cc79341721cdd.md)
- [定制热词](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别HarmonyOS SDK](../../raw/_short/qwen-audio-asr-filetrans-harmonyos-sdk-bca7ed5502ce3fcf.md)
- [定制热词HTTP API参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-http-api.md)
- [定制热词Java SDK参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-java-sdk.md)
- [定制热词Python SDK参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-python-sdk.md)
- [其他模型](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/non-realtime-asr-other-models.md)
- [Fun-ASR](../../raw/_short/fun-asr-recorded-speech-recognition-api-referenc-b0273c90bb44d4cc.md)
- [Fun-ASR非实时语音识别HTTP API参考](../../raw/_short/fun-asr-recorded-speech-recognition-http-api-0e04e08da4894bf2.md)
- [Fun-ASR非实时语音识别Python SDK](../../raw/_short/funauidio-asr-recorded-speech-recognition-python-d69dda8f4675042c.md)
- [Fun-ASR非实时语音识别Android SDK](../../raw/_short/fun-asr-recorded-speech-recognition-android-sdk-f828ab21cfa96d66.md)
- [Fun-ASR非实时语音识别Java SDK](../../raw/_short/fun-asr-recorded-speech-recognition-java-sdk-b2ce5e0f37e9003f.md)
- [Fun-ASR非实时语音识别HarmonyOS SDK](../../raw/_short/fun-asr-recorded-speech-recognition-harmonyos-sd-f2337ad439819fc6.md)
- [Fun-ASR非实时语音识别iOS SDK](../../raw/_short/fun-asr-recorded-speech-recognition-ios-sdk-e6f16b9236096238.md)
- [Fun-ASR-Flash](../../raw/_short/non-real-time-speech-recognition-for-fun-asr-fla-650fa37d535f17b4.md)
- [非实时语音识别（Fun-ASR-Flash）HTTP API](../../raw/_short/fun-asr-flash-recorded-speech-recognition-http-a-7716e5d27dfd9a7b.md)
- [非实时语音识别（Fun-ASR-Flash）Android SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-androi-5c29202b31b7bc7c.md)
- [非实时语音识别（Fun-ASR-Flash）iOS SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-ios-sd-ebb52f47ee469aa4.md)
- [非实时语音识别（Fun-ASR-Flash）HarmonyOS SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-harmon-eee2d6e9b92ea2cc.md)
- [非实时语音识别（Qwen-ASR）API参考](../../raw/_short/qwen-asr-api-reference-6234af32190b8ba9.md)
- [Qwen-ASR](../../raw/_short/qwen-asr-non-realtime-api-da664e843d2e7fef.md)
- [Paraformer](../../raw/_short/paraformer-recorded-speech-recognition-api-refer-3f19f98cbb4ce26b.md)
- [Paraformer非实时语音识别HTTP API](../../raw/_short/paraformer-recorded-speech-recognition-restful-a-8b487acdee52d08d.md)
- [Paraformer非实时语音识别Python SDK](../../raw/_short/paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md)
- [Paraformer非实时语音识别Java SDK](../../raw/_short/paraformer-recorded-speech-recognition-java-sdk-915d733e99a3db9b.md)
- [Paraformer非实时语音识别iOS SDK](../../raw/_short/paraformer-recorded-speech-recognition-ios-sdk-137ff6eb176e867a.md)
- [Paraformer非实时语音识别Android SDK](../../raw/_short/paraformer-recorded-speech-recognition-android-s-13e83d144d148a4f.md)
- [Paraformer非实时语音识别HarmonyOS SDK](../../raw/_short/paraformer-recorded-speech-recognition-harmonyos-71907f3ccc6c91c4.md)
- [最佳实践](../../raw/_short/paraformer-best-practices-b5bb2777c9abaf3c.md)
- [语音合成](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference.md)
- [Qwen-Audio-TTS](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-qwen-audio-tts-api.md)
- [非实时语音合成Qwen-Audio-TTS HTTP API参考](../../raw/_short/qwen-audio-tts-http-api-ee05f9b13900b687.md)
- [非实时语音合成Qwen-Audio-TTS Python SDK参考](../../raw/_short/qwen-audio-tts-http-python-sdk-5de04c79426618ab.md)
- [CosyVoice](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-cosyvoice-api.md)
- [非实时语音合成Qwen-Audio-TTS Java SDK参考](../../raw/_short/qwen-audio-tts-http-java-sdk-e802adc41b79b00c.md)
- [非实时语音合成CosyVoice Java SDK参考](../../raw/_short/cosyvoice-tts-java-sdk-b4e23dd3f27b95e0.md)
- [非实时语音合成CosyVoice HTTP API参考](../../raw/_short/cosyvoice-tts-http-api-63e05680db50f996.md)
- [非实时语音合成CosyVoice Python SDK参考](../../raw/_short/cosyvoice-tts-python-sdk-01187ba238f52941.md)
- [Qwen-TTS](../../raw/_short/qwen-tts-non-realtime-api-1c364eb278c0a2e2.md)
- [非实时语音合成（Qwen-TTS）API参考](../../raw/_short/qwen-tts-api-3dac64d546223453.md)
- [MiniMax](../../raw/_short/minimax-speech-synthesis-9ac5812df734fd8c.md)
- [音频生成 API参考](../../raw/model-api-reference/audio-api-directory/audio-generation-api.md)
- [音视频翻译](../../raw/model-api-reference/audio-api-directory/qwen3-livetranslate-flash-api.md)
- [MiniMax同步语音合成API参考](../../raw/_short/minimax-synchronous-speech-synthesis-api-cddb40af595ff320.md)
- [其他模型](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-tts-other-models.md)


