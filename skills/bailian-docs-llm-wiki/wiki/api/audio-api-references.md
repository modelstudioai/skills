# audio api references

百炼平台提供覆盖语音合成、识别、翻译、对话及音频/音乐生成的全链路音频 API，支持开发者快速集成多模态语音能力。所有接口均通过统一的 RESTful API 形式调用，需使用 API Key 进行身份认证。各功能模块独立演进，模型版本与参数配置可能存在差异，建议以最新版 [原文标题](../../raw/model-api-reference/audio-api-references.md) 为准。

## 支持的模型与功能

当前音频 API 包含六大核心能力：
- **语音合成（TTS）**：支持多语种、多音色、可调节语速/音调的高质量文本转语音  
- **语音识别（ASR）**：支持实时流式识别与离线文件识别，覆盖中英文及部分方言  
- **语音翻译（ST）**：端到端语音到文本翻译（如中文语音→英文文本），暂不支持语音到语音直译  
- **语音对话（Voice Conversation）**：低延迟双工语音交互，依赖专用对话模型，需配合 SDK 使用  
- **音频生成（Audio Generation）**：基于文本提示生成环境音、音效等非音乐类音频  
- **音乐生成（Music Generation）**：支持旋律、风格、时长控制的 AI 音乐创作  

> **注意**：[原文标题](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md) 中提及的“语音到语音翻译”能力尚未上线，实际仅支持语音→目标语言文本；该描述与 [原文标题](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 中关于双工延迟的指标说明存在不一致，以后者实测文档为准。

## 关键参数

通用必填参数：
- `model`: 模型标识符（如 `qwen2-audio-tts-01`, `qwen2-audio-asr-02`），详见各子文档  
- `input`: 输入结构体，格式依功能而异（如 TTS 为 `{ "text": "..." }`，ASR 为 `{ "audio_url": "..." }`）  
- `output_format`: 返回音频编码格式（`mp3`, `wav`, `pcm`），部分模型仅支持特定格式  

功能特有参数示例：
- TTS：`voice`, `speed`, `pitch`  
- ASR：`language`, `audio_format`, `sample_rate`  
- 音乐生成：`style`, `bpm`, `instrumentation`  

所有参数定义与默认值请参考对应子文档，例如 [原文标题](../../raw/model-api-reference/audio-api-references/music-generation-references.md) 中的 `style` 枚举值已更新为包含 `"lofi"` 和 `"cinematic"` 新选项。

## 使用方式

1. **认证**：在请求 Header 中携带 `Authorization: Bearer <api_key>`  
2. **请求**：POST 到 `https://dashscope.aliyuncs.com/api/v1/audio/{endpoint}`（`endpoint` 如 `tts`, `asr`, `music-generation`）  
3. **响应**：成功时返回 `200`，音频内容位于 `output.audio_url`（直传 URL）或 `output.audio_bytes`（Base64 编码）字段  
4. **错误处理**：关注 `code` 字段（如 `InvalidParameter`, `QuotaExceeded`），详见各子文档错误码表  

## 限制和注意事项

- 单次请求音频时长上限：TTS ≤ 5 分钟，ASR ≤ 30 分钟，音乐生成 ≤ 2 分钟  
- 免费调用量按模型独立计算，超出后触发计费；具体配额见控制台  
- ASR 的 `audio_url` 必须为公网可访问的 HTTPS 地址，且文件大小 ≤ 100 MB  
- 所有音频输入需为单声道，采样率建议 16kHz（ASR/TTS）或 44.1kHz（音乐生成）  
- 语音对话接口要求客户端维持长连接，超时时间默认 60 秒，不可修改

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


