# audio api references

百炼平台的 Audio API 提供语音合成、识别、翻译、对话、音乐及通用音频生成等能力，所有接口均通过 RESTful 方式调用，支持流式响应与异步任务模式。各功能由独立模型提供服务，需按场景选择对应 endpoint 与参数组合。详细行为以各子文档为准，本文档仅作统一索引与关键共性说明。

## 支持的模型/功能

当前支持以下六大类音频处理能力，每类对应专用模型与独立 API 接口：

- **语音合成（TTS）**：支持多语种、多音色、可控语速与停顿，模型如 `qwen2-audio-tts-v1`  
- **语音识别（ASR）**：支持长音频转写、带标点与说话人分离（diarization），模型如 `qwen2-audio-asr-v1`  
- **语音翻译（ST）**：支持源语音→目标文本（如中文语音→英文文本），非端到端语音→语音，详见 [语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md)  
- **语音对话（Voice Conversation）**：实时双工语音交互，需配合 SDK 使用，低延迟设计，参考 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md)  
- **音频生成（Audio Generation）**：基于文本提示生成环境音、音效、人声片段等非音乐类音频，区别于音乐生成，参见 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md)  
- **音乐生成（Music Generation）**：支持旋律、风格、BPM、乐器编排等控制，输出为完整音乐片段，详见 [音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md)  

> **注意**：`qwen2-audio-asr-v1` 当前不支持方言识别，而旧版文档中提及的 `qwen-audio-asr-beta` 已下线且未在 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 中更新说明，请以该文档最新版本为准。

## 关键参数

所有 Audio API 共享以下基础参数（必填项标 `*`）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model*` | string | 是 | 模型标识符，如 `qwen2-audio-tts-v1`；必须与所选功能匹配，错误值将返回 400 |
| `input*` | object | 是 | 输入结构体，格式因功能而异（如 ASR 为 `{ "audio_url": "..." }`，TTS 为 `{ "text": "..." }`） |
| `parameters` | object | 否 | 控制生成质量、时长、风格等，例如 `{"voice": "zhiyan", "speed": 1.2}`（TTS）或 `{"language": "zh", "diarization": true}`（ASR） |

部分高级参数（如 `stream`、`response_format`）仅在特定接口生效，具体请查阅对应子文档，例如 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 明确支持 `stream=true` 返回 chunked audio。

## 使用方式

1. **认证**：使用 `Authorization: Bearer <api_key>` 请求头  
2. **请求方法**：全部为 `POST`，Endpoint 格式为 `https://dashscope.aliyuncs.com/api/v1/audio/{service}`（如 `/api/v1/audio/tts`）  
3. **输入格式**：`input` 字段必须为 JSON 对象，不可传 raw audio binary；音频文件需先上传至 OSS 或提供可公开访问的 HTTPS URL（含有效 CORS 头）  
4. **响应结构**：统一遵循 `{ "output": { ... }, "usage": { ... }, "request_id": "..." }`，错误时返回 `{"code": "...", "message": "..."}`  

流式响应需设置 `Accept: application/x-ndjson` 并解析逐行 JSON，具体协议细节见 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 的“流式交互”章节。

## 限制和注意事项

- 单次请求音频时长上限：ASR 最长 60 分钟，TTS 输出最长 10 分钟，音乐生成最长 30 秒（超限将截断并返回警告）  
- 音频格式要求：仅支持 `mp3`, `wav`, `flac`, `m4a`；采样率建议 16kHz/44.1kHz，位深 16bit；不支持视频容器（如 mp4 中的音频轨需先提取）  
- 异步任务（如长音频 ASR）需轮询 `GET /api/v1/tasks/{task_id}` 获取结果，任务保留期为 24 小时  
- 所有音频 URL 必须可被百炼服务端直连访问（禁止私有内网地址、需鉴权的签名 URL 或临时过期链接）  
- > **注意**：[音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md) 文档中声明支持 `prompt` + `negative_prompt`，但当前后端实际忽略 `negative_prompt` 字段——该不一致已在内部 issue #AUD-287 中登记，暂勿依赖此参数。

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


