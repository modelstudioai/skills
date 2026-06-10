# speech recognition api reference

阿里云百炼平台提供三大语音识别模型系列（Fun-ASR、Paraformer、Qwen-ASR），覆盖**实时流式识别**与**录音文件识别**两类场景，支持中、英、日、粤及多种外语，并提供 WebSocket、RESTful 协议与 Python/Java/Android/iOS 多语言 SDK。本文汇总各系列的服务端点、交互流程、核心参数、SDK 接口与定制热词能力，供开发者按场景快速选型与接入。

## 模型系列与适用场景

| 模型系列 | 适用场景 | 协议 | 地域 | 主要 SDK |
| --- | --- | --- | --- | --- |
| **Fun-ASR 实时** | 低延迟实时转写、会议/对话 | WebSocket | 华北2（北京）、新加坡 | Python / Java / Android / iOS |
| **Paraformer 实时** | 实时转写（仅北京地域） | WebSocket | 华北2（北京） | Python / Java / Android / iOS |
| **Qwen-ASR 实时** | 多语种实时识别，支持 VAD/Manual 两种断句模式 | WebSocket | 华北2（北京）、新加坡 | Python / Java |
| **Paraformer 录音文件** | 长音频离线批量转写 | RESTful（异步） | 华北2（北京） | Python / Java / Android / iOS / cURL |

> **注意**：Paraformer 实时识别**仅支持华北2（北京）地域**，不支持新加坡；Fun-ASR 与 Qwen-ASR 同时支持北京与新加坡。选型时请结合地域合规与语种需求决定，详见 [Paraformer实时语音识别WebSocket API](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/websocket-for-paraformer-real-time-service.md)。

## 服务端点

### 实时识别 WebSocket URL

**Fun-ASR / Paraformer 实时**（URL 固定，模型通过 `run-task` 消息体指定）：

- 华北2（北京）：`wss://dashscope.aliyuncs.com/api-ws/v1/inference`
- 新加坡：`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference`

**Qwen-ASR 实时**（模型通过 URL 查询参数 `model` 指定）：

- 华北2（北京）：`wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=<model_name>`
- 新加坡：`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime?model=<model_name>`

