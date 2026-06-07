# speech recognition api reference

百炼平台的语音识别（ASR）API 覆盖**录音文件识别**（异步上传 URL，处理长音频）与**实时语音识别**（WebSocket 流式上传 PCM/Opus），按模型家族分为三条线：千问家族（Qwen-ASR / Qwen-ASR-Realtime）、Paraformer 家族和 Fun-ASR 家族。三者鉴权方式、URL 域名规则、热词与 ITN 等增强能力大体一致，但接入协议、参数命名、模型代号、支持的采样率与语种各不相同——本页汇总三条线在 API 层面的差异与共性，作为开发者集成时的索引。

## 支持的模型家族与接入方式

| 模型家族 | 录音文件识别 | 实时识别 | 主要接入协议 |
| --- | --- | --- | --- |
| 千问 Qwen-ASR | `qwen3-asr-flash`（同步）、`qwen3-asr-flash-filetrans`（异步） | `qwen3-asr-realtime` | OpenAI 兼容 / DashScope 同步 / DashScope 异步 / Realtime WebSocket |
| Paraformer | `paraformer-v2`（异步） | `paraformer-realtime-v2`、`paraformer-realtime-v1`、`paraformer-realtime-8k-v2/v1` | DashScope 异步 RESTful / WebSocket（DashScope 协议） |
| Fun-ASR | `fun-asr`、`fun-asr-2025-11-07`、`fun-asr-2025-08-25`、`fun-asr-mtl`、`fun-asr-mtl-2025-08-25`（异步） | `fun-asr-realtime` 等 | DashScope 异步 HTTP / WebSocket（DashScope 协议） |

录音文件识别 API 的协议差异参见 [录音文件识别（Qwen-ASR）API参考](../../raw/model-api-reference/speech-recognition-api-reference/qwen-asr-api-reference.md)、[Paraformer录音文件识别RESTful API](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-recorded-speech-recognition-api-reference/paraformer-recorded-speech-recognition-restful-api.md) 与 [Fun-ASR录音文件识别HTTP API参考](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/fun-asr-recorded-speech-recognition-http-api.md)。三者均提供 Java / Python SDK，Paraformer 与 Fun-ASR 还额外提供 Android / iOS SDK。

> **注意**：`paraformer-v1` 系列模型已逐步被 `v2` 取代；`paraformer-realtime-v1` 仅支持 16000 Hz 采样率，新接入建议直接使用 `paraformer-realtime-v2`（支持任意采样率），见 [实时语音识别（Paraformer）客户端事件](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/paraformer-client-events.md)。

## 服务端点与地域

录音文件识别（异步）服务端点：

- **中国内地（北京）**：`POST https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription`，查询任务 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`。
- **国际（新加坡）**：`POST https://dashscope-intl.aliyuncs.com/...`（Qwen-ASR）或新版多租域名 `POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/...`（Paraformer / Fun-ASR）。
- 提交任务必须携带 `X-DashScope-Async: enable` 请求头，否则不会进入异步队列。

Qwen-ASR 还支持 **OpenAI 兼容**（`POST /compatible-mode/v1/chat/completions`）和 **DashScope 同步**（`POST /api/v1/services/aigc/multimodal-generation/generation`）两种"立即返回"协议，仅适用于 `qwen3-asr-flash`；`qwen3-asr-flash-filetrans` 长音频版本必须使用异步流程。

实时识别 WebSocket 端点：

- **Paraformer**：仅在华北 2（北京），`wss://dashscope.aliyuncs.com/api-ws/v1/inference`。
- **Fun-ASR**：北京 `wss://dashscope.aliyuncs.com/api-ws/v1/inference`；新加坡 `wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference`。
- **Qwen-ASR-Realtime**：通过 URL 查询参数 `model=<model_name>` 指定模型，北京 `wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=<model_name>`，新加坡同上结构。

所有端点的鉴权统一通过 `Authorization: Bearer <API_KEY>` 请求头传递（北京和新加坡的 API Key 不同，需分别获取）。详见 [Paraformer实时语音识别WebSocket API](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/websocket-for-paraformer-real-time-service.md)、[Fun-ASR实时语音识别WebSocket API](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/fun-asr-realtime-websocket-api.md) 与 [Qwen-ASR实时语音识别WebSocket API](../../raw/model-api-reference/speech-recognition-api-reference/qwen-asr-realtime-api/qwen-asr-realtime-interaction-process.md)。

