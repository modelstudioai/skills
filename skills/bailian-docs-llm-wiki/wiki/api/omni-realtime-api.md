# omni realtime api

omni realtime api 是百炼平台提供的低延迟、流式多模态交互接口，支持语音输入、文本理解、语音合成与视觉理解的实时协同。适用于智能客服、实时会议纪要、语音助手等需要端到端流式响应的场景。该 API 基于 Qwen-Omni 模型构建，采用 WebSocket 协议实现双向流式通信。

## 支持的模型/功能

- 当前仅支持 `qwen-omni` 模型（v1.0 及以上），不支持其他 Qwen 系列模型（如 qwen-max、qwen-plus）调用此接口  
- 支持全链路实时多模态能力：语音识别（ASR）、自然语言理解（NLU）、大模型推理（LLM）、语音合成（TTS）及可选视觉理解（需传入 base64 图像帧）  
- 功能模块解耦，允许客户端按需启用/禁用 ASR 或 TTS，例如仅使用文本输入+TTS 输出（见 [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api.md)）  
- 声音复刻能力需提前在控制台创建并绑定 voice_id，具体配置方式参见 [声音复刻](../../raw/model-api-reference/omni-realtime-api.md)

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 固定为 `"qwen-omni"`，其他值将返回 400 错误 |
| `voice_id` | string | 否 | 指定复刻音色 ID；若未提供，则使用默认系统音色（[声音复刻](../../raw/model-api-reference/omni-realtime-api.md) 中有详细说明） |
| `enable_asr` | boolean | 否 | 默认 `true`；设为 `false` 时跳过语音识别，仅处理文本输入 |
| `enable_tts` | boolean | 否 | 默认 `true`；设为 `false` 时服务端不返回音频流，仅返回文本片段 |
| `max_output_tokens` | integer | 否 | 最大生成 token 数，默认 2048，上限 4096 |

> **注意**：原始文档中部分 SDK 示例（如早期 Python SDK 文档）仍将 `model` 参数列为可选或支持别名，但实际服务端已强制校验为 `"qwen-omni"`，请以 [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api.md) 的协议定义为准。

## 使用方式

1. 建立 WebSocket 连接：`wss://dashscope.aliyuncs.com/realtime/qwen-omni/v1`（需携带鉴权 Header `Authorization: Bearer <api_key>`）  
2. 发送初始化消息（`session.update` event），包含上述关键参数及 `input_format`（`"pcm"` 或 `"wav"`）  
3. 流式发送音频帧（`input.audio` event）或文本（`input.text` event）  
4. 接收服务端事件：`output.text.delta`、`output.audio.delta`、`output.image` 等（详见 [服务端事件](../../raw/model-api-reference/omni-realtime-api.md)）  
5. 客户端可随时发送 `input.interrupt` 中断当前响应  

推荐优先使用官方 SDK：[Python SDK](../../raw/model-api-reference/omni-realtime-api.md) 提供自动重连与事件分发封装；Java SDK 同步支持流式 buffer 管理。

## 限制和注意事项

- 单次会话最长持续 300 秒，超时后连接自动关闭  
- 音频采样率必须为 16kHz，单声道，位深 16bit；非标准格式将导致 ASR 质量下降或失败  
- 不支持跨 session 的上下文继承，如需长程记忆，需由应用层维护 history 并通过 `input.text` 显式注入  
- 同一 API Key 下并发连接数上限为 50，超出将拒绝新连接（错误码 `429 Too Many Connections`）  
- 视觉理解仅支持单帧图像（非视频流），且每帧需 ≤ 5MB，格式为 JPEG/PNG  

> **注意**：原始文档中“客户端事件”链接指向的帮助中心页面未明确说明 `input.interrupt` 的幂等性行为，实测多次发送相同 interrupt id 不会重复触发中断，但建议客户端对 interrupt 做去重处理，避免状态错乱。

## 来源文档

- [实时多模态](../../raw/model-api-reference/omni-realtime-api.md)


