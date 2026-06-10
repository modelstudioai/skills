# 语音合成 API 参考

阿里云百炼平台提供多套语音合成（TTS）模型，涵盖非实时合成、实时流式合成与声音复刻三大类场景。本文汇总 Qwen-TTS、CosyVoice、Sambert、MiniMax 四大模型家族的 API 调用方式、关键参数、地域端点与 SDK 支持情况，供开发者按场景选型与接入。

## 模型家族总览

| 模型系列 | 适用场景 | 协议 | 地域 | 典型模型 |
| --- | --- | --- | --- | --- |
| Qwen-TTS（非实时） | 离线 / 批量合成 | HTTP | 北京、新加坡 | `qwen3-tts-flash`、`qwen3-tts-instruct-flash` |
| Qwen-TTS Realtime | 实时对话、低延迟 | WebSocket | 北京、新加坡 | `qwen3-tts-flash-realtime` |
| CosyVoice | 实时流式、高表现力 | WebSocket | 北京、新加坡 | `cosyvoice-v3-plus`、`cosyvoice-v3.5-plus` 等 |
| Sambert | 实时、多音色、多端 | WebSocket | 仅北京 | `sambert-zhichu-v1` 等 |
| MiniMax Speech | 同步 / 流式 HTTP | HTTP | 北京 | `MiniMax/speech-2.8-hd`、`MiniMax/speech-02-turbo` 等 |

Qwen-TTS 系列侧重自然度与指令控制（`instruct` 模型可通过 `instructions` 字段描述语速、语调、情绪）；CosyVoice 侧重情感与韵律表现；Sambert 是传统的拼接 + 神经网络混合引擎，音色库丰富且支持移动端 SDK；MiniMax 模型提供兼容 OpenAI 风格的 HTTP 接口，支持情绪标签（如 `(laughs)`、`(happy)`）与自定义词典。

## 通用鉴权与端点

所有 API 统一使用 DashScope 鉴权体系：

- HTTP 请求：`Authorization: Bearer <your_api_key>`
- WebSocket 请求：握手阶段在 Header 中携带 `Authorization: Bearer <your_api_key>`，无效 Key 会返回 HTTP 401/403

各地域端点（[CosyVoice WebSocket API参考](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-websocket-api.md)）：

| 地域 | HTTP base URL | WebSocket URL |
| --- | --- | --- |
| 华北 2（北京） | `https://dashscope.aliyuncs.com/api/v1` | `wss://dashscope.aliyuncs.com/api-ws/v1/inference` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1` | `wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference` |

> **注意**：新加坡地域旧版域名 `dashscope-intl.aliyuncs.com` 即将下线，请迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com` 的新域名。Qwen-TTS Realtime 的 WebSocket 端点路径不同，需通过查询参数 `?model=qwen3-tts-flash-realtime` 指定模型（[Qwen-TTS-Realtime WebSocket API 参考](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-realtime-api-reference/interactive-process-of-qwen-tts-realtime-synthesis.md)）。

可选 Header：

- `user-agent`：客户端标识
- `X-DashScope-WorkSpace`：[业务空间](../concepts/workspace.md) ID
- `X-DashScope-DataInspection`：数据合规检测（默认不启用，勿随意开启）

## Qwen-TTS（非实时）

通过 HTTP 调用 `MultiModalConversation.call` 接口，支持流式与非流式两种输出模式。

请求体关键字段：

- `model`：`qwen3-tts-flash` 或 `qwen3-tts-instruct-flash`（支持指令控制）
- `input.text`：待合成文本
- `input.voice`：音色，如 `Cherry`
- `input.language_type`：语言（如 `Chinese`、`English`）
- `instructions` + `optimize_instructions`：仅在 instruct 模型下生效，用自然语言描述语速、语调、情绪

> **注意**：原 DashScope Python SDK 中的 `SpeechSynthesizer` 接口已统一为 `MultiModalConversation`，参数保持兼容（[非实时语音合成（Qwen-TTS）API参考](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-api.md)）。

## Qwen-TTS Realtime（实时流式）

基于 WebSocket，提供两种工作模式：

- **ServerCommit 模式**：服务端智能判断文本分段时机，开发者只需调用 `input_text_buffer.append` 追加文本；如需立即合成可手动 `commit`。
- **Commit 模式**：客户端必须显式调用 `input_text_buffer.commit` 才会触发合成，适合精确控制节奏的场景。

