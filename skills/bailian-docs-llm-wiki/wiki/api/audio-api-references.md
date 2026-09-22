# audio api references

百炼平台的 Audio API 提供语音识别、语音合成、音频生成、音乐生成、语音翻译和语音对话六大核心能力，覆盖从语音到文本、文本到语音、以及端到端语音交互的全链路场景。所有接口均通过 RESTful 方式调用，支持流式响应与非流式响应。开发者需关注各模型的输入格式、采样率要求及语言支持范围。

## 支持的模型/功能

当前支持以下六大音频处理能力，对应独立 API 文档：
- 语音识别（ASR）：支持多语种实时转写，含标点恢复与说话人分离选项  
- 语音合成（TTS）：提供多音色、多语种、可控语速与情感表达能力  
- 音频生成：基于文本生成环境音、音效等非语音类音频内容  
- 音乐生成：支持旋律、风格、时长、BPM 等维度控制的 AI 音乐创作  
- 语音翻译：端到端语音→目标语言语音输出，支持中英日韩等主流语对  
- 语音对话：集成 ASR+LLM+TTS 的低延迟语音交互流水线  

各能力详情请参阅 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md)、[语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 和 [语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md)。

## 关键参数

通用关键参数包括：
- `model`: 必填，如 `qwen2-audio`（ASR/TTS）、`qwen2-music`（音乐生成），具体取值见各子文档  
- `audio`: Base64 编码的音频数据或 OSS URL（推荐用于 >5MB 文件）  
- `sample_rate`: 必填，ASR/TTS 要求 16000 Hz，音乐生成支持 24000/44100/48000 Hz  
- `response_format`: 可选 `json`（默认）或 `wav`（仅 TTS/音乐生成）  
- `stream`: 布尔值，仅 ASR、TTS、语音对话支持流式响应  

> **注意**：`audio_generation_api.md` 中声明支持 `mp3` 输入，但 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md) 实际仅接受 `wav` 或 `flac`；请以该文档为准。

## 使用方式

1. 构造 POST 请求至对应 endpoint（如 `/v1/audio/transcriptions`）  
2. 设置 `Authorization: Bearer <api_key>` 与 `Content-Type: application/json`  
3. 在 request body 中传入必要参数（参考各子文档示例）  
4. 处理响应：非流式返回 JSON 或二进制音频；流式响应需按 SSE 协议解析  

完整调用示例与 SDK 封装说明见 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 文档。

## 限制和注意事项

- 单次请求音频时长上限：ASR ≤ 300 秒，TTS ≤ 120 秒，音乐生成 ≤ 60 秒  
- 免费额度内调用受 QPS 限制（默认 5 QPS），超限返回 `429 Too Many Requests`  
- 所有音频接口均不支持 DRM 保护内容，且输入文件需为合法可解码格式  
- 语音对话接口依赖 ASR/TTS 模型协同，若任一环节失败将中断整条流水线  

请务必查阅 [音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md) 中关于版权与商用授权的特别说明。

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


