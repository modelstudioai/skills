# Qwen-Omni-Realtime WebRTC 接入

Qwen-Omni-Realtime WebRTC 接入

WebRTC 使用媒体轨道传输音视频，使用 DataChannel 传输模型事件和文本。Web 端可使用浏览器原生 API，其他端可使用支持标准 WebRTC 的库。百炼不提供专用 WebRTC SDK。

本文提供本模型的 WebRTC 接入流程和完整的浏览器端示例。

## 适用范围

本文面向 Qwen-Omni-Realtime。现有接入说明覆盖：qwen3.8-omni-flash-realtime、qwen3.5-omni-plus-realtime、qwen3.5-omni-flash-realtime。示例模型为 `qwen3.8-omni-flash-realtime`。

-   使用所选地域和业务空间对应的 [API Key](raw/model-api-reference/preparations/get-api-key.md) 与 [API Host](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)（不含协议和路径）。
-   北京域名：`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`；新加坡域名：`{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`。
-   长期 API Key 由服务端保管，不放入浏览器或移动端应用。临时 API Key 的生成方式和权限说明参见[生成临时 API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

浏览器采集媒体时使用安全上下文；使用麦克风或摄像头时申请对应权限。接收音频时应处理浏览器自动播放限制。

## 鉴权与 SDP 交换

浏览器向业务 AppServer 提交 Offer SDP。AppServer 使用 API Key 转发以下请求，并将 Answer SDP 原样返回浏览器；长期 API Key 不进入前端。

-   方法：`POST`
-   新加坡地址：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/webrtc/realtime?model=qwen3.8-omni-flash-realtime`
-   请求头：`Authorization: Bearer <API_KEY>`、`Content-Type: application/sdp`
-   请求体：Offer SDP 字符串。
-   成功响应：HTTP 200，正文为 Answer SDP；失败返回 4xx。

以下地址默认为北京地域，请将域名替换为业务空间对应的 API Host：

```
https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/webrtc/realtime?model=qwen3.8-omni-flash-realtime
```

WebRTC 在 SDP 交换时鉴权，不需要先申请 AOQ Token。下文示例中的 `/api/realtime/sdp` 是业务 AppServer 的自建接口，需要实现上述转发，不是百炼提供的 URL。

## 整体流程

![WebRTC 接入时序图](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/images/6a4b3c2d1e0f92f8.png)

1.  业务 AppServer 准备 API Key 和目标模型参数。
2.  客户端创建连接对象并注册回调。
3.  配置媒体方向及 DataChannel，暂不挂载上行媒体轨道。
4.  通过 AppServer 交换 SDP，等待连接及事件通道就绪。
5.  按模型协议完成配置，收到确认后挂载所需上行媒体轨道。
6.  完成交互后停止采集、关闭连接并释放资源。

**说明**

-   音视频通过 WebRTC 媒体轨道传输；应用负责获取本地媒体轨道、绑定远端播放器，并按目标模型的事件定义收发 DataChannel 消息。
    
-   WebRTC 的鉴权在 SDP 交换时完成，无需先获取 AOQ Token。浏览器通过业务 AppServer 完成鉴权请求与 SDP 转发，避免将长期 API Key 放入前端代码。
    
-   连接成功表示传输通道已建立，不代表模型已完成初始化。本页使用 `qwen3.8-omni-flash-realtime` 时，发送 `session.update` 并收到 `session.updated` 后，再开启所需的上行媒体。
    

## 完整示例

以下是浏览器端的完整示例。先按[鉴权与 SDP 交换](#authentication)实现业务 AppServer 的 `/api/realtime/sdp` 接口，再从业务 AppServer 的同源地址打开此 HTML 页面；协议、主机和端口须一致。例如，页面和 `/api/realtime/sdp` 均由 `http://localhost:3000` 提供。服务端负责保存 API Key 并转发 SDP，不要将长期 API Key 放在页面中。点击“开始”建立连接；结束交互时点击“结束”释放资源。本示例每次建立一条连接；需要再次使用时请重新加载页面。

```
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>WebRTC 接入示例</title>
</head>
<body>
<button id="start-session" type="button">开始</button>
<button id="end-session" type="button">结束</button>
<script>
const pc = new RTCPeerConnection({ iceServers: [ ] });

const channels = new Set();
const senders = new Map();
const remoteAudio = document.createElement("audio");
remoteAudio.controls = true; // 自动播放被阻止时，用户可手动播放。
remoteAudio.autoplay = true;
document.body.appendChild(remoteAudio);

let localStream = null;
let eventChannel = null;
let stopped = false;
let started = false;
let sessionCreated = false;
let updateSent = false;
let modelReady = false;
let mediaStarted = false;
const requestController = new AbortController();
const media = {
  sendAudio: true,
  receiveAudio: true,
  sendVideo: false,
};

function mediaDirection(send, receive) {
  if (send && receive) return "sendrecv";
  if (send) return "sendonly";
  if (receive) return "recvonly";
  return "inactive";
}

async function configureMedia() {
  for (const kind of ["audio", "video"]) {
    const send = kind === "audio" ? media.sendAudio : media.sendVideo;
    const receive = kind === "audio" ? media.receiveAudio : false;
    // 保留 m=audio；具体方向组合须由目标服务支持。
    if (kind === "audio" || send || receive) {
      const transceiver = pc.addTransceiver(kind, {
        direction: mediaDirection(send, receive),
      });
      if (send) senders.set(kind, transceiver.sender);
    }
  }
  if (!media.sendAudio && !media.sendVideo) return;
  const stream = await navigator.mediaDevices.getUserMedia({
    audio: media.sendAudio,
    video: media.sendVideo ? {
      width: { ideal: 640 }, height: { ideal: 480 },
      frameRate: { ideal: 2, max: 2 },
    } : false,
  });
  // 用户可能在权限弹窗期间结束通话。
  if (stopped) {
    stream.getTracks().forEach(track => track.stop());
    throw new Error("会话已结束");
  }
  localStream = stream;
  // 此时 sender.track 仍为空，不向模型发送采集数据。
}
// bindDataChannel 的完整实现见“Data 通道发送和接收事件”。
pc.ondatachannel = ({ channel }) => bindDataChannel(channel);
const clientChannel = pc.createDataChannel("oai-events");
bindDataChannel(clientChannel);
pc.onconnectionstatechange = () => {
  console.log("WebRTC 状态：", pc.connectionState);
  if (pc.connectionState === "connected") {
    tryInitializeModel();
  } else if (["failed", "disconnected", "closed"].includes(pc.connectionState)) {
    // 本示例选择结束连接；业务可按需要设计断线恢复策略。
    endSession();
  }
};

function waitForIceComplete() {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => finish(new Error("ICE 收集超时")), 15000);
    function finish(error) {
      clearTimeout(timer);
      pc.removeEventListener("icegatheringstatechange", check);
      requestController.signal.removeEventListener("abort", cancel);
      error ? reject(error) : resolve();
    }
    function check() {
      if (pc.iceGatheringState === "complete") finish();
    }
    function cancel() { finish(new Error("会话已结束")); }
    pc.addEventListener("icegatheringstatechange", check);
    requestController.signal.addEventListener("abort", cancel, { once: true });
    if (stopped) cancel();
    else check();
  });
}

function normalizeAnswerSdp(sdp) {
  return String(sdp).trim().replace(/\r?\n/g, "\r\n") + "\r\n";
}

async function startSession() {
  if (started || stopped) return;
  started = true;
  try {
    await configureMedia();
    if (stopped) return;
    const offer = await pc.createOffer();
    await pc.setLocalDescription(offer);
    await waitForIceComplete();

    // 这是业务自行实现的同源接口，不是百炼官方接口。
    // AppServer 为目标模型转发 SDP，附带 API Key，并原样返回 Answer SDP。
    const response = await fetch("/api/realtime/sdp", {
      method: "POST",
      headers: { "Content-Type": "application/sdp" },
      body: pc.localDescription.sdp,
      signal: requestController.signal,
    });
    if (!response.ok) {
      throw new Error(`SDP 交换失败：${response.status} ${await response.text()}`);
    }
    const answerSdp = normalizeAnswerSdp(await response.text());
    if (stopped) return;
    await pc.setRemoteDescription({ type: "answer", sdp: answerSdp });
    // 后续由 connectionstatechange、DataChannel 和模型事件驱动。
  } catch (error) {
    if (!stopped) console.error("建连失败：", error);
    endSession();
  }
}
function tryInitializeModel() {
  if (stopped || updateSent || !sessionCreated ||
      pc.connectionState !== "connected" ||
      eventChannel?.readyState !== "open") return;
  sendModelEvent({
    event_id: `event_${crypto.randomUUID()}`,
    type: "session.update",
    session: {
      "modalities": media.receiveAudio ? ["text", "audio"] : ["text"],
      "voice": "Tina",
      "turn_detection": { "type": "server_vad" },
    },
  });
  updateSent = true;
}

async function handleModelEvent(event, channel) {
  if (stopped) return;
  if (event.type === "session.created") {
    sessionCreated = true;
    eventChannel = channel; // 沿收到会话事件的通道发送配置。
    tryInitializeModel();
  } else if (event.type === "session.updated" && updateSent) {
    modelReady = true;
    await startSendingMedia();
  } else if (event.type === "error") {
    console.error("模型错误：", event.error);
    endSession();
  } else {
    // 按所选模型定义展示文本、转录或响应状态；音频从媒体轨道接收。
    console.log("模型事件：", event);
  }
}
async function startSendingMedia() {
  if (stopped || !modelReady || mediaStarted) return;
  mediaStarted = true;

  for (const track of localStream?.getTracks() ?? []) {

    if (stopped) return;
    const sender = senders.get(track.kind);
    if (sender) await sender.replaceTrack(track);
  }
}

// 在 startSession() 前注册。无 streams 的轨道也能正确接收。
const remoteAudioStream = new MediaStream();
pc.ontrack = ({ track }) => {
  if (stopped) return;
  if (track.kind === "audio" && media.receiveAudio) {
    remoteAudioStream.addTrack(track);
    remoteAudio.srcObject = remoteAudioStream;
    remoteAudio.play().catch(() => {
      console.info("自动播放受限，请点击音频控件播放");
    });
  }
};
function endSession() {
  if (stopped) return;
  stopped = true;
  modelReady = false;
  sessionCreated = false;
  updateSent = false;
  mediaStarted = false;
  requestController.abort(); // 取消未完成的 SDP 请求/ICE 等待。
  localStream?.getTracks().forEach(track => track.stop());
  localStream = null;
  channels.forEach(channel => channel.close());
  channels.clear();
  eventChannel = null;
  pc.close();
  senders.clear();
  remoteAudioStream.getTracks().forEach(track => track.stop());
  remoteAudio.pause();
  remoteAudio.srcObject = null;
  remoteAudio.remove();
}
function sendModelEvent(event, channel = eventChannel) {
  if (stopped || pc.connectionState !== "connected" ||
      channel?.readyState !== "open") {
    throw new Error("Data 通道尚不可用");
  }
  channel.send(JSON.stringify(event));
}

function bindDataChannel(channel) {
  channels.add(channel);
  channel.onopen = () => {
    if (stopped) return;
    console.log("DataChannel 已打开：", channel.label);
    tryInitializeModel();
  };
  channel.onmessage = ({ data }) => {
    if (stopped) return;
    let event;
    try { event = JSON.parse(data); }
    catch (error) {
      console.warn("无法解析模型事件：", error);
      return;
    }
    if (!event || typeof event !== "object") return;
    handleModelEvent(event, channel).catch(error => {
      if (!stopped) console.error("模型事件处理失败：", error);
      endSession();
    });
  };
  channel.onerror = error => console.error("DataChannel 错误：", error);
  channel.onclose = () => {
    channels.delete(channel);
    if (channel === eventChannel) endSession();
  };
  if (channel.readyState === "open") channel.onopen();
}

document.getElementById("start-session").addEventListener("click", startSession);
document.getElementById("end-session").addEventListener("click", endSession);
</script>
</body>
</html>
```

## 1\. 准备鉴权和连接参数

业务 AppServer 根据目标模型、地域和业务空间配置 SDP 交换请求。标准 Realtime 建连参数如下；应用专属接入参数以对应最佳实践为准。

配置项

值

方法

`POST`

地址

`https://{endpoint}/api/v1/webrtc/realtime?model={model_name}`

`Content-Type`

`application/sdp`

`Authorization`

`Bearer <API_KEY>`

请求体

Offer SDP

成功响应

Answer SDP

完整地域、地址和鉴权说明见[鉴权与 SDP 交换](#authentication)。业务 AppServer 的接口由业务自行实现，不属于百炼 SDK API。

## 2\. 初始化连接对象并注册回调

Web 端创建 `RTCPeerConnection`，其他端执行对应库的初始化操作。建立连接前注册以下处理逻辑：

-   连接状态变化：判断连接是否成功，以及失败或断开。
    
-   DataChannel 建立、打开、消息和关闭：承载模型事件。
    
-   远端媒体轨道：接收并播放音频，或处理目标应用支持的其他媒体。
    

完整示例在同一脚本中创建连接对象、状态变量和回调。示例每次创建一条连接；结束后再次通话需重新创建这些对象。

连接对象和状态变量见[完整示例](#conn-rtc-complete-example)。

注册消息监听应早于模型初始化，避免遗漏服务端主动发送的会话事件。不要只监听客户端创建的通道：服务端会通过名为 `txt` 的通道推送事件，应处理 `datachannel` 回调。

## 3\. 配置媒体方向和 DataChannel

### 选择媒体方向

以下方向均以客户端为视角。WebRTC 通过媒体收发器协商发送与接收能力：双向为 `sendrecv`，仅发送为 `sendonly`，仅接收为 `recvonly`。最终可用能力还取决于服务端 SDP 应答及模型支持范围。

方向

配置内容

推音频

协商音频发送能力，准备麦克风或外部音频轨道；模型就绪后挂载

拉音频

协商音频接收能力，在远端轨道回调中绑定音频播放

推视频

目标模型支持视觉输入时协商视频发送能力，准备摄像头或外部视频轨道

例如，语音对话一般使用双向音频，带视觉输入的语音对话还需要视频上行。Offer SDP 需要包含音频媒体段 `m=audio`；不能仅因业务无需播放音频就删除该媒体段。

### 本模型的媒体方向

模型/应用

推音频

拉音频

推视频

拉视频

Qwen-Omni-Realtime

语音输入时开启

需要语音回复时开启

需要视觉输入时开启

不支持开启

该表描述业务需要的媒体方向，不承诺所有方向组合都可单独协商。实际配置以目标模型和当前服务端协商能力为准。

### 准备媒体但延后上行

在创建 Offer 前预先协商所需媒体方向。对需要等待初始化确认的模型，先保留发送能力而不挂载真实采集轨道；模型就绪后再通过对应 sender 的 `replaceTrack` 等操作开始发送。接收媒体的处理逻辑可以提前注册。

音频发送、音频接收和视频发送应分别按需配置，不要把打开麦克风、播放音频和模型初始化合并为一个操作。

### 媒体配置示例

下面以双向语音、可选视频上行为例。`media` 的三个开关分别控制音频发送、音频接收和视频发送。`addTransceiver` 预先协商方向，采集到的轨道先保存在本地，直到模型就绪后再挂载到 sender。

代码见[完整示例](#conn-rtc-complete-example)。

视频分辨率和帧率按目标模型要求设置；需要将本地预览与上行帧率分离时，可参考最佳实践中的 Canvas 降帧实现。

### 创建事件通道

在创建 Offer 前创建 DataChannel，使 SDP 包含数据通道协商。客户端创建通道及服务端创建通道的处理方式参见[Data 通道发送和接收事件](#conn-rtc-data-channel)。

DataChannel 负责发送模型初始化、文本和控制事件，并接收模型结果、状态和错误。媒体轨道负责音视频传输。

完整示例在创建 Offer 前创建客户端事件通道，并注册服务端通道回调。

## 4\. 建立连接

按以下顺序完成建连：

1.  调用 `createOffer` 和 `setLocalDescription`。
2.  按服务端支持的 ICE 方式完成候选信息收集；本示例等待 ICE 收集完成后发送本地 SDP。
3.  将本地 SDP 发送到业务 AppServer，由 AppServer 携带 API Key 请求百炼 SDP 交换接口。
4.  检查 HTTP 状态，成功后以返回的 Answer SDP 调用 `setRemoteDescription`。
5.  等待连接状态成功，并确认用于发送模型事件的 DataChannel 已打开。

SDP 交换成功或 `setRemoteDescription` 完成，只表示完成相应协商步骤，不能直接当作媒体连接已经成功。DataChannel 未处于 `open` 状态时也不能发送模型事件。

### 建连代码及状态回调

监听 `connectionstatechange` 判断连接状态，监听 `icegatheringstatechange` 等待完整的本地 SDP。模型初始化还需要 DataChannel 的 `open` 和模型的就绪事件，不能仅依靠 SDP 交换完成判断。

完整示例通过 `startSession()` 完成 SDP 交换，并通过连接状态回调处理连接结果。

业务 AppServer 应按第 1 节的地址和请求头转发 Offer；示例接口约定返回纯 SDP 文本。不要将含有 HTTP 响应头、日志或 JSON 包装的内容直接传给 `setRemoteDescription`。

## 5\. 按模型协议交互并收发媒体

### 初始化模型

连接及事件通道可用后，按目标模型协议处理初始化。应用需要保存已收到的服务端初始化事件，并结合通道状态推进流程，避免依赖回调到达的固定顺序。

例如，使用 `session.update` 配置会话的模型，应按其协议构造事件，等待配置确认后再发送输入。音色、输出模态、VAD、采样率等参数都应来自当前模型文档。

`session.created` 表示会话创建，不能统一视为配置已生效。对于要求确认会话配置的模型，应等待 `session.updated`。

本模型事件定义见[客户端事件](raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory/client-events.md)和[服务端事件](raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory/server-events.md)。媒体传输和可用模式按本页说明处理。

Qwen-Omni-Realtime 使用 WebRTC 时，仅支持 VAD 模式，不支持 Manual 模式。音频通过音频轨道传输，不发送 `input_audio_buffer.append`；画面通过视频轨道传输，不发送 `input_image_buffer.append`。

### 模型事件示例

**说明**音视频通过媒体轨道传输，不使用 WebSocket 的媒体发送事件。

以下示例演示 `qwen3.8-omni-flash-realtime` 的 `session.created → session.update → session.updated` 流程。配置字段以本模型事件参考为准。收到 `session.updated` 确认配置完成后，再挂载上行媒体轨道。

代码见[完整示例](#conn-rtc-complete-example)。

对于示例型号 `qwen3.8-omni-flash-realtime`，启用音频输出时可通过 `response.audio.done` 了解模型的音频生成状态；该事件不表示客户端的音频已播放完毕。

### 开始媒体收发

满足模型就绪条件后，挂载需要上行的音频、视频轨道。通过远端轨道回调处理模型输出，并持续解析 DataChannel 返回的事件。

-   音频通过 RTP 媒体轨道传输，无需发送 `input_audio_buffer.append`。
    
-   画面通过视频轨道传输；当前 WebRTC 接入不支持 `input_image_buffer.append`。
    
-   文本、状态、控制和错误通过 DataChannel 处理。
    

完整示例通过 `startSendingMedia()` 挂载上行轨道，通过 `ontrack` 处理接收到的媒体。

## 6\. 结束交互并释放资源

不再使用连接时，由客户端业务层停止应用持有的本地采集轨道，关闭 DataChannel 和 `RTCPeerConnection`，释放播放器等资源并清理业务状态。

连接失败或异常断开时，撤销模型就绪状态。重新建立连接后按目标模型协议初始化，避免沿用上一条连接的会话状态。

完整示例中的 `endSession()` 负责释放连接和媒体资源。

在用户点击结束按钮或页面退出时调用 `endSession()`。如果业务额外启用了最佳实践中的 Canvas 降帧或录制，还需取消动画循环、停止 Canvas 媒体轨道及 `MediaRecorder`。

## Data 通道发送和接收事件

客户端通过 WebRTC DataChannel 发送和接收模型事件。发送前确认通道处于 `open` 状态，使用 `send` 发送序列化后的模型事件；接收时在对应通道的 `message` 回调中解析消息，并处理服务端创建的事件通道。

发送事件的名称、字段、参数和调用时机遵循目标模型的**客户端事件定义**；收到消息后的解析方式、状态变更、结果和错误处理遵循该模型的**服务端事件定义**。初始化事件根据模型要求按需发送，后续文本和控制事件按照业务需要发送。

### Data 通道代码示例

同一个绑定函数处理客户端创建和服务端创建的通道；它只负责收发与 JSON 解析，模型语义交给第 5 节的 `handleModelEvent`。`sendModelEvent` 可用于发送模型定义的初始化、文本或控制事件，但应在对应模型允许的时机调用。

完整示例中的 `sendModelEvent()` 和 `bindDataChannel()` 负责发送和接收事件。

完整示例中，开始按钮调用 `startSession()`，结束按钮调用 `endSession()`。这两个函数为本文示例函数，不是 WebRTC 内置 API。

### Qwen-Omni-Realtime 事件定义

模型/应用

客户端事件定义（发送）

服务端事件定义（接收）

Qwen-Omni-Realtime

[客户端事件](raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory/client-events.md)

[服务端事件](raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory/server-events.md)

模型事件的发送与接收还应遵循以下规则：

-   使用事件的 `type` 字段识别模型事件，关联标识按本模型事件参考处理。
    
-   模型要求的初始化确认、输入提交、响应取消和任务结束等操作，均在 Data 通道中按对应协议处理；它们属于模型交互语义，与断开传输连接是不同操作。
    
-   音视频数据通过媒体轨道传输。引用模型事件文档时，媒体封装和可用交互模式仍遵循本文的接入方式，不直接套用 WebSocket 的媒体发送方式。
    

## 事件参考

-   [客户端事件](raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory/client-events.md)
-   [服务端事件](raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory/server-events.md)

## 场景教程

-   [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
