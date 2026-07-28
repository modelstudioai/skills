# realtime api user guide

百炼 Realtime API 是针对实时[多模态](../concepts/multimodal.md)交互场景提供的一套接入方案，支持 WebSocket、WebRTC 和 AOQ（AI over QUIC）三种传输协议，开发者可根据业务场景在服务端集成、浏览器端和移动端原生应用之间灵活选择。核心能力包括实时语音/视频对话、流式 ASR/TTS、[多模态](../concepts/multimodal.md)输入，以及内置回声消除、降噪和弱网对抗。

## 协议选择

参见 [Realtime API简介](../../raw/model-user-guide/realtime-api-user-guide/realtime-api-overview.md) 的完整对比表。简要说明：

| 协议 | 适用场景 | 端侧平台 | 弱网对抗 | 回声消除/降噪 |
|------|----------|----------|----------|--------------|
| WebSocket | 服务端集成、快速原型 | 全平台 | 差 | 无，需自行处理 |
| WebRTC | 浏览器端、已有 RTC 基础设施 | 浏览器、移动端 | 良好 | 内置 |
| AOQ | 移动端原生、弱网、[多模态](../concepts/multimodal.md) | Android / iOS / HarmonyOS | 极致 | 内置 |

## 支持的模型与应用

| 模型/应用类型 | 模型 | AOQ | WebRTC | WebSocket |
|-------------|------|-----|--------|-----------|
| 实时全模态 | qwen3.5-omni-plus-realtime | ✓ | ✓ | ✓ |
| 实时全模态 | qwen3.5-omni-flash-realtime | ✓ | ✓ | ✓ |
| 实时全模态 | qwen3.5-livetranslate-flash-realtime | ✓ | ✓ | ✓ |
| [多模态](../concepts/multimodal.md)开发套件 | multimodal-dialog | ✗ | ✓ | ✓ |
| 实时语音识别 | FunASR 系列 | ✗ | ✗ | ✓ |
| 实时语音合成 | CosyVoice 系列 | ✗ | ✗ | ✓ |
| 实时语音对话 | qwen-audio-3.0-realtime-plus/flash | ✗ | ✗ | ✓ |

## 鉴权机制

三种协议均使用 [API Key](../concepts/api-key.md)，通过 HTTP 请求头 `Authorization: Bearer <API_KEY>` 完成建连鉴权，连接建立后无需重复鉴权。

**AOQ 特殊机制**：[API Key](../concepts/api-key.md) 仅在业务 AppServer 侧使用，客户端从 AppServer 换取临时 [Token](../concepts/token.md)。AppServer 向百炼网关发起如下请求：

```bash
curl -X POST \
  "https://{endpoint}/api/v1/webrtc/realtime?model=qwen3.5-omni-plus-realtime" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  -H "x-dashscope-rtc-transport: moq" \
  -d '{"clientIp": "<客户端真实公网IP>"}'
```

