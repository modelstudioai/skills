# omni realtime api

Qwen-Omni-Realtime API 是面向实时多模态交互（语音+文本）的流式 WebSocket 接口，支持低延迟语音识别、大模型推理与 TTS 合成一体化处理。它采用事件驱动架构，通过客户端事件（如 `session.update`）配置会话行为，服务端以结构化 JSON 事件（如 `session.created`、`conversation.item.created`）实时反馈状态与内容。该 API 适用于智能客服、语音助手等需自然对话体验的场景。

## 支持的模型/功能

- **核心模型**：`qwen3.8-omni-flash-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3.5-omni-plus-realtime`、`qwen3-omni-flash-realtime`、`qwen-omni-turbo-realtime`；各模型在参数支持、VAD 类型、工具调用能力上存在差异（详见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)）。
- **多模态输出**：默认支持 `["text", "audio"]`，可选仅 `["text"]`；音频 I/O 格式支持 `pcm`（默认）和 `wav`，采样率按模型不同支持 8k/16k/24k/48k Hz。
- **语音活动检测（VAD）**：支持 `server_vad`（声学特征）和 `semantic_vad`（语义有效性），后者仅限 Qwen3.8-Omni-Flash-Realtime 和 Qwen3.5-Omni-Realtime 系列模型。
- **扩展能力**：
  - Function Calling（`tools` 数组中 `type="function"`）
  - MCP（`tools` 数组中 `type="mcp"`），支持工具发现与调用
  - 联网搜索（`enable_search: true`），但与 `tools` 互斥
  - 输入音频转录（`input_audio_transcription`，固定模型 `qwen3-asr-flash-realtime`）

> **注意**：文档 2 中 `session.created` 示例显示 `"output_audio_format": "pcm"` 且注明“当前不支持自定义输出采样率”，而文档 1 明确允许 `session.audio.output.format.sample_rate` 设为 24000（默认）或 8000/16000/48000。实际以 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 的配置能力为准，服务端事件中的回显字段可能滞后或简化。

## 关键参数

所有参数均通过 `session.update` 事件的 `session` 对象传递，关键字段包括：

- `model`: 指定模型 ID（如 `"qwen3.5-omni-flash-realtime"`），必须与接入协议匹配。
- `modalities`: 输出模态数组，仅支持 `["text"]` 或 `["text","audio"]`。
- `voice` / `audio.output.voice`: 音色标识符（如 `"Tina"`），新接入推荐使用嵌套路径 `audio.output.voice`。
- `audio.input.format` / `audio.output.format`: 控制输入/输出音频格式与采样率；多通道输入（2/4 声道）仅支持 `pcm` + `16000` Hz + `s16le` + `interleaved` 组合。
- `turn_detection`: VAD 配置对象，含 `type`、`threshold`（[-1.0, 1.0]）、`silence_duration_ms`（[200, 6000]）；`idle_timeout_ms` 仅对 `qwen3.5-omni-plus-realtime`/`flash-realtime` + `server_vad` 生效。
- `instructions`: 系统角色提示词，影响模型响应风格。
- `tools`: 工具列表，Function Calling 与 MCP 可共存于同一数组（Qwen3.8-Omni-Flash-Realtime），但 `tools` 与 `enable_search` 不可同时启用。
- 生成控制参数：`temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed`；其中 `qwen-omni-turbo` 系列模型**不支持修改**多数参数（见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 详细说明）。

## 使用方式

1. **建立连接**：通过 WebSocket（推荐）、AOQ 或 WebRTC 连接到对应模型的 endpoint（接入方式详见 [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)）。
2. **初始化会话**：连接后立即发送 `session.update` 事件配置 `session` 对象；服务端校验成功后返回 `session.created`（首次）或 `session.updated`（后续更新）。
3. **音频输入**：
   - 在 `IDLE` 或 `INPUT_AUDIO_BUFFERING` 状态下，按配置格式（如 PCM 16kHz）分块发送二进制音频数据；
   - 若启用 VAD，服务端自动触发 `input_audio_buffer.speech_started` / `.speech_stopped` / `.committed` 事件；
   - 手动模式下需显式发送 `input_audio_buffer.commit`。
4. **接收响应**：服务端持续推送事件，包括 `conversation.item.created`（含文本/音频/工具调用内容）、`response.audio.delta`（TTS 流式音频片段）、`error`（异常）等。
5. **工具交互**：当 `conversation.item.created` 返回 `type="function_call"` 或 `type="mcp_call"` 时，客户端需执行对应逻辑并发送 `conversation.item.input_audio` 或 `conversation.item.input_text` 回传结果。

## 限制和注意事项

- **Token 限制**：单次 `session.update` 的 `session` 对象总 Token 数上限为 196608；`max_tokens` 仅控制响应截断，不影响生成过程。
- **兼容性约束**：
  - `qwen-omni-turbo` 系列模型不支持修改 `temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed`（见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)）。
  - `tools` 与 `enable_search` 互斥，不可同时设为 `true`。
- **音频配置时机**：`audio.input.format` 必须在首段音频发送前完成配置；`audio.output.format` 应在会话初期、音频交互开始前设置。
- **MCP 安全要求**：`server_url` 必须为公网 HTTPS 443 地址，`authorization` 和 `headers` 不在 `session.updated` 中回显，客户端不得依赖其重建敏感配置。
- **错误处理**：服务端错误统一通过 `error` 事件返回，含 `type`、`code`、`message` 和 `param`（如 `"session.modalities"`），需据此定位问题（参考 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)）。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)


