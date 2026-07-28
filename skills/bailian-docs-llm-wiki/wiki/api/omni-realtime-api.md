# omni realtime api

Qwen-Omni-Realtime API 是百炼平台基于 WebSocket 的实时[多模态](../concepts/multimodal.md)对话接口，支持音频、图像（视频帧）与文本的流式输入输出，适用于语音助手、音视频客服、实时同传等场景。本页汇总其支持的模型、交互模式、事件协议、SDK 用法与声音复刻能力。

## 支持的模型与功能

- **模型系列**：`qwen3.5-omni-realtime` 系列（含 `qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`）、`qwen3-omni-flash-realtime`、`qwen-omni-turbo-realtime`。
- **输出模态**：`["text"]` 仅文本，或 `["text","audio"]`（默认）文本+音频。
- **默认音色**：Qwen3.5 系列为 `Tina`，Qwen3-Omni-Flash 为 `Cherry`，Qwen-Omni-Turbo 为 `Chelsie`；音色列表见实时文档。
- **音频格式**：输入仅支持 16 kHz PCM，输出仅支持 24 kHz PCM，不支持自定义输出采样率。
- **图像输入**：JPG/JPEG，建议 480p/720p（最高 1080p），Base64 编码后 ≤256KB，建议 1 张/秒，且须在发送过音频之后再发图像。
- **能力差异**：
  - `semantic_vad`、联网搜索（`enable_search`）、工具调用（`tools`）仅 Qwen3.5-Omni-Realtime 系列支持；
  - `idle_timeout_ms`（静默超时后模型主动引导对话，范围 [5000, 30000]）仅 `qwen3.5-omni-plus/flash-realtime` + `server_vad` 生效；
  - `smooth_output`（口语化/书面化风格）仅 Qwen3-Omni-Flash-Realtime 支持；
  - `qwen-omni-turbo` 系列**不支持修改** temperature / top_p / top_k / max_tokens / repetition_penalty / presence_penalty / seed 等采样参数。

> **注意**：`tools` 与 `enable_search` 不兼容，不可同时开启。

## 交互流程

详见[实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)。

- **VAD 模式**（默认，`turn_detection.type = "server_vad"`）：服务端自动检测语音起止、自动提交缓冲区并生成响应，支持语音打断。事件序列：`speech_started` → `speech_stopped` → `input_audio_buffer.committed` → `conversation.item.created` → 响应事件。
- **Manual 模式**（`turn_detection = null`）：客户端显式发送 `input_audio_buffer.commit` 提交音频，再发 `response.create` 触发响应，适用于"按下即说"场景。
- **工具调用**：服务端通过 `response.function_call_arguments.delta/done` 下发调用参数（含 `call_id`）→ 客户端本地执行 → 通过 `conversation.item.create`（type 为 `function_call_output`）回传结果 → VAD 模式下服务端自动生成最终响应，Manual 模式需客户端再发 `response.create`。命中工具调用时模型不生成音频，仅返回参数。

## 事件协议

### 客户端事件

完整字段定义见[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)：

| 事件 | 说明 |
| --- | --- |
| `session.update` | 更新会话配置（modalities、voice、instructions、turn_detection、tools、enable_search、采样参数等） |
| `response.create` | 触发模型生成响应（VAD 模式下通常无需发送） |
| `response.cancel` | 取消进行中的响应 |
| `input_audio_buffer.append` | 追加 Base64 音频到缓冲区 |
| `input_audio_buffer.commit` | 提交缓冲区创建用户消息项（Manual 模式必需；同时提交图像缓冲区） |
| `input_audio_buffer.clear` | 清空音频缓冲区 |
| `input_image_buffer.append` | 追加 Base64 图像到缓冲区 |
| `conversation.item.create` | 回传工具执行结果（仅支持 `function_call_output` 类型） |

### 服务端事件

完整定义见[服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)，主要包括：

- **会话类**：`session.created`（连接后首个事件，含默认配置）、`session.updated`、`error`。
- **缓冲区类**：`input_audio_buffer.speech_started/speech_stopped/committed/cleared`。
- **对话项类**：`conversation.item.created`（type 为 `message` 或 `function_call`）。
- **输入转录类**：`conversation.item.input_audio_transcription.delta`（实时预览 = `text` + `stash`，附带 `language`、`emotion`）与 `.completed`；转录模型固定为 `qwen3-asr-flash-realtime`，转录结果仅供参考，可能与模型理解存在差异。
- **响应类**：`response.created`、`response.output_item.added`、`response.content_part.added`、`response.audio.delta`、`response.audio_transcript.delta/done`、`response.audio.done`、`response.content_part.done`、`response.output_item.done`、`response.done`，以及工具调用的 `response.function_call_arguments.delta/done`。

## 关键会话参数

- **turn_detection**：`server_vad`（默认）或 `semantic_vad`；`threshold` ∈ [-1.0, 1.0]（默认 0.5，越低越灵敏），`silence_duration_ms` ∈ [200, 6000]（默认 800）。设为 `null` 即 Manual 模式。
- **采样参数默认值**（temperature / top_p / top_k）：qwen3.5 系列 0.7 / 0.8 / 20；qwen3-omni-flash 0.9 / 1.0 / 50；qwen-omni-turbo 1.0 / 0.01 / 20。temperature 与 top_p 建议只设其一。
- **presence_penalty**：qwen3.5 系列默认 1.5，其他默认 0.0；范围 [-2.0, 2.0]。
- **max_tokens**：仅截断输出，不影响生成过程。
- **seed**：0 ~ 2³¹−1，默认 -1，用于结果复现。

## SDK 使用方式

- **Python SDK**（dashscope ≥ 1.25.17）：核心类 `OmniRealtimeConversation`，方法包括 `connect()`、`update_session()`、`append_audio()`、`append_video()`、`commit()`、`create_response()`、`cancel_response()`、`create_item()`、`close()`，服务端事件通过 `OmniRealtimeCallback` 回调下发。详见 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)。
- **Java SDK**（dashscope ≥ v2.22.15）：对应类 `OmniRealtimeConversation` + `OmniRealtimeParam` / `OmniRealtimeConfig`；注意 `instructions`、`smooth_output`、`enable_search`、`search_options`、`tools` 及采样参数需通过 `OmniRealtimeConfig.parameters` 传入。详见 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)。
- **接入地址**（WebSocket）：
  - 北京：`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`
  - 新加坡：`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime`

  官方建议从旧域名 `wss://dashscope.aliyuncs.com` / `wss://dashscope-intl.aliyuncs.com` 迁移至[业务空间](../concepts/workspace.md)专属域名（旧域名仍可用）。

## 声音复刻

通过 `qwen-voice-enrollment` 模型上传 10~20 秒音频（WAV 16bit / MP3 / M4A，≥24 kHz，单声道，<10 MB）即可免训练创建定制音色，随后在 Realtime 会话的 `voice` 参数中使用。详见[声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。

> **注意**：创建音色时的 `target_model` 必须与后续对话调用的模型一致（支持 qwen3.5-omni-plus/flash-realtime 及非实时 qwen3.5-omni-plus/flash），否则合成失败。

## 限制与注意事项

- 输入/输出音频格式均仅支持 PCM，采样率固定（输入 16 kHz、输出 24 kHz）。
- VAD 模式下推荐使用耳机播放，避免回声触发语音打断。
- 提交音频缓冲区（commit）本身不会触发模型响应。
- Manual 模式下 `append_audio` 单次最多 15 MiB。
- 联网搜索与工具调用互斥；`semantic_vad` 仅 qwen3.5 系列可用。
- qwen-omni-turbo 系列采样参数不可修改。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)





