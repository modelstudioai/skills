# 实现接通模型/应用

介绍如何通过 AOQ、WebRTC、WebSocket 三种协议接入 Realtime API 模型或应用，包含各协议的连接流程、时序图和代码示例。

## **AOQ 接入**

AOQ 基于 QUIC 协议深度定制，适合移动端原生应用，支持音频/视频/数据混合传输，内置极致抗弱网能力。以下以 iOS Demo 为例。

### **整体流程时序图**

![AOQ中文1](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5755914871/p1088073.jpg)

### **创建引擎并设置回调**

```
let config = AoqCreateConfig()
config.workDir = workDir
config.enableDumpAudio = false
engine = AoqClientEngine.createEngine(config, delegate: self)
```

实现 `AoqEngineDelegate` 协议监听 `onConnectionStatusChange`、`onDataMsg`、`onError` 等回调。

### **启动音频采集与播放**

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

### **获取连接凭证**

由业务 AppServer 代理百炼请求，参考 [Token 鉴权](https://help.aliyun.com/zh/model-studio/realtime-token-authentication) 章节。

### **设置编解码及建立连接**

设置编解码参数后调用 `connect`：

```
// 音频编解码配置
let encCfg = AoqAudioCodecConfig()
encCfg.codecType = .audioPCM; encCfg.sampleRate = 16000; encCfg.channel = 1
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

**重要**

**重要**：AOQ SDK 在建联后会默认发送媒体数据，此示例演示了连接模型时关闭媒体发送的能力。

### **配置 AI 会话**

连接成功后发送 `session.update` 的示例，详见[模型客户端事件参考](https://help.aliyun.com/zh/model-studio/client-events)：

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
          "voice": "Ethan",
          // 输入音频格式，当前仅支持设置为pcm。输入音频为16 kHz采样率的PCM音频流。
          "input_audio_format": "pcm",
          // 输出音频格式，当前仅支持设置为pcm。输出音频为24 kHz采样率的PCM音频流。
          "output_audio_format": "pcm",
          // 系统消息，用于设定模型的目标或角色。
          "instructions": "你是某五星级酒店的AI客服专员，请准确且友好地解答客户关于房型、设施、价格、预订政策的咨询。请始终以专业和乐于助人的态度回应，杜绝提供未经证实或超出酒店服务范围的信息。",
          // 是否开启语音活动检测。若需启用，需传入一个配置对象，服务端将据此自动检测语音起止。
          // 设置为null表示由客户端决定何时发起模型响应。
          "turn_detection": {
              // VAD类型，取值为server_vad或semantic_vad。使用qwen3.5-omni-realtime模型时推荐设为semantic_vad。
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

### **收到 session.updated 后开启媒体发送**

收到模型回复 `session.updated` 的示例，详见[模型服务器事件参考](https://help.aliyun.com/zh/model-studio/server-events)：

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

**重要**：

1.  模型必须在收到 `session.updated` 后才开启媒体流发送，否则 AI 侧可能还未准备好接收数据。
    
2.  建连时添加的音频轨道和视频轨道（即 AOQ 媒体通道）会自动将数据传输到服务端。
    
    1.  音频：通过音频轨道直接传输，无需发送 `input_audio_buffer.append` 事件。
        
    2.  视频：通过视频轨道发送画面帧，无需发送 `input_image_buffer.append` 事件。
        

### **断开连接与销毁引擎**

```
engine.disconnect()
AoqClientEngine.destroy()
```

## **WebRTC 接入**

WebRTC 协议不提供 SDK，Web 端可以通过 JavaScript，其他端可以通过开源项目或者第三方支持标准 WebRTC 协议的 RTC 服务商进行接入。以下文档以 Web 端 JavaScript 为例进行介绍。

### **整体流程图**

![AOQ中文2](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5755914871/p1088074.jpg)

### **建立连接**

```
# pip install aiortc aiohttp certifi
import asyncio, aiohttp, ssl, certifi
from aiortc import RTCPeerConnection, RTCConfiguration, RTCSessionDescription
from aiortc.mediastreams import AudioStreamTrack

API_KEY = "your-api-key"
MODEL = "目标模型"
SIGNALING_URL = f"https://{{endpoint}}/api/v1/webrtc/realtime?model={MODEL}"

async def connect():
    pc = RTCPeerConnection(RTCConfiguration(iceServers=[]))

    # 添加音频轨道，确保 Offer SDP 包含 m=audio（服务端必需）
    pc.addTrack(AudioStreamTrack())

    # 创建 DataChannel 以触发 SDP 协商（名称可自定义，服务端会通过名为 "txt" 的通道推送事件）
    pc.createDataChannel("oai-events")

    # SDP 交换：创建 Offer 并发送到服务端
    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)

    async with aiohttp.ClientSession() as session:
        async with session.post(
            SIGNALING_URL,
            ssl=ssl.create_default_context(cafile=certifi.where()),
            data=offer.sdp.encode("utf-8"),
            headers={
                "Content-Type": "application/sdp",
                "Authorization": f"Bearer {API_KEY}",
            },
        ) as resp:
            if not resp.ok:
                raise Exception(f"SDP 交换失败: {resp.status} {await resp.text()}")
            answer_sdp = await resp.text()

    print("=== Offer SDP ===")
    print(offer.sdp)
    print("=== Answer SDP ===")
    print(answer_sdp)

    # ICE 建连自动完成
    await pc.setRemoteDescription(RTCSessionDescription(sdp=answer_sdp, type="answer"))
    print("WebRTC 连接已建立")
    return pc
