# [more](more.md) about models

百炼平台提供丰富的模型调用能力，覆盖同步/异步任务、多模态文件处理、子空间隔离、连接优化及实时音视频交互等场景。开发者需根据模型类型（如文本生成、图像生成、实时ASR/TTS）选择对应API机制，并注意权限、地域、时效性等关键约束。

## 支持的模型/功能

- **标准与调优模型**：`qwen-plus` 等标准模型需在子业务空间中[设置模型调用权限](../../model-user-guide/security-and-compliance/permission-management-overview.md#f642213a1f38l)；而[调优并部署的模型](../../model-user-guide/model-training/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)仅限其所在业务空间的 API Key 调用，且不支持 OpenAI 兼容方式 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。
- **异步任务模型**：图像生成、视频生成等长耗时模型采用异步机制，需先创建任务再轮询或接收事件通知 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。
- **实时多模态模型**：`Qwen-Omni-Realtime`、`Qwen-Audio-Realtime` 等通过 AOQ SDK 或 WebSocket 协议接入，支持自定义音视频采集/播放、屏幕共享等深度控制能力 [AOQ SDK 简介](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)。
- **多模态交互协议**：基于 WebSocket 的低延迟全双工通信，适用于语音识别（Paraformer、FunASR、qwen3-asr-flash-realtime）和语音合成（cosyvoice-v3.5-flash 等）场景 [多模态交互开发套件](../../raw/model-api-reference/more-about-models/multimodal-interaction-protocol.md)。

> **注意**：文档 25 中列出的 `cosyvoice-v3-plus`、`cosyvoice-v3.5-plus` 等语音合成模型链接指向通用帮助页（`https://help.aliyun.com/zh/model-studio/text-to-speech`），未提供具体 API 文档，实际调用前请以控制台模型列表及最新 SDK 示例为准。

## 关键参数

- **临时 API Key 有效期**：默认 60 秒，可通过 `expire_in_seconds` 参数设置为 \[1, 1800\] 秒，过期后自动失效且不可手动删除 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。
- **异步任务保留期**：任务完成后通常保留 24 小时，超时后系统自动清理，具体以各任务文档为准 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。
- **临时文件 URL 有效期**：上传至百炼临时存储的文件 URL 有效期为 48 小时，过期后无法使用，**严禁用于生产环境** [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
- **连接池配置（Java SDK）**：`connectionPoolSize`（默认 32）、`maximumAsyncRequests`（默认 32）等参数需根据并发量合理调整，过高可能压垮服务端，过低则导致阻塞 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。

## 使用方式

- **安全调用**：在浏览器、App 等不可信环境，必须通过后端服务生成临时 API Key，避免永久 Key 泄露；客户端不得硬编码 API Key [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。
- **异步任务轮询**：查询单个任务结果接口限流 20 QPS，建议按任务类型设置合理间隔（文本向量可短，图像/视频宜长），避免触发限流 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。
- **异步任务通知**：高并发场景推荐配置 HTTP 回调 URL 或 RocketMQ 接收事件总线推送，避免轮询资源浪费与限流风险 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。
- **文件上传与引用**：调用多模态模型前，需先上传文件获取 `oss://` 开头的临时 URL，并确保该 URL 与后续模型调用使用的 `model_name` 完全一致 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
- **AOQ 实时流控制**：对于要求严格时序的模型（如部分实时 ASR），必须在收到 `session.updated` 事件后，再调用 `enableSendMediaStream(true)` 启动媒体流发送，否则模型可能拒绝接收数据 [媒体流发送管理](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)。

## 限制和注意事项

- **地域隔离**：北京、新加坡、弗吉尼亚、中国香港等地域的 API Key 互不通用，Endpoint 也需匹配对应地域 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。
- **文件绑定约束**：上传文件时指定的 `model_name` 必须与后续模型调用的模型完全一致，且文件仅限同一主账号下使用，不同模型或跨账号不可共享 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
- **临时存储限流**：文件上传凭证接口限流为 100 QPS（按“主账号+模型”维度），且不支持扩容，**禁止用于生产环境、高并发及压测场景**，生产环境应使用 OSS [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
- **AOQ 平台差异**：Linux C++ SDK 的 `startAudioCapture`/`startAudioPlayer` 为空实现，无实际设备操作；Windows/macOS/iOS/Android 等平台则提供完整音视频设备控制能力，选型时需注意功能边界 [AOQ Client SDK Linux C++ API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-linux-cpp-sdk-reference.md)。

## 来源文档

- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [AOQ SDK](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api.md)
- [SDK 下载](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-sdk-download.md)
- [AOQ Client SDK Windows API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-windows-sdk-reference.md)
- [AOQ Client SDK macOS API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-macos-sdk-reference.md)
- [AOQ SDK 简介](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [AOQ Client SDK Electron API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-electron-sdk-reference.md)
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
- [AOQ Client SDK Linux C++ API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-linux-cpp-sdk-reference.md)
- [AOQ Client SDK Linux Python API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-linux-python-sdk-reference.md)


