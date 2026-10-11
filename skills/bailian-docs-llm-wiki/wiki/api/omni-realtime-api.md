# omni realtime api

Qwen-Omni-Realtime 是面向实时多模态交互（语音+文本+视频）的低延迟流式 API，支持 WebSocket、WebRTC 和 AOQ 三种传输协议。它提供端到端的语音识别（ASR）、大模型推理、语音合成（TTS）及工具调用能力，适用于智能客服、虚拟助手等强实时性场景。所有交互基于事件驱动模型，客户端通过发送标准事件（如 `session.update`、`response.create`）控制会话行为，服务端通过结构化事件（如 `session.created`、`input_audio_buffer.speech_stopped`）反馈状态与结果。

## 支持的模型/功能

当前支持以下模型：
- `qwen3.8-omni-flash-realtime`
- `qwen3.5-omni-plus-realtime`
- `qwen3.5-omni-flash-realtime`
- `qwen3-omni-flash-realtime-2025-09-15`（实验性）

核心功能包括：
- **多模态 I/O**：支持 `["text"]` 或 `["text", "audio"]` 输出；音频输入支持单/双/四通道 PCM（需显式配置 `channels`、`channel_layout` 等字段）；视频输入支持表征聚合（`representation_compact`）以降低 Token 开销。
- **语音活动检测（VAD）**：支持 `server_vad`（声学）和 `semantic_vad`（语义）两种模式，后者可过滤背景音与回应语。
- **工具调用**：支持 Function Calling（`type=function`）和 MCP（`type=mcp`），但二者与 `enable_search` 互斥，不可同时启用。
- **联网搜索**：仅 `qwen3.8-omni-flash-realtime` 和 `qwen3.5-omni-realtime` 系列支持，启用后模型可自主触发搜索。

> **注意**：文档 3 中 `session.created` 示例显示 `output_audio_format` 固定为 `"pcm"` 且“不支持自定义输出采样率”，但文档 2 明确说明 `qwen3.5-omni-plus-realtime` 等模型支持 `output.audio.format.sample_rate` 设为 8000/16000/24000/48000 Hz（默认 24000）。该矛盾以 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 为准，服务端实际支持动态配置。

## 关键参数

所有参数均在 `session.update` 事件的 `session` 对象中设置：

- **基础配置**  
  `modalities`: 必须为 `["text"]` 或 `["text","audio"]`（`["audio"]` 单独不支持）；  
  `model`: 指定模型 ID，如 `"qwen3.5-omni-flash-realtime"`；  
  `voice`: 音色名（如 `"Tina"`），新接入推荐使用 `session.audio.output.voice` 而非顶层 `voice` 字段。

- **音频配置**  
  `audio.input.format`: `type`（`pcm`/`wav`）和 `sample_rate`（16000 Hz 为通用默认值）；多通道输入必须为 `pcm` + `16000` + `s16le` + `interleaved`；  
  `audio.output.format`: 同上，支持 `wav` 封装（便于直接播放）；  
  `input_audio_transcription`: 设为 `{"model":"qwen3-asr-flash-realtime"}` 启用转录。

- **VAD 与超时**  
  `turn_detection.type`: `"server_vad"`（默认）或 `"semantic_vad"`；  
  `turn_detection.silence_duration_ms`: 默认 800 ms，范围 [200, 6000]；  
  `idle_timeout_ms`: 仅 `qwen3.5-omni-*` 在 `server_vad` 模式下生效，范围 [5000, 30000]。

- **生成控制**  
  `temperature` / `top_p`: 二选一控制多样性（避免同时设置）；  
  `max_tokens`: 最大输出 Token 数，超限将截断（不影响生成过程）；  
  `repetition_penalty`: `qwen3.8-omni-flash-realtime` 支持设为 `0`（禁用惩罚），其他模型需 >0；  
  `seed`: 用于结果复现，默认 `-1`（随机）。

- **高级功能**  
  `tools`: Function Calling 或 MCP 工具数组；MCP 配置中 `server_url` 必须为公网 HTTPS 443 地址，且 `authorization`/`headers` 不在 `session.updated` 中回显；  
  `enable_search`: 布尔值，启用后自动判断是否搜索；  
  `smooth_output`: 仅 `qwen3-omni-flash-realtime-2025-09-15` 支持，控制口语化/书面化风格。

详细字段定义与示例见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 和 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)。

## 使用方式

1. **建立连接**：选择 WebSocket、WebRTC 或 AOQ 协议接入。WebSocket 是最常用方式，连接地址与握手流程详见 [WebSocket 接入指南](../../raw/_short/omni-realtime-interaction-process-c1786114b7f9b9c5.md)。  
2. **初始化会话**：连接成功后，服务端立即返回 `session.created` 事件，包含默认配置。  
3. **更新配置**：发送 `session.update` 事件定制会话（如设置 `modalities`、`voice`、`tools`）。服务端校验通过后返回 `session.updated`，失败则返回 `error`。  
4. **输入数据**：  
   - 音频：分块发送 `input_audio_buffer.append`，VAD 自动触发 `speech_started`/`speech_stopped`；  
   - 文本：通过 `conversation.item.create` 发送 `message` 类型项。  
5. **触发响应**：VAD 检测结束或手动发送 `response.create` 后，服务端开始流式返回 `conversation.item.created`（含 `message` 或 `function_call`）、`response.audio.delta` 等事件。  
6. **工具调用处理**：收到 `function_call` 后，客户端执行本地函数并调用 `conversation.item.create` 回传结果，再发 `response.create` 续答；MCP 调用需处理 `mcp_approval_request` 等事件。  

SDK 支持 Python 和 Java，具体用法参考 [Python SDK](../../raw/_short/omni-realtime-python-sdk-c6ee137356d19420.md) 和 [Java SDK](../../raw/_short/omni-realtime-java-sdk-80f4b2a483df02c3.md)。

## 限制和注意事项

- **Token 限制**：`qwen3.8-omni-flash-realtime` 的 `session.update` 输入总 Token 上限为 196608；`max_tokens` 输出上限为 65536；各模型最大输出长度参见 [模型列表](../../raw/model-user-guide/get-started-with-models/models.md)。  
- **协议约束**：  
  - WebRTC 仅支持音频流，不支持文本/视频；  
  - AOQ 为 QUIC 协议优化，适合高丢包网络，但需客户端支持 QUIC 栈。  
- **兼容性警告**：  
  - `input_audio_format`/`output_audio_format` 是历史字段，新增接入必须使用嵌套的 `audio.input.format`/`audio.output.format`；  
  - `session.voice` 与 `session.audio.output.voice` 同时存在时，以后者为准；  
  - `qwen3.8-omni-flash-realtime` 的多通道输入强制要求 `channels`、`sample_format` 等字段符合严格约束，省略即用默认值，但显式提供时必须匹配类型与取值范围。  
- **安全限制**：MCP 的 `server_url` 不得含敏感信息（如用户名、密码），`headers` 禁止使用 `host`、`authorization` 等保留头；`tools` 与 `enable_search` 不能共存，否则返回 `invalid_request_error`。  
- **错误处理**：所有错误均通过 `error` 事件返回，含 `code`（如 `invalid_value`）和 `param`（如 `session.modalities`），需根据 `param` 定位问题字段。完整错误码见 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)。

## 来源文档

- [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)
- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)


