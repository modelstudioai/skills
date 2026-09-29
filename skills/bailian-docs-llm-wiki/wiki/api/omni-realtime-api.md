# omni realtime api

omni realtime api 是百炼平台提供的低延迟、流式多模态推理接口，支持语音、文本、图像等模态的实时交互。该 API 采用 WebSocket 协议，以事件驱动方式实现双向通信，适用于实时对话、音视频分析、交互式智能体等场景。其设计强调端到端时延可控与事件语义清晰，不提供 HTTP 轮询替代方案。

## 支持的模型/功能

当前仅支持 `qwen-omni-realtime-202410` 模型（v1.2+），该模型具备语音识别（ASR）、语音合成（TTS）、多轮上下文理解及轻量视觉理解能力。不支持图像生成或离线批量处理。所有功能均通过 [模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md) 中定义的握手流程启用，具体能力集以该文档为准。客户端需按 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 规范发送 `start`, `audio_chunk`, `text_input` 等事件；服务端响应遵循 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md) 定义的 `transcript`, `tts_audio`, `response_text` 等结构。

## 关键参数

- `model`: 必填，固定为 `qwen-omni-realtime-202410`（其他值将被拒绝）  
- `sample_rate`: 音频采样率，仅支持 `16000`（Hz），非此值将导致 `audio_chunk` 事件被静默丢弃  
- `language`: 可选，`zh`, `en`, `ja`, `ko`；默认 `zh`，但 `zh` 与 `en` 混合输入时可能触发降级行为（详见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 的 language 兼容性说明）  
- `enable_tts`: 布尔值，默认 `false`；设为 `true` 后服务端才推送 `tts_audio` 事件  

> **注意**：原始文档中 `raw/model-api-reference/omni-realtime-api.md` 的导航栏列出三篇子文档，但未明确说明 `enable_tts` 参数在握手请求体中的位置——实际应置于 `initial_message` 的 JSON payload 内，而非 WebSocket URL query string，此细节以 [模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md) 为准。

## 使用方式

1. 建立 WebSocket 连接，URL 格式为 `wss://dashscope.aliyuncs.com/realtime/v1/omni`  
2. 发送 `auth` 事件携带 `api_key`（需提前在控制台开通权限）  
3. 发送 `start` 事件，包含 `model`, `sample_rate`, `language` 等初始化参数  
4. 流式发送 `audio_chunk`（Base64 编码的 PCM 数据）或 `text_input` 事件  
5. 监听服务端 `transcript`, `response_text`, `tts_audio` 等事件并处理  

完整握手与事件序列示例见 [模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)。

## 限制和注意事项

- 单连接最大持续时长：180 秒（超时后连接关闭，需重连）  
- 音频流要求：单次 `audio_chunk` 数据 ≤ 64KB，间隔建议 ≤ 200ms，否则可能触发 ASR 重置  
- 不支持跨连接上下文共享；如需长会话，须由客户端维护 session state 并在 `start` 中传递 `session_id`（该字段无服务端校验，仅作透传）  
- `tts_audio` 事件返回的音频为 `audio/pcm; rate=24000`，需客户端自行解码播放  

> **注意**：`raw/model-api-reference/omni-realtime-api.md` 中未声明连接时长限制，但实测与平台通用实时 API SLA 一致（180 秒），此限制以 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md) 的 `error` 事件描述及控制台配额页为准。

## 来源文档

- [实时多模态](../../raw/model-api-reference/omni-realtime-api.md)


