# omni realtime api

Qwen-Omni-Realtime 是面向多模态实时交互场景的低延迟流式 API，支持语音、文本、工具调用与（部分模型）视频输入，提供端到端音频流式输入/输出能力。它通过 AOQ、WebSocket 和 WebRTC 三种协议接入，适用于智能客服、实时会议助手、语音交互终端等对时延和交互自然度要求高的场景。开发者需关注模态组合、VAD 配置、工具与搜索互斥性等关键约束。

## 支持的模型/功能

当前支持以下模型（均需通过 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 统一入口接入）：
- `qwen3.8-omni-flash-realtime`：支持多通道音频（1/2/4 声道）、语义 VAD、MCP 工具集成、联网搜索、视频输入（`representation_compact` 可配）及 `smooth_output` 风格控制；
- `qwen3.5-omni-plus-realtime` 与 `qwen3.5-omni-flash-realtime`：支持双模态（text+audio）、server_vad、`idle_timeout_ms`、Function Calling，**不支持视频与 MCP**；
- `qwen3-omni-flash-realtime-2025-09-15`（预发布）：启用 `smooth_output`、默认 `temperature=0.9`，音色默认为 `Cherry`。

> **注意**：文档 2 中 `session.created` 示例显示 `qwen3.8-omni-flash-realtime` 默认 `voice="Tina"`，而文档 3 明确指出该模型默认音色为 `Tina`，但 `qwen3-omni-flash-realtime-2025-09-15` 默认为 `Cherry`；文档 3 的客户端事件说明中 `voice` 字段描述更完整，应以文档 3 为准。  
> **注意**：文档 2 的 `session.updated` 示例中字段 `max_response_output_token: "inf"` 与文档 3 的 `max_tokens` 参数定义存在不一致——文档 3 明确 `max_tokens` 是整数且有明确取值范围（如 `qwen3.8-omni-flash-realtime` 为 `[1, 65536]`），而 `"inf"` 非合法 JSON 数值，属示例错误，实际应传整数或省略。

核心功能包括：
- 实时语音输入/输出（PCM/WAV，采样率可配）；
- 语音活动检测（VAD）：`server_vad`（声学）与 `semantic_vad`（语义）两种模式；
- 工具调用：Function Calling（`type=function`）与 MCP（`type=mcp`）并存于 `qwen3.8-omni-flash-realtime`；
- 联网搜索（`enable_search=true`），但**与 `tools` 配置互斥**；
- 多通道空间音频（仅 `qwen3.8-omni-flash-realtime`，需 `pcm`+`16000Hz`+`s16le`+`interleaved`）；
- 视频输入（仅 `qwen3.8-omni-flash-realtime`，`representation_compact` 控制表征粒度）。

## 关键参数

所有配置通过客户端发送 `session.update` 事件完成，服务端返回 `session.updated` 或 `error` 事件确认。关键参数如下：

| 参数 | 类型 | 说明 | 默认值 | 模型支持 |
|------|------|------|--------|----------|
| `modalities` | `["text"]` \| `["text","audio"]` | 输出模态，`["audio"]` 单独不支持 | `["text","audio"]` | 全系列 |
| `voice` / `audio.output.voice` | `string` | 输出音色，新接入**必须使用 `audio.output.voice`** | `Tina`（除 `2025-09-15` 为 `Cherry`） | 全系列 |
| `audio.input.format.type` | `"pcm"` \| `"wav"` | 输入格式，`qwen3.8` 仅支持 `pcm` | `pcm` | `qwen3.5` 系列支持两者；`qwen3.8` 仅 `pcm` |
| `audio.input.format.sample_rate` | `integer` | 输入采样率（Hz） | `16000` | `qwen3.5`: 8k/16k/24k/48k；`qwen3.8`: 仅 `16000` |
| `audio.output.format.type` | `"pcm"` \| `"wav"` | 输出格式 | `pcm` | `qwen3.5` 系列支持两者；`qwen3.8` 仅 `pcm`（文档 2 明确“当前仅支持设为 `pcm`”） |
| `turn_detection.type` | `"server_vad"` \| `"semantic_vad"` | VAD 类型 | `"server_vad"` | `qwen3.8` 与 `qwen3.5` 系列均支持 |
| `idle_timeout_ms` | `integer` | 静默超时（毫秒），仅 `qwen3.5` 系列 + `server_vad` 生效 | — | 仅 `qwen3.5-omni-plus/flash-realtime` |
| `enable_search` | `boolean` | 启用联网搜索 | `false` | `qwen3.8` 与 `qwen3.5` 系列 |
| `tools` | `array` | 工具列表，`type=function` 或 `type=mcp` | — | `qwen3.8` 支持两者；`qwen3.5` 仅 `function` |
| `temperature` / `top_p` / `top_k` | `float` / `float` / `integer` | 采样参数，**二者选一设置即可** | 见文档 3 表格 | 全系列（默认值不同） |
| `max_tokens` | `integer` | 最大输出 token 数 | 模型上限（如 `qwen3.8`: `65536`） | 全系列 |

