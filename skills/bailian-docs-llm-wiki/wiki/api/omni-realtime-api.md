# omni realtime api

Qwen-Omni-Realtime API 是基于 WebSocket 的实时多模态交互接口，支持语音输入、文本/音频输出、实时转录、VAD 检测、工具调用与联网搜索等能力。它面向低延迟对话场景设计，适用于智能客服、语音助手、音视频交互等应用。协议采用事件驱动模型，客户端通过发送标准事件（如 `session.update`、`input_audio_buffer.append`）控制会话状态，服务端通过异步事件流（如 `session.created`、`response.audio.delta`）实时反馈。

## 支持的模型/功能

- **核心模型**：`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3-omni-flash-realtime`、`qwen-omni-turbo-realtime`；其中 `qwen3.5-omni-realtime` 系列（含 `plus` 和 `flash`）是当前功能最全的版本，支持 `semantic_vad`、`enable_search` 和完整工具调用 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **多模态输出**：默认同时返回 `text` 和 `audio`；可配置为仅 `text` 输出以降低带宽消耗。
- **语音活动检测（VAD）**：支持 `server_vad`（声学特征）和 `semantic_vad`（语义有效性）两种模式，后者仅限 `qwen3.5-omni-realtime` 系列模型 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)。
- **声音复刻集成**：支持将自定义音色（通过 `qwen-voice-enrollment` 创建）直接用于 `voice` 参数，但需确保复刻时指定的 `target_model` 与 Omni 实时调用模型严格一致 [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。
- **扩展能力**：
  - 工具调用（`tools`）：模型自主触发[函数调用](../concepts/function-calling.md)，客户端回传结果后生成最终响应；
  - 联网搜索（`enable_search`）：仅 `qwen3.5-omni-realtime` 系列支持，与 `tools` 不兼容；
  - 输入音频实时转录（`enable_input_audio_transcription`），使用固定 ASR 模型 `qwen3-asr-flash-realtime`。

> **注意**：文档 2（服务端事件）中称 `output_audio_format` “当前仅支持设为 `pcm`”，而文档 1（客户端事件）和 SDK 文档（文档 3/4）均明确支持 `wav` 格式及 `8000/16000/24000/48000` 多种采样率。该矛盾以客户端事件文档为准，服务端实际已支持 `wav` 输出。

## 关键参数

所有参数均通过 `session.update` 事件或 SDK 的 `update_session()` 方法配置，按功能分组如下：

| 参数 | 类型 | 说明 | 模型限制 |
|------|------|------|----------|
| `modalities` | `["text"]` 或 `["text","audio"]` | 输出模态，默认 `["text","audio"]` | 全系列支持 |
| `voice` | `string` | 音色名称，如 `"Tina"`（`qwen3.5-omni-plus-realtime` 默认） | 各模型有默认值，见文档 1 |
| `audio.input.format` / `audio.output.format` | `{type: "pcm"\|"wav", sample_rate: 8000\|16000\|24000\|48000}` | 输入/输出音频格式与采样率，推荐在会话初期配置 | `qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime` |
| `instructions` | `string` | 系统角色指令，影响模型行为 | 全系列支持 |
| `turn_detection.type` | `"server_vad"`（默认）或 `"semantic_vad"` | VAD 类型，`semantic_vad` 仅 `qwen3.5-omni-realtime` 支持 | 见文档 1 |
| `turn_detection.silence_duration_ms` | `integer [200, 6000]` | 静音超时阈值，默认 `800` ms | 全系列支持 |
| `idle_timeout_ms` | `integer [5000, 30000]` | 静默超时后主动引导，仅 `server_vad` + `qwen3.5-omni-plus/flash-realtime` 生效 | 见文档 1 |
| `enable_search` | `boolean` | 启用联网搜索，默认 `false` | 仅 `qwen3.5-omni-realtime` 系列支持，且与 `tools` 互斥 |
| `tools` | `array` of `function` objects | 工具定义列表，含 `name`、`description`、`parameters` | 同上 |
| `temperature` / `top_p` / `top_k` | `float` / `float` / `integer` | 采样控制参数，建议二者择一设置 | `qwen-omni-turbo` 系列不支持修改，见文档 1 |
| `max_tokens` | `integer` | 响应最大 token 数，超长则截断 | 同上 |
| `smooth_output` | `boolean` or `null` | 仅 `qwen3-omni-flash-realtime` 支持：`true`（口语化）、`false`（书面化） | 见文档 1 |

## 使用方式

1. **建立连接**：使用 WebSocket 连接到地域专属域名（如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`），[Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 和 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md) 提供封装好的 `connect()` 方法。
2. **初始化会话**：连接后服务端立即返回 `session.created` 事件；随后调用 `update_session()` 发送 `session.update` 事件配置参数（如 `modalities`、`voice`、`turn_detection`）。
3. **输入处理**：
   - **VAD 模式**（推荐）：持续 `append_audio()`，服务端自动检测 `speech_started`/`speech_stopped` 并 `committed`，无需手动提交。
   - **Manual 模式**：`append_audio()` 后必须显式 `commit()` 创建用户消息项，再发 `response.create()` 触发响应。
4. **响应消费**：监听 `response.audio.delta`（流式音频）、`response.text.delta`（流式文本）、`response.audio_transcript.delta`（ASR 中间结果）等事件，按需合成或展示。
5. **工具调用**：当收到 `conversation.item.created` 类型为 `function_call` 时，执行本地工具，再通过 `conversation.item.create` 回传结果，并发送 `response.create` 触发后续响应 [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)。
6. **清理**：调用 `cancel_response()` 中止进行中的响应，`close()` 终止连接。

## 限制和注意事项

- **音频限制**：输入音频格式支持 `pcm`（裸 PCM）和 `wav`（WAV 封装），采样率支持 `8000/16000/24000/48000 Hz`；单次 `append_audio()` 数据量无硬性上限，但缓冲区总大小建议 ≤15 MiB。
- **图像输入**：仅支持 JPG/JPEG，Base64 编码后 ≤256 KB，建议分辨率 480p–720p，发送频率 ≤1 张/秒；需先 `append_audio()` 再 `append_video()`。
- **参数兼容性**：`tools` 与 `enable_search` 不可同时启用；`qwen-omni-turbo` 系列模型不支持修改 `temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed`。
- **错误处理**：服务端返回 `error` 事件（如 `invalid_value`），需检查 `error.param` 字段定位问题（如 `session.modalities` 配置非法）。
- **域名迁移**：强烈建议使用业务空间专属域名（如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)