> **注意**：新加坡地域旧版域名 `wss://dashscope-intl.aliyuncs.com` / `https://dashscope-intl.aliyuncs.com` 即将下线，请迁移到 `*.ap-southeast-1.maas.aliyuncs.com` 的新版多租域名（Qwen-ASR-OpenAI 兼容入口仍使用 `dashscope-intl` 域名，未迁移）。

## 录音文件识别：异步"提交-轮询"流程

三个家族的异步流程一致：

1. 客户端 `POST .../audio/asr/transcription`，请求头带 `X-DashScope-Async: enable`，请求体核心字段：
   - `model`：模型代号；
   - `input.file_urls`：HTTPS 公网可下载 URL 列表（单次仅 1 个 URL；URL 中如含中文/空格需 URL 编码，否则报 `InvalidFile.DownloadFailed`）；
   - `parameters`：通用增强参数（见下节）。
2. 服务端立即返回 `task_id` 与 `task_status`。
3. 客户端轮询 `GET .../tasks/{task_id}` 获取识别结果（`SUCCEEDED` / `FAILED` / `RUNNING`），失败返回 `code` 与 `message`。

Qwen-ASR 与 Fun-ASR/Paraformer 在请求体 schema 上略有差异：

- **Qwen-ASR 异步** 使用 `input.file_url`（单字符串）而非 `input.file_urls`（数组），模型固定为 `qwen3-asr-flash-filetrans`；
- **Paraformer / Fun-ASR** 使用 `input.file_urls`（数组，目前实际限制为 1 个）。

SDK 侧，Python `async_call()` / Java `asyncCall()` 返回任务对象，配合 `fetch()` 自动轮询；详见 [Paraformer录音文件识别Python SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-recorded-speech-recognition-api-reference/paraformer-recorded-speech-recognition-python-sdk.md)、[Paraformer录音文件识别Java SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-recorded-speech-recognition-api-reference/paraformer-recorded-speech-recognition-java-sdk.md)、[Fun-ASR录音文件识别Python SDK](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/funauidio-asr-recorded-speech-recognition-python-sdk.md)、[Fun-ASR录音文件识别Java SDK](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/fun-asr-recorded-speech-recognition-java-sdk.md)。移动端可用 [Paraformer录音文件识别Android SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-recorded-speech-recognition-api-reference/paraformer-recorded-speech-recognition-android-sdk.md) / [iOS SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-recorded-speech-recognition-api-reference/paraformer-recorded-speech-recognition-ios-sdk.md) 与 Fun-ASR 的同名 SDK。

### 录音识别通用 parameters

| 参数 | 类型 | 默认 | 支持范围 | 说明 |
| --- | --- | --- | --- | --- |
| `channel_id` | array[int] | `[0]` | 全部 | 多音轨索引，每个被指定的音轨独立计费 |
| `vocabulary_id` | string | - | Paraformer-v2、Fun-ASR | 热词列表 ID（v2 系列），通过定制热词 API 获取 |
| `resource_id` + `resource_type` | string | - | Paraformer v1 | 老 v1 系列热词方案（`resource_type` 固定 `asr_phrase`） |
| `disfluency_removal_enabled` | bool | false | Paraformer | 过滤语气词 |
| `timestamp_alignment_enabled` | bool | false | Paraformer | 时间戳校准 |
| `special_word_filter` | string(JSON) | - | Paraformer、Fun-ASR | 敏感词处理（替换为 `*` / 直接过滤；可关闭系统内置词表） |
| `diarization_enabled` + `speaker_count` | bool / int | false / 自动 | Paraformer、Fun-ASR | 说话人分离（仅单声道，建议时长 ≤ 2 小时） |
| `language_hints` | array[string] | - | Paraformer-v2、Fun-ASR | 语种提示（`zh`、`en`、`ja`、`yue`、`ko` 等；Fun-ASR 系统只取数组第一个元素） |
| `enable_itn` | bool | false | Qwen-ASR | 逆文本标准化（中英文音频生效） |

