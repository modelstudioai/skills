# speech synthesis api reference

百炼平台的语音合成（TTS）API 覆盖 Qwen-TTS、CosyVoice、Sambert、MiniMax 四大模型族，提供**非实时 HTTP**、**实时 WebSocket** 两种交互形态，并配套**声音设计（Voice Design）**与**声音复刻（Voice Clone）**用于自定义音色。本主题聚合各模型族的请求/事件协议、关键参数、SDK 入口与限制说明，便于按场景选型与排错。

## 支持的模型族与交互形态

| 模型族 | 典型模型 ID | 交互形态 | 主要 SDK |
| --- | --- | --- | --- |
| Qwen-TTS（非实时） | `qwen3-tts-flash`、`qwen3-tts-instruct-flash` | HTTP（DashScope `MultiModalConversation`） | Python / Java |
| Qwen-TTS-Realtime | `qwen3-tts-flash-realtime` | WebSocket（客户端事件 + 服务端事件） | Python / Java |
| CosyVoice（实时/流式） | `cosyvoice-v1` / `v2` / `v3` / `v3-plus` / `v3.5` / `v3.5-plus` | WebSocket | Python / Java / Android / iOS |
| CosyVoice（非实时） | `cosyvoice-v3.5-plus` 等 | HTTP | Python / Java |
| Sambert | `sambert-zhichu-v1` 等多发音人 | WebSocket | Python / Java / Android / iOS |
| MiniMax | `MiniMax/speech-02-hd`、`speech-02-turbo`、`speech-2.8-hd`、`speech-2.8-turbo` | HTTP（同步） | HTTP only |
| Voice Design（声音设计） | `voice-enrollment`（CosyVoice）、`qwen-voice-design`（Qwen） | HTTP | HTTP |
| Voice Clone（声音复刻） | `voice-enrollment` | HTTP | Python / Java / HTTP |

> **注意**：Sambert 与早期 CosyVoice 系列属于 DashScope 经典 TTS 协议；Qwen-TTS / Qwen-TTS-Realtime 是新一代基于多模态对话的语音合成，二者请求体与字段命名不同，不可互换。新业务建议优先选 Qwen-TTS（非实时）或 Qwen-TTS-Realtime（低时延）。

## 服务端点

- **中国内地（华北 2 / 北京）**：HTTP `https://dashscope.aliyuncs.com`，WebSocket `wss://dashscope.aliyuncs.com/api-ws/v1/inference`
- **国际（新加坡）新版**：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
- **国际旧版**：`https://dashscope-intl.aliyuncs.com`

> **注意**：新加坡地域旧版域名 `dashscope-intl.aliyuncs.com` 即将下线，国际地域请尽快迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`，详见 [非实时语音合成（Qwen-TTS）API参考](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-api.md)。两个地域的 API Key 不通用，需分别申请。

## Qwen-TTS（非实时 HTTP）

入口：`dashscope.MultiModalConversation.call(...)`（Python）/ `MultiModalConversation` builder（Java）。关键参数：

- `model`：`qwen3-tts-flash` 或 `qwen3-tts-instruct-flash`（后者支持指令控制风格）。
- `text`：合成文本。
- `voice`：音色，如 `Cherry`。
- `instructions`（仅 `qwen3-tts-instruct-flash`）：自然语言风格指令，如"语速较快，带有明显的上扬语调"。
- `language_type` / `languageType`：语种提示。

返回为整段音频结果，适用于离线生成、消息播报等无强实时需求的场景。完整字段说明见 [非实时语音合成（Qwen-TTS）API参考](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-api.md)。

> **注意**：DashScope Python SDK 中原有的 `SpeechSynthesizer`（`dashscope.audio.qwen_tts.SpeechSynthesizer`）接口已统一为 `MultiModalConversation`，使用方法与参数保持一致；新代码请直接使用统一接口。

## Qwen-TTS-Realtime（WebSocket）

面向交互式场景的双向流式协议，包含**客户端事件**与**服务端事件**两类消息，建议参考：

- 协议概览：[Qwen-TTS-Realtime WebSocket API 参考](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-realtime-api-reference/interactive-process-of-qwen-tts-realtime-synthesis.md)
- 客户端事件（如 `session.update`、`response.create`、`input_text.append`）：见 `qwen-tts-realtime-client-events`
- 服务端事件（如 `response.audio.delta`、`response.done`、`error`）：见 `qwen-tts-realtime-server-events`
- SDK：`qwen-tts-realtime-python-sdk` / `qwen-tts-realtime-java-sdk`

典型流程：建立 WebSocket → 发送 `session.update` 配置 voice/format → 多轮 `input_text.append` + `response.create` → 持续接收 `response.audio.delta` 拼接 PCM/Opus 音频 → `response.done` 标志一轮结束。

## CosyVoice（实时 WebSocket）

CosyVoice 大模型支持流式低延迟合成，通过统一的 `wss://.../api-ws/v1/inference` 入口接入。完整事件契约见 [CosyVoice WebSocket API参考](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-websocket-api.md)，配套：

