# audio api directory

audio api directory 是百炼平台提供的非实时音视频处理能力集合，涵盖语音识别、语音合成、音频打标、音频生成及音视频翻译等核心功能。所有接口均通过 HTTP RESTful 方式调用，适用于离线批量处理或低延迟要求不严格的场景。详细技术细节请参考 [音视频（非实时）](../../raw/model-api-reference/audio-api-directory.md)。

## 支持的模型与功能

当前目录下支持以下功能模块（均基于 `qwen-audio` 系列及 `qwen3-livetranslate-flash` 模型）：
- **语音识别（ASR）**：支持多语种、带标点和说话人分离的转写；  
- **语音合成（TTS）**：提供多种音色与语速控制；  
- **音频打标（Captioning）**：对音频内容生成结构化标签与摘要；  
- **音频生成（Audio Generation）**：根据文本提示生成高质量语音或环境音；  
- **音视频翻译（LiveTranslate Flash）**：支持源语言到目标语言的端到端字幕/语音翻译。  
各功能入口与能力边界详见 [音视频（非实时）](../../raw/model-api-reference/audio-api-directory.md)。

## 关键参数

通用请求头需包含 `Authorization: Bearer <api_key>` 与 `Content-Type: application/json`。各接口共性关键参数包括：
- `model`: 必填，如 `"qwen-audio-asr"`、`"qwen-audio-tts"` 或 `"qwen3-livetranslate-flash"`；  
- `input`: 音频数据以 base64 编码字符串或 OSS URL 形式传入（部分接口支持二者之一）；  
- `parameters`: 控制行为的 JSON 对象，例如 `{"language": "zh", "enable_punctuation": true}`；  
- `response_format`: 可选 `"json"` 或 `"srt"`（仅 ASR 和翻译接口支持）。  
完整参数定义请查阅对应子文档，例如 [语音识别](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference.md) 中的 `parameters` 字段说明。

## 使用方式

1. 上传音频至百炼支持的存储（如 OSS），获取可公开访问的 URL；或直接 base64 编码音频文件（≤25 MB）；  
2. 构造 POST 请求至对应功能 endpoint（如 `/v1/audio/transcriptions`）；  
3. 解析响应体中的 `result` 字段（异步任务需轮询 `job_id` 获取结果）。  
> **注意**：`qwen3-livetranslate-flash-api.md` 文档中描述的 `stream=true` 参数在当前非实时目录下**不生效**，该参数仅适用于实时流式接口（见 [音视频（非实时）](../../raw/model-api-reference/audio-api-directory.md) 的上下文说明）。

## 限制和注意事项

- 单次请求音频时长上限为 30 分钟（ASR/TTS）、10 分钟（打标）、5 分钟（生成与翻译）；  
- 免费调用量受项目配额限制，超出后返回 `429 Too Many Requests`；  
- 音频格式仅支持 `mp3`, `wav`, `m4a`, `flac`，采样率建议 16kHz 或 44.1kHz；  
- 所有接口默认超时时间为 120 秒，长音频建议使用异步模式；  
- 若发现 `qwen-audio-asr-captioner-http-api.md` 中标注的“支持视频输入”与实际 API 行为不符，请以 [音视频（非实时）](../../raw/model-api-reference/audio-api-directory.md) 的功能列表为准——该子文档明确限定其输入为纯音频。

## 来源文档

- [音视频（非实时）](../../raw/model-api-reference/audio-api-directory.md)


