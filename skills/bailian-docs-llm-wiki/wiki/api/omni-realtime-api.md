# omni realtime api

omni realtime api 是百炼平台提供的低延迟、流式多模态实时交互接口，支持语音输入/输出、文本流式响应与视觉理解能力的协同。该 API 采用 WebSocket 协议实现双向实时通信，适用于智能客服、实时会议辅助、语音助手等场景。详细协议规范和事件定义见 [实时多模态](../../raw/model-api-reference/omni-realtime-api.md)。

## 支持的模型/功能

- 当前仅支持 `qwen-omni-realtime-v1` 模型（v2 尚未 GA，详见 [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)）  
- 支持语音识别（ASR）、大语言模型推理（LLM）、语音合成（TTS）三阶段端到端流式处理  
- 可选启用声音复刻（Voice Cloning），需提前上传参考音频并获取 voice_id；具体配置方式参见 [声音复刻](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)  

> **注意**：文档中提及的 `qwen-omni-v2` 模型在当前生产环境尚未开放，调用将返回 `404 model not found`；请以 [实时多模态](../../raw/model-api-reference/omni-realtime-api.md) 中的模型列表为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 固定为 `qwen-omni-realtime-v1` |
| `voice_id` | string | 否 | 声音复刻 ID；若不传则使用默认 TTS 声音 |
| `enable_interim_results` | boolean | 否 | 默认 `false`；设为 `true` 时服务端将推送 ASR 中间识别结果（见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)） |
| `max_input_audio_seconds` | number | 否 | 单次语音输入最大时长（秒），默认 30，上限 60 |

## 使用方式

1. 建立 WebSocket 连接：`wss://dashscope.aliyuncs.com/realtime/v1/omni`（需携带 `Authorization: Bearer <api_key>` 和 `X-DashScope-Date` 头）  
2. 发送 `session.update` 控制帧初始化会话（含 `model`、`voice_id` 等参数）  
3. 通过 `input.audio` 帧持续发送 PCM 音频数据（16kHz, 16-bit, mono）  
4. 接收服务端 `output.text.delta`、`output.audio.delta` 等流式事件（完整事件类型见 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)）  
5. 官方 SDK 已封装连接管理与帧序列化逻辑：[Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)、[Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)

## 限制和注意事项

- 单连接最长存活时间 10 分钟；超时后需重连并重新 `session.update`  
- 音频输入必须为连续 PCM 流，不可分段重传；丢包或乱序将导致 ASR 质量下降  
- 不支持跨 session 复用 `voice_id`，每次新会话需重新声明（即使相同 voice_id）  
- 错误码 `429 too many requests` 表示并发连接数超限（默认配额：5 个并发连接/项目）  
- 所有事件格式、状态机流转及重连策略均严格遵循 [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md) 定义

## 来源文档

- [实时多模态](../../raw/model-api-reference/omni-realtime-api.md)


