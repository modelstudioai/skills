# audio api references

百炼平台提供覆盖语音合成、识别、翻译、对话及音频/音乐生成的全链路音频 API，支持开发者快速集成多模态语音能力。所有接口均通过统一的 RESTful 设计对外暴露，需使用 API Key 进行身份认证。各功能模块独立演进，模型版本与参数配置请以对应子文档为准。

## 支持的模型与功能

当前音频 API 包含六大核心能力：
- **语音合成（TTS）**：支持多语种、多音色、可调节语速/音调的高质量文本转语音  
- **语音识别（ASR）**：支持中英文混合识别、实时流式识别与离线文件识别  
- **语音翻译（ST）**：端到端语音到文本翻译，支持中↔英等主流语对  
- **语音对话（Voice Conversation）**：低延迟双工语音交互，内置唤醒与上下文管理  
- **音频生成（Audio Generation）**：基于文本提示生成环境音、音效等非音乐类音频  
- **音乐生成（Music Generation）**：支持风格、时长、BPM 等细粒度控制的原创音乐生成  

各功能详情见 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md)、[语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 与 [音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md) 的独立参考文档。

## 关键参数

通用请求头需包含 `Authorization: Bearer <api_key>`；所有接口均支持 `model` 参数指定具体模型 ID（如 `paraformer-v1`、`qwen2-audio-tts`）。关键参数因功能而异：
- TTS：`input.text`、`voice`、`speed`、`pitch`  
- ASR：`audio_url` 或 `audio_bytes`、`language`、`enable_punctuation`  
- 音乐生成：`prompt`、`duration`（秒）、`style`、`bpm`  
> **注意**：`duration` 在 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md) 中最大支持 30 秒，但在 [音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md) 中上限为 60 秒，二者语义与限制不同，请按实际功能选用对应文档。

## 使用方式

1. 通过 HTTPS POST 请求目标 endpoint（如 `https://dashscope.aliyuncs.com/api/v1/services/aigc/tts`）  
2. 请求体为 JSON 格式，结构遵循各子功能规范  
3. 响应含 `output.audio_url`（直连可播放 URL）或 `output.text`（ASR/ST 场景），部分接口支持 `response_format=wav` 等格式协商  
完整调用示例与错误码说明参见 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 文档中的「请求示例」章节。

## 限制和注意事项

- 单次请求音频文件大小上限：ASR/ST 为 100 MB，TTS 输入文本长度 ≤ 5000 字符，音乐生成 [prompt](../guides/prompt.md) ≤ 200 字符  
- 所有音频类接口暂不支持跨区域调用，请求必须发往与 API Key 绑定的 Region（如 `cn-shanghai`）  
- 流式接口（如语音对话）需维持长连接，超时阈值为 300 秒，断连后需重置会话上下文  
- 模型兼容性：`qwen2-audio` 系列模型仅支持语音对话与语音识别，不兼容 TTS 或音乐生成任务——该约束在 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 文档中有明确声明。

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


