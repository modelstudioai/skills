# audio api references

百炼平台提供统一的音频类 API 接口，覆盖语音合成、语音识别、音频/音乐生成、语音对话及语音翻译等核心能力。所有接口均通过 RESTful 方式调用，支持流式响应与非流式响应两种模式。开发者需使用有效的 API Key 并遵循各模型的输入格式与配额限制。

## 支持的模型与功能

当前支持以下六大音频处理能力，对应独立的 API 端点与模型标识：

- **语音合成（TTS）**：支持多语种、多音色、可调节语速/音调，模型如 `qwen2-audio-tts-0.5b`；详见 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md)  
- **语音识别（ASR）**：支持中英文混合识别、标点恢复、说话人分离（部分模型），模型如 `qwen2-audio-asr-1b`；详见 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md)  
- **音频生成（Audio Generation）**：基于文本生成环境音、音效、简单语音片段，不支持长语音或复杂语义；详见 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md)  
- **音乐生成（Music Generation）**：支持旋律+节奏控制、BPM/风格提示词，输出为 WAV/MP3；详见 [音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md)  
- **语音对话（Voice Conversation）**：端到端实时语音交互，含唤醒、VAD、TTS 合成闭环，需 WebSocket 连接；详见 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md)  
- **语音翻译（Speech Translation）**：支持源语言语音→目标语言文本/语音双路径输出，当前仅开放中↔英互译；详见 [语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md)

> **注意**：[语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 文档中提及的 `v1.2` 协议版本已废弃，实际服务仅接受 `v2.0` WebSocket 消息格式；请以最新 SDK 示例为准，避免连接失败。

## 关键参数

所有音频 API 共享以下通用参数（部分接口有扩展）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型 ID，如 `qwen2-audio-tts-0.5b`，不可省略 |
| `input` | object | 是 | 输入结构体，具体字段依功能而异（如 `text`、`audio_url`、`audio_bytes`） |
| `parameters` | object | 否 | 可选配置项，如 `voice`, `speed`, `temperature`, `top_p` 等 |
| `stream` | boolean | 否 | 是否启用流式响应（仅 TTS、ASR、Voice Conversation 支持） |

> **注意**：`input.audio_bytes` 字段在 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 和 [语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md) 中要求 Base64 编码的原始 PCM/WAV 数据（16-bit, 16kHz 单声道），而 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md) 接受任意格式 URL，二者输入规范不一致，请严格按对应文档校验。

## 使用方式

1. **认证**：在 HTTP Header 中携带 `Authorization: Bearer <api_key>`  
2. **请求方法**：全部使用 `POST`，Content-Type 为 `application/json`  
3. **Endpoint**：统一前缀 `https://dashscope.aliyuncs.com/api/v1/services/aigc/audio`，后接子路径（如 `/tts`, `/asr`, `/music`）  
4. **示例（TTS）**：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/audio/tts" \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen2-audio-tts-0.5b",
           "input": {"text": "你好，欢迎使用百炼音频 API。"},
           "parameters": {"voice": "zhitian_003", "speed": 1.0}
         }'
   ```

## 限制和注意事项

- 单次请求音频时长上限：ASR/ST 最长 60 秒，TTS 输出最长 120 秒，音乐生成最长 30 秒  
- 文件上传：`audio_url` 必须为公网可访问 HTTPS 地址，且响应头需包含 `Content-Length`；`audio_bytes` 总大小 ≤ 10 MB  
- 流式响应需设置 `stream=true`，并按 SSE 格式解析 `data:` 块；未正确处理可能导致连接中断  
- 所有音频 API 均不支持跨区域调用（例如华东地域密钥不可调用华北节点），请确保 endpoint 与密钥所属 region 一致  
- 错误码统一遵循 [API 错误码规范](../../raw/common/error-codes.md)，其中 `InvalidInput.AudioFormat` 表示音频编码不被支持（如 MP3 未转 WAV 直接用于 ASR）

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


