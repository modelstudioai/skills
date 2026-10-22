# audio api references

百炼平台提供多种音频处理能力的 API，覆盖语音合成、语音识别、音频生成、语音对话及语音翻译等核心场景。所有接口均通过统一的 RESTful 方式调用，支持流式响应与[异步任务](../concepts/asynchronous-task.md)模式。开发者需根据具体任务类型选择对应模型与参数配置。

## 支持的模型/功能

当前支持以下五大类音频处理能力：
- **语音合成（TTS）**：支持多语种、多音色、可控语速与情感表达，详见 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md)  
- **语音识别（ASR）**：支持实时流式识别与长音频离线识别，含标点恢复与说话人分离选项，详见 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md)  
- **音频生成（Audio Generation）**：基于文本生成背景音乐、音效或语音风格音频，支持时长与风格控制，详见 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md)  
- **语音对话（Voice Conversation）**：端到端语音交互接口，集成 ASR + LLM + TTS，支持低延迟双工通信  
- **语音翻译（Speech Translation）**：支持源语音→目标语言文本/语音的直译，含中英日韩等主流语向，详见 [语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md)

> **注意**：[语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 文档中描述的 `enable_diarization` 参数在 v2.3.0+ 版本已更名为 `speaker_separation`，旧参数名将被弃用，请以最新 SDK 示例为准。

## 关键参数

通用必选参数（所有音频 API 共享）：
- `model`: 模型标识符（如 `qwen2-audio-tts-16k`、`qwen2-audio-asr-zh`），必须与功能类型匹配  
- `input`: 音频数据载体，支持 `audio_url`（公网可访问 HTTPS URL）或 `audio_bytes`（Base64 编码二进制）  
- `response_format`: 可选 `json`（默认）或 `stream`（仅部分接口支持）

功能特有参数示例：
- TTS：`voice`（音色 ID）、`speed`（0.5–2.0）、`emotion`（`neutral`/`happy`/`serious`）  
- ASR：`language`（`zh`/`en`/`auto`）、`word_timestamps`（布尔值）、`diarization`（已迁移至 `speaker_separation`）  
- Audio Generation：`duration`（秒，最大 30）、`style`（`ambient`/`cinematic`/`vocal`）

## 使用方式

1. **认证**：使用 `Authorization: Bearer <api_key>` 请求头  
2. **请求方法**：全部为 `POST`，Endpoint 统一为 `/v1/audio/<task>`（如 `/v1/audio/speech-to-text`）  
3. **响应结构**：成功时返回 `200 OK`，含 `output` 字段（文本结果、音频 URL 或字节流元信息）；错误时返回标准 `error.code` 与 `error.message`  
4. **流式调用**：对支持 `stream=true` 的接口（如 TTS、语音对话），响应体为 `text/event-stream`，按 SSE 协议解析 chunk  

## 限制和注意事项

- 单次请求音频时长上限：ASR 最长 600 秒，TTS 输出最长 120 秒，Audio Generation 最长 30 秒  
- 音频格式要求：WAV/MP3/FLAC/M4A，采样率 ≥ 8kHz，推荐 16kHz 单声道；ASR 输入建议 16kHz 16-bit PCM  
- 计费单位：ASR/TTS 按音频秒数计费，Audio Generation 按生成秒数计费，语音对话按会话时长计费  
- > **注意**：[音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md) 文档中列出的 `temperature` 参数在当前生产环境尚未开放，实际调用将被忽略，该字段将在下个版本文档中移除。

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


