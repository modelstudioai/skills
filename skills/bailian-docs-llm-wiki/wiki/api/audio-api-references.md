# audio api references

百炼平台提供统一的音频类 API 接口，覆盖语音识别、语音合成、音乐生成、语音翻译和语音对话五大能力。所有接口均通过 RESTful 方式调用，支持流式响应与非流式响应两种模式。开发者需使用有效的 API Key 并遵循各模型的输入格式与计费规则。

## 支持的模型/功能

当前支持以下五类音频处理能力，每类对应独立的 API 端点与模型选型：

- **语音识别（ASR）**：支持中文、英文及多语种混合识别，推荐模型 `asr-general-v2`；  
- **语音合成（TTS）**：支持音色定制与情感控制，主流模型为 `tts-1` 和 `tts-1-hd`；  
- **音乐生成**：支持文本生成背景音乐或完整乐曲，模型 `musicgen-0.5` 为默认版本；  
- **语音翻译**：支持端到端语音→目标语言文本/语音输出，仅限 `speech-translate-v1` 模型；  
- **语音对话**：实时双工语音交互，依赖 `voice-conversation-v1` 模型，需 WebSocket 连接。  

详细能力说明与模型列表见 [音频](../../raw/model-api-reference/audio-api-references.md)。

## 关键参数

所有音频 API 共享以下基础参数（部分接口有扩展字段）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `asr-general-v2`，必须与所选功能匹配；具体取值参考 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 等子文档 |
| `audio_url` 或 `audio_bytes` | string / base64 | 是（二选一） | 音频源：远程 URL（需公网可访问）或 Base64 编码的原始 PCM/WAV/MP3 数据；注意 `audio_bytes` 最大限制为 25 MB |
| `response_format` | string | 否 | 返回格式，可选 `json`（默认）、`text`、`srt`（仅 ASR/TTS）；详见 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 文档 |

> **注意**：`sample_rate` 参数在 [音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md) 中要求固定为 32000 Hz，但 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 明确支持 8k–48k 动态采样率——若同时调用多个音频 API，请按具体接口文档校验参数兼容性。

## 使用方式

1. **认证**：在 HTTP Header 中携带 `Authorization: Bearer <api_key>`；  
2. **请求**：向对应端点（如 `POST https://dashscope.aliyuncs.com/api/v1/audio/speech-to-text`）发送 JSON 请求体；  
3. **响应**：成功时返回 `200 OK`，结构含 `output` 字段；错误时返回标准 `code` 与 `message`（如 `InvalidAudioFormat`）；  
4. **流式支持**：ASR、TTS、Voice Conversation 支持 `Accept: text/event-stream`，其余接口暂不支持。

## 限制和注意事项

- 单次请求音频时长上限：ASR ≤ 600 秒，TTS ≤ 120 秒，Music Generation ≤ 30 秒，Speech Translation ≤ 300 秒；  
- 所有音频文件须为单声道（mono），采样精度建议 16-bit；WAV 格式需含 RIFF 头，MP3 需为标准 CBR/VBR 编码；  
- 语音对话（Voice Conversation）必须使用 WebSocket 协议并维持心跳（`ping/pong`），超时断连后上下文不保留；  
- 免费额度仅适用于 `asr-general-v2` 和 `tts-1`，其他模型按实际调用量计费；详情参见 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 的配额说明。

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


