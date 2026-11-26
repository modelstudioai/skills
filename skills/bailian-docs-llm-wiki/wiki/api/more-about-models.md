# [more](more.md) about models

阿里云百炼平台提供多样化的模型调用能力，覆盖同步/异步推理、实时多模态交互、子空间隔离、连接复用及安全凭证管理等核心场景。开发者需根据任务类型（如文本生成、图像/视频生成、实时语音对话）选择适配的模型接口、SDK 和调用模式，并严格遵循各模型的参数约束与生命周期管理规范。

## 支持的模型/功能

百炼支持三类主要模型调用路径：  
- **标准大模型（如 `qwen-plus`、`qwen3-vl-plus`）**：通过 HTTP 或 OpenAI 兼容方式调用，适用于文本生成、多模态理解等场景；调用前需确保模型在对应业务空间已授权 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。  
- **异步长耗时模型（如文生图、文生视频）**：采用任务制流程，需先创建任务获取 `task_id`，再轮询或通过事件总线接收结果通知 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。  
- **实时多模态模型（如 `Qwen-Omni-Realtime`、`Qwen-Audio-Realtime`）**：依赖 AOQ SDK 实现低延迟音视频流处理，不支持纯 HTTP 调用，必须通过平台专属 SDK 接入 [AOQ SDK 简介](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)。  
> **注意**：文档 4 明确指出“调用在阿里云百炼调优并部署的模型，无需模型调用授权”，但文档 29（iOS SDK 参考）和文档 25（视频常用功能）均强调 `Qwen-Audio-Realtime` 不支持视频输入/输出，而文档 6、8–17、24–25 多次重申该限制，属一致描述，非矛盾。

## 关键参数

| 参数 | 说明 | 示例值 | 来源依据 |
|------|------|--------|----------|
| `task_id` | 异步任务唯一标识，用于查询结果 | `a8532587-xxxx-xxxx-xxxx-0c46b17950d1` | [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) |
| `model` | 模型名称，上传文件时必须与调用模型一致 | `qwen3-vl-plus` | [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) |
| `expire_in_seconds` | 临时 API Key 有效期，范围 [1, 1800] 秒 | `1800` | [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md) |
| `trackType` | AOQ 媒体流控制参数，取值 `.audio` 或 `.video` | `.audio` | [媒体流发送管理](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md) |

## 使用方式

- **异步任务轮询**：调用 `GET /api/v1/tasks/{task_id}` 查询状态，建议按任务类型设置合理间隔（文本向量可短间隔，图像/视频宜长间隔），避免触发 20 QPS 限流 [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。  
- **异步任务通知**：配置事件总线 HTTP 回调 URL 或 RocketMQ，由系统主动推送 `任务完成事件`，规避轮询资源消耗与限流风险 [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)。  
- **实时模型接入**：必须使用 AOQ SDK（Windows/macOS/Electron/Android/iOS/HarmonyOS/Web 等全平台支持），通过 `enableSendMediaStream(.audio, true)` 等 API 精确控制媒体流启停，并在收到 `session.updated` 后开启发送 [媒体流发送管理](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)。  
- **子空间模型调用**：使用子业务空间的 API Key，并配置对应 `base_url`（如北京地域为 `https://dashscope.aliyuncs.com/compatible-mode/v1`），不可混用默认空间凭证 [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)。  

## 限制和注意事项

- **文件上传限制**：临时 URL 有效期仅 48 小时，且文件与模型强绑定、与主账号强绑定；生产环境严禁使用，应迁移到 OSS 等长期存储 [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。  
- **临时 API Key 限制**：无法手动删除，到期自动失效；其权限继承自生成它的永久 API Key，需谨慎管控源密钥权限 [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。  
- **AOQ 平台差异**：Linux C++ SDK 的 `startAudioCapture`/`startAudioPlayer` 为“空实现”，而 Android/iOS/macOS 等平台为真实设备操作；调用前须确认目标平台能力边界 [AOQ Client SDK Linux C++ API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-linux-cpp-sdk-reference.md)。  
- **连接复用配置**：Java SDK 默认启用连接池，Python SDK 需传入自定义 HTTP 客户端；高并发下需调优 `connectionPoolSize` 与 `maximumAsyncRequests`，避免阻塞或服务端过载 [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)。

## 来源文档

- [异步任务管理 API](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)
- [生成临时API Key](../../raw/model-api-reference/more-about-models/generate-temporary-api-key.md)
- [通过HTTP回调URL或MQ接收异步任务完成通知](../../raw/model-api-reference/more-about-models/async-task-api.md)
- [子业务空间的模型调用](../../raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)
- [AOQ SDK](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api.md)
- [AOQ SDK 简介](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [SDK 下载](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-sdk-download.md)
- [AOQ Client SDK Windows API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-windows-sdk-reference.md)
- [AOQ Client SDK macOS API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-macos-sdk-reference.md)
- [AOQ Client SDK Electron API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-electron-sdk-reference.md)
- [AOQ Client SDK Linux C++ API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-linux-cpp-sdk-reference.md)
- [DashScope SDK连接复用配置](../../raw/model-api-reference/more-about-models/connection-multiplexing-configuration.md)
- [AOQ Client SDK Linux Python API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-linux-python-sdk-reference.md)
- [上传本地文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)
- [AOQ Client SDK Android API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-android-sdk-reference.md)
- [AOQ Client SDK OHOS (HarmonyOS) API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-harmony-sdk-reference.md)
- [AOQ Web SDK API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-web-sdk-reference.md)
- [功能参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-function.md)
- [连接状态管理](../../raw/_short/aoq-connection-management-b3a43f4f91587453.md)
- [媒体流发送管理](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [音频常用功能介绍](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频播放](../../raw/_short/aoq-custom-audio-playback-7832b33ccf014535.md)
- [自定义音频采集](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [自定义视频输入](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)
- [视频常用功能介绍](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [C# 语音 SDK](../../raw/model-api-reference/more-about-models/csharp-speech-sdk.md)
- [SDK 简介](../../raw/model-api-reference/more-about-models/csharp-speech-sdk/csharp-sdk.md)
- [C# SDK 接口与事件](../../raw/model-api-reference/more-about-models/csharp-speech-sdk/csharp-sdk-methods-and-events.md)
- [AOQ Client SDK iOS API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-ios-sdk-reference.md)
- [移动端语音 SDK 选型与下载](../../raw/model-api-reference/more-about-models/sdk-selection-and-download.md)


