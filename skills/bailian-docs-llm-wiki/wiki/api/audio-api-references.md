# audio api references

百炼平台提供统一的音频处理 API 接口，覆盖语音合成、语音识别、音频生成、语音对话和语音翻译五大核心能力。所有接口均通过 RESTful 方式调用，支持流式响应与非流式响应两种模式。开发者需使用有效的 API Key 并遵循各模型的输入格式与计费规则。

## 支持的模型/功能

当前支持以下五类音频相关能力，对应独立的 API 端点与模型标识：

- **语音合成（TTS）**：支持多语种、多音色，模型如 `qwen2-audio-tts-zh`、`qwen2-audio-tts-en`；详见 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md)  
- **语音识别（ASR）**：支持中英文混合识别、带标点自动断句，模型如 `qwen2-audio-asr`；详见 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md)  
- **音频生成（Audio Generation）**：支持文本到音频（如环境音、音效）、文本+参考音频生成；详见 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md)  
- **语音对话（Voice Conversation）**：端到端实时语音交互，含唤醒、VAD、TTS 与 ASR 集成；详见 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md)  
- **语音翻译（Speech Translation）**：支持语音输入→目标语言文本/语音双模输出，当前仅开放中英互译；详见 [语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md)

> **注意**：原始文档中 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 提及支持“离线唤醒词配置”，但该能力已在 v2.3.0 版本后移除，实际仅支持服务端触发，最新行为以 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 的「请求参数」章节中 `trigger_mode` 字段说明为准。

## 关键参数

通用必填参数（所有音频 API 共享）：
- `model`: 模型 ID（如 `qwen2-audio-asr`），不可省略  
- `input.audio_url` 或 `input.audio_bytes`: 二选一，推荐使用 `audio_url`（支持 HTTPS 公网可访问地址，有效期 ≥10 分钟）  
- `output_format`: 输出编码格式，如 `mp3`、`wav`、`pcm`（仅部分模型支持）  

功能特有参数示例：
- TTS：`voice`（音色 ID）、`speed`（0.5–2.0）、`pitch`（-5–5）  
- ASR：`language`（`zh`/`en`/`auto`）、`enable_punctuation`（布尔值）  
- Audio Generation：`duration_seconds`（最大 30）、`reference_audio_url`（可选）  

## 使用方式

1. 构造 POST 请求至对应 API 端点（如 `https://dashscope.aliyuncs.com/api/v1/services/aigc/audio-generation`）  
2. 设置 Header：`Authorization: Bearer YOUR_API_KEY`、`Content-Type: application/json`  
3. Body 为 JSON，结构遵循各子文档定义；例如语音识别请求体必须包含 `input.audio_url` 和 `model` 字段  
4. 响应状态码 `200` 表示成功，流式接口返回 `application/octet-stream`，非流式返回标准 JSON（含 `output.text` 或 `output.audio_url`）

## 限制和注意事项

- 单次请求音频时长上限：ASR ≤ 60 秒，TTS ≤ 120 秒，Audio Generation ≤ 30 秒  
- 文件大小限制：`audio_bytes` 方式 ≤ 10 MB；`audio_url` 方式无平台侧限制，但需确保服务端可稳定下载  
- 所有音频接口暂不支持跨区域调用（如杭州 region 账号不可调用上海 endpoint）  
- 采样率要求：ASR/TTS 推荐 16kHz 单声道 PCM；Audio Generation 输入建议 24kHz/48kHz，否则可能降质  
- > **注意**：[音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md) 文档中示例使用 `input.text` 作为唯一输入字段，但实际 v2.1.0+ 版本已强制要求同时传入 `input.prompt`（用于风格控制），遗漏将返回 `400 Bad Request` —— 请以该文档最新版「请求体示例」为准。

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


