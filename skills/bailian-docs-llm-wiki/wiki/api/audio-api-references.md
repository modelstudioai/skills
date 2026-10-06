# audio api references

百炼平台提供统一的音频类 API 接口，覆盖语音合成、语音识别、音频/音乐生成、语音对话及语音翻译等核心能力。所有接口均通过 RESTful 方式调用，支持流式响应与非流式响应两种模式。开发者需根据具体任务选择对应模型，并严格遵循各接口的参数约束与配额限制。

## 支持的模型与功能

当前支持以下六大音频处理能力，每类均有独立的模型与 API 文档：
- 语音合成（TTS）：支持多语种、多音色、情感调节，详见 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md)  
- 音频生成：面向环境音、音效、ASMR 等非音乐类音频内容，详见 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md)  
- 音乐生成：支持旋律创作、风格迁移、歌词续写等，详见 [音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md)  
- 语音识别（ASR）：支持长语音、带标点、多语种混合识别，详见 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md)  
- 语音对话：端到端实时语音交互，含唤醒、VAD、TTS 合成闭环，详见 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md)  
- 语音翻译：支持语音→文本翻译（ST）及语音→语音翻译（S2S），详见 [语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md)

> **注意**：[语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 文档中描述的 `enable_vad=true` 默认行为，与最新 SDK v2.3.0 实际行为不符（实际默认为 `false`），请以 SDK 文档或 OpenAPI Schema 为准。

## 关键参数

所有音频 API 共享以下基础参数（部分接口有扩展）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen2-audio-tts-16k`、`qwen2-audio-asr-zh`；完整列表见各子文档 |
| `input` | object | 是 | 输入结构体，格式因任务而异（如 ASR 的 `audio_url` 或 `audio_bytes`，TTS 的 `text`） |
| `parameters` | object | 否 | 模型级控制参数，如 `temperature`（仅音乐生成支持）、`voice_type`（TTS）、`language`（ASR/ST） |
| `stream` | boolean | 否 | 是否启用流式响应，默认 `false`；流式模式下响应为 SSE 格式 |

> **注意**：`parameters.sample_rate` 在 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md) 和 [音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md) 中含义不一致——前者指输出采样率（仅支持 16000/24000/48000），后者指输入参考音频采样率（必须匹配上传音频）。使用时请严格对照对应文档。

## 使用方式

1. **认证**：在请求 Header 中携带 `Authorization: Bearer <api_key>`  
2. **Endpoint**：统一前缀 `https://dashscope.aliyuncs.com/api/v1/`，后接子路径（如 `/audio/tts`、`/audio/asr`）  
3. **请求体**：JSON 格式，`input` 字段需按接口要求构造（如 ASR 支持 `audio_url` 远程 URL 或 `audio_bytes` Base64 编码二进制）  
4. **响应解析**：非流式返回 `output.audio_url`（直连可下载）或 `output.text`；流式响应按 chunk 解析 `data:` 行中的 JSON  

示例（TTS 调用）：
```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/audio/tts" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "qwen2-audio-tts-16k",
        "input": {"text": "你好，欢迎使用百炼音频 API。"},
        "parameters": {"voice_type": "zhitian_003"}
      }'
```

## 限制和注意事项

- **文件大小**：ASR/ST 最大支持 120 分钟音频（MP3/WAV/FLAC），TTS 输入文本长度上限 5000 字符  
- **并发与配额**：免费版限 5 QPS，企业版按 license 配置；单次请求超时为 300 秒（音乐生成类任务建议设为 600 秒）  
- **格式要求**：所有音频输入须为单声道，采样率建议 16kHz；非标准格式（如 AMR、AAC）需先转码  
- **地域限制**：`/audio/voice-conversation` 接口仅在 `cn-shanghai` 地域可用，详见 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md)  
- **错误处理**：常见错误码 `400 Bad Request` 多因 `input` 结构错误或 `model` 不匹配，建议优先校验 [原文标题](../../raw/model-api-reference/audio-api-references.md) 中列出的子接口路径与模型兼容性

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


