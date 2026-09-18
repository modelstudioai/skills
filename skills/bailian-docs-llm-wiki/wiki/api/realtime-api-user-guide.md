# realtime api user guide

Realtime API 是阿里云百炼平台提供的低延迟、高可靠实时交互能力，支持 AOQ、WebRTC 和 WebSocket 三种传输协议，面向多模态语音对话、实时语音识别/合成、语音翻译等场景。开发者可根据终端平台、网络环境、功能需求和接入成本选择最适配的协议方案，并通过统一 Token 鉴权机制安全接入。

## 支持的模型/功能

Realtime API 当前支持以下核心模型与应用类型，但**协议支持存在显著差异**：

- **全模态交互**：`qwen3.5-omni-plus-realtime` 和 `qwen3.5-omni-flash-realtime` 均支持 AOQ、WebRTC 和 WebSocket [实时全模态](raw/model-user-guide/model-experience/omni-modal/realtime.md)。
- **实时语音翻译**：`qwen3.5-livetranslate-flash-realtime` 同样三协议全支持。
- **多模态开发套件**：`multimodal-dialog` 应用支持全部三种协议。
- **实时语音识别（ASR）**：`Qwen-Audio-3.0-ASR-Flash-Streaming` 和 `Fun-ASR-Realtime` 系列**仅支持 AOQ 和 WebSocket**，**不支持 WebRTC** [实时语音识别](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide)。
- **实时语音合成（TTS）**：`CosyVoice` 系列、`qwen-audio-3.0-tts-flash` 和 `qwen-audio-3.0-tts-plus` **同样仅支持 AOQ 和 WebSocket**，**不支持 WebRTC** [实时语音合成](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide)。
- **实时语音对话**：`qwen-audio-3.0-realtime-plus` 和 `qwen-audio-3.0-realtime-flash` 支持全部三种协议。

> **注意**：文档 1 中明确指出 ASR 和 TTS 模型“不支持 WebRTC”，但部分旧版文档（如未在原始列表中提供）曾暗示其 WebRTC 兼容性。请以本文档及 [实时语音识别](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide) 和 [实时语音合成](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide) 的最新说明为准。

## 关键参数

Realtime API 的关键参数分为协议通用参数和协议特有参数：

- **通用鉴权参数**：所有协议均需在建连请求的 HTTP Header 中携带 `Authorization: Bearer <API_KEY>`。API Key 须通过百炼控制台创建并严格保密，**切勿硬编码于客户端** [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。
- **AOQ 特有参数**：建连时需传入由服务端 `/api/v1/allocate` 接口返回的凭证，包括 `token`（客户端连接令牌）、`sid`（会话ID）、`certFingerprint`（Relay 证书指纹）、`relayEndpoints`（Relay 接入点）和 `workspaceIdHash`（工作区哈希）[Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。
- **会话配置参数**：连接成功后，客户端需发送 `session.update` 事件配置 AI 会话，关键字段包括：
  - `modalities`: 输出模态，如 `["text"]` 或 `["text","audio"]`。
  - `voice`: 输出音色（如 `"Ethan"`）。
  - `input_audio_format` / `output_audio_format`: 输入/输出音频格式，当前仅支持 `"pcm"`。
  - `instructions`: 系统角色指令，用于设定模型行为。

## 使用方式

使用 Realtime API 的标准流程为：**准备 SDK/环境 → 获取鉴权凭证 → 建立连接 → 配置会话 → 交互**。

- **SDK 选择与下载**：AOQ 协议需集成对应平台的 AOQ Client SDK，官方提供 Android、iOS、HarmonyOS、Windows、macOS、Electron 和 Linux（C++/Python）版本，各平台 SDK API 设计高度一致，详情见 [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)。
- **协议接入**：
  - **AOQ**：适用于移动端原生 App，需调用 `createEngine` 创建引擎，`connect` 建连，并通过 `enableSendMediaStream` 精确控制媒体流发送时机（通常需等待 `session.updated` 后开启）[媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)。
  - **WebRTC**：适用于浏览器端，利用原生 WebRTC API，需处理 SDP 交换和 ICE 候选者收集。
  - **WebSocket**：适用于服务端或快速原型验证，通过标准 WebSocket 连接，接入门槛最低。
- **高级功能**：SDK 提供丰富的扩展能力，例如：
  - **自定义音频采集/播放**：通过 `isExternal=true` 关闭内部设备，使用 `pushAudioExternalStreamData` 或 `onPlaybackAudioFrame` 回调实现完全自定义的音频管线 [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md) 和 [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)。
  - **自定义视频输入**：支持原始帧（BGRA/I420）或已编码帧（JPEG）两种模式，通过 `pushExternalVideoCapturedFrame` 或 `pushExternalVideoEncodedFrame` 推送 [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)。

## 限制和注意事项

- **协议兼容性限制**：如前所述，ASR 和 TTS 模型**不支持 WebRTC 协议**，此为硬性限制，非配置问题。
- **AOQ 连接状态管理**：AOQ SDK 采用明确的状态机，状态包括 `Connecting`、`Connected`、`Failed` 和 `Disconnected`。`Failed` 是瞬态，SDK 会在触发 `onConnectionStatusChange(Failed)` 后自动迁移到 `Disconnected`，业务层无需也**不应**在此时调用 `disconnect` [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)。
- **媒体流控制最佳实践**：为避免模型未就绪即收到媒体数据导致错误，强烈建议在 `connect` 前调用 `enableSendMediaStream(.audio, false)` 暂停发送，并在收到服务端 `session.updated` 事件后再调用 `enableSendMediaStream(.audio, true)` 开启发送 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)。
- **平台能力差异**：Linux 平台的 AOQ SDK 对音频/视频设备管理（如 `startAudioCapture`）为“空实现”，仅支持外部采集和文件播放；HarmonyOS SDK 的 `createEngine` 在 native 创建失败时会返回 `null`，而 Android/iOS 则返回有效实例，调用方需做判空处理 [AOQ Client SDK Linux C++ API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-linux-cpp-sdk-reference.md) 和 [AOQ Client SDK OHOS (HarmonyOS) API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-harmony-sdk-reference.md)。

## 来源文档

- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)
- [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [AOQ Client SDK Android API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-android-sdk-reference.md)
- [AOQ Client SDK iOS API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-ios-sdk-reference.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [AOQ Client SDK macOS API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-macos-sdk-reference.md)
- [AOQ Client SDK Electron API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-electron-sdk-reference.md)
- [AOQ Client SDK OHOS (HarmonyOS) API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-harmony-sdk-reference.md)
- [AOQ Client SDK Linux C++ API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-linux-cpp-sdk-reference.md)
- [AOQ Client SDK Linux Python API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-linux-python-sdk-reference.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [AOQ Client SDK Windows API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-windows-sdk-reference.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)
- [功能参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function.md)


