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
  - `voice`: TTS 专用，指定音色 ID（如 `"zhiyu"`）  

> **注意**：`audio_base64` 字段在 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md) 中要求必须为 PCM 16-bit 小端格式，而 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 同时支持 MP3/WAV/FLAC，二者对编码格式的要求存在不一致，请按具体接口文档校验。

## 使用方式

1. 构造 POST 请求至对应 endpoint（例如 ASR：`https://dashscope.aliyuncs.com/api/v1/services/aigc/audio/asr`）  
2. 在请求体中传入 `model`、`input` 及必要 `parameters`  
3. 解析响应：成功时返回 `output` 字段（含 `text`、`segments` 或 `audio_url` 等），错误时返回标准 `code` 与 `message`  

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

- 单次请求音频时长上限：ASR/ST ≤ 600 秒，TTS ≤ 300 秒，Audio Generation ≤ 120 秒  
- 非流式响应最大 payload 为 10 MB；流式响应需客户端持续读取 SSE event  
- 所有音频 URL 必须为 HTTPS 且可被服务端直连访问（内网地址、临时签名过期链接将失败）  
- 语音对话接口需配合 WebSocket 连接建立会话上下文，不支持纯 HTTP POST 调用 —— 具体协议细节参见 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md)  
- 计费按实际处理音频时长（秒）或生成 token 数计算，与请求次数无关  

> **注意**：原始文档中 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md) 提到支持 `style` 参数控制音乐风格，但该字段在 v2.3.0+ 版本已弃用，实际生效参数为 `prompt` + `negative_prompt`，请以最新 SDK 示例为准。

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


