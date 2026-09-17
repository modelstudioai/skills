# audio api references

百炼平台提供多种音频处理能力的 API，涵盖语音识别、语音合成、音乐生成、语音翻译和语音对话五大核心场景。所有音频 API 均通过统一的 HTTP 接口调用，支持流式与非流式响应，并遵循平台通用鉴权与错误码规范。开发者需根据具体任务选择对应模型及参数配置，详见各子模块文档。

## 支持的模型与功能

当前支持以下五类音频处理能力，每类对应独立的 API 端点与模型选型：

- **语音识别（ASR）**：支持中文、英文等多语种实时/离线转写，模型包括 `asr-general-v2`、`asr-dialect-v1` 等；  
- **语音合成（TTS）**：提供多音色、多语速、情感可控的文本转语音服务，主流模型为 `tts-1` 和 `tts-1-hd`；  
- **音乐生成**：支持文本描述生成 5–30 秒背景音乐，模型为 `music-gen-2024`；  
- **语音翻译**：端到端实现语音输入→目标语言语音输出（如中→英），不返回中间文本；  
- **语音对话**：支持带上下文记忆的双工语音交互，需配合 `voice-conversation-api-references.md` 中定义的会话生命周期管理。

> **注意**：`music-gen-2024` 模型在 [音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md) 文档中标注为“仅限白名单开通”，而 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 文档未说明类似限制，实际调用前请确认账号权限。

## 关键参数

所有音频 API 共享以下基础参数（部分为必填）：

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `model` | string | 必填，如 `"asr-general-v2"`、`"tts-1"`；取值严格匹配 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 等文档所列模型 ID |
| `input` | object | 必填，结构依任务而异（如 ASR 传 `audio_url` 或 `audio_bytes`，TTS 传 `text`） |
| `response_format` | string | 可选，`"json"`（默认）或 `"wav"`（仅 TTS/音乐生成支持二进制响应） |
| `stream` | boolean | 可选，`true` 启用 SSE 流式响应（ASR/TTS/语音对话支持） |

## 使用方式

1. **认证**：在请求 Header 中携带 `Authorization: Bearer <api_key>`；  
2. **请求体**：以 JSON 格式提交，`input` 字段内容需符合对应子能力要求（例如语音识别需提供 `audio_url` 或 base64 编码的 `audio_bytes`）；  
3. **响应解析**：成功时返回 `200 OK`，结构参考各子文档示例；流式响应需按 SSE 协议解析 `data:` 行；  
4. **调试建议**：首次调用推荐使用非流式模式，并参考 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 中的完整 cURL 示例验证链路。

## 限制和注意事项

- 单次请求音频时长上限：ASR ≤ 600 秒，TTS 输入文本 ≤ 500 字符，音乐生成提示词 ≤ 200 字符；  
- 所有音频文件需为 PCM/WAV/MP3/M4A 格式，采样率建议 16kHz（ASR 最佳），单文件大小 ≤ 100 MB；  
- 语音对话 API 要求客户端维持 WebSocket 连接并正确处理 `session_id` 生命周期，细节见 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md)；  
- > **注意**：[语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md) 文档中声明“支持中→日、中→韩双向”，但当前后端仅开放中→英、英→中，其他语向返回 `400 Unsupported language pair` —— 该差异已在内部任务 #AUD-289 中标记为待同步更新。

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


