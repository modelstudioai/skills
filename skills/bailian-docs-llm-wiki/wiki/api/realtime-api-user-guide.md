# realtime api user guide

Realtime API 是百炼平台提供的低延迟、高可靠实时交互能力，支持多模态（音视频+文本）与纯文本场景。它通过 AOQ、WebRTC 和 WebSocket 三种传输协议，为不同终端和业务需求提供灵活接入方案。开发者可根据延迟敏感度、弱网环境、平台兼容性及集成复杂度选择最适配的协议。

## 支持的模型与功能

Realtime API 支持全模态、语音识别（ASR）、语音合成（TTS）、语音翻译、语音对话等核心能力，但**不同协议对模型的支持存在差异**：

- **AOQ 协议**：支持全部模型，包括 `[实时全模态](raw/model-user-guide/model-experience/omni-modal/realtime.md)`、`qwen3.8-omni-flash-realtime`、`qwen3.5-livetranslate-flash-realtime`、`Qwen-Audio-3.0-ASR-Flash-Streaming`、`CosyVoice` 系列、`qwen-audio-3.1-realtime-plus` 等。其深度定制的 QUIC 栈原生适配 AI 多模态数据特征，是移动端和弱网场景的首选。
- **WebRTC 协议**：支持 `[实时全模态](raw/model-user-guide/model-experience/omni-modal/realtime.md)`、`qwen3.8-omni-flash-realtime`、`qwen3.5-livetranslate-flash-realtime`、`qwen-audio-3.1-realtime-plus` 等，**但不支持 ASR 和 TTS 类模型**（如 `Qwen-Audio-3.0-ASR-Flash-Streaming`、`CosyVoice` 系列）。适用于已有 WebRTC 基础设施的浏览器端互动场景。
- **WebSocket 协议**：支持 `[实时语音识别](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide)`、`[实时语音合成](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide)`、`[实时语音对话](https://help.aliyun.com/zh/model-studio/fun-audiochat-realtime)` 等模型，**但不支持全模态类模型**（如 `qwen3.8-omni-flash-realtime`）。适合服务端集成与快速原型验证。

> **注意**：文档 1 中明确指出 WebRTC 不支持 ASR/TTS 模型，而部分旧版文档（如未列出的过时用例）可能隐含错误示例。请以本节描述为准，实际接入前务必查阅 [模型/应用支持力度](raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 表格。

此外，`[多模态开发套件](raw/application-user-guide/application-gallery/multimodal-products/multimodal-products-overview.md)`（`multimodal-dialog`）在所有三种协议下均受支持，可作为快速构建交互界面的标准化组件。

## 关键参数

Realtime API 的核心参数围绕连接建立、媒体控制与会话配置展开，关键参数如下：

- **建连凭证**：`aoqTokenForClient`（AOQ）、`Authorization: Bearer <API_KEY>`（WebRTC/WebSocket）。AOQ 采用服务端代理鉴权模式，客户端仅使用网关返回的临时 Token，避免 API Key 暴露；后两者则直接在握手请求头中携带 API Key。详情见 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。
- **会话配置事件**（`session.update`）：必须在连接成功后发送，用于声明 AI 侧行为。关键字段包括：
  - `modalities`: 输出模态数组，如 `["text"]` 或 `["text","audio"]`；
  - `voice`: 输出音色（如 `"Tina"`），仅当 `modalities` 包含 `"audio"` 时生效；
  - `input_audio_format` / `output_audio_format`: 当前仅支持 `"pcm"`；
  - `turn_detection`: 语音打断检测策略（如 `"server_vad"`）。
- **媒体流控制**：`enableSendMediaStream` 是 AOQ 接入的关键控制接口，用于在收到 `session.updated` 事件前暂停音频/视频发送，防止模型未就绪时数据丢失或错乱。详见 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)。
- **编解码配置**：`setAudioEncoderConfig` / `setAudioDecoderConfig` 等接口需在 `connect` 前调用，指定采样率（如 16kHz 输入、24kHz 输出）、声道数、编码格式（Opus/PCM）等。Linux 平台的 `set_video_decoder_config` 仅部分字段生效，详见 [AOQ Client SDK Linux Python API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-linux-python-sdk-reference.md)。

