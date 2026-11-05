# audio api references

百炼平台提供统一的音频处理 API 接口，覆盖语音合成、语音识别、音频生成、语音对话和语音翻译五大核心能力。所有接口均通过 RESTful 方式调用，支持流式响应与非流式响应两种模式。开发者需使用有效的 API Key 并遵循各模型的输入格式与计费规则。

## 支持的模型/功能

当前支持以下五类音频相关能力，对应独立的 API 端点与模型标识：

- **语音合成（TTS）**：支持多语种、多音色，模型如 `qwen2-audio-tts-01`；详见 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md)  
- **语音识别（ASR）**：支持长音频转写、实时流式识别，模型如 `qwen2-audio-asr-02`；详见 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md)  
- **音频生成（Audio Generation）**：支持文本到音频（如旁白、音效）、音频风格迁移等，模型如 `qwen2-audio-gen-03`；详见 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md)  
- **语音对话（Voice Conversation）**：端到端语音交互，含唤醒、理解、合成闭环，仅限授权设备 SDK 集成；详见 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md)  
- **语音翻译（Speech Translation）**：支持源语音→目标语言文本/语音双路径输出，模型如 `qwen2-audio-st-01`；详见 [语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md)

> **注意**：[语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 文档中提及的 `v1.5` 协议版本已下线，实际生产环境仅支持 `v2.0` WebSocket 协议，旧版 HTTP 轮询方式不再可用。

## 关键参数

通用必填参数（所有音频 API 共享）：
- `model`: 字符串，必须为文档中明确列出的模型 ID（如 `qwen2-audio-asr-02`），不可自行构造或省略  
- `input`: 对象，结构依能力而异（如 ASR 为 `{ "audio_url": "..." }`，TTS 为 `{ "text": "..." }`）  
- `parameters`: 可选对象，常见字段包括 `sample_rate`（Hz）、`response_format`（`json` / `wav` / `mp3`）、`stream`（布尔值）  

部分能力特有参数：
- TTS：`voice`（音色 ID）、`speed`（0.5–2.0）、`pitch`（-5–5）  
- ASR：`language`（自动检测时设为 `auto`）、`diarization`（是否启用说话人分离）  
- Audio Generation：`duration`（秒，最大 30）、`prompt`（可选控制描述）

## 使用方式

1. **认证**：在请求 Header 中携带 `Authorization: Bearer <API_KEY>`  
2. **请求地址**：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/audio/<service_name>`，其中 `<service_name>` 为 `speech-synthesis`、`speech-recognition` 等（与子文档路径末段一致）  
3. **示例（ASR）**：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/audio/speech-recognition" \
     -H "Authorization: Bearer sk-xxx" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen2-audio-asr-02",
           "input": {"audio_url": "https://example.com/audio.wav"},
           "parameters": {"language": "zh", "stream": false}
         }'
   ```

## 限制和注意事项

- 单次请求音频时长上限：ASR 和语音翻译 ≤ 60 分钟；TTS 输入文本 ≤ 5000 字符；音频生成 ≤ 30 秒  
- 音频格式要求：ASR/TTS/ST 仅支持 `wav`、`mp3`、`m4a`、`flac`；采样率建议 16kHz 或 44.1kHz，位深 16bit  
- 流式响应仅支持 `wav` 格式（`response_format=wav` 且 `stream=true`），其他格式返回 400 错误  
- > **注意**：[音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md) 文档中“支持 60 秒生成”为历史版本描述，当前服务端强制截断至 30 秒，该限制已在最新 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 文档中同步更新，以实际 API 响应为准。

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


