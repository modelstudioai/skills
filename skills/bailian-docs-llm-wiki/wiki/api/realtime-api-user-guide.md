# realtime api user guide

Realtime API 是百炼平台面向实时多模态交互场景提供的低延迟、高鲁棒性通信能力，支持 AOQ、WebRTC 和 WebSocket 三种传输协议，覆盖从移动端原生应用、浏览器互动到服务端集成的全场景需求。开发者可根据业务对延迟、弱网对抗、接入成本和平台兼容性的要求选择最适配的协议方案。所有协议均统一通过 DashScope SDK 或标准 HTTP 接口接入，并共享模型能力与鉴权体系。

## 支持的模型/功能

Realtime API 当前支持以下核心模型与应用类型，但**协议支持存在差异**：

- **实时全模态**（`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`）：AOQ、WebRTC、WebSocket 均完全支持。
- **实时语音翻译**（`qwen3.5-livetranslate-flash-realtime`）：AOQ、WebRTC、WebSocket 均完全支持。
- **多模态开发套件**（`multimodal-dialog`）：AOQ、WebRTC、WebSocket 均完全支持。
- **实时语音识别**（`Qwen-Audio-3.0-ASR-Flash-Streaming`、`Fun-ASR-Realtime` 系列）：**仅 AOQ 和 WebSocket 支持，WebRTC 不支持** [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。
- **实时语音合成**（`CosyVoice` 系列、`qwen-audio-3.0-tts-flash`、`qwen-audio-3.0-tts-plus`）：**仅 AOQ 和 WebSocket 支持，WebRTC 不支持** [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。
- **实时语音对话**（`qwen-audio-3.0-realtime-plus`、`qwen-audio-3.0-realtime-flash`）：AOQ、WebRTC、WebSocket 均完全支持。

> **注意**：文档中“[实时语音识别](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide)”和“[实时语音合成](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide)”的官方链接指向外部帮助中心，其内容未明确说明 WebRTC 协议限制；但原始文档 1 的表格已明确标注 WebRTC 对 ASR/TTS 模型为“不支持”，该信息具有更高权威性，应以表格为准。

## 关键参数

### 协议选择参数
- `x-dashscope-rtc-transport`：HTTP 请求头字段，用于指定传输协议。取值为 `moq`（AOQ）、`webrtc`（WebRTC）或 `websocket`（WebSocket）。此参数必须在建连请求中显式声明。

### AOQ 连接凭证参数（由 `/api/v1/webrtc/realtime` 或 `/api/v1/webrtc/inference` 接口返回）
- `aoqTokenForClient`：客户端连接令牌，传入 SDK 的 `token` 字段。
- `sid`：会话唯一标识符，必需。
- `clientRelayEndpoints`：Relay 接入点数组（含 `endpoint` 和 `port`），必需。
- `clientRelayCertFingerprint`：Relay TLS 证书指纹，必需。
- `sidExpiresInSecs`：会话过期时间（秒），建议在过期前主动重连。

### 会话配置参数（`session.update` 事件）
- `modalities`：输出模态列表，如 `["text"]` 或 `["text", "audio"]`。
- `voice`：TTS 音色名称（如 `"Ethan"`）。
- `input_audio_format` / `output_audio_format`：当前仅支持 `"pcm"`。
- `instructions`：系统角色指令，影响模型行为。
- `turn_detection`：语音活动检测（VAD）配置对象，启用后服务端自动检测语音起止。

## 使用方式

### 1. 快速接入流程
1. **获取 API Key**：在百炼控制台创建并安全保管 API Key，**切勿硬编码至客户端** [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。
2. **选择协议与 SDK**：
   - **AOQ**：适用于移动端（Android/iOS/HarmonyOS）及桌面端（Windows/macOS/Electron/Linux），需下载对应平台 SDK [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)。
   - **WebRTC**：适用于浏览器环境，无需额外 SDK，基于标准 WebRTC API。
   - **WebSocket**：适用于任何支持 WebSocket 的环境（包括服务端 Node.js/Python），推荐使用 DashScope SDK 封装。
3. **建连鉴权**：根据协议向百炼网关发起建连请求，携带 `Authorization: Bearer <API_KEY>`。AOQ 协议需服务端代理请求获取临时 [Token](../concepts/token.md)，客户端使用该 [Token](../concepts/token.md) 连接 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。
4. **配置与发送**：连接成功后，发送 `session.update` 事件配置会话，再通过 `enableSendMediaStream` 精确控制媒体流发送时机 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)。

### 2. AOQ 媒体流控制（关键实践）
为避免模型未就绪时数据丢失，**必须**采用“先禁用、后开启”模式：
- `connect` 前调用 `enableSendMediaStream(.audio, false)` 和 `enableSendMediaStream(.video, false)`。
- 在收到服务端 `session.updated` 事件后，再调用 `enableSendMediaStream(.audio, true)` 启动发送 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)。

### 3. 自定义音视频处理
- **自定义音频播放**：设置 `isExternal=true` 关闭 SDK 内部播放器，通过 `onPlaybackAudioFrame` 回调获取 PCM 数据，自行渲染或处理 [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)。
- **自定义音频采集**：设置 `isExternal=true` 关闭麦克风采集，通过 `addAudioExternalStream` 添加外部流，并用 `pushAudioExternalStreamData` 推送 PCM 数据 [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)。
- **自定义视频输入**：设置 `isExternal=true` 后，通过 `pushExternalVideoCapturedFrame`（原始帧）或 `pushExternalVideoEncodedFrame`（已编码帧）注入视频 [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)。

## 限制和注意事项

- **协议兼容性限制**：WebRTC 协议**不支持**实时语音识别（ASR）和实时语音合成（TTS）模型，仅支持全模态、语音翻译和语音对话类模型。此限制在文档 1 中有明确表格说明，开发者选型时需严格规避。
- **AOQ SDK 平台差异**：
  - **Linux Python/C++ 版本**：音频设备管理接口（`startAudioCapture` 等）为空实现，无实际采集/播放能力，仅支持外部音频流和文件播放 [AOQ Client SDK Linux Python API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-linux-python-sdk-reference.md)。
  - **HarmonyOS (OHOS) 版本**：`createEngine` 失败时返回 `null`，调用方**必须判空**；而 Android/iOS/macOS/Windows 版本均为单例且不返回 null [AOQ Client SDK OHOS (HarmonyOS) API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-harmony-sdk-reference.md)。
- **连接状态管理**：`onConnectionStatusChange` 回调中的 `Failed` 状态是瞬态，SDK 会自动迁移到 `Disconnected`，业务层**无需也不应**在此状态下调用 `disconnect` [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)。
- **安全要求**：API Key 仅限服务端使用。AOQ 协议强制要求服务端代理鉴权，客户端仅使用网关下发的短期 [Token](../concepts/token.md)，有效防止密钥泄露 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。

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
- [AOQ Client SDK macOS API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-macos-sdk-reference.md)
- [AOQ Client SDK Windows API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-windows-sdk-reference.md)
- [AOQ Client SDK Electron API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-electron-sdk-reference.md)
- [AOQ Client SDK Linux Python API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-linux-python-sdk-reference.md)
- [AOQ Client SDK Linux C++ API 参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc/aoq-linux-cpp-sdk-reference.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)
- [功能参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function.md)


