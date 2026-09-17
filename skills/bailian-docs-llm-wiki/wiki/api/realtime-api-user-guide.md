# realtime api user guide

Realtime API 是百炼平台面向低延迟、高并发 AI 交互场景提供的实时流式服务接口，支持音频、视频、文本等[多模态](../concepts/multi-modal.md)数据的端到端实时传输与处理。它通过 AOQ（AI over QUIC）、WebRTC 和 WebSocket 三种协议提供差异化接入能力，适用于智能客服、实时翻译、语音助手等对时延和弱网鲁棒性要求严苛的生产环境。开发者需结合业务目标、终端类型和模型需求选择合适协议，并严格遵循鉴权与连接生命周期管理规范。

## 支持的模型/功能

Realtime API 当前支持以下核心模型与能力，不同协议的支持范围存在差异：

- **实时全模态模型**：`qwen3.5-omni-plus-realtime` 和 `qwen3.5-omni-flash-realtime`，支持文本+音频双模态输出，AOQ/WebRTC/WebSocket 均完全支持。
- **实时语音识别（ASR）**：`fun-asr-realtime`、`Qwen-Audio-3.0-ASR-Flash-Streaming` 等，**仅 AOQ 和 WebSocket 支持**，WebRTC 不支持 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。
- **实时语音合成（TTS）**：`CosyVoice` 系列、`qwen-audio-3.0-tts-flash` 等，**仅 AOQ 和 WebSocket 支持**，WebRTC 不支持 [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。
- **实时语音对话模型**：`qwen-audio-3.0-realtime-plus`、`qwen-audio-3.0-realtime-flash`，三协议均支持。
- **实时语音翻译**：`qwen3.5-livetranslate-flash-realtime`，三协议均支持。
- **[多模态](../concepts/multi-modal.md)开发套件**：`multimodal-dialog`，三协议均支持。

> **注意**：文档中关于 `fun-asr-realtime` 的支持范围存在矛盾。[Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 明确指出 WebRTC **不支持** ASR 模型，但部分旧版示例代码未作区分。请以概述文档为准，WebRTC 场景下如需 ASR，应改用 AOQ 或 WebSocket 协议。

## 关键参数

Realtime API 的关键参数分为建连参数与会话配置两类：

### 建连参数（HTTP 请求头/体）
- `Authorization: Bearer <API_KEY>`：建连阶段必需，用于身份认证。**API Key 必须由服务端持有并下发，严禁硬编码至客户端** [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。
- `x-dashscope-rtc-transport: moq`：指定使用 AOQ 协议（`moq` 表示 Media Over QUIC）。
- `clientIp`（选填）：客户端真实公网 IP，用于 Relay 接入点智能调度；若不填，则默认使用请求网关的 IP。
- `model`（URL Path 参数）：指定目标模型，例如 `?model=qwen3.5-omni-plus-realtime`。

### 会话配置参数（`session.update` 事件）
- `modalities`: 字符串数组，指定输出模态，如 `["text"]` 或 `["text","audio"]`。
- `voice`: 输出音色名称，如 `"Ethan"`。
- `input_audio_format` / `output_audio_format`: 当前仅支持 `"pcm"`。
- `instructions`: 系统角色指令，用于设定模型行为边界。
- `turn_detection`: 语音活动检测（VAD）配置对象，启用后服务端自动识别语音起止。

## 使用方式

### 1. 协议选型
- **AOQ**：推荐用于移动端原生应用（Android/iOS/HarmonyOS/Windows/macOS/Electron/Linux），具备极致弱网对抗、内置 3A（回声消除/降噪/AGC）、混合媒体传输能力。SDK 提供跨平台统一 API [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)。
- **WebRTC**：适用于浏览器端或已有 WebRTC 基础设施的场景，原生兼容，但建连慢、弱网表现弱于 AOQ。
- **WebSocket**：适用于服务端集成、快速原型验证，接入成本最低，但无音视频处理能力，需自行实现编解码与传输。

### 2. AOQ 标准接入流程（以移动端为例）
1. **服务端鉴权**：AppServer 调用 `/api/v1/webrtc/realtime` 接口，携带 `Authorization` 头获取 `aoqTokenForClient`、`sid`、`clientRelayEndpoints` 等凭证 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。
2. **客户端初始化**：调用 `createEngine` 创建单例引擎，设置 `AoqEngineDelegate` 监听回调。
3. **媒体控制**：调用 `startAudioCapture`/`startVideoCapture` 启动采集（可选），**务必在 `connect` 前调用 `enableSendMediaStream(.audio, false)` 暂停发送**，避免模型未就绪时数据丢失 [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)。
4. **建立连接**：传入服务端下发的 `aoqTokenForClient`、`sid` 等参数调用 `connect`。
5. **会话配置**：在 `onConnectionStatusChange(.connected)` 回调中发送 `session.update` 事件。
6. **开启媒体**：收到 `session.updated` 事件后，调用 `enableSendMediaStream(.audio, true)` 开启音频发送。

### 3. SDK 下载与版本
AOQ SDK 提供全平台支持，最新稳定版为 **v1.2.2**（iOS）和 **v1.2.0**（其余平台）。各平台 SDK 包含独立的 PluginOpus 编解码库，下载地址详见 [SDK下载](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)。Linux 平台同时提供 Python 和 C++ 接口，但音频设备管理为空实现，仅支持外部音频流注入。

## 限制和注意事项

- **连接生命周期**：鉴权仅发生在建连阶段，连接建立后无需重复鉴权；连接状态迁移由 SDK 自动管理，`Failed` 为瞬态，SDK 会自动迁移到 `Disconnected`，业务层无需手动调用 `disconnect` [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)。
- **媒体流控制**：`enableSendMediaStream` 必须在 `createEngine` 之后调用；默认行为是 connect 成功后立即发送媒体流，**强烈建议采用“先禁用、后开启”模式**，以确保与 `session.updated` 事件同步。
- **平台差异**：
  - **Linux**：无内置音频采集/播放能力，必须使用 `isExternal=true` 配合 `pushAudioExternalStreamData` 实现自定义采集与播放。
  - **OHOS**：`createEngine` 失败时返回 `null`，调用方需判空；而 Android/iOS 返回非空实例。
  - **Electron**：`createEngine()` 依赖 libuv 消息泵，JS 线程不可长时间阻塞。
- **安全要求**：API Key 是最高权限凭证，必须通过服务端代理下发，禁止出现在客户端代码、HTML、配置文件或 Git 仓库中 [Token鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。
- **资源释放**：`destroy` 后引擎实例失效，需重新 `createEngine` 才能继续使用；所有平台均要求 `listener`/`delegate` 生命周期长于引擎实例。

## 来源文档

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
- [功能参考](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function.md)
- [连接状态管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [媒体流发送管理](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [音频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频播放](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [自定义音频采集](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [视频常用功能介绍](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义视频输入](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)
- [Realtime API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)


