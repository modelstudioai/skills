# speech recognition api reference

阿里云百炼语音识别服务提供实时语音转写与录音文件异步转写两种核心模式，全面支持 Qwen-ASR、Paraformer 与 Fun-ASR 系列模型。开发者可通过 [[dashscope-sdk]]、OpenAI 兼容协议或原生 WebSocket/HTTP API 快速集成，并可根据业务需求配置定制热词、说话人分离、情感分析等高级能力。

## 支持的模型与功能
平台按应用场景将语音识别 API 分为实时流式识别与录音文件识别两大类，核心模型特性如下：
| 模型系列 | 适用模式 | 核心特性 | 支持协议/SDK |
|---|---|---|---|
| **Qwen-ASR** | 实时/录音文件 | 多语种高精度、支持[[streaming-output|流式输出]]、VAD/Manual 双模式 | WebSocket、OpenAI 兼容、Python/Java SDK |
| **Paraformer** | 实时/录音文件 | 默认标点预测与 ITN、支持情感识别（仅 8k-v2）、定制热词 | WebSocket、DashScope SDK (Java/Python/Android/iOS) |
| **Fun-ASR** | 实时/录音文件 | 长音频支持强、多语种覆盖广、支持声道分离 | WebSocket、RESTful 异步、全平台 SDK |

> **注意**：Paraformer 情感识别功能仅限 `paraformer-realtime-8k-v2` 模型，且必须显式关闭语义断句（`semantic_punctuation_enabled=false`）。若同时开启语义断句，情感标签将无法正常返回。

## 关键参数说明
### 认证与路由
- **鉴权方式**：HTTP Header 需携带 `Authorization: Bearer <api_key>`，或 WebSocket 握手阶段在 Header 传入。生产环境强烈建议使用临时鉴权 Token 替代长期 Key 以降低泄露风险，详见 [[api-key]]。
- **地域路由**：中国内地与国际版端点严格隔离，API Key 不可混用。
  - 中国内地：`dashscope.aliyuncs.com`
  - 国际：`dashscope-intl.aliyuncs.com`

### 音频输入参数
| 参数名 | 类型 | 说明 |
|---|---|---|
| `file_urls` / `input` | array/object | 录音文件需传入公网可访问的 HTTP/HTTPS URL；实时流需按协议发送二进制 PCM/Opus 数据。 |
| `format` | string | 支持 `pcm`, `wav`, `mp3`, `opus`, `aac`, `amr` 等。OPUS/SPEEX 需 Ogg 封装，WAV 需 PCM 编码。 |
| `sample_rate` | integer | 依模型而定。`paraformer-realtime-v2` 支持任意采样率；v1 固定 16kHz；8k 系列仅支持 8000Hz。 |
| `language_hints` | array | 预设识别语种，可提升准确率。部分模型仅读取数组首值，未配置时由模型自动推断。 |

### 处理与输出控制
- `vocabulary_id`：绑定通过 [[custom-hot-words]] 管理的热词列表 ID，提升专有名词召回率。
- `disfluency_removal_enabled`：布尔值，控制是否过滤“呃、啊”等语气词，默认 `false`。
- `diarization_enabled` / `speaker_count`：开启说话人分离并预估人数，适用于会议录音转写。
- `turn_detection`：实时交互核心参数。配置 `server_vad` 开启服务端自动断句；设为 `null` 切换至 Manual 模式（由客户端主动控制语句边界）。

## 调用方式
### 1. SDK 快速接入
推荐优先使用官方 [[dashscope-sdk]]。以 Python SDK 录音文件识别为例，核心类 `Transcription` 提供 `async_call()` 与 `wait()` 方法，支持提交后阻塞等待或异步轮询。
> **注意**：部分旧版文档提及 Paraformer 录音文件支持同步直调，但当前服务端架构已全面转向异步任务队列（`PENDING` → `RUNNING` → `SUCCEEDED`），长任务直调极易触发网关超时，请严格遵循异步提交规范。

### 2. [[openai-compatible-api|OpenAI 兼容接口]]
适用于希望无缝迁移现有 LLM 代码库的开发者。通过 `chat/completions` 端点提交 `input_audio` 消息体即可触发识别，支持配置 `stream` 实现流式结果返回。详细参数映射与请求体结构可参考 [录音文件识别（Qwen-ASR）API参考](../../raw/model-api-reference/speech-recognition-api-reference/qwen-asr-api-reference.md)。

### 3. WebSocket 实时流式协议
适用于低延迟交互场景（如直播字幕、语音助手）。客户端建立连接后需立即发送 `run-task` 指令并等待 `task-started` 响应，随后持续追加二进制音频流。事件交互模型与完整 JSON 结构定义见 [实时语音识别（Paraformer）客户端事件](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/paraformer-client-events.md)。Qwen-ASR 实时流采用 `session.update` 与 `input_audio_buffer.append` 事件体系，交互逻辑略有差异。

### 4. RESTful 异步接口（录音文件）
适用于大批量历史音频处理。流程分为两步：
1. **提交任务**：`POST` 携带 `X-DashScope-Async: enable` 请求头与文件 URL 数组，获取 `task_id`。
2. **轮询结果**：通过 `GET /tasks/{task_id}` 查询状态，直至返回 `SUCCEEDED` 或 `FAILED`。
接口鉴权与完整请求示例详见 [Fun-ASR录音文件识别HTTP API参考](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/fun-asr-recorded-speech-recognition-http-api.md)。

