# [more](more.md) about models

百炼平台提供多种模型调用方式与配套能力，覆盖同步/异步任务、多模态文件处理、子空间隔离、连接优化及实时音视频交互等核心场景。开发者需根据业务需求选择合适的技术路径，并严格遵循权限、地域、时效性等约束条件。

## 支持的模型/功能

- **异步模型**：图像生成、视频生成、长文本处理等耗时操作采用异步模式，需先创建任务获取 `task_id`，再轮询或通过事件总线接收结果通知。[通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md) 提供了免轮询的高可靠方案。
- **实时多模态模型**：基于 WebSocket 的 `Qwen-Omni-Realtime`、`Qwen-Audio-Realtime` 等模型支持语音识别（ASR）、语音合成（TTS）、实时翻译等能力，要求客户端在收到 `DialogStateChanged` 且 `state=Listening` 后才可发送音频流。[多模态交互开发套件](../../raw/model-api-reference/more-about-models/multimodal-interaction-protocol.md) 明确了该关键时序约束。
- **AOQ SDK 支持的实时模型**：包括 `Qwen-Omni-Realtime`、`Qwen-Audio-Realtime` 和 `Qwen-LiveTranslate-Realtime`，各平台 SDK（Windows/macOS/Android/iOS/Web 等）均提供统一 API 抽象，但需注意 `Qwen-Audio-Realtime` 不支持视频输入或输出。[AOQ SDK 简介](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md) 汇总了各模型的媒体能力边界。

> **注意**：文档 25 与文档 27 均列出 `Qwen-Audio-Realtime`，但文档 25 在“语音识别支持的模型”列表中错误地将其与 Paraformer、FunASR 等并列作为 ASR 模型；而文档 27 及所有 AOQ SDK 参考文档（如文档 8–16）一致强调其**不支持视频输入或输出**，且其核心定位是端到端实时语音交互，非通用 ASR 引擎。实际使用应以文档 27 及各 SDK 参考为准，避免将 `Qwen-Audio-Realtime` 误用于纯离线 ASR 场景。

## 关键参数

- **临时 API Key 有效期（TTL）**：默认 60 秒，可通过 `expire_in_seconds` 参数设置，范围为 [1, 1800] 秒。该 Key 继承生成它的永久 Key 的全部权限。[生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) 明确了此安全机制。
- **异步任务查询限流**：20 QPS（每秒每个主账号），超限将触发限流。建议按任务类型设置合理查询间隔（如图像生成任务间隔 ≥ 2 秒）。[异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 提供了具体指导。
- **文件上传有效期**：通过临时存储上传的文件 URL 有效期为 48 小时，过期后无法使用。生产环境必须使用 OSS 等长期存储方案。[上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 多次强调此限制。

## 使用方式

- **子业务空间调用**：需使用该子空间专属的 API Key，并确保已为其配置对应模型的调用权限（标准模型需显式授权，调优模型仅限本空间调用）。OpenAI 兼容方式仅支持标准模型，不支持调优模型。[子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md) 给出了完整流程。
- **连接复用**：高并发场景下，Java SDK 默认启用连接池，Python SDK 需传入自定义 HTTP 客户端；推荐调整 `connectionPoolSize`（默认 32）和 `connectionIdleTimeout`（默认 300 秒）以匹配业务负载。[DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md) 提供了参数说明与示例。
- **实时音视频控制**：必须遵循“先禁用、后开启”原则——连接前调用 `enableSendMediaStream(false)`，待收到 `session.updated` 消息后再调用 `enableSendMediaStream(true)`，否则模型可能因未就绪而丢弃媒体流。[媒体流发送管理](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md) 是该流程的权威依据。

## 限制和注意事项

- **地域隔离**：北京、新加坡、弗吉尼亚、中国香港四地的 API Key 互不通用，Endpoint 也不同。调用前必须确认 Key 与 Endpoint 地域一致，否则返回 `InvalidApiKey` 错误。[生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) 和 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 均明确指出此要点。
- **临时文件限制**：上传凭证接口限流为 100 QPS（按“主账号+模型”维度），且不支持扩容；文件大小上限 1GB，但不同模型对输入文件有额外限制；文件仅限同一主账号下使用。[上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 将其列为“重要”警告。
- **AOQ 平台能力差异**：Linux C++ SDK 的 `startAudioCapture`/`stopAudioCapture` 为空实现，`setLocalView`/`setRemoteView` 无渲染实现；Web SDK 依赖 WebTransport 和 HTTPS；HarmonyOS SDK 通过 NAPI 桥接。跨平台开发时须查阅对应平台的 [API 参考文档](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-windows-sdk-reference.md)（如文档 8–16），不可假设接口行为完全一致。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [SDK 下载](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-sdk-download.md)
- [AOQ Client SDK Windows API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-windows-sdk-reference.md)
- [AOQ Client SDK macOS API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-macos-sdk-reference.md)
- [AOQ Client SDK Electron API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-electron-sdk-reference.md)
- [AOQ Client SDK Linux C++ API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-linux-cpp-sdk-reference.md)
- [AOQ Client SDK Linux Python API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-linux-python-sdk-reference.md)
- [AOQ Client SDK Android API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-android-sdk-reference.md)
- [AOQ Client SDK iOS API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-ios-sdk-reference.md)
- [AOQ Client SDK OHOS (HarmonyOS) API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-harmony-sdk-reference.md)
- [AOQ Web SDK API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-web-sdk-reference.md)
- [功能参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-function.md)
- [连接状态管理](../../raw/_short/aoq-connection-management-b3a43f4f91587453.md)
- [媒体流发送管理](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [音频常用功能介绍](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频播放](../../raw/_short/aoq-custom-audio-playback-7832b33ccf014535.md)
- [自定义音频采集](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [视频常用功能介绍](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义视频输入](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)
- [多模态交互开发套件](../../raw/model-api-reference/more-about-models/multimodal-interaction-protocol.md)
- [AOQ SDK](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api.md)
- [AOQ SDK 简介](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)


