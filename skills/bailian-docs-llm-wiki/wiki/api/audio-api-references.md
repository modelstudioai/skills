# audio api references

百炼平台提供多种音频处理能力的 API 接口，覆盖语音识别、语音合成、音乐生成、语音翻译和语音对话五大核心场景。所有接口均通过统一的 RESTful API 调用，支持标准 HTTP 请求与 JSON 响应格式。开发者需使用有效的 API Key 并遵循各模型的输入/输出规范。

## 支持的模型与功能

当前音频类 API 包含以下功能模块（按生产可用性排序）：
- **语音识别（ASR）**：支持中英文混合识别、实时流式识别及离线音频转写  
- **语音合成（TTS）**：提供多音色、多语种、可调节语速/语调的高质量语音生成  
- **音乐生成**：支持文本生成背景音乐（BGM）、旋律片段或完整曲目（需指定风格与时长）  
- **语音翻译（ST）**：端到端语音→目标语言文本翻译（暂不支持语音→语音直出）  
- **语音对话（Voice Chat）**：基于大模型的语音交互能力，支持唤醒词、上下文连续对话与意图理解  

> **注意**：语音对话功能在 [音频 (raw/model-api-reference/audio-api-references.md)](../../raw/model-api-reference/audio-api-references.md) 中描述为“支持语音唤醒与多轮对话”，但最新 SDK v2.3.0 文档明确指出该能力目前仅限 WebRTC 流式接入且不支持自定义唤醒词——请以 [语音对话 (raw/model-api-reference/voice-conversation-api-references.md)](../../raw/model-api-reference/voice-conversation-api-references.md) 的实际参数说明为准。

## 关键参数

所有音频 API 共享以下基础参数（必填）：
- `model`: 模型标识符（如 `paraformer-v1`、`cosyvoice-v1`、`musicgen-v2`）  
- `input.audio_url` 或 `input.audio_bytes`: 音频源（推荐使用 `audio_url` 指向 OSS 或公网可访问 URL；若传 `audio_bytes`，需 Base64 编码且总大小 ≤ 25 MB）  
- `parameters`: 功能特化配置对象（详见各子文档）  

各功能特有参数示例：
- ASR：`parameters.language`（`zh`/`en`/`auto`）、`parameters.word_timestamps`（布尔值）  
- TTS：`parameters.voice`（音色 ID）、`parameters.speech_rate`（-50 ~ +100）  
- 音乐生成：`parameters.duration`（秒，10–180）、`parameters.style`（`pop`/`cinematic`/`lofi` 等）  

完整参数列表请参考 [音频 (raw/model-api-reference/audio-api-references.md)](../../raw/model-api-reference/audio-api-references.md)。

## 使用方式

1. **认证**：在请求 Header 中携带 `Authorization: Bearer <API_KEY>`  
2. **请求方法**：`POST /v1/audio/<task>`（`<task>` 为 `transcribe`/`synthesize`/`generate_music`/`translate_speech`/`converse`）  
3. **请求体**：JSON 格式，结构符合 [语音识别](https://help.aliyun.com/zh/model-studio/speech-recognition-api-reference) 等官方文档要求  
4. **响应**：成功返回 `200 OK`，含 `output.text`（ASR/ST）、`output.audio_url`（TTS/音乐）、或 `output.conversation_id`（语音对话）  

## 限制和注意事项

- 单次请求音频时长上限：ASR/TTS ≤ 120 秒，音乐生成 ≤ 180 秒，语音翻译 ≤ 90 秒  
- 音频格式要求：WAV/MP3/OGG/M4A（采样率 ≥ 8 kHz，推荐 16 kHz；单声道优先）  
- 错误重试：网络超时建议设置 30s+，服务端错误（如 `503`）需指数退避重试  
- 计费单位：ASR/TTS 按音频秒数计费，音乐生成按生成时长计费，语音对话按会话分钟计费  
- **重要**：语音翻译（ST）当前仅支持 `zh→en` 和 `en→zh` 方向，其他语种组合将返回 `400 Bad Request` —— 此限制未在 [音频 (raw/model-api-reference/audio-api-references.md)](../../raw/model-api-reference/audio-api-references.md) 中明确说明，需以各子功能 API 参考文档为准。

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


