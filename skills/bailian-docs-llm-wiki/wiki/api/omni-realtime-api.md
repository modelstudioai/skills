# omni realtime api

omni realtime api 是百炼平台提供的低延迟、流式多模态实时交互接口，支持语音、文本、图像等多类型输入的实时处理与响应。该 API 采用 WebSocket 协议，基于事件驱动模型实现双向流式通信，适用于实时对话、音视频分析、交互式智能体等场景。详细协议规范和事件定义请参考 [实时多模态](../../raw/model-api-reference/omni-realtime-api.md)。

## 支持的模型/功能

当前支持 `omni-realtime-202409` 模型版本（默认），具备以下能力：
- 实时语音识别（ASR）与合成（TTS）
- 多轮上下文感知的文本生成
- 图像理解（需通过 `image_url` 或 base64 上传，单图最大 10 MB）
- 音视频流端到端低延迟处理（端到端 P95 < 800 ms）

> **注意**：文档 [实时多模态](../../raw/model-api-reference/omni-realtime-api.md) 中提及的 `omni-realtime-202406` 已下线，实际调用将自动路由至最新稳定版；旧版参数兼容性请以 [模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md) 为准。

## 关键参数

WebSocket 连接需在 URL 中携带以下查询参数（均为必需）：
- `model`: 模型标识，目前仅支持 `omni-realtime-202409`
- `api_key`: 百炼平台有效 API Key（需具备 `realtime` 权限 scope）
- `stream`: 布尔值，必须为 `true`

消息体中关键字段（JSON 格式）：
- `event`: 事件类型，如 `"input_audio"`、`"input_text"`、`"input_image"`
- `audio_chunk`: 音频分片（PCM 16-bit, 16kHz, mono），base64 编码
- `max_output_tokens`: 单次响应最大 token 数（128–4096，默认 2048）
- `temperature`: 控制生成随机性（0.0–1.0，默认 0.7）

完整事件结构与字段约束详见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 和 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)。

## 使用方式

1. 建立 WebSocket 连接：  
   `wss://dashscope.aliyuncs.com/realtime/v1/omni?model=omni-realtime-202409&api_key=<YOUR_KEY>&stream=true`

2. 发送初始化事件（`session.update`）配置会话参数（如语言、TTS voice）

3. 按需发送输入事件（如 `input_audio`、`input_text`），服务端将立即返回 `output_text`、`output_audio` 等流式事件

4. 连接保持活跃；超时 30 秒无消息将被服务端关闭

示例代码与错误码说明见 [模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)。

## 限制和注意事项

- 单连接最长持续 10 分钟；超时后需重建连接
- 音频流要求严格按 16kHz PCM 分片，非标准格式将触发 `invalid_audio_format` 错误
- 同一 `api_key` 并发连接数上限为 50（企业版可申请提升）
- 图像输入不支持 GIF 动画，仅接受 JPEG/PNG；若使用 base64，请勿包含 `data:image/...;base64,` 前缀

> **注意**：[实时多模态](../../raw/model-api-reference/omni-realtime-api.md) 中描述的 `session.reset` 事件已废弃，应改用新建连接方式重置会话状态。

## 来源文档

- [实时多模态](../../raw/model-api-reference/omni-realtime-api.md)