关键流程：`session.created` → `session.update`（配置音色、格式、模式）→ 多次 `input_text_buffer.append` → `response.created` + 分片 `response.audio.delta`（base64）→ `response.audio.done` → `session.finish` → `session.finished`。

支持的参数包括 `voice`、`response_format`（`pcm` 等）、`sample_rate`（默认 24000）。

## CosyVoice（WebSocket 流式）

采用"run-task → continue-task → finish-task"三段式事件协议，客户端与服务端通过 JSON 事件交互（[CosyVoice服务端事件](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-server-events.md)）：

1. 客户端发送 `run-task`，服务端回 `task-started`。
2. 客户端分片发送 `continue-task`（携带 `text`），服务端自动分句，完整语句立即返回 `result-generated` + 音频流；不完整语句缓存至完整。
3. 客户端发送 `finish-task`，服务端强制合成所有缓存内容并回 `task-finished`。

音频通过 WebSocket 的 `binary` 通道接收。同一次合成任务中 `run-task`、所有 `continue-task`、`finish-task` 必须使用相同的 `task_id`（建议 UUID），不同任务之间使用新 `task_id`。

> **注意**：建议复用 WebSocket 连接处理多个任务，避免每次任务都重新握手。

## Sambert（WebSocket 仅北京）

Sambert 与 CosyVoice 类似但**不支持流式输入**：必须在 `run-task` 事件中一次性发送完整文本，不支持 `continue-task` / `finish-task`。

`run-task` 中可配置的参数：

| 参数 | 类型 | 默认 | 取值范围 | 说明 |
| --- | --- | --- | --- | --- |
| `model` | string | — | 如 `sambert-zhichu-v1` | 模型 + 音色 |
| `parameters.format` | string | `wav` | `pcm` / `wav` / `mp3` | 音频编码 |
| `parameters.sample_rate` | integer | 16000 | 8000 / 16000 / 22050 / 24000 | 采样率 |
| `parameters.volume` | integer | 50 | [0, 100] | 音量 |
| `parameters.rate` | float | 1.0 | [0.5, 2.0] | 语速 |
| `parameters.pitch` | float | 1.0 | [0.5, 2.0] | 音调 |
| `parameters.word_timestamp_enabled` | boolean | false | — | 字级时间戳 |
| `parameters.phoneme_timestamp_enabled` | boolean | false | — | 音素时间戳（需先开启字级） |

服务端事件会按 `sentence-begin` / `sentence-synthesis` / `sentence-end` 分阶段上报，`sentence-end` 中包含 `words` 字级别时间信息与 `usage.characters` 计费字符数。

Sambert 提供 Java、Python、Android、iOS 多端 SDK，可直接调用而无须自行维护 WebSocket 状态。

## MiniMax Speech（HTTP 同步 / 流式）

请求体结构（[MiniMax同步语音合成API参考](../../raw/model-api-reference/speech-synthesis-api-reference/minimax-speech-synthesis/minimax-synchronous-speech-synthesis-api.md)）：

```json
{
  "model": "MiniMax/speech-2.8-hd",
  "input": {
    "text": "今天是不是很开心呀(laughs)，当然了！",
    "voice_setting": {
      "voice_id": "male-qn-qingse",
      "speed": 1, "vol": 1, "pitch": 0, "emotion": "happy"
    },
    "audio_setting": {
      "sample_rate": 32000, "bitrate": 128000,
      "format": "mp3", "channel": 1
    },
    "pronunciation_dict": { "tone": ["处理/(chu3)(li3)"] },
    "subtitle_enable": false
  }
}
```

- 文本长度 < 10000 字符，> 3000 字符建议开启流式（请求头 `X-DashScope-SSE: enable`）。
- 流式模式下 `stream_options.exclude_aggregated_audio=true` 可让结束帧不返回完整音频，减少尾包体积，适合边收边播场景。
- 支持在文本中插入情绪标签（如 `(laughs)`）或在 `voice_setting.emotion` 指定整体情绪。
- 单价：`hd` 系列 3.5 元 / 万字符，`turbo` 系列 2 元 / 万字符。

## 声音复刻（Voice Clone）

百炼提供 CosyVoice 与 Qwen 两套声音复刻方案，均通过 HTTP API 管理音色生命周期（创建 / 列表 / 查询 / 更新 / 删除），复刻得到的 `voice_id` 可直接传入对应系列的合成 API 使用。

