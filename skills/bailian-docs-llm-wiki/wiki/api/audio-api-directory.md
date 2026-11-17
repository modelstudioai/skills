# audio api directory

本目录提供非实时音频处理能力的完整 API 接口规范，涵盖语音识别（ASR）、语音合成（TTS）、音频生成及音视频翻译四大核心功能。所有接口均基于百炼平台统一的多模态服务框架，支持 HTTP、各类 SDK（Python/Java/Android/iOS/HarmonyOS）及 OpenAI 兼容协议调用。实时音频能力请参见 [Realtime API 概述](raw/model-api-reference/realtime-api-directory/realtime-api-overview.md)。

## 支持的模型/功能

非实时音频 API 主要分为两大类能力：

- **语音识别（ASR）**：支持 `Qwen-Audio-ASR`（含 Flash 变体）、`Qwen-Audio-ASR-Filetrans`、`Fun-ASR`（含 Flash）、`Qwen-ASR` 和 `Paraformer` 等主流模型。其中 `Qwen-Audio-ASR` 和 `Fun-ASR-Flash` 支持上下文增强与 SSE 流式返回；`Qwen-Audio-ASR-Filetrans` 和 `Fun-ASR` 采用“提交-轮询”[异步任务](../concepts/asynchronous-task.md)模式，适用于长音频文件；`Paraformer` 提供高精度转写与丰富的预处理最佳实践 [Paraformer最佳实践](raw/_short/paraformer-best-practices-b5bb2777c9abaf3c.md)。  
- **语音合成（TTS）**：提供 `Qwen-Audio-TTS` 和 `CosyVoice` 两大引擎，均支持 SSML/LaTeX 文本格式、多音色（系统音色、声音复刻、声音设计）及多种音频格式（mp3/wav/opus/pcm）。  

此外，该目录还包含[定制热词](raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words.md)功能，用于提升特定领域词汇识别准确率（注意：新加坡地域暂不支持）。

## 关键参数

所有非实时音频 API 的通用关键参数如下：

- **`model`**（必选 `string`）：指定模型 ID，如 `qwen-audio-3.1-asr-flash-filetrans`、`cosyvoice-v3.5-plus`。不同模型对输入结构要求不同（例如 `Qwen-Audio-ASR` 使用 `messages` 数组，而 `Filetrans` 类模型使用 `file_urls` 字段）。
- **`input`**（必选 `object`）：承载核心输入数据。ASR 接口通常为 `{"file_urls": ["https://..."]}` 或 `{"messages": [...]}`；TTS 接口为 `{"text": "hello", "voice": "zhitian_emo"}`。
- **`Authorization` 请求头**（必选）：格式为 `Bearer <your_api_key>`，需使用与目标地域匹配的 API Key。
- **`X-DashScope-SSE` 请求头**（可选）：设为 `enable` 启用流式响应（仅部分 ASR/TTS 模型支持，且对音频时长有最低要求，详见 [非实时语音识别（Qwen-Audio-ASR）HTTP API](raw/_short/qwen-audio-asr-http-api-90b9d62787e911f4.md)）。
- **`X-DashScope-Async` 请求头**（ASR [异步任务](../concepts/asynchronous-task.md)必选）：设为 `enable` 以触发任务提交流程（如 `Fun-ASR`、`Paraformer`），否则请求将失败。

> **注意**：`Qwen-ASR` 模型存在接入方式矛盾——文档 [非实时语音识别（Qwen-ASR）API参考](raw/_short/qwen-asr-api-reference-6234af32190b8ba9.md) 明确说明其支持 OpenAI 兼容模式（`/compatible-mode/v1/chat/completions`），但同系列其他文档（如 `Qwen-Audio-ASR`）均未提及此路径，且实际 SDK 实现中未暴露该能力。开发者应优先使用 DashScope 协议，OpenAI 兼容模式仅限特定千问3-ASR-Flash模型。

## 使用方式

### 调用模式选择
- **同步直连模式**：适用于短音频（通常 < 1 分钟）或低延迟敏感场景，直接返回结果（如 `Qwen-Audio-ASR` HTTP API）。  
- **[异步任务](../concepts/asynchronous-task.md)模式**：适用于长音频或批量处理，需先 `POST /transcription` 提交任务获取 `task_id`，再 `GET /tasks/{task_id}` 轮询结果（如 `Qwen-Audio-ASR-Filetrans`、`Paraformer`）。任务结果 URL 有效期为 24 小时。  
- **流式模式**：通过 `X-DashScope-SSE: enable` 启用，服务端分片推送中间结果（ASR）或音频数据（TTS），需客户端支持 SSE 解析。

### SDK 集成要点
- 所有 SDK 均需配置 `WorkspaceId` 和对应地域的 API Key。地域配置方式因 SDK 而异：Python SDK 通过 `Client(region="cn-beijing")`，Java SDK 通过 `Constants.baseHttpApiUrl`，移动端 SDK 则在初始化 `parameters` JSON 中显式传入 `url` 字段（如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/...`）。  
- 移动端 SDK（Android/iOS/HarmonyOS）的 `url` 参数必须使用 `wss://` 协议，且 `service_mode` 固定为 `"1"`。  
- Python/Java SDK 的 `client.audio.asr.jobs.create` 和 `client.audio.tts.http.synthesize` 等高层封装已自动处理任务提交、等待与结果解析逻辑，推荐优先使用。

