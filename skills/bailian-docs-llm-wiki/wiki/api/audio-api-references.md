# audio api references

百炼平台提供统一的音频类 API 接口，覆盖语音合成、语音识别、音频生成、语音对话和语音翻译五大能力。所有接口均通过 RESTful 方式调用，支持流式响应与非流式响应两种模式。开发者需使用有效的 API Key 并遵循各模型的输入格式与配额限制。

## 支持的模型/功能

当前支持以下五类音频处理能力，对应独立的 API 端点与模型标识符：

- **语音合成（TTS）**：支持多语种、多音色，模型如 `qwen2-audio-tts-0.5b`；详见 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md)  
- **语音识别（ASR）**：支持长音频分段识别与实时流式识别，模型如 `qwen2-audio-asr-1b`；详见 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md)  
- **音频生成（Audio Generation）**：支持文本到音频（text-to-audio）、音频风格迁移等，模型如 `qwen2-audio-gen-2b`；详见 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md)  
- **语音对话（Voice Conversation）**：端到端语音交互，含唤醒、理解、合成闭环；详见 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md)  
- **语音翻译（Speech Translation）**：支持源语音→目标文本/目标语音双路径输出，模型如 `qwen2-audio-st-1.5b`；详见 [语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md)

> **注意**：`qwen2-audio-asr-1b` 在 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 中标注为默认模型，但 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 文档中仍引用已下线的 `qwen-audio-dialog-asr-v1`，请以 ASR 文档为准。

## 关键参数

通用必填参数（所有音频 API 共享）：
- `model`: 字符串，模型 ID（如 `qwen2-audio-tts-0.5b`），不可省略  
- `input`: 对象，结构依能力而异（如 ASR 为 `{ "audio_url": "..." }`，TTS 为 `{ "text": "..." }`）  
- `parameters`: 可选对象，控制质量、时长、语速等（例如 `{"voice": "zhiyan", "speed": 1.0}`）  

流式请求需额外设置：
- `stream: true`（仅部分能力支持，详见各子文档）  
- `response_format`: 可选 `"mp3"`、`"wav"`、`"pcm"`（TTS 和 Audio Generation 支持；ASR 固定返回 JSON）

## 使用方式

1. **认证**：在 HTTP Header 中携带 `Authorization: Bearer <api_key>`  
2. **请求方法**：全部使用 `POST`  
3. **Endpoint**：统一为 `https://dashscope.aliyuncs.com/api/v1/audio/{service}`，其中 `{service}` 为 `tts`、`asr`、`audio_generation`、`voice_conversation` 或 `speech_translation`  
4. **示例（TTS）**：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/audio/tts" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen2-audio-tts-0.5b",
           "input": {"text": "你好，欢迎使用百炼音频 API。"},
           "parameters": {"voice": "zhiyan"}
         }'
   ```

## 限制和注意事项

- 单次请求音频时长上限：ASR 最长 600 秒，TTS 输出最长 120 秒，Audio Generation 最长 30 秒  
- 音频格式要求：输入仅支持 `mp3`、`wav`、`flac`、`m4a`（采样率 ≥ 8kHz，位深 ≥ 16bit）；不支持视频容器封装（如 `.mp4` 内嵌音频需先提取）  
- 流式响应仅支持 `text/event-stream` MIME 类型，客户端需正确处理 SSE 协议  
- > **注意**：[语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 文档中描述的 `session_id` 自动续期机制，与 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 中明确要求“每次请求必须新建 session”存在冲突；实际行为以 ASR 文档为准，语音对话暂不支持跨请求 session 复用。  
- 错误码统一遵循百炼平台标准（如 `400 Bad Request`、`429 Rate Limited`），具体含义见各子文档说明

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


