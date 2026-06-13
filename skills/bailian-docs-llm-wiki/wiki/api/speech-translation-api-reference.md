# speech translation api reference

百炼平台提供两类音视频翻译 API：基于 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)的离线翻译模型 `qwen3-livetranslate-flash`，以及基于 WebSocket 的实时翻译 API `qwen3.5-livetranslate-flash-realtime`。前者适合对整段音视频进行异步翻译，后者适合直播、同声传译等低延迟场景。两类接口均支持多语种，可通过 [音视频翻译-通义千问 API 参考](../../raw/model-api-reference/speech-translation-api-reference/qwen3-livetranslate-flash-api.md) 查阅完整参数表。

## 支持的模型

| 模型 | 接口形态 | 说明 |
| --- | --- | --- |
| `qwen3-livetranslate-flash` | OpenAI 兼容 HTTP（流式） | 离线音视频翻译，输入整段音频/视频 URL |
| `qwen3-livetranslate-flash-2025-12-01` | 同上 | 快照版本 |
| `qwen3.5-livetranslate-flash-realtime` | WebSocket 事件协议 | 实时流式翻译，支持音频+可选视频帧 |
| `qwen3-livetranslate-flash-realtime` | WebSocket 事件协议 | 上一代实时翻译模型 |

## 离线翻译：[OpenAI 兼容接口](../concepts/openai-compatible-api.md)

### Endpoint

- 北京：`https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`
- 新加坡：`https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions`

> 两地 API Key 不通用，需分别申请。不支持 DashScope 原生接口。

### 关键参数

- `model`：必填，取值 `qwen3-livetranslate-flash` 或快照版本。
- `messages`：仅允许一条 `user` 消息，`content` 为数组，`type` 可选：
  - `input_audio`：需给出 `data`（URL 或 Base64）与 `format`（如 `wav`/`mp3`）；
  - `video_url`：需给出 `url`。
- `stream`：**必须为 `true`**，模型仅支持[流式输出](../concepts/streaming-output.md)。
- `modalities`：`["text"]` 或 `["text","audio"]`（默认前者）。
- `audio`：仅当输出含音频时生效，`voice` 为音色，`format` 仅支持 `wav`。
- `translation_options`（非 OpenAI 标准，Python SDK 需放入 `extra_body`）：
  - `source_lang`：源语种英文全称，省略则自动识别；
  - `target_lang`：目标语种英文全称（必填）。
- 采样相关：`temperature`（默认 0.000001）、`top_p`（0.8）、`top_k`（1）、`repetition_penalty`（1.05）。为保翻译质量不建议修改。

### 响应结构

流式返回 `chat.completion.chunk`，按 `delta` 内容分为三类：

1. **文本 chunk**：`delta.content` 为翻译文本片段。
2. **音频 chunk**：`delta.audio` 包含 `data`（Base64 增量音频）、`id`、`expires_at`。
3. **Usage chunk**：最后一个 chunk，需设置 `stream_options.include_usage=true`，含 `prompt_tokens`/`completion_tokens` 以及 `audio_tokens`/`text_tokens` 明细。

完整字段说明参见 [音视频翻译-通义千问 API 参考](../../raw/model-api-reference/speech-translation-api-reference/qwen3-livetranslate-flash-api.md)。

## 实时翻译：WebSocket 事件协议

实时 API 采用双向事件流，客户端事件与服务端事件命名风格参考 OpenAI Realtime API。接入流程：建立 WebSocket → 发送 `session.update` → 持续 `input_audio_buffer.append`（可选 `input_image_buffer.append`）→ 监听响应 → 发送 `session.finish`。

### 客户端事件

| 事件 | 作用 |
| --- | --- |
| `session.update` | 建连后首条消息，配置 modalities、voice、采样率、翻译语种、热词、ASR、声音复刻等 |
| `input_audio_buffer.append` | 追加 Base64 音频字节 |
| `input_image_buffer.append` | 追加 JPG/JPEG 图像（≤500KB，≤2 帧/秒，须先发过音频） |
| `session.finish` | 结束会话，等待 `session.finished` 后断连 |

