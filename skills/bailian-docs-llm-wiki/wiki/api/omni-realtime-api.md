# omni realtime api

Qwen-Omni-Realtime API 是百炼平台提供的实时多模态对话接口，通过 WebSocket 协议实现低延迟的语音、文本与图像交互。它支持语音活动检测（VAD）自动判别语音起止，也支持手动模式（Manual）由客户端控制发送节奏，适用于智能客服、语音助手、音视频对话等场景。

## 支持的模型

当前支持三类 Qwen-Omni 实时模型，它们在参数默认值与功能支持上有所差异：

| 模型系列 | 默认音色 | temperature 默认值 | 联网搜索 / 工具调用 | 备注 |
| --- | --- | --- | --- | --- |
| Qwen3.5-Omni-Realtime（含 plus / flash） | Tina | 0.7 | 支持 | 支持 `semantic_vad`、`idle_timeout_ms` 等新特性 |
| Qwen3-Omni-Flash-Realtime | Cherry | 0.9 | 不支持 | 支持 `smooth_output` 控制口语化/书面化风格 |
| Qwen-Omni-Turbo-Realtime | Chelsie | 1.0 | 不支持 | `temperature` / `top_p` / `top_k` / `max_tokens` / `seed` 等参数**不支持修改** |

语音转录统一使用内置的 `qwen3-asr-flash-realtime` 模型，不可修改。

## 交互模式

API 提供两种交互模式，在 `session.update` 时通过 `turn_detection` 配置切换。详细的事件时序参见[实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)。

### VAD 模式（默认）

`turn_detection.type` 设为 `server_vad` 或 `semantic_vad`。服务端持续接收客户端通过 `input_audio_buffer.append` 发来的音频流，自动检测语音起止并提交缓冲区、触发模型响应。

- `server_vad`：基于声学特征检测语音结束，所有实时模型均支持。
- `semantic_vad`：基于语义有效性检测语音结束，可过滤"嗯/啊"等回应语和背景噪音，仅 Qwen3.5-Omni-Realtime 支持。

关键 VAD 参数：

| 参数 | 取值范围 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `threshold` | [-1.0, 1.0] | 0.5 | 越接近 -1 越灵敏，嘈杂环境建议调高 |
| `silence_duration_ms` | [200, 6000] | 800 | 静音持续多久后触发响应，越小响应越快但易误触 |
| `idle_timeout_ms` | [5000, 30000] | — | 播报完毕后用户持续静默多久模型主动引导对话，仅 `qwen3.5-omni-plus/flash-realtime` + `server_vad` 生效 |

### Manual 模式

`turn_detection` 设为 `null`。客户端显式调用 `input_audio_buffer.commit` 提交音频，再发 `response.create` 触发模型响应，适合"按下即说"类的聊天场景。

## 音频与图像输入输出

- 输入音频：16 kHz 单声道 PCM，通过 `input_audio_buffer.append` 以 Base64 分片发送。
- 输出音频：24 kHz 单声道 PCM，通过 `response.audio.delta` 流式返回，**当前不支持自定义输出采样率**。
- 图像输入（可选）：通过 `input_image_buffer.append` 发送 JPG/JPEG，建议 480p/720p、最高 1080p，单张 Base64 编码后不超过 256KB（建议原始 < 190KB），发送频率约 1 帧/秒。发送图像事件前需至少发送过一次音频 append。图像与音频共用 `input_audio_buffer.commit` 提交。

## 客户端事件