详细字段定义、错误码及完整示例见 [Paraformer录音文件识别RESTful API](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-recorded-speech-recognition-api-reference/paraformer-recorded-speech-recognition-restful-api.md) 与 [Fun-ASR录音文件识别HTTP API参考](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/fun-asr-recorded-speech-recognition-http-api.md)。

### Qwen-ASR 的 OpenAI 兼容 / 同步调用

`qwen3-asr-flash` 可通过 OpenAI Chat Completions 协议调用，音频以 `input_audio.data` 形式传入（URL 或 `data:audio/wav;base64,...` Base64），并通过 `extra_body.asr_options` 传 ASR 特有参数：

```json
{
  "model": "qwen3-asr-flash",
  "messages": [{
    "role": "user",
    "content": [{"type": "input_audio", "input_audio": {"data": "https://.../welcome.mp3"}}]
  }],
  "stream": true,
  "stream_options": {"include_usage": true},
  "extra_body": {"asr_options": {"language": "zh", "enable_itn": false}}
}
```

返回体复用 Chat Completions 结构，`message.annotations` 数组中包含 `{"type":"audio_info","language":"zh","emotion":"neutral"}` 等元信息；`asr_options.language` 取值范围覆盖 26 种语种（`zh/yue/en/ja/de/ko/ru/fr/pt/ar/it/es/hi/id/th/tr/uk/vi/cs/da/fil/fi/is/ms/no/pl/sv`），未指定时模型自动识别（含中英日韩混合）。详见 [录音文件识别（Qwen-ASR）API参考](../../raw/model-api-reference/speech-recognition-api-reference/qwen-asr-api-reference.md)。

## 实时识别：WebSocket 双工流式

### Paraformer / Fun-ASR：DashScope 协议

两者复用同一套事件协议，时序：

```
client                                server
  ─── run-task ─────────────────────►
  ◄────────────────── task-started ───
  ─── binary audio frames ──────────►
  ◄────── result-generated × N ───────
  ─── finish-task ──────────────────►
  ◄────── result-generated（尾部）─────
  ◄────────────────── task-finished ───
```

`run-task` 的 JSON 结构：

```json
{
  "header": {"action": "run-task", "task_id": "<uuid>", "streaming": "duplex"},
  "payload": {
    "task_group": "audio",
    "task": "asr",
    "function": "recognition",
    "model": "paraformer-realtime-v2",
    "input": {},
    "parameters": {"format": "pcm", "sample_rate": 16000, "language_hints": ["en"]}
  }
}
```

`parameters` 字段差异参见 [实时语音识别（Paraformer）客户端事件](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/paraformer-client-events.md) 与 [实时语音识别（Fun-ASR）客户端事件](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/fun-asr-client-events.md)：

- 通用：`format`（`pcm` / `wav` / `mp3` / `opus` / `speex` / `aac` / `amr`，opus/speex 需 Ogg 封装，wav 必须 PCM 编码，amr 仅 AMR-NB），`sample_rate`，`vocabulary_id`，`language_hints`，`semantic_punctuation_enabled` + `max_sentence_silence`（200–6000 ms）+ `multi_threshold_mode_enabled`，`heartbeat`（默认 false，纯静音 60 秒后断连）。
- Paraformer 独有：`disfluency_removal_enabled`、`punctuation_prediction_enabled`、`inverse_text_normalization_enabled`（默认 true，中文数字转阿拉伯数字）。
- Fun-ASR 独有：`speech_noise_threshold`（`[-1.0, 1.0]` 调整 VAD 灵敏度，步长 0.1 调）；`language_hints` 仅取首个值。
- 采样率约束：Paraformer 因模型而异（v2 任意 / v1 16000 / 8k 系列 8000），Fun-ASR 8k 模型固定 8000，其他固定 16000。

服务端事件主要包括 `task-started`、`result-generated`（增量结果，`payload.output.sentence` 含 `begin_time` / `end_time` / `text` / `words[]` / `sentence_end`；当 `sentence_end=true` 时 `usage.duration` 为计费时长）、`task-finished`、`task-failed`，详见 [实时语音识别（Paraformer）服务端事件](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/paraformer-server-events.md) 与 [实时语音识别（Fun-ASR）服务端事件](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/fun-asr-server-events.md)。

