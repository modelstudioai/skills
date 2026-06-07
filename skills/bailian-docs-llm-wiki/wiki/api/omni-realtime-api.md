# omni realtime api

Qwen-Omni-Realtime API 是百炼提供的实时多模态对话接口，基于 WebSocket 通道在客户端与服务端之间双向流式传输音频、图像与文本，并由模型实时返回音频/文本响应。本主题汇总了交互流程、客户端/服务端事件、SDK 调用、会话参数与声音复刻等开发者必须的 API 细节。

## 适用模型与端点

支持的 Qwen-Omni-Realtime 系列模型主要分为三组：

- `qwen3.5-omni-realtime` 系列（如 `qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`）：支持 `semantic_vad`、`enable_search`、`tools`，可修改全部采样参数。
- `qwen3-omni-flash-realtime` 系列：支持 `smooth_output` 控制口语化/书面化风格。
- `qwen-omni-turbo-realtime` 系列：默认参数固定，**不支持修改** `temperature` / `top_p` / `top_k` / `max_tokens` / `repetition_penalty` / `presence_penalty` / `seed`。

WebSocket 调用地址：

- 华北 2（北京）：`wss://dashscope.aliyuncs.com/api-ws/v1/realtime`
- 新加坡：`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime`

> **注意**：新加坡地域旧版域名 `https://dashscope-intl.aliyuncs.com` 即将下线，请迁移到带 `WorkspaceId` 的新版域名。新加坡与北京地域的 API Key 不同，不可混用。

## 交互流程：VAD 模式与 Manual 模式

通过 `session.turn_detection` 字段切换两种工作模式，完整时序图与事件顺序见 [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)。

| 维度 | VAD 模式（默认） | Manual 模式 |
| --- | --- | --- |
| `turn_detection` | `"server_vad"` 或 `"semantic_vad"` | `null` |
| 适用场景 | 持续推流、自由对话、支持语音打断 | 按下即说、本地音视频文件回放 |
| 触发响应 | 服务端检测到静音超阈值后自动生成响应 | 客户端显式发送 `input_audio_buffer.commit` + `response.create` |
| 工具调用回传后 | 服务端自动基于工具结果生成响应 | 客户端需再次发送 `response.create` 触发最终响应 |

`semantic_vad` 仅 `qwen3.5-omni-realtime` 支持，会过滤回应语和背景音；`server_vad` 通过 `threshold`（取值 `[-1.0, 1.0]`，默认 0.5）和 `silence_duration_ms`（`[200, 6000]`，默认 800）控制灵敏度。

## 客户端事件

完整字段定义和示例见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)，核心事件如下：

- `session.update`：建立连接后更新会话默认配置，参数非法时服务端返回 `error`，合法时返回完整配置。
- `response.create`：Manual 模式或工具回传后用来手动触发模型响应；VAD 模式由服务端自动触发。
- `response.cancel`：取消正在进行的响应；若无响应可取消，服务端返回错误事件。
- `input_audio_buffer.append`：将 Base64 编码的 PCM 音频片段追加到输入缓冲区。
- `input_audio_buffer.commit` / `input_audio_buffer.clear`：提交或清空缓冲区；VAD 模式下提交由服务端自动完成。
- `input_image_buffer.append`：将 Base64 JPG/JPEG 图像写入图像缓冲区；图像将随下一次 `input_audio_buffer.commit` 一起提交。
- `conversation.item.create`：仅用于回传 `function_call_output`，把工具执行结果送回服务端。

## 服务端事件

按生命周期可分为四类，详细字段见 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)：

- 会话/错误：`session.created`（连接建立后第一帧）、`session.updated`、`error`。
- 输入缓冲：`input_audio_buffer.speech_started` / `speech_stopped` / `committed` / `cleared`。
- 对话项与转录：`conversation.item.created`、`conversation.item.input_audio_transcription.delta` / `completed` / `failed`（ASR 由内置 `qwen3-asr-flash-realtime` 完成，不可修改）。
- 响应生成：`response.created` → `response.output_item.added` → `response.content_part.added` → 流式 `response.audio.delta` / `response.text.delta` / `response.audio_transcript.delta` → `*.done` 系列 → `response.done`。
- 工具调用：`response.function_call_arguments.delta` / `response.function_call_arguments.done`，由客户端基于其中的 `call_id` 在本地执行函数后通过 `conversation.item.create` 回传 `output`。

## 关键会话参数

| 参数 | 取值 / 默认 | 说明 |
| --- | --- | --- |
| `modalities` | `["text"]` 或 `["text","audio"]`（默认） | 输出模态。 |
| `voice` | 字符串 | 模型音色，默认 `Tina`（Qwen3.5）/ `Cherry`（Qwen3 Flash）/ `Chelsie`（Qwen-Omni-Turbo）。 |
| `input_audio_format` | 仅 `pcm` | 16 kHz、单声道、16bit PCM。 |
| `output_audio_format` | 仅 `pcm` | 24 kHz PCM，**不支持自定义采样率**。 |
| `smooth_output` | `true` / `false` / `null` | 仅 Qwen3-Omni-Flash-Realtime 生效，控制口语化/书面化。 |
| `enable_search` + `search_options.enable_source` | 默认关闭 | 仅 Qwen3.5-Omni-Realtime 支持；与 `tools` **互斥**，不能同时开启。 |
| `tools` | 函数描述数组 | 仅 Qwen3.5-Omni-Realtime 系列生效；命中工具调用时模型不输出音频，仅返回参数。 |
| `temperature` / `top_p` / `top_k` / `max_tokens` / `repetition_penalty` / `presence_penalty` / `seed` | 各模型默认值不同 | Qwen-Omni-Turbo 全部锁定；建议 `temperature` 与 `top_p` 只调其一。 |

