# omni realtime api

Qwen-Omni-Realtime 是面向多模态实时交互场景的低延迟大模型 API，支持语音、文本、视频等输入与文本+音频混合输出，适用于智能客服、语音助手、实时会议摘要等强交互场景。其核心能力基于 AOQ、WebSocket 和 WebRTC 三种协议实现端到端毫秒级响应，并提供细粒度的会话控制、VAD 配置、工具调用与联网搜索能力。开发者需通过 `session.update` 初始化配置，并按事件驱动模型与服务端交互。

## 支持的模型/功能

当前支持以下模型（均以 `-realtime` 后缀标识）：
- `qwen3.8-omni-flash-realtime`
- `qwen3.5-omni-plus-realtime`
- `qwen3.5-omni-flash-realtime`
- `qwen3-omni-flash-realtime-2025-09-15`（实验性版本，部分参数行为不同）

核心功能包括：
- **多模态 I/O**：支持 `["text"]` 或 `["text","audio"]` 输出；Qwen3.8-Omni-Flash-Realtime 还支持视频输入（`video.input.representation_compact`）。
- **语音活动检测（VAD）**：支持 `server_vad`（声学）和 `semantic_vad`（语义）两种模式，后者可过滤背景音与回应语。
- **工具调用**：同时支持 Function Calling（`type=function`）和 MCP（`type=mcp`），但二者不可与 `enable_search` 共存。
- **联网搜索**：通过 `enable_search: true` 启用，由模型自主判断是否触发，支持来源返回（`search_options.enable_source`）。
- **输入音频转录**：固定使用 `qwen3-asr-flash-realtime` 模型，通过 `input_audio_transcription` 配置启用。

> **注意**：文档 3 中 `session.created` 示例声明“`output_audio_format` 当前仅支持设为 `pcm`”且“不支持自定义输出采样率”，但文档 2 明确允许 `wav` 格式及 `8000/16000/24000/48000` Hz 输出采样率（对 Qwen3.5 系列），且 `session.updated` 事件会回显客户端设置的 `audio.output.format`。该矛盾以 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 为准，服务端实际支持动态配置。

## 关键参数

所有配置通过 `session.update` 事件传递，关键字段如下：

| 字段 | 说明 | 默认值（按模型） |
|------|------|----------------|
| `modalities` | 输出模态数组，必须为 `["text"]` 或 `["text","audio"]` | `["text","audio"]` |
| `voice` / `audio.output.voice` | 音色名，新接入**必须使用 `audio.output.voice`**；`session.voice` 为兼容字段 | `Tina`（Qwen3.8/Qwen3.5 系列）；`Cherry`（`2025-09-15`） |
| `audio.input.format` | 输入格式：`pcm`（默认）或 `wav`；Qwen3.8 多通道仅支持 `pcm` | `pcm` |
| `audio.input.format.sample_rate` | 输入采样率：Qwen3.5 系列支持 `8000/16000/24000/48000`；Qwen3.8 多通道**强制 `16000`** | `16000` |
| `audio.output.format` | 输出格式：`pcm` 或 `wav` | `pcm` |
| `audio.output.format.sample_rate` | 输出采样率：Qwen3.5 系列支持 `8000/16000/24000/48000`（默认 `24000`） | `24000` |
| `turn_detection.type` | VAD 类型：`server_vad`（默认）或 `semantic_vad` | `server_vad` |
| `turn_detection.silence_duration_ms` | 语音后静音阈值（ms），范围 `[200, 6000]` | `800` |
| `instructions` | 系统角色提示词，影响模型行为 | — |
| `enable_search` | 是否启用联网搜索（与 `tools` 互斥） | `false` |
| `tools` | 工具定义数组，`type=function` 或 `type=mcp` | — |
| `temperature` / `top_p` / `top_k` | 采样参数，**建议只设置其中一个**控制多样性 | 见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) |
| `max_tokens` | 响应最大 Token 数（截断，不影响生成逻辑） | `qwen3.8`: `[1, 65536]`；其余见[模型列表](../../raw/model-user-guide/get-started-with-models/models.md) |
| `smooth_output` | **仅 `2025-09-15` 版本生效**：`true`（口语化）、`false`（书面化） | `true` |

## 使用方式

1. **建立连接**：选择 AOQ、WebSocket 或 WebRTC 协议接入。推荐 WebSocket（[WebSocket 接入指南](../../raw/_short/omni-realtime-interaction-process-c1786114b7f9b9c5.md)）或 AOQ（[AOQ 接入](../../raw/model-api-reference/realtime-api-user-guide/realtime-model-connection/realtime-aoq-access.md)）。
2. **初始化会话**：连接成功后立即发送 `session.update` 事件配置参数（如 `modalities`, `voice`, `turn_detection` 等）。服务端返回 `session.updated` 或 `error`。
3. **输入数据**：
   - 音频：分块 Base64 编码后发 `input_audio_buffer.append`；VAD 模式下由服务端自动 `commit`，Manual 模式需主动发送 `input_audio_buffer.commit`。
   - 文本/图像：通过 `conversation.item.create` 发送（文档未展开，详见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)）。
4. **触发响应**：VAD 模式下语音停止后自动响应；Manual 模式或工具调用后需显式发 `response.create`。
5. **处理响应**：监听 `response.created` → `conversation.item.created` → `response.content_part.added` → `response.done` 流式事件。
6. **错误处理**：所有错误均以 `error` 事件返回，含 `type`、`code`、`message` 和 `param`（如 `session.modalities`）。

SDK 支持：[Python SDK](../../raw/_short/omni-realtime-python-sdk-c6ee137356d19420.md) 和 [Java SDK](../../raw/_short/omni-realtime-java-sdk-80f4b2a483df02c3.md)。

## 限制和注意事项

- **Token 限制**：Qwen3.8-Omni-Flash-Realtime 输入总 Token 上限为 196608；多通道音频（2/4 声道）输入 Token 数为单声道的 2 倍（见 [Token 计算](https://help.aliyun.com/zh/model-studio/realtime#cfba3898e4d0h)）。
- **协议约束**：
  - WebRTC：仅支持音频，不支持视频或工具调用。
  - AOQ：支持全功能，但需客户端实现 QUIC 栈。
- **参数互斥**：`tools` 与 `enable_search` 不可同时为 `true`；`temperature` 与 `top_p` 建议只设其一。
- **MCP 安全限制**：`server_url` 必须为公网 HTTPS 443 地址；`headers` 禁用敏感头（如 `authorization`, `host`）；凭证类字段（`authorization`, `headers`）**不会在 `session.updated` 中回显**，客户端不可依赖。
- **VAD 模式差异**：`idle_timeout_ms` 仅在 `qwen3.5-omni-plus-realtime` 或 `qwen3.5-omni-flash-realtime` + `server_vad` 时生效；`semantic_vad` 在 Qwen3.8 和 Qwen3.5 系列均支持。
- **音色兼容性**：`qwen3-omni-flash-realtime-2025-09-15` 默认音色为 `Cherry`，与其他模型不同，需显式指定避免意外切换。

## 来源文档

- [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)
- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)


