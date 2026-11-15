# audio api directory

本目录汇总百炼平台提供的非实时音频处理能力，涵盖语音识别（ASR）、语音合成（TTS）、音频生成及音视频翻译等核心服务。所有接口均面向开发者设计，支持 HTTP、多种语言 SDK（Python/Java/Node.js/Android/iOS/HarmonyOS）及流式/[异步调用](../concepts/asynchronous-invocation.md)模式，适用于长音频转写、批量文本配音等生产级场景。

## 支持的模型/功能

### 语音识别（ASR）
- **Qwen-Audio-ASR**：主打高精度、低延迟的通用语音识别，支持上下文增强与流式返回（[Qwen-Audio-ASR](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/qwen-audio-asr-api.md)）。
- **Qwen-Audio-ASR-Filetrans**：专为长音频文件转写优化，采用“提交-轮询”异步架构，支持多文件批量处理（[Qwen-Audio-ASR-Filetrans](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/qwen-audio-asr-filetrans-api.md)）。
- **Fun-ASR / Fun-ASR-Flash**：兼顾速度与准确率，Flash 版本支持 SSE 流式中间结果（[Fun-ASR](../../raw/_short/fun-asr-recorded-speech-recognition-api-referenc-b0273c90bb44d4cc.md)）。
- **Qwen-ASR**：提供 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，便于迁移现有应用（[Qwen-ASR](../../raw/_short/qwen-asr-non-realtime-api-da664e843d2e7fef.md)）。
- **Paraformer**：轻量高效模型，适合对时延敏感或资源受限场景，推荐预处理音频以提升吞吐（[Paraformer](../../raw/_short/paraformer-recorded-speech-recognition-api-refer-3f19f98cbb4ce26b.md)）。

### 语音合成（TTS）
- **Qwen-Audio-TTS**：支持 SSML/LaTeX 格式输入，提供丰富系统音色及定制音色接入能力（[Qwen-Audio-TTS](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-qwen-audio-tts-api.md)）。
- **CosyVoice**：强调自然度与表现力，提供多个版本模型（v2/v3/v3.5），覆盖不同质量与性能需求（[CosyVoice](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-cosyvoice-api.md)）。

### 辅助能力
- **定制热词**：通过 `speech-biasing` 模型管理热词列表，显著提升专有词汇（如人名、术语）识别准确率（[定制热词](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words.md)）。

## 关键参数

### 通用连接参数
- `url`：服务地址必须使用业务空间专属域名（如 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名 `dashscope.aliyuncs.com` 已不推荐（见 [Qwen-Audio-ASR-Filetrans Android SDK](../../raw/_short/qwen-audio-asr-filetrans-android-sdk-a3c0fbd842a710b1.md) 和 [Fun-ASR HTTP API](../../raw/_short/fun-asr-recorded-speech-recognition-http-api-0e04e08da4894bf2.md)）。
- `apikey`：鉴权凭证，**强烈建议使用临时 API Key**（有效期60秒）而非长期密钥，以降低泄露风险（见 [Qwen-Audio-ASR HarmonyOS SDK](../../raw/_short/qwen-audio-asr-harmonyos-sdk-b1335f47a12054cd.md) 和 [Paraformer Python SDK](../../raw/_short/paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md)）。
- `service_mode`：非实时识别固定为 `"1"`；`device_id` 为必填项，用于日志追踪。

### ASR 核心请求参数
- `model`：明确指定模型名（如 `qwen-audio-3.1-asr-flash-filetrans`, `paraformer-v2`）。
- `input.file_urls`：异步识别必需，传入公网可访问的音频 URL 数组。
- `input.messages`：同步识别必需，包含 `user`（含 `input_audio`）和可选 `assistant` 上下文消息，顺序严格（见 [Qwen-Audio-ASR HTTP API](../../raw/_short/qwen-audio-asr-http-api-90b9d62787e911f4.md)）。
- `X-DashScope-Async`：HTTP [异步调用](../concepts/asynchronous-invocation.md)必需头，值为 `enable`；若独享部署报错 `current user api does not support asynchronous calls`，需设为 `disable` 改用同步（见 [Qwen-Audio-ASR-Filetrans HTTP API](../../raw/_short/qwen-audio-asr-filetrans-http-api-e0184f38f9d98459.md)）。

