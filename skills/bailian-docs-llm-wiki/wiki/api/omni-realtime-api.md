# omni realtime api

Qwen-Omni-Realtime API 是面向多模态实时语音交互场景的 WebSocket/QUIC/WebRTC 接口，支持文本与音频同步生成、端到端低延迟语音活动检测（VAD）、工具调用（Function Calling / MCP）及可配置的语音合成输出。其核心设计围绕会话生命周期管理，通过 `session.update` 初始化或动态调整模型行为，并基于事件流（如 `input_audio_buffer.speech_started`、`conversation.item.created`）实现双向实时响应。

## 支持的模型与功能

- **当前支持模型**：`qwen3.8-omni-flash-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3.5-omni-plus-realtime`、`qwen3-omni-flash-realtime`、`qwen-omni-turbo-realtime`；各模型在参数可调性、模态组合、VAD 类型和工具能力上存在差异（详见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)）。
- **核心功能**：
  - 多模态输出：支持 `["text"]` 或 `["text", "audio"]`（默认），部分模型支持视频输入（仅 `qwen3.8-omni-flash-realtime`）。
  - 音频 I/O 灵活配置：输入支持单/双/四通道 PCM（16 kHz），输出支持 `pcm`/`wav` 及多档采样率（8k–48k Hz）。
  - 语音活动检测（VAD）：`server_vad`（声学）与 `semantic_vad`（语义）双模式，后者仅限 `qwen3.8-omni-flash-realtime` 和 `qwen3.5-omni-realtime` 系列。
  - 工具调用：Function Calling（`type=function`）与 MCP（`type=mcp`）并存，但 **`tools` 与 `enable_search` 不可同时启用**。
  - 联网搜索：`enable_search: true` 仅对 `qwen3.8-omni-flash-realtime` 和 `qwen3.5-omni-realtime` 系列有效，启用后模型自主决策是否触发搜索。

> **注意**：文档 2 中 `session.created` 示例显示 `output_audio_format` 固定为 `"pcm"` 且“不支持自定义输出采样率”，但文档 1 明确允许 `session.audio.output.format.sample_rate` 设置为 8000/16000/24000/48000 Hz。以 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 为准，服务端实际支持输出采样率配置，文档 2 的描述已过时。

## 关键参数

所有参数均在 `session.update` 的 `session` 对象中设置，部分参数模型间默认值或可调性不同：

| 参数 | 说明 | 典型取值/范围 | 模型兼容性备注 |
|------|------|----------------|----------------|
| `model` | 模型标识符 | `qwen3.5-omni-flash-realtime` 等 | 必填，会话建立后不可变更 |
| `modalities` | 输出模态 | `["text"]`, `["text","audio"]` | `["audio"]` 单独不支持 |
| `voice` / `audio.output.voice` | 合成音色 | `Tina`, `Cherry`, `longanlingxin` 等 | 新接入推荐使用 `audio.output.voice`，若两者共存则后者优先 |
| `audio.input.format` | 输入格式与采样率 | `{ "type": "pcm", "sample_rate": 16000 }` | Qwen3.8 多通道强制 `pcm`+`16000`+`s16le`+`interleaved` |
| `turn_detection` | VAD 配置 | `{ "type": "semantic_vad", "threshold": 0.3, "silence_duration_ms": 600 }` | `idle_timeout_ms` 仅在 `qwen3.5-omni-*` + `server_vad` 下生效 |
| `temperature` / `top_p` / `top_k` | 生成多样性控制 | `temperature: 0.6–1.0`, `top_p: 0.8–0.95`, `top_k: 20–50` | `qwen-omni-turbo` 系列**不支持修改**任何采样参数 |
| `max_tokens` | 响应最大 Token 数 | `1–65536`（`qwen3.8`）；其他模型上限为模型最大输出长度 | 截断响应，不影响生成过程 |
| `repetition_penalty` / `presence_penalty` | 重复抑制 | `repetition_penalty: 0–1.05`, `presence_penalty: -2.0–2.0` | `qwen3.8` 支持 `repetition_penalty: 0`；`qwen-omni-turbo` 不支持修改 |
| `seed` | 生成确定性种子 | `0–2^31-1`，默认 `-1` | `qwen-omni-turbo` 不支持修改 |

## 使用方式

1. **建立连接**：选择 AOQ、WebSocket 或 WebRTC 协议接入，具体地址与握手流程见 [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)。
2. **初始化会话**：连接成功后，立即发送 `session.update` 事件配置 `session`（含 `model`, `modalities`, `voice`, `audio`, `instructions` 等）。服务端校验通过后返回 `session.updated`，失败则返回 `error`。
3. **音频输入**：
   - 在 `IDLE` 状态下配置 `audio.input.format`（推荐）；
   - 持续发送 `input_audio_buffer.append` 二进制音频帧；
   - VAD 自动触发 `input_audio_buffer.speech_started` → `input_audio_buffer.speech_stopped` → `input_audio_buffer.committed`；手动模式需显式发送 `input_audio_buffer.commit`。
4. **接收响应**：
   - 文本流：`conversation.item.created` 中 `item.type="message"` 的 `content` 字段；
   - 音频流：`conversation.item.created` 中 `item.type="message"` 的 `content` 包含 `{"type":"output_audio","audio":"<base64>"}`；
   - 工具调用：`item.type="function_call"` 或 `item.type="mcp_call"`，需按规范返回 `conversation.item.input_audio_transcription.completed` 或 `conversation.item.mcp_call_output`。
5. **SDK 辅助**：Python/Java SDK 封装了连接、事件序列化与重连逻辑，降低接入复杂度（参见 [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)）。

## 限制和注意事项

- **Token 限制**：单次 `session.update` 总输入 Token ≤ 196608；多通道音频（2/4 声道）输入 Token 数为单声道的 2 倍；详细计算规则见 [Token 计算](https://help.aliyun.com/zh/model-studio/realtime#cfba3898e4d0h)。
- **参数互斥**：`tools` 与 `enable_search` 不可同时设为 `true`；`temperature` 与 `top_p` 建议只设置其一。
- **音色与格式兼容性**：`qwen3.8-omni-flash-realtime` 默认 `voice="Tina"`，`qwen3-omni-flash-realtime` 默认 `voice="Cherry"`；输出格式 `wav` 仅影响容器封装，音频内容与 `pcm` 一致。
- **MCP 安全约束**：`server_url` 必须为公网 HTTPS 443 地址，`authorization` 和 `headers` 不在 `session.updated` 中回显，客户端不得依赖该事件重建敏感配置。
- **错误处理**：所有错误通过 `error` 事件返回，含 `code`（如 `invalid_value`）与 `param`（如 `session.modalities`），需根据 `param` 定位问题字段（参见 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)）。
- **静默超时**：`idle_timeout_ms` 仅在 `qwen3.5-omni-*` 模型且 `turn_detection.type="server_vad"` 时生效，范围 `[5000, 30000]` ms。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)


