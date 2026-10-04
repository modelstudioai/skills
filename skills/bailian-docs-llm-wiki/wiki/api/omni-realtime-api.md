# omni realtime api

omni realtime api 是百炼平台提供的低延迟、流式多模态推理接口，支持语音、文本、图像等输入的实时交互与响应。该 API 采用 WebSocket 协议，以事件驱动方式收发数据，适用于实时对话、音视频分析、智能座舱等对时延敏感的场景。其设计遵循统一事件模型，客户端和服务端通过标准化事件类型进行双向通信。

## 支持的模型与功能

当前支持 `omni-realtime-202409` 及后续版本的多模态模型，具备语音识别（ASR）、语音合成（TTS）、图文理解（VLM）和上下文感知生成能力。模型支持动态输入组合，例如“语音+屏幕截图”或“麦克风流+用户文字指令”。具体模型接入细节请参考 [实时多模态](../../raw/model-api-reference/omni-realtime-api.md) 文档中的 [模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)。

> **注意**：文档中提及的 `omni-realtime-202406` 版本已下线，实际调用时若指定该版本将返回 `404`；请以控制台模型列表或 [实时多模态](../../raw/model-api-reference/omni-realtime-api.md) 中最新支持列表为准。

## 关键参数

建立 WebSocket 连接时需在 URL 查询参数中传入：
- `model`: 必填，如 `omni-realtime-202409`
- `api_key`: 必填，项目级 API Key（非个人 [Token](../concepts/token.md)）
- `stream`: 可选，布尔值，默认 `true`；设为 `false` 将禁用流式响应，仅在会话结束时返回完整结果（不推荐用于实时场景）

连接后，所有消息体均为 JSON 格式，必须包含 `event` 字段（如 `"input_audio"`、`"input_text"`），详见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 和 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md) 定义。

## 使用方式

1. 构造 WebSocket URL：`wss://dashscope.aliyuncs.com/api/v1/omni/realtime?model=omni-realtime-202409&api_key=<YOUR_KEY>`  
2. 建立连接后，先发送 `session_init` 事件初始化会话（含可选 `temperature`、`max_output_tokens` 等配置）  
3. 按需发送输入事件（如 `input_audio` 分片、`input_text`）  
4. 监听服务端返回的 `output_text_delta`、`output_audio_chunk` 等事件进行实时渲染  

完整事件序列与错误码说明见 [实时多模态](../../raw/model-api-reference/omni-realtime-api.md)。

## 限制和注意事项

- 单次会话最长 300 秒，超时自动断连；如需长连接，请主动发送 `ping` 事件并处理 `pong` 响应  
- 音频输入仅支持 16kHz 单声道 PCM（`int16`），每帧建议 20–200ms，过大易触发缓冲延迟  
- 同一 `api_key` 并发连接数上限为 50，超出将拒绝新连接（HTTP 429）  
- 不支持跨域直接浏览器直连（因 `api_key` 泄露风险），生产环境必须通过后端代理中转 —— 此要求在 [实时多模态](../../raw/model-api-reference/omni-realtime-api.md) 的安全章节中有明确强调

## 来源文档

- [实时多模态](../../raw/model-api-reference/omni-realtime-api.md)