### TTS 核心请求参数
- `text`：待合成文本，支持 SSML（需 `enable_ssml=true`）和 LaTeX。
- `voice`：音色标识符，可为系统音色或通过音色定制服务创建的 ID。
- `format` / `sample_rate`：控制输出音频格式（mp3/wav/opus 等）与采样率（8000–48000 Hz）。

> **注意**：Paraformer iOS/Android SDK 的 `url` 参数示例中仍使用过时的 `wss://dashscope.aliyuncs.com/api-ws/v1/inference`（见 [文档39](../../raw/_short/paraformer-recorded-speech-recognition-ios-sdk-137ff6eb176e867a.md) 和 [文档40](../../raw/_short/paraformer-recorded-speech-recognition-android-s-13e83d144d148a4f.md)），而其他所有 SDK（如 Qwen-Audio-ASR、Fun-ASR）及 HTTP 文档均要求使用 `.../api/v1/services/audio/asr/transcription` 或 `.../aigc/multimodal-generation/generation`。请以最新 HTTP 文档为准，避免因端点错误导致调用失败。

## 使用方式

### 调用模式选择
- **同步调用（HTTP/SDK）**：适用于短音频（通常 < 1 分钟）或需即时响应的场景。直接发送请求并等待最终结果（如 `Qwen-Audio-ASR` HTTP API）。
- **[异步调用](../concepts/asynchronous-invocation.md)（HTTP/SDK）**：适用于长音频（> 1 分钟）或后台批量任务。分两步：1) 提交任务获取 `task_id`；2) 轮询 `GET /api/v1/tasks/{task_id}` 查询状态与结果（如 `Qwen-Audio-ASR-Filetrans`、`Fun-ASR`、`Paraformer`）。
- **流式调用（SSE）**：适用于需低首包延迟的场景（如实时字幕）。通过 `X-DashScope-SSE: enable` 头启用，服务端按音频片段分批推送（仅 `Qwen-Audio-ASR`、`Fun-ASR-Flash`、`Qwen-Audio-TTS`、`CosyVoice` 支持）。

### SDK 快速集成
1. **配置环境**：设置 `DASHSCOPE_API_KEY` 和 `DASHSCOPE_WORKSPACE_ID` 环境变量。
2. **安装 SDK**：如 Python 使用 `pip install dashscope>=2.0.1`（见 [Qwen-Audio-TTS Python SDK](../../raw/_short/qwen-audio-tts-http-python-sdk-5de04c79426618ab.md)）。
3. **初始化 Client**：指定 `region`（如 `cn-beijing`）和 `workspace`（见 [Qwen-Audio-ASR-Filetrans Python SDK](../../raw/_short/qwen-audio-asr-filetrans-python-sdk-e244defb9b1288ee.md)）。
4. **发起请求**：
   - ASR 异步：`client.audio.asr.jobs.create(model="...", file_urls=["..."])`
   - TTS 非流式：`client.audio.tts.http.synthesize(text="...", model="...", voice="...")`
   - TTS 流式：`client.audio.tts.http.stream(...)` 并实现回调处理分片。

## 限制和注意事项

- **地域与域名**：华北2（北京）和新加坡地域已全面启用业务空间专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名虽兼容但性能与稳定性较低，**必须迁移**（见 [Qwen-Audio-ASR-Filetrans HTTP API](../../raw/_short/qwen-audio-asr-filetrans-http-api-e0184f38f9d98459.md) 和 [Fun-ASR HTTP API](../../raw/_short/fun-asr-recorded-speech-recognition-http-api-0e04e08da4894bf2.md)）。
- **热词地域限制**：定制热词功能**不支持新加坡地域子业务空间**（见 [定制热词 HTTP API](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-http-api.md) 和 [定制热词 Python SDK](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-python-sdk.md)）。
- **异步任务生命周期**：所有异步任务（Filetrans/Fun-ASR/Paraformer）的结果与下载 URL 有效期为 **24 小时**，超时后无法查询或下载（见 [Qwen-Audio-ASR-Filetrans Python SDK](../../raw/_short/qwen-audio-asr-filetrans-python-sdk-e244defb9b1288ee.md) 和 [Fun-ASR Python SDK](../../raw/_short/funauidio-asr-recorded-speech-recognition-python-d69dda8f4675042c.md)）。
- **音频预处理**：Paraformer 推荐对视频文件进行预处理（提取音轨、降采样至 16kHz、编码为 opus），可显著提升转写效率（见 [Paraformer 最佳实践](../../raw/_short/paraformer-best-practices-b5bb2777c9abaf3c.md)）。
- **SDK 版本要求**：Qwen-Audio-TTS Java SDK 要求 DashScope SDK ≥ 2.22.15；Python SDK 要求 ≥ 2.0.1（见 [Qwen-Audio-TTS Java SDK](../../raw/_short/qwen-audio-tts-http-java-sdk-e802adc41b79b00c.md) 和 [Qwen-Audio-TTS Python SDK](../../raw/_short/qwen-audio-tts-http-python-sdk-5de04c79426618ab.md)）。

