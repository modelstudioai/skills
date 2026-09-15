# audio api references

百炼平台提供多种音频处理能力的 API 接口，覆盖语音识别、语音合成、音乐生成、语音翻译和语音对话五大核心场景。所有接口均通过统一的 RESTful HTTP 接口调用，支持流式响应与非流式响应两种模式。开发者需使用有效的 API Key 进行身份认证，并遵循各模型的输入格式与配额限制。

## 支持的模型与功能

当前支持以下五类音频相关模型能力：
- **语音识别（ASR）**：支持中英文多语种实时/离线转写，含标点恢复与说话人分离选项  
- **语音合成（TTS）**：提供多音色、可调节语速/语调/停顿的高质量语音生成  
- **音乐生成**：支持文本描述驱动的短时长（≤30s）BGM 生成，输出为 WAV/MP3 格式  
- **语音翻译**：端到端实现语音→目标语言文本/语音的跨语种转换（如中文语音→英文语音）  
- **语音对话**：集成 ASR+LLM+TTS 的全链路语音交互，支持上下文感知的实时对话流  

各能力详情请参阅 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md)、[语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 和 [音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md) 的独立参考文档。

## 关键参数

通用请求头必须包含：
- `Authorization: Bearer <api_key>`  
- `Content-Type: application/json`（非流式）或 `application/x-www-form-urlencoded`（部分 TTS 场景）

核心请求体字段（以语音识别为例）：
- `audio_url`（必填）：公网可访问的音频文件 URL（支持 MP3/WAV/FLAC，≤100MB）  
- `language`（可选）：`zh`, `en`, `zh-en` 等，未指定时自动检测  
- `response_format`（可选）：`json`（默认）或 `srt`（字幕格式）  
- `enable_punctuation`（可选）：布尔值，控制是否启用智能标点  
> **注意**：`audio_url` 不支持本地文件路径或 base64 内联数据；若需上传原始音频流，请使用 `/v1/audio/transcriptions` 的 multipart/form-data 方式 —— 具体要求见 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 文档，该文档与 [语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md) 中关于输入格式的说明存在不一致（后者仍提及 base64 支持），请以前者为准。

## 使用方式

1. **构造请求**：根据目标能力选择对应 endpoint（如 `POST /v1/audio/transcriptions`）  
2. **提交音频**：优先使用 `audio_url`（推荐）；若需低延迟或私有网络环境，可改用 `audio_file` 字段上传二进制流（需 `multipart/form-data`）  
3. **处理响应**：成功返回 `200 OK`，结构化 JSON 包含 `text`、`segments` 或 `audio_url` 等字段；错误码详见 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 的错误码附录  

流式接口（如 TTS [流式输出](../concepts/streaming-output.md)、语音对话）需设置 `stream=true` 并按 SSE 协议解析事件流。

## 限制和注意事项

- 单次请求音频时长上限：ASR/TTS ≤ 600 秒，音乐生成 ≤ 30 秒，语音翻译 ≤ 180 秒  
- 音频采样率建议 16kHz，单声道；非标准格式可能导致识别准确率下降  
- 所有音频 URL 必须支持 HEAD 请求且无跳转（302 不被跟随）  
- 免费额度内调用受 QPS 限制（默认 5 QPS），超出将返回 `429 Too Many Requests`  
- 语音对话接口暂不支持自定义 LLM 模型，固定使用 `qwen-audio` 底层模型（详见 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md)）

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


