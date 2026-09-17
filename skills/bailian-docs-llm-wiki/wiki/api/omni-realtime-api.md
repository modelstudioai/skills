# omni realtime api

Qwen-Omni-Realtime API 是基于 WebSocket 的实时[多模态](../concepts/multi-modal.md)交互接口，支持语音输入/输出、文本生成、图像理解及工具调用等能力。它采用事件驱动模型，客户端通过发送标准化事件（如 `session.update`、`input_audio_buffer.append`）控制会话状态与数据流，服务端通过异步事件（如 `session.created`、`response.audio.delta`）实时反馈处理结果。该 API 专为低延迟、高保真语音对话场景设计，适用于智能客服、虚拟助手等实时交互应用。

## 支持的模型/功能

- **核心模型**：`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3-omni-flash-realtime`、`qwen-omni-turbo-realtime`。其中 `qwen3.5-omni-realtime` 系列（文档中未明确列出但上下文隐含）支持 `semantic_vad` 和 `enable_search`；`qwen-omni-turbo-realtime` 系列不支持修改多数采样参数（如 `temperature`、`top_p`、`max_tokens` 等）[原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **[多模态](../concepts/multi-modal.md)输出**：支持 `["text"]`（纯文本）或 `["text", "audio"]`（文本+音频）组合，`audio` 输出默认为 `wav` 格式、24 kHz 采样率 [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **语音活动检测（VAD）**：提供 `server_vad`（声学特征）和 `semantic_vad`（语义有效性）两种模式，后者仅 `qwen3.5-omni-realtime` 系列支持 [原文标题](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **扩展能力**：
  - 工具调用（`tools`）：支持定义 `function` 类型工具，模型自主触发并返回参数。
  - 联网搜索（`enable_search`）：仅 `qwen3.5-omni-realtime` 系列支持，且与 `tools` 不兼容。
  - 声音复刻：需先调用独立的 `qwen-voice-enrollment` 模型创建音色，再在 `session.update` 中通过 `voice` 参数指定使用，**驱动模型必须与复刻时指定的 `target_model` 严格一致** [原文标题](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。

> **注意**：文档 2（服务端事件）声称 `output_audio_format` 当前“仅支持设为 `pcm`”，而文档 1（客户端事件）和 SDK 文档（文档 3/4）均明确支持 `wav` 格式配置（如示例中 `"type": "wav"`）。此为矛盾信息，以客户端事件和 SDK 文档为准，服务端实际支持 `wav` 输出。

## 关键参数

所有参数均通过 `session.update` 事件或 SDK 的 `update_session` 方法配置：

- **基础配置**：
  - `modalities`: 输出模态数组，如 `["text", "audio"]`。
  - `voice`: 音色名称，不同模型有默认值（`Tina`/`Cherry`/`Chelsie`），亦可传入声音复刻生成的自定义 `voice` ID。
  - `instructions`: 系统角色指令，用于设定模型行为边界。

- **音频配置**（推荐使用嵌套结构）：
  - `audio.input.format.type` / `sample_rate`: 输入格式（`pcm` 或 `wav`）与采样率（`8000`/`16000`/`24000`/`48000` Hz）。
  - `audio.output.format.type` / `sample_rate`: 输出格式与采样率（默认 `wav`/`24000`）。
  - `smooth_output`: 仅 `qwen3-omni-flash-realtime` 系列有效，控制口语化（`true`）或书面化（`false`）风格。

- **VAD 参数**：
  - `turn_detection.type`: `server_vad`（默认）或 `semantic_vad`。
  - `turn_detection.threshold`: VAD 灵敏度（`-1.0` 到 `1.0`），默认 `0.5`。
  - `turn_detection.silence_duration_ms`: 静音超时（`200`–`6000` ms），默认 `800`。
  - `idle_timeout_ms`: 静默超时（`5000`–`30000` ms），仅 `qwen3.5-omni-plus-realtime`/`flash-realtime` + `server_vad` 时生效。

- **生成控制参数**（部分模型受限）：
  - `temperature` / `top_p` / `top_k`: 控制多样性，建议只设其一。`qwen-omni-turbo` 系列不可修改。
  - `max_tokens`: 最大输出 [Token](../concepts/token.md) 数，超长将被截断。
  - `repetition_penalty` / `presence_penalty` / `seed`: 分别控制重复惩罚、全局重复度与确定性。

## 使用方式

1. **建立连接**：使用 WebSocket URL（如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`）连接，**强烈推荐迁移至业务空间专属域名**以获得更高稳定性 [原文标题](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)。
2. **初始化会话**：连接后，服务端立即返回 `session.created` 事件；随后客户端应调用 `session.update` 配置参数（如 `modalities`, `voice`, `turn_detection`）。
3. **数据输入**：
   - **VAD 模式**（默认）：持续发送 `input_audio_buffer.append`，服务端自动检测起止并提交（`input_audio_buffer.committed`），无需手动 `commit`。
   - **Manual 模式**：发送 `input_audio_buffer.append` 后，必须显式发送 `input_audio_buffer.commit` 创建用户消息项。
   - 图像输入：通过 `input_image_buffer.append` 发送 Base64 编码的 JPG/JPEG（≤256KB，建议 480p/720p）。
4. **触发响应**：
   - VAD 模式：服务端自动触发，无需客户端事件。
   - Manual 模式：发送 `response.create` 显式请求。
5. **工具调用处理**：当收到 `response.function_call_arguments.done` 事件时，执行本地工具，再通过 `conversation.item.create` 回传结果，并在 Manual 模式下再次发送 `response.create`。
6. **流式消费**：监听 `response.audio.delta`（音频）、`response.text.delta`（文本）、`response.audio_transcript.delta`（ASR 实时转录）等事件进行增量渲染。

## 限制和注意事项

- **音频限制**：输入音频建议 `16000` Hz PCM/WAV；单次 `append` 数据无硬上限，但缓冲区总大小受服务端约束（SDK 文档提及 `15 MiB` 上限）。
- **图像限制**：仅支持 JPG/JPEG，Base64 编码后 ≤256KB，建议分辨率 480p/720p，发送频率 ≤1 张/秒。
- **参数互斥**：`tools` 与 `enable_search` 不可同时启用。
- **模型兼容性**：
  - `semantic_vad`、`enable_search` 仅 `qwen3.5-omni-realtime` 系列支持。
  - `smooth_output` 仅 `qwen3-omni-flash-realtime` 系列支持。
  - `qwen-omni-turbo-realtime` 系列不支持修改 `temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed`。
- **声音复刻关键约束**：复刻时指定的 `target_model` 必须与 Omni 对话时使用的 `model` 完全一致，否则合成失败 [原文标题](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。
- **错误处理**：服务端返回 `error` 事件（如 `invalid_request_error`），需检查 `error.param` 字段定位问题（如 `session.modalities` 配置错误）。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)