## 限制与注意事项
1. **文件体积与时长**：单次录音文件限制为 2GB 且时长 ≤12 小时。若启用说话人分离（`diarization_enabled`），建议时长压缩至 2 小时内，否则可能触发处理中断。
2. **URL 协议限制**：服务不支持本地文件直传或 Base64 编码音频。SDK 调用时**不支持** `oss://` 协议的临时链接，必须使用完整的 HTTP/HTTPS 公网 URL；仅 RESTful API 底层兼容 `oss://` 临时凭证（有效期 48 小时，严禁用于高并发生产环境）。
3. **并发与限流**：文件上传凭证接口限流 100 QPS 且不可扩容。生产环境应统一使用稳定对象存储（如阿里云 OSS）预生成签名 URL。
4. **队列排队机制**：文件转写服务采用尽力调度策略，任务提交后进入 `PENDING` 状态，排队时长受当前集群负载与音频长度影响，通常为数分钟至数十分钟。识别结果与下载链接仅保留 24 小时，请及时落库。

## 来源文档

- [录音文件识别（Qwen-ASR）API参考](../../raw/model-api-reference/speech-recognition-api-reference/qwen-asr-api-reference.md)
- [Paraformer实时语音识别WebSocket API](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/websocket-for-paraformer-real-time-service.md)
- [实时语音识别（Paraformer）服务端事件](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/paraformer-server-events.md)
- [Paraformer实时语音识别Java SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/paraformer-real-time-speech-recognition-java-sdk.md)
- [实时语音识别（Paraformer）客户端事件](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/paraformer-client-events.md)
- [Paraformer实时语音识别Python SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/paraformer-real-time-speech-recognition-python-sdk.md)
- [Paraformer实时语音识别Android SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/android-sdk-for-paraformer-real-time-service.md)
- [Fun-ASR实时语音识别WebSocket API](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/fun-asr-realtime-websocket-api.md)
- [实时语音识别（Fun-ASR）客户端事件](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/fun-asr-client-events.md)
- [Paraformer实时语音识别iOS SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/ios-sdk-for-paraformer-real-time-service.md)
- [实时语音识别（Fun-ASR）服务端事件](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/fun-asr-server-events.md)
- [Python SDK](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/fun-asr-realtime-python-sdk.md)
- [Java SDK](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/fun-asr-realtime-java-sdk.md)
- [Fun-ASR实时语音识别Android SDK](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/android-sdk-for-fun-asr-real-time-service.md)
- [Qwen-ASR实时语音识别WebSocket API](../../raw/model-api-reference/speech-recognition-api-reference/qwen-asr-realtime-api/qwen-asr-realtime-interaction-process.md)
- [Fun-ASR实时语音识别iOS SDK](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-real-time-speech-recognition-api-reference/ios-sdk-for-fun-asr-real-time-service.md)
- [实时语音识别（Qwen-ASR-Realtime）Java SDK-API参考](../../raw/model-api-reference/speech-recognition-api-reference/qwen-asr-realtime-api/qwen-asr-realtime-java-sdk.md)
- [实时语音识别（Qwen-ASR-Realtime）Python SDK-API参考](../../raw/model-api-reference/speech-recognition-api-reference/qwen-asr-realtime-api/qwen-asr-realtime-python-sdk.md)
- [实时语音识别（Qwen-ASR-Realtime）服务端事件](../../raw/model-api-reference/speech-recognition-api-reference/qwen-asr-realtime-api/qwen-asr-realtime-server-events.md)
- [实时语音识别（Qwen-ASR-Realtime）客户端事件](../../raw/model-api-reference/speech-recognition-api-reference/qwen-asr-realtime-api/qwen-asr-realtime-client-events.md)
- [Paraformer录音文件识别Java SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-recorded-speech-recognition-api-reference/paraformer-recorded-speech-recognition-java-sdk.md)
- [Paraformer录音文件识别Python SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-recorded-speech-recognition-api-reference/paraformer-recorded-speech-recognition-python-sdk.md)
- [Paraformer录音文件识别RESTful API](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-recorded-speech-recognition-api-reference/paraformer-recorded-speech-recognition-restful-api.md)
- [最佳实践](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-recorded-speech-recognition-api-reference/paraformer-best-practices.md)
- [Paraformer录音文件识别Android SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-recorded-speech-recognition-api-reference/paraformer-recorded-speech-recognition-android-sdk.md)
- [Paraformer录音文件识别iOS SDK](../../raw/model-api-reference/speech-recognition-api-reference/paraformer-recorded-speech-recognition-api-reference/paraformer-recorded-speech-recognition-ios-sdk.md)
- [Fun-ASR录音文件识别Python SDK](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/funauidio-asr-recorded-speech-recognition-python-sdk.md)
- [Fun-ASR录音文件识别HTTP API参考](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/fun-asr-recorded-speech-recognition-http-api.md)
- [Fun-ASR录音文件识别Java SDK](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/fun-asr-recorded-speech-recognition-java-sdk.md)
- [Fun-ASR录音文件识别Android SDK](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/fun-asr-recorded-speech-recognition-android-sdk.md)
- [Fun-ASR录音文件识别iOS SDK](../../raw/model-api-reference/speech-recognition-api-reference/fun-asr-recorded-speech-recognition-api-reference/fun-asr-recorded-speech-recognition-ios-sdk.md)
- [定制热词Java SDK参考](../../raw/model-api-reference/speech-recognition-api-reference/custom-hot-words/vocabulary-java-sdk.md)
- [定制热词HTTP API参考](../../raw/model-api-reference/speech-recognition-api-reference/custom-hot-words/vocabulary-http-api.md)
- [定制热词Python SDK参考](../../raw/model-api-reference/speech-recognition-api-reference/custom-hot-words/vocabulary-python-sdk.md)

