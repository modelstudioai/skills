# omni realtime api

Qwen-Omni-Realtime API 是基于 WebSocket（也支持 AOQ/WebRTC）的低延迟多模态实时交互接口，面向语音对话、音视频助手等场景提供文本+音频同步生成能力。它采用事件驱动模型，客户端通过发送结构化事件（如 `session.update`、`response.create`）控制会话行为，服务端以对称事件（如 `session.updated`、`response.done`）反馈状态与内容。该 API 不是 RESTful 接口，需维持长连接并正确处理事件生命周期。

## 支持的模型/功能

当前支持以下核心模型（均需显式在 `session.model` 中指定）：
- `qwen3.8-omni-flash-realtime`：主力低延迟模型，支持多通道音频输入（1/2/4 声道）、语义 VAD（`semantic_vad_ec`）、MCP 工具、视频表征压缩（`representation_compact`）及 `smooth_output` 风格控制。
- `qwen3.5-omni-plus-realtime` 与 `qwen3.5-omni-flash-realtime`：兼容性模型，支持 `server_vad` 和 `semantic_vad`，但**不支持** `semantic_vad_ec`、MCP、视频输入或 `smooth_output`。
- `qwen3-omni-flash-realtime-2025-09-15`：特定日期快照模型，启用 `smooth_output` 且默认 `temperature=0.9`、`top_p=1.0`、`top_k=50`。

通用功能包括：
- 双模态输出：`["text", "audio"]`（默认）或仅 `["text"]`；
- 输入音频转录（ASR）：固定使用 `qwen3-asr-flash-realtime` 模型；
- 语音活动检测（VAD）：`server_vad`（声学）、`semantic_vad`（语义）、`semantic_vad_ec`（客服增强）；
- 联网搜索（`enable_search=true`）与 Function Calling/MCP 工具调用（二者互斥）；
- 系统指令（`instructions`）、采样参数（`temperature`/`top_p`/`top_k`）、惩罚项（`repetition_penalty`/`presence_penalty`）等标准 LLM 控制能力。

> **注意**：文档 3 中 `session.created` 示例声明“`output_audio_format` 当前仅支持设为 `pcm`”且“不支持自定义输出采样率”，但[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)明确允许 `audio.output.format.sample_rate` 在 8000–48000 Hz 间配置（如 `24000`），且 `session.updated` 事件会回显该值。实际以[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)为准，服务端支持自定义输出采样率。

## 关键参数

所有配置通过 `session.update` 事件的 `session` 对象传递，关键字段如下：

| 字段 | 说明 | 约束与默认值 |
|--------|------|----------------|
| `modalities` | 输出模态 | 必须为 `["text"]` 或 `["text","audio"]`；`["audio"]` 单独不支持 |
| `voice` / `audio.output.voice` | 音色 | 新接入**必须使用 `audio.output.voice`**；`session.voice` 为兼容字段，若两者共存，以 `audio.output.voice` 为准。默认值因模型而异（如 `Tina`、`Cherry`） |
| `audio.input.format` | 输入音频格式 | `type`（`pcm`/`wav`）和 `sample_rate`（8000/16000/24000/48000）；Qwen3.8 多通道输入强制 `pcm`+`16000`+`s16le`+`interleaved` |
| `audio.output.format` | 输出音频格式 | 同上，`type` 和 `sample_rate` 可自由组合 |
| `turn_detection.type` | VAD 类型 | `server_vad`（全模型）、`semantic_vad`（Qwen3.5+Qwen3.8）、`semantic_vad_ec`（**仅 Qwen3.8**） |
| `enable_search` | 联网搜索 | `boolean`，默认 `false`；与 `tools` 互斥 |
| `tools` | 工具列表 | `type=function`（Function Calling）或 `type=mcp`（MCP）；`mcp` 配置中 `server_url` 必须为公网 HTTPS 443 地址，敏感字段（`authorization`/`headers`）**不在 `session.updated` 中回显** |
| `smooth_output` | 回复风格 | **仅 `qwen3-omni-flash-realtime-2025-09-15` 生效**；`true`（口语化）、`false`（书面化）、`null`（自动） |
| `max_tokens` | 最大输出 Token 数 | `qwen3.8-omni-flash-realtime`：`[1, 65536]`；其他模型取值范围见[模型列表](raw/model-user-guide/get-started-with-models/models.md)；**截断响应，不影响生成过程** |

