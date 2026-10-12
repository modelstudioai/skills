# omni realtime api

omni realtime api 是百炼平台提供的低延迟、流式[多模态](../concepts/multi-modal.md)实时交互接口，支持语音、文本、图像等多类型输入的实时处理与响应。该 API 采用 WebSocket 协议，基于事件驱动模型实现双向流式通信，适用于实时对话、音视频分析、交互式智能体等场景。详细协议规范和事件定义请参考 [实时多模态](../../raw/model-api-reference/omni-realtime-api.md)。

## 支持的模型/功能

当前支持 `omni-realtime-202409` 模型版本（默认），具备以下能力：
- 实时语音识别（ASR）与合成（TTS）
- 多轮上下文感知的文本生成
- 图像理解（需通过 `image_url` 或 base64 上传，单图最大 10 MB）
- 音视频流端到端低延迟处理（端到端 P95 < 800 ms）

> **注意**：文档 [实时多模态](../../raw/model-api-reference/omni-realtime-api.md) 中提及的 `omni-realtime-202406` 已下线，实际调用将自动路由至最新稳定版；旧版参数兼容性请以 [模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md) 为准。

## 关键参数

WebSocket 连接需在 URL 中携带以下查询参数（均为必需）：
- `model`: 模型标识符，目前仅支持 `omni-realtime-202409`
- `api_key`: 百炼平台有效 API Key（需具备 `realtime` 权限 scope）
- `stream`: 布尔值，必须为 `true`

连接建立后，首条客户端消息须为 `session.update` 事件，其中可设置：
- `input_audio_format`（如 `"pcm-16000"`）、`output_audio_format`（如 `"mp3"`）
- `max_output_tokens`（默认 1024，上限 2048）
- `temperature`（0.0–1.0，仅影响文本生成）

完整事件字段说明见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 和 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)。

## 使用方式

1. 构建 WebSocket URL：`wss://dashscope.aliyuncs.com/api/v1/omni/realtime?model=omni-realtime-202409&api_key=<YOUR_KEY>&stream=true`  
2. 发送 `session.update` 初始化会话（含音频/输出配置）  
3. 按需发送 `input.audio`、`input.text` 或 `input.image` 事件  
4. 监听 `output.text.delta`、`output.audio.delta` 等服务端流式响应事件  

示例代码与错误码列表详见 [模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)。

## 限制和注意事项

- 单连接最长存活时间：300 秒（超时无 activity 将断连）  
- 并发连接数上限：每个 API Key 最多 10 个活跃连接  
- 音频输入要求：单次 `input.audio` 数据块 ≤ 4 KB，采样率必须与 `input_audio_format` 严格匹配  
- 不支持跨 session 的上下文继承；如需长程记忆，需由客户端维护并显式传入 `session.context`  

> **注意**：[服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md) 中描述的 `error.code: 429` 行为已更新——现返回 `rate_limit_exceeded` 而非 `too_many_requests`，请按新 code 字符串做判断。

## 来源文档

- [实时多模态](../../raw/model-api-reference/omni-realtime-api.md)


