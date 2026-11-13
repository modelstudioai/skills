# audio api directory

本目录提供非实时音频处理能力的 API 参考，涵盖语音识别（ASR）、语音合成（TTS）、音频生成和音视频翻译四大核心功能。所有接口均面向离线或长时音频文件场景设计，支持同步与异步调用模式，并提供多语言 SDK 封装。实时音频能力请参见 [Realtime API 概述](raw/model-api-reference/realtime-api-directory/realtime-api-overview.md)。

## 支持的模型/功能

非实时音频 API 主要分为三大类服务：

- **语音识别（ASR）**：支持 `Qwen-Audio-ASR`（含上下文增强）、`Qwen-Audio-ASR-Filetrans`（纯异步长文件转写）、`Fun-ASR`、`Fun-ASR-Flash`、`Qwen-ASR` 和 `Paraformer` 六大主流模型。其中 `Qwen-Audio-ASR` 与 `Fun-ASR-Flash` 支持流式响应（需 `X-DashScope-SSE: enable` 且音频 ≥1 分钟），而 `Qwen-Audio-ASR-Filetrans`、`Fun-ASR`、`Paraformer` 等专为长文件设计，采用“提交任务 → 轮询查询”异步范式。详见 [语音识别](raw/model-api-reference/audio-api-directory/speech-recognition-api-reference.md)。

- **语音合成（TTS）**：提供 `Qwen-Audio-TTS` 和 `CosyVoice` 两大引擎，均支持非流式（返回音频 URL 或二进制数据）与流式（SSE 分片返回）两种调用方式。`CosyVoice` 支持多版本模型（如 `cosyvoice-v3.5-plus`）及声音复刻/设计音色集成，[非实时语音合成CosyVoice HTTP API参考](raw/_short/cosyvoice-tts-http-api-63e05680db50f996.md) 中明确列出了全部模型与音色取值范围。

- **其他能力**：还包括 [音频生成](raw/model-api-reference/audio-api-directory/audio-generation-api.md) 和 [音视频翻译](raw/model-api-reference/audio-api-directory/qwen3-livetranslate-flash-api.md)，适用于音乐生成、配音翻译等高级场景。

> **注意**：`Qwen-ASR` 模型的接入方式存在文档矛盾——[非实时语音识别（Qwen-ASR）API参考](raw/_short/qwen-asr-api-reference-6234af32190b8ba9.md) 声明其同时支持 OpenAI 兼容模式与 DashScope 同步调用，但实际仅 `qwen-audio-3.1-asr-flash` 等音频专用模型被广泛验证；通用文本模型 `qwen-3` 不具备 ASR 能力，开发者应优先选用 `qwen-audio-*` 前缀模型。

## 关键参数

所有非实时音频 API 的核心参数结构高度统一，关键字段如下：

- **`model`**（必选 `string`）：模型标识符，如 `qwen-audio-3.1-asr-flash`、`cosyvoice-v3.5-plus`、`paraformer-v2`。不同模型对输入格式要求不同，务必查阅对应模型文档。
- **`input`**（必选 `object`）：
  - ASR 类：`file_urls`（数组，公网可访问音频 URL）或 `audio`（Base64 编码字符串）；`Qwen-Audio-ASR` 还支持 `messages` 数组携带上下文（`user` + `assistant` 轮次）。
  - TTS 类：`text`（待合成文本，支持 SSML/LaTeX）、`voice`（音色 ID）、`format`（`mp3`/`wav`/`opus` 等）、`sample_rate`（如 `16000`、`22050`）。
- **请求头**：
  - `Authorization: Bearer <your_api_key>`（必选，API Key 鉴权）
  - `Content-Type: application/json`（必选）
  - `X-DashScope-SSE: enable`（TTS/部分 ASR 流式调用时必选）
  - `X-DashScope-Async: enable`（[异步任务](../concepts/asynchronous-task.md)提交接口必选，如 Filetrans/Paraformer）

## 使用方式

### 调用路径选择
- **短音频（<2 分钟）+ 低延迟需求**：优先使用 `Qwen-Audio-ASR` 或 `Fun-ASR-Flash` 的同步 HTTP 接口（`/multimodal-generation/generation`），配合 `X-DashScope-SSE: enable` 获取流式中间结果。
- **长音频（≥2 分钟）或批量处理**：必须使用异步接口（`/audio/asr/transcription` 等），通过 `task_id` 轮询或 SDK 封装的 `wait()` 方法获取结果。`Qwen-Audio-ASR-Filetrans`、`Paraformer`、`Fun-ASR` 均属此类。
- **移动端集成**：各模型均提供 Android/iOS/HarmonyOS SDK，初始化时需传入 `url`（含 WorkspaceId）、`apikey`、`service_mode: "1"`；HarmonyOS SDK 的 `url` 固定为北京地域专属域名，[Qwen-Audio-ASR-Filetrans非实时语音识别HarmonyOS SDK](raw/_short/qwen-audio-asr-filetrans-harmonyos-sdk-bca7ed5502ce3fcf.md) 明确指出此限制。