`session.update` 的关键配置：

- `modalities`：`["text"]` 或 `["text","audio"]`（默认）。
- `voice`：预设音色；启用声音复刻时须设为 `default` 或预复刻音色 ID。
- `enable_voice_clone` + `voice_clone_options.frequency`：`once`（单人单次复刻）/ `always`（多人实时跟随）/ `never`（使用预复刻音色）。
- `input_audio_transcription.model`：设为 `qwen3-asr-flash-realtime` 可同时返回源语言 ASR 结果。
- `translation.language`：目标语种；`translation.corpus.phrases`：热词表，如 `{"人工智能": "Artificial Intelligence"}`。
- `input_audio_format`：`pcm`（默认）或 `opus`；`output_audio_format` 仅 `pcm`。

详见 [客户端事件](../../raw/model-api-reference/speech-translation-api-reference/live-translator-api/live-translator-client-events.md)。

### 服务端事件

| 事件 | 作用 |
| --- | --- |
| `session.created` | 建连后首条，返回默认配置 |
| `session.updated` | `session.update` 成功后回显完整配置 |
| `error` | 参数校验失败等错误 |
| `response.created` / `response.done` | 一次响应的开始与结束，`response.done` 携带 usage |
| `response.text.text` / `response.text.done` | 纯文本输出模态下的增量与完整文本（含 `stash` 临时片段） |
| `response.audio.delta` / `response.audio.done` | 音频输出模态下的 Base64 增量音频 |
| `response.audio_transcript.text` / `response.audio_transcript.done` | 输出音频对应的翻译文本流 |
| `conversation.item.input_audio_transcription.text` / `.completed` | 输入音频的 ASR 原文（流式 + 最终） |
| `session.finished` | 客户端 `session.finish` 处理完毕的最终信号 |

> **注意**：服务端 `session.created` 文档示例里 `input_audio_format`/`output_audio_format` 写为 `pcm16`/`pcm24`，而 `session.updated` 回显为 `pcm`/`pcm`；客户端配置项也只接受 `pcm` 或 `opus`。实际接入建议以 `pcm` 为准，不要被 `session.created` 示例值误导。

更多事件字段解释参见 [服务端事件](../../raw/model-api-reference/speech-translation-api-reference/live-translator-api/live-translator-server-events.md)。

## 使用建议与限制

- **必须流式调用**：离线模型 `stream` 只能为 `true`；实时模型本身就是流式事件协议。
- **语种拼写**：`source_lang` / `target_lang` / `translation.language` 均需填写**英文全称**（如 `chinese`、`english`），而非代码。
- **声音复刻约束**：`frequency=once|always` 时 `voice` 必须为 `default`；`frequency=never` 时须填预复刻音色 ID，混用会触发 `invalid_request_error`。
- **图像输入限制**（仅实时 API）：JPG/JPEG，建议 480p/720p（≤1080p），单张 ≤500KB，≤2 帧/秒，且必须先发过音频事件。
- **采样参数**：翻译场景下建议保持 `temperature`、`top_p`、`top_k`、`repetition_penalty` 默认值，调整会明显降低翻译质量。
- **Token 计费**：输入/输出都会区分 `text_tokens` 与 `audio_tokens`，音频 token 与时长相关。
- **地域差异**：北京与新加坡 endpoint 与 API Key 独立，跨地域调用需同时更换 base_url 与密钥。

## 来源文档

- [音视频翻译-通义千问 API 参考](../../raw/model-api-reference/speech-translation-api-reference/qwen3-livetranslate-flash-api.md)
- [客户端事件](../../raw/model-api-reference/speech-translation-api-reference/live-translator-api/live-translator-client-events.md)
- [服务端事件](../../raw/model-api-reference/speech-translation-api-reference/live-translator-api/live-translator-server-events.md)





