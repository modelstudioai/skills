# audio api references

百炼平台提供统一的音频类 API 接口，覆盖语音识别、语音合成、音乐生成、语音翻译和语音对话五大能力。所有接口均通过 RESTful 方式调用，支持流式响应与非流式响应两种模式。开发者需使用有效的 API Key 并遵循各模型的输入格式与计费规则。

## 支持的模型/功能

当前支持以下五类音频处理能力，每类对应独立的 API 端点与模型选型：

- **语音识别（ASR）**：支持中文、英文及多语种混合识别，推荐模型 `asr-general` 和 `asr-dialect`；详细参数见 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md)  
- **语音合成（TTS）**：提供多音色、多语速、情感可调的合成能力，支持 SSML 标签；具体模型列表与音色 ID 参考 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md)  
- **音乐生成**：支持文本描述生成背景音乐或完整乐曲，输出格式为 WAV/MP3；输入约束与风格控制说明详见 [音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md)  
- **语音翻译**：端到端实现语音→目标语言文本/语音的跨语种转换，暂不支持源语言自动检测；[语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md) 文档明确要求必须显式指定 `source_language` 和 `target_language`  
- **语音对话**：面向实时交互场景，支持双工语音流接入与上下文感知应答；该能力依赖专用 SDK 配合服务端 API，完整集成流程请查阅 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md)

> **注意**：原始文档中 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 提到“支持 WebSocket 长连接”，但最新 SDK v2.3.0 已弃用该方式，改用基于 HTTP/2 的双向流；请以 SDK 文档为准，避免直接复用旧版连接逻辑。

## 关键参数

通用必填参数（所有音频 API 共享）：
- `model`: 字符串，如 `"asr-general"`、`"tts-zhiyin-v1"`，不可省略  
- `input`: 对象，结构因任务而异（如 ASR 为 `{ "audio_url": "..." }`，TTS 为 `{ "text": "..." }`）  
- `api_key`: 请求头 `Authorization: Bearer <api_key>`，不参与请求体签名  

部分能力特有参数：
- ASR：`language`, `audio_format`, `sample_rate`（必须与实际音频匹配）  
- TTS：`voice`, `speed`, `pitch`, `volume`  
- 音乐生成：`duration`, `style`, `instrumentation`  
- 语音翻译：`source_language`, `target_language`, `output_format`（`text` 或 `audio`）  

## 使用方式

1. **准备音频资源**：上传音频至百炼对象存储（OSS）并获取 `audio_url`，或使用 Base64 编码内联（仅限 ≤1MB 文件）  
2. **构造请求**：POST 到对应端点（如 `https://dashscope.aliyuncs.com/api/v1/services/aigc/audio/asr`），设置 `Content-Type: application/json`  
3. **处理响应**：成功时返回 `200 OK`，结果位于 `output.text`（ASR/TTS）、`output.audio_url`（TTS/翻译）、`output.music_url`（音乐生成）等字段；流式响应需按 SSE 协议解析  

示例（ASR 调用）：
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/audio/asr \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "asr-general",
        "input": {"audio_url": "https://xxx.oss-cn-hangzhou.aliyuncs.com/test.wav"},
        "parameters": {"language": "zh"}
      }'
```

## 限制和注意事项

- 单次请求音频时长上限：ASR/TTS ≤ 5 分钟，音乐生成 ≤ 90 秒，语音翻译 ≤ 3 分钟，语音对话单轮 ≤ 60 秒  
- 音频格式要求：WAV（PCM, 16bit, 小端序）、MP3、M4A、OGG；采样率建议 16kHz（ASR/TTS）或 44.1kHz（音乐生成）  
- 错误重试：网络超时建议设为 30s，服务端错误（如 503）需指数退避重试，最大间隔不超过 60s  
- 计费单位：ASR/TTS 按音频秒数计费，音乐生成按生成时长计费，语音翻译按输入+输出音频总秒数计费  

> **注意**：[语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 文档中提及“支持 `.flac` 格式”，但实测 v2024.07 版本服务已返回 `400 UnsupportedFormat`；请优先使用 WAV/MP3，避免依赖该过时说明。

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


