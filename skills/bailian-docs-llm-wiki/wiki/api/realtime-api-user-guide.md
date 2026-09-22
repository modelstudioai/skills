# realtime api user guide

Realtime API 是百炼平台面向低延迟、高可靠性实时交互场景提供的统一接入层，支持 AOQ、WebRTC 和 WebSocket 三种传输协议，覆盖语音识别、语音合成、多模态对话、实时翻译等全栈 AI 实时能力。开发者可根据终端平台、网络环境、功能需求和集成成本灵活选型，无需从零构建音视频基础设施。

## 支持的模型/功能

Realtime API 支持以下核心模型与应用类型，但**协议支持存在差异**：

- **全模态实时交互**：`qwen3.8-omni-flash-realtime`、`qwen3.5-omni-plus-realtime`、`multimodal-dialog` 等模型在 AOQ、WebRTC、WebSocket 三协议下均完全支持 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。
- **实时语音识别（ASR）**：`Qwen-Audio-3.0-ASR-Flash-Streaming`、`Fun-ASR-Realtime` 系列仅支持 AOQ 和 WebSocket，**不支持 WebRTC** [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。
- **实时语音合成（TTS）**：`CosyVoice`、`qwen-audio-3.0-tts-flash` 等系列同样仅支持 AOQ 和 WebSocket，**不支持 WebRTC** [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。
- **实时语音对话**：`qwen-audio-3.1-realtime-plus` 等模型三协议均支持。

> **注意**：文档 1 明确指出 ASR/TTS 类模型“WebRTC 不支持”，但部分旧版示例代码（如未列出的 `best-practice-webrtc-asr.md`）可能隐含错误引导。请以文档 1 的表格为准，WebRTC 协议不可用于纯 ASR/TTS 场景。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `Authorization: Bearer <API_KEY>` | 建连阶段唯一鉴权凭证，**绝不暴露于客户端** | `Bearer sk-xxx` | [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md) |
| `x-dashscope-rtc-transport: moq` | AOQ 协议标识头 | `moq` | [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md) |
| `clientIp` | 客户端真实公网 IP，用于 Relay 节点智能调度 | `203.204.205.206` | [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md) |
| `aoqTokenForClient` | AOQ 客户端连接令牌，由服务端 allocate 接口返回后传入 SDK | `ecc1a460...` | [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md) |
| `session.modalities` | 会话输出模态配置，决定返回内容类型 | `["text", "audio"]` | [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md) |

## 使用方式

### 1. 协议选型与 SDK 集成
- **AOQ**：适用于移动端原生 App（Android/iOS/HarmonyOS）、桌面端（Windows/macOS/Linux/Electron），需集成对应平台 AOQ Client SDK。最新 v1.3.0 版本已支持屏幕共享、Opus 默认编解码及远程 .so 库加载 [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)。
- **WebRTC**：适用于浏览器端或已有 WebRTC 基础设施的场景，无需额外 SDK，依赖浏览器原生能力。
- **WebSocket**：适用于服务端集成、快速原型验证，可直接使用 DashScope SDK 或标准 WebSocket 客户端。

### 2. 标准接入流程（以 AOQ 为例）
1. **服务端鉴权**：业务 AppServer 调用 `/api/v1/webrtc/realtime` 接口，携带 `Authorization` 头和 `x-dashscope-rtc-transport: moq`，获取 `aoqTokenForClient` 和 `clientRelayEndpoints`。
2. **客户端建连**：将 `aoqTokenForClient` 等参数注入 AOQ SDK 的 `AoqConnectConfig`，调用 `connect()`。
3. **媒体流控制**：为避免模型未就绪即发送数据，**必须**在 `connect()` 前调用 `enableSendMediaStream(.audio, false)`，待收到 `session.updated` 事件后再启用发送 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)。
4. **自定义采集/播放（可选）**：如需接管音频输入（如 TTS 输出）或输出（如 ASR 结果二次处理），使用 `addAudioExternalStream` + `pushAudioExternalStreamData` 或 `setAudioFrameObserver` + `onPlaybackAudioFrame` [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md) / [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)。

## 限制和注意事项

- **API Key 安全**：`API_KEY` 仅限服务端使用，**严禁硬编码至前端或客户端代码**。AOQ 协议通过服务端代理鉴权，客户端只持有临时 `aoqTokenForClient`，符合最小权限原则 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。
- **平台能力差异**：
  - Linux C++ SDK 的 `startAudioCapture`/`startAudioPlayer` 为空实现，仅支持外部音频流；视频渲染无 native 实现，需自行处理 [AOQ Client SDK Linux C++ API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-linux-cpp-sdk-reference.md)。
  - iOS SDK 的 `enableSpeakerphone` 在非 VoIP 模式下调用会触发 `AoqECAudioDeviceEarpieceRequiresVoipMode` 错误 [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)。
- **连接状态管理**：`Failed` 是瞬态，SDK 触发 `onConnectionStatusChange(Failed)` 后会自动迁移到 `Disconnected`，业务层**无需且不应**在此状态下调用 `disconnect()` [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)。
- **并发与限流**：具体并发数、QPS 限制取决于所选模型、[Token](../concepts/token.md) Plan 配置及工作空间规格，详情请查阅 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 文档。

## 来源文档

- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)
- [AOQ Client SDK macOS API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-macos-sdk-reference.md)
- [AOQ Client SDK Windows API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-windows-sdk-reference.md)
- [AOQ Client SDK Electron API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-electron-sdk-reference.md)
- [AOQ Client SDK Linux Python API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-linux-python-sdk-reference.md)
- [AOQ Client SDK Android API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-android-sdk-reference.md)
- [AOQ Client SDK iOS API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-ios-sdk-reference.md)
- [AOQ Client SDK OHOS (HarmonyOS) API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-harmony-sdk-reference.md)
- [功能参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)
- [AOQ Client SDK Linux C++ API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-linux-cpp-sdk-reference.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)