官方 SDK 仅 Java 与 Python，移动端单独提供：[Paraformer实时语音识别Java SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/paraformer-real-time-speech-recognition-java-sdk.md) / [Python SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/paraformer-real-time-speech-recognition-python-sdk.md) / [Android SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/android-sdk-for-paraformer-real-time-service.md) / [iOS SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/ios-sdk-for-paraformer-real-time-service.md)，以及 Fun-ASR 的 [Java SDK](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/fun-asr-realtime-java-sdk.md) / [Python SDK](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/fun-asr-realtime-python-sdk.md) / [Android SDK](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/android-sdk-for-fun-asr-real-time-service.md) / [iOS SDK](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/ios-sdk-for-fun-asr-real-time-service.md)。

### Qwen-ASR-Realtime：Realtime 协议

Qwen 实时与 Paraformer/Fun-ASR 的事件结构**完全不同**，使用 OpenAI Realtime 风格 schema：

- 客户端事件：`session.update`（配置音频格式、语种、VAD），`input_audio_buffer.append`（追加音频块，base64 编码；非 VAD 模式下单事件 `audio` 最大 15 MiB），`input_audio_buffer.commit`（Manual 模式手动断句），`session.finish`（结束会话）。
- 服务端事件：`input_audio_buffer.speech_started` / `.speech_stopped` / `.committed`、`conversation.item.created`、`conversation.item.input_audio_transcription.text`（实时结果）、`conversation.item.input_audio_transcription.completed`（最终结果）、`session.finished`。

支持两种交互模式（通过 `session.turn_detection` 切换）：

- **VAD 模式（默认）**：服务端自动断句，适合实时对话和会议；`turn_detection.type=server_vad`，`threshold` 推荐 `0.0`（默认 0.2，越低越灵敏），`silence_duration_ms` 推荐 `400`（默认 800，范围 200–6000）。
- **Manual 模式**：将 `turn_detection` 设为 `null`，由客户端发 `input_audio_buffer.commit` 显式断句，适合聊天软件录音发送场景。

音频参数：`input_audio_format` 支持 `pcm` 和 `opus`（默认 `pcm`），`sample_rate` 支持 `16000` 与 `8000`（设置为 8000 时服务端会升采样到 16000，仅推荐源音频确为 8000 Hz 时使用）。语种通过 `session.input_audio_transcription.language` 指定，取值与 Qwen-ASR 录音版一致的 26 种。详见 [实时语音识别（Qwen-ASR-Realtime）客户端事件](../../raw/model-api-reference/speech-recognition-api-reference/qwen-asr-realtime-api/qwen-asr-realtime-client-events.md) 与 [服务端事件](../../raw/model-api-reference/speech-recognition-api-reference/qwen-asr-realtime-api/qwen-asr-realtime-server-events.md)，SDK 见 [Python SDK](../../raw/model-api-reference/speech-recognition-api-reference/qwen-asr-realtime-api/qwen-asr-realtime-python-sdk.md) 与 [Java SDK](../../raw/model-api-reference/speech-recognition-api-reference/qwen-asr-realtime-api/qwen-asr-realtime-java-sdk.md)。

> **注意**：Paraformer/Fun-ASR 的 `task_id` 由客户端自行生成（UUID），需在 `run-task` 与 `finish-task` 中保持一致；Qwen-ASR-Realtime 则用 `event_id` 标识每个事件，不存在共享 `task_id`，状态由 `session.id` 维护——切换两套协议时需重写事件路由逻辑。

## 定制热词

Paraformer-v2 与 Fun-ASR 的实时及录音识别都支持 `vocabulary_id` 热词参数。热词通过专门的定制热词管理 API 创建、查询、更新和删除：

