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

所有音频 API 共享以下通用参数（部分参数为特定接口必需）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen2-audio-asr`；必须与所选功能匹配 |
| `audio_url` 或 `audio` | string / binary | 是 | 音频源：`audio_url` 指向公网可访问的 WAV/MP3/FLAC 文件（≤100MB），或直接以 `audio` 字段提交 base64 编码二进制数据（≤25MB） |
| `response_format` | string | 否 | 返回格式，可选 `json`（默认）或 `wav`（仅 TTS 和 Audio Generation 支持） |
| `stream` | boolean | 否 | 是否启用流式响应（仅 ASR、TTS、Conversation 支持）；设为 `true` 时返回 `text/event-stream` |

> **注意**：`audio_generation` 接口的 `prompt` 字段在 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md) 中定义为必填，但最新 SDK v2.3+ 已允许空 prompt 生成无条件音频——请以该文档为准，避免因旧版文档遗漏导致 400 错误。

## 使用方式

1. **认证**：在 HTTP Header 中携带 `Authorization: Bearer <api_key>`  
2. **请求**：向 `https://dashscope.aliyuncs.com/api/v1/audio/{endpoint}` 发送 POST 请求，其中 `{endpoint}` 为对应功能路径（如 `/asr`, `/tts`, `/st`）  
3. **示例（ASR）**：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/audio/asr" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen2-audio-asr",
           "audio_url": "https://example.com/audio.wav",
           "language": "zh"
         }'
   ```

完整调用示例与错误码说明参见 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 文档。

## 限制和注意事项

- 单次请求音频时长上限：ASR ≤ 600 秒，TTS ≤ 300 秒，Audio Generation ≤ 120 秒，ST ≤ 300 秒  
- 音频采样率要求：WAV/FLAC 建议 16kHz/16bit 单声道；MP3 建议 ≤ 192kbps  
- 流式响应下，ASR 的 `partial_result` 可能包含未最终确认文本，需监听 `is_final: true` 字段  
- 所有音频接口均不支持实时麦克风流输入（即 WebRTC 直连），仅接受文件 URL 或 base64 数据  
- 跨区域调用（如杭州节点调用上海模型）可能导致延迟升高，建议就近选择 endpoint  

如遇模型不可用或参数校验失败，请优先核对 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 中的模型兼容性表格。

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