### SDK 快速启动示例（Python）
```python
import dashscope
client = dashscope.Client(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    workspace="{WorkspaceId}",  # 替换为真实ID
    region="cn-beijing"
)

# 异步转写（Filetrans）
job = client.audio.asr.jobs.create(
    model="qwen-audio-3.1-asr-flash-filetrans",
    file_urls=["https://example.com/audio.mp3"]
)
job = client.audio.asr.jobs.wait(job=job)  # 阻塞等待
print(job.results[0].text)

# 流式合成（CosyVoice）
stream = client.audio.tts.http.stream(
    text="你好，世界",
    model="cosyvoice-v3.5-plus",
    voice="zhitian_emo"
)
for chunk in stream:
    if chunk.type == 'audio':
        write_audio_chunk(chunk.data)
```

## 限制和注意事项

- **地域与域名**：华北2（北京）和新加坡地域已全面启用业务空间专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名 `dashscope.aliyuncs.com` 仍兼容但不推荐。[Qwen-Audio-ASR-Filetrans非实时语音识别HTTP API参考](raw/_short/qwen-audio-asr-filetrans-http-api-e0184f38f9d98459.md) 和 [Fun-ASR非实时语音识别HTTP API参考](raw/_short/fun-asr-recorded-speech-recognition-http-api-0e04e08da4894bf2.md) 均强调迁移必要性。
  
- **热词功能限制**：定制热词（`speech-biasing`）仅在北京地域可用，新加坡子业务空间明确不支持，见 [定制热词HTTP API参考](raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-http-api.md)。