响应包含 `aoqTokenForClient`、`sid`、`clientRelayEndpoints`、`clientRelayCertFingerprint` 等字段，客户端使用这些凭证调用 SDK `connect`。详见 [Token鉴权](../../raw/model-user-guide/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。

> **注意**：[API Key](../concepts/api-key.md) 不要硬编码到客户端代码或代码仓库。AOQ 方案本身的设计目标就是避免 [API Key](../concepts/api-key.md) 下发到端侧，务必通过 AppServer 代理换取 [Token](../concepts/token.md)。

## SDK 下载与集成

WebSocket 协议使用 [DashScope SDK](../concepts/dashscope-sdk.md)，参见官方安装文档。

AOQ Client SDK 当前最新版本 v1.0.1，支持 Android（`.aar` + `libPluginOpus.so`）、iOS（`.framework` + `PluginOpus.framework`）和 HarmonyOS（`.har` + `libPluginOpus.so`）。如需 Opus 编解码，须同时下载音频插件。详见 [SDK下载](../../raw/model-user-guide/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)。

Android 集成要点：
- `minSdk 21`，ABI 过滤 `armeabi-v7a` 和 `arm64-v8a`
- Manifest 需声明 `INTERNET`、`RECORD_AUDIO`、`CAMERA` 等权限，其中 `RECORD_AUDIO` 和 `CAMERA` 为运行时权限

iOS 集成要点：
- framework 选 **Embed & Sign**
- Info.plist 声明 `NSMicrophoneUsageDescription` 和 `NSCameraUsageDescription`

## 接入流程

### AOQ 接入

参见 [实现接通模型/应用](../../raw/model-user-guide/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md) 的 AOQ 章节。核心步骤：

1. 调用 `AoqClientEngine.createEngine` 创建引擎，注册 `onConnectionStatusChange` / `onDataMsg` / `onError` 回调
2. 调用 `startAudioCapture` / `startAudioPlayer`（可选 `startVideoCapture`）启动媒体设备
3. AppServer 向百炼换取 [Token](../concepts/token.md)，下发给客户端
4. **建连前**调用 `enableSendMediaStream(.audio, enable: false)` 关闭媒体发送
5. 调用 `connect(config)` 建立连接
6. 收到 `session.updated` 后调用 `enableSendMediaStream(.audio, enable: true)` 开启媒体发送
7. 通话结束后调用 `disconnect()` → `AoqClientEngine.destroy()`

> **注意**：AOQ SDK 建连成功后默认立即开始发送媒体数据。若未在 `connect` 前关闭媒体发送，模型侧可能在会话配置完成前收到数据。务必遵循"先禁用、收到 `session.updated` 后再开启"的模式。

### WebRTC 接入（浏览器）

1. `new RTCPeerConnection({ iceServers: [] })`
2. `getUserMedia` 获取音频（必须）和视频（可选）媒体流
3. 添加媒体轨道；建连前将 sender track 替换为 `null` 实现媒体门控
4. 创建名为 `oai-events` 的 DataChannel
5. `createOffer` → `setLocalDescription`，等待 `iceGatheringState === "complete"`
6. HTTP POST Offer SDP 到 `https://{endpoint}/api/v1/webrtc/realtime?model=<模型名>`，Header 携带 [API Key](../concepts/api-key.md)
7. 将返回的 Answer SDP 设置为 `setRemoteDescription`（注意行尾规范化为 `\r\n`）
8. 收到 `session.created` 后恢复媒体发送

> **注意**：浏览器端受 CORS 限制，无法直接向百炼服务端发起 SDP 交换请求。Demo 中通过 curl 命令手动执行；正式产品应由业务 AppServer 代理此请求。WebRTC 仅支持 VAD 模式（`server_vad` 或 `semantic_vad`），不支持手动模式。

### [多模态](../concepts/multimodal.md)开发套件（multimodal-dialog）接入

WebRTC 接入端点格式为：
```
POST https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/webrtc/inference?model=multimodal-dialog
```
`workspace_id` 和 `region` 从百炼控制台获取。DataChannel 就绪后向服务端发送 `run-task` 消息启动会话。

## 会话配置（session.update）

连接建立后通过 DataChannel 或 AOQ data track 发送 `session.update` 事件配置会话：

```json
{
  "type": "session.update",
  "session": {
    "modalities": ["text", "audio"],
    "voice": "Ethan",
    "input_audio_format": "pcm",
    "output_audio_format": "pcm",
    "instructions": "系统提示词",
    "turn_detection": {
      "type": "semantic_vad",
      "threshold": 0.5,
      "silence_duration_ms": 800
    }
  }
}
```

- `input_audio_format` / `output_audio_format`：当前仅支持 `pcm`；输入 16 kHz，输出 24 kHz
- `turn_detection.type`：`server_vad` 或 `semantic_vad`；使用 qwen3.5-omni-realtime 系列模型推荐 `semantic_vad`；设为 `null` 表示手动模式（WebRTC 不支持）

## AOQ SDK 核心 API

### 媒体流发送控制

`enableSendMediaStream(trackType, enable)` 控制音频/视频发送开关，支持独立控制。必须在 `createEngine` 之后调用；未调用时建连成功后 SDK 立即开始发送。

### 音频功能

AOQ SDK 提供完整音频能力，包含：
- **采集**：`startAudioCapture(config)`，支持内部采集（默认）和外部采集（`isExternal=true`）
- **播放**：`startAudioPlayer(config)`，支持暂停/恢复（带淡入淡出 `fadeMs` 参数）和打断当前轮
- **编解码**：`setAudioEncoderConfig` / `setAudioDecoderConfig`，支持 PCM（AudioPCM）和 Opus（AudioOpus）两种格式，PCM 支持 8K/16K/32K/48K 采样率
- **扬声器管理**：`enableSpeakerphone(enable)`，需在 VoIP 模式下才可切换
- **自定义音频播放**：设置 `isExternal=true` 启动播放器后，通过 `setAudioFrameObserver` + `enableAudioFrameObserver` 接收 PCM 帧回调，自行渲染
- **自定义音频采集**：通过 `addAudioExternalStream` + `pushAudioExternalStreamData` 向 SDK 注入 PCM 数据；硬件采集建议 10ms 一帧，文件解析建议 40ms 一帧；缓冲区满时返回错误码 110，需等待重试
- **音频文件混音**：`startAudioFile(fileId, config)` 将本地音频文件混入推流

### 视频功能

- **采集**：`startVideoCapture(config)`，支持内部摄像头采集和外部帧输入（`isExternal=true`）
- **渲染**：`setLocalView` / `setRemoteView`，渲染模式支持 Auto / Stretch / Fill / Crop
- **编码**：`setVideoEncoderConfig`，编码格式 H.264（默认）或 JPEG（外部编码帧模式）
- **自定义视频输入**：
  - 原始帧模式：`pushExternalVideoCapturedFrame`，支持 BGRA、I420、NV12/NV21、RGBA；iOS 支持 CVPixelBuffer 零拷贝
  - 编码帧模式：`pushExternalVideoEncodedFrame`，目前支持 JPEG 格式，跳过 SDK 内部编码器
  - 两种模式不可混用

### 连接状态管理

SDK 连接状态为四态：`Disconnected(0)` → `Connecting(1)` → `Connected(2)` / `Failed(3)`。`Failed` 是瞬态，SDK 会自动迁移到 `Disconnected`，业务层无需手动调用 `disconnect`。`disconnect` 后引擎不会自动释放，可重新调用 `connect` 重连。

## 注意事项与限制

- AOQ SDK 不支持浏览器环境，仅支持 Android / iOS / HarmonyOS 原生应用
- WebRTC 协议不提供官方 SDK，Web 端通过原生 WebRTC API 接入，其他端通过开源项目或第三方 RTC 服务商接入
- 音视频轨道数据（AOQ）通过媒体轨道直接传输，无需发送 `input_audio_buffer.append` 或 `input_image_buffer.append` 事件
- 模型并发[限流](../concepts/rate-limit.md)条件参见百炼控制台的[限流](../concepts/rate-limit.md)文档；模型名称、快照版本、价格等信息以控制台展示为准
- AOQ SDK 异常处理优先内部恢复，仅在物理限制（网络、设备、资源）或外部因素（token 无效）无法恢复时才回调错误
- `onPlaybackAudioFrame` 回调在 SDK 内部线程触发，回调中的数据指针仅在回调期间有效，异步使用需自行拷贝

## 来源文档

- [Realtime API简介](../../raw/model-user-guide/realtime-api-user-guide/realtime-api-overview.md)
- [SDK下载](../../raw/model-user-guide/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
- [Token鉴权](../../raw/model-user-guide/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
- [实现接通模型/应用](../../raw/model-user-guide/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-connect-model.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/realtime-api-user-guide/realtime-api-best-practices/best-practice-webrtc-omni-realtime.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/realtime-api-user-guide/realtime-api-best-practices/best-practice-webrtc-multimodal-dialog.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/realtime-api-user-guide/realtime-api-best-practices/best-practice-aoq-omni-realtime.md)
- [AOQ SDK简介](../../raw/model-user-guide/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
- [媒体流发送管理](../../raw/model-user-guide/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-media-stream-control.md)
- [音频常用功能介绍](../../raw/model-user-guide/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)
- [自定义音频播放](../../raw/model-user-guide/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-playback.md)
- [自定义音频采集](../../raw/model-user-guide/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-audio-capture.md)
- [连接状态管理](../../raw/model-user-guide/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-connection-management.md)
- [视频常用功能介绍](../../raw/model-user-guide/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)
- [自定义视频输入](../../raw/model-user-guide/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-custom-video-input.md)







