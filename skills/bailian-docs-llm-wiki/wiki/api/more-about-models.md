# more about models

百炼平台提供丰富的模型调用能力，覆盖同步/异步任务、多模态交互、实时音视频、连接复用及安全鉴权等核心场景。开发者需根据模型类型（如文本生成、图像生成、实时ASR/TTS）选择对应调用方式，并严格遵循权限、地域、时效性等约束条件。

## 支持的模型/功能

- **异步模型**：图像生成、视频生成等长耗时任务需通过异步任务管理 API 调用，支持单任务查询、批量状态轮询及任务取消（仅限排队中任务）[异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。
- **实时多模态模型**：Qwen-Omni-Realtime、Qwen-Audio-Realtime、Qwen-LiveTranslate-Realtime 等模型通过 AOQ SDK 接入，提供低延迟音视频流与数据消息能力 [AOQ SDK 简介](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)。
- **WebSocket 多模态交互**：支持 Paraformer、FunASR、qwen3-asr-flash-realtime 等语音识别模型，以及 cosyvoice-v2/v3/v3.5 系列语音合成模型，基于 WebSocket 协议实现全双工实时交互 [多模态交互开发套件](../../raw/model-api-reference/more-about-models/multimodal-interaction-protocol.md)。
- **子业务空间模型**：支持在非默认业务空间中调用标准模型（如 `qwen-plus`）或调优部署模型，适用于权限隔离与费用分账场景 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。

> **注意**：文档 4 中指出“调用在阿里云百炼调优并部署的模型，无需模型调用授权”，但文档 26 的前提条件强调“客户端处理 API Key 有安全风险，建议从服务端获取临时 [Token](../concepts/token.md)”。二者逻辑冲突——调优模型虽免授权，但仍需安全鉴权；实际应统一采用临时 API Key 或服务端代理鉴权，避免客户端硬编码或直接暴露主账号凭证。

## 关键参数

- **临时 API Key TTL**：有效期范围为 `[1, 1800]` 秒，默认 60 秒，由 `expire_in_seconds` 参数控制 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。
- **文件上传有效期**：通过 `get-temporary-file-url` 接口上传的文件 URL 有效期固定为 **48 小时**，超期自动失效，不可续期。
- **异步任务保留期**：任务完成后通常保留 24 小时（具体以对应任务文档为准），超时后系统自动清理。
- **连接池参数（Java SDK）**：`connectionPoolSize`（默认 32）、`maximumAsyncRequests`（默认 32）、`readTimeout`（默认 300 秒）等可调优，高并发场景需按业务负载合理配置 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。

## 使用方式

- **异步任务推荐模式**：优先使用事件总线（EventBridge）接收 HTTP 回调或 RocketMQ 通知，避免轮询触发 20 QPS 限流；若必须轮询，需按任务类型设置合理间隔（如文生图建议 ≥2s）[通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。
- **本地文件输入**：调用多模态模型前，须先调用 `POST /api/v1/uploads?action=getPolicy` 获取上传策略，再上传文件获得 `oss://` 开头的临时 URL，**该 URL 必须与模型名称严格绑定且不可跨模型复用** [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
- **实时模型媒体流控制**：必须在收到 `session.updated` 消息后，再调用 `enableSendMediaStream(.audio, true)` 启动媒体发送，否则模型可能拒绝接收数据 [媒体流发送管理](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)。
- **子空间模型调用**：必须使用该子业务空间生成的 API Key，并确保已为其授予对应模型调用权限（标准模型）或确认模型已部署于该空间（调优模型）。

## 限制和注意事项

- **临时 API Key 安全边界**：继承生成者 API Key 的全部权限（含知识库访问限制），且**各地域 API Key 不互通**（北京、新加坡、弗吉尼亚、中国香港需分别创建）。
- **文件上传生产禁用**：临时文件存储接口限流为 100 QPS（按“主账号+模型”维度），且 URL 48 小时过期，**明确禁止用于生产环境、高并发及压测场景**；生产环境应使用 OSS 等持久化存储 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
- **AOQ 平台能力差异**：
  - Linux C++ SDK 的 `startAudioCapture` 和 `startAudioPlayer` 为空实现，不支持内部采集/播放；
  - iOS/macOS 需额外集成 `AoqPluginOpus` 插件启用 Opus 编解码；
  - Web SDK 依赖 WebTransport（HTTP/3）和 HTTPS 安全上下文，需调用 `isAoqSupported()` 检查浏览器兼容性。
- **Qwen-Audio-Realtime 限制**：明确不支持视频输入或输出，所有视频相关接口（如 `startVideoCapture`、`setLocalView`）在此模型下无效，详见各平台 SDK 参考文档头部说明。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [AOQ SDK](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api.md)
- [AOQ SDK 简介](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [SDK 下载](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-sdk-download.md)
- [AOQ Client SDK Windows API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-windows-sdk-reference.md)
- [AOQ Client SDK macOS API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-macos-sdk-reference.md)
- [AOQ Client SDK Electron API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-electron-sdk-reference.md)
- [AOQ Client SDK Linux C++ API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-linux-cpp-sdk-reference.md)
- [AOQ Client SDK Linux Python API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-linux-python-sdk-reference.md)
- [AOQ Client SDK iOS API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-ios-sdk-reference.md)
- [AOQ Client SDK OHOS (HarmonyOS) API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-harmony-sdk-reference.md)
- [AOQ Web SDK API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-web-sdk-reference.md)
- [连接状态管理](../../raw/_short/aoq-connection-management-b3a43f4f91587453.md)
- [功能参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-function.md)
- [音频常用功能介绍](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [媒体流发送管理](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [自定义音频采集](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [自定义音频播放](../../raw/_short/aoq-custom-audio-playback-7832b33ccf014535.md)
- [视频常用功能介绍](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义视频输入](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)
- [多模态交互开发套件](../../raw/model-api-reference/more-about-models/multimodal-interaction-protocol.md)
- [AOQ Client SDK Android API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-android-sdk-reference.md)