> **注意**：新加坡地域旧版域名 `wss://dashscope-intl.aliyuncs.com` 即将下线，请迁移至新版 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com` 域名。

### 录音文件识别 RESTful URL

- 提交任务：`POST https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription`
- 查询任务：`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`

请求头需携带 `X-DashScope-Async: enable`，否则无法提交[异步任务](../concepts/async-task.md)。详见 [Paraformer录音文件识别RESTful API](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-recorded-speech-recognition-api-reference/paraformer-recorded-speech-recognition-restful-api.md)。

## 公共请求头

所有 WebSocket 与 RESTful 接口共享以下请求头：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `Authorization` | string | 是 | `Bearer <your_api_key>`，握手阶段校验，无效则返回 HTTP 401/403 |
| `user-agent` | string | 否 | 客户端标识 |
| `X-DashScope-WorkSpace` | string | 否 | [业务空间](../concepts/workspace.md) ID |
| `X-DashScope-DataInspection` | string | 否 | 数据合规检测，默认不传或 `enable`；非必要请勿启用 |

建议使用环境变量而非硬编码 API Key，敏感场景可改用 60 秒有效期的[临时鉴权 Token](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)。

## 实时识别交互流程

### Fun-ASR / Paraformer 实时（run-task 协议）

1. 建立 WebSocket 连接。
2. 客户端发送 `run-task`（携带 `model`、`format`、`sample_rate` 等），服务端返回 `task-started`。
3. 客户端持续发送二进制单声道音频流，服务端持续推送 `result-generated`（含中间结果与 `sentence_end=true` 的最终结果）。
4. 客户端发送 `finish-task`，继续接收剩余 `result-generated`。
5. 服务端返回 `task-finished`，客户端关闭连接。

`run-task` 的关键参数（位于 `payload.parameters`）：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `model` | string | 是 | 模型名称（如 `fun-asr-realtime`、`paraformer-realtime-*`） |
| `format` | string | 是 | 音频格式：`pcm` / `wav` / `mp3` / `opus` / `speex` / `aac` / `amr` |
| `sample_rate` | integer | 是 | 采样率（Hz）。8k 模型仅支持 8000，其他仅支持 16000 |
| `vocabulary_id` | string | 否 | 定制热词 ID |
| `language_hints` | array | 否 | 语种提示（`zh` / `en` / `ja`），仅取首个值 |
| `semantic_punctuation_enabled` | bool | 否 | 语义断句（默认 `false`，即 VAD 断句） |
| `max_sentence_silence` | integer | 否 | VAD 静音阈值（ms），\[200, 6000\]，仅 VAD 断句生效 |
| `heartbeat` | bool | 否 | 心跳保活，避免长静音超时断连（默认 60 秒） |
| `speech_noise_threshold` | float | 否 | 仅 Fun-ASR 支持，\[-1.0, 1.0\]，调整 VAD 灵敏度 |

服务端 `result-generated` 事件返回 `sentence` 结构，含 `begin_time` / `end_time` / `text` / `words`（逐字时间戳与标点）。详见 [实时语音识别（Fun-ASR）客户端事件](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/fun-asr-client-events.md) 与 [实时语音识别（Fun-ASR）服务端事件](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/fun-asr-server-events.md)。

### Qwen-ASR 实时（Realtime API 协议）

Qwen-ASR 采用与 OpenAI Realtime 风格一致的事件协议，支持两种断句模式：

- **VAD 模式（默认）**：服务端自动检测语音起点/终点，适合实时对话、会议记录。
- **Manual 模式**：客户端通过 `input_audio_buffer.commit` 显式提交断句，适合聊天语音消息等边界明确场景。

典型流程：`session.update` → 持续 `input_audio_buffer.append` → 服务端推送 `conversation.item.input_audio_transcription.completed`。关键配置位于 `session.input_audio_transcription`：

| 参数 | 说明 |
| --- | --- |
| `language` | 源语言：`zh`（含普通话/四川话/闽南语/吴语）、`yue`（粤语）、`en`、`ja`、`de`、`ko`、`ru`、`fr`、`pt`、`ar`、`it`、`es` |
| `model` | 通过 URL 查询参数指定，如 `qwen-asr-realtime` |
| `input_audio_format` | `pcm` / `opus` |
| `sample_rate` | 16000 / 8000（8000 会升采样，建议仅在电话线路使用） |

详见 [Qwen-ASR实时语音识别WebSocket API](../../raw/model-api-reference/speech-recognition-api-reference/qwen-asr-realtime-api/qwen-asr-realtime-interaction-process.md) 与 [实时语音识别（Qwen-ASR-Realtime）客户端事件](../../raw/model-api-reference/speech-recognition-api-reference/qwen-asr-realtime-api/qwen-asr-realtime-client-events.md)。

## 录音文件识别（Paraformer）

针对长音频（分钟到小时级）离线转写，采用[异步任务](../concepts/async-task.md)模型：

1. 调用提交接口，上传 `file_urls`（可批量，支持音频/视频 URL），任务进入 `PENDING` 排队。
2. 轮询查询接口直到状态变为 `SUCCEEDED` / `FAILED`。识别以数百倍加速完成，结果与下载链接**有效期 24 小时**。
3. 关键参数：
   - `model`：如 `paraformer-v2`（必选）
   - `file_urls`：待识别文件 URL 数组（必选）
   - `channel_id`：音轨索引数组（多轨场景）
   - `language_hints`：仅 `paraformer-v2` 支持，语种提示
   - `diarization_enabled` / `speaker_count`：说话人分离
   - `disfluency_removal_enabled`：过滤"嗯""啊"等语气词
   - `timestamp_alignment_enabled`：时间戳校准
   - `special_word_filter`：敏感词过滤

Java / Python SDK 封装了 `Transcription` 核心类，提供 `asyncCall` + `wait`（同步等待）和 `asyncCall` + 轮询（异步查询）两种调用方式。Android / iOS SDK 通过 `startFileTranscriber` / `nui_file_trans_start` 发起任务，并通过 `onFileTransEventCallback` 监听 `EVENT_FILE_TRANS_RESULT` 事件获取结果。详见 [Paraformer录音文件识别Java SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-recorded-speech-recognition-api-reference/paraformer-recorded-speech-recognition-java-sdk.md)。

> **注意**：视频文件建议先用 `ffmpeg` 预处理，仅提取单声道 16kHz opus 音轨再提交，可显著降低传输耗时。示例：`ffmpeg -i input.mp4 -ac 1 -ar 16000 -acodec libopus output.opus`。详见 [最佳实践](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-recorded-speech-recognition-api-reference/paraformer-best-practices.md)。

## SDK 接入

### DashScope SDK（推荐，服务端语言）

- **Python**：`pip install dashscope`，覆盖 Fun-ASR / Paraformer / Qwen-ASR 实时与录音文件所有场景。
- **Java**：Maven 引入 `dashscope-sdk-java`，同样覆盖全系列。

两类 SDK 均封装了连接管理、事件序列化与断线重试，优先使用。

### 端侧 SDK（Android / iOS）

以 ZIP 整合包形式分发：
- **Android**：`app/libs` 下 AAR，C++ 场景使用 `android_libs` + `android_include`。
- **iOS**：`nuisdk.framework`，需在 Build Phases 设置为 Embed & Sign。

端侧 SDK 同时覆盖实时识别与录音文件识别两套接口，核心 API 包括 `initialize` / `startTranscriber`（实时）与 `startFileTranscriber`（文件）/ `release`。

> **注意**：DashScope 官方 SDK 仅支持 Java 与 Python。使用 Go、Node.js、C# 等其他语言时，需直接按本文 WebSocket 协议或 RESTful 接口自行实现序列化，参考 [Fun-ASR实时语音识别WebSocket API](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/fun-asr-realtime-websocket-api.md)。

## 定制热词

通过热词列表提升特定术语（人名、产品名、行业词）的识别准确率。热词列表通过 `vocabulary_id` 参数在 `run-task` 或录音文件请求中引用。

### HTTP API

- URL：`POST https://dashscope.aliyuncs.com/api/v1/services/audio/asr/customization`（北京）/ `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/audio/asr/customization`（新加坡）
- 请求体通过 `input.action` 区分操作：`create_vocabulary` / `query_vocabulary` / `update_vocabulary` / `delete_vocabulary`
- `target_model` 指定目标模型系列（如 `fun-asr`、`paraformer`）
- 每条热词包含 `text` 与 `weight`（权重，通常 1-5）