> **注意**：`input_audio_transcription.model` 固定为 `"qwen3-asr-flash-realtime"`，不可修改；`input_audio_format`/`output_audio_format` 为历史兼容字段，新接入应统一使用 `audio.input.format`/`audio.output.format` 结构。详见[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。

## 使用方式

1. **建立连接**：使用 WebSocket（推荐）、AOQ 或 WebRTC 连接至对应地域的 endpoint（参见[Realtime API](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)）；
2. **初始化会话**：连接后服务端立即返回 `session.created` 事件，含默认配置；
3. **配置会话**：发送 `session.update` 事件调整参数（如 `modalities`、`voice`、`turn_detection`）；服务端校验后返回 `session.updated` 或 `error`；
4. **输入数据**：
   - 音频：持续发送 `input_audio_buffer.append`（Base64 PCM/WAV），VAD 模式下由服务端自动 `commit`，Manual 模式需客户端显式发送 `input_audio_buffer.commit`；
   - 文本/图像：通过 `conversation.item.create` 事件添加（本文档未展开，详见[服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)）；
5. **触发响应**：VAD 模式下语音停止后自动开始；Manual 模式或工具调用后需发送 `response.create`；
6. **接收响应**：服务端按序返回 `response.created` → `conversation.item.created` → `response.content_part.added` → `response.done`；
7. **控制流程**：发送 `response.cancel` 中断当前响应，或 `input_audio_buffer.clear` 清空缓冲区。

SDK 封装了上述流程，推荐优先使用 [Python SDK](../../raw/_short/omni-realtime-python-sdk-c6ee137356d19420.md) 或 [Java SDK](../../raw/_short/omni-realtime-java-sdk-80f4b2a483df02c3.md)。

## 限制和注意事项

- **Token 限制**：Qwen3.8-Omni-Flash-Realtime 单次会话总输入 Token 上限为 **196608**；多通道音频（2/4 声道）输入 Token 数为单声道的 2 倍；视频 Token 计算详见[Token 计算](https://help.aliyun.com/zh/model-studio/realtime#cfba3898e4d0h)。
- **音频约束**：
  - 输入：PCM 必须为 `s16le`、`interleaved`；WAV 必须为单声道 16-bit；采样率需与 `audio.input.format.sample_rate` 严格一致；
  - 输出：`audio.output.format.sample_rate` 可配置，但服务端实际输出采样率可能因编解码器微调（如 `24000` 输出可能为 `24048`），客户端应以实际流为准。
- **工具与搜索互斥**：`tools` 数组非空时，`enable_search` 必须为 `false`，否则返回 `invalid_request_error`。
- **MCP 安全限制**：`server_url` 必须为公网 HTTPS 443；`headers` 名称禁止含 `mcp-`、`host`、`authorization` 等敏感前缀或关键字；`authorization` 和 `headers` 值**不会在 `session.updated` 中回显**，客户端不可依赖该事件重建凭证。
- **VAD 超时**：`idle_timeout_ms` 仅在 `qwen3.5-omni-plus-realtime`/`qwen3.5-omni-flash-realtime` + `server_vad` 组合下生效；Qwen3.8 模型无此字段。
- **错误处理**：所有错误均以 `error` 事件返回，含 `error.type`、`error.code` 和 `error.message`，例如模态不支持时 `param` 字段会指出 `session.modalities`。详细错误码见[服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)


