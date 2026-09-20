# omni realtime api

Qwen-Omni Realtime API 是一个基于 WebSocket 的流式多模态实时交互接口，支持语音输入、文本与音频混合输出、实时语音转录（ASR）、语音活动检测（VAD）、工具调用（Function Calling）及联网搜索等能力。它面向低延迟、高交互性的语音助手、智能客服等场景，提供端到端的实时对话体验。

## 支持的模型/功能

- **核心模型**：`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3-omni-flash-realtime`、`qwen-omni-turbo-realtime`。各模型在音色默认值、参数可调性、VAD 类型支持等方面存在差异（详见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)）。
- **多模态输出**：支持 `["text"]`（纯文本）或 `["text", "audio"]`（文本+音频）两种模态组合；音频输出格式支持 `pcm` 和 `wav`，采样率支持 `8000`/`16000`/`24000`/`48000` Hz（[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 明确列出适用模型范围）。
- **语音活动检测（VAD）**：提供 `server_vad`（声学特征检测）和 `semantic_vad`（语义有效性检测）两种模式；后者仅 `qwen3.5-omni-realtime` 系列模型支持。
- **工具调用（Function Calling）**：支持定义 `function` 类型工具，模型可自主触发调用；需通过 `conversation.item.create` 回传结果并发送 `response.create` 触发后续响应（[服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md) 中详细描述了 `conversation.item.created` 和 `response.function_call_arguments.*` 事件）。
- **联网搜索**：仅 `qwen3.5-omni-realtime` 系列模型支持 `enable_search`，且与 `tools` 不兼容，不可同时启用。
- **声音复刻集成**：支持将自定义音色（通过 `qwen-voice-enrollment` 创建）用于 Omni 实时对话，但要求复刻时指定的 `target_model` 必须与实时 API 调用的 `model` 完全一致（参见 [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)）。

> **注意**：文档 4（Java SDK）中称 `inputAudioFormat` “当前仅支持设为 `PCM_16000HZ_MONO_16BIT`”，而文档 2（客户端事件）和文档 3（Python SDK）均明确支持 `wav` 格式及多种采样率（如 `8000`/`24000`/`48000` Hz）。该限制属于 Java SDK 的历史兼容性说明，非服务端能力限制，应以 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 为准。

## 关键参数

所有参数均通过 `session.update` 客户端事件或 SDK 的 `update_session` 方法配置，服务端校验后返回 `session.updated` 事件确认。

- **基础配置**：
  - `modalities`: 输出模态数组，必选值为 `["text"]` 或 `["text","audio"]`。
  - `voice`: 音色名称，不同模型有默认值（`Tina`/`Cherry`/`Chelsie`），复刻音色亦在此处传入。
  - `instructions`: 系统角色指令，用于设定模型行为边界。
- **音频配置**：
  - `audio.input.format` / `audio.output.format`: 推荐使用嵌套对象同时指定 `type`（`pcm`/`wav`）和 `sample_rate`（Hz），取代已废弃的 `input_audio_format`/`output_audio_format` 字符串字段。
- **VAD 配置**（`turn_detection`）：
  - `type`: `server_vad`（默认）或 `semantic_vad`（仅 qwen3.5 系列）。
  - `threshold`: [-1.0, 1.0]，值越小越灵敏。
  - `silence_duration_ms`: [200, 6000]，静音超时触发响应。
  - `idle_timeout_ms`: [5000, 30000]，仅 `server_vad` + `qwen3.5-omni-plus/flash-realtime` 有效，用于静默引导。
- **生成控制**：
  - `temperature` / `top_p`: 二选一控制多样性（`qwen-omni-turbo` 系列不支持修改）。
  - `max_tokens`: 响应截断上限，不影响生成过程。
  - `repetition_penalty` / `presence_penalty`: 分别控制连续重复与全局重复。
  - `seed`: 控制确定性，默认 `-1`。
- **高级功能**：
  - `enable_search`: 仅 qwen3.5 系列支持，启用后模型可自主搜索。
  - `tools`: 工具定义列表，每个工具含 `name`、`description`、`parameters`（含 `properties` 和 `required`）。

## 使用方式

1. **建立连接**：使用 WebSocket URL（推荐业务空间专属域名，如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`）发起连接，服务端立即返回 `session.created` 事件。
2. **配置会话**：连接后立即调用 `session.update`（或 SDK `update_session`）设置模型、模态、音色、VAD 等参数；服务端校验成功后返回 `session.updated`。
3. **输入处理**：
   - **VAD 模式**（默认）：持续发送 `input_audio_buffer.append`，服务端自动检测 `speech_started`/`speech_stopped` 并提交缓冲区，无需客户端调用 `commit`。
   - **Manual 模式**：关闭 VAD（`turn_detection: null`），由客户端控制 `append` 后显式发送 `input_audio_buffer.commit` 创建用户消息项。
4. **响应触发**：
   - VAD 模式下，服务端在语音停止后自动触发 `response.create`。
   - Manual 模式下，客户端需在 `commit` 后主动发送 `response.create`。
5. **工具调用处理**：当收到 `response.function_call_arguments.done` 事件时，执行本地工具，再通过 `conversation.item.create` 提交结果，最后发送 `response.create` 获取最终响应。
6. **流式消费**：监听 `response.audio.delta`（音频流）、`response.text.delta`（文本流）、`response.audio_transcript.delta`（ASR 实时预览）等事件，按需渲染。

## 限制和注意事项

- **音频格式与采样率**：输入音频必须为单声道 PCM 或 WAV（16-bit），采样率建议 `16000` Hz；输出音频采样率默认 `24000` Hz，但 `qwen3.5-omni-plus/flash-realtime` 支持自定义（[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 明确说明）。
- **并发与资源**：单次会话中，`input_audio_buffer.append` 单次数据量无硬性上限，但总缓冲区大小受服务端限制；`input_image_buffer.append` 有严格限制（JPG/JPEG、≤256KB Base64、≤1080p、建议 1 张/秒）。
- **功能互斥**：`enable_search` 与 `tools` 不可同时启用，否则服务端返回 `invalid_request_error`。
- **模型兼容性**：`semantic_vad`、`idle_timeout_ms`、`smooth_output`、`search_options` 等高级参数仅对特定模型系列生效，使用前务必核对 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 中的“适用模型”说明。
- **错误处理**：所有客户端事件失败均返回 `error` 事件，需解析 `error.code`（如 `invalid_value`）和 `error.param`（如 `session.modalities`）进行针对性修复（[服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md) 提供完整错误结构示例）。

## 来源文档

- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)