## 使用方式

接入流程遵循“准备 → 鉴权 → 连接 → 配置 → 交互”五步法：

1.  **准备 SDK 与依赖**：根据目标平台下载对应版本的 AOQ SDK（Android/iOS/HarmonyOS/Windows/macOS/Electron/Linux），并集成 Opus 插件。各平台 API 差异较大，需参考对应 [AOQ Client SDK API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-android-sdk-reference.md)（如 Android）、[AOQ Client SDK iOS API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-ios-sdk-reference.md)（如 iOS）等文档。
2.  **获取并配置 API Key**：在百炼控制台创建 API Key，并通过环境变量或后端服务安全下发。**严禁硬编码到客户端**，参见 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。
3.  **发起建连请求**：由业务 AppServer 调用百炼网关分配连接参数（如 `aoqTokenForClient`, `clientRelayEndpoints`）。AOQ 请求需指定 `x-dashscope-rtc-transport: moq` 头；WebRTC/WebSocket 则分别使用 `webrtc/realtime` 和 `websocket/realtime` 路径。
4.  **初始化 SDK 并建立连接**：创建引擎实例，设置 `AoqEngineDelegate` 回调，调用 `connect` 并传入网关返回的凭证。连接状态迁移由 `onConnectionStatusChange` 回调通知，状态机详见 [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)。
5.  **配置会话与收发数据**：在 `onConnectionStatusChange(.connected)` 后发送 `session.update`；在 `onDataMsg` 中监听 `session.updated` 后，调用 `enableSendMediaStream(.audio, true)` 开启媒体流；后续通过 `sendDataMsg` 发送文本/指令，通过 `onDataMsg` 接收 AI 返回的 `response.text_delta`、`response.audio_delta` 等事件。

## 限制和注意事项

- **平台能力差异**：Linux 平台 SDK **不支持内部音频/视频设备采集与渲染**（`startAudioCapture` 等为空实现），仅支持外部音频流注入与原始/编码视频帧推送；macOS/Windows Electron 的屏幕采集需先调用 `getScreenSourceList` 获取源列表；iOS 屏幕采集依赖 `AoqScreenShare.framework`，而 Android/HarmonyOS 则使用系统广播机制。
- **自定义采集约束**：启用外部音频/视频采集（`isExternal=true`）后，必须调用 `addAudioExternalStream` 或 `startVideoCapture(isExternal=true)`，否则 `pushExternal*` 接口将返回错误码（如 `AoqECVideoExternalCaptureNotEnabled`）。Linux 平台外部视频采集**强制要求 `isExternal=true` 且不支持内部采集**。
- **连接稳定性**：AOQ 连接状态为瞬态 `Failed` 时，SDK 会自动迁移到 `Disconnected`，业务层无需手动调用 `disconnect`。重连应基于 `onConnectionStatusChange(.disconnected)` 触发，并重新调用 `connect`。
- **安全与合规**：API Key 必须通过服务端代理下发，客户端不得存储或泄露。所有音频/视频数据传输均经 TLS 加密，但客户端侧的 PCM 数据回调（如 `onPlaybackAudioFrame`）为明文，需自行保障处理链路安全。

## 来源文档

- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [AOQ Client SDK Android API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-android-sdk-reference.md)
- [AOQ Client SDK iOS API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-ios-sdk-reference.md)
- [AOQ Client SDK OHOS (HarmonyOS) API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-harmony-sdk-reference.md)
- [AOQ Client SDK Windows API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-windows-sdk-reference.md)
- [AOQ Client SDK macOS API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-macos-sdk-reference.md)
- [AOQ Client SDK Electron API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-electron-sdk-reference.md)
- [AOQ Client SDK Linux Python API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-linux-python-sdk-reference.md)
- [AOQ Client SDK Linux C++ API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-linux-cpp-sdk-reference.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [功能参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)


