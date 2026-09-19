# realtime api user guide

Realtime API 是百炼平台提供的低延迟、高可靠实时交互能力接口，支持 AOQ、WebRTC 和 WebSocket 三种传输协议，面向[多模态](../concepts/multimodal.md)语音对话、实时语音识别/合成、语音翻译等场景。开发者可根据终端平台、网络环境、功能需求和接入成本选择最适配的协议方案，并通过统一 [Token](../concepts/token.md) 鉴权与标准化会话配置快速集成。

## 支持的模型/功能

Realtime API 当前支持以下核心模型与应用类型，但**协议支持存在显著差异**：

- **全模态实时交互**：`qwen3.5-omni-plus-realtime` 和 `qwen3.5-omni-flash-realtime` 均支持 AOQ、WebRTC 和 WebSocket [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。
- **实时语音翻译**：`qwen3.5-livetranslate-flash-realtime` 同样三协议全支持。
- **[多模态](../concepts/multimodal.md)开发套件**（如 `multimodal-dialog`）：三协议均支持。
- **实时语音识别（ASR）**：仅 AOQ 和 WebSocket 支持 `Qwen-Audio-3.0-ASR-Flash-Streaming` 及 `Fun-ASR-Realtime` 系列；**WebRTC 不支持 ASR 模型** [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。
- **实时语音合成（TTS）**：仅 AOQ 和 WebSocket 支持 `CosyVoice`、`qwen-audio-3.0-tts-flash` 等系列；**WebRTC 不支持 TTS 模型**。
- **实时语音对话**：`qwen-audio-3.0-realtime-plus` 等模型三协议全支持。

> **注意**：文档 1 明确指出 WebRTC 协议对 ASR 和 TTS 模型“不支持”，但部分旧版文档或示例代码可能未同步此限制。请以 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 的表格为准。

## 关键参数

### 协议选择参数
- `x-dashscope-rtc-transport`：HTTP 请求头中指定协议，值为 `moq`（AOQ）、`webrtc`（WebRTC）或 `websocket`（WebSocket）。

### AOQ 连接凭证（由服务端 `/api/v1/allocate` 接口返回）
- `aoqTokenForClient`：客户端 SDK 初始化时必需的连接令牌。
- `sid`：会话唯一标识符。
- `clientRelayEndpoints`：Relay 接入点数组（含 `endpoint` 和 `port`）。
- `clientRelayCertFingerprint`：Relay TLS 证书指纹（SHA256）。
- `sidExpiresInSecs`：会话过期时间（秒），默认 7200。

### 会话配置（`session.update` 事件）
- `modalities`：输出模态列表，如 `["text"]` 或 `["text", "audio"]`。
- `voice`：TTS 音色名称（如 `"Ethan"`）。
- `input_audio_format` / `output_audio_format`：当前仅支持 `"pcm"`。
- `instructions`：系统角色提示词。
- `turn_detection`：语音活动检测（VAD）配置对象（可选）。

## 使用方式

### 1. 鉴权与建连
所有协议均在**建连阶段**通过 `Authorization: Bearer <API_KEY>` 完成鉴权，连接建立后数据传输无需重复鉴权 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。  
- **AOQ**：业务 AppServer 调用 `/api/v1/allocate` 获取临时凭证，客户端 SDK 使用 `aoqTokenForClient` 等参数连接 Relay。
- **WebRTC**：客户端或服务端在 SDP 交换 HTTP 请求中携带 API Key。
- **WebSocket**：客户端在 WebSocket 握手请求中携带 API Key。

### 2. SDK 集成（以 AOQ 为例）
- 下载对应平台 SDK（Android/iOS/HarmonyOS/Windows/macOS/Electron/Linux）[SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)。
- 创建引擎并设置 `AoqEngineDelegate` 回调监听连接状态。
- **关键实践**：为避免模型未就绪即接收媒体流，应在 `connect()` 前调用 `enableSendMediaStream(.audio, false)` 暂停发送，待收到 `session.updated` 事件后再启用 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)。

### 3. 模型接入
通过 `session.update` 事件配置会话参数后，即可开始双向实时交互。各协议的具体连接流程、时序图及代码示例详见 [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)。

## 限制和注意事项

- **协议兼容性限制**：WebRTC 协议**不支持**实时语音识别（ASR）和实时语音合成（TTS）模型，仅支持全模态对话、翻译及[多模态](../concepts/multimodal.md)套件。此限制在 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中明确列出，开发者需规避误用。
- **Linux 平台能力受限**：Linux 版 AOQ SDK 的音频采集/播放为“空实现”，无设备控制能力；视频渲染亦无实现，仅支持外部视频帧输入与推流 [AOQ Client SDK Linux Python API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-linux-python-sdk-reference.md)。
- **API Key 安全**：API Key **严禁硬编码于客户端**，必须通过服务端代理下发或环境变量管理 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。
- **连接状态管理**：`onConnectionStatusChange` 回调中的 `Failed` 状态为瞬态，SDK 会自动迁移至 `Disconnected`，业务层无需主动调用 `disconnect` [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)。
- **自定义音视频流**：若需自定义采集或播放，须显式设置 `isExternal = true` 并通过 `pushAudioExternalStreamData` 或 `pushExternalVideoCapturedFrame` 推送数据，同时注意 `enable3A` 等处理选项的配置 [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)、[自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)。

## 来源文档

- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [AOQ Client SDK Android API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-android-sdk-reference.md)
- [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)
- [AOQ Client SDK OHOS (HarmonyOS) API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-harmony-sdk-reference.md)
- [AOQ Client SDK Windows API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-windows-sdk-reference.md)
- [AOQ Client SDK Electron API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-electron-sdk-reference.md)
- [AOQ Client SDK macOS API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-macos-sdk-reference.md)
- [AOQ Client SDK iOS API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-ios-sdk-reference.md)
- [AOQ Client SDK Linux Python API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-linux-python-sdk-reference.md)
- [AOQ Client SDK Linux C++ API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-linux-cpp-sdk-reference.md)
- [功能参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)