```

### **配置目标模型参数**

监听模型返回的 DataChannel 消息保证交互时序：

```
pc.ondatachannel = (event) => {
  const ch = event.channel;
  ch.onmessage = (e) => {
    let obj;
    try { obj = JSON.parse(e.data); }
    catch (err) {
      return;
    }
    if (obj?.type === "session.created") {
      sendUpdate(event.channel);
      //开始推送音视频
      audioSender?.replaceTrack(audioTrack);
      videoSender?.replaceTrack(videoTrack);
    }
  };
};
```

### **收发媒体数据**

建连时添加的音频轨道和视频轨道（即 RTP 媒体通道）会自动将数据传输到服务端。

-   音频：通过音频轨道（RTP）直接传输，无需发送 `input_audio_buffer.append` 事件。
    
-   图片：通过视频轨道（RTP）发送画面帧，不支持 `input_image_buffer.append` 事件。
    

**说明**

WebRTC 仅支持服务端 VAD 模式（`server_vad` 或 `semantic_vad`），不支持手动模式。

### **Demo 源码**

#### **前提条件**

-   使用支持 WebRTC 的现代浏览器（Chrome、Edge、Firefox、Safari 等）。
    
-   浏览器需要麦克风权限。
    
-   浏览器无法直接向服务端发起建立连接的请求（受浏览器跨域安全策略限制），因此需要通过终端执行 curl 命令来完成连接建立。
    

#### **运行示例**

新建一个 HTML 文件，命名为 `webrtc_demo.html`，并将以下代码复制到文件中：

[webrtc\_demo.html](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260715/crtwmi/webrtc_demo.html)。

在浏览器中打开此文件，按以下步骤操作：

1.  点击开始会话，页面会自动生成 Offer SDP 和对应的 curl 命令。
    
2.  点击复制 curl 命令，在终端中执行。命令返回的内容即为 Answer SDP。
    
3.  将 Answer SDP 粘贴到页面的 Answer SDP 文本框中，点击设置 Answer 即可建立连接并开始语音对话。
    

## **WebSocket 接入**

可以通过 DashScope SDK 或者模型的 API 进行接入，详见：

-   [实时全模态](https://help.aliyun.com/zh/model-studio/realtime#bdaa43cdd7hsd)
    
-   [多模态开发套件](https://help.aliyun.com/zh/model-studio/multimodal-interaction-protocol/)
    
-   [实时语音识别](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-websocket-api)
    
-   [实时语音合成](https://help.aliyun.com/zh/model-studio/cosyvoice-websocket-api)
