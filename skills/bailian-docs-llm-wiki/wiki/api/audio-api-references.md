# audio api references

百炼平台提供多种音频处理能力的 API 接口，覆盖语音合成、语音识别、音频/音乐生成、语音对话及语音翻译等核心场景。所有接口均通过统一的 RESTful 设计对外暴露，支持流式响应与非流式响应两种模式。开发者需根据具体任务选择对应模型并配置关键参数，详见各子模块文档。

## 支持的模型与功能

当前支持以下六大类音频相关能力：

- **语音合成（TTS）**：支持多语种、多音色、可控韵律的文本转语音，模型包括 `qwen2-audio-tts-zh` 和 `qwen2-audio-tts-en`；  
- **语音识别（ASR）**：支持中英文混合识别、带标点恢复与说话人分离（需开启 `diarization`）；  
- **音频生成**：基于文本生成环境音、音效或语音片段（非音乐），适用于提示音、通知音等场景；  
- **音乐生成**：支持歌词/风格描述驱动的完整音乐片段生成，输出为 WAV/MP3 格式；  
- **语音对话**：端到端语音输入→理解→生成→语音输出的闭环交互，依赖 `qwen2-audio-chat` 模型；  
- **语音翻译**：支持源语音实时转译为目标语言文本，或直接合成目标语言语音（TTS+ASR 级联）。  

各能力细节请参阅 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md)、[语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 与 [音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md) 的原始文档。

## 关键参数

通用必填参数（所有音频 API 共享）：
- `model`: 模型标识符（如 `qwen2-audio-tts-zh`, `qwen2-audio-asr`），必须与所选功能匹配；  
- `input`: 输入结构体，类型因接口而异（如 ASR 为 `{"audio_url": "..."}`，TTS 为 `{"text": "..."}`）；  
- `response_format`: 可选 `"json"`（返回文本结果）或 `"wav"`/`"mp3"`（返回二进制音频流，仅部分接口支持）；  
- `stream`: 布尔值，控制是否启用流式响应（`true` 时需按 SSE 协议解析）。

功能特有参数示例：
- TTS：`voice`（音色 ID）、`speed`（0.5–2.0）、`pitch`（-10–10）；  
- ASR：`language`（`"zh"`/`"en"`/`"auto"`）、`diarization`（`true`/`false`）；  
- 音乐生成：`duration`（秒，最大 30）、`style`（如 `"pop"`, `"lofi"`）。

> **注意**：`response_format=wav` 在 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 中实际返回 base64 编码字符串而非原始二进制流，与 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 的行为不一致，请以最新 SDK 示例为准。

## 使用方式

1. **认证**：在请求 Header 中携带 `Authorization: Bearer <api_key>`；  
2. **请求地址**：`POST https://dashscope.aliyuncs.com/api/v1/audio/<endpoint>`，其中 `<endpoint>` 对应功能路径（如 `/tts`, `/asr`, `/music`）；  
3. **请求体**：JSON 格式，遵循各接口定义的 `input` 结构；  
4. **响应处理**：非流式响应直接解析 JSON；流式响应需按行解析 SSE 事件（`data:` 字段含 chunked audio 或 partial text）。

建议优先使用官方 Python/Node.js SDK，其已封装鉴权、重试、流式解码等逻辑。SDK 调用示例见 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 文档末尾。

## 限制和注意事项

- 单次请求音频时长上限：ASR ≤ 60 秒，TTS ≤ 1000 字符，音乐生成 ≤ 30 秒；  
- 所有音频 URL 必须可公开访问（HTTP/HTTPS），且响应头需包含 `Content-Type`（如 `audio/wav`）；  
- 不支持本地文件直传，必须先上传至 OSS 或提供可访问 URL；  
- 流式响应下，若连接中断，服务端不会自动重发已发送 chunk，客户端需自行实现断点续传逻辑（仅 ASR/TTS 支持）；  
- 多语种混合识别（如中英混说）在 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 中明确支持，但 `language=auto` 模式下可能误判语种，建议显式指定主语言。

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


