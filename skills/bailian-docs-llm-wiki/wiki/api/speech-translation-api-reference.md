# speech translation api reference

本文档汇总百炼平台语音与音视频翻译 API 的核心协议、参数配置及集成方式，涵盖 [[openai-compatible-api|OpenAI 兼容接口]]与 WebSocket 实时接口两类技术路线。开发者可根据业务对延迟、多模态输入及音频输出的要求选择合适的调用模型，并通过官方 SDK 或标准协议快速对接。所有接口均支持[[streaming-output|流式输出]]与细粒度会话控制，适用于同声传译、多语言会议及音视频实时转译场景。

## 支持的模型与核心功能

| 调用协议 | 推荐模型 | 核心能力 | 适用场景 |
|:---|:---|:---|:---|
| **OpenAI 兼容 HTTP** (`/chat/completions`) | `qwen3-livetranslate-flash` | 支持音频/视频公网 URL 输入，强制流式返回译文与音频。详见 [音视频翻译-通义千问 API 参考](../../raw/model-api-reference/speech-translation-api-reference/qwen3-livetranslate-flash-api.md) | 异步文件翻译、视频内容转写与翻译、Web 后端批量处理 |
| **WebSocket 实时接口** (`wss://.../realtime`) | `qwen3.5-livetranslate-flash-realtime` | 低延迟语音流推送、服务端自动 VAD、实时音频/文本流输出、支持声音复刻与热词定制。详见 [客户端事件](../../raw/model-api-reference/speech-translation-api-reference/live-translator-api/live-translator-client-events.md) | 同声传译设备、实时语音通话、移动端交互式翻译 |

**核心功能特性**：
- **多模态输入**：HTTP 接口支持 `input_audio` 与 `video_url`；WebSocket 接口支持 PCM 音频流与实时 JPG 图像流缓冲。
- **输出控制**：支持纯文本或文本+音频双模态输出，可指定发音人（Voice）与音频格式。
- **辅助能力**：内置 [[qwen-asr-realtime]] 语音识别模型可同步返回源语言原文；支持 [[voice-cloning-api]] 实现输入音色克隆；支持自定义 `corpus` 映射表提升专有名词准确率。

## 关键参数配置

### 1. [[openai-compatible-api|OpenAI 兼容接口]]参数
- `model`：必填。当前仅支持 `qwen3-livetranslate-flash`。
- `messages`：必填。数组类型，仅允许传入单条 `role: "user"` 消息。`content` 中需指定 `type: "input_audio"` 或 `type: "video_url"`。
- `translation_options`：**非标准参数（必填）**。包含 `target_lang`（目标语言代码，必填）与 `source_lang`（可选，默认自动识别）。
- `modalities`：可选，默认 `["text"]`。需输出音频时设为 `["text", "audio"]`。
- `audio`：模态含音频时必填，配置 `voice`（音色标识）与 `format`（仅支持 `"wav"`）。
- `stream`：**强制必填**且仅支持 `true`。模型不支持非流式同步响应。

### 2. WebSocket 实时接口与会话参数
通过 `session.update` 事件或 SDK 配置类下发：
- `modalities` / `voice`：输出模态与音色。未启用复刻时需使用系统预设音色。
- `translation`：目标语言 `language` 及热词映射 `corpus.phrases`（Key: 源语, Value: 目标语）。
- `input_audio_transcription`：设置 `model: "qwen3-asr-flash-realtime"` 以流式获取原文识别结果。
- `enable_voice_clone`：布尔值。开启后配合 `voice_clone_options.frequency` 控制复刻策略（`once`/`always`/`never`）。

> **注意**：
> - `translation_options`、`top_k`、`repetition_penalty` 等参数不属于 OpenAI 标准协议。在 Python OpenAI SDK 中必须置于 `extra_body` 对象内传递；Node.js SDK 或原生 HTTP 请求需作为顶层参数平铺。
> - 文档中提及的旧版模型 `qwen3-livetranslate-flash-realtime` 已标记为过时，新业务请统一使用 `qwen3.5-livetranslate-flash-realtime`。
> - 实时接口连接成功后服务端默认返回的音频格式为 `pcm16`/`pcm24`，而 `session.updated` 响应示例中简写为 `pcm`。实际开发请以 `OmniRealtimeAudioFormat` 枚举或显式声明的采样率为准。

