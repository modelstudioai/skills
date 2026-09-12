# omni realtime api

omni realtime api 是百炼平台提供的低延迟、流式多模态交互接口，支持语音输入、文本理解、语音合成与视觉理解的实时协同。适用于智能客服、实时会议纪要、语音助手等需要端到端流式响应的场景。该 API 基于 Qwen-Omni 架构实现，需通过 WebSocket 连接进行双向事件通信。

## 支持的模型/功能

- 当前仅支持 `qwen-omni` 模型（v1.0 及以上），不支持其他 Qwen 系列模型或第三方模型  
- 支持全链路实时多模态能力：语音识别（ASR）→ 文本理解（LLM）→ 语音合成（TTS）→ 可选图像理解（VLM），各阶段可独立启用或组合使用  
- 支持声音复刻（Voice Cloning），需提前上传参考音频并获取 voice_id；详细流程见 [声音复刻](https://help.aliyun.com/zh/model-studio/qwen-omni-voice-cloning) —— 该能力在 [原文标题](../../raw/model-api-reference/omni-realtime-api.md) 中有明确说明，但注意其依赖独立的声纹注册 API，非本接口内联完成。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 固定为 `"qwen-omni"`，其他值将被拒绝 |
| `stream` | boolean | 是 | 必须为 `true`，不支持非流式调用 |
| `enable_audio` | boolean | 否 | 默认 `true`，禁用后关闭 ASR/TTS，仅保留文本通道 |
| `voice_id` | string | 否 | 声音复刻 ID；若提供，TTS 将使用定制音色；参见 [原文标题](../../raw/model-api-reference/omni-realtime-api.md) 中的客户端事件文档说明 |
| `max_output_tokens` | integer | 否 | 最大生成 token 数，默认 2048，硬上限 4096 |

> **注意**：原始文档中 [实时多模态交互流程](https://help.aliyun.com/zh/model-studio/omni-realtime-interaction-process) 描述了 `audio_input_format: "pcm16"` 为唯一支持格式，但最新 SDK 实际已支持 `wav` 和 `mp3` 封装（需带有效 PCM 数据），此差异已在 [原文标题](../../raw/model-api-reference/omni-realtime-api.md) 的 Python SDK 文档中得到验证，请以 SDK 行为为准。

## 使用方式

1. 建立 WebSocket 连接，Endpoint 格式：`wss://dashscope.aliyuncs.com/realtime/v1/omni`  
2. 发送 `session.create` 初始化消息（含 `model`, `stream`, `voice_id` 等）  
3. 按需发送 `input.audio`（二进制 PCM 音频帧）或 `input.text`（UTF-8 字符串）  
4. 接收服务端事件：`output.text.delta`, `output.audio.chunk`, `output.vision.result` 等  
5. 全流程事件规范详见 [客户端事件](https://help.aliyun.com/zh/model-studio/client-events) 和 [服务端事件](https://help.aliyun.com/zh/model-studio/server-events)，均在 [原文标题](../../raw/model-api-reference/omni-realtime-api.md) 中列出为权威参考。

## 限制和注意事项

- 单次会话最长 120 秒，超时自动断连；如需持续交互，须新建 session  
- 音频输入采样率必须为 16kHz，单通道，16-bit little-endian PCM；非标准格式需客户端自行转码  
- 不支持并发发送多个 `input.audio` 帧而未等待服务端 `ack`，否则可能触发流控丢帧  
- 错误码 `429 Too Many Requests` 表示当前项目级 QPS 超限，需检查配额或降频；该行为与通用 dashscope 限流策略一致，但 omni realtime 的熔断阈值更低（默认 5 QPS/项目）

## 来源文档

- [实时多模态](../../raw/model-api-reference/omni-realtime-api.md)