### Python SDK

封装为 `dashscope.audio.asr.vocab` 模块下的 `create_vocabulary` / `list_vocabulary` / `update_vocabulary` / `delete_vocabulary` 四个函数，参数与 HTTP 接口一一对应。

> **注意**：新加坡地域的**子[业务空间](../concepts/workspace.md)暂不支持热词功能**。各地域 API Key 不互通，切换地域需重新创建热词列表。详见 [定制热词HTTP API参考](../../raw/model-api-reference/speech-recognition-api-reference/custom-hot-words/vocabulary-http-api.md)。

## 限制与注意事项

- **地域与协议**：Paraformer 实时仅北京；Fun-ASR、Qwen-ASR 实时与 Paraformer 录音文件支持北京（Qwen-ASR 录音文件也仅北京）。新加坡旧版域名 `dashscope-intl.aliyuncs.com` 即将下线，请尽快迁移。
- **采样率**：8k 模型仅接受 8000 Hz，其他模型仅接受 16000 Hz；Qwen-ASR 虽支持 8000 输入，但会升采样到 16000 再识别。
- **音频通道**：所有实时识别接口**必须单声道**，立体声会被拒绝或识别异常。
- **超时与保活**：WebSocket 持续 60 秒无音频会超时断开，可通过 `heartbeat=true` 或持续发送静音帧保活。
- **鉴权**：`Authorization` 在握手阶段校验，失败直接返回 HTTP 401/403；生产环境建议使用临时鉴权 Token（60 秒有效期）。
- **录音文件结果时效**：识别结果与下载 URL 有效期 24 小时，过期需重新提交任务。
- **热词配额**：受账号与地域限制，具体上限见官方"限制与计费"文档。