## 调用方式

### HTTP / SDK (OpenAI 兼容)
使用标准 OpenAI SDK，按地域配置 `base_url`（北京 `dashscope.aliyuncs.com` / 新加坡 `dashscope-intl.aliyuncs.com`），通过 `messages` 构造多模态输入，开启流式遍历 Chunk。

```python
# Python OpenAI SDK 示例核心结构
completion = client.chat.completions.create(
    model="qwen3-livetranslate-flash",
    messages=[{"role": "user", "content": [...]}],
    modalities=["text", "audio"],
    audio={"voice": "Cherry", "format": "wav"},
    stream=True, stream_options={"include_usage": True},
    extra_body={"translation_options": {"target_lang": "en"}}
)
```

### WebSocket 原生调用
1. 建立 `wss` 连接，接收 `session.created`。
2. 发送 `session.update` 覆盖默认翻译配置。
3. 循环发送 `input_audio_buffer.append`（Base64 PCM 片段）与可选的 `input_image_buffer.append`。
4. 语音停止后发送 `session.finish`，等待 `session.finished` 事件后安全断开。服务端事件解析详见 [服务端事件](../../raw/model-api-reference/speech-translation-api-reference/live-translator-api/live-translator-server-events.md)。

### 官方 SDK 集成
- **Python**：引入 `dashscope.audio.qwen_omni`。通过 `OmniRealtimeConversation` 管理连接，实现 `OmniRealtimeCallback` 处理 `response.audio.delta`、`response.audio_transcript.done` 等回调事件。集成指南参考 [[dashscope-python-sdk]]。
- **Java**：引入 `com.alibaba.dashscope.audio.omni`。通过 `OmniRealtimeParam` 构建连接参数，使用 `OmniRealtimeConfig` 链式配置会话。实现 `OmniRealtimeCallback` 接口接收流数据。集成指南参考 [[dashscope-java-sdk]]。

## 限制与注意事项

- **地域与 Key 隔离**：中国内地与国际（新加坡）地域的 Endpoint、WebSocket 地址及 [[api-key-management]] 严格隔离，混用将导致鉴权失败。
- **音频与图像输入规范**：
  - WebSocket 模式默认要求 16kHz 16bit PCM 流，需 Base64 编码后追加至云端缓冲区。
  - 图像输入限制为 JPG/JPEG，单张 ≤500KB，帧率 ≤2张/秒。**必须在发送过至少一次 `input_audio_buffer.append` 后才允许发送图像缓冲事件**，否则将被拒绝。
- **强制流式调用**：HTTP 接口 `stream` 参数不可为 `false`，非流式请求将直接返回参数错误。
- **会话生命周期管理**：客户端调用 `endSession()` 或发送 `session.finish` 后，服务端会完成当前语音段的翻译与转写。**必须在收到 `session.finished` 事件后再主动关闭 WebSocket**，提前断连可能导致计费异常或最后一句翻译丢失。
- **采样与参数建议**：为翻译稳定性，`temperature`、`top_p`、`presence_penalty` 等控制生成多样性的参数强烈建议保持默认值（接近 0 或 0.8），修改可能引发译文不一致。

## 来源文档

- [音视频翻译-通义千问 API 参考](../../raw/model-api-reference/speech-translation-api-reference/qwen3-livetranslate-flash-api.md)
- [客户端事件](../../raw/model-api-reference/speech-translation-api-reference/live-translator-api/live-translator-client-events.md)
- [服务端事件](../../raw/model-api-reference/speech-translation-api-reference/live-translator-api/live-translator-server-events.md)
- [实时音视频翻译（Qwen-LiveTranslate）Python SDK-API参考](../../raw/model-api-reference/speech-translation-api-reference/live-translator-api/qwen-livetranslate-python-sdk.md)
- [实时音视频翻译（Qwen-LiveTranslate）Java SDK-API参考](../../raw/model-api-reference/speech-translation-api-reference/live-translator-api/qwen-livetranslate-java-sdk.md)

