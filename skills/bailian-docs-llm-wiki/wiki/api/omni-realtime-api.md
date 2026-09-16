# omni realtime api

Qwen-Omni Realtime API 是一个基于 WebSocket 的流式多模态实时交互接口，支持语音输入、文本与音频混合输出、实时语音转写、工具调用及联网搜索（部分模型）。其核心设计围绕低延迟、端到端流式响应和灵活的 VAD/Manual 交互模式展开，适用于智能客服、语音助手等实时对话场景。

## 支持的模型/功能

- **主流模型**：`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3-omni-flash-realtime`、`qwen-omni-turbo-realtime`。各模型在音色默认值、参数可调性、VAD 类型支持上存在差异，详见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **多模态输出**：支持 `["text"]`（纯文本）或 `["text", "audio"]`（文本+音频）两种 `modalities` 组合；音频格式当前仅支持 `pcm`（16 kHz 输入 / 24 kHz 输出），但 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 和 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md) 已扩展支持 `wav` 容器封装及自定义采样率（8k/16k/24k/48k）。
- **语音活动检测（VAD）**：提供 `server_vad`（声学特征）和 `semantic_vad`（语义有效性）两种模式；后者仅 `qwen3.5-omni-realtime` 系列支持。
- **高级功能**：
  - 工具调用（Function Calling）：通过 `tools` 参数定义函数，模型自主触发并返回结构化参数。
  - 联网搜索（`enable_search`）：仅 `qwen3.5-omni-realtime` 系列支持，且与 `tools` 互斥。
  - 声音复刻：需先调用独立的 `qwen-voice-enrollment` 接口创建音色，再于 `session.update` 中传入 `voice` 字段使用；驱动模型必须与复刻时指定的 `target_model` 严格一致。

> **注意**：文档 1 中 `session.created` 示例显示 `output_audio_format` 固定为 `"pcm"` 且“不支持自定义输出采样率”，但文档 2、3、4 明确说明 `qwen3.5-omni-plus-realtime`/`flash-realtime` 模型支持 `audio.output.format.sample_rate` 配置（如 24000 Hz）。该矛盾表明文档 1 的描述已过时，应以 SDK 文档为准。

## 关键参数

| 参数 | 类型 | 说明 | 默认值/约束 |
|------|------|------|-------------|
| `model` | string | 必选，指定模型名称 | — |
| `voice` | string | 音色名称 | `Tina`（qwen3.5）、`Cherry`（qwen3-flash）、`Chelsie`（turbo） |
| `modalities` | array | 输出模态 | `["text","audio"]` |
| `instructions` | string | 系统角色指令 | — |
| `turn_detection.type` | string | VAD 类型 | `"server_vad"` |
| `turn_detection.threshold` | float | VAD 灵敏度 | `0.5`（范围 [-1.0, 1.0]） |
| `turn_detection.silence_duration_ms` | int | 静音触发阈值 | `800`（范围 [200, 6000]） |
| `enable_search` | boolean | 启用联网搜索 | `false`（仅 qwen3.5 系列） |
| `tools` | array | 工具定义列表 | —（仅 qwen3.5 系列，且与 `enable_search` 互斥） |
| `temperature` / `top_p` | float | 控制生成多样性 | 建议只设其一；qwen3.5: `0.7`/`0.8`，qwen3-flash: `0.9`/`1.0` |
| `max_tokens` | int | 最大输出 token 数 | 截断响应，不影响生成过程 |

> **注意**：`qwen-omni-turbo` 系列模型对 `temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed` 均**不支持修改**，此限制在文档 2、3、4 中一致强调，开发者需特别注意。

## 使用方式

1. **建立连接**：使用 WebSocket 连接到地域专属域名（如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`），[服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md) 将立即返回 `session.created`。
2. **配置会话**：发送 `session.update` 客户端事件（或调用 SDK 的 `update_session` 方法）设置 `modalities`、`voice`、`turn_detection` 等参数。
3. **输入处理**：
   - **VAD 模式**（推荐）：持续发送 `input_audio_buffer.append`，服务端自动检测 `speech_started`/`speech_stopped` 并提交缓冲区。
   - **Manual 模式**：手动发送 `input_audio_buffer.append` → `input_audio_buffer.commit` → `response.create`。
4. **响应消费**：监听服务端事件流，关键事件包括：
   - `conversation.item.input_audio_transcription.delta`：拼接 `text` + `stash` 获取实时转写预览；
   - `conversation.item.created`（`type="function_call"`）：提取 `call_id` 和 `arguments` 执行工具；
   - `response.audio.delta` / `response.text.delta`：流式消费音频或文本输出。

## 限制和注意事项

- **音频要求**：输入音频需为 16 kHz PCM（VAD 模式强制要求），若使用 `wav` 格式需确保为单声道、16 bit；图片输入限 JPG/JPEG，Base64 编码后 ≤ 256 KB。
- **并发与超时**：`idle_timeout_ms` 仅在 `server_vad` + `qwen3.5-omni-plus/flash-realtime` 下生效，范围 [5000, 30000] ms；静默超时后模型将主动发起引导性回复。
- **功能互斥**：`tools` 与 `enable_search` 不可同时启用，否则服务端返回 `invalid_request_error`。
- **SDK 兼容性**：Python SDK（≥1.26.5）与 Java SDK（≥2.22.15）均要求使用业务空间专属域名（`{WorkspaceId}.<region>.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低。
- **错误处理**：所有客户端事件失败均返回 `error` 事件，需检查 `error.code`（如 `invalid_value`）和 `error.param`（如 `session.modalities`）定位问题。

## 来源文档

- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)