## 来源文档

- [Fun-ASR实时语音识别WebSocket API](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/fun-asr-realtime-websocket-api.md)
- [实时语音识别（Fun-ASR）客户端事件](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/fun-asr-client-events.md)
- [实时语音识别（Fun-ASR）服务端事件](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/fun-asr-server-events.md)
- [Python SDK](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/fun-asr-realtime-python-sdk.md)
- [Java SDK](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/fun-asr-realtime-java-sdk.md)
- [Fun-ASR实时语音识别Android SDK](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/android-sdk-for-fun-asr-real-time-service.md)
- [Paraformer实时语音识别WebSocket API](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/websocket-for-paraformer-real-time-service.md)
- [Fun-ASR实时语音识别iOS SDK](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/ios-sdk-for-fun-asr-real-time-service.md)
- [实时语音识别（Paraformer）客户端事件](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/paraformer-client-events.md)
- [实时语音识别（Paraformer）服务端事件](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/paraformer-server-events.md)
- [Paraformer实时语音识别Java SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/paraformer-real-time-speech-recognition-java-sdk.md)
- [Paraformer实时语音识别Python SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/paraformer-real-time-speech-recognition-python-sdk.md)
- [Paraformer实时语音识别Android SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/android-sdk-for-paraformer-real-time-service.md)
- [Qwen-ASR实时语音识别WebSocket API](../../raw/model-api-reference/speech-recognition-api-reference/qwen-asr-realtime-api/qwen-asr-realtime-interaction-process.md)
- [Paraformer实时语音识别iOS SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/ios-sdk-for-paraformer-real-time-service.md)
- [实时语音识别（Qwen-ASR-Realtime）客户端事件](../../raw/model-api-reference/speech-recognition-api-reference/qwen-asr-realtime-api/qwen-asr-realtime-client-events.md)
- [实时语音识别（Qwen-ASR-Realtime）服务端事件](../../raw/model-api-reference/speech-recognition-api-reference/qwen-asr-realtime-api/qwen-asr-realtime-server-events.md)
- [实时语音识别（Qwen-ASR-Realtime）Python SDK-API参考](../../raw/model-api-reference/speech-recognition-api-reference/qwen-asr-realtime-api/qwen-asr-realtime-python-sdk.md)
- [实时语音识别（Qwen-ASR-Realtime）Java SDK-API参考](../../raw/model-api-reference/speech-recognition-api-reference/qwen-asr-realtime-api/qwen-asr-realtime-java-sdk.md)
- [Paraformer录音文件识别Java SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-recorded-speech-recognition-api-reference/paraformer-recorded-speech-recognition-java-sdk.md)
- [Paraformer录音文件识别Python SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-recorded-speech-recognition-api-reference/paraformer-recorded-speech-recognition-python-sdk.md)
- [Paraformer录音文件识别RESTful API](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-recorded-speech-recognition-api-reference/paraformer-recorded-speech-recognition-restful-api.md)
- [Paraformer录音文件识别Android SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-recorded-speech-recognition-api-reference/paraformer-recorded-speech-recognition-android-sdk.md)
- [Paraformer录音文件识别iOS SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-recorded-speech-recognition-api-reference/paraformer-recorded-speech-recognition-ios-sdk.md)
- [最佳实践](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-recorded-speech-recognition-api-reference/paraformer-best-practices.md)
- [定制热词HTTP API参考](../../raw/model-api-reference/speech-recognition-api-reference/custom-hot-words/vocabulary-http-api.md)
- [定制热词Python SDK参考](../../raw/model-api-reference/speech-recognition-api-reference/custom-hot-words/vocabulary-python-sdk.md)