## 来源文档

- [语音识别](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference.md)
- [音频（非实时）](../../raw/model-api-reference/audio-api-directory/audio-api-references.md)
- [Qwen-Audio-ASR](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/qwen-audio-asr-api.md)
- [非实时语音识别（Qwen-Audio-ASR）Android SDK](../../raw/_short/qwen-audio-asr-android-sdk-1e97f1d8b5e9135c.md)
- [非实时语音识别（Qwen-Audio-ASR）iOS SDK](../../raw/_short/qwen-audio-asr-ios-sdk-fc08c802d4ff7f08.md)
- [非实时语音识别（Qwen-Audio-ASR）HTTP API](../../raw/_short/qwen-audio-asr-http-api-90b9d62787e911f4.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别HTTP API参考](../../raw/_short/qwen-audio-asr-filetrans-http-api-e0184f38f9d98459.md)
- [Qwen-Audio-ASR-Filetrans](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/qwen-audio-asr-filetrans-api.md)
- [非实时语音识别（Qwen-Audio-ASR）HarmonyOS SDK](../../raw/_short/qwen-audio-asr-harmonyos-sdk-b1335f47a12054cd.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别Python SDK](../../raw/_short/qwen-audio-asr-filetrans-python-sdk-e244defb9b1288ee.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别Java SDK](../../raw/_short/qwen-audio-asr-filetrans-java-sdk-e33c81cb99967d86.md)
- [Qwen-Audio-ASR-Filetrans Node.js SDK](../../raw/_short/qwen-audio-asr-filetrans-nodejs-sdk-6457111def74455c.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别Android SDK](../../raw/_short/qwen-audio-asr-filetrans-android-sdk-a3c0fbd842a710b1.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别HarmonyOS SDK](../../raw/_short/qwen-audio-asr-filetrans-harmonyos-sdk-bca7ed5502ce3fcf.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别iOS SDK](../../raw/_short/qwen-audio-asr-filetrans-ios-sdk-ac5cc79341721cdd.md)
- [定制热词](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words.md)
- [定制热词HTTP API参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-http-api.md)
- [定制热词Python SDK参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-python-sdk.md)
- [定制热词Java SDK参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-java-sdk.md)
- [其他模型](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/non-realtime-asr-other-models.md)
- [Fun-ASR](../../raw/_short/fun-asr-recorded-speech-recognition-api-referenc-b0273c90bb44d4cc.md)
- [Fun-ASR非实时语音识别HTTP API参考](../../raw/_short/fun-asr-recorded-speech-recognition-http-api-0e04e08da4894bf2.md)
- [Fun-ASR非实时语音识别Python SDK](../../raw/_short/funauidio-asr-recorded-speech-recognition-python-d69dda8f4675042c.md)
- [Fun-ASR非实时语音识别Android SDK](../../raw/_short/fun-asr-recorded-speech-recognition-android-sdk-f828ab21cfa96d66.md)
- [Fun-ASR非实时语音识别iOS SDK](../../raw/_short/fun-asr-recorded-speech-recognition-ios-sdk-e6f16b9236096238.md)
- [Fun-ASR非实时语音识别Java SDK](../../raw/_short/fun-asr-recorded-speech-recognition-java-sdk-b2ce5e0f37e9003f.md)
- [Fun-ASR-Flash](../../raw/_short/non-real-time-speech-recognition-for-fun-asr-fla-650fa37d535f17b4.md)
- [Fun-ASR非实时语音识别HarmonyOS SDK](../../raw/_short/fun-asr-recorded-speech-recognition-harmonyos-sd-f2337ad439819fc6.md)
- [非实时语音识别（Fun-ASR-Flash）HTTP API](../../raw/_short/fun-asr-flash-recorded-speech-recognition-http-a-7716e5d27dfd9a7b.md)
- [非实时语音识别（Fun-ASR-Flash）Android SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-androi-5c29202b31b7bc7c.md)
- [非实时语音识别（Fun-ASR-Flash）iOS SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-ios-sd-ebb52f47ee469aa4.md)
- [Qwen-ASR](../../raw/_short/qwen-asr-non-realtime-api-da664e843d2e7fef.md)
- [非实时语音识别（Fun-ASR-Flash）HarmonyOS SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-harmon-eee2d6e9b92ea2cc.md)
- [非实时语音识别（Qwen-ASR）API参考](../../raw/_short/qwen-asr-api-reference-6234af32190b8ba9.md)
- [Paraformer非实时语音识别HTTP API](../../raw/_short/paraformer-recorded-speech-recognition-restful-a-8b487acdee52d08d.md)
- [Paraformer](../../raw/_short/paraformer-recorded-speech-recognition-api-refer-3f19f98cbb4ce26b.md)
- [Paraformer非实时语音识别Python SDK](../../raw/_short/paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md)
- [Paraformer非实时语音识别Java SDK](../../raw/_short/paraformer-recorded-speech-recognition-java-sdk-915d733e99a3db9b.md)
- [Paraformer非实时语音识别iOS SDK](../../raw/_short/paraformer-recorded-speech-recognition-ios-sdk-137ff6eb176e867a.md)
- [Paraformer非实时语音识别Android SDK](../../raw/_short/paraformer-recorded-speech-recognition-android-s-13e83d144d148a4f.md)
- [Paraformer非实时语音识别HarmonyOS SDK](../../raw/_short/paraformer-recorded-speech-recognition-harmonyos-71907f3ccc6c91c4.md)
- [最佳实践](../../raw/_short/paraformer-best-practices-b5bb2777c9abaf3c.md)
- [语音合成](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference.md)
- [非实时语音合成Qwen-Audio-TTS HTTP API参考](../../raw/_short/qwen-audio-tts-http-api-ee05f9b13900b687.md)
- [Qwen-Audio-TTS](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-qwen-audio-tts-api.md)
- [非实时语音合成Qwen-Audio-TTS Java SDK参考](../../raw/_short/qwen-audio-tts-http-java-sdk-e802adc41b79b00c.md)
- [CosyVoice](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-cosyvoice-api.md)
- [非实时语音合成Qwen-Audio-TTS Python SDK参考](../../raw/_short/qwen-audio-tts-http-python-sdk-5de04c79426618ab.md)
- [非实时语音合成CosyVoice HTTP API参考](../../raw/_short/cosyvoice-tts-http-api-63e05680db50f996.md)
- [非实时语音合成CosyVoice Python SDK参考](../../raw/_short/cosyvoice-tts-python-sdk-01187ba238f52941.md)
- [非实时语音合成CosyVoice Java SDK参考](../../raw/_short/cosyvoice-tts-java-sdk-b4e23dd3f27b95e0.md)
- [其他模型](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-tts-other-models.md)
- [非实时语音合成（Qwen-TTS）API参考](../../raw/_short/qwen-tts-api-3dac64d546223453.md)
- [Qwen-TTS](../../raw/_short/qwen-tts-non-realtime-api-1c364eb278c0a2e2.md)
- [MiniMax同步语音合成API参考](../../raw/_short/minimax-synchronous-speech-synthesis-api-cddb40af595ff320.md)
- [MiniMax](../../raw/_short/minimax-speech-synthesis-9ac5812df734fd8c.md)
- [音频生成 API参考](../../raw/model-api-reference/audio-api-directory/audio-generation-api.md)
- [音视频翻译](../../raw/model-api-reference/audio-api-directory/qwen3-livetranslate-flash-api.md)


