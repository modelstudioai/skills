# audio api references

百炼平台提供统一的音频类 API 接口，覆盖语音合成、语音识别、音频生成、语音对话及语音翻译五大核心能力。所有接口均通过 RESTful 方式调用，支持 JSON 格式请求与响应，并遵循统一的鉴权与错误码规范。开发者需根据具体任务选择对应模型与参数组合，详见各子模块文档。

## 支持的模型与功能

当前支持以下五类音频处理能力，每类对应独立的 API 端点与模型选型：

- **语音合成（TTS）**：支持 `qwen2-audio-tts` 等多语种、多音色模型，可控制语速、音调、停顿等；参考 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md)  
- **语音识别（ASR）**：支持中英文混合识别、带标点恢复、说话人分离（部分模型），延迟与准确率因模型而异；参考 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md)  
- **音频生成（Audio Generation）**：支持文本到音乐、音效、环境声等生成任务，输出格式为 WAV/MP3；参考 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md)  
- **语音对话（Voice Conversation）**：端到端实时语音交互，含唤醒、流式响应、上下文保持能力；参考 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md)  
- **语音翻译（Speech Translation）**：支持语音输入→目标语言文本/语音双路径输出，当前仅开放中英互译；参考 [语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md)

> **注意**：`qwen2-audio-tts` 模型在 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 中声明支持“情感强度调节”，但该参数在 v1.2.0+ SDK 中已被移除，实际调用将被忽略——请以 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 的最新版参数列表为准。

## 关键参数

所有音频 API 共享以下基础参数：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen2-audio-tts`, `qwen2-audio-asr-zh`；详见各子文档模型列表 |
| `input` | object | 是 | 音频输入结构，含 `audio_url`（远程 URL）或 `audio_bytes`（Base64 编码二进制）；[语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 明确要求采样率 ≥16kHz，位深 ≥16bit |
| `parameters` | object | 否 | 任务相关配置，如 `voice`, `language`, `response_format`；各功能差异较大，须查阅对应子文档 |

## 使用方式

1. **认证**：在 HTTP Header 中携带 `Authorization: Bearer <api_key>`  
2. **请求**：POST 到对应端点（如 `/v1/audio/speech-to-text`），Body 为 JSON，`input.audio_url` 优先于 `input.audio_bytes`（若同时提供，以 `audio_url` 为准）  
3. **响应**：成功时返回 `200 OK`，结构含 `output` 字段（文本、音频 URL 或结构化结果）；失败时返回标准错误码（如 `400 Bad Request`, `429 Rate Limited`）

## 限制和注意事项

- 单次请求音频时长上限：TTS ≤ 300 秒，ASR ≤ 60 秒，Audio Generation ≤ 15 秒，Voice Conversation 单轮 ≤ 120 秒  
- 音频格式要求：WAV（PCM）、MP3、M4A；不支持 FLAC、OGG 等非主流封装（即使编码为 PCM）  
- 跨区域调用：`audio_url` 必须可被百炼服务端公网访问，内网地址或带鉴权头的 URL 将失败  
- 计费粒度：按音频秒数（ASR/TTS）或生成 token 数（Audio Generation）计费，详情见 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 附录说明

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


