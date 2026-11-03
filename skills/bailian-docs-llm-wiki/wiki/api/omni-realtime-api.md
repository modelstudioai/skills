# omni realtime api

Qwen-Omni-Realtime API 是面向[多模态](../concepts/multi-modal.md)实时交互场景的流式 WebSocket 接口，支持语音、文本、图像（Qwen3.8+）、视频（Qwen3.8+）输入与文本/音频同步输出。它采用事件驱动模型，通过客户端事件触发会话配置、音频输入、响应生成等操作，服务端以结构化事件流返回状态、内容和工具调用结果。该 API 适用于智能客服、语音助手、实时会议摘要等低延迟交互场景。

## 支持的模型与功能

当前支持以下核心模型（按发布顺序）：
- `qwen3.5-omni-flash-realtime` 和 `qwen3.5-omni-plus-realtime`：基础[多模态](../concepts/multi-modal.md)实时模型，支持文本+音频双模态输入/输出，提供 `server_vad` 和 `semantic_vad` 两种语音活动检测模式。
- `qwen3.8-omni-flash-realtime`：增强版模型，**新增视频输入支持**（需配置 `session.video.input.representation_compact`），支持 **MCP（Model Control Protocol）工具集成**、多通道空间音频（2/4 声道）、`semantic_vad_ec` 场景优化 VAD，并统一 `audio.input.format` 等嵌套配置结构。详见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- `qwen3-omni-flash-realtime-2025-09-15`：预发布模型，启用 `smooth_output` 控制口语化/书面化风格，并调整默认采样参数（`temperature=0.9`, `top_p=1.0`, `top_k=50`）。

> **注意**：文档 2 中 `session.created` 示例声明“当前不支持自定义输出采样率”，但文档 1 明确允许在 `session.audio.output.format.sample_rate` 中设置 `8000/16000/24000/48000`（对 Qwen3.5 系列）或 `24000`（Qwen3.8 默认），且 `session.updated` 事件会回显该值。实际能力以 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 为准。

功能覆盖：
- [多模态](../concepts/multi-modal.md)输入：PCM/WAV 音频、Base64 图像、H.264 视频（Qwen3.8+）
- 多模态输出：流式文本（`text.delta`）、流式音频（`audio.delta`）、完整音频片段（`audio.done`）
- 智能交互：语音活动检测（VAD）、自动打断、静默超时引导（`idle_timeout_ms`）、输入音频转录（ASR）
- 扩展能力：Function Calling、MCP 工具集成、联网搜索（`enable_search`，与 `tools` 互斥）

## 关键参数

所有参数均通过 `session.update` 事件的 `session` 对象传递，部分参数也出现在 `session.created` / `session.updated` 服务端事件中：

| 参数 | 类型 | 说明 | 默认值（按模型） |
|------|------|------|------------------|
| `modalities` | `["text"]` \| `["text","audio"]` | 输出模态组合，**不支持仅 `["audio"]`** | `["text","audio"]` |
| `voice` / `audio.output.voice` | `string` | 音色标识，新接入**必须使用 `audio.output.voice`**；`session.voice` 为兼容字段 | `Tina`（Qwen3.5/Qwen3.8），`Cherry`（`2025-09-15`） |
| `audio.input.format.type` & `.sample_rate` | `string`, `integer` | 输入格式（`pcm`/`wav`）与采样率（Qwen3.5: 8k/16k/24k/48k；Qwen3.8: 仅 16k） | `pcm`, `16000` |
| `audio.output.format.type` & `.sample_rate` | `string`, `integer` | 输出格式与采样率（Qwen3.5: 8k/16k/24k/48k；Qwen3.8: 24k） | `pcm`, `24000`（Qwen3.5），`wav`, `24000`（Qwen3.8 示例） |
| `turn_detection.type` | `server_vad` \| `semantic_vad` \| `semantic_vad_ec` | VAD 类型；`semantic_vad_ec` **仅 Qwen3.8+ 支持** | `server_vad` |
| `enable_search` | `boolean` | 启用联网搜索（自动触发） | `false` |
| `tools` | `array` | Function Calling 或 MCP 工具定义；**与 `enable_search` 不可共存** | `[]` |
| `temperature` / `top_p` / `top_k` | `float`, `float`, `integer` | 采样控制参数；**建议只设其一** | 见文档 1 表格（如 Qwen3.8: `0.6`, `0.95`, `20`） |
| `max_tokens` | `integer` | 响应最大 [Token](../concepts/token.md) 数（截断，非硬限） | Qwen3.8: `[1,65536]`；其他模型见[模型列表](raw/model-user-guide/get-started-with-models/models.md) |

> **注意**：`input_audio_transcription.model` 固定为 `"qwen3-asr-flash-realtime"`，不可修改；`input_audio_format` / `output_audio_format` 为历史兼容字段，新接入应使用 `audio.input.format` / `audio.output.format` 嵌套结构，详见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。

## 使用方式

1. **建立连接**：通过 WebSocket 连接到指定地域的 Realtime API 入口（支持 AOQ/WebRTC/WebSocket，详见 [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)）。
2. **初始化会话**：连接后服务端立即返回 `session.created` 事件，含默认配置；客户端可立即发送 `session.update` 覆盖默认值。
3. **输入数据**：
   - 音频：分块发送 `input_audio_buffer.append`（Base64 PCM/WAV），VAD 模式下由服务端自动 `commit`；Manual 模式需显式发送 `input_audio_buffer.commit`。
   - 图像/视频：使用对应 `append` 事件（文档未展开，参见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 中 `video.input` 部分）。
4. **触发响应**：VAD 模式下语音停止后自动开始；手动模式或工具回调后，需发送 `response.create`。
5. **处理响应**：监听 `conversation.item.created`（新建消息项）、`response.content_part.added`（流式内容）、`response.done`（响应结束）等事件。
6. **管理工具**：Function Calling 返回 `function_call` 项后，客户端执行并用 `conversation.item.create` 提交结果，再发 `response.create`；MCP 工具由服务端执行，需等待 `response.done` 后再发 `response.create` 续答。

## 限制和注意事项

- **[Token](../concepts/token.md) 限制**：Qwen3.8-Omni-Flash-Realtime 单次会话总输入 [Token](../concepts/token.md) 上限为 **196608**；多通道音频（2/4 声道）输入 Token 数为单声道的 2 倍；视频 `representation_compact=normal` 可降至 `none` 模式的 1/4 [Token 计算](https://help.aliyun.com/zh/model-studio/realtime#cfba3898e4d0h)。
- **协议与兼容性**：`qwen3.5-omni-plus-realtime` 和 `qwen3.5-omni-flash-realtime` **不支持 `semantic_vad_ec` 和视频输入**；`qwen3-omni-flash-realtime-2025-09-15` 的 `smooth_output` 参数在旧模型上无效。
- **工具冲突**：`tools` 与 `enable_search` **严格互斥**，同时设置将导致 `error` 事件。
- **音频配置约束**：Qwen3.8 多通道输入**强制要求** `format.type=pcm`, `sample_rate=16000`, `sample_format=s16le`, `packing=interleaved`；省略字段则使用默认值，但显式提供时必须完全匹配。
- **错误处理**：所有客户端事件失败均返回 `error` 事件，含 `type`、`code`、`message` 和 `param`（如 `"session.modalities"`），需据此定位问题。详细错误码见 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)