- 服务端点：`POST https://dashscope.aliyuncs.com/api/v1/services/audio/asr/customization`（新加坡 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/...`）。
- 模型固定为 `speech-biasing`，通过 `input.action` 区分操作：`create_vocabulary`、`list_vocabulary`、`query_vocabulary`、`update_vocabulary`、`delete_vocabulary`。
- 创建时需指定 `target_model`（如 `paraformer-v2`、`fun-asr`）、`prefix`（前缀，便于区分业务）、`vocabulary[]`（每条 `{"text": "...", "weight": 1-4}`），返回 `vocabulary_id` 即可在识别请求中使用。
- HTTP / Java / Python 三种调用方式分别见 [定制热词HTTP API参考](../../raw/model-api-reference/speech-recognition-api-reference/custom-hot-words/vocabulary-http-api.md)、[Java SDK](../../raw/model-api-reference/speech-recognition-api-reference/custom-hot-words/vocabulary-java-sdk.md)、[Python SDK](../../raw/model-api-reference/speech-recognition-api-reference/custom-hot-words/vocabulary-python-sdk.md)。

> **注意**：新加坡地域的**子业务空间**暂不支持热词功能；Paraformer 老 v1 系列只能使用 `resource_id` / `phrase_id` 方案（参见 `paraformer-asr-phrase-manager`），与 v2 的 `vocabulary_id` 不兼容。

## 限制与注意事项

- **API Key 区分地域**：北京与新加坡地域的 API Key 互不通用，跨地域必须分别获取（链接：`https://help.aliyun.com/zh/model-studio/get-api-key`）。生产环境对外部调用建议使用 60 秒有效期的临时鉴权 Token。
- **OSS 临时 URL 仅用于测试**：以 `oss://` 为前缀的临时 URL 有效期仅 48 小时，且文件上传凭证接口限流 100 QPS 不可扩容，**禁止用于生产环境与压测**——生产请使用阿里云 OSS 等稳定存储的 HTTPS URL，并对 URL 中的中文/空格做 URL 编码。
- **音轨独立计费**：录音识别中 `channel_id` 指定的每条音轨都会单独计费，例如 `[0, 1]` 单文件会产生两笔费用。
- **说话人分离的限制**：仅单声道音频，建议时长 ≤ 2 小时；多声道音频不支持。
- **WebSocket 心跳**：实时识别默认 60 秒静音超时断连；如需保持长连接，将 `heartbeat` 置为 `true` 并持续发送静音音频。
- **音频格式约束**：实时识别中 opus / speex 必须用 Ogg 封装，wav 必须为 PCM 编码，amr 仅支持 AMR-NB。
- **音频预处理**：对于长视频文件，强烈建议先用 ffmpeg 提取第一条音轨、降采样到 16 kHz、压缩为 opus，可显著缩小文件体积并加快异步转写吞吐：`ffmpeg -i input -ac 1 -ar 16000 -acodec libopus out.opus`，参见 [最佳实践](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-recorded-speech-recognition-api-reference/paraformer-best-practices.md)。
- **`X-DashScope-DataInspection`**：数据合规检测请求头，非必要请勿开启，会增加调用开销。

## 来源文档

- [录音文件识别（Qwen-ASR）API参考](../../raw/model-api-reference/speech-recognition-api-reference/qwen-asr-api-reference.md)
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
- [Fun-ASR录音文件识别Python SDK](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/funauidio-asr-recorded-speech-recognition-python-sdk.md)
- [Fun-ASR录音文件识别HTTP API参考](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/fun-asr-recorded-speech-recognition-http-api.md)
- [Fun-ASR录音文件识别Android SDK](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/fun-asr-recorded-speech-recognition-android-sdk.md)
- [Fun-ASR录音文件识别iOS SDK](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/fun-asr-recorded-speech-recognition-ios-sdk.md)
- [Fun-ASR录音文件识别Java SDK](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/fun-asr-recorded-speech-recognition-java-sdk.md)
- [定制热词HTTP API参考](../../raw/model-api-reference/speech-recognition-api-reference/custom-hot-words/vocabulary-http-api.md)
- [定制热词Java SDK参考](../../raw/model-api-reference/speech-recognition-api-reference/custom-hot-words/vocabulary-java-sdk.md)
- [定制热词Python SDK参考](../../raw/model-api-reference/speech-recognition-api-reference/custom-hot-words/vocabulary-python-sdk.md)



