# realtime api user guide

Realtime API 是百炼平台面向低延迟、高可靠性实时交互场景提供的统一接入层，支持 AOQ、WebRTC 和 WebSocket 三种传输协议，覆盖语音识别（ASR）、语音合成（TTS）、多模态对话、实时翻译等全栈能力。开发者可根据终端类型、网络环境和业务需求选择最适配的协议，并通过标准化 Token 鉴权与 SDK 快速集成。

## 支持的模型/功能

Realtime API 当前支持以下核心模型与应用类型，不同协议的支持情况存在差异：

- **实时全模态**：`qwen3.5-omni-plus-realtime` 和 `qwen3.5-omni-flash-realtime` —— 全协议（AOQ/WebRTC/WebSocket）均支持，是多模态实时交互的首选模型 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。
- **实时语音翻译**：`qwen3.5-livetranslate-flash-realtime` —— 全协议支持。
- **多模态开发套件**：`multimodal-dialog` —— 全协议支持。
- **实时语音识别（ASR）**：`Qwen-Audio-3.0-ASR-Flash-Streaming`、`Fun-ASR-Realtime` 系列 —— **仅 AOQ 和 WebSocket 支持，WebRTC 不支持** [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。
- **实时语音合成（TTS）**：`CosyVoice` 系列、`qwen-audio-3.0-tts-flash`、`qwen-audio-3.0-tts-plus` —— **仅 AOQ 和 WebSocket 支持，WebRTC 不支持**。
- **实时语音对话**：`qwen-audio-3.0-realtime-plus`、`qwen-audio-3.0-realtime-flash` —— 全协议支持。

> **注意**：文档 1 中明确指出 WebRTC 不支持 ASR/TTS 类模型，但部分旧版示例文档（如未列出的 `best-practice-webrtc-asr`）可能隐含矛盾用法。请以 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 的表格为准，避免在 WebRTC 场景中尝试调用 ASR/TTS 模型。

## 关键参数

### 协议选择参数
- `x-dashscope-rtc-transport`: 必填 HTTP Header，指定协议：
  - `moq` → AOQ 协议（推荐移动端/弱网场景）
  - `webrtc` → WebRTC 协议（推荐浏览器端音视频通话）
  - `websocket` → WebSocket 协议（推荐服务端集成/快速验证）

### 建连鉴权参数
- `Authorization: Bearer <API_KEY>`：建连阶段唯一身份凭证，**绝不暴露于客户端**（AOQ 协议下由 AppServer 代理请求获取临时 token）。
- `clientIp`（可选）：客户端真实公网 IP，用于 Relay 接入点智能调度；不填则默认使用请求网关的 IP。

### 会话配置参数（`session.update` 事件）
- `modalities`: 输出模态数组，如 `["text"]` 或 `["text","audio"]`。
- `voice`: TTS 音色 ID（如 `"Ethan"`），仅当 `modalities` 包含 `"audio"` 时生效。
- `input_audio_format` / `output_audio_format`: 当前仅支持 `"pcm"`。
- `instructions`: 系统角色指令，影响模型行为。
- `turn_detection`: 语音活动检测（VAD）配置对象，启用后服务端自动检测语音起止。

## 使用方式

### 1. 准备工作
- 在 [阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/) 开通服务并创建 [API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- 根据目标平台下载对应 SDK：[SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md) 提供 Android/iOS/HarmonyOS/Windows/macOS/Electron/Linux 全平台 AOQ SDK。

### 2. 建连流程（以 AOQ 为例）
1. **服务端鉴权**：AppServer 调用 `/api/v1/webrtc/realtime?model=...` 接口，携带 `Authorization` Header 获取 `aoqTokenForClient`、`sid`、`clientRelayEndpoints` 等凭证。
2. **客户端连接**：使用凭证初始化 `AoqClientEngine`，调用 `connect(config)` 建立连接。
3. **媒体流控制**：为避免模型未就绪即发送数据，**必须在 `connect` 前调用 `enableSendMediaStream(.audio, false)`**，待收到 `session.updated` 事件后再开启发送 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)。
4. **会话配置**：连接成功后（`onConnectionStatusChange(.connected)`），发送 `session.update` 事件完成会话初始化。

### 3. 自定义音视频处理（可选）
- **自定义音频采集**：设置 `isExternal=true` 后，通过 `addAudioExternalStream` + `pushAudioExternalStreamData` 注入外部 PCM 数据（如 TTS 输出、文件音频） [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)。
- **自定义音频播放**：设置 `isExternal=true` 后，通过 `setAudioFrameObserver` + `enableAudioFrameObserver` 接收解码后的 PCM 数据，交由应用层渲染或二次处理 [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)。
- **自定义视频输入**：设置 `isExternal=true` 后，通过 `pushExternalVideoCapturedFrame`（原始帧）或 `pushExternalVideoEncodedFrame`（JPEG 编码帧）注入视频源 [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)。

## 限制和注意事项

- **协议兼容性限制**：WebRTC 协议**不支持 ASR/TTS 类模型**，仅支持全模态对话与语音翻译类模型；WebSocket 和 AOQ 支持全部模型。
- **AOQ 客户端 Token 安全**：`aoqTokenForClient` 为一次性短期凭证（默认 2 小时过期），但 `API_KEY` 绝不可下发至客户端。AOQ 的服务端代理鉴权模式是安全基线 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。
- **Linux 平台能力限制**：Linux SDK 的 `startAudioCapture`/`startAudioPlayer` 等设备操作接口为空实现，仅支持外部音频流注入、文件播放及帧回调，**不支持直接访问麦克风或扬声器** [AOQ Client SDK Linux Python API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-linux-python-sdk-reference.md)。
- **媒体流控制时机**：`enableSendMediaStream` 必须在 `createEngine` 之后、`connect` 之前调用；若未显式调用，SDK 默认在 `connect` 成功后立即发送媒体流，可能导致模型因未收到 `session.update` 而丢弃首段音频。
- **并发与限流**：具体并发数与 QPS 限制取决于所选模型及工作空间配额，详情请参考 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 文档。

## 来源文档

- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)
- [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md)
- [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [AOQ SDK简介](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)
- [AOQ Client SDK Android API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-android-sdk-reference.md)
- [AOQ Client SDK iOS API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-ios-sdk-reference.md)
- [AOQ Client SDK OHOS (HarmonyOS) API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-harmony-sdk-reference.md)
- [AOQ Client SDK Windows API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-windows-sdk-reference.md)
- [AOQ Client SDK macOS API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-macos-sdk-reference.md)
- [AOQ Client SDK Linux Python API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-linux-python-sdk-reference.md)
- [AOQ Client SDK Electron API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-electron-sdk-reference.md)
- [AOQ Client SDK Linux C++ API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-linux-cpp-sdk-reference.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [功能参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)


