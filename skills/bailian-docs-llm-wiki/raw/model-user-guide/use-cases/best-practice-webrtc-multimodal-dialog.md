# 通过WebRTC使用多模态交互套件实现实时通话

本文档说明如何在浏览器端通过 WebRTC + JavaScript 接入通义多模态交互套件（multimodal-dialog），实现与多模态 AI 应用的实时音视频交互。

**说明**

多模态交互套件面向 **AI/AR 眼镜、学习机、智能机器人**等硬件场景，提供可视化应用配置、预置 Agent/插件、音色管理等完整业务能力。WebRTC 模式下音频通过 UDP 直接传输，内置回声消除和降噪，适合浏览器端低延迟交互场景。

## **前提条件及注意事项**

1.  已在百炼控制台完成以下准备：
    
    -   已[配置 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并将其[设置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
        
    -   创建多模态交互应用，获取 **Workspace ID** 和 **App ID**（详情请参见[应用创建](https://help.aliyun.com/zh/model-studio/multimodal-app-creation)）。
        
    -   在应用中完成模型、音色、提示词、Agent/插件等配置（详情请参见[应用配置](https://help.aliyun.com/zh/model-studio/multimodal-app-configuration)）。
        
2.  使用支持 WebRTC 的现代浏览器（Chrome、Edge、Firefox、Safari 等）。
    
3.  浏览器需要麦克风权限；如需视频交互，还需摄像头权限。
    
4.  浏览器无法直接向服务端发起 SDP 交换请求（受 CORS 限制），Demo 中需通过终端执行 curl 命令完成连接建立；正式产品中由业务后端代理时不存在此限制。
    

## **实现实时通话**

以下时序图展示了整个 WebRTC 实时通话的完整流程：

WebRTC 多模态交互套件实时通话流程时序图

![1111](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6265914871/p1088078.svg)

### **创建 RTCPeerConnection**

调用浏览器原生 `RTCPeerConnection` 构造函数创建连接实例。服务端采用 ICE-lite 模式直连，无需配置 ICE 服务器。

```
pc = new RTCPeerConnection();
```

同时注册关键回调：

```
pc.onconnectionstatechange = () => {
  if (pc.connectionState === 'connected') {
    // 连接成功
  } else if (['failed', 'closed', 'disconnected'].includes(pc.connectionState)) {
    // 连接断开，清理资源
    endSession();
  }
};

pc.ontrack = (e) => {
  // 将远端音频流绑定到 audio 元素播放
  const remoteAudio = document.createElement('audio');
  remoteAudio.autoplay = true;
  remoteAudio.srcObject = e.streams[0];
  document.body.appendChild(remoteAudio);
};
```

### **获取本地媒体流**

通过 `navigator.mediaDevices.getUserMedia` 获取麦克风权限（必须），以及摄像头权限（可选）。

**纯音频模式：**

```
const localStream = await navigator.mediaDevices.getUserMedia({ audio: true });
```

**音视频模式（需要 AI 视觉理解时）：**

```
const localStream = await navigator.mediaDevices.getUserMedia({
  audio: true,
  video: {
    facingMode: { ideal: 'environment' },  // 后置摄像头
    frameRate: { ideal: 30, max: 30 },
    width: { ideal: 640 },
    height: { ideal: 480 }
  }
});
```

**说明**

视频帧率根据场景调整。需要 AI 实时理解画面的场景（如物体识别、场景描述）建议 15-30 fps。

### **添加媒体轨道到 PeerConnection**

将本地音频轨道添加到 PeerConnection。如果开启了视频，视频轨道一并添加。

```
localStream.getTracks().forEach(track => pc.addTrack(track, localStream));
```

**维持视频发送质量（可选）：**

在弱网环境下，浏览器可能自动降低视频分辨率。可通过设置 sender 参数尽量维持：

```
const sender = pc.getSenders().find(s => s.track && s.track.kind === 'video');
if (sender) {
  const params = sender.getParameters();
  if (!params.encodings || params.encodings.length === 0) params.encodings = [{}];
  params.encodings[0].scaleResolutionDownBy = 1.0;
  params.encodings[0].maxBitrate = 2500000;  // 2.5 Mbps
  params.encodings[0].maxFramerate = 30;
  params.degradationPreference = 'maintain-resolution';
  await sender.setParameters(params);
}
```

### **创建 DataChannel**

创建名为 `oai-events` 的 DataChannel，用于与服务端交换控制消息（run-task、事件通知等）。

```
const dc = pc.createDataChannel('oai-events');

dc.onopen = () => {
  console.log('DataChannel open');
  // DataChannel 就绪后发送 run-task
  sendStartMessage(dc);
};

dc.onmessage = (e) => {
  const evt = JSON.parse(e.data);
  handleServerEvent(evt, dc);
};
```

同时监听 `pc.ondatachannel` 以处理服务端主动创建的 DataChannel：

```
pc.ondatachannel = (event) => {
  const ch = event.channel;
  if (ch.label === 'txt' || ch.label === 'oai-events') {
    ch.onopen = () => sendStartMessage(ch);
    ch.onmessage = (e) => handleServerEvent(JSON.parse(e.data), ch);
  }
};
```

### **生成 Offer SDP**

调用 `createOffer` 并 `setLocalDescription`，浏览器生成包含本地媒体能力描述的 Offer SDP。服务端采用 ICE-lite 模式，客户端无需等待 ICE candidates 收集完成，`setLocalDescription` 后即可发送。

```
const offer = await pc.createOffer();
await pc.setLocalDescription(offer);

// offer.sdp 即为待发送的 Offer SDP 字符串
```

### **交换 SDP（HTTP POST）**

将 Offer SDP 通过 HTTP POST 发送到服务端 WebRTC 端点，服务端返回 Answer SDP。

**Endpoint 格式：**`{workspace_id}.{region}.maas.aliyuncs.com`，其中 `workspace_id` 为百炼工作空间 ID（如 `llm-xxxxxxxxxx`），`region` 为部署区域（如 `cn-beijing`）。创建工作空间后即可在百炼控制台获取。

**请求配置：**

**配置项**

**说明**

请求地址

`POST https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/webrtc/inference?model=multimodal-dialog`

Content-Type

`application/sdp`

请求头

`Authorization: Bearer {DASHSCOPE_API_KEY}`

请求体

客户端生成的 Offer SDP 字符串

响应

成功：HTTP 200，返回服务端 Answer SDP 字符串

```
const API_KEY = 'your-api-key';       // 百炼控制台获取
const WORKSPACE_ID = '{workspace-id}';  // 百炼控制台获取
const REGION = 'cn-beijing';
const SIGNALING_URL = `https://${WORKSPACE_ID}.${REGION}.maas.aliyuncs.com/api/v1/webrtc/inference?model=multimodal-dialog`;

const resp = await fetch(SIGNALING_URL, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/sdp',
    'Authorization': `Bearer ${API_KEY}`,
  },
  body: offer.sdp,
});

if (!resp.ok) throw new Error('SDP 交换失败: ' + resp.status);
const answerSdp = await resp.text();
```

**说明**

由于浏览器端受 CORS 限制无法直接请求服务端，Demo 中需用户手动在终端执行 curl 命令。正式产品中应通过业务后端代理此请求。

**curl 命令格式：**

```
curl -X POST 'https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/webrtc/inference?model=multimodal-dialog' \
  -H 'Content-Type: application/sdp' \
  -H 'Authorization: Bearer $DASHSCOPE_API_KEY' \
  --data-binary '<Offer SDP 内容>'
```

### **设置 Answer SDP 建立连接**

将从服务端获取的 Answer SDP 设置为远端描述，WebRTC 连接随即建立。

```
await pc.setRemoteDescription({ type: 'answer', sdp: answerSdp });
// 连接建立完成，pc.connectionState 将变为 'connected'
```

### **发送 run-task 启动会话**

WebRTC 连接建立、DataChannel 就绪后，客户端发送 **run-task** 消息启动多模态会话。

```
let currentTaskId = null;

function sendStartMessage(channel) {
  currentTaskId = generateTaskId();
  const msg = {
    payload: {
      input: {
        workspace_id: '{workspace-id}',
        app_id: '{app-id}',
        directive: 'Start'
      },
      task_group: 'aigc',
      task: 'multimodal-generation',
      function: 'generation',
      model: 'multimodal-dialog',
      parameters: {
        client_info: {
          user_id: '{user-id}',
          device: { uuid: '{device-uuid}' },
          network: { ip: '{client-ip}' }
        },
        upstream: {
          mode: 'duplex',
          sample_rate: '16000',
          type: 'AudioAndVideo'   // 'Audio' 或 'AudioAndVideo'
        },
        dialog_attributes: {
          vocabulary_id: '{vocabulary-id}'  // 可选
        },
        downstream: {
          voice: 'longanhuan',
          sample_rate: 24000,
          audio_format: 'pcm'
        }
      }
    },
    header: {
      streaming: 'duplex',
      action: 'run-task',
      task_id: currentTaskId
    }
  };
  channel.send(JSON.stringify(msg));
}

function generateTaskId() {
  if (window.crypto && typeof window.crypto.randomUUID === 'function') {
    return window.crypto.randomUUID().replace(/-/g, '');
  }
  const r = () => Math.random().toString(16).slice(2);
  return (Date.now().toString(16) + r() + r()).slice(0, 32);
}
```

**参数说明：**

**参数路径**

**类型**

**说明**

`payload.input.workspace_id`

string

百炼工作空间 ID，在控制台「应用管理」中获取

`payload.input.app_id`

string

多模态交互应用 ID，在控制台「应用管理」中获取

`payload.input.directive`

string

固定值 `Start`

`payload.parameters.client_info.user_id`

string

业务系统中的用户标识，用于日志追踪

`payload.parameters.client_info.device.uuid`

string

设备唯一标识，用于设备维度的数据分析

`payload.parameters.upstream.mode`

string

交互模式：`duplex`（全双工）、`push2talk`（按住说话）、`tap2talk`（点击说话）

`payload.parameters.upstream.type`

string

上行媒体类型：`Audio`（纯语音）或 `AudioAndVideo`（音视频）

`payload.parameters.upstream.sample_rate`

string

上行音频采样率，通常 `16000`

`payload.parameters.downstream.voice`

string

下行音色，可在百炼控制台音色列表中选取

`payload.parameters.downstream.sample_rate`

number

下行音频采样率，通常 `24000`

`payload.parameters.dialog_attributes.vocabulary_id`

string

可选，热词表 ID，提升专有名词识别准确率

**说明**

应用中的模型选择、提示词、Agent/插件、知识库等配置均在百炼控制台可视化完成，无需通过代码传入。run-task 只需指定 `workspace_id` 和 `app_id`，服务端会自动加载对应配置。

### **实时对话**

run-task 发送成功后，进入实时对话状态：

-   **上行**：浏览器采集的音频/视频通过 RTP 协议自动发送到服务端
    
-   **下行音频**：AI 语音回复通过 `ontrack` 回调接收并播放
    
-   **下行事件**：通过 DataChannel 接收业务事件
    

```
function handleServerEvent(evt, channel) {
  const type = evt.type || evt.header?.action;

  switch (type) {
    case 'open_videochat':
      // 服务端请求开启视频通道
      // 延迟数秒响应，确保视频处理通道就绪
      setTimeout(() => {
        channel.send(JSON.stringify({
          payload: {
            input: { text: '', type: 'prompt', directive: 'RequestToRespond' },
            parameters: {
              biz_params: {
                videos: [{ action: 'connect', type: 'voicechat_video_channel' }]
              }
            }
          },
          header: {
            streaming: 'duplex',
            action: 'continue-task',
            task_id: currentTaskId
          }
        }));
      }, 3000);
      break;

    default:
      console.log('[服务端事件]', type, evt);
      break;
  }
}
```

**说明**

**open\_videochat 机制**：当 `upstream.type` 设为 `AudioAndVideo` 时，客户端已通过 WebRTC 发送视频轨道。服务端在需要时（如 AI Agent 判断需要"看"画面）会推送 `open_videochat` 事件，客户端需回复 `continue-task` 确认视频通道建立。该机制允许按需开启视频处理，节省服务端资源。

**静音 / 取消静音：**

```
// 静音
localStream.getAudioTracks().forEach(t => { t.enabled = false; });
// 取消静音
localStream.getAudioTracks().forEach(t => { t.enabled = true; });
```

**开启/关闭视频：**

```
// 关闭视频
localStream.getVideoTracks().forEach(t => { t.enabled = false; });
// 开启视频
localStream.getVideoTracks().forEach(t => { t.enabled = true; });
```

### **结束会话与资源清理**

通话结束后需要正确释放所有资源，避免内存泄漏和设备占用。

```
function endSession() {
  // 1. 关闭 DataChannel
  if (dataChannel) {
    dataChannel.close();
    dataChannel = null;
  }

  // 2. 停止本地媒体流（释放麦克风/摄像头）
  if (localStream) {
    localStream.getTracks().forEach(t => t.stop());
    localStream = null;
  }

  // 3. 关闭 PeerConnection
  if (pc) {
    pc.close();
    pc = null;
  }

  // 4. 重置状态
  currentTaskId = null;
}
```

## **注意事项**

1.  **API Key 安全**：切勿将 API Key 硬编码在前端代码中。生产环境应通过后端服务代理 SDP 交换请求，API Key 仅存放在服务端。
    
2.  **CORS 限制**：浏览器端无法直接调用百炼 API 进行 SDP 交换，正式产品中需要通过后端代理转发请求。
    
3.  **HTTPS 要求**：`getUserMedia` 在非 localhost 环境下要求页面必须通过 HTTPS 提供服务。
    
4.  **交互模式选择**：多模态套件支持三种交互模式——`duplex`（全双工，用户可随时打断）、`push2talk`（按住说话）、`tap2talk`（点击说话）。根据硬件形态选择合适的模式。
    
5.  **视频帧率**：视频理解场景建议 15-30 fps；如果仅需偶尔拍照识别，可降低帧率节省带宽。
    
6.  **浏览器兼容性**：推荐使用 Chrome 90+、Edge 90+、Firefox 85+、Safari 15+。
    
7.  **单实例限制**：同一页面同时只应维护一个 `RTCPeerConnection` 实例，创建新会话前需先关闭旧连接。
    

## **完整 Demo 示例下载**

以下是一个完整的 HTML 页面 Demo，可直接在浏览器中运行体验多模态交互。由于浏览器 CORS 限制，SDP 交换通过 curl 命令手动完成。

[webrtc\_multimodel\_demo.html](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260715/ifirko/webrtc_multimodel_demo.html)

**使用步骤：**

1.  在浏览器中打开该文件。
    
2.  填写连接配置：Endpoint（格式为 `{workspace_id}.{region}.maas.aliyuncs.com`）、API Key、Workspace ID 和 App ID。
    
3.  如需视频交互，勾选“开启视频”。
    
4.  点击**开始会话**，允许浏览器访问麦克风（及摄像头）。
    
5.  如果浏览器能直接发起请求（无 CORS 限制），将自动完成连接；否则页面会显示 curl 命令，复制到终端执行后将返回的 Answer SDP 粘贴回页面即可。
    
6.  连接建立后，对着麦克风说话即可与多模态 AI 实时对话。
    
7.  通话结束后可点击“下载远端音频”保存 AI 回复的录音。
    

## **相关文档**

-   [通义多模态交互开发套件产品概述](https://help.aliyun.com/zh/model-studio/multimodal-products-overview)
    
-   [多模态交互套件使用指南](https://help.aliyun.com/zh/model-studio/multimodal-guidelines/)
    
-   [多模态交互 SDK（Python/Java）GitHub 示例代码](https://github.com/aliyun/alibabacloud-bailian-speech-demo/tree/master/samples/conversation/multimodal_dialog)
    
-   [WebRTC API (MDN)](https://developer.mozilla.org/zh-CN/docs/Web/API/WebRTC_API)
    
-   [WebRTC 接入模型/应用](https://help.aliyun.com/zh/model-studio/realtime-connect-model#conn-rtc-title)
