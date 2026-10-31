# audio api references

百炼平台提供统一的音频类 API 接口，覆盖语音合成、语音识别、音频生成、语音对话及语音翻译五大核心能力。所有接口均通过 RESTful 方式调用，支持 JSON 格式请求与响应，并遵循统一的鉴权与错误码规范。开发者需根据具体任务选择对应模型与参数组合，详见各子模块文档。

## 支持的模型与功能

当前支持以下五类音频处理能力，每类对应独立的 API 端点与模型选型：

- **语音合成（TTS）**：支持多语种、多音色、可控语速/语调的文本转语音，模型包括 `qwen2-audio-tts-zh`, `qwen2-audio-tts-en` 等；  
- **语音识别（ASR）**：支持中英文混合识别、带标点恢复、说话人分离（需开启 `diarization`），模型如 `qwen2-audio-asr-v1`；  
- **音频生成（Audio Generation）**：基于文本生成背景音乐、音效或语音风格音频，模型为 `qwen2-audio-gen-v1`；  
- **语音对话（Voice Conversation）**：端到端语音交互，支持流式输入/输出与上下文保持，依赖 `qwen2-audio-conversational-v1`；  
- **语音翻译（Speech Translation）**：支持语音→目标语言文本/语音双路径输出，模型含 `qwen2-audio-st-zh2en` 等；  

各能力详情请参阅 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md)、[语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 和 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md) 的独立参考文档。

## 关键参数

通用必填参数（所有音频 API 共享）：
- `model`: 字符串，指定模型 ID（如 `"qwen2-audio-asr-v1"`），不可省略；  
- `input`: 对象，结构依能力而异（如 ASR 为 `{"audio_url": "..."}`，TTS 为 `{"text": "..."}`）；  
- `parameters`: 可选对象，用于控制生成质量、时长、采样率等（如 `{"sample_rate": 16000, "voice": "zhiyan"}`）；  

> **注意**：`parameters` 中 `temperature` 在 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 中有效，但在 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 中被忽略——后者使用 `speed` 和 `pitch` 替代随机性控制。

## 使用方式

1. **认证**：在 HTTP Header 中携带 `Authorization: Bearer <api_key>`；  
2. **请求**：向对应 endpoint（如 `POST https://dashscope.aliyuncs.com/api/v1/services/aigc/audio-generation`）发送 POST 请求；  
3. **响应**：成功返回 `200`，`output.audio_url` 或 `output.text` 为结果；流式接口（如语音对话）需按 SSE 协议解析事件流；  
4. **调试建议**：首次调用前务必查阅 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 中的流式连接示例与心跳机制说明。

## 限制和注意事项

- 单次请求音频时长上限：ASR ≤ 60 秒，TTS ≤ 500 字符，Audio Generation ≤ 30 秒；  
- 所有音频文件需为 PCM/WAV/MP3/M4A 格式，采样率建议 8–48 kHz，单声道优先；  
- 语音翻译暂不支持实时流式输入，仅接受完整音频片段；  
- 错误码 `429 Too Many Requests` 表示超出模型 QPS 限制，需检查配额或启用异步模式；  
- [异步任务](../concepts/asynchronous-task.md)（如长音频 ASR）需轮询 `task_id` 获取结果，超时时间为 10 分钟，详见 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 文档。

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


