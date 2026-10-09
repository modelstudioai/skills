# audio api references

百炼平台提供统一的音频类 API 接口，覆盖语音合成、语音识别、音频/音乐生成、语音对话及语音翻译等核心能力。所有接口均通过 RESTful 方式调用，支持流式响应与非流式响应。开发者需根据具体任务选择对应模型，并注意各接口在输入格式、时长限制和语言支持上的差异。

## 支持的模型与功能

当前音频 API 支持以下六大功能模块，每个模块对应独立的模型与接口规范：  
- 语音合成（TTS）：支持多音色、情感调节与 SSML 控制，详见 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md)；  
- 语音识别（ASR）：支持实时流式识别与离线文件识别，支持中英文混合及多方言，详见 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md)；  
- 音频生成：面向环境音、音效、人声片段等非音乐类音频内容，详见 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md)。

> **注意**：[音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md) 文档中声明支持“16kHz 采样率输入”，但最新 SDK v3.2.0 已要求统一使用 44.1kHz 或 48kHz，旧参数配置将被拒绝。请以 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 中的采样率说明为准。

## 关键参数

通用必填参数包括：`model`（如 `qwen2-audio-tts-16k`）、`input`（结构化请求体）、`output_format`（`wav`/`mp3`/`pcm`）。  
- `speech-synthesis` 接口需指定 `voice` 和 `speed`，其中 `voice` 值必须来自 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 文档附录的合法枚举列表；  
- `speech-recognition` 接口需设置 `language`（如 `zh-CN`、`en-US`），部分模型不支持自动语言检测；  
- 所有音频上传类接口（含 `audio-generation`、`speech-recognition`）要求 base64 编码或直传 URL，且原始音频时长不得超过 60 秒（音乐生成除外，上限为 120 秒）。

## 使用方式

1. 构造 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/audio/{endpoint}`（如 `/speech-synthesis`）；  
2. 设置 Header：`Authorization: Bearer <api_key>`，`Content-Type: application/json`；  
3. 在 request body 中按 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 定义的 schema 提交 `input` 字段；  
4. 流式响应需额外添加 `Accept: text/event-stream`，并按 SSE 协议解析 chunk。

## 限制和注意事项

- 单次请求最大 payload 为 10 MB（含 base64 编码后体积）；  
- 免费调用量按自然月重置，超出后按模型粒度计费；  
- `speech-translation` 接口暂不支持目标语言为 `zh-CN` 以外的中文变体（如 `zh-TW`），该限制未在 [语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md) 中明确说明，实际调用将返回 `400 Unsupported language code`；  
- 所有音频输出默认为单声道，如需立体声需显式设置 `channels: 2`（仅部分 TTS 和音乐生成模型支持）。

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


