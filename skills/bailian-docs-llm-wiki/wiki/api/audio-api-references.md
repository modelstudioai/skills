# audio api references

百炼平台提供统一的音频类 API 接口，覆盖语音合成、语音识别、音乐生成、音频生成、语音对话及语音翻译六大能力。所有接口均通过 RESTful 方式调用，支持流式响应与非流式响应两种模式。开发者需使用有效的 API Key 并遵循各模型的输入格式与配额限制。

## 支持的模型与功能

当前支持以下六类音频处理能力，对应独立的 API 端点与模型标识符：

- **语音合成（TTS）**：支持多语种、多音色、可控语速/语调，模型如 `qwen2-audio-tts-0.5b`；详见 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md)  
- **语音识别（ASR）**：支持中英文混合识别、标点恢复、说话人分离（部分模型），模型如 `qwen2-audio-asr-1.5b`；详见 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md)  
- **音乐生成**：支持文本描述生成 30s–90s 原创音乐，输出 WAV/MP3，模型如 `qwen2-music-1.0b`；详见 [音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md)  
- **音频生成（非音乐）**：生成音效、环境声、拟声词等，不支持旋律结构；参见 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md)  
- **语音对话**：端到端实时语音交互，含唤醒、理解、TTS 合成闭环，仅限 WebSocket 接入；参考 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md)  
- **语音翻译**：支持语音→目标语言文本、语音→目标语言语音双路径，延迟敏感，需指定源/目标语种；见 [语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md)

> **注意**：[语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 文档中声明支持 HTTP POST 回调模式，但最新 SDK v3.2+ 已废弃该方式，仅保留 WebSocket 实时通道——请以 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 中“接入方式”章节的 WebSocket 示例为准。

## 关键参数

所有音频 API 共享以下基础参数（部分为必填）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型 ID，如 `qwen2-audio-tts-0.5b`，不可省略 |
| `input` | object | 是 | 输入内容，结构因能力而异（如 ASR 为 `{"audio": "base64..."}`，TTS 为 `{"text": "你好"}`） |
| `parameters` | object | 否 | 控制参数，如 `{"voice": "zhiyan", "speed": 1.2}`（TTS）、`{"language": "zh"}`（ASR） |
| `stream` | boolean | 否 | 是否启用流式响应，默认 `false`；仅 TTS、ASR、语音对话支持 `true` |

> **注意**：`parameters.language` 在 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 中为可选，但在 [语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md) 中为必填；若未显式指定，ASR 默认使用 `"auto"`，而语音翻译将返回 400 错误。

## 使用方式

1. **认证**：在请求 Header 中携带 `Authorization: Bearer <api_key>`  
2. **请求地址**：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/audio/<service_name>`，其中 `<service_name>` 对应 `speech-synthesis`、`speech-recognition` 等（与子文档路径末段一致）  
3. **Body 格式**：JSON，`input` 和 `parameters` 遵循各子文档定义；音频二进制需 Base64 编码（最大 25MB）  
4. **响应**：成功时返回 `200 OK`，结构含 `output`（结果数据）与 `usage`（token/时长消耗）；错误码详见各子文档  

示例（TTS 调用）：
```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/audio/speech-synthesis" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "qwen2-audio-tts-0.5b",
        "input": {"text": "欢迎使用百炼音频 API"},
        "parameters": {"voice": "zhiyan"}
      }'
```

## 限制和注意事项

- 单次请求音频时长上限：ASR ≤ 300s，TTS ≤ 120s，音乐生成 ≤ 90s，语音对话单轮 ≤ 60s  
- 文件大小限制：Base64 编码后 ≤ 25MB（约对应原始 WAV 12MB / MP3 4MB）  
- 所有音频 API 均不支持跨区域调用，必须使用与 API Key 绑定地域一致的 endpoint（如 `dashscope.aliyuncs.com` 仅支持杭州地域）  
- 流式响应下，TTS 返回 chunked audio data（`audio/wav`），ASR 返回逐句文本 JSON；语音对话流式仅支持 WebSocket  
- 错误重试建议：对 `429 Too Many Requests` 或 `503 Service Unavailable` 应实现指数退避（初始 100ms，最多 3 次）  

如需调试，推荐先使用 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 的 Hello World 示例验证环境连通性。

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


