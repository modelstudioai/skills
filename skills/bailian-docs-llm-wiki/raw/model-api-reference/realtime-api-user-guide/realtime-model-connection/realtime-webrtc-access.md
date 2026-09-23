# WebRTC 接入

介绍通过 WebRTC 接入 Realtime API 的连接流程和示例。

**说明**开始前，请先查看[接入概览](raw/model-api-reference/realtime-api-user-guide/realtime-model-connection/realtime-connect-model.md)中的前提条件。

WebRTC 不提供专用 SDK。Web 端可直接使用浏览器原生 JavaScript API 接入，其他端可通过开源 WebRTC 库或支持标准 WebRTC 协议的第三方 RTC 服务接入。以下以 Web 端 JavaScript 为例进行介绍。

## 整体流程图

![AOQ中文2](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5755914871/p1088074.jpg)

## 建立连接

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

## 配置目标模型参数

监听模型通过 DataChannel 返回的消息，确保交互时序正确：

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

## 收发媒体数据

建连时添加的音频轨道和视频轨道（即 RTP 媒体通道）会自动将数据传输到服务端。

-   音频：通过音频轨道（RTP）直接传输，无需发送 `input_audio_buffer.append` 事件。
-   图片：通过视频轨道（RTP）发送画面帧，不支持 `input_image_buffer.append` 事件。

**说明**WebRTC 仅支持服务端 VAD 模式（`server_vad` 或 `semantic_vad`），不支持手动模式。

## Demo 源码

### 前提条件

-   使用支持 WebRTC 的现代浏览器（Chrome、Edge、Firefox、Safari 等）。
-   浏览器需要麦克风权限。
-   浏览器受跨域安全策略限制，无法直接向服务端发起建连请求，因此需要通过终端执行 curl 命令完成连接建立。

### 运行示例

新建一个 HTML 文件，命名为 `webrtc_demo.html`，并将以下代码复制到文件中：

[webrtc\_demo.html](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260715/crtwmi/webrtc_demo.html)。

在浏览器中打开此文件，按以下步骤操作：

1.  点击开始会话，页面会自动生成 Offer SDP 和对应的 curl 命令。
2.  点击复制 curl 命令，在终端中执行。命令返回的内容即为 Answer SDP。
3.  将 Answer SDP 粘贴到页面的 Answer SDP 文本框中，点击设置 Answer 即可建立连接并开始语音对话。

## 最佳实践

-   [通过WebRTC使用多模态交互套件实现实时通话](raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
-   [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
