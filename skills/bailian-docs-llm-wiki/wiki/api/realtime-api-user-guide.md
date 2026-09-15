# realtime api user guide

Realtime API 是百炼平台提供的低延迟、高可靠实时交互能力，支持多模态（音视频+文本）AI 场景。它通过 AOQ、WebRTC 和 WebSocket 三种传输协议提供差异化接入方案，适用于移动端原生应用、浏览器互动和后端服务集成等不同场景。开发者可根据业务对延迟、弱网对抗、平台兼容性和接入成本的要求选择最适配的协议。

## 支持的模型与功能

Realtime API 当前支持以下核心模型与应用类型，但**协议支持存在差异**：

- **实时全模态**（`qwen3.5-omni-plus-realtime`, `qwen3.5-omni-flash-realtime`）：AOQ、WebRTC、WebSocket 均支持。
- **实时语音翻译**（`qwen3.5-livetranslate-flash-realtime`）：AOQ、WebRTC、WebSocket 均支持。
- **多模态开发套件**（`multimodal-dialog`）：AOQ、WebRTC、WebSocket 均支持。
- **实时语音识别**（`Qwen-Audio-3.0-ASR-Flash-Streaming`, `Fun-ASR-Realtime` 系列）：**仅 AOQ 和 WebSocket 支持**，WebRTC 不支持 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。
- **实时语音合成**（`CosyVoice` 系列、`qwen-audio-3.0-tts-flash`、`qwen-audio-3.0-tts-plus`）：**仅 AOQ 和 WebSocket 支持**，WebRTC 不支持 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。
- **实时语音对话**（`qwen-audio-3.0-realtime-plus`, `qwen-audio-3.0-realtime-flash`）：AOQ、WebRTC、WebSocket 均支持。

> **注意**：文档中关于 `qwen-audio-3.0-realtime-plus` 的接入示例同时存在于 AOQ 和 WebRTC 场景下，但模型支持矩阵明确指出其 WebRTC 支持性，而 `Fun-ASR-Realtime` 等 ASR/TTS 模型在 WebRTC 列被标记为“不支持”。这表明模型支持是按协议粒度定义的，而非全局通用。请以 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中的表格为准，避免跨协议复用配置。

## 关键参数

### 协议选择参数
- `x-dashscope-rtc-transport`: 请求头字段，用于指定传输协议。值为 `moq` 表示 AOQ，`webrtc` 表示 WebRTC，WebSocket 无此字段，由连接 URL 隐式决定。

### AOQ 连接凭证（由 `/api/v1/allocate` 接口返回）
- `aoqTokenForClient`: 客户端 SDK 必填的连接令牌，非 API Key。
- `sid`: 会话唯一标识符。
- `clientRelayEndpoints`: Relay 接入点数组（含 `endpoint` 和 `port`）。
- `clientRelayCertFingerprint`: Relay TLS 证书指纹，用于客户端校验。
- `extraInfo.workspaceIdHash`: 工作区 ID 哈希，需传入 `AoqConnectConfig`。

### 会话配置（`session.update` 事件）
- `modalities`: 输出模态列表，如 `["text"]` 或 `["text", "audio"]`。
- `voice`: 输出音频音色（如 `"Ethan"`）。
- `input_audio_format` / `output_audio_format`: 当前仅支持 `"pcm"`。
- `instructions`: 系统角色指令，用于设定模型行为。

## 使用方式

### 1. 协议选型与接入路径
- **AOQ**: 适用于移动端（Android/iOS/HarmonyOS）及桌面端（Windows/macOS/Electron/Linux）原生应用，需集成 [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md) 提供的 AOQ Client SDK。建连需服务端代理鉴权，客户端使用临时 [Token](../concepts/token.md)。
- **WebRTC**: 适用于浏览器环境或已有 WebRTC 基础设施的场景，通过 SDP 交换流程完成建连，客户端可直接携带 API Key。
- **WebSocket**: 适用于服务端集成或快速原型验证，通过标准 WebSocket 握手建立连接，客户端可直接携带 API Key。

### 2. AOQ 核心接入步骤（以 iOS 为例）
1. **创建引擎**：调用 `createEngine:delegate:`，传入 `AoqCreateConfig`。
2. **启动媒体设备**：调用 `startAudioCapture:` 和 `startAudioPlayer:`（可选 `startVideoCapture:`）。
3. **获取并设置连接凭证**：由 AppServer 调用 `/api/v1/allocate` 获取响应，并构造 `AoqConnectConfig`。
4. **控制媒体流发送时机**：**关键实践**——连接前调用 `enableSendMediaStream(.audio, enable: false)` 暂停发送，待收到 `session.updated` 事件后再调用 `enableSendMediaStream(.audio, enable: true)` 开启，确保模型已就绪 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)。
5. **发起连接**：调用 `connect:`。

### 3. 鉴权机制
所有协议均在建连阶段通过 `Authorization: Bearer <API_KEY>` 完成鉴权，**连接建立后数据传输无需重复鉴权**。AOQ 协议采用服务端代理模式，API Key 仅在服务端使用，客户端使用网关下发的临时 [Token](../concepts/token.md)，安全性更高 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。

## 限制和注意事项

- **平台能力差异**：
  - Linux SDK 的音频设备管理（`startAudioCapture` 等）为空实现，仅支持外部音频流注入和文件播放；视频渲染亦无实现，仅支持外部帧推送 [AOQ Client SDK Linux Python API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-linux-python-sdk-reference.md)。
  - HarmonyOS (OHOS) SDK 的 `createEngine` 在 native 创建失败时返回 `null`，调用方必须判空处理，而 Android/iOS/macOS 版本均为单例且不返回 null [AOQ Client SDK OHOS (HarmonyOS) API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-harmony-sdk-reference.md)。

- **连接状态管理**：
  - `Failed` 是瞬态，SDK 触发 `onConnectionStatusChange(failed)` 后会自动迁移到 `Disconnected`，业务层无需手动调用 `disconnect` [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)。
  - `disconnect` 在未连接状态下调用是安全的，返回 `0`。

- **自定义采集/播放**：
  - 自定义音频采集时，若需启用 3A（回声消除、降噪），必须在 `addAudioExternalStream` 的 `AoqAudioExternalStreamConfig` 中显式设置 `enable3A = true`。
  - 自定义视频输入分“原始帧模式”（`pushExternalVideoCapturedFrame`）和“编码帧模式”（`pushExternalVideoEncodedFrame`），二者不可混用，且需在 `startVideoCapture` 时设置 `isExternal = true` [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)。

- **安全提示**：API Key 是敏感凭证，**严禁硬编码到客户端代码或提交至代码仓库**，应通过环境变量或后端服务下发 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。

## 来源文档

- [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md)
- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)
- [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [AOQ Client SDK iOS API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-ios-sdk-reference.md)
- [AOQ Client SDK Android API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-android-sdk-reference.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [AOQ Client SDK OHOS (HarmonyOS) API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-harmony-sdk-reference.md)
- [AOQ Client SDK Windows API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-windows-sdk-reference.md)
- [AOQ Client SDK macOS API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-macos-sdk-reference.md)
- [AOQ Client SDK Electron API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-electron-sdk-reference.md)
- [AOQ Client SDK Linux Python API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-linux-python-sdk-reference.md)
- [AOQ Client SDK Linux C++ API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-linux-cpp-sdk-reference.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [功能参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)


