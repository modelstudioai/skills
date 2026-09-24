# audio api references

百炼平台提供覆盖语音合成、识别、翻译、对话及音频/音乐生成的全链路音频 API，支持开发者快速集成多模态语音能力。所有接口均通过统一的 RESTful API 形式调用，需使用 API Key 进行身份认证。各功能模块独立演进，模型版本与参数行为请以对应子文档为准。

## 支持的模型与功能

当前音频 API 包含六大核心能力：
- **语音合成（TTS）**：支持多语种、多音色、可控语速与情感表达  
- **语音识别（ASR）**：高精度实时/离线转写，支持带标点和 speaker diarization  
- **语音翻译（ST）**：端到端语音到文本翻译，支持中英等 12 种语言对  
- **语音对话（Voice Conversation）**：低延迟流式语音交互，内置唤醒与上下文管理  
- **音频生成（Audio Generation）**：基于文本生成环境音、音效、旁白等非音乐类音频  
- **音乐生成（Music Generation）**：支持风格、BPM、时长控制的原创音乐生成  

详细能力说明与模型列表见 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md)、[语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 和 [音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md)。

## 关键参数

通用请求头需包含 `Authorization: Bearer <api_key>`；部分接口要求 `Content-Type: multipart/form-data`（如文件上传类）或 `application/json`（如文本输入类）。关键参数包括：

- `model`: 必填，如 `qwen2-audio-tts-01`、`qwen2-audio-asr-02`，具体取值见各子文档  
- `input`: 输入结构因功能而异：TTS 为 `{"text": "..."}`，ASR 为 `{"audio_url": "..."}` 或二进制文件字段  
- `parameters`: 可选对象，常见字段有 `voice`, `speed`, `temperature`, `duration` 等，含义与取值范围严格以 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 等对应子文档定义为准  

> **注意**：`temperature` 在音乐生成接口中影响风格随机性，但在 ASR 接口中无意义——该参数仅在 [音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md) 文档中被明确定义，ASR 文档未声明其作用，实际调用时传入将被忽略。

## 使用方式

1. 通过 POST 请求调用对应 endpoint（如 `https://dashscope.aliyuncs.com/api/v1/services/aigc/audio-generation`）  
2. 构造请求体（JSON 或 form-data），确保 `input` 格式与所选模型兼容  
3. 解析响应：成功时返回 `output.audio_url`（生成类）或 `output.text`（识别/翻译类）；错误时返回标准 `code` 与 `message`  

示例代码与 SDK 调用方式详见 [语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md) 文档中的 Quick Start 章节。

## 限制和注意事项

- 单次请求音频时长上限：TTS ≤ 10 分钟，ASR ≤ 60 分钟，音乐生成 ≤ 90 秒（超长请求将被截断并返回警告）  
- 免费调用量按自然月重置，超出后需绑定计费项；具体配额见控制台「API 配额管理」  
- 所有音频文件 URL 为临时直链，有效期 24 小时，需及时下载或转存  
- 流式语音对话接口要求客户端维持长连接，超时阈值为 30 秒无数据帧即断连  

> **注意**：原始文档中 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 提到“支持 WebSocket 与 HTTP/2”，但最新 SDK 仅默认启用 WebSocket；HTTP/2 支持已在 v3.2.0+ 版本中移除，该描述已过时，请以 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 的「版本变更日志」章节为准。

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


