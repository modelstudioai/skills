# audio api references

百炼平台提供多种音频处理能力的 API，覆盖语音合成、语音识别、音频/音乐生成、语音对话及语音翻译等核心场景。所有音频相关接口均通过统一的 RESTful API 形式提供，支持流式响应与非流式响应两种模式。开发者需根据具体任务选择对应模型，并注意各接口在输入格式、时长限制和语言支持上的差异。

## 支持的模型与功能

当前支持以下六大类音频 API 功能，每类对应独立的模型与调用路径：

- **语音合成（TTS）**：支持多语种、多音色、可控语速与停顿，模型如 `qwen2-audio-tts-v1`；详见 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md)  
- **语音识别（ASR）**：支持实时流式识别与离线文件识别，支持中英文混合及方言适配；详见 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md)  
- **音频生成**：面向环境音、音效、人声片段等非音乐类音频生成；参考 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md)  
- **音乐生成**：支持歌词驱动、风格提示词驱动的完整音乐段落生成，输出为 WAV/MP3；详见 [音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md)  
- **语音对话**：端到端语音交互，支持语音输入→语义理解→语音回复闭环；参见 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md)  
- **语音翻译**：支持源语音→目标语言文本+目标语言语音双路输出，当前仅支持中↔英；详见 [语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md)

> **注意**：[语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 文档中提及的 `enable_vad=true` 默认行为，与 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 中同名参数默认值为 `false` 存在不一致，实际调用以接口返回的 `X-Model-Config` 响应头为准。

## 关键参数

通用关键参数（适用于多数音频 API）包括：

- `model`: 必填，模型标识符（如 `qwen2-audio-asr-v1`），不可省略  
- `input.audio_url` 或 `input.audio_bytes`: 二选一，推荐使用 `audio_url`（支持 HTTPS 公网可访问的音频 URL，格式需为 WAV/MP3/FLAC，采样率 ≥ 16kHz）  
- `parameters.response_format`: 可选 `json`（默认）或 `wav`（仅部分 TTS/音乐生成接口支持）  
- `parameters.language`: ASR/TTS/翻译类接口必填，如 `"zh"`、`"en"`；音乐与音效生成类接口不生效  

部分接口特有参数（如 `parameters.style` 用于音乐生成、`parameters.voice` 用于 TTS）请严格参照对应子文档说明。

## 使用方式

1. **认证**：所有请求需携带 `Authorization: Bearer <api_key>`  
2. **请求方法**：统一使用 `POST`，Content-Type 为 `application/json`  
3. **示例请求体**（ASR）：
   ```json
   {
     "model": "qwen2-audio-asr-v1",
     "input": {
       "audio_url": "https://example.com/audio.wav"
     },
     "parameters": {
       "language": "zh",
       "response_format": "json"
     }
   }
   ```
4. **响应结构**：成功时返回 `200 OK`，主体为 JSON；错误时返回标准 `error.code` 与 `error.message`（如 `invalid_audio_format`, `audio_too_long`）

## 限制和注意事项

- 单次请求音频时长上限：ASR/TTS ≤ 120 秒，音乐生成 ≤ 60 秒，语音对话单轮 ≤ 30 秒（超时将截断并报错 `audio_too_long`）  
- 音频文件大小上限：50 MB（无论 URL 还是 base64 上传）  
- 所有音频接口均**不支持**直接上传本地文件（即不接受 `multipart/form-data`），必须转为公网 URL 或 base64 编码字符串（后者仅限 ≤ 5 MB 小文件）  
- 流式响应（`Accept: text/event-stream`）目前仅在 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 和部分 TTS 接口中可用，其他接口启用将返回 `406 Not Acceptable`  
- > **注意**：[音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md) 文档中列出的 `input.text` 字段为必填项，但实测 v1.2.3 版本 API 已支持纯提示词（`input.prompt`）驱动，该字段已废弃，以最新 OpenAPI Schema 为准。

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