- 客户端事件：`cosyvoice-client-events`（`run-task` / `continue-task` / `finish-task`）。
- 服务端事件：`cosyvoice-server-events`（`task-started` / `result-generated` / `task-finished` / `task-failed`）。
- SDK：Python / Java / Android / iOS 四端均提供官方封装。

关键参数：

- `model`：`cosyvoice-v1`、`cosyvoice-v2`、`cosyvoice-v3`、`cosyvoice-v3-plus`、`cosyvoice-v3.5`、`cosyvoice-v3.5-plus`（版本越新音质/稳定性越好，部分新功能仅在 v3+ 提供）。
- `voice`：内置音色 ID，或通过声音复刻得到的自定义音色。
- `format`：`wav` / `mp3` / `pcm` / `opus` 等；`opus` 支持额外比特率参数。
- `sample_rate`：常用 `22050` / `24000` / `48000`。

## CosyVoice（非实时 HTTP）

无需建立 WebSocket，适合一次性合成长文本。请求/响应字段、批处理与错误码见 [非实时语音合成CosyVoice HTTP API参考](../../raw/model-api-reference/speech-synthesis-api-reference/non-realtime-cosyvoice-api/cosyvoice-tts-http-api.md)，对应 SDK 入口为 `cosyvoice-tts-java-sdk` / `cosyvoice-tts-python-sdk`。

## Sambert（WebSocket）

Sambert 是 DashScope 经典 TTS，按发音人提供多模型（如 `sambert-zhichu-v1` 等），协议入口见 [Sambert WebSocket API 参考](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-websocket-api.md)，配套：

- 客户端 / 服务端事件：`sambert-client-events` / `sambert-server-events`，沿用 DashScope `run-task` / `result-generated` 等标准事件。
- SDK：Python / Java / Android / iOS。

关键参数：`format`（Python SDK 使用 `AudioFormat`，如 `AudioFormat.MP3_22050HZ_MONO_256KBPS`）、`sample_rate`、`volume`、`rate`、`pitch`。

> **注意**：Sambert 与 CosyVoice 虽然都走 WebSocket，但**模型 ID 与可用音色不互通**；切换模型族时需要同步替换 `model`、`voice` 及对应的 SDK 类名。

## MiniMax（同步 HTTP）

平台代理的 MiniMax 语音合成，仅提供同步 HTTP 接口。字段定义见 [MiniMax同步语音合成API参考](../../raw/model-api-reference/speech-synthesis-api-reference/minimax-speech-synthesis/minimax-synchronous-speech-synthesis-api.md)。

- 模型：`MiniMax/speech-02-hd`、`MiniMax/speech-02-turbo`、`MiniMax/speech-2.8-hd`、`MiniMax/speech-2.8-turbo`（hd 偏音质、turbo 偏速度）。
- `Content-Type` 固定为 `application/json; charset=utf-8`。
- 单次请求长度、并发上限以 MiniMax 计费规则为准，超长文本需自行分片。

## 声音设计（Voice Design）

通过自然语言描述（`voice_prompt`）+ 预览文本（`preview_text`）创建专属音色，分两条路径：

- **CosyVoice 路径**：`model="voice-enrollment"`，`action="create_voice"`，`target_model` 指定 `cosyvoice-v3.5-plus` 等。
- **Qwen 路径**：`model="qwen-voice-design"`，`action="create"`，`target_model` 指定 `qwen3-tts-vd-realtime-*`。