客户端通过 WebSocket 发送 JSON 事件驱动会话。完整字段参见[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。主要事件：

| 事件 | 作用 |
| --- | --- |
| `session.update` | 建立连接后更新会话配置（modalities、voice、instructions、VAD、tools 等） |
| `input_audio_buffer.append` | 追加 Base64 音频片段到输入缓冲区 |
| `input_image_buffer.append` | 追加 Base64 图像到图像缓冲区 |
| `input_audio_buffer.commit` | 提交音/图像缓冲区，创建用户消息项（不直接触发响应） |
| `input_audio_buffer.clear` | 清空缓冲区 |
| `response.create` | 指示服务端生成响应；Manual 模式或工具调用回传结果后使用 |
| `response.cancel` | 取消正在进行的响应 |
| `conversation.item.create` | 回传工具调用结果（`type: function_call_output`） |

## 服务端事件

服务端通过 WebSocket 下行事件通知会话状态与[流式输出](../concepts/streaming-output.md)。详见[服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)。关键事件：

| 事件 | 作用 |
| --- | --- |
| `session.created` / `session.updated` | 连接成功返回默认配置 / 配置更新成功 |
| `error` | 参数校验失败等错误，含 `type` / `code` / `message` / `param` |
| `input_audio_buffer.speech_started` / `speech_stopped` | VAD 检测到语音起止 |
| `input_audio_buffer.committed` / `cleared` | 缓冲区提交或清空确认 |
| `conversation.item.created` | 对话项创建（用户消息或 assistant 工具调用） |
| `conversation.item.input_audio_transcription.delta` / `.completed` | 输入音频实时转录中间结果与最终结果；`delta` 中 `text` 为已确认前缀、`stash` 为草稿后缀，预览需拼接 |
| `response.audio.delta` / `response.text.delta` | 模型[流式输出](../concepts/streaming-output.md)的音频/文本增量 |
| `response.audio_transcript.delta` / `.done` | 模型音频输出的转录增量与完成 |
| `response.function_call_arguments.delta` / `.done` | 工具调用参数的增量与完成 |
| `response.done` | 单次响应结束 |

## 关键生成参数

以下参数在 `session.update` 中配置。注意 Qwen-Omni-Turbo-Realtime 系列除 `modalities`、`voice`、`instructions` 等基础项外，**多数生成参数不支持修改**。

| 参数 | 取值范围 | 说明 |
| --- | --- | --- |
| `modalities` | `["text"]` 或 `["text","audio"]` | 输出模态，默认同时输出文本和音频 |
| `voice` | 字符串 | 音色名，可用声音复刻生成的自定义音色 |
| `instructions` | 字符串 | 系统消息 / 角色设定 |
| `temperature` | [0, 2) | 与 `top_p` 建议只设其一 |
| `top_p` | (0, 1.0] | 核采样阈值 |
| `top_k` | ≥ 0 | 设 null 或 > 100 时禁用，仅 `top_p` 生效 |
| `max_tokens` | 正整数 | 不影响生成过程，超出则截断响应 |
| `repetition_penalty` | > 0 | 连续序列重复惩罚，1.0 表示不惩罚 |
| `presence_penalty` | [-2.0, 2.0] | 正数降重复、负数增重复 |
| `seed` | [0, 2³¹−1] | -1 为不固定；相同 seed + 相同参数可复现结果 |
| `enable_search` | bool | 仅 Qwen3.5-Omni-Realtime 生效，启用联网搜索 |
| `search_options.enable_source` | bool | 启用后在响应中返回搜索来源列表 |
| `tools` | 数组 | 仅 Qwen3.5-Omni-Realtime 生效，**与 `enable_search` 互斥**；命中工具调用时模型不生成音频，仅返回参数 |

## SDK 调用

DashScope 提供 Python 与 Java 两套 SDK，核心类均为 `OmniRealtimeConversation`，通过回调接口接收服务端事件。

**Python SDK**（`dashscope >= 1.25.17`）：
- 构造：`OmniRealtimeConversation(model=..., callback=..., url=...)`
- 主要方法：`connect` / `update_session` / `append_audio` / `append_video` / `clear_appended_audio` / `commit` / `create_response` / `cancel_response` / `create_item` / `close` / `get_session_id` / `get_last_response_id`
- 回调类 `OmniRealtimeCallback` 需实现 `on_open` / `on_event` / `on_close`，在 `on_event` 中按 `type` 分支处理音频、转录、工具调用等事件。

**Java SDK**（`dashscope >= 2.22.15`）：
- 通过 `OmniRealtimeParam` 配置连接，通过 `OmniRealtimeConfig.builder()` 配置会话。
- 方法名与 Python 一一对应（`connect` / `updateSession` / `appendAudio` / `appendVideo` / `clearAppendedAudio` / `commit` / `createResponse` / `cancelResponse` / `createItem` / `close`）。
- `instructions`、`smooth_output`、`enable_search`、`search_options`、`temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed` 等参数需通过 `OmniRealtimeConfig` 的 `parameters(Map.of(...))` 传入。

调用地址：
- 北京：`wss://dashscope.aliyuncs.com/api-ws/v1/realtime`
- 新加坡：`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime`（旧版 `dashscope-intl.aliyuncs.com` 即将下线）

更多代码示例参见 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 与 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)。

