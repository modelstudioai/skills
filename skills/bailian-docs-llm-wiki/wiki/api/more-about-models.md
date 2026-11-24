# [more](more.md) about models

阿里云百炼平台提供多样化的模型调用能力，覆盖同步/异步推理、实时多模态交互、子空间隔离、文件上传与连接复用等关键场景。本文面向开发者，系统梳理模型服务的核心能力、参数配置、使用方式及约束条件，帮助您高效、安全地集成模型能力。

## 支持的模型/功能

百炼支持三类主流调用模式：  
- **同步模型**（如 `qwen-plus`、`qwen3`）：通过 HTTP 或 SDK 直接调用，适用于低延迟文本生成任务；  
- **异步模型**（如图像生成、视频生成、长音频转录）：需先提交任务获取 `task_id`，再轮询或通过事件总线接收结果通知，详见[异步任务管理 API](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)；  
- **实时流式模型**（如 `Qwen-Omni-Realtime`、`Qwen-Audio-Realtime`）：基于 WebSocket 或 AOQ SDK 实现端到端低延迟音视频交互，不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)。  

> **注意**：`Qwen-Audio-Realtime` 明确不支持视频输入或输出，该限制在所有平台 SDK 文档中一致强调（如 [AOQ SDK 简介](raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)、[AOQ Client SDK Windows API 参考](raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-windows-sdk-reference.md) 等），无矛盾。

实时交互场景推荐使用 **AOQ SDK**，其提供跨平台（Windows/macOS/Electron/Linux C++/Python/Android/iOS/HarmonyOS/Web）统一 API，封装连接管理、媒体流控制、3A 处理、帧级回调等能力，并支持自定义采集/播放、屏幕共享等高级功能。详细接口请参见各平台参考文档，例如 [AOQ Client SDK Android API 参考](raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-android-sdk-reference.md)。

## 关键参数

| 参数 | 说明 | 典型取值/范围 | 注意事项 |
|------|------|----------------|----------|
| `expire_in_seconds` | 临时 API Key 有效期 | `[1, 1800]` 秒（默认 60） | 用于不可信环境，继承源 Key 权限，不可手动删除 |
| `task_id` | 异步任务唯一标识 | UUID 字符串 | 查询结果接口限流 20 QPS，建议按任务类型设置合理轮询间隔 |
| `model_name` | 文件上传时指定的模型名 | 如 `qwen3-vl-plus` | 文件与模型强绑定，不同模型无法共享同一临时 URL |
| `connectionPoolSize` | Java SDK 连接池大小 | 默认 32，高并发建议调优 | 过低易阻塞，过高可能压垮服务端；需同步调整 `maximumAsyncRequests` |
| `enableSendMediaStream` | AOQ 媒体流发送开关 | `true`/`false`（按 `trackType` 独立控制） | 模型要求先收到 `session.updated` 后再开启，否则可能被拒绝 |

## 使用方式

### 1. 安全调用（客户端场景）
在浏览器或移动 App 等不可信环境，**禁止硬编码永久 API Key**。应由可信后端调用 [生成临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md) 接口，获取带 TTL 的 `st-***` [Token](../concepts/token.md) 下发至前端，避免密钥泄露风险。

### 2. 异步任务结果获取
- **轮询方式**：调用 `GET /api/v1/tasks/{task_id}`，注意遵守 20 QPS 限流，对图像/视频类任务建议间隔 ≥5s；  
- **事件驱动方式**：配置 HTTP 回调 URL 或 RocketMQ 到事件总线，由百炼主动推送 `任务完成事件`，规避轮询资源浪费和限流问题，详见[通过HTTP回调URL或MQ接收异步任务完成通知](raw/model-api-reference/more-about-models/async-task-api.md)。

### 3. 多模态文件处理
调用多模态模型（如 `qwen3-vl-plus`）前，需先上传本地文件获取临时 OSS URL：  
- 调用 `GET /api/v1/uploads?action=getPolicy&model={model_name}` 获取上传凭证；  
- 使用凭证将文件上传至临时存储（有效期 48 小时）；  
- 在模型请求中传入返回的 `oss://` URL。  
> **注意**：该功能限流 100 QPS（按主账号+模型维度），且文件仅限同主账号下使用，**严禁用于生产环境或压测**；生产环境请使用阿里云 OSS。

### 4. 连接优化
高并发调用时，启用连接复用可显著降低延迟与资源消耗：  
- **Java SDK**：直接配置 `ConnectionConfigurations`（如 `connectionPoolSize=64`, `readTimeout=300`）；  
- **Python SDK**：传入自定义 `httpx.Client` 或 `aiohttp.ClientSession` 复用连接池。

## 限制和注意事项

- **地域隔离**：北京、新加坡、弗吉尼亚、中国香港四地 API Key **完全独立**，Endpoint 和鉴权 [Token](../concepts/token.md) 不互通，调用前务必确认地域配置；  
- **子空间权限**：子业务空间的 API Key 调用标准模型（如 `qwen-plus`）前，必须在控制台[设置模型调用权限](https://help.aliyun.com/zh/model-studio/permission-management-overview#f642213a1f38l)；调优部署的私有模型则无需额外授权，但仅限本空间 Key 调用；  
- **临时文件生命周期**：上传的文件 48 小时后自动清理，且无法查询、修改或下载，仅能作为 URL 参数在模型请求中一次性使用；  
- **AOQ 初始化约束**：`enableSendMediaStream` 必须在 `createEngine` 之后、`connect` 之前调用；若未显式调用，默认 `connect` 成功后立即发送媒体流，可能违反部分模型的 `session.updated` 就绪协议；  
- **WebSocket 安全要求**：多模态 WebSocket (`wss://dashscope.aliyuncs.com/api-ws/v1/inference`) 要求 TLS 1.2+、启用 SNI，并信任 GlobalSign Root CA - R46 证书。

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
- [AOQ Client SDK Android API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-android-sdk-reference.md)
- [AOQ Client SDK iOS API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-ios-sdk-reference.md)
- [AOQ Client SDK OHOS (HarmonyOS) API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-harmony-sdk-reference.md)
- [AOQ Web SDK API 参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/aoq-web-sdk-reference.md)
- [功能参考](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-function.md)
- [连接状态管理](../../raw/_short/aoq-connection-management-b3a43f4f91587453.md)
- [媒体流发送管理](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [自定义音频播放](../../raw/_short/aoq-custom-audio-playback-7832b33ccf014535.md)
- [音频常用功能介绍](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频采集](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [视频常用功能介绍](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义视频输入](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)
- [多模态交互开发套件](../../raw/model-api-reference/more-about-models/multimodal-interaction-protocol.md)


