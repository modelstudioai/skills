# omni realtime api

omni realtime api 是百炼平台提供的低延迟、流式[多模态](../concepts/multimodal.md)实时交互接口，支持语音输入/输出、文本流式响应与实时音色克隆能力。该 API 采用 WebSocket 协议，适用于智能客服、实时会议助手、虚拟人对话等对端到端延迟敏感的场景。详细协议规范与事件语义见 [实时多模态](../../raw/model-api-reference/omni-realtime-api.md)。

## 支持的模型与功能

- 当前仅支持 `qwen-omni-realtime` 模型（v1.0+），不兼容旧版 `qwen-audio` 或 `qwen-vl` 系列。
- 核心功能包括：实时语音识别（ASR）、流式大语言模型推理（LLM）、语音合成（TTS）及可选的声音复刻（Voice Cloning）——后者需提前上传参考音频并获取 voice_id，具体流程参见 [声音复刻](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。
- 所有交互基于双向流式 WebSocket 连接，客户端与服务端通过结构化事件通信，事件定义详见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 和 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 固定为 `"qwen-omni-realtime"` |
| `voice_id` | string | 否 | 声音复刻 ID；若未提供，则使用默认 TTS 声音。需确保该 ID 已通过 [声音复刻](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md) 流程注册成功 |
| `input_format` / `output_format` | string | 否 | 音频编码格式，支持 `"pcm16"`（默认）、`"wav"`；注意 [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md) 明确要求客户端发送 PCM 小端 16bit 数据 |
| `enable_interim_results` | boolean | 否 | 是否启用 ASR 中间结果（默认 `false`）；设为 `true` 时服务端将推送部分识别文本 |

> **注意**：原始文档中 [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md) 描述的 `sample_rate` 默认值为 16000 Hz，但 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 示例代码中硬编码为 24000 Hz。实际调用必须显式指定 `sample_rate: 16000`，否则连接将被拒绝。

## 使用方式

1. 建立 WebSocket 连接：`wss://dashscope.aliyuncs.com/realtime/qwen-omni-realtime/v1?api_key=<YOUR_API_KEY>`  
2. 发送 `session.update` 事件初始化会话（含 `model`, `voice_id` 等配置）  
3. 持续发送 `input.audio` 二进制帧（PCM16，16kHz，单声道）  
4. 接收 `output.text.delta`、`output.audio.delta` 等流式事件  
SDK 封装已简化上述流程，推荐直接使用官方 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 或 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)。

## 限制和注意事项

- 单次会话最长 180 秒，超时后连接自动关闭；如需长会话，请在 `session.update` 中设置 `max_duration: 180` 并主动重连。
- 音频输入必须严格为 16kHz 采样率、16-bit PCM、单声道；任意偏差将导致 ASR 失败或静音。
- `voice_id` 仅对同一阿里云账号下创建的克隆音色有效，跨账号或过期 ID 将返回 `400 Bad Request`。
- 不支持 HTTP 轮询或 SSE；所有交互必须基于 WebSocket 双向流。

## 来源文档

- [实时多模态](../../raw/model-api-reference/omni-realtime-api.md)


