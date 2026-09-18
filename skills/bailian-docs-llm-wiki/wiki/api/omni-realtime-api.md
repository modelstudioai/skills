# omni realtime api

omni realtime api 是百炼平台提供的低延迟、流式多模态实时交互接口，支持语音输入/输出、文本流式响应与实时音色克隆能力。该 API 采用 WebSocket 协议，适用于智能客服、实时会议助手、语音交互终端等对端到端延迟敏感的场景。其设计强调事件驱动架构，客户端与服务端通过结构化事件双向通信。

## 支持的模型与功能

- 当前仅支持 `qwen-omni-realtime` 模型（v1.0+），不兼容旧版 `qwen-omni` 或 `qwen-audio` 模型。
- 核心功能包括：实时语音识别（ASR）、流式大语言模型推理（LLM）、语音合成（TTS）及可选的声音复刻（Voice Cloning）[实时多模态](../../raw/model-api-reference/omni-realtime-api.md)。
- 声音复刻需提前上传参考音频并生成 voice_id，具体流程见 [声音复刻](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 固定为 `"qwen-omni-realtime"` |
| `voice_id` | string | 否 | 指定复刻音色 ID；若未提供，则使用默认 TTS 声音 |
| `enable_interim_results` | boolean | 否 | 默认 `false`；设为 `true` 时返回 ASR 中间结果（含 `is_final: false` 的事件） |
| `max_response_tokens` | integer | 否 | 最大响应 token 数，范围 32–2048，默认 512 |

> **注意**：`enable_interim_results` 在 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 文档中被标记为“实验性”，生产环境建议保持默认值 `false`，避免因中间结果重置导致下游状态错乱。

## 使用方式

1. 建立 WebSocket 连接，URL 格式为：`wss://dashscope.aliyuncs.com/realtime/v1/omni`（需携带 `Authorization: Bearer <api_key>` 头）；
2. 发送 `session.update` 事件初始化会话（含 `model`、`voice_id` 等配置）；
3. 通过 `input.audio` 事件持续推送 PCM 音频帧（16-bit, 16kHz, 单声道）；
4. 接收服务端事件，如 `output.text.delta`、`output.audio.delta`、`response.done` 等 —— 完整事件定义参见 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)。

SDK 封装推荐：Python 开发者应优先使用 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)，其自动处理帧分片、心跳保活与事件解析；Java 用户参考 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)。

## 限制和注意事项

- 单次会话最长 120 秒，超时后连接自动关闭；
- 音频输入必须为连续 PCM 流，采样率严格限定为 16kHz，不支持 MP3/WAV 封装；
- 不支持跨会话复用 `voice_id`，每个 `voice_id` 仅在创建它的 app_key 下有效；
- 实时交互流程依赖严格时序，客户端须按 [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md) 执行事件顺序，否则可能触发 `session.error`。

## 来源文档

- [实时多模态](../../raw/model-api-reference/omni-realtime-api.md)