## 声音复刻

Qwen-Omni-Realtime 支持通过少量音频（10~20 秒）免训练复刻音色，复刻后在实时对话中作为 `voice` 传入即可。关键约束：

- 复刻模型固定为 `qwen-voice-enrollment`，创建时必须指定 `target_model`（可选 `qwen3.5-omni-plus-realtime` / `qwen3.5-omni-flash-realtime` / `qwen3.5-omni-plus` / `qwen3.5-omni-flash`）。
- 后续调用 Omni 接口时使用的模型必须与 `target_model` 一致，否则合成失败。
- 音频要求：WAV(16bit)/MP3/M4A，时长 10~20 秒（≤60 秒），< 10MB，采样率 ≥ 24kHz，单声道；至少 3 秒清晰朗读，避免背景噪音与歌曲；支持 28 种语言及 10 种中文方言。
- 接口为 REST（`POST /api/v1/services/audio/tts/customization`，`action=create`），返回的 `voice` 字段即为后续对话使用的音色 ID。

实现细节与端到端代码参见[声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。

## 工具调用（Function Calling）

仅 Qwen3.5-Omni-Realtime 支持。在 `session.update` 的 `tools` 中声明函数（`type: function`，含 `name` / `description` / `parameters`），模型会在合适时机自主触发。流程要点：

1. 模型决定调用工具时，不生成音频，仅通过 `response.function_call_arguments.delta` / `.done` 下发参数。
2. 客户端在本地执行函数后，通过 `conversation.item.create`（`type: function_call_output`，带 `call_id` 与 `output`）回传结果。
3. VAD 模式下服务端会自动基于结果继续生成响应；Manual 模式下需客户端再发 `response.create` 触发。

> **注意**：`tools` 与 `enable_search` 互斥，不可同时开启。

## 限制与注意事项

- 输出音频采样率固定为 24 kHz PCM，**不支持自定义**。
- Qwen-Omni-Turbo-Realtime 系列**不支持修改** `temperature` / `top_p` / `top_k` / `max_tokens` / `repetition_penalty` / `presence_penalty` / `seed` 等生成参数。
- `smooth_output` 仅在 Qwen3-Omni-Flash-Realtime 生效。
- `enable_search` 与 `tools` 仅在 Qwen3.5-Omni-Realtime 生效，且二者**互斥**。
- `semantic_vad` 与 `idle_timeout_ms` 仅在 Qwen3.5-Omni-Realtime + `server_vad` 下可用。
- 图像输入前必须至少发送过一次 `input_audio_buffer.append`；单张 Base64 后 ≤ 256KB。
- `max_tokens` 不控制生成过程，仅在超出时截断响应。
- 语音转录使用的是与主模型独立的 ASR 模型，转录文本与主模型理解可能存在差异，仅供参考。
- 新加坡地域旧版域名 `dashscope-intl.aliyuncs.com` 即将下线，需迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)




