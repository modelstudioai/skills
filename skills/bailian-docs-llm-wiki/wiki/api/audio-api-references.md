# audio api references

百炼平台提供多种音频处理能力的 API 接口，覆盖语音识别、语音合成、音乐生成、语音翻译和语音对话五大核心场景。所有接口均通过统一的 RESTful 设计对外暴露，支持流式与非流式调用。开发者需根据具体任务选择对应模型，并注意各接口在输入格式、时长限制及并发策略上的差异。

## 支持的模型/功能

当前音频类 API 包含以下功能模块：
- **语音识别（ASR）**：支持中英文混合识别，提供实时流式与离线批量两种模式  
- **语音合成（TTS）**：支持多音色、语速/语调调节，部分模型支持情感控制  
- **音乐生成**：基于文本提示生成短时长（≤30 秒）背景音乐或旋律片段  
- **语音翻译**：支持源语音→目标语言文本（如中文语音→英文文本），暂不支持语音输出  
- **语音对话**：端到端语音交互，含唤醒、语义理解与语音响应闭环，依赖专用 voice-conversation 模型  

各功能详情请参阅 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md)、[语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 和 [音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md) 的独立参考文档。

## 关键参数

通用请求头需包含 `Authorization: Bearer <api_key>` 与 `Content-Type: application/json`。核心参数如下：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `paraformer-realtime-v1`（ASR）、`sambert-zh-cn`（TTS）等，详见各子文档 |
| `audio_url` 或 `audio_bytes` | string / base64 | 是 | 音频源，优先使用 `audio_url`（HTTPS 公网可访问 URL）；`audio_bytes` 仅限 ≤4MB 短音频 |
| `language` | string | 否（ASR/TTS 必填） | 如 `zh-CN`, `en-US`；音乐生成与语音对话无需此参数 |
| `stream` | boolean | 否 | 仅 ASR/TTS 支持，设为 `true` 启用流式响应（SSE） |

> **注意**：[语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md) 文档中提及的 `target_language_audio` 参数已在 v2.3.0 版本移除，当前语音翻译仅输出文本，该参数描述已过时，请以最新 SDK 示例为准。

## 使用方式

1. **认证**：使用平台颁发的 `api_key`，通过 `Authorization` 请求头传递  
2. **请求构造**：POST 到对应 endpoint（如 `/v1/audio/transcriptions`），body 为 JSON 格式参数  
3. **响应解析**：成功返回 `200`，结构含 `text`（ASR/翻译）、`audio_url`（TTS）、`music_url`（音乐生成）等字段；错误时返回标准 `error.code` 与 `error.message`  

完整调用示例见 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 文档中的 cURL 与 Python 片段。

## 限制和注意事项

- 单次请求音频时长上限：ASR/TTS ≤120 秒，音乐生成 ≤30 秒，语音对话单轮 ≤60 秒  
- 并发限制：免费版 2 QPS，企业版按配额配置，超限返回 `429 Too Many Requests`  
- 音频格式：仅支持 `wav`（PCM 16-bit）、`mp3`、`m4a`；采样率建议 16kHz 或 44.1kHz，单声道优先  
- 所有音频 URL 必须为 HTTPS 且可公开访问（内网地址、带鉴权 Header 的 URL 不被接受）  
- 语音对话接口要求客户端实现 WebSocket 连接维持，不支持 HTTP 短连接轮询  

如遇 `invalid_audio_format` 错误，请先校验音频编码完整性，而非仅检查文件扩展名——该问题在 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 文档的“常见错误”章节中有详细排查指引。

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


