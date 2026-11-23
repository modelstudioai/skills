# audio api directory

百炼平台的 Audio API Directory 提供了一组面向非实时音视频处理任务的 HTTP 接口，覆盖语音识别、语音合成、音频打标、音频生成及音视频翻译等核心能力。所有接口均采用 RESTful 设计，支持标准 JSON 请求/响应格式，并通过 API Key 进行身份认证。该目录不包含实时流式交互能力，如需低延迟流式 ASR 或 TTS，请参考 [音视频（非实时）](../../raw/model-api-reference/audio-api-directory.md) 中明确标注的例外接口。

## 支持的模型与功能

当前目录下支持以下功能模块，每个模块对应独立的模型与服务端点：

- **语音识别（ASR）**：支持多语种转写，基于 Qwen-Audio-ASR 系列模型，详见 [语音识别](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference.md)  
- **语音合成（TTS）**：提供高自然度中文语音生成，支持音色、语速、语调调节，详见 [语音合成](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference.md)  
- **音频打标（Audio Captioning）**：对输入音频生成结构化描述（如场景、情绪、声源事件），基于 Qwen-Audio-ASR-Captioner 模型，详见 [音频打标](../../raw/model-api-reference/audio-api-directory/qwen-audio-asr-captioner-http-api.md)  
- **音频生成（Audio Generation）**：支持文本到音频（T2A）生成，当前仅开放基础音效与简单播报类音频，详见 [音频生成](../../raw/model-api-reference/audio-api-directory/audio-generation-api.md)  
- **音视频翻译（AV Translation）**：支持音视频文件输入→目标语言字幕/文本输出，注意该能力实际调用的是离线批量翻译流水线，非实时流式翻译，详见 [音视频翻译](../../raw/model-api-reference/audio-api-directory/qwen3-livetranslate-flash-api.md)

> **注意**：[音视频翻译](../../raw/model-api-reference/audio-api-directory/qwen3-livetranslate-flash-api.md) 文档标题含 “live” 字样，但其接口行为为全量文件上传+异步回调，与实时流式无实质关联；请以接口实际请求方式和响应字段（如 `task_id`、`status`）为准，勿被命名误导。

## 关键参数

所有 Audio API 均要求以下通用参数：

- `model`: 必填，字符串，取值须为目录中各子文档明确列出的合法模型名（如 `"qwen-audio-asr-v1"`、`"qwen-tts-v2"`），不支持通配符或别名  
- `input`: 必填，对象，结构因功能而异（如 ASR 要求 `audio_url` 或 `audio_bytes`，TTS 要求 `text`），具体见各子文档的 [请求体示例](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference.md)  
- `response_format`: 可选，字符串，支持 `"json"`（默认）或 `"srt"`（仅部分 ASR/TTS 接口支持字幕格式）  

部分接口支持高级控制参数，例如：
- ASR：`language`, `diarization`, `word_timestamps`（见 [语音识别](../../raw/model-api-reference/audio-api-directory/speech-recognition-api-reference.md)）  
- TTS：`voice`, `speed`, `pitch`（见 [语音合成](../../raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference.md)）  
- 音频生成：`duration`, `noise_level`（见 [音频生成](../../raw/model-api-reference/audio-api-directory/audio-generation-api.md)）

## 使用方式

1. **鉴权**：在 HTTP Header 中携带 `Authorization: Bearer <api_key>`  
2. **请求**：向对应接口 URL（如 `POST https://dashscope.aliyuncs.com/api/v1/services/aigc/audio/asr`）发送 JSON body  
3. **异步任务**：对于耗时较长的操作（如长音频打标、音视频翻译），响应返回 `task_id`，需轮询 `GET /api/v1/tasks/{task_id}` 获取结果  
4. **错误处理**：统一遵循 RFC 7807 格式，`error.code` 为平台定义错误码（如 `InvalidParameter`、`AudioTooLong`），详情参见 [概述](../../raw/model-api-reference/audio-api-directory/audio-api-references.md)

## 限制和注意事项

- **文件大小限制**：单次请求音频文件 ≤ 100 MB（MP3/WAV/FLAC），超限将返回 `400 Bad Request` 与 `AudioTooLarge` 错误码  
- **时长限制**：ASR/TTS 单次请求音频时长 ≤ 60 分钟；音频生成单次输出时长 ≤ 30 秒  
- **并发限制**：免费版账户默认 5 QPS，企业版按配额配置，超出将返回 `429 Too Many Requests`  
- **音频格式**：仅支持 PCM（16-bit, 16kHz/44.1kHz）、MP3、WAV、FLAC；不支持 AMR、OPUS 等编码（即使后缀为 `.wav` 但内部为 OPUS 编码亦会失败）  
- **地域约束**：所有 Audio API 当前仅部署于 `cn-shanghai` 地域，跨地域调用可能失败或延迟激增  

> **注意**：[音频打标](../../raw/model-api-reference/audio-api-directory/qwen-audio-asr-captioner-http-api.md) 文档中提及的 `"scene_detection": true` 参数，在 v2.3.0+ 服务版本中已被移除，实际调用将忽略该字段；最新支持的能力请以 `/models` 接口返回的模型元数据为准。

## 来源文档

- [音视频（非实时）](../../raw/model-api-reference/audio-api-directory.md)


