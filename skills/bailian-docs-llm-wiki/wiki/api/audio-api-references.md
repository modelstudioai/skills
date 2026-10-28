# audio api references

百炼平台的 Audio API 提供语音合成、音频生成、语音识别、语音对话和语音翻译五大核心能力，所有接口均通过统一的 RESTful 方式调用，支持流式响应与非流式响应。各能力由专用模型支撑，需按场景选择对应模型并传入规范参数。详细实现细节请参考 [原文标题](../../raw/model-api-reference/audio-api-references.md)。

## 支持的模型与功能

| 功能             | 对应模型（示例）                     | 说明 |
|------------------|----------------------------------------|------|
| 语音合成         | `qwen-audio-tts-v1`                    | 支持中英文多音色、语速/音调调节，输出 WAV/MP3 格式；详见 [原文标题](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) |
| 音频生成         | `qwen-audio-gen-v1`                    | 文本到背景音/音效/音乐片段生成，支持 [prompt](../guides/prompt.md) 控制风格与时长 |
| 语音识别         | `qwen-audio-asr-v1`                    | 支持单/多通道音频、带标点和说话人分离（需开启 `diarization=true`），采样率建议 16kHz；参见 [原文标题](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) |
| 语音对话         | `qwen-audio-conversation-v1`           | 实时双工语音交互，需配合 WebSocket 长连接，支持中断重连与上下文保持 |
| 语音翻译         | `qwen-audio-st-v1`                     | 端到端语音→目标语言文本/语音，当前仅支持中↔英互译 |

> **注意**：文档中提及的 `qwen-audio-asr-v2` 模型已在 v2.3.0 版本后下线，实际可用模型以 [原文标题](../../raw/model-api-reference/audio-api-references.md) 中最新列表为准，旧文档中残留的 v2 型号描述已过时。

## 关键参数

通用必填参数：
- `model`: 模型标识符（如 `qwen-audio-tts-v1`），不可省略  
- `input`: 输入结构体，格式依能力而异（如 ASR 的 `audio_url` 或 `audio_bytes`，TTS 的 `text`）  
- `parameters`: 可选配置对象，常见字段包括：  
  - `voice`: TTS 专用音色 ID（如 `"zhitian_emo"`）  
  - `sample_rate`: 输出音频采样率（ASR/TTS 均支持 16000/22050/44100）  
  - `response_format`: 返回格式（`json` / `wav` / `mp3`）  
  - `enable_stream`: 是否启用流式响应（`true` / `false`）

## 使用方式

1. **认证**：在请求 Header 中携带 `Authorization: Bearer <api_key>`  
2. **请求地址**：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/audio/<service_name>`（`<service_name>` 如 `tts`、`asr`）  
3. **Body 示例（TTS）**：
   ```json
   {
     "model": "qwen-audio-tts-v1",
     "input": {"text": "你好，欢迎使用百炼语音服务。"},
     "parameters": {"voice": "zhitian_emo", "sample_rate": 22050}
   }
   ```
4. 流式响应需设置 `Accept: text/event-stream`，并按 SSE 协议解析 chunk。

## 限制和注意事项

- 单次请求音频时长上限：ASR ≤ 600 秒，TTS ≤ 300 秒，音频生成 ≤ 30 秒  
- [文件上传](../concepts/file-upload.md)方式仅支持 `audio_url`（公网可访问 HTTPS URL）或 Base64 编码的 `audio_bytes`（≤ 25MB）  
- 语音对话接口要求客户端维持 WebSocket 连接，超时断连后需重新初始化会话  
- 所有音频输入必须为 PCM/WAV/MP3/OPUS 格式，不支持 AMR、WMA 等非标准格式  
- > **注意**：部分旧版 SDK 示例中将 `speech_translation` 的 service_name 写为 `st`，但当前 API 路由已统一为 `speech-translation`，务必以 [原文标题](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md) 中定义为准。

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