> **注意**：文档 2 的 `session.updated` 示例中出现 `max_response_output_token: "inf"`，但文档 3 明确 `max_tokens` 为整数且有严格范围，该字段为无效示例，**请忽略 `max_response_output_token`，统一使用 `max_tokens`**。

## 使用方式

1. **建立连接**：选择 AOQ、WebSocket 或 WebRTC 协议接入。推荐 WebSocket（[WebSocket 接入指南](../../raw/_short/omni-realtime-interaction-process-c1786114b7f9b9c5.md)）或使用官方 SDK（[Python SDK](../../raw/_short/omni-realtime-python-sdk-c6ee137356d19420.md)、[Java SDK](../../raw/_short/omni-realtime-java-sdk-80f4b2a483df02c3.md)）；
2. **初始化会话**：连接后立即发送 `session.update` 事件配置 `modalities`、`voice`、`audio`、`turn_detection` 等基础参数；
3. **流式输入音频**：按配置格式（如 `pcm`/`16000Hz`）持续发送 `input_audio` 事件；
4. **处理服务端事件**：监听 `input_audio_buffer.speech_started/stopped`、`conversation.item.created`、`response.*` 等事件驱动后续逻辑；
5. **工具调用**：若 `tools` 已配置，服务端可能返回 `conversation.item.created`（`type=function_call`），客户端执行后需发送 `conversation.item.create` 回传结果，再发 `response.create` 触发续答；
6. **更新配置**：运行中可再次发送 `session.update` 动态调整参数（如切换音色、启停搜索）。

## 限制和注意事项

- **协议与模型兼容性**：`qwen3.8-omni-flash-realtime` 支持全部协议（AOQ/WebSocket/WebRTC），`qwen3.5` 系列仅明确支持 WebSocket 与 WebRTC（文档 1 未提 AOQ 对 `qwen3.5` 的支持）；
- **音频格式硬约束**：输入必须为单声道/多声道 PCM（`s16le`），输出当前仅支持 PCM（文档 2 明确“当前不支持自定义输出采样率”，且 `output_audio_format` 仅限 `pcm`）；
- **互斥配置**：`tools` 与 `enable_search` **不可同时为 `true`**，否则返回 `invalid_request_error`；
- **MCP 安全约束**：`server_url` 必须为公网 HTTPS 443 地址，`authorization` 与 `headers` **不会在 `session.updated` 中回显**，客户端不得依赖该事件重建敏感配置；
- **[Token](../concepts/token.md) 计算**：多通道音频（2/4 声道）输入 [Token](../concepts/token.md) 数为单声道的 2 倍；视频 `representation_compact=normal` 时 [Token](../concepts/token.md) 数为 `none` 模式的 1/4（详见 [Token 计算](https://help.aliyun.com/zh/model-studio/realtime#cfba3898e4d0h)）；
- **VAD 模式行为**：`semantic_vad` 可过滤背景音，但仅 `qwen3.8` 与 `qwen3.5` 系列支持；`server_vad` 下 `idle_timeout_ms` 仅对 `qwen3.5` 系列生效；
- **错误处理**：所有错误均通过 `error` 事件返回，含 `type`、`code`、`message` 和 `param`（如 `session.modalities` 格式错误），需解析 `param` 定位具体字段（见 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)）。

## 来源文档

- [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)


