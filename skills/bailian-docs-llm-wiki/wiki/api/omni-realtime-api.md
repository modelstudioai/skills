# omni realtime api

Qwen-Omni-Realtime 是面向多模态[实时交互](../concepts/realtime.md)场景的低延迟大模型 API，支持语音、文本、视频等输入与文本+音频混合输出，适用于智能客服、虚拟助手、会议纪要等强交互场景。其核心能力基于 WebSocket、AOQ（AI over QUIC）和 WebRTC 三种传输协议实现端到端流式响应，开发者可通过事件驱动方式控制会话生命周期与模型行为。详细接入流程请参见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。

## 支持的模型与功能

当前支持以下模型（均需通过 `session.update` 显式指定 `session.model`）：
- `qwen3.8-omni-flash-realtime`（推荐用于多通道音频/视频输入）
- `qwen3.5-omni-plus-realtime`
- `qwen3.5-omni-flash-realtime`
- `qwen3-omni-flash-realtime-2025-09-15`（实验性版本，启用 `smooth_output` 等新参数）

核心功能包括：
- **多模态 I/O**：支持 `["text"]` 或 `["text", "audio"]` 输出；音频输入支持单/双/四通道 PCM（仅 `qwen3.8-omni-flash-realtime`），输出支持 `pcm`/`wav` 格式；
- **语音活动检测（VAD）**：`server_vad`（声学）与 `semantic_vad`（语义）两种模式，支持自定义灵敏度与静音时长；
- **工具调用**：同时支持 Function Calling（`type=function`）与 MCP（`type=mcp`），但不可与 `enable_search` 共存；
- **联网搜索**：`enable_search: true` 启用，支持来源标注（`search_options.enable_source`）；
- **音色定制**：通过 `session.audio.output.voice` 指定音色（如 `"longanlingxin"`），旧字段 `session.voice` 仅作兼容，[音色列表](https://help.aliyun.com/zh/model-studio/omni-voice-list#qwen38-voices) 可查完整支持列表。

> **注意**：文档 2 中 `qwen3.5-omni-flash-realtime` 的默认 `temperature` 为 0.7，而文档 3 的 `session.created` 示例中 `qwen3.8-omni-flash-realtime` 默认值为 0.6 —— 实际默认值依模型版本而定，以 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 中各模型的明确声明为准。

## 关键参数

所有配置均通过 `session.update` 事件的 `session` 对象传递，关键字段如下：

| 字段 | 类型 | 说明 | 默认值/约束 |
|------|------|------|-------------|
| `modalities` | `array` | 输出模态，仅支持 `["text"]` 或 `["text","audio"]` | `["text","audio"]` |
| `voice` / `audio.output.voice` | `string` | 音色标识符 | `Tina`（`qwen3.8`/`qwen3.5` 系列）；`Cherry`（`qwen3-omni-flash-realtime-2025-09-15`） |
| `audio.input.format` | `object` | 输入格式：`type`（`pcm`/`wav`）、`sample_rate`（8k/16k/24k/48k Hz）；多通道仅支持 `pcm`+`16000`+`s16le`+`interleaved` | `{"type":"pcm","sample_rate":16000}` |
| `audio.output.format` | `object` | 输出格式：同上 | `{"type":"wav","sample_rate":24000}` |
| `turn_detection` | `object` | VAD 配置：`type`（`server_vad`/`semantic_vad`）、`threshold`（-1.0~1.0）、`silence_duration_ms`（200~6000 ms） | `{"type":"server_vad","threshold":0.5,"silence_duration_ms":800}` |
| `enable_search` | `boolean` | 是否启用联网搜索 | `false`（与 `tools` 互斥） |
| `tools` | `array` | 工具定义列表，支持 `function` 和 `mcp` 类型 | — |
| `temperature` / `top_p` | `float` | 生成多样性控制（二者选一设置即可） | `qwen3.8`: `0.6`/`0.95`；`qwen3.5`: `0.7`/`0.8`；`2025-09-15`: `0.9`/`1.0` |
| `max_tokens` | `integer` | 响应最大 Token 数 | `qwen3.8`: 1~65536；其余模型取值上限为模型最大输出长度 |

完整字段定义与示例详见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。

## 使用方式

1. **建立连接**：选择 WebSocket / AOQ / WebRTC 协议接入，具体地址与握手流程见 [WebSocket 接入指南](../../raw/_short/omni-realtime-interaction-process-c1786114b7f9b9c5.md)；
2. **初始化会话**：连接成功后，服务端立即返回 `session.created` 事件（参考 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)）；
3. **配置会话**：发送 `session.update` 事件更新模型、模态、VAD、工具等参数；
4. **输入数据**：
   - 音频：通过 `input_audio_buffer.append` 发送原始 PCM/WAV 数据；
   - 文本：通过 `conversation.item.create` 发送 `message` 类型项；
5. **触发响应**：VAD 自动触发 `response.create`；手动模式下需显式发送该事件；
6. **处理响应**：监听 `conversation.item.created`（含 `message`、`function_call`、`mcp_call` 等类型）及 `response.audio.delta` 等流式事件。

SDK 支持 Python 与 Java，详见 [Python SDK](../../raw/_short/omni-realtime-python-sdk-c6ee137356d19420.md) 与 [Java SDK](../../raw/_short/omni-realtime-java-sdk-80f4b2a483df02c3.md)。

## 限制和注意事项

- **Token 限制**：`qwen3.8-omni-flash-realtime` 单次 `session.update` 的输入 Token 总数上限为 196608；多通道音频输入（2/4 声道）Token 消耗为单声道的 2 倍，详见 [Token 计算](https://help.aliyun.com/zh/model-studio/realtime#cfba3898e4d0h)；
- **音频配置约束**：`audio.input.format` 必须在首段音频发送前完成设置，之后不可修改；多通道输入必须使用 `pcm`/`16000`/`s16le`/`interleaved` 组合；
- **功能互斥**：`tools` 与 `enable_search` 不可同时启用；`smooth_output` 仅对 `qwen3-omni-flash-realtime-2025-09-15` 生效；
- **MCP 安全限制**：`server_url` 必须为公网 HTTPS 443 地址，`authorization` 与 `headers` 不会在 `session.updated` 中回显，客户端不得依赖该事件重建敏感配置；
- **错误处理**：服务端返回 `error` 事件时需检查 `error.code`（如 `invalid_value`）与 `error.param`（如 `session.modalities`），并按 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md) 文档修正请求；
- **兼容性提示**：`input_audio_format`/`output_audio_format` 为历史字段，新增接入应统一使用嵌套的 `audio.input.format`/`audio.output.format`。

## 来源文档

- [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)
- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)