- **音频规格**：所有模型均遵循统一的[音频规格](https://help.aliyun.com/zh/model-studio/asr-model#asr_audio_spec02)，包括格式（MP3/WAV/OPUS/PCM）、采样率（8k–48k Hz）、单文件大小（≤100 MB）和时长（≤6 小时）。Paraformer 推荐预处理视频为 OPUS 音频以提升效率，详见 [最佳实践](raw/_short/paraformer-best-practices-b5bb2777c9abaf3c.md)。

- **安全实践**：生产环境必须使用环境变量管理 API Key；高敏感场景（如第三方调用）应使用时效仅 60 秒的[临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)，该建议在 Paraformer、Fun-ASR、Qwen-Audio-TTS 等多份 SDK 文档中重复强调。

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
- [Qwen-Audio-ASR-Filetrans非实时语音识别Java SDK](../../raw/_short/qwen-audio-asr-filetrans-java-sdk-e33c81cb99967d86.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别Python SDK](../../raw/_short/qwen-audio-asr-filetrans-python-sdk-e244defb9b1288ee.md)
- [Qwen-Audio-ASR-Filetrans Node.js SDK](../../raw/_short/qwen-audio-asr-filetrans-nodejs-sdk-6457111def74455c.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别iOS SDK](../../raw/_short/qwen-audio-asr-filetrans-ios-sdk-ac5cc79341721cdd.md)
- [定制热词](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别Android SDK](../../raw/_short/qwen-audio-asr-filetrans-android-sdk-a3c0fbd842a710b1.md)
- [Qwen-Audio-ASR-Filetrans非实时语音识别HarmonyOS SDK](../../raw/_short/qwen-audio-asr-filetrans-harmonyos-sdk-bca7ed5502ce3fcf.md)
- [定制热词HTTP API参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-http-api.md)
- [定制热词Java SDK参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-java-sdk.md)
- [其他模型](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/non-realtime-asr-other-models.md)
- [Fun-ASR](../../raw/_short/fun-asr-recorded-speech-recognition-api-referenc-b0273c90bb44d4cc.md)
- [Fun-ASR非实时语音识别HTTP API参考](../../raw/_short/fun-asr-recorded-speech-recognition-http-api-0e04e08da4894bf2.md)
- [Fun-ASR非实时语音识别Java SDK](../../raw/_short/fun-asr-recorded-speech-recognition-java-sdk-b2ce5e0f37e9003f.md)
- [Fun-ASR非实时语音识别Android SDK](../../raw/_short/fun-asr-recorded-speech-recognition-android-sdk-f828ab21cfa96d66.md)
- [Fun-ASR非实时语音识别iOS SDK](../../raw/_short/fun-asr-recorded-speech-recognition-ios-sdk-e6f16b9236096238.md)
- [Fun-ASR非实时语音识别HarmonyOS SDK](../../raw/_short/fun-asr-recorded-speech-recognition-harmonyos-sd-f2337ad439819fc6.md)
- [Fun-ASR-Flash](../../raw/_short/non-real-time-speech-recognition-for-fun-asr-fla-650fa37d535f17b4.md)
- [非实时语音识别（Fun-ASR-Flash）HTTP API](../../raw/_short/fun-asr-flash-recorded-speech-recognition-http-a-7716e5d27dfd9a7b.md)
- [非实时语音识别（Fun-ASR-Flash）Android SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-androi-5c29202b31b7bc7c.md)
- [非实时语音识别（Fun-ASR-Flash）iOS SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-ios-sd-ebb52f47ee469aa4.md)
- [非实时语音识别（Fun-ASR-Flash）HarmonyOS SDK](../../raw/_short/fun-asr-flash-recorded-speech-recognition-harmon-eee2d6e9b92ea2cc.md)
- [定制热词Python SDK参考](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words/vocabulary-python-sdk.md)
- [非实时语音识别（Qwen-ASR）API参考](../../raw/_short/qwen-asr-api-reference-6234af32190b8ba9.md)
- [Qwen-ASR](../../raw/_short/qwen-asr-non-realtime-api-da664e843d2e7fef.md)
- [Fun-ASR非实时语音识别Python SDK](../../raw/_short/funauidio-asr-recorded-speech-recognition-python-d69dda8f4675042c.md)
- [Paraformer](../../raw/_short/paraformer-recorded-speech-recognition-api-refer-3f19f98cbb4ce26b.md)
- [Paraformer非实时语音识别HTTP API](../../raw/_short/paraformer-recorded-speech-recognition-restful-a-8b487acdee52d08d.md)
- [Paraformer非实时语音识别Java SDK](../../raw/_short/paraformer-recorded-speech-recognition-java-sdk-915d733e99a3db9b.md)
- [Paraformer非实时语音识别Python SDK](../../raw/_short/paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md)
- [Paraformer非实时语音识别Android SDK](../../raw/_short/paraformer-recorded-speech-recognition-android-s-13e83d144d148a4f.md)
- [Paraformer非实时语音识别iOS SDK](../../raw/_short/paraformer-recorded-speech-recognition-ios-sdk-137ff6eb176e867a.md)
- [最佳实践](../../raw/_short/paraformer-best-practices-b5bb2777c9abaf3c.md)
- [语音合成](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference.md)
- [Qwen-Audio-TTS](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-qwen-audio-tts-api.md)
- [非实时语音合成Qwen-Audio-TTS Java SDK参考](../../raw/_short/qwen-audio-tts-http-java-sdk-e802adc41b79b00c.md)
- [Paraformer非实时语音识别HarmonyOS SDK](../../raw/_short/paraformer-recorded-speech-recognition-harmonyos-71907f3ccc6c91c4.md)
- [CosyVoice](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-cosyvoice-api.md)
- [非实时语音合成Qwen-Audio-TTS Python SDK参考](../../raw/_short/qwen-audio-tts-http-python-sdk-5de04c79426618ab.md)
- [非实时语音合成CosyVoice HTTP API参考](../../raw/_short/cosyvoice-tts-http-api-63e05680db50f996.md)
- [非实时语音合成CosyVoice Java SDK参考](../../raw/_short/cosyvoice-tts-java-sdk-b4e23dd3f27b95e0.md)
- [非实时语音合成CosyVoice Python SDK参考](../../raw/_short/cosyvoice-tts-python-sdk-01187ba238f52941.md)
- [其他模型](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference/non-realtime-tts-other-models.md)
- [Qwen-TTS](../../raw/_short/qwen-tts-non-realtime-api-1c364eb278c0a2e2.md)
- [非实时语音合成（Qwen-TTS）API参考](../../raw/_short/qwen-tts-api-3dac64d546223453.md)
- [MiniMax](../../raw/_short/minimax-speech-synthesis-9ac5812df734fd8c.md)
- [MiniMax同步语音合成API参考](../../raw/_short/minimax-synchronous-speech-synthesis-api-cddb40af595ff320.md)
- [音频生成 API参考](../../raw/model-api-reference/audio-api-directory/audio-generation-api.md)
- [音视频翻译](../../raw/model-api-reference/audio-api-directory/qwen3-livetranslate-flash-api.md)
- [非实时语音合成Qwen-Audio-TTS HTTP API参考](../../raw/_short/qwen-audio-tts-http-api-ee05f9b13900b687.md)


