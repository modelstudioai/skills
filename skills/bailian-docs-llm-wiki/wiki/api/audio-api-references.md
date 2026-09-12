# audio api references

百炼平台提供多种音频处理能力的 API 接口，覆盖语音识别、语音合成、音乐生成、语音翻译和语音对话五大核心场景。所有接口均通过统一的 RESTful API 形式调用，支持流式与非流式响应。开发者需根据具体任务选择对应模型，并注意各接口在输入格式、时长限制及计费维度上的差异。

## 支持的模型/功能

当前支持以下音频相关能力：
- **语音识别（ASR）**：将音频转为文本，支持多语种、带标点和说话人分离选项  
- **语音合成（TTS）**：文本转语音，提供多种音色与语速调节能力  
- **音乐生成**：根据文本描述生成高质量背景音乐或完整乐曲片段  
- **语音翻译**：实时将一种语言的语音识别并翻译为另一种语言的文本或语音  
- **语音对话**：端到端语音交互，支持唤醒、语义理解与语音应答闭环  

各能力详情请参阅 [音频](../../raw/model-api-reference/audio-api-references.md) 文档中列出的官方链接。

## 关键参数

通用关键参数包括：
- `model`：必需，指定模型标识符（如 `paraformer-v1`、`cosyvoice-v1`、`musicgen-v1`）  
- `audio_url` 或 `audio_bytes`：二选一，音频源（远程 URL 或 base64 编码 PCM/WAV/MP3 数据）  
- `format`：音频编码格式（`wav`、`mp3`、`pcm`），部分模型强制要求 `wav`（详见 [音频](../../raw/model-api-reference/audio-api-references.md)）  
- `sample_rate`：采样率（Hz），常见值为 `16000`；不匹配将触发自动重采样或报错  
- `response_format`：返回格式（`json` 或 `stream`），仅部分接口支持流式（如 TTS、ASR 实时模式）

> **注意**：`musicgen-v1` 模型当前不支持 `sample_rate` 参数自定义，固定使用 32kHz 内部采样——该行为与 [音频](../../raw/model-api-reference/audio-api-references.md) 中“音乐生成”链接指向的文档描述存在不一致，以实际 API 行为为准。

## 使用方式

1. 构造 POST 请求至 `/api/v1/audio/{task}`（如 `/api/v1/audio/transcribe`）  
2. 设置 `Authorization: Bearer <api_key>` 与 `Content-Type: application/json`  
3. 在请求体中传入上述关键参数（示例见 [音频](../../raw/model-api-reference/audio-api-references.md) 所引各子文档）  
4. 解析响应：成功时返回 `200 OK` 及结构化 JSON；流式接口需按 SSE 协议解析事件流  

## 限制和注意事项

- 单次请求音频时长上限：ASR/TTS ≤ 60 秒，音乐生成 ≤ 30 秒，语音翻译 ≤ 120 秒  
- 音频文件大小上限：50 MB（URL 方式无此限制，但需确保可公开访问）  
- 所有音频输入必须为单声道；双声道将被静音左/右通道之一（具体策略依模型而定）  
- 语音对话接口需配合特定 SDK 初始化会话上下文，纯 HTTP 调用仅支持单轮问答  

请务必查阅各子能力的最新接口规范，例如 [语音识别](https://help.aliyun.com/zh/model-studio/speech-recognition-api-reference) 和 [语音合成](https://help.aliyun.com/zh/model-studio/speech-synthesis-api-reference) 的官方说明，避免因版本迭代导致参数失效。

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)



