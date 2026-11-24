# audio api directory

audio api directory 是百炼平台提供的非实时音视频处理能力集合，涵盖语音识别、语音合成、音频打标、音频生成及音视频翻译等核心场景。所有接口均采用 HTTP RESTful 设计，支持 JSON 请求/响应格式，适用于离线批量处理或低延迟非实时任务。开发者需通过 API Key 鉴权，并遵循各子服务的输入输出规范。

## 支持的模型与功能

当前目录下包含以下五类能力：
- **语音识别（ASR）**：支持多语种、高噪环境下的转写，底层模型为 Qwen-Audio-ASR 系列；详见 [语音识别](raw/model-api-reference/audio-api-directory/speech-recognition-api-reference.md)  
- **语音合成（TTS）**：提供多音色、可控语速与情感的文本到语音服务；详见 [语音合成](raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference.md)  
- **音频打标（Audio Captioning）**：对音频内容生成结构化描述标签（如场景、情绪、声源类型），基于 [音频打标](raw/model-api-reference/audio-api-directory/qwen-audio-asr-captioner-http-api.md) 实现  
- **音频生成（Audio Generation）**：支持文生音频（text-to-audio）及音频风格迁移，调用 [音频生成](raw/model-api-reference/audio-api-directory/audio-generation-api.md) 接口  
- **音视频翻译（A/V Translation）**：面向中文↔英文等双语场景的端到端翻译，注意该能力在 [音视频翻译](raw/model-api-reference/audio-api-directory/qwen3-livetranslate-flash-api.md) 中定义为“Flash”模式，实际为非实时批处理，非流式服务  

> **注意**：原始文档中 `qwen3-livetranslate-flash-api.md` 标题含 “live” 字样，易误解为实时接口；但其说明文档明确限定为“单次上传完整音视频文件后异步返回结果”，与本目录“非实时”定位一致。请勿将其与未来可能上线的真正实时流式翻译 API 混淆。

## 关键参数

通用请求头需包含：
- `Authorization: Bearer <API_KEY>`  
- `Content-Type: multipart/form-data`（文件上传类）或 `application/json`（纯文本类）  

各接口共性参数包括：
- `model`: 必填，取值如 `qwen-audio-asr-zh`, `qwen-tts-en-01`, `qwen-audio-captioner-v1` 等，具体枚举见对应子文档  
- `audio_url` 或 `file`: 二选一，支持公网可访问 URL 或 base64 编码音频（≤50MB，格式限 WAV/MP3/FLAC/M4A）  
- `response_format`: 可选 `json`（默认）或 `srt`（仅 ASR/TTS 支持）  

## 使用方式

1. 构造 POST 请求至对应子接口 endpoint（如 ASR 为 `/api/v1/audio/asr`）  
2. 按需携带 `model`、音频源及可选参数（如 `language`, `speaker`, `prompt`）  
3. 解析响应体中的 `result` 字段（结构因接口而异，ASR 返回 text+segments，TTS 返回 audio_url）  
4. 异步任务需轮询 `job_id` 获取状态，详见 [概述](raw/model-api-reference/audio-api-directory/audio-api-references.md)  

## 限制和注意事项

- 单次请求音频时长上限为 30 分钟（ASR/TTS/Captioning）、5 分钟（Audio Generation）  
- 免费额度按调用量计费（每千次 ASR 请求 ≈ 1 小时音频处理），超出后按量计费  
- 所有音频文件将被临时存储 ≤24 小时用于处理与调试日志，不作长期留存  
- > **注意**：[音频打标](raw/model-api-reference/audio-api-directory/qwen-audio-asr-captioner-http-api.md) 文档中示例使用 `POST /v1/audio/caption`，但最新生产环境已统一为 `/api/v1/audio/caption` —— 请以 OpenAPI Schema 及控制台调试页为准，旧路径将逐步下线  
- 错误码统一遵循 RFC 7807，常见 `400 Bad Request` 表示参数校验失败，`413 Payload Too Large` 表示文件超限，`429 Too Many Requests` 触发速率限制（默认 10 QPS/Key）

## 来源文档

- [音视频（非实时）](../../raw/model-api-reference/audio-api-directory.md)


