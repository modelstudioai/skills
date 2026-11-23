# Qwen-Audio-Live WebRTC 接入

通过控制 WebSocket 交换 SDP，使用 WebRTC 收发 Qwen-Audio-Live 的实时音频。

通过 WebRTC 媒体轨道收发音频。会话初始化和 SDP 协商通过控制 WebSocket 完成，会话期间保持该连接。

## 接入前准备

按 [WebSocket 接入](raw/model-api-reference/realtime-api-directory/qwen-audio-live-api-directory/qwen-audio-live-websocket-access.md) 选择地域和 URL。浏览器连接应用服务端的 WebSocket 代理，由代理携带 API Key 连接百炼，并在两条连接之间转发 JSON 事件。长期 API Key 存在应用服务端。浏览器页面通过 HTTPS 或本机 `localhost` 提供，并获取麦克风权限。

## 建连流程

阶段

操作和检查点

打开控制连接

浏览器连到应用服务端代理。代理携带 API Key 连接百炼。

提交 Offer SDP

浏览器收集 ICE 候选，通过控制 WebSocket 发送 `session.update`。

应用 Answer SDP

从 `session.updated` 的 `session.transport.sdp` 读取 Answer，再设置远端描述。

收发音频

媒体连接就绪后挂载麦克风轨道。收到远端音轨后检查播放器能否播放语音。

### 生成并提交 Offer SDP

即使只收发语音，Offer SDP 也必须包含 `m=video` 和 `m=application` 两个媒体段。添加视频收发器和创建 DataChannel 分别生成这两个媒体段。纯语音接入无需采集摄像头或发送视频。

