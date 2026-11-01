# omni realtime api

omni realtime api 是百炼平台提供的低延迟、流式多模态实时交互接口，支持语音、文本、图像等多类型输入的实时处理与响应。该 API 采用 WebSocket 协议实现双向流式通信，适用于实时对话、音视频分析、智能座舱等对时延敏感的场景。其设计遵循事件驱动模型，客户端与服务端通过结构化事件进行状态同步与数据交换。

## 支持的模型与功能

当前支持 `qwen2-audio-realtime-v1` 和 `qwen2-vl-realtime-v1` 两类实时多模态模型，分别面向音频流和视觉-语言联合流任务。模型能力包括实时语音识别（ASR）、语义理解、多轮上下文保持、图像帧级理解及流式文本生成。所有模型均需通过 [模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md) 中定义的鉴权与会话初始化流程启用。

## 关键参数

- `model`: 必填，指定模型标识符（如 `qwen2-audio-realtime-v1`），必须与 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 中声明的模型能力匹配  
- `sample_rate`: 音频输入必填，仅支持 16000 或 48000 Hz；图像输入则需指定 `frame_rate` 和 `resolution`  
- `enable_interim_results`: 布尔值，默认 `true`，控制是否返回中间识别结果（ASR）或分块生成文本（LLM）  
- `max_latency_ms`: 整数，单位毫秒，建议设为 300–800，影响服务端调度策略；超出将触发 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md) 中的 `latency_exceeded` 通知  

> **注意**：原始文档中 `max_latency_ms` 的默认值在 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 中标注为 `500`，但在 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md) 示例中使用 `300` 作为基准阈值。实际行为以服务端事件定义的触发逻辑为准，建议显式传入。

## 使用方式

1. 建立 WebSocket 连接，URL 格式为 `wss://dashscope.aliyuncs.com/realtime/v1/omni`，携带 `Authorization: Bearer <api_key>` 头  
2. 发送 `session.update` 事件初始化会话（含 `model`, `sample_rate` 等参数）  
3. 持续发送 `input.audio` / `input.image` / `input.text` 事件流，接收 `output.text.delta` / `output.audio.chunk` 等服务端事件  
4. 会话结束前需发送 `session.terminate`；异常断连时服务端将在 30 秒后自动清理资源  

完整事件协议与序列约束详见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 与 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)。

## 限制和注意事项

- 单会话最大持续时间 10 分钟，超时后连接强制关闭并返回 `session.expired` 事件  
- 音频流要求 PCM 编码、小端序、16-bit，不支持压缩格式（如 MP3、Opus）；图像流需为 RGB/BGR 格式原始帧，JPEG 编码需客户端自行解码  
- 同一 API Key 下并发实时会话数上限为 5，超出请求将被拒绝并返回 `429 Too Many Requests`  
- 服务端事件中的 `error.code` 字段可能包含 `invalid_input_format`、`model_unavailable` 等枚举值，具体含义请参考 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md) 定义

## 来源文档

- [实时多模态](../../raw/model-api-reference/omni-realtime-api.md)


