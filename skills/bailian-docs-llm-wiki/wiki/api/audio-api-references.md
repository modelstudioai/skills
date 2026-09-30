# audio api references

百炼平台提供统一的音频类 API 接口，覆盖语音合成、语音识别、语音翻译、音频生成、音乐生成及语音对话六大能力。所有接口均通过 RESTful 方式调用，支持流式响应与非流式响应两种模式。开发者需使用有效的 API Key 并遵循各模型的输入格式与计费规则。

## 支持的模型/功能

当前支持以下六大音频处理能力，对应独立的模型与 API 端点：

- **语音合成（TTS）**：支持多语种、多音色、可控语速与停顿，详见 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md)  
- **语音识别（ASR）**：支持长音频转写、标点恢复、说话人分离（部分模型），详见 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md)  
- **语音翻译（ST）**：支持实时语音到目标语言文本的端到端翻译，支持中英互译及部分小语种，详见 [语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md)  
- **音频生成（Audio Generation）**：基于文本生成环境音、音效或带语义的短音频片段，不支持长语音合成  
- **音乐生成（Music Generation）**：支持文本描述驱动的背景音乐生成，输出为 WAV/MP3 格式，时长限制为 30 秒以内  
- **语音对话（Voice Conversation）**：集成 ASR + LLM + TTS 的全链路语音交互能力，需按会话生命周期管理 token，详见 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md)

> **注意**：[音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md) 文档中提及的“支持 60 秒音频”与当前生产环境实际限制（≤15 秒）不符，以控制台最新配额页和 API 返回的 `max_duration` 字段为准。

## 关键参数

所有音频 API 共享以下基础参数（部分为必填）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen2-audio-tts-01`、`qwen2-audio-asr-02`；具体取值见各子文档 |
| `input` | object | 是 | 输入结构体，字段因能力而异（如 `audio_url`、`text`、`language`） |
| `parameters` | object | 否 | 可选配置项，如 `voice`（TTS）、`sample_rate`（ASR）、`temperature`（音乐生成） |
| `stream` | boolean | 否 | 是否启用流式响应，默认 `false`；仅部分模型支持 `true` |

> **注意**：`parameters.voice` 在 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 中定义为字符串枚举值（如 `"zhiyuan"`），但在旧版 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 示例中误写为对象格式，应以 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 文档为准。

## 使用方式

1. **认证**：在 HTTP Header 中携带 `Authorization: Bearer <api_key>`  
2. **请求**：向 `https://dashscope.aliyuncs.com/api/v1/audio/{endpoint}` 发送 POST 请求（`{endpoint}` 如 `tts`、`asr`、`music`）  
3. **输入构造**：`input` 字段需符合各能力要求——例如 ASR 要求 `input.audio_url` 或 `input.audio_bytes`（Base64 编码二进制），TTS 要求 `input.text` 和 `input.language`  
4. **响应解析**：成功响应含 `output` 字段，其中 `output.audio_url`（直连可下载链接）或 `output.text`（ASR/ST 结果）为核心数据  

完整调用示例与错误码说明请参考各子文档，例如 [音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md) 提供了 Python SDK 封装示例。

## 限制和注意事项

- 所有音频 API 均受百炼平台通用速率限制（QPS/TPM）与单次请求资源约束（如最大音频时长、文件大小上限）  
- 音频文件需为 PCM/WAV/MP3/M4A 格式；采样率建议 16kHz 或 44.1kHz，位深 16bit；超出范围可能触发静音检测失败或识别降质  
- 流式响应（`stream=true`）仅适用于 TTS、ASR 和 Voice Conversation，且客户端必须正确处理 Server-Sent Events（SSE）协议  
- 语音对话（Voice Conversation）需显式调用 `/close` 端点终止会话，否则会话上下文持续占用资源并计费  
- 音频内容须符合中国法律法规及百炼内容安全策略，含违规内容的请求将被拦截并记录日志

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