**CosyVoice 复刻**（`model=voice-enrollment`）：

- `input.action = create_voice`
- `input.target_model` 必须与后续合成使用的模型一致
- `input.url`：公网可访问的样本音频 URL
- `input.prefix`：音色名前缀（≤10 字符，字母数字），生成的音色名格式 `{target_model}-{prefix}-{唯一标识}`
- `input.language_hints`：提示语种（如 `["zh"]`、`["en"]`），仅 v3/v3.5 系列支持
- `input.max_prompt_audio_length`：预处理后参考音频最大秒数，[3.0, 30.0]，默认 10.0
- `input.enable_preprocess`：有背景噪音时建议开启

**Qwen 复刻**（`model=qwen-voice-enrollment`）：

- `input.action = create`
- `input.audio`：支持 Data URL（base64）或公网音频 URL
- `input.text`：可选，音频对应文本，可提升复刻质量
- `input.preferred_name`：≤16 字符，字母数字加下划线

**MiniMax 复刻**：端点与合成接口相同，参考 MiniMax 专属文档。

> **注意**：音色 ID 需妥善保管；每次 `create_voice` 都会创建新音色，达到配额上限后无法继续创建，避免频繁调用。

## SDK 与接入建议

- **Java / Python**：推荐直接使用 DashScope SDK，已封装 WebSocket 握手与事件循环。Sambert、CosyVoice、Qwen-TTS Realtime 均有对应 SDK 模块。
- **其他语言**：需自行实现 WebSocket 客户端，严格按"run-task → continue-task → finish-task"（或 Qwen Realtime 的 session/input_text_buffer 协议）推进状态。
- **移动端**：Sambert 提供 Android 与 iOS SDK，可离线或在线合成。
- **连接复用**：WebSocket 接口建议长连接复用，避免每个任务重新握手。
- **task_id 管理**：同一合成任务内所有事件必须共享 `task_id`；不同任务之间要使用新 ID。

## 限制与注意事项

- Sambert **仅支持北京地域**，不支持流式输入，文本必须在 `run-task` 一次性发送。
- Qwen-TTS Realtime 的 WebSocket 端点需要在 URL 上携带 `?model=...` 查询参数，与 CosyVoice / Sambert 端点不同。
- 所有新加坡地域的旧版 `dashscope-intl` 域名即将下线，请迁移到带 `WorkspaceId` 的新域名。
- 流式文本输入时，不完整语句会被服务端缓存，需发送 `finish-task` 强制合成剩余内容，否则会丢失尾部音频。
- 声音复刻得到的 `voice_id` 必须与 `target_model` 配套使用，跨模型合成会失败。
- 临时 API Key 有效期 60 秒，长任务请使用常规 API Key。

## 来源文档

- [非实时语音合成（Qwen-TTS）API参考](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-api.md)
- [CosyVoice WebSocket API参考](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-websocket-api.md)
- [CosyVoice服务端事件](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-server-events.md)
- [Sambert客户端事件](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-client-events.md)
- [Sambert WebSocket API 参考](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-websocket-api.md)
- [Sambert服务端事件](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-server-events.md)
- [语音合成Sambert Java SDK](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-java-sdk.md)
- [语音合成Sambert Android SDK](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-android-sdk.md)
- [语音合成Sambert Python SDK](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-python-sdk.md)
- [Qwen-TTS-Realtime WebSocket API 参考](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-realtime-api-reference/interactive-process-of-qwen-tts-realtime-synthesis.md)
- [语音合成Sambert iOS SDK](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-ios-sdk.md)
- [客户端事件](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-realtime-api-reference/qwen-tts-realtime-client-events.md)
- [服务端事件](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-realtime-api-reference/qwen-tts-realtime-server-events.md)
- [Python SDK](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-realtime-api-reference/qwen-tts-realtime-python-sdk.md)
- [Java SDK](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-realtime-api-reference/qwen-tts-realtime-java-sdk.md)
- [MiniMax同步语音合成API参考](../../raw/model-api-reference/speech-synthesis-api-reference/minimax-speech-synthesis/minimax-synchronous-speech-synthesis-api.md)
- [声音复刻HTTP API参考](../../raw/model-api-reference/speech-synthesis-api-reference/sound-reengraving/voice-clone-design-http-api.md)
- [声音复刻Python SDK参考](../../raw/model-api-reference/speech-synthesis-api-reference/sound-reengraving/voice-clone-design-python-sdk.md)



