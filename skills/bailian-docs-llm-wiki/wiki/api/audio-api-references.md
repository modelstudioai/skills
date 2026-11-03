# audio api references

百炼平台提供统一的音频处理 API 接口，覆盖语音合成、语音识别、音频生成、语音对话和语音翻译五大核心能力。所有接口均通过 RESTful 方式调用，支持流式响应与非流式响应两种模式。开发者需使用有效的 API Key 并遵循各模型的输入格式与计费规则。

## 支持的模型/功能

当前音频 API 支持以下功能模块，每个模块对应独立的模型与服务端点：

- **语音合成（TTS）**：支持多语种、多音色、可调节语速/音调，模型包括 `qwen2-audio-tts-zh` 和 `qwen2-audio-tts-en`  
- **语音识别（ASR）**：支持中英文混合识别、带标点恢复、说话人分离（需开启 `diarization` 参数），模型为 `qwen2-audio-asr`  
- **音频生成（Audio Generation）**：基于文本生成背景音乐、音效或完整音频片段，模型为 `qwen2-audio-gen`  
- **语音对话（Voice Conversation）**：端到端语音交互，支持唤醒词检测、上下文保持与低延迟响应，模型为 `qwen2-audio-conversation`  
- **语音翻译（Speech Translation）**：支持语音→目标语言文本、语音→目标语言语音双路径，模型为 `qwen2-audio-st`  

各功能详细说明见 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md)、[语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 和 [语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md)。

## 关键参数

通用请求头（必填）：
- `Authorization: Bearer <api_key>`
- `Content-Type: application/json`

核心请求体字段（按功能略有差异）：
- `model`: 模型标识符（如 `"qwen2-audio-asr"`），不可省略  
- `input`: 音频数据载体，支持 `audio_url`（公网可访问 HTTPS URL）或 `audio_base64`（需 Base64 编码且 ≤ 25 MB）  
- `parameters`: 对象，常见字段包括：  
  - `language`: 输入/输出语言代码（如 `"zh"`、`"en"`），ASR 和 ST 必填  
  - `response_format`: `"json"` 或 `"text"`（仅部分接口支持）  
  - `stream`: `true` / `false`，控制是否启用 SSE 流式响应  
  - `voice`: TTS 专用，指定音色 ID（如 `"zhiyuan"`）  

> **注意**：`audio_base64` 字段在 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md) 中要求必须为 PCM 编码（16-bit, 16kHz, mono），而 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 文档未明确此限制，实际调用时若传入 MP3 Base64 将返回 `400 Bad Request` —— 请以 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 的最新行为为准。

## 使用方式

1. 构造 POST 请求至对应 endpoint（例如 ASR：`https://dashscope.aliyuncs.com/api/v1/services/aigc/audio/asr`）  
2. 在请求体中传入 `model`、`input` 和必要 `parameters`  
3. 解析响应：非流式返回 JSON；流式响应需按 SSE 协议解析 `data:` 行  
4. 错误处理：关注 `HTTP status code`（如 `429` 表示限流）及响应体中 `code` 字段（如 `"InvalidParameter"`）

示例（ASR 简单调用）：
```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/audio/asr" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "qwen2-audio-asr",
        "input": {"audio_url": "https://example.com/audio.wav"},
        "parameters": {"language": "zh"}
      }'
```

## 限制和注意事项

- 单次请求音频时长上限：ASR 和 ST ≤ 600 秒；TTS 输入文本 ≤ 5000 字符；Audio Generation 输入文本 ≤ 200 字符  
- 音频格式要求：WAV/MP3/FLAC/M4A（采样率 8–48 kHz，位深 16-bit），不支持视频容器（如 MP4 中的音频轨需先提取）  
- 计费单位：ASR/ST 按音频秒数计费；TTS/Audio Generation 按输出音频秒数计费；Voice Conversation 按会话时长（秒）计费  
- 所有接口均不支持跨区域调用（例如华东 region 的 key 不可调用华北 endpoint）  

请务必参考各子功能的原始文档确认最新兼容性，例如 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 中关于 WebSocket 连接保活机制的说明已更新，旧版 SDK 可能存在超时断连问题。

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