## 图像与音视频输入限制

- 图片格式必须为 JPG/JPEG，推荐分辨率 480P 或 720P，**最大 1080P**。
- 单张图片 Base64 后 ≤ 256 KB（原图建议 ≤ 190 KB）。
- 至少先发送过一次 `input_audio_buffer.append` 后才允许追加图像。
- 推荐图像帧率 1～2 fps，音频按 100 ms 一包发送；Manual 模式下单事件音频量不超过 15 MiB。
- 图像缓冲区不能独立提交，必须跟随 `input_audio_buffer.commit` 一起提交。

## SDK 调用

### Python（DashScope）

详见 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)。版本需 `dashscope >= 1.25.17`。核心类是 `OmniRealtimeConversation`（从 `dashscope.audio.qwen_omni` 引入），常用方法：

- `connect()` / `close()`：建立与终止 WebSocket 连接。
- `update_session(...)`：在 `connect()` 之后立刻调用，传入 `output_modalities`、`voice`、`turn_detection_type`、`turn_detection_threshold`、`turn_detection_silence_duration_ms` 等参数。
- `append_audio(audio_b64)` / `append_video(video_b64)`：推送音频和图像。
- `commit()` / `clear_appended_audio()`：手动提交或清空缓冲区。
- `create_response(instructions=None, output_modalities=None)` / `cancel_response()`：Manual 模式下触发或取消响应。
- `create_item(item)`：回传 `function_call_output` 工具结果，`item` 需包含 `type`、`call_id`、`output`。
- `get_session_id()` / `get_last_response_id()`：会话与响应 ID 获取。

回调通过 `OmniRealtimeCallback` 实现 `on_open` / `on_event(message)` / `on_close(close_status_code, close_msg)` 三个方法。

### Java（DashScope）

详见 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)。SDK 版本需 `≥ v2.22.15`。配置流程：

1. 用 `OmniRealtimeParam` 链式方法配置 `model`、`url`、`apiKey`，构造 `OmniRealtimeConversation`。
2. `connect()` 后调用 `updateSession(OmniRealtimeConfig)`；`instructions` 通过 `OmniRealtimeConfig.parameters(Map.of(...))` 传入。
3. 推流：`appendAudio(String audioBase64)` / `appendVideo(String videoBase64)`。
4. Manual 模式：`commit()` → `createResponse(instructions, modalities)`；打断使用 `cancelResponse()`。
5. 工具回传：`createItem(JsonObject item)`，字段同 Python。
6. 回调实现 `onOpen()` / `onEvent(JsonObject message)` / `onClose(int code, String reason)`。

> **注意**：Python 文档使用 `output_modalities` + `MultiModality` 枚举，Java 文档对应字段为 `modalities` + `OmniRealtimeModality` 枚举；同时 Python 的 `cancel_response` 与 Java 的 `cancelResponse` 在原生事件层面均映射为 `response.cancel`，但 Java 文档 FAQ 中曾把它称为 `response_cancel`，以代码方法名为准。

## 声音复刻（关联 API）

[声音复刻 API 参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md) 通过 `qwen-voice-enrollment` 模型把 10～20 秒的样本音频复刻为专属音色，再由 Omni 模型作为 `voice` 参数使用。要点：

- HTTP 端点：`POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization`（新加坡地域换成 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`）。
- 支持 `action`：`create`（必传 `target_model`、`preferred_name`、`audio.data`，`audio.data` 为 `data:<mime>;base64,<...>` 形式）、`list`、`delete`。
- 创建音色时指定的 `target_model` 必须与后续 Omni 对话使用的模型一致，否则合成失败。可选 `target_model` 包括 `qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3.5-omni-plus`、`qwen3.5-omni-flash`。
- 音频要求：WAV(16bit) / MP3 / M4A，≥ 24 kHz、单声道、≤ 10 MB、含至少 3 秒连续清晰朗读。
- 配额：每账号 1000 个音色；超过 1 年未使用自动清理。
- 计费：创建按 0.01 元/个（失败不计费、删除不计费、删除不返还免费额度）；北京/新加坡地域开通后 90 天内首 1000 次免费。

## 限制与常见注意事项

- 输入音频固定为 16 kHz PCM；输出固定为 24 kHz PCM，不支持自定义。
- `tools` 与 `enable_search` **互斥**，不能在同一会话中同时启用。
- ASR 转录模型固定为 `qwen3-asr-flash-realtime`，不可修改；Omni 不会直接输出输入音频的转录文本，需通过 `conversation.item.input_audio_transcription.completed` 事件获取。
- VAD 模式下也可随时通过 `response.create` / `response.cancel` 主动触发或打断响应。
- 推荐使用耳机播放模型音频，避免回声导致 VAD 误触发打断。
- 出现接口报错时通过事件 `error` 中的 `error.code` / `error.param` 排查（如 `invalid_value` + `session.modalities`）。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)



