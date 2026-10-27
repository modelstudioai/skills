# omni realtime api

Qwen-Omni-Realtime 是百炼平台提供的低延迟、多模态实时交互 API，支持语音输入/输出、文本生成、工具调用（Function Calling / MCP）、联网搜索等能力，适用于智能客服、实时语音助手、会议纪要等场景。API 基于事件驱动模型，通过 WebSocket、AOQ 或 WebRTC 协议实现双向流式通信。所有交互均围绕会话（session）生命周期展开，配置灵活且可动态更新。

## 支持的模型与核心功能

当前支持以下模型（均需通过 [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md) 接入）：
- `qwen3.8-omni-flash-realtime`（推荐用于高并发、低延迟场景）
- `qwen3.5-omni-plus-realtime`
- `qwen3.5-omni-flash-realtime`
- `qwen3-omni-flash-realtime-2025-09-15`（实验性版本，含 `smooth_output` 等新字段）

**核心功能包括**：
- **多模态 I/O**：支持 `["text"]` 或 `["text", "audio"]` 输出模态；音频输入支持单/双/四声道空间音频（仅 `qwen3.8-omni-flash-realtime`）。
- **语音活动检测（VAD）**：提供 `server_vad`（基础声学检测）、`semantic_vad`（语义级静音判断）和 `semantic_vad_ec`（客服优化版，仅 `qwen3.8-omni-flash-realtime` 支持）。
- **工具调用**：支持 Function Calling（`type=function`）和 MCP（`type=mcp`），但二者不可与 `enable_search: true` 同时启用。
- **联网搜索**：由 `enable_search` 控制，启用后模型可自主触发搜索，结果来源可通过 `search_options.enable_source` 开启。
- **音色与音频格式控制**：支持多音色（如 `Tina`, `Cherry`），输入/输出音频格式支持 `pcm`/`wav`，采样率可配（注意模型间约束差异）。

> **注意**：文档 3 中 `session.created` 示例声明“`output_audio_format` 当前仅支持 `pcm`”且“不支持自定义输出采样率”，但文档 2 明确允许 `session.audio.output.format.sample_rate` 设置为 `8000/16000/24000/48000`（对 `qwen3.5` 系列）或 `24000`（默认值）。该矛盾以 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 为准——服务端实际支持按配置返回对应采样率的 `wav` 输出，文档 3 的描述已过时。

## 关键参数

所有会话级配置通过 `session.update` 客户端事件设置，关键参数如下（完整定义见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)）：

| 参数 | 类型 | 说明 | 默认值（按模型） |
|------|------|------|------------------|
| `modalities` | `array` | 输出模态，必须为 `["text"]` 或 `["text","audio"]` | `["text","audio"]` |
| `voice` / `audio.output.voice` | `string` | 音色名；新接入**必须使用 `audio.output.voice`**，`session.voice` 为兼容字段 | `Tina`（`qwen3.8`/`qwen3.5` 系列）；`Cherry`（`2025-09-15`） |
| `audio.input.format.type` | `string` | 输入格式：`pcm`（必选，多通道仅支持 `pcm`）或 `wav`（`qwen3.5` 系列） | `pcm` |
| `audio.input.format.sample_rate` | `integer` | 输入采样率：`qwen3.5` 系列支持 `8000/16000/24000/48000`；`qwen3.8` 多通道**强制 `16000`** | `16000` |
| `turn_detection.type` | `string` | VAD 类型：`server_vad`（全模型）、`semantic_vad`（全模型）、`semantic_vad_ec`（仅 `qwen3.8`） | `server_vad` |
| `enable_search` | `boolean` | 是否启用联网搜索 | `false` |
| `tools` | `array` | 工具定义列表；`type=function` 或 `type=mcp`；与 `enable_search` 互斥 | — |
| `temperature` / `top_p` / `top_k` | `float`/`integer` | 采样参数；**建议只设置其中一个多样性参数** | 见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 表格 |
| `max_tokens` | `integer` | 响应最大 Token 数；超长将被截断 | `qwen3.8`: `[1,65536]`；其余模型见 [模型列表](../../raw/model-user-guide/get-started-with-models/models.md) |

## 使用方式

1. **建立连接**：选择 AOQ、WebSocket 或 WebRTC 协议接入。推荐 WebSocket（[WebSocket 接入指南](../../raw/_short/omni-realtime-interaction-process-c1786114b7f9b9c5.md)），Python/Java SDK 已封装连接与事件处理逻辑（[Python SDK](../../raw/_short/omni-realtime-python-sdk-c6ee137356d19420.md)、[Java SDK](../../raw/_short/omni-realtime-java-sdk-80f4b2a483df02c3.md)）。
2. **初始化会话**：连接后服务端立即返回 `session.created` 事件，包含默认配置。
3. **配置会话**：发送 `session.update` 事件（如设置 `modalities`, `voice`, `turn_detection` 等），服务端校验后返回 `session.updated` 或 `error`。
4. **交互流程**：
   - **VAD 模式（默认）**：客户端持续发送 `input_audio_buffer.append`；服务端自动检测语音起止，触发 `input_audio_buffer.speech_started`/`.speech_stopped`，并创建 `conversation.item.created`。
   - **Manual 模式**：客户端在音频结束后显式发送 `input_audio_buffer.commit`。
   - **触发响应**：VAD 自动触发，或手动发送 `response.create`（如工具调用后续答）。
   - **取消响应**：发送 `response.cancel`。
5. **处理服务端事件**：监听 `conversation.item.created`（含文本/音频内容）、`response.content_part.added`（流式音频片段）、`response.done`（响应结束）等事件。

## 限制和注意事项

- **Token 限制**：`qwen3.8-omni-flash-realtime` 输入总 Token 上限为 `196608`；多通道音频输入 Token 消耗为单声道的 2 倍（详见 [Token 计算](https://help.aliyun.com/zh/model-studio/realtime#cfba3898e4d0h)）。
- **音频约束**：
  - 多通道输入（2/4 声道）**仅 `qwen3.8-omni-flash-realtime` 支持**，且**必须**使用 `pcm` + `16000 Hz` + `s16le` + `interleaved`。
  - `input_audio_buffer.append` 的 Base64 数据需为原始 PCM/WAV，无额外封装。
- **工具与搜索互斥**：`tools` 和 `enable_search` 不可同时为 `true`，否则返回 `invalid_request_error`。
- **MCP 安全限制**：`server_url` 必须为公网 HTTPS 443 地址；`authorization`/`headers` 不在 `session.updated` 中回显，客户端不可依赖其重建敏感配置。
- **参数覆盖规则**：`session.audio.output.voice` 优先级高于 `session.voice`；`audio.input.format` 优先级高于历史字段 `input_audio_format`。
- **错误处理**：所有客户端事件失败均返回 `error` 事件（结构见 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)），需检查 `error.param` 定位具体字段。

## 来源文档

- [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)
- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)


