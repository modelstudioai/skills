# omni realtime api

Qwen-Omni-Realtime 是面向实时语音交互场景的多模态大模型 API，支持文本、音频（含 TTS/ASR）及视频输入，提供低延迟流式响应。它通过 AOQ、WebSocket 和 WebRTC 三种协议接入，适用于智能客服、语音助手、会议纪要等需要端到端实时交互的业务。核心能力包括动态会话配置、多模态输出控制、VAD 驱动的语音轮转、Function Calling 与 MCP 工具集成，以及可选的联网搜索。

## 支持的模型与功能

当前支持以下模型系列（均需显式指定 `model` 字段）：
- `qwen3.8-omni-flash-realtime`（推荐新项目使用）
- `qwen3.5-omni-plus-realtime`
- `qwen3.5-omni-flash-realtime`

> **注意**：文档中提及的 `qwen3-omni-flash-realtime`（无版本号）和 `qwen-omni-turbo-realtime` 系列在 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 中被多次标注为“不支持修改 temperature/top_p/top_k/max_tokens/repetition_penalty/presence_penalty/seed”，但 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md) 的 `session.created` 示例中却返回了 `temperature: 0.8` 等可变参数。实际开发中请以 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 的明确限制为准，`qwen-omni-turbo` 系列参数不可覆盖。

功能特性包括：
- **多模态输出控制**：通过 `modalities: ["text", "audio"]` 同时返回文本与音频流；`["text"]` 仅返回文本。
- **音色定制**：支持 `Tina`（Qwen3.5 默认）、`Cherry`（Qwen3-Omni-Flash 默认）、`Chelsie`（Turbo 默认）及 `longanlingxin`（Qwen3.8 新增），优先级为 `session.audio.output.voice` > `session.voice`。
- **VAD 检测**：支持 `server_vad`（声学检测）和 `semantic_vad`（语义检测），后者可过滤背景音与回应语，仅 Qwen3.8-Omni-Flash-Realtime 和 Qwen3.5-Omni-Realtime 系列支持。
- **工具调用**：支持 Function Calling（`tools` 数组）和 MCP（`type: "mcp"`）两种扩展方式，但 `tools` 与 `enable_search` 不可同时启用。
- **联网搜索**：`enable_search: true` 启用后，模型可自主触发搜索，支持 `search_options.enable_source` 返回来源。

## 关键参数

所有参数均在 `session.update` 事件的 `session` 对象中配置。关键字段如下：

| 参数 | 类型 | 说明 | 默认值（按模型） |
|------|------|------|------------------|
| `modalities` | `array` | 输出模态，仅支持 `["text"]` 或 `["text","audio"]` | `["text","audio"]` |
| `voice` / `audio.output.voice` | `string` | 音色名称 | 见上文“支持的模型与功能” |
| `audio.input.format` | `object` | 输入格式：`{type: "pcm"\|"wav", sample_rate: 8000\|16000\|24000\|48000}` | `{"type": "pcm", "sample_rate": 16000}` |
| `audio.output.format` | `object` | 输出格式：同上，`sample_rate` 支持 24000（默认） | `{"type": "pcm", "sample_rate": 24000}` |
| `turn_detection` | `object` | VAD 配置：`{type: "server_vad"\|"semantic_vad", threshold: [-1.0,1.0], silence_duration_ms: [200,6000]}` | `{type: "server_vad", threshold: 0.5, silence_duration_ms: 800}` |
| `idle_timeout_ms` | `integer` | 静默超时（仅 `qwen3.5-omni-plus-realtime`/`flash-realtime` + `server_vad` 生效） | `[5000, 30000]` |
| `enable_search` | `boolean` | 启用联网搜索 | `false` |
| `tools` | `array` | Function Calling 工具定义列表 | `[]` |
| `temperature` | `float` | 控制输出多样性（0–2） | Qwen3.8: `0.6`；Qwen3.5: `0.7`；Flash: `0.9`；Turbo: `1.0`（不可改） |
| `top_p` | `float` | 核采样阈值（0–1） | Qwen3.8: `0.95`；Qwen3.5: `0.8`；Flash: `1.0`；Turbo: `0.01`（不可改） |
| `max_tokens` | `integer` | 最大输出 token 数 | Qwen3.8: `[1,65536]`；其余模型见[模型列表](../../raw/model-user-guide/get-started-with-models/models.md) |

> **注意**：`input_audio_format` 和 `output_audio_format` 为历史兼容字段，新增接入**必须使用嵌套的 `audio.input.format` 和 `audio.output.format`**，否则部分高级配置（如多通道、自定义采样率）将不生效。详见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 中的“音频配置”章节。

## 使用方式

1. **建立连接**：选择 AOQ（推荐低延迟）、WebSocket（通用）或 WebRTC（浏览器直连）协议。详细流程参见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。
2. **初始化会话**：连接成功后，立即发送 `session.update` 事件配置会话参数（如 `modalities`, `model`, `voice`, `audio`, `turn_detection` 等）。
3. **发送音频**：通过 `input_audio_buffer.append` 发送 PCM/WAV 音频数据；VAD 自动触发 `speech_started`/`speech_stopped` 事件。
4. **处理响应**：监听服务端事件：
   - `session.created` / `session.updated`：确认配置生效；
   - `conversation.item.created`：获取模型回复（含 `message` 或 `function_call`）；
   - `conversation.item.input_audio_transcription.delta`：获取 ASR 实时识别结果（拼接 `text` + `stash`）；
   - `error`：捕获并处理错误（如 `invalid_value` 错误码对应参数校验失败）。
5. **SDK 快速接入**：官方提供 [Python SDK](../../raw/_short/omni-realtime-python-sdk-c6ee137356d19420.md) 和 [Java SDK](../../raw/_short/omni-realtime-java-sdk-80f4b2a483df02c3.md)，封装连接管理、事件序列化与重试逻辑。

## 限制和注意事项

- **协议与模型兼容性**：`qwen3.8-omni-flash-realtime` 支持全部三种协议（AOQ/WebSocket/WebRTC），而 `qwen3.5-omni-plus-realtime` 仅明确支持 WebSocket（见 [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)）。
- **多通道音频**：仅 `qwen3.8-omni-flash-realtime` 支持 2/4 声道输入，且**必须**在首段音频发送前完成 `audio.input.format` 配置，且固定为 `pcm`/`16000`/`s16le`/`interleaved`。
- **参数互斥规则**：
  - `tools` 与 `enable_search` 不可同时为 `true`；
  - `temperature` 与 `top_p` 建议只设置其一，避免策略冲突；
  - `qwen-omni-turbo` 系列所有生成参数（`temperature`, `top_p`, `top_k`, `max_tokens`, `repetition_penalty`, `presence_penalty`, `seed`）均**不可修改**。
- **[Token](../concepts/token.md) 计算**：多通道音频、视频 `representation_compact: "normal"` 等配置显著影响 [Token](../concepts/token.md) 消耗，具体规则见 [Token 计算](https://help.aliyun.com/zh/model-studio/realtime#cfba3898e4d0h)（外部链接）。
- **MCP 配置约束**：`server_url` 必须为公网 HTTPS 443 地址，禁止包含用户名、密码、fragment；`headers` 禁止设置 `host`, `authorization`, `content-type` 等敏感头；`allowed_tools` 为空数组表示不暴露任何工具。

## 来源文档

- [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)
- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)


