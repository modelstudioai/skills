# AOQ 接入

介绍通过 AOQ 接入 Realtime API 的连接流程和示例。

**说明**开始前，请先查看[接入概览](raw/model-api-reference/realtime-api-user-guide/realtime-model-connection/realtime-connect-model.md)中的前提条件。

AOQ 基于 QUIC 协议深度定制，适合移动端原生应用，支持音频/视频/数据混合传输，内置极致抗弱网能力。以下以实时全模态（Omni）的 iOS Demo 为例介绍 AOQ 接入流程。AOQ SDK API 详情请参见[AOQ客户端SDK](raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)。

## 整体流程时序图

![AOQ中文1](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5755914871/p1088073.jpg)

开始前，请从[SDK 下载](raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)获取 AOQ Client SDK 和 Opus 插件，将 `AoqClientSdk.framework` 与 `PluginOpus.framework` 导入 Xcode 工程，并选择 **Embed & Sign**。

## 创建引擎并设置回调

```
let config = AoqCreateConfig()
config.workDir = workDir
config.enableDumpAudio = false
engine = AoqClientEngine.createEngine(config, delegate: self)
```

实现 `AoqEngineDelegate` 协议监听 `onConnectionStatusChange`、`onDataMsg`、`onError` 等回调。

## 启动音频采集与播放

```
// 音频采集
let capCfg = AoqAudioCaptureConfig()
capCfg.channel = 1; capCfg.isExternal = false
engine.startAudioCapture(capCfg)

// 音频播放
let playCfg = AoqAudioPlaybackConfig()
playCfg.channel = 1; playCfg.isExternal = false
engine.startAudioPlayer(playCfg)

// 视频采集（可选）
let vidCfg = AoqVideoCaptureConfig()
vidCfg.width = 720; vidCfg.height = 1280; vidCfg.fps = 15
engine.startVideoCapture(vidCfg)
```

## 获取连接凭证

由业务 AppServer 代理百炼请求，参见[Token鉴权](raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。

## 设置编解码及建立连接

设置编解码参数后调用 `connect`：

```
// 音频编解码配置
let encCfg = AoqAudioCodecConfig()
encCfg.codecType = .audioOpus; encCfg.sampleRate = 16000; encCfg.channel = 1
engine.setAudioEncoderConfig(encCfg)
engine.setAudioDecoderConfig(encCfg)

// connect 前关闭媒体发送，待 session.updated 后再开启
engine.enableSendMediaStream(.audio, enable: false)

let config = AoqConnectConfig()
config.token = token
config.sid = sid
config.certFingerprint = certificate
config.relayEndpoints = relayEndpoints
config.workspaceIdHash = workspaceIdHash
config.publishTracks = [audioTrack, dataTrack]
config.subscribeTracks = [audioTrack, dataTrack]
engine.connect(config)
```

**重要****重要**：AOQ SDK 在建连后会默认发送媒体数据，此示例演示了在连接模型时先关闭媒体发送，待会话就绪后再开启的流程。

## 配置 AI 会话

连接成功后发送 `session.update` 的示例，详见[客户端事件](raw/model-api-reference/omni-realtime-api/client-events.md)：

```
func onConnectionStatusChange(_ status: AoqConnectionStatus) {
    if status == .connected { sendSessionUpdate() }
}

private func sendSessionUpdate() {
    let json = """
    {
      // 该事件的id，由客户端生成
      "event_id": "event_ToPZqeobitzUJnt3QqtWg",
      // 事件类型，固定为session.update
      "type": "session.update",
      // 会话配置
      "session": {
          // 输出模态，支持设置为["text"]（仅输出文本）或["text","audio"]（输出文本与音频）。
          "modalities": [
              "text",
              "audio"
          ],
          // 输出音频的音色
          "voice": "Tina",
          // 输入音频格式，当前仅支持设置为pcm。输入音频为16 kHz采样率的PCM音频流。
          "input_audio_format": "pcm",
          // 输出音频格式，当前仅支持设置为pcm。输出音频为24 kHz采样率的PCM音频流。
          "output_audio_format": "pcm",
          // 系统消息，用于设定模型的目标或角色。
          "instructions": "你是某五星级酒店的AI客服专员，请准确且友好地解答客户关于房型、设施、价格、预订政策的咨询。请始终以专业和乐于助人的态度回应，杜绝提供未经证实或超出酒店服务范围的信息。",
          // 是否开启语音活动检测。若需启用，需传入一个配置对象，服务端将据此自动检测语音起止。
          // 设置为null表示由客户端决定何时发起模型响应。
          "turn_detection": {
              // VAD类型，取值为server_vad或semantic_vad。Qwen3.8-Omni-Flash-Realtime和Qwen3.5-Omni-Realtime系列推荐设为semantic_vad。
              "type": "semantic_vad",
              // VAD检测阈值。建议在嘈杂的环境中增加，在安静的环境中降低。
              "threshold": 0.5,
              // 检测语音停止的静音持续时间，超过此值后会触发模型响应
              "silence_duration_ms": 800
          }
      }
    }
    """
    let msg = AoqDataMsg()
    msg.data = json.data(using: .utf8)!
    engine.send(msg)
}
```

## 收到 session.updated 后开启媒体发送

收到模型回复 `session.updated` 的示例，详见[服务端事件](raw/model-api-reference/omni-realtime-api/server-events.md)：

```
func onDataMsg(_ msg: AoqDataMsg) {
    guard let obj = try? JSONSerialization.jsonObject(with: msg.data) as? [String: Any],
          let type = obj["type"] as? String else { return }
    if type == "session.updated" {
        engine.enableSendMediaStream(.audio, enable: true)
        engine.enableSendMediaStream(.video, enable: true)
    }
}
```

**重要**

1.  必须在收到 `session.updated` 后才开启媒体流发送，否则服务端可能尚未准备好接收数据。
    
2.  建连时添加的音频轨道和视频轨道（即 AOQ 媒体通道）会自动将数据传输到服务端。
    
    1.  音频：通过音频轨道直接传输，无需发送 `input_audio_buffer.append` 事件。
    2.  视频：通过视频轨道发送画面帧，无需发送 `input_image_buffer.append` 事件。
3.  建连时添加的 DATA 轨道（即 AOQ 文本通道）用于客户端和服务端的文本通信。客户端通过此通道发送客户端事件、接收服务端事件。
    

## 断开连接与销毁引擎

```
engine.disconnect()
AoqClientEngine.destroy()
```

## 模型接入最佳实践

-   [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
-   [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
-   [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
-   [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
-   [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
