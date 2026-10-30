# audio api references

百炼平台提供统一的音频处理 API 接口，覆盖语音合成、语音识别、音频生成、语音对话和语音翻译五大核心能力。所有接口均通过 RESTful 方式调用，支持流式响应与非流式响应两种模式。开发者需使用有效的 API Key 并遵循各模型的输入格式与计费规则。

## 支持的模型/功能

当前支持以下五类音频相关能力，对应独立的 API 端点与模型标识：

- **语音合成（TTS）**：支持多语种、多音色，可调节语速、语调、停顿；模型如 `qwen2-audio-tts-zh`、`qwen2-audio-tts-en`  
- **语音识别（ASR）**：支持中英文混合识别、带标点恢复、说话人分离（需开启 `diarization` 参数）  
- **音频生成（Audio Generation）**：基于文本生成背景音乐、音效或简单旋律，不支持长时序连贯语音生成  
- **语音对话（Voice Conversation）**：端到端实时语音交互，内置唤醒词检测与低延迟响应，依赖 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 文档定义的会话生命周期管理  
- **语音翻译（Speech Translation）**：支持语音→目标语言文本（ST），以及语音→目标语言语音（TTS+ST联合链路），具体能力边界详见 [语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md)

> **注意**：原始文档中将“语音对话”归类为独立能力，但其底层依赖 ASR + LLM + TTS 三阶段串联；实际调用时若启用 `enable_streaming=true`，必须按 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 规定的 WebSocket 协议交互，不可混用 HTTP POST 流式请求。

## 关键参数

通用必填参数（所有音频 API 共享）：
- `model`: 字符串，模型 ID（如 `qwen2-audio-asr`），不可省略  
- `input`: 对象，结构依任务而异（如 ASR 为 `{ "audio_url": "..." }`，TTS 为 `{ "text": "..." }`）  
- `parameters`: 可选对象，用于控制生成质量与行为（如 `temperature`, `top_p`, `sample_rate`）  

任务特有参数示例：
- ASR：`language`, `diarization`, `punctuation`（默认开启）  
- TTS：`voice`, `speed`, `pitch`  
- Audio Generation：`duration`, `style`, `instrumental_only`  
- 详细字段说明请参阅 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 等子文档。

## 使用方式

1. **认证**：在 HTTP Header 中携带 `Authorization: Bearer <api_key>`  
2. **请求方法**：全部使用 `POST`，Content-Type 为 `application/json`  
3. **音频输入**：仅接受公网可访问的 `audio_url`（HTTP/HTTPS），暂不支持 Base64 或 multipart/form-data 上传  
4. **响应格式**：成功时返回 `200 OK`，含 `output` 字段（文本、音频 URL 或结构化结果）；错误时返回标准 `error.code` 与 `error.message`  

## 限制和注意事项

- 单次请求音频时长上限：ASR/TTS ≤ 120 秒，Audio Generation ≤ 30 秒，语音对话单轮 ≤ 60 秒  
- 音频格式要求：仅支持 `wav`, `mp3`, `m4a`, `flac`；采样率建议 16kHz 或 44.1kHz，位深 16bit  
- 所有音频 URL 必须支持 `HEAD` 请求且返回有效 `Content-Length`，否则触发 `invalid_audio_url` 错误  
- 语音翻译的 `target_language` 必须与模型支持的语言集严格匹配，不支持运行时自动检测目标语种  
- > **注意**：[语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 文档中提及的 `enable_word_timestamps=true` 在 v2.3.0+ 版本已弃用，应改用 `word_level_timestamps=true`，旧参数将返回 400 错误

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


