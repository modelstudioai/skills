# audio api references

百炼平台提供多种音频处理能力的 API 接口，覆盖语音识别、语音合成、音乐生成、语音翻译和语音对话五大核心场景。所有接口均通过统一的 RESTful 设计对外暴露，支持 JSON 格式请求与响应，并需携带有效的 API Key 进行鉴权。开发者可根据具体任务选择对应模型与参数组合，实现端到端音频智能处理。

## 支持的模型与功能

当前音频 API 支持以下五类功能，每类对应独立的模型服务与调用路径：

- **语音识别（ASR）**：将音频流或文件转为文本，支持多语种及带标点/时间戳输出  
- **语音合成（TTS）**：将文本转为自然语音，支持音色选择、语速/语调调节  
- **音乐生成**：基于文本描述生成高质量、可商用的背景音乐片段  
- **语音翻译**：支持源语音→目标语言文本，或源语音→目标语音（端到端）两种模式  
- **语音对话**：实时双工语音交互，集成 ASR + LLM + TTS 全链路，适用于智能硬件场景  

各功能详情请参阅 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md)、[语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 和 [音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md) 的独立参考文档。

## 关键参数

通用必选参数（所有音频 API 共享）：
- `model`: 模型标识符，如 `paraformer-realtime-v1`（ASR）、`sambert-zh-cn`（TTS）、`musicgen-pro-2024`（音乐）  
- `input`: 音频输入对象，支持 `audio_url`（公网可访问 URL）或 `audio_bytes`（Base64 编码二进制数据）  
- `api_key`: 用于身份认证，需在请求 Header 中以 `Authorization: Bearer <api_key>` 方式传递  

功能特有参数示例：
- ASR：`language`, `enable_punctuation`, `word_timestamps`  
- TTS：`voice`, `speed`, `pitch`  
- 音乐生成：`duration`, `style`, `instrumental`  

> **注意**：`audio_bytes` 字段最大支持 25 MB；若使用 `audio_url`，服务端将发起 GET 请求并要求响应头含 `Content-Type: audio/*`，否则可能解析失败 —— 此限制在 [语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md) 文档中未明确说明，但已在 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 和 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 文档中一致确认。

## 使用方式

1. 构造 POST 请求至对应功能的 endpoint（如 `/v1/audio/transcriptions`）  
2. 设置 Header：`Content-Type: application/json`，`Authorization: Bearer <your_api_key>`  
3. 在 JSON body 中传入 `model`、`input` 及功能相关参数  
4. 解析返回的 `output` 字段（结构因功能而异，详见各子文档）

完整请求示例与响应格式请参考 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 文档中的“快速开始”章节。

## 限制和注意事项

- 单次请求音频时长上限：ASR/TTS ≤ 600 秒，音乐生成 ≤ 30 秒，语音对话流式会话 ≤ 1800 秒（30 分钟）  
- 所有音频接口均不支持实时流式上传（chunked transfer encoding），必须提交完整音频数据或有效 URL  
- 语音翻译的端到端模式（speech-to-speech）暂不支持自定义目标音色，仅复用默认 TTS 声音  
- 错误码统一遵循百炼平台标准（如 `400 Bad Request`、`401 Unauthorized`、`429 Too Many Requests`），详细含义见各子文档末尾的错误码表  

请务必查阅 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 文档中关于音色合规性与商用授权的说明，避免法律风险。

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


