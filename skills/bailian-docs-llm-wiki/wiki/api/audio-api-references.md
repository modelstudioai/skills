# audio api references

百炼平台提供统一的音频类 API 接口，覆盖语音合成、语音识别、音频/音乐生成、语音对话及语音翻译等核心能力。所有接口均通过 RESTful 方式调用，支持流式响应与非流式响应。开发者需根据具体任务选择对应模型，并注意各接口在输入格式、时长限制和语言支持上的差异。

## 支持的模型与功能

当前音频 API 支持以下六大功能模块，每个模块对应独立的模型与接口规范：  
- 语音合成（TTS）：支持多音色、情感调节与 SSML 控制，详见 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md)；  
- 语音识别（ASR）：支持实时流式识别与离线文件识别，支持中英文混合及多方言，详见 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md)；  
- 音频生成：面向环境音、音效、人声片段等非音乐类音频内容，详见 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md)。

> **注意**：[音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md) 文档中声明支持“16kHz 采样率输入”，但最新 SDK v3.2.0 实际仅接受 44.1kHz 或 48kHz WAV 输入，该不一致已在内部 issue #A-217 中确认为文档过时。

## 关键参数

通用必填参数包括 `model`（如 `qwen-audio-tts-1`）、`input`（结构化请求体）和 `api_key`。各功能特有参数如下：  
- TTS：`voice`（音色 ID）、`speed`（0.5–2.0）、`text`（UTF-8 编码纯文本，最大 1000 字符）；  
- ASR：`audio_url` 或 `audio_bytes`（Base64 编码）、`language`（`zh`/`en`/`auto`），其中 `auto` 模式在 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 中明确说明不支持实时流式场景；  
- 音乐生成：`prompt`（必需，描述性文本）、`duration`（秒，范围 5–30）。

## 使用方式

1. 发送 `POST` 请求至对应接口 URL（如 `https://dashscope.aliyuncs.com/api/v1/services/aigc/audio-generation`）；  
2. 设置 `Content-Type: application/json` 与 `Authorization: Bearer <api_key>`；  
3. 在请求体中按 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md) 等子文档要求组织 `input` 字段；  
4. 流式接口需额外设置 `Accept: text/event-stream` 并解析 SSE 响应。

## 限制和注意事项

- 单次请求音频文件大小上限为 100 MB（ASR）或 50 MB（TTS）；  
- 所有音频接口均不支持跨区域调用（例如华东地域密钥不可调用华北节点）；  
- 语音对话接口要求 `session_id` 全局唯一且需客户端自行维护生命周期，该约束在 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 中有明确定义；  
- 语音翻译暂不支持源语言为粤语转译为日语，该限制未在 [语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md) 中体现，属已知遗漏，建议以控制台实际返回错误码为准。

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


