# omni realtime api

Qwen-Omni-Realtime 是百炼平台提供的低延迟、多模态实时交互 API，支持语音输入/输出、文本生成、工具调用与联网搜索等能力，适用于智能客服、语音助手、实时会议摘要等场景。它通过 AOQ、WebRTC 或 WebSocket 协议建立长连接，以事件流方式实现双向实时通信。开发者需先建立会话，再通过标准客户端事件控制交互流程。

## 支持的模型与功能

当前支持以下模型（均需通过 [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md) 接入）：
- `qwen3.8-omni-flash-realtime`（推荐新项目使用）
- `qwen3.5-omni-plus-realtime`
- `qwen3.5-omni-flash-realtime`
- `qwen3-omni-flash-realtime-2025-09-15`（实验性版本，部分参数行为不同）

核心功能包括：
- **多模态 I/O**：支持 `["text"]` 或 `["text", "audio"]` 输出；音频支持 PCM/WAV 输入与输出，Qwen3.8-Omni-Flash-Realtime 还支持 2/4 声道空间音频输入。
- **语音活动检测（VAD）**：提供 `server_vad`（基础声学）、`semantic_vad`（语义过滤）和 `semantic_vad_ec`（客服优化）三种模式。
- **工具调用**：支持 Function Calling（`type=function`）与 MCP（`type=mcp`），但二者不可与 `enable_search: true` 同时启用。
- **联网搜索**：由 `enable_search` 控制，启用后模型可自主触发搜索；需注意其与 `tools` 的互斥性。
- **输入音频转录**：固定使用 `qwen3-asr-flash-realtime` 模型，通过 `input_audio_transcription` 配置。

> **注意**：文档 3 中 `session.created` 示例显示 `output_audio_format` 固定为 `"pcm"` 且“不支持自定义采样率”，但文档 2 明确说明 `qwen3.5-omni-plus-realtime` 等模型支持 `output.audio.format.sample_rate` 设为 8000/16000/24000/48000 Hz。该矛盾以 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 为准，服务端实际支持动态配置。

## 关键参数

所有会话级参数均通过 `session.update` 事件设置，服务端在 `session.updated` 中回显确认。关键字段如下：

| 参数 | 类型 | 说明 | 默认值（按模型） |
|--------|------|------|------------------|
| `modalities` | `array` | 输出模态，仅支持 `["text"]` 或 `["text","audio"]` | `["text","audio"]` |
| `voice` / `audio.output.voice` | `string` | 音色，新接入**必须使用 `audio.output.voice`**；`session.voice` 为兼容字段 | `Tina`（Qwen3.8/Qwen3.5 系列）；`Cherry`（`2025-09-15`） |
| `audio.input.format.type` | `string` | 输入格式：`pcm`（默认）或 `wav`（Qwen3.5 系列）；Qwen3.8 多通道仅支持 `pcm` | `pcm` |
| `audio.input.format.sample_rate` | `integer` | 输入采样率：Qwen3.5 系列支持 8000/16000/24000/48000；Qwen3.8 多通道**强制 16000** | Qwen3.5: `16000`；Qwen3.8: `16000` |
| `audio.output.format.sample_rate` | `integer` | 输出采样率：Qwen3.5 系列支持 8000/16000/24000/48000；Qwen3.8 默认 `24000` | Qwen3.5: `24000`；Qwen3.8: `24000` |
| `turn_detection.type` | `string` | VAD 类型：`server_vad`（全模型）、`semantic_vad`（Qwen3.5+Qwen3.8）、`semantic_vad_ec`（Qwen3.8 专属） | `server_vad` |
| `enable_search` | `boolean` | 是否启用联网搜索 | `false` |
| `tools` | `array` | 工具定义列表，`type=function` 或 `type=mcp` | — |
| `temperature` / `top_p` / `top_k` | `float`/`integer` | 采样参数，**建议只设置其中一个**控制多样性 | 见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 表格 |
| `max_tokens` | `integer` | 响应最大输出 [Token](../concepts/token.md) 数（截断生效） | Qwen3.8: `[1, 65536]`；其他模型见 [模型列表](../../raw/model-user-guide/get-started-with-models/models.md) |

> **注意**：`smooth_output` 参数**仅对 `qwen3-omni-flash-realtime-2025-09-15` 生效**，其他模型忽略；`idle_timeout_ms` 仅在 `qwen3.5-omni-plus-realtime`/`qwen3.5-omni-flash-realtime` + `server_vad` 下有效。这些约束需严格遵循 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 定义。

## 使用方式

1. **建立连接**：选择 AOQ、WebRTC 或 WebSocket 协议接入。WebSocket 是最常用方式，详见 [WebSocket 接入指南](../../raw/_short/omni-realtime-interaction-process-c1786114b7f9b9c5.md)；SDK 支持 Python 和 Java（[Python SDK](../../raw/_short/omni-realtime-python-sdk-c6ee137356d19420.md)、[Java SDK](../../raw/_short/omni-realtime-java-sdk-80f4b2a483df02c3.md)）。
2. **初始化会话**：连接后服务端自动发送 `session.created`；如需自定义配置，立即发送 `session.update` 事件。
3. **输入数据**：
   - 音频：通过 `input_audio_buffer.append` 追加 Base64 音频，再以 `input_audio_buffer.commit` 提交（Manual 模式）或等待服务端自动提交（VAD 模式）。
   - 文本：通过 `conversation.item.create` 发送 `message` 类型项。
4. **触发响应**：VAD 模式下服务端自动响应；Manual 模式或工具调用后需显式发送 `response.create`。
5. **处理响应**：监听 `conversation.item.created`（含 `text`/`audio` 内容）、`response.content_part.added`、`response.done` 等事件。
6. **错误处理**：所有错误均以 `error` 事件返回，需检查 `error.code` 和 `error.param` 定位问题（参见 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)）。

## 限制和注意事项

- **[Token](../concepts/token.md) 限制**：Qwen3.8-Omni-Flash-Realtime 单次 `session.update` 的全部输入 [Token](../concepts/token.md) 上限为 196608；多通道音频输入（2/4 声道）Token 消耗为单声道的 2 倍（详见 [Token 计算](https://help.aliyun.com/zh/model-studio/realtime#cfba3898e4d0h)）。
- **协议与模型兼容性**：AOQ/WebRTC/WebSocket 均支持全部模型，但 WebRTC 对音视频编解码有额外要求，生产环境建议优先验证 WebSocket。
- **工具与搜索互斥**：`tools` 和 `enable_search` 不可同时为 `true`，否则 `session.update` 将返回 `invalid_request_error`。
- **MCP 敏感字段不回显**：`server_url`、`authorization`、`headers` 等 MCP 配置**不会出现在 `session.updated` 事件中**，客户端不得依赖该事件重建凭证。
- **音频格式兼容性**：`input_audio_format` 和 `output_audio_format` 字段为历史兼容字段，新接入**必须使用嵌套的 `audio.input.format` 和 `audio.output.format`**，否则部分高级配置（如多通道）将无法生效。
- **静默超时行为差异**：`idle_timeout_ms` 仅对 `qwen3.5-omni-plus-realtime` 和 `qwen3.5-omni-flash-realtime` 生效，Qwen3.8 系列模型不支持该参数。

## 来源文档

- [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)
- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)