请求体、列表查询、删除等完整操作见 [声音设计API参考](../../raw/model-api-reference/speech-synthesis-api-reference/voice-design-api-references.md)。常用参数：`prefix` / `preferred_name`（音色前缀，最大长度受限）、`language_hints` / `language`、`sample_rate`、`response_format`。

## 声音复刻（Voice Clone）

基于音频样本克隆现实音色，统一走 `voice-enrollment` 模型，可用 [声音复刻HTTP API参考](../../raw/model-api-reference/speech-synthesis-api-reference/sound-reengraving/voice-clone-design-http-api.md) 直接调用，也可使用 `voice-clone-design-python-sdk` / `voice-clone-design-java-sdk` 封装。操作包括创建、查询列表、查询详情、删除音色，鉴权同样使用 `Authorization: Bearer <API Key>`。

## 通用参数与约定

- **鉴权**：所有接口均使用 `Authorization: Bearer <DASHSCOPE_API_KEY>`；推荐通过 `DASHSCOPE_API_KEY` 环境变量注入，避免硬编码。
- **音频格式**：跨模型族通用键为 `format`（或 SDK 中的 `AudioFormat` 枚举）；`opus` 模式下方可使用比特率/码率类参数，其他格式忽略。
- **采样率 `sample_rate`**：常见可选 `16000` / `22050` / `24000` / `48000`；建议与下游播放/存储链路一致以避免重采样开销。
- **音色 `voice`**：内置音色 ID 因模型族而异；自定义音色需先经声音设计或声音复刻生成。
- **错误处理**：HTTP 接口看响应 `code` / `message`；WebSocket 接口监听 `task-failed` 或 `error` 事件，错误信息位于事件 payload。

## 限制与注意事项

- 不同模型族的字段命名、事件名、SDK 类名不可混用；新接入请优先看本主题对应小节的"原文标题"链接，避免按旧 demo 拼接出已废弃的字段。
- 实时 WebSocket 接口需要稳定的长连接与有序事件处理，强烈建议使用官方 SDK 而非自行实现协议。
- 跨地域使用时，API Key、Endpoint、可用模型列表三者必须配套，新加坡地域请使用新版 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com` 域名。
- 声音设计/复刻创建的自定义音色是账号资产，需通过删除接口主动清理，避免占用配额。

## 来源文档

- [非实时语音合成（Qwen-TTS）API参考](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-api.md)
- [声音设计API参考](../../raw/model-api-reference/speech-synthesis-api-reference/voice-design-api-references.md)
- [CosyVoice WebSocket API参考](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-websocket-api.md)
- [CosyVoice服务端事件](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-server-events.md)
- [CosyVoice客户端事件](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-client-events.md)
- [实时语音合成CosyVoice Java SDK](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-java-sdk.md)
- [实时语音合成CosyVoice Python SDK](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-python-sdk.md)
- [语音合成CosyVoice Android SDK](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-android-sdk.md)
- [语音合成CosyVoice iOS SDK](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-ios-sdk.md)
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
- [非实时语音合成CosyVoice HTTP API参考](../../raw/model-api-reference/speech-synthesis-api-reference/non-realtime-cosyvoice-api/cosyvoice-tts-http-api.md)
- [Java SDK](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-realtime-api-reference/qwen-tts-realtime-java-sdk.md)
- [非实时语音合成CosyVoice Java SDK参考](../../raw/model-api-reference/speech-synthesis-api-reference/non-realtime-cosyvoice-api/cosyvoice-tts-java-sdk.md)
- [非实时语音合成CosyVoice Python SDK参考](../../raw/model-api-reference/speech-synthesis-api-reference/non-realtime-cosyvoice-api/cosyvoice-tts-python-sdk.md)
- [MiniMax同步语音合成API参考](../../raw/model-api-reference/speech-synthesis-api-reference/minimax-speech-synthesis/minimax-synchronous-speech-synthesis-api.md)
- [声音复刻Java SDK参考](../../raw/model-api-reference/speech-synthesis-api-reference/sound-reengraving/voice-clone-design-java-sdk.md)
- [声音复刻HTTP API参考](../../raw/model-api-reference/speech-synthesis-api-reference/sound-reengraving/voice-clone-design-http-api.md)
- [声音复刻Python SDK参考](../../raw/model-api-reference/speech-synthesis-api-reference/sound-reengraving/voice-clone-design-python-sdk.md)