1.  创建 `RTCPeerConnection`，添加 `sendrecv` 音频收发器和视频收发器，再创建 DataChannel。示例将视频收发器设为 `recvonly`，DataChannel 名称为 `oai-events`。
2.  调用 `createOffer()` 和 `setLocalDescription()`。等 `iceGatheringState` 变为 `complete` 后，从 `localDescription.sdp` 读取包含 ICE 候选的完整 Offer。
3.  通过控制 WebSocket 发送 [session.update](https://help.aliyun.com/zh/model-studio/qwen-audio-live-client-events#live-session-update)。将 `session.transport.type` 设为 `rtc`，将 Offer SDP 写入 `session.transport.sdp`。

示例用 `iceServers: []` 收集本机候选地址。如果部署环境需要 STUN 或 TURN，在 `iceServers` 中填入相应的服务器配置。

### 读取 Answer SDP 并收发音频

服务端通过控制 WebSocket 返回 [session.updated](https://help.aliyun.com/zh/model-studio/qwen-audio-live-server-events#live-session-updated) 后，从 `session.transport.sdp` 读取 Answer SDP。调用 `setRemoteDescription({ type: "answer", sdp })` 应用 Answer。等媒体连接建立后，挂载麦克风轨道，并将收到的远端音轨交给播放器。

媒体连接就绪后，可从控制 WebSocket 或 WebRTC DataChannel 接收服务端事件。如果两路收到相同 `event_id` 的事件，只处理一次。例如，输入转写 `session.input_transcript.delta` 和输出字幕 `session.output_transcript.delta` 可能同时从两路到达。

## 运行浏览器示例

示例使用 Responses 模式。准备 Node.js 20 或以上版本，在一个空目录下执行 `npm install ws`，并将百炼 API Key 配置到 `DASHSCOPE_API_KEY`。将 [WebSocket 接入](raw/model-api-reference/realtime-api-directory/qwen-audio-live-api-directory/qwen-audio-live-websocket-access.md) 中填写业务空间 ID 后的请求地址复制到下面的 `UPSTREAM_URL`。

### 创建应用服务端

将代码保存为 `server.mjs`。服务端提供本地页面，并为每次浏览器连接建立一条百炼控制 WebSocket。示例只监听本机。

示例代理在上游 WebSocket 握手时额外发送 `X-Session-Id`，值以 `sess_` 开头，后接 32 个随机十六进制字符。

```
import { createServer } from "node:http";
import { randomBytes } from "node:crypto";
import { readFile } from "node:fs/promises";
import WebSocket, { WebSocketServer } from "ws";

const UPSTREAM_URL = "粘贴填写业务空间 ID 后的 WebSocket 请求地址";
const apiKey = process.env.DASHSCOPE_API_KEY;
const localOrigin = "http://localhost:8000";
if (!apiKey) throw new Error("请设置 DASHSCOPE_API_KEY");

const files = {
  "/": ["index.html", "text/html; charset=utf-8"],
  "/live.js": ["live.js", "text/javascript; charset=utf-8"],
};
const server = createServer(async (request, response) => {
  const file = Object.hasOwn(files, request.url) && files[request.url];
  if (request.method !== "GET" || !file) return response.writeHead(404).end();
  try {
    const content = await readFile(new URL(file[0], import.meta.url));
    response.writeHead(200, { "Content-Type": file[1] }).end(content);
  } catch {
    response.writeHead(500).end("请检查示例文件是否齐全");
  }
});

const proxy = new WebSocketServer({ noServer: true });
server.on("upgrade", (request, socket, head) => {
  if (request.url !== "/control" || request.headers.origin !== localOrigin) {
    socket.destroy();
    return;
  }
  proxy.handleUpgrade(request, socket, head, browser => proxy.emit("connection", browser));
});

proxy.on("connection", browser => {
  let upstream;
  try {
    upstream = new WebSocket(UPSTREAM_URL, {
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "X-Session-Id": `sess_${randomBytes(16).toString("hex")}`,
      },
      handshakeTimeout: 10000,
    });
  } catch {
    browser.close(1011, "Invalid upstream URL");
    return;
  }

  let closing = false;
  function closeBoth() {
    if (closing) return;
    closing = true;
    upstream.terminate();
    if (browser.readyState === WebSocket.OPEN) browser.close();
  }

  browser.on("close", closeBoth);
  browser.on("error", closeBoth);
  upstream.on("error", () => {
    if (!closing && browser.readyState === WebSocket.OPEN) {
      browser.close(1011, "上游连接失败");
    }
    closeBoth();
  });
  upstream.on("close", closeBoth);
  browser.on("message", data => {
    if (upstream.readyState === WebSocket.OPEN) upstream.send(data.toString());
  });
  upstream.on("message", data => {
    if (browser.readyState === WebSocket.OPEN) browser.send(data.toString());
  });
  upstream.on("open", () => {
    if (browser.readyState === WebSocket.OPEN) {
      browser.send(JSON.stringify({ type: "proxy.ready" }));
    }
  });
});

server.listen(8000, "127.0.0.1", () => console.log(localOrigin));
```

### 创建浏览器页面

将以下 HTML 保存为 `index.html`。然后将下面的 JavaScript 保存为同一目录下的 `live.js`。

```
<!doctype html>
<html lang="zh-CN">
<meta charset="utf-8">
<title>Qwen-Audio-Live WebRTC 示例</title>
<button id="start">开始</button>
<button id="end" disabled>结束</button>
<audio id="reply" controls></audio>
<p id="status" role="status"></p>
<p>用户：<span id="user-text"></span></p>
<p>模型：<span id="model-text"></span></p>
<script src="/live.js" defer></script>
</html>
```

浏览器等待本地代理发来 `proxy.ready`，再开始 SDP 协商。应用通过 `onTranscript` 接收字幕，按 `type` 区分用户和模型。

```
async function startWebRTC(control, audio, onTranscript, onConnected, onError) {
  if (control.readyState !== WebSocket.OPEN) throw new Error("控制连接尚未打开");

  let track;
  let pc;
  let sender;
  const channels = [];
  const seenTranscripts = new Set();
  let answered = false;
  let startingAudio = false;
  let stopped = false;
  let closing = false;
  let connectionTimer;
  let closeTimer;

  function finish() {
    if (stopped) return;
    stopped = true;
    clearTimeout(connectionTimer);
    clearTimeout(closeTimer);
    track?.stop();
    pc?.close();
    control.close();
    audio.srcObject = null;
    seenTranscripts.clear();
  }

  function fail(error) {
    if (stopped) return;
    finish();
    onError(error);
  }

  const openChannel = () => channels.find(channel => channel.readyState === "open");

  async function startAudio() {
    if (stopped || closing || startingAudio || !pc.remoteDescription ||
        pc.connectionState !== "connected" || !openChannel()) return;
    startingAudio = true;
    try {
      await sender.replaceTrack(track);
      clearTimeout(connectionTimer);
      if (!stopped && !closing) {
        track.enabled = true;
        onConnected();
      }
    } catch (error) {
      fail(error);
    }
  }

  async function receive(raw, fromWebSocket) {
    if (stopped) return;
    try {
      const message = JSON.parse(raw);
      if (message.type === "session.updated" && fromWebSocket && !answered) {
        const transport = message.session?.transport;
        if (transport?.type !== "rtc" || typeof transport.sdp !== "string" || !transport.sdp.trim()) {
          throw new Error("session.updated 未返回有效的 Answer SDP");
        }
        answered = true;
        const sdp = transport.sdp.trim().replace(/\r?\n/g, "\r\n") + "\r\n";
        await pc.setRemoteDescription({ type: "answer", sdp });
        await startAudio();
      } else if (message.type === "session.input_transcript.delta" ||
                 message.type === "session.output_transcript.delta") {
        const id = message.event_id;
        if (id && seenTranscripts.has(id)) return;
        if (id) seenTranscripts.add(id);
        onTranscript(message);
      } else if (message.type === "session.closed" && fromWebSocket) {
        finish();
      } else if (message.type === "error") {
        throw new Error(message.error?.message || "会话失败");
      }
    } catch (error) {
      if (!stopped) fail(error);
    }
  }

  function bindChannel(channel) {
    channel.addEventListener("open", startAudio);
    channel.addEventListener("message", ({ data }) => receive(data, false));
  }

  try {
    const microphone = await navigator.mediaDevices.getUserMedia({ audio: true });
    track = microphone.getAudioTracks()[0];
    if (control.readyState !== WebSocket.OPEN) throw new Error("控制连接已关闭");
    track.enabled = false;

    pc = new RTCPeerConnection({ iceServers: [] });
    sender = pc.addTransceiver("audio", { direction: "sendrecv" }).sender;
    pc.addTransceiver("video", { direction: "recvonly" });
    channels.push(pc.createDataChannel("oai-events"));
    bindChannel(channels[0]);
    pc.addEventListener("datachannel", ({ channel }) => {
      channels.push(channel);
      bindChannel(channel);
    });
    pc.addEventListener("track", ({ track: remoteTrack }) => {
      if (stopped || remoteTrack.kind !== "audio") return;
      audio.srcObject = new MediaStream([remoteTrack]);
      audio.play().catch(() => { audio.controls = true; });
    });
    pc.addEventListener("connectionstatechange", () => {
      if (pc.connectionState === "failed") fail(new Error("WebRTC 连接失败"));
      else void startAudio();
    });
    control.addEventListener("message", ({ data }) => receive(data, true));
    control.addEventListener("close", () => fail(new Error("控制连接关闭")));

    await pc.setLocalDescription(await pc.createOffer());
    await new Promise((resolve, reject) => {
      if (pc.iceGatheringState === "complete") return resolve();
      const timer = setTimeout(() => {
        pc.removeEventListener("icegatheringstatechange", check);
        reject(new Error("ICE 候选收集超时"));
      }, 15000);
      function check() {
        if (pc.iceGatheringState !== "complete") return;
        clearTimeout(timer);
        pc.removeEventListener("icegatheringstatechange", check);
        resolve();
      }
      pc.addEventListener("icegatheringstatechange", check);
    });

    const sdp = pc.localDescription.sdp;
    if (!/^a=candidate:/m.test(sdp)) throw new Error("Offer 缺少 ICE 候选");
    if (stopped || control.readyState !== WebSocket.OPEN) throw new Error("控制连接已关闭");
    connectionTimer = setTimeout(() => fail(new Error("WebRTC 建连超时")), 200000);
    control.send(JSON.stringify({
      type: "session.update",
      event_id: crypto.randomUUID(),
      session: {
        model: "qwen-audio-4.0-realtime-preview",
        modalities: ["text", "audio"],
        delegation: { type: "responses", responses: { model: "qwen3.8-flash" } },
        transport: { type: "rtc", sdp }
      }
    }));
  } catch (error) {
    finish();
    throw error;
  }

  return function closeSession() {
    if (stopped || closing) return;
    closing = true;
    clearTimeout(connectionTimer);
    track.enabled = false;
    try {
      control.send(JSON.stringify({ type: "session.close", event_id: crypto.randomUUID() }));
      closeTimer = setTimeout(finish, 8000);
    } catch (error) {
      fail(error);
    }
  };
}
const startButton = document.querySelector("#start");
const endButton = document.querySelector("#end");
const audio = document.querySelector("#reply");
const statusElement = document.querySelector("#status");

startButton.onclick = () => {
  startButton.disabled = true;
  statusElement.textContent = "正在连接。";
  const control = new WebSocket("ws://localhost:8000/control");
  const showError = error => { statusElement.textContent = `出错：${error.message}`; };

  control.addEventListener("error", () => showError(new Error("无法连接本地代理")));
  control.addEventListener("close", event => {
    endButton.disabled = true;
    if (event.reason) showError(new Error(event.reason));
    if (!statusElement.textContent.startsWith("出错")) statusElement.textContent = "连接已关闭。";
  });
  control.addEventListener("message", async function waitForProxy({ data }) {
    if (JSON.parse(data).type !== "proxy.ready") return;
    control.removeEventListener("message", waitForProxy);
    try {
      const closeSession = await startWebRTC(control, audio, event => {
        const selector = event.type === "session.input_transcript.delta" ? "#user-text" : "#model-text";
        document.querySelector(selector).textContent += event.delta;
      }, () => { statusElement.textContent = "媒体连接已建立，可以说话。"; }, showError);
      endButton.disabled = false;
      endButton.onclick = closeSession;
    } catch (error) {
      showError(error);
    }
  });
};
```

## 验证连接

运行 `node server.mjs`，打开 `http://localhost:8000`，点击**开始**并允许使用麦克风。页面显示「媒体连接已建立，可以说话」后说一句话，确认播放器能播出模型的语音回复。结束后刷新页面可以发起新会话。若有字幕但没有声音，检查 `track` 回调是否收到远端音轨，然后检查浏览器是否阻止自动播放。若未收到 Answer，先确认 Offer 包含 `m=video` 和 `m=application`，再检查服务端错误。若已收到 Answer 但媒体连接未建立，检查是否已应用 Answer，以及 Offer 是否含有当前网络可用的 ICE 候选。

## 处理任务和结束会话

业务接入见[任务委派与工具](https://help.aliyun.com/zh/model-studio/qwen-audio-live-delegation)。请求和返回字段见[客户端事件](raw/model-api-reference/realtime-api-directory/qwen-audio-live-api-directory/qwen-audio-live-client-events.md)与[服务端事件](raw/model-api-reference/realtime-api-directory/qwen-audio-live-api-directory/qwen-audio-live-server-events.md)。

点击**结束**，示例调用 `closeSession()` 发送 `session.close`。收到 `session.closed` 后停止音频采集并关闭连接。