## 限制和注意事项

- **地域与域名**：华北2（北京）和新加坡地域已全面启用业务空间专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但官方强烈建议迁移以获得更高性能与稳定性。  
- **热词限制**：定制热词功能仅在北京地域可用，新加坡地域明确不支持 [定制热词HTTP API参考](raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-http-api.md)。  
- **音频规格**：所有模型均遵循统一的[音频规格](https://help.aliyun.com/zh/model-studio/asr-model#asr_audio_spec02)，包括格式（wav/mp3/opus等）、采样率（8k–48k Hz）、单文件大小（≤ 100 MB）及时长（≤ 6 小时）限制。  
- **SDK 版本兼容性**：`Qwen-Audio-TTS` 和 `CosyVoice` 的 Java SDK 明确要求 DashScope SDK ≥ 2.22.15，Python SDK 要求 ≥ 2.0.1；旧版本可能缺失关键参数（如 `sample_rate`）或流式回调支持。  
- **临时 [Token](../concepts/token.md) 安全实践**：涉及第三方调用或高风险操作时，应使用时效性为 60 秒的[临时 API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)，而非长期有效 Key，以降低泄露风险。

## 来源文档

- [音频（非实时）](../../raw/model-api-reference/audio-api-directory/audio-api-references.md)
- [语音识别](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference.md)
- [Qwen-Audio-ASR](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/qwen-audio-asr-api.md)
- [非实时语音识别（Qwen-Audio-ASR）HTTP API](../../raw/_short/qwen-audio-asr-http-api-90b9d62787e911f4.md)
- [非实时语音识别（Qwen-Audio-ASR）Android SDK](../../raw/_short/qwen-audio-asr-android-sdk-1e97f1d8b5e9135c.md)
- [非实时语音识别（Qwen-Audio-ASR）HarmonyOS SDK](../../raw/_short/qwen-audio-asr-harmonyos-sdk-b1335f47a12054cd.md)
- [Qwen-Audio-ASR-Filetrans](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/qwen-audio-asr-filetrans-api.md)
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
- [Qwen-Audio-ASR-Filetrans非实时语音识别HTTP API参考](../../raw/_short/qwen-audio-asr-filetrans-http-api-e0184f38f9d98459.md)
- [Fun-ASR非实时语音识别HarmonyOS SDK](../../raw/_short/fun-asr-recorded-speech-recognition-harmonyos-sd-f2337ad439819fc6.md)
- [非实时语音识别（Qwen-Audio-ASR）iOS SDK](../../raw/_short/qwen-audio-asr-ios-sdk-fc08c802d4ff7f08.md)
- [Fun-ASR-Flash](../../raw/_short/non-real-time-speech-recognition-for-fun-asr-fla-650fa37d535f17b4.md)
- [非实时语音识别（Fun-ASR-Flash）HTTP API](../../raw/_short/fun-asr-flash-recorded-speech-recognition-http-a-7716e5d27dfd9a7b.md)
- [非实时语音识别（Fun-ASR-Flash）Android SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-androi-5c29202b31b7bc7c.md)
- [非实时语音识别（Fun-ASR-Flash）iOS SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-ios-sd-ebb52f47ee469aa4.md)
- [非实时语音识别（Fun-ASR-Flash）HarmonyOS SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-harmon-eee2d6e9b92ea2cc.md)
- [非实时语音识别（Qwen-ASR）API参考](../../raw/_short/qwen-asr-api-reference-6234af32190b8ba9.md)
- [Qwen-ASR](../../raw/_short/qwen-asr-non-realtime-api-da664e843d2e7fef.md)
- [Paraformer](../../raw/_short/paraformer-recorded-speech-recognition-api-refer-3f19f98cbb4ce26b.md)
- [Paraformer非实时语音识别Python SDK](../../raw/_short/paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md)
- [Paraformer非实时语音识别HTTP API](../../raw/_short/paraformer-recorded-speech-recognition-restful-a-8b487acdee52d08d.md)
- [Paraformer非实时语音识别Java SDK](../../raw/_short/paraformer-recorded-speech-recognition-java-sdk-915d733e99a3db9b.md)
- [Paraformer非实时语音识别Android SDK](../../raw/_short/paraformer-recorded-speech-recognition-android-s-13e83d144d148a4f.md)
- [Paraformer非实时语音识别iOS SDK](../../raw/_short/paraformer-recorded-speech-recognition-ios-sdk-137ff6eb176e867a.md)
- [Paraformer非实时语音识别HarmonyOS SDK](../../raw/_short/paraformer-recorded-speech-recognition-harmonyos-71907f3ccc6c91c4.md)
- [语音合成](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference.md)
- [Qwen-Audio-TTS](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-qwen-audio-tts-api.md)
- [最佳实践](../../raw/_short/paraformer-best-practices-b5bb2777c9abaf3c.md)
- [非实时语音合成Qwen-Audio-TTS Java SDK参考](../../raw/_short/qwen-audio-tts-http-java-sdk-e802adc41b79b00c.md)
- [非实时语音合成Qwen-Audio-TTS Python SDK参考](../../raw/_short/qwen-audio-tts-http-python-sdk-5de04c79426618ab.md)
- [非实时语音合成Qwen-Audio-TTS HTTP API参考](../../raw/_short/qwen-audio-tts-http-api-ee05f9b13900b687.md)
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


