# audio api references

百炼平台提供统一的音频处理 API 接口，覆盖语音合成、语音识别、音频生成、语音对话和语音翻译五大核心能力。所有接口均通过 RESTful 方式调用，支持流式响应与非流式响应两种模式，并遵循统一的鉴权、错误码与重试规范。开发者需根据具体任务选择对应模型与参数组合，详见各子模块文档。

## 支持的模型/功能

当前支持以下五类音频相关能力：
- **语音合成（TTS）**：支持多语种、多音色、可控语速与情感表达，模型包括 `qwen-audio-tts-v1` 等；
- **语音识别（ASR）**：支持中英文混合识别、标点自动恢复、热词增强，模型如 `qwen-audio-asr-v2`；
- **音频生成（Audio Generation）**：支持文本到音频（如环境音、音效）、音频风格迁移等，模型为 `qwen-audio-gen-v1`；
- **语音对话（Voice Conversation）**：端到端语音交互，含唤醒、理解、合成闭环，依赖 `qwen-voice-conversation-v1`；
- **语音翻译（Speech Translation）**：支持语音输入→目标语言文本/语音双路输出，模型为 `qwen-speech-translate-v1`。  
各能力细节请参阅 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md)、[语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 和 [语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md) 的独立参考文档。

## 关键参数

通用必填参数：`model`（字符串，指定模型 ID）、`input`（对象，结构依任务而异）、`output_format`（可选，`wav`/`mp3`/`pcm`）。  
任务特有参数示例：
- TTS：`voice`（音色 ID）、`speed`（0.5–2.0）、`pitch`（-50–50）；
- ASR：`language`（`zh`/`en`/`auto`）、`enable_punctuation`（布尔）、`hotword`（字符串数组）；
- Audio Generation：`duration`（秒，最大 30）、`prompt`（文本描述）；  
> **注意**：`sample_rate` 参数在 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md) 文档中标注为“仅影响输出采样率”，但在 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 文档中明确要求必须与输入音频实际采样率一致，否则导致静音或截断——请以实际输入音频为准，勿硬编码。

## 使用方式

1. 构造 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/audio`；  
2. Header 中携带 `Authorization: Bearer <api_key>` 与 `Content-Type: application/json`；  
3. Body 中按能力类型组织 `input` 字段（如 ASR 的 `input.audio_url` 或 `input.audio_bytes`）；  
4. 流式请求需额外设置 `stream: true`，响应为 SSE 格式；非流式响应直接返回 JSON。  
完整调用示例与 SDK 封装说明见 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 文档的「快速开始」章节。

## 限制和注意事项

- 单次请求音频时长上限：ASR ≤ 600 秒，TTS ≤ 300 秒，Audio Generation ≤ 30 秒，语音对话单轮 ≤ 120 秒；  
- 所有音频输入须为 Base64 编码（`audio_bytes`）或公网可直连 URL（`audio_url`），URL 有效期建议 ≥ 10 分钟；  
- 错误码 `422 Unprocessable Entity` 常因 `input` 结构不合法或 `model` 不支持该任务类型引发，需核对 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md) 等各子文档的 input schema 定义；  
- 非中文语音识别推荐显式指定 `language`，避免 `auto` 模式在低信噪比下误判。

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


