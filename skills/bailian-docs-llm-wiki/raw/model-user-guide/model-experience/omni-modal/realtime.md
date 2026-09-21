# Qwen-Omni-Realtime

Qwen-Omni-Realtime 是千问推出的实时音视频聊天模型。能同时理解流式的音频与图像输入（例如从视频流中实时抽取的连续图像帧），并实时输出高质量的文本与音频。

**支持的地域：**北京、新加坡，需使用各地域的[API Key](raw/model-api-reference/preparations/get-api-key.md)。

**在线体验：**请参见[如何在线体验 Qwen-Omni-Realtime 模型？](https://help.aliyun.com/zh/model-studio/realtime#14a119f447ehf)

## 如何使用

### 1\. 建立连接

通用 WebSocket 和 WebRTC 建连示例使用 `qwen3.8-omni-flash-realtime`；型号专属配置示例使用各自标注的模型。

Qwen-Omni-Realtime 模型支持 WebSocket、WebRTC 和 AOQ 三种协议接入。WebSocket 适合服务端集成和快速接入；WebRTC 适合浏览器端、低延迟语音场景，音频通过 UDP 直接传输，内置回声消除和降噪。如果是客户端对接，且更看重稳定的延迟、弱网下的交互能力、实时双工的降噪与回声消除，可优先考虑 AOQ。协议对比与选型请参见[Realtime API 概述](https://help.aliyun.com/zh/model-studio/realtime-api-overview#rtov-s02h2)。

#### WebSocket

**说明**`qwen3.8-omni-flash-realtime` 必须使用下方绑定业务空间的调用地址。调用前请获取对应地域、对应业务空间的 [API Key](raw/model-api-reference/preparations/get-api-key.md) 和[业务空间 ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。

#### WebSocket 原生连接

连接时需要以下配置项：

**配置项**

**说明**

调用地址

华北2（北京）地域：`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`

新加坡地域：`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

查询参数

查询参数为model，需指定为访问的模型名。示例：`?model=qwen3.8-omni-flash-realtime`

请求头

使用 Bearer Token 鉴权：Authorization: Bearer DASHSCOPE\_API\_KEY

> DASHSCOPE\_API\_KEY 是您在百炼上申请的[API Key](raw/model-api-reference/preparations/get-api-key.md)。

```
# pip install websocket-client
import json
import websocket
import os

API_KEY=os.getenv("DASHSCOPE_API_KEY")
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
API_URL = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime?model=qwen3.8-omni-flash-realtime"

headers = [
    "Authorization: Bearer " + API_KEY
]

def on_open(ws):
    print(f"Connected to server: {API_URL}")
def on_message(ws, message):
    data = json.loads(message)
    print("Received event:", json.dumps(data, indent=2))
def on_error(ws, error):
    print("Error:", error)

ws = websocket.WebSocketApp(
    API_URL,
    header=headers,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error
)

ws.run_forever()
```

#### DashScope Python SDK

```
# SDK 版本不低于1.26.5
import os
import json
from dashscope.audio.qwen_omni import OmniRealtimeConversation,OmniRealtimeCallback
import dashscope
# 若没有配置 API Key，请将下行改为 dashscope.api_key = "sk-xxx"
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

class PrintCallback(OmniRealtimeCallback):
    def on_open(self) -> None:
        print("Connected Successfully")
    def on_event(self, response: dict) -> None:
        print("Received event:")
        print(json.dumps(response, indent=2, ensure_ascii=False))
    def on_close(self, close_status_code: int, close_msg: str) -> None:
        print(f"Connection closed (code={close_status_code}, msg={close_msg}).")

callback = PrintCallback()
conversation = OmniRealtimeConversation(
    model="qwen3.8-omni-flash-realtime",
    callback=callback,
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    url="wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime"
)
try:
    conversation.connect()
    print("Conversation started. Press Ctrl+C to exit.")
    conversation.thread.join()
except KeyboardInterrupt:
    conversation.close()
```

#### DashScope Java SDK

```
// SDK 版本不低于 2.22.15
import com.alibaba.dashscope.audio.omni.*;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.google.gson.JsonObject;
import java.util.concurrent.CountDownLatch;

public class Main {
    public static void main(String[] args) throws InterruptedException, NoApiKeyException {
        CountDownLatch latch = new CountDownLatch(1);
        OmniRealtimeParam param = OmniRealtimeParam.builder()
                .model("qwen3.8-omni-flash-realtime")
                .apikey(System.getenv("DASHSCOPE_API_KEY"))
                // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
                .url("wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime")
                .build();

        OmniRealtimeConversation conversation = new OmniRealtimeConversation(param, new OmniRealtimeCallback() {
            @Override
            public void onOpen() {
                System.out.println("Connected Successfully");
            }
            @Override
            public void onEvent(JsonObject message) {
                System.out.println(message);
            }
            @Override
            public void onClose(int code, String reason) {
                System.out.println("connection closed code: " + code + ", reason: " + reason);
                latch.countDown();
            }
        });
        conversation.connect();
        latch.await();
        conversation.close(1000, "bye");
        System.exit(0);
    }
}
```

#### WebRTC

WebRTC 建立连接分为两个阶段：

1.  **SDP 交换（HTTP）**：客户端先将自身的媒体能力和网络地址（Offer SDP）通过 HTTP POST 发送给服务端，服务端返回自身信息（Answer SDP），双方完成能力协商。
2.  **建连（自动）**：协商完成后，WebRTC 底层自动建立音频传输通道。

SDP 交换的配置项：

**配置项**

**说明**

请求地址

华北2（北京）地域：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/webrtc/realtime`

新加坡地域：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/webrtc/realtime`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

查询参数

查询参数为model，需指定为访问的模型名。示例：`?model=qwen3.5-omni-plus-realtime`

Content-Type

application/sdp

请求头

Authorization: Bearer DASHSCOPE\_API\_KEY

请求体

客户端生成的 Offer SDP 字符串

响应

成功：HTTP 200，返回服务端 Answer SDP 字符串。失败：HTTP 4xx，返回 JSON 错误信息。

**配置项**

**说明**

请求地址

华北2（北京）地域：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/webrtc/realtime`

新加坡地域：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/webrtc/realtime`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。

查询参数

查询参数为model，需指定为访问的模型名。示例：`?model=qwen3.8-omni-flash-realtime`

Content-Type

application/sdp

请求头

Authorization: Bearer DASHSCOPE\_API\_KEY

请求体

客户端生成的 Offer SDP 字符串

响应

成功：HTTP 200，返回服务端 Answer SDP 字符串。失败：HTTP 4xx，返回 JSON 错误信息。

建连示例代码：

python

```
# pip install aiortc aiohttp certifi
import asyncio, aiohttp, ssl, certifi
from aiortc import RTCPeerConnection, RTCConfiguration, RTCSessionDescription
from aiortc.mediastreams import AudioStreamTrack

API_KEY = "your-api-key"
MODEL = "qwen3.8-omni-flash-realtime"
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
SIGNALING_URL = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/webrtc/realtime?model=" + MODEL

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

javascript

```
const API_KEY = 'your-api-key';
// 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
const API_URL = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/webrtc/realtime?model=qwen3.8-omni-flash-realtime';

async function connect() {
  const pc = new RTCPeerConnection({ iceServers: [] });

  // 添加音频轨道，确保 Offer SDP 包含 m=audio（服务端必需）
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  stream.getAudioTracks().forEach(t => pc.addTrack(t, stream));

  // 创建 DataChannel 以触发 SDP 协商（名称可自定义，服务端会通过名为 "txt" 的通道推送事件）
  pc.createDataChannel('oai-events');

  // 等待 ICE 收集完成后发送 Offer 获取 Answer
  pc.onicegatheringstatechange = async () => {
    if (pc.iceGatheringState !== 'complete') return;
    const resp = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/sdp',
        'Authorization': `Bearer ${API_KEY}`,
      },
      body: pc.localDescription.sdp,
    });
    if (!resp.ok) throw new Error('SDP 交换失败: ' + resp.status);
    const answerSdp = await resp.text();
    // ICE 建连自动完成
    await pc.setRemoteDescription({ type: 'answer', sdp: answerSdp });
    console.log('WebRTC 连接已建立');
  };

  // 创建 Offer
  const offer = await pc.createOffer();
  await pc.setLocalDescription(offer);
  return pc;
}
```

#### AOQ

AOQ 通过业务 AppServer 发起 HTTP 请求获取连接参数，再由客户端 SDK 建立媒体连接。鉴权步骤见[Token 鉴权](https://help.aliyun.com/zh/model-studio/realtime-token-authentication#tkauth-aoq-title)。使用 `qwen3.8-omni-flash-realtime` 的完整示例见[实时通话](raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)或[按键语音对话](raw/model-user-guide/use-cases/realtime-audio-video-integration/use-aoq-to-access-qwen3-5-omni-plus-realtime-to-realize-key-voice-dialogue.md)。

### 2\. 配置会话

发送客户端事件[session.update](https://help.aliyun.com/zh/model-studio/client-events#26a8302028sjm)：

#### Qwen3.8-Omni-Flash-Realtime

Qwen3.8-Omni-Flash-Realtime 的会话配置见[调用示例](#qwen38-realtime)。

-   **多通道音频（WebSocket 接入）**：在首段音频前设置 `session.audio.input.format`。支持 1、2、4 声道；多通道必须为 PCM、16000 Hz、s16le、interleaved。2 声道使用 `raw_mic_array`，4 声道使用 `foa_ambix`。字段约束和 JSON 片段见[客户端事件](https://help.aliyun.com/zh/model-studio/client-events#qwen38-client)。
-   **视频聚合**：`session.video.input.representation_compact` 默认为 `none`；设为 `normal` 可聚合视频表征，降低计算开销，适用于不依赖细粒度视觉信息的场景。也必须在首段音频前配置，开始输入后不得修改。
-   **音色**：默认音色为 `Tina`。新接入使用 `session.audio.output.voice`，它优先于兼容字段 `session.voice`。支持 `longanlingxin`（龙安灵心，知心温暖音）等音色。使用方式和声音复刻入口见[音色列表](https://help.aliyun.com/zh/model-studio/omni-voice-list#qwen38-voices)。
-   **MCP**：在 `session.tools` 中配置公网 HTTPS MCP Streamable HTTP 服务；默认需要审批。先确认工具发现完成，再发起需要该工具的 Response。执行结果、拒绝和失败处理以及续答步骤见[MCP 交互流程](https://help.aliyun.com/zh/model-studio/omni-realtime-interaction-process#qwen38-mcp-flow)。

##### SDK 配置视频聚合

Qwen3.8-Omni-Flash-Realtime 使用 DashScope Python SDK 1.26.5 及以上版本，或 Java SDK 2.22.15 及以上版本。视频聚合参数通过 SDK 透传：Python 在 `update_session` 中传入 `video`，Java 通过 `OmniRealtimeConfig.builder().parameters(...)` 传入。

以下示例配置一个 Manual 模式会话：文本与音频输出、`Tina` 音色、关闭输入转写，并启用视频聚合。先按下方 SDK 示例建立连接，将模型设为 `qwen3.8-omni-flash-realtime`，用本例替换该示例的会话配置调用，在首段音频输入前调用一次。`conversation` 为已连接的 SDK 会话。SDK 会同时发送音色、VAD 等配置；如需其他音色、VAD 或转写设置，在同一次调用中完整设置。Java 需导入 `java.util.Arrays`、`java.util.Map`、`java.util.HashMap`、`com.alibaba.dashscope.audio.omni.OmniRealtimeConfig` 和 `com.alibaba.dashscope.audio.omni.OmniRealtimeModality`。

Python

```
from dashscope.audio.qwen_omni import MultiModality

conversation.update_session(
    output_modalities=[MultiModality.AUDIO, MultiModality.TEXT],
    voice="Tina",
    enable_turn_detection=False,
    enable_input_audio_transcription=False,
    video={
        "input": {
            "representation_compact": "normal",
        },
    },
)
```

Java

```
Map<String, Object> videoInput = new HashMap<>();
videoInput.put("representation_compact", "normal");

Map<String, Object> video = new HashMap<>();
video.put("input", videoInput);

Map<String, Object> parameters = new HashMap<>();
parameters.put("video", video);

OmniRealtimeConfig config =
    OmniRealtimeConfig.builder()
        .modalities(Arrays.asList(OmniRealtimeModality.AUDIO, OmniRealtimeModality.TEXT))
        .voice("Tina")
        .enableTurnDetection(false)
        .enableInputAudioTranscription(false)
        .parameters(parameters)
        .build();
conversation.updateSession(config);
```

#### Qwen3.5-Omni-Realtime

以下示例使用 Qwen3.5-Omni-Realtime 的 Ethan 音色和 `semantic_vad` 配置。

```
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
        // 推荐写法：同时配置音频格式和采样率（仅 qwen3.5-omni-plus-realtime / qwen3.5-omni-flash-realtime 支持）
        // 输入格式：pcm / wav，默认 pcm；采样率：8000/16000/24000/48000，默认 16000
        // 输出格式：pcm / wav，默认 pcm；采样率：8000/16000/24000/48000，默认 24000
        "audio": {
            "input": {
                "format": {
                    "type": "pcm",
                    "sample_rate": 16000
                }
            },
            "output": {
                "format": {
                    "type": "pcm",
                    "sample_rate": 24000
                }
            }
        },
        // 系统消息，用于设定模型的目标或角色。
        "instructions": "你是某五星级酒店的AI客服专员，请准确且友好地解答客户关于房型、设施、价格、预订政策的咨询。请始终以专业和乐于助人的态度回应，杜绝提供未经证实或超出酒店服务范围的信息。",
        // 是否开启语音活动检测。若需启用，需传入一个配置对象，服务端将据此自动检测语音起止。
        // 设置为null表示由客户端决定何时发起模型响应。
        "turn_detection": {
            // VAD类型，取值为server_vad或semantic_vad。使用qwen3.5-omni-realtime系列模型时推荐设为semantic_vad。
            "type": "semantic_vad",
            // VAD检测阈值。建议在嘈杂的环境中增加，在安静的环境中降低。
            "threshold": 0.5,
            // 检测语音停止的静音持续时间，超过此值后会触发模型响应。取值范围 200-6000，默认 800。金融核实等短回答场景建议 500-600。
            "silence_duration_ms": 800
        }
    }
}
```

> 本段列举的音频格式与采样率选项适用于 `qwen3.5-omni-plus-realtime` 和 `qwen3.5-omni-flash-realtime` 模型，历史兼容字段 `input_audio_format` / `output_audio_format` 仍有效，建议采用 `audio.input.format` / `audio.output.format` 字段。Qwen3.8-Omni-Flash-Realtime 的输入格式约束见[客户端事件](https://help.aliyun.com/zh/model-studio/client-events#qwen38-client)，接入示例见[本页 3.8 章节](#qwen38-realtime)。

每通会话结束后，发送 `session.finish` 事件关闭会话，或直接断开 WebSocket 连接。同一会话不关闭会导致上下文持续累积。

### 3\. 输入音频与图片

音频输入是推荐的主要输入方式；图片输入可选。模型也支持纯文本输入：通过 `conversation.item.create` 发送 `input_text` 类型内容，无需音频，适用于非实时对话场景。模型目录标注的“支持文本输入”包括用户纯文本对话、system instructions 和 `function_call_output`。输入方式取决于接入协议。

#### WebSocket

客户端通过[input\_audio\_buffer.append](https://help.aliyun.com/zh/model-studio/client-events#2ea4b5e41fhjd)和 [input\_image\_buffer.append](https://help.aliyun.com/zh/model-studio/client-events#c28ed38410nfw) 事件发送 Base64 编码的音频和图片数据到服务端缓冲区。

> 图片可以来自本地文件，或从视频流中实时采集。

> 启用服务端VAD时，服务端会在检测到语音结束时自动提交数据并触发响应。禁用VAD时（手动模式），客户端必须在发送完数据后，主动调用[input\_audio\_buffer.commit](https://help.aliyun.com/zh/model-studio/client-events#1cbea5fa7fkfl)事件来提交。

#### WebRTC

建连时添加的音频轨道和视频轨道（即 RTP 媒体通道）会自动将数据传输到服务端。

-   **音频**：通过音频轨道（RTP）直接传输，无需发送 `input_audio_buffer.append` 事件。
-   **图片**：通过视频轨道（RTP）发送画面帧，不支持 `input_image_buffer.append` 事件。

> WebRTC 仅支持服务端 VAD 模式（`server_vad` 或 `semantic_vad`），不支持手动模式。

### 4\. 接收模型响应

模型的响应格式取决于配置的输出模态。

#### WebSocket

-   **仅输出文本**
    
    通过[response.text.delta](https://help.aliyun.com/zh/model-studio/server-events#0c54be63e0c3w)事件接收流式文本，[response.text.done](https://help.aliyun.com/zh/model-studio/server-events#d675635a94jfb)事件获取完整文本。
    
-   **输出文本+音频**
    -   **文本**：通过[response.audio\_transcript.delta](https://help.aliyun.com/zh/model-studio/server-events#35396453cfood)事件接收流式文本，[response.audio\_transcript.done](https://help.aliyun.com/zh/model-studio/server-events#f4d1698567bsm)事件获取完整文本。
    -   **音频**：通过[response.audio.delta](https://help.aliyun.com/zh/model-studio/server-events#a25cc50a15car)事件获取 Base64 编码的流式输出音频数据。[response.audio.done](https://help.aliyun.com/zh/model-studio/server-events#9e8eb59c67qnt)事件标志音频数据生成完成。

#### WebRTC

-   **仅输出文本**
    
    通过 DataChannel 接收 `response.text.delta` 和 `response.text.done` 等流式文本事件。
    
-   **输出文本+音频**
    -   **文本**：通过 DataChannel 接收 `response.text.delta` 和 `response.text.done` 等流式文本事件。
    -   **音频**：通过 RTP 轨道实时接收和播放，无需通过 `response.audio.delta` 事件获取音频数据。

## 模型选型

### Qwen3.8-Omni-Flash-Realtime

实时音视频对话优先使用 **Qwen3.8-Omni-Flash-Realtime**，接收流式音视频输入，返回文本与音频，支持自定义 Function Calling、MCP、多通道音频和声音复刻。接入方式见[建立连接](#bdaa43cdd7hsd)。

支持 [113 种语种和方言](https://help.aliyun.com/zh/model-studio/qwen-omni#d54e85c641oux)的语音识别，以及 [36 种语种和方言](https://help.aliyun.com/zh/model-studio/qwen-omni#d54e85c641oux)的语音生成；音色及试听见[音色列表](https://help.aliyun.com/zh/model-studio/omni-voice-list#qwen38-voices)。

### Qwen3.5-Omni-Realtime

Qwen3.5-Omni-Realtime 系列模型是千问的实时多模态模型，相比于上一代的 Qwen3-Omni-Flash-Realtime：

-   **智能水平**
    
    模型智力大幅提升，与 Qwen3.5-Plus 智能水平相当。
    
-   **联网搜索**
    
    原生支持联网搜索（WebSearch），模型可自主判断是否需要搜索来回应即时问题。详见[联网搜索](https://help.aliyun.com/zh/model-studio/realtime#f6g7h8i9j0s7k)。
    
-   **工具调用**
    
    支持 Function Calling，模型可自主判断是否需要调用外部工具，实现与外部系统的交互。详见[Qwen-Omni-Realtime 系列](https://help.aliyun.com/zh/model-studio/qwen-function-calling#rt02realtime01)。
    
-   **语义打断**
    
    自动识别对话意图，避免附和声和无意义背景音触发打断。
    
-   **语音控制**
    
    通过语音指令控制声音大小、语速和情绪，如“语速快一些”、“声音大一些”、“用开心的语气”等。
    
-   **支持的语言**
    
    支持 [113 种语种和方言](raw/model-user-guide/model-experience/omni-modal/qwen-omni.md)的语音识别，以及 [36 种语种和方言](raw/model-user-guide/model-experience/omni-modal/qwen-omni.md)的语音生成。
    
-   **支持的音色**
    
    支持 55 种音色（47 种多语言 + 8 种方言），具体可查看[音色列表](https://help.aliyun.com/zh/model-studio/realtime#f4c9fd97f221z)。
    
-   **声音复刻**
    
    qwen3.5-omni-plus-realtime 和 qwen3.5-omni-flash-realtime 支持声音复刻功能，可使用自定义音色进行实时对话。详见[声音复刻](raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。
    

> 模型的名称、上下文、价格、快照版本等信息请参见百炼控制台；并发限流条件请参考[限流](raw/model-user-guide/get-started-with-models/rate-limit.md)。

## 使用限制

`qwen3.8-omni-flash-realtime` 的全部输入 Token 总数上限为 196608，输入长度计算规则与 Qwen3.5-Omni-Realtime 一致。

-   联网搜索和工具调用不兼容，不可同时开启。
    
-   单次会话最长可持续 **120 分钟**，达到此上限后服务将主动关闭连接。
    
-   模型会维护对话历史上下文，当对话轮次或累计时长超过以下限制时，将自动丢弃更早的历史信息。**最大时长**指模型上下文中能保留的音频或视频（图像帧）累计时长上限。该时长不是整个会话的持续时间。
    
    > 由于视频以抽帧方式输入（建议 1 帧/秒），视频最大时长即模型能保留的图像帧累计时长。例如 240 秒表示模型最多保留最近 240 秒内收到的帧，超过后更早的帧将被丢弃。
    
    > qwen3-omni-flash-realtime 最大轮次为 8 轮，一般会先触及轮次限制，时长限制为模型的上下文长度限制，不再单独列出。
    
    **模型**
    
    **音频最大轮次**
    
    **视频最大轮次**
    
    **音频最大时长**
    
    **视频最大时长**
    
    qwen3.8-omni-flash-realtime
    
    100轮
    
    50轮
    
    600秒
    
    240秒
    
    qwen3.5-omni-plus-realtime
    
    100轮
    
    50轮
    
    600秒
    
    240秒
    
    qwen3.5-omni-flash-realtime
    
    80轮
    
    50轮
    
    480秒
    
    120秒
    
    qwen3-omni-flash-realtime
    
    8轮
    
    8轮
    
    —
    
    —
    
-   调用 `close()` 关闭 WebSocket 连接时，若连接刚建立即关闭（无会话交互），关闭耗时约 5-10 秒，此为正常现象。服务端需完成音频流处理、上下文缓存及推理资源初始化后才能响应关闭请求。建议异步执行 `close()` 操作，避免阻塞主流程。
    

## 快速开始

您需要[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

请选择您熟悉的编程语言，通过以下步骤快速体验与 Realtime 模型实时对话的功能。

#### WebSocket

### 最小音频问答

先配置 [API Key](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)，安装 `websocket-client`。将 `REALTIME_WS_URL` 设为[建立连接](#bdaa43cdd7hsd)中对应地域的完整 WebSocket 地址并替换业务空间 ID；示例自动添加模型查询参数。将 `PCM_FILE` 设为一段短的 16 kHz、16-bit little-endian、单声道、无文件头 PCM 语音文件路径。

示例使用 Manual 模式：等待会话配置生效后发送音频、提交缓冲区，再请求回复。文本打印到终端，音频写入 `reply.pcm`（24 kHz PCM，非 WAV 文件）。

在 macOS 或 Linux 终端中执行以下命令。将 WebSocket 地址替换为所选地域、业务空间的服务地址，无需手动添加模型查询参数。

```
python3 -m pip install websocket-client
export REALTIME_WS_URL="<workspace-websocket-url>"
export PCM_FILE="./input.pcm"
```

如果已有单声道、16 kHz、16-bit PCM 编码的 `input.wav`，可用 Python 提取 PCM 音频。此步骤检查格式，不进行重采样。

```
import wave
from pathlib import Path

with wave.open("input.wav", "rb") as source:
    if (source.getnchannels(), source.getframerate(), source.getsampwidth(),
            source.getcomptype()) != (1, 16000, 2, "NONE"):
        raise ValueError("Expected mono 16 kHz, 16-bit PCM WAV audio.")
    Path("input.pcm").write_bytes(source.readframes(source.getnframes()))
```

准备好输入后，运行以下客户端：

```
import base64
import json
import os
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
import websocket

parts = urlsplit(os.environ["REALTIME_WS_URL"])
query = dict(parse_qsl(parts.query))
query["model"] = "qwen3.8-omni-flash-realtime"
url = urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), ""))
audio = Path(os.environ["PCM_FILE"]).read_bytes()
if not audio or len(audio) % 2:
    raise ValueError("Provide non-empty 16-bit mono PCM audio.")

ws = websocket.create_connection(
    url,
    header=["Authorization: Bearer " + os.environ["DASHSCOPE_API_KEY"]],
    timeout=30,
)

def receive():
    event = json.loads(ws.recv())
    if event["type"] == "error":
        raise RuntimeError(event.get("error"))
    return event

try:
    while receive()["type"] != "session.created":
        pass
    ws.send(json.dumps({
        "type": "session.update",
        "session": {
            "modalities": ["text", "audio"],
            "turn_detection": None,
            "audio": {
                "input": {"format": {
                    "type": "pcm", "sample_rate": 16000,
                    "sample_format": "s16le", "channels": 1,
                    "packing": "interleaved", "channel_layout": "mono",
                }},
                "output": {
                    "voice": "longanlingxin",
                    "format": {"type": "pcm", "sample_rate": 24000},
                },
            },
        },
    }))
    while receive()["type"] != "session.updated":
        pass
    for offset in range(0, len(audio), 3200):
        ws.send(json.dumps({
            "type": "input_audio_buffer.append",
            "audio": base64.b64encode(audio[offset:offset + 3200]).decode("ascii"),
        }))
    ws.send(json.dumps({"type": "input_audio_buffer.commit"}))
    while receive()["type"] != "input_audio_buffer.committed":
        pass
    ws.send(json.dumps({"type": "response.create"}))
    with open("reply.pcm", "wb") as output:
        while True:
            event = receive()
            if event["type"] == "response.audio.delta":
                output.write(base64.b64decode(event["delta"]))
            elif event["type"] in ("response.audio_transcript.delta", "response.text.delta"):
                print(event["delta"], end="", flush=True)
            elif event["type"] == "response.done":
                print("\nResponse status:", event["response"]["status"])
                break
finally:
    ws.close()
```

成功收到回复后，将 `reply.pcm` 包装为 WAV 文件，再使用音频播放器播放：

```
import wave
from pathlib import Path

with wave.open("reply.wav", "wb") as target:
    target.setnchannels(1)
    target.setsampwidth(2)
    target.setframerate(24000)
    target.writeframes(Path("reply.pcm").read_bytes())
```

### SDK 实时录音示例

#### DashScope Python SDK

-   **准备运行环境**

您的 Python 版本需要不低于 3.10。

首先根据您的操作系统安装 pyaudio。

#### macOS

```
brew install portaudio && pip install pyaudio
```

#### Debian/Ubuntu

-   **若未使用虚拟环境**，可直接通过系统包管理器安装：

```
sudo apt-get install python3-pyaudio
```

-   **若使用虚拟环境**，需先安装编译依赖：

```
sudo apt update
sudo apt install -y python3-dev portaudio19-dev
```

然后在已激活的虚拟环境中使用 pip 安装：

```
pip install pyaudio
```

#### CentOS

```
sudo yum install -y portaudio portaudio-devel && pip install pyaudio
```

#### Windows

```
pip install pyaudio
```

安装完成后，通过 pip 安装依赖：

```
pip install websocket-client dashscope
```

-   **选择交互模式**
    
    -   VAD 模式（Voice Activity Detection，自动检测语音起止）
        
        服务端自动判断用户何时开始与停止说话并作出回应。
        
    -   Manual 模式（按下即说，松开即发送）
        
        客户端控制语音起止。用户说话结束后，客户端需主动发送消息至服务端。
        
    
    #### VAD 模式
    
    新建一个 python 文件，命名为vad\_dash.py，并将以下代码复制到文件中：
    
    vad\_dash.py
    
    ```
    # 依赖：dashscope >= 1.26.5，pyaudio
    import os
    import base64
    import time
    import pyaudio
    from dashscope.audio.qwen_omni import MultiModality, AudioFormat,OmniRealtimeCallback,OmniRealtimeConversation
    import dashscope
    
    # 配置参数：地址、API Key、音色、模型、模型角色
    # 指定地域，设为cn表示华北2（北京）地域，设为intl表示新加坡地域。请将 {WorkspaceId} 替换为您的百炼业务空间ID。
    region = 'cn'
    base_domain = '{WorkspaceId}.cn-beijing.maas.aliyuncs.com' if region == 'cn' else '{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com'
    url = f'wss://{base_domain}/api-ws/v1/realtime'
    # 配置 API Key，若没有设置环境变量，请用 API Key 将下行替换为 dashscope.api_key = "sk-xxx"
    dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')
    # 指定音色
    voice = 'Tina'
    # 指定模型
    model = 'qwen3.8-omni-flash-realtime'
    # 指定模型角色
    instructions = "你是个人助理小云，请用幽默风趣的方式回答用户的问题"
    class SimpleCallback(OmniRealtimeCallback):
        def __init__(self, pya):
            self.pya = pya
            self.out = None
        def on_open(self):
            # 初始化音频输出流
            self.out = self.pya.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=24000,
                output=True
            )
        def on_event(self, response):
            if response['type'] == 'response.audio.delta':
                # 播放音频
                self.out.write(base64.b64decode(response['delta']))
            elif response['type'] == 'conversation.item.input_audio_transcription.delta':
                # 流式预览：text为已确认前缀，stash为待确认后缀
                preview = response.get('text', '') + response.get('stash', '')
                print(f"\r[User] {preview}", end='', flush=True)
            elif response['type'] == 'conversation.item.input_audio_transcription.completed':
                # 转录完成，打印最终文本并换行
                print(f"\r[User] {response['transcript']}")
            elif response['type'] == 'response.audio_transcript.done':
                # 打印助手回复文本
                print(f"[LLM] {response['transcript']}")
    
    # 1. 初始化音频设备
    pya = pyaudio.PyAudio()
    # 2. 创建回调函数和会话
    callback = SimpleCallback(pya)
    conv = OmniRealtimeConversation(model=model, callback=callback, url=url)
    # 3. 建立连接并配置会话
    conv.connect()
    conv.update_session(output_modalities=[MultiModality.AUDIO, MultiModality.TEXT], voice=voice, instructions=instructions)
    # 4. 初始化音频输入流
    mic = pya.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True)
    # 5. 主循环处理音频输入
    print("对话已开始，对着麦克风说话 (Ctrl+C 退出)...")
    try:
        while True:
            audio_data = mic.read(3200, exception_on_overflow=False)
            conv.append_audio(base64.b64encode(audio_data).decode())
            time.sleep(0.01)
    except KeyboardInterrupt:
        # 清理资源
        conv.close()
        mic.close()
        callback.out.close()
        pya.terminate()
        print("\n对话结束")
    ```
    
    运行`vad_dash.py`，通过麦克风即可与 Qwen-Omni-Realtime 模型实时对话，系统会检测您的音频起始位置并自动发送到服务器，无需您手动发送。
    
    #### Manual 模式
    
    新建一个 python 文件，命名为`manual_dash.py`，并将以下代码复制进文件中：
    
    manual\_dash.py
    
    ```
    # 此示例使用 Qwen3.5-Omni-Plus-Realtime，演示输入转写及会话控制。
    # 依赖：dashscope >= 1.26.5，pyaudio。
    import os
    import base64
    import sys
    import threading
    import pyaudio
    from dashscope.audio.qwen_omni import *
    import dashscope
    
    # 如果没有设置环境变量，请用您的 API Key 将下行替换为 dashscope.api_key = "sk-xxx"
    dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')
    voice = 'Tina'
    
    class MyCallback(OmniRealtimeCallback):
        """最简回调：建立连接时初始化扬声器，事件中直接播放返回音频。"""
        def __init__(self, ctx):
            super().__init__()
            self.ctx = ctx
    
        def on_open(self) -> None:
            # 连接建立后初始化 PyAudio 与扬声器(24k/mono/16bit)
            print('connection opened')
            try:
                self.ctx['pya'] = pyaudio.PyAudio()
                self.ctx['out'] = self.ctx['pya'].open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=24000,
                    output=True
                )
                print('audio output initialized')
            except Exception as e:
                print('[Error] audio init failed: {}'.format(e))
    
        def on_close(self, close_status_code, close_msg) -> None:
            print('connection closed with code: {}, msg: {}'.format(close_status_code, close_msg))
            sys.exit(0)
    
        def on_event(self, response: str) -> None:
            try:
                t = response['type']
                handlers = {
                    'session.created': lambda r: print('start session: {}'.format(r['session']['id'])),
                    'conversation.item.input_audio_transcription.delta': lambda r: print('\rquestion: {}'.format(r.get('text', '') + r.get('stash', '')), end='', flush=True),
                    'conversation.item.input_audio_transcription.completed': self._transcription_completed,
                    'response.audio_transcript.delta': lambda r: print('llm text: {}'.format(r['delta'])),
                    'response.audio.delta': self._play_audio,
                    'response.done': self._response_done,
                }
                h = handlers.get(t)
                if h:
                    h(response)
            except Exception as e:
                print('[Error] {}'.format(e))
    
        def _transcription_completed(self, response):
            print()
            self.ctx['transcription_done'].set()
    
        def _play_audio(self, response):
            # 直接解码base64并写入输出流进行播放
            if self.ctx['out'] is None:
                return
            try:
                data = base64.b64decode(response['delta'])
                self.ctx['out'].write(data)
            except Exception as e:
                print('[Error] audio playback failed: {}'.format(e))
    
        def _response_done(self, response):
            # 标记本轮对话完成，用于主循环等待
            if self.ctx['conv'] is not None:
                print('[Metric] response: {}, first text delay: {}, first audio delay: {}'.format(
                    self.ctx['conv'].get_last_response_id(),
                    self.ctx['conv'].get_last_first_text_delay(),
                    self.ctx['conv'].get_last_first_audio_delay(),
                ))
            if self.ctx['resp_done'] is not None:
                self.ctx['resp_done'].set()
    
    def shutdown_ctx(ctx):
        """安全释放音频与PyAudio资源。"""
        try:
            if ctx['out'] is not None:
                ctx['out'].close()
                ctx['out'] = None
        except Exception:
            pass
        try:
            if ctx['pya'] is not None:
                ctx['pya'].terminate()
                ctx['pya'] = None
        except Exception:
            pass
    
    def stream_record_and_send(pya_inst, conversation, sample_rate=16000, chunk_size=3200):
        stop_evt = threading.Event()
        stream = pya_inst.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=sample_rate,
            input=True,
            frames_per_buffer=chunk_size
        )
    
        def _reader():
            while not stop_evt.is_set():
                try:
                    data = stream.read(chunk_size, exception_on_overflow=False)
                    conversation.append_audio(base64.b64encode(data).decode())
                except Exception:
                    break
    
        t = threading.Thread(target=_reader, daemon=True)
        t.start()
        input()
        stop_evt.set()
        t.join(timeout=1.0)
        stream.close()
    
    if __name__  == '__main__':
        print('Initializing ...')
        # 运行时上下文：存放音频与会话句柄
        ctx = {'pya': None, 'out': None, 'conv': None, 'resp_done': threading.Event(), 'transcription_done': threading.Event()}
        callback = MyCallback(ctx)
        conversation = OmniRealtimeConversation(
            model='qwen3.5-omni-plus-realtime',
            callback=callback,
            # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
            url="wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime",
        )
        try:
            conversation.connect()
        except Exception as e:
            print('[Error] connect failed: {}'.format(e))
            sys.exit(1)
    
        ctx['conv'] = conversation
        # 会话配置：启用文本+音频输出（禁用服务端VAD，改为手动录音）
        conversation.update_session(
            output_modalities=[MultiModality.AUDIO, MultiModality.TEXT],
            voice=voice,
            enable_input_audio_transcription=True,
            input_audio_transcription_model='qwen3-asr-flash-realtime',
            enable_turn_detection=False,
            instructions="你是个人助理小云，请你准确且友好地解答用户的问题，始终以乐于助人的态度回应。"
        )
    
        try:
            turn = 1
            while True:
                print(f"\n--- 第 {turn} 轮对话 ---")
                print("按 Enter 开始录音（输入 q 回车退出）...")
                user_input = input()
                if user_input.strip().lower() in ['q', 'quit']:
                    print("用户请求退出...")
                    break
                print("录音中... 再次按 Enter 停止。")
                if ctx['pya'] is None:
                    ctx['pya'] = pyaudio.PyAudio()
                stream_record_and_send(ctx['pya'], conversation)
    
                ctx['transcription_done'].clear()
                ctx['resp_done'].clear()
                conversation.commit()
                ctx['transcription_done'].wait(timeout=10)
                print("等待模型回复...")
                conversation.create_response()
                ctx['resp_done'].wait()
                turn += 1
        except KeyboardInterrupt:
            print("\n程序被用户中断")
        finally:
            shutdown_ctx(ctx)
            print("程序退出")
    ```
    
    运行`manual_dash.py`，按 Enter 键开始说话，再按一次获取模型响应的音频。
    

#### DashScope Java SDK

**选择交互模式**

-   VAD 模式（Voice Activity Detection，自动检测语音起止）
    
    Realtime API 自动判断用户何时开始与停止说话并作出回应。
    
-   Manual 模式（按下即说，松开即发送）
    
    客户端控制语音起止。用户说话结束后，客户端需主动发送消息至服务端。
    

#### VAD 模式

OmniServerVad.java

```
// 此示例使用 Qwen3.5-Omni-Plus-Realtime，演示输入转写及会话控制。
import com.alibaba.dashscope.audio.omni.*;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.google.gson.JsonObject;
import javax.sound.sampled.*;
import java.nio.ByteBuffer;
import java.util.Arrays;
import java.util.Base64;
import java.util.Map;
import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.atomic.AtomicBoolean;

public class OmniServerVad {
    static class SequentialAudioPlayer {
        private final SourceDataLine line;
        private final Queue<byte[]> audioQueue = new ConcurrentLinkedQueue<>();
        private final Thread playerThread;
        private final AtomicBoolean shouldStop = new AtomicBoolean(false);

        public SequentialAudioPlayer() throws LineUnavailableException {
            AudioFormat format = new AudioFormat(24000, 16, 1, true, false);
            line = AudioSystem.getSourceDataLine(format);
            line.open(format);
            line.start();

            playerThread = new Thread(() -> {
                while (!shouldStop.get()) {
                    byte[] audio = audioQueue.poll();
                    if (audio != null) {
                        line.write(audio, 0, audio.length);
                    } else {
                        try { Thread.sleep(10); } catch (InterruptedException ignored) {}
                    }
                }
            }, "AudioPlayer");
            playerThread.start();
        }

        public void play(String base64Audio) {
            try {
                byte[] audio = Base64.getDecoder().decode(base64Audio);
                audioQueue.add(audio);
            } catch (Exception e) {
                System.err.println("音频解码失败: " + e.getMessage());
            }
        }

        public void cancel() {
            audioQueue.clear();
            line.flush();
        }

        public void close() {
            shouldStop.set(true);
            try { playerThread.join(1000); } catch (InterruptedException ignored) {}
            line.drain();
            line.close();
        }
    }

    public static void main(String[] args) {
        try {
            SequentialAudioPlayer player = new SequentialAudioPlayer();
            AtomicBoolean userIsSpeaking = new AtomicBoolean(false);
            AtomicBoolean shouldStop = new AtomicBoolean(false);

            OmniRealtimeParam param = OmniRealtimeParam.builder()
                    .model("qwen3.5-omni-plus-realtime")
                    .apikey(System.getenv("DASHSCOPE_API_KEY"))
                    // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
                    .url("wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime")
                    .build();

            OmniRealtimeConversation conversation = new OmniRealtimeConversation(param, new OmniRealtimeCallback() {
                @Override public void onOpen() {
                    System.out.println("连接已建立");
                }
                @Override public void onClose(int code, String reason) {
                    System.out.println("连接已关闭 (" + code + "): " + reason);
                    shouldStop.set(true);
                }
                @Override public void onEvent(JsonObject event) {
                    handleEvent(event, player, userIsSpeaking);
                }
            });

            conversation.connect();
            conversation.updateSession(OmniRealtimeConfig.builder()
                    .modalities(Arrays.asList(OmniRealtimeModality.AUDIO, OmniRealtimeModality.TEXT))
                    .voice("Tina")
                    .enableTurnDetection(true)
                    .enableInputAudioTranscription(true)
                    .parameters(Map.of("instructions",
                            "你是五星级酒店的AI客服专员，请准确且友好地解答客户关于房型、设施、价格、预订政策的咨询。请始终以专业和乐于助人的态度回应，杜绝提供未经证实或超出酒店服务范围的信息。"))
                    .build()
            );

            System.out.println("请开始说话（自动检测语音开始/结束，按Ctrl+C退出）...");
            AudioFormat format = new AudioFormat(16000, 16, 1, true, false);
            TargetDataLine mic = AudioSystem.getTargetDataLine(format);
            mic.open(format);
            mic.start();

            ByteBuffer buffer = ByteBuffer.allocate(3200);
            while (!shouldStop.get()) {
                int bytesRead = mic.read(buffer.array(), 0, buffer.capacity());
                if (bytesRead > 0) {
                    byte[] chunk = new byte[bytesRead];
                    System.arraycopy(buffer.array(), 0, chunk, 0, bytesRead);
                    try {
                        conversation.appendAudio(Base64.getEncoder().encodeToString(chunk));
                    } catch (Exception e) {
                        if (e.getMessage() != null && e.getMessage().contains("closed")) {
                            System.out.println("对话已关闭，停止录音");
                            break;
                        }
                    }
                }
                Thread.sleep(20);
            }

            conversation.close(1000, "正常结束");
            player.close();
            mic.close();
            System.out.println("\n程序已退出");

        } catch (NoApiKeyException e) {
            System.err.println("未找到API KEY: 请设置环境变量 DASHSCOPE_API_KEY");
            System.exit(1);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static void handleEvent(JsonObject event, SequentialAudioPlayer player, AtomicBoolean userIsSpeaking) {
        String type = event.get("type").getAsString();
        switch (type) {
            case "input_audio_buffer.speech_started":
                System.out.println("\n[用户开始说话]");
                player.cancel();
                userIsSpeaking.set(true);
                break;
            case "input_audio_buffer.speech_stopped":
                System.out.println("[用户停止说话]");
                userIsSpeaking.set(false);
                break;
            case "response.audio.delta":
                if (!userIsSpeaking.get()) {
                    player.play(event.get("delta").getAsString());
                }
                break;
            case "conversation.item.input_audio_transcription.delta":
                // 流式预览：text为已确认前缀，stash为待确认后缀
                String preview = event.get("text").getAsString() + event.get("stash").getAsString();
                System.out.print("\r用户: " + preview);
                break;
            case "conversation.item.input_audio_transcription.completed":
                System.out.println();
                break;
            case "response.audio_transcript.done":
                System.out.println("助手: " + event.get("transcript").getAsString());
                break;
            case "response.done":
                System.out.println("回复完成");
                break;
        }
    }
}
```

运行`OmniServerVad.main()`方法，通过麦克风即可与 Realtime 模型实时对话，系统会检测您的音频起始位置并自动发送到服务器，无需您手动发送。

#### Manual 模式

OmniWithoutServerVad.java

```
// 此示例使用 Qwen3.5-Omni-Plus-Realtime，演示输入转写及会话控制。
// DashScope Java SDK 版本不低于2.22.15

import com.alibaba.dashscope.audio.omni.*;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.google.gson.JsonObject;
import javax.sound.sampled.*;
import java.io.IOException;
import java.util.Arrays;
import java.util.Base64;
import java.util.HashMap;
import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicReference;

public class OmniWithoutServerVad {
    // RealtimePcmPlayer 类定义开始
    public static class RealtimePcmPlayer {
        private int sampleRate;
        private SourceDataLine line;
        private AudioFormat audioFormat;
        private Thread decoderThread;
        private Thread playerThread;
        private AtomicBoolean stopped = new AtomicBoolean(false);
        private Queue<String> b64AudioBuffer = new ConcurrentLinkedQueue<>();
        private Queue<byte[]> RawAudioBuffer = new ConcurrentLinkedQueue<>();

        // 构造函数初始化音频格式和音频线路
        public RealtimePcmPlayer(int sampleRate) throws LineUnavailableException {
            this.sampleRate = sampleRate;
            this.audioFormat = new AudioFormat(this.sampleRate, 16, 1, true, false);
            DataLine.Info info = new DataLine.Info(SourceDataLine.class, audioFormat);
            line = (SourceDataLine) AudioSystem.getLine(info);
            line.open(audioFormat);
            line.start();
            decoderThread = new Thread(new Runnable() {
                @Override
                public void run() {
                    while (!stopped.get()) {
                        String b64Audio = b64AudioBuffer.poll();
                        if (b64Audio != null) {
                            byte[] rawAudio = Base64.getDecoder().decode(b64Audio);
                            RawAudioBuffer.add(rawAudio);
                        } else {
                            try {
                                Thread.sleep(100);
                            } catch (InterruptedException e) {
                                throw new RuntimeException(e);
                            }
                        }
                    }
                }
            });
            playerThread = new Thread(new Runnable() {
                @Override
                public void run() {
                    while (!stopped.get()) {
                        byte[] rawAudio = RawAudioBuffer.poll();
                        if (rawAudio != null) {
                            try {
                                playChunk(rawAudio);
                            } catch (IOException e) {
                                throw new RuntimeException(e);
                            } catch (InterruptedException e) {
                                throw new RuntimeException(e);
                            }
                        } else {
                            try {
                                Thread.sleep(100);
                            } catch (InterruptedException e) {
                                throw new RuntimeException(e);
                            }
                        }
                    }
                }
            });
            decoderThread.start();
            playerThread.start();
        }

        // 播放一个音频块并阻塞直到播放完成
        private void playChunk(byte[] chunk) throws IOException, InterruptedException {
            if (chunk == null || chunk.length == 0) return;

            int bytesWritten = 0;
            while (bytesWritten < chunk.length) {
                bytesWritten += line.write(chunk, bytesWritten, chunk.length - bytesWritten);
            }
            int audioLength = chunk.length / (this.sampleRate*2/1000);
            // 等待缓冲区中的音频播放完成
            Thread.sleep(audioLength - 10);
        }

        public void write(String b64Audio) {
            b64AudioBuffer.add(b64Audio);
        }

        public void cancel() {
            b64AudioBuffer.clear();
            RawAudioBuffer.clear();
        }

        public void waitForComplete() throws InterruptedException {
            while (!b64AudioBuffer.isEmpty() || !RawAudioBuffer.isEmpty()) {
                Thread.sleep(100);
            }
            line.drain();
        }

        public void shutdown() throws InterruptedException {
            stopped.set(true);
            decoderThread.join();
            playerThread.join();
            if (line != null && line.isRunning()) {
                line.drain();
                line.close();
            }
        }
    } // RealtimePcmPlayer 类定义结束
    // 录音并实时发送方法
    private static void recordAndSend(TargetDataLine line, OmniRealtimeConversation conversation) {
        byte[] buffer = new byte[3200];
        AtomicBoolean stopRecording = new AtomicBoolean(false);

        // 启动监听Enter键的线程
        Thread enterKeyListener = new Thread(() -> {
            try {
                System.in.read();
                stopRecording.set(true);
            } catch (IOException e) {
                e.printStackTrace();
            }
        });
        enterKeyListener.start();

        // 录音并实时发送
        while (!stopRecording.get()) {
            int count = line.read(buffer, 0, buffer.length);
            if (count > 0) {
                byte[] chunk = new byte[count];
                System.arraycopy(buffer, 0, chunk, 0, count);
                conversation.appendAudio(Base64.getEncoder().encodeToString(chunk));
            }
        }
    }

    public static void main(String[] args) throws InterruptedException, LineUnavailableException {
        OmniRealtimeParam param = OmniRealtimeParam.builder()
                .model("qwen3.5-omni-plus-realtime")
                // .apikey("your-dashscope-api-key")
                // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
                .url("wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime")
                .build();
        AtomicReference<CountDownLatch> responseDoneLatch = new AtomicReference<>(null);
        responseDoneLatch.set(new CountDownLatch(1));
        AtomicReference<CountDownLatch> transcriptionDoneLatch = new AtomicReference<>(null);
        transcriptionDoneLatch.set(new CountDownLatch(1));

        RealtimePcmPlayer audioPlayer = new RealtimePcmPlayer(24000);
        final AtomicReference<OmniRealtimeConversation> conversationRef = new AtomicReference<>(null);
        OmniRealtimeConversation conversation = new OmniRealtimeConversation(param, new OmniRealtimeCallback() {
            @Override
            public void onOpen() {
                System.out.println("connection opened");
            }
            @Override
            public void onEvent(JsonObject message) {
                String type = message.get("type").getAsString();
                switch(type) {
                    case "session.created":
                        System.out.println("start session: " + message.get("session").getAsJsonObject().get("id").getAsString());
                        break;
                    case "conversation.item.input_audio_transcription.delta":
                        // 流式预览：text为已确认前缀，stash为待确认后缀
                        String transcriptPreview = message.get("text").getAsString() + message.get("stash").getAsString();
                        System.out.print("\rquestion: " + transcriptPreview);
                        break;
                    case "conversation.item.input_audio_transcription.completed":
                        System.out.println();
                        transcriptionDoneLatch.get().countDown();
                        break;
                    case "response.audio_transcript.delta":
                        System.out.println("got llm response delta: " + message.get("delta").getAsString());
                        break;
                    case "response.audio.delta":
                        String recvAudioB64 = message.get("delta").getAsString();
                        audioPlayer.write(recvAudioB64);
                        break;
                    case "response.done":
                        System.out.println("======RESPONSE DONE======");
                        if (conversationRef.get() != null) {
                            System.out.println("[Metric] response: " + conversationRef.get().getResponseId() +
                                    ", first text delay: " + conversationRef.get().getFirstTextDelay() +
                                    " ms, first audio delay: " + conversationRef.get().getFirstAudioDelay() + " ms");
                        }
                        responseDoneLatch.get().countDown();
                        break;
                    default:
                        break;
                }
            }
            @Override
            public void onClose(int code, String reason) {
                System.out.println("connection closed code: " + code + ", reason: " + reason);
            }
        });
        conversationRef.set(conversation);
        try {
            conversation.connect();
        } catch (NoApiKeyException e) {
            throw new RuntimeException(e);
        }
        OmniRealtimeConfig config = OmniRealtimeConfig.builder()
                .modalities(Arrays.asList(OmniRealtimeModality.AUDIO, OmniRealtimeModality.TEXT))
                .voice("Tina")
                .enableTurnDetection(false)
                // 设定模型角色
                .parameters(new HashMap<String, Object>() {{
                    put("instructions","你是个人助理小云，请你准确且友好地解答用户的问题，始终以乐于助人的态度回应。");
                }})
                .build();
        conversation.updateSession(config);

        // 新增麦克风录音功能
        AudioFormat format = new AudioFormat(16000, 16, 1, true, false);
        DataLine.Info info = new DataLine.Info(TargetDataLine.class, format);

        if (!AudioSystem.isLineSupported(info)) {
            System.out.println("Line not supported");
            return;
        }

        TargetDataLine line = null;
        try {
            line = (TargetDataLine) AudioSystem.getLine(info);
            line.open(format);
            line.start();

            while (true) {
                System.out.println("按Enter开始录音...");
                try {
                    System.in.read();
                } catch (IOException e) {
                    System.err.println("读取输入时发生错误: " + e.getMessage());
                    break; // 发生错误时退出循环
                }
                System.out.println("开始录音，请说话...再次按Enter停止录音并发送");
                recordAndSend(line, conversation);
                conversation.commit();
                // 等待转录完成后再触发模型回复，避免输出交错
                transcriptionDoneLatch.get().await(10, TimeUnit.SECONDS);
                System.out.println("等待模型回复...");
                conversation.createResponse(null, null);
                responseDoneLatch.get().await();
                // 重置latch以便下次等待
                responseDoneLatch.set(new CountDownLatch(1));
                transcriptionDoneLatch.set(new CountDownLatch(1));
            }
        } catch (LineUnavailableException e) {
            e.printStackTrace();
        } finally {
            if (line != null) {
                line.stop();
                line.close();
            }
        }
    }}
```

运行`OmniWithoutServerVad.main()`方法，按 Enter 键开始录音，录音过程中再次按 Enter 键停止录音并发送，随后将接收并播放模型响应。

#### WebSocket（Python）

-   **准备运行环境**
    
    您的 Python 版本需要不低于 3.10。
    
    首先根据您的操作系统来安装 pyaudio。
    
    #### macOS
    
    ```
    brew install portaudio && pip install pyaudio
    ```
    
    #### Debian/Ubuntu
    
    ```
    sudo apt-get install python3-pyaudio
    
    或者
    
    pip install pyaudio
    ```
    
    > 推荐使用`pip install pyaudio`。如果安装失败，请先根据您的操作系统安装`portaudio`依赖。
    
    #### CentOS
    
    ```
    sudo yum install -y portaudio portaudio-devel && pip install pyaudio
    ```
    
    #### Windows
    
    ```
    pip install pyaudio
    ```
    
    安装完成后，通过 pip 安装 websocket 相关的依赖：
    

```
pip install websockets==15.0.1
```

-   **创建客户端**
    
    在本地新建一个 python 文件，命名为`omni_realtime_client.py`，并将以下代码复制进文件中：
    
    omni\_realtime\_client.py
    
    ```
    import asyncio
    import websockets
    import json
    import base64
    import time
    from typing import Optional, Callable, List, Dict, Any
    from enum import Enum
    
    class TurnDetectionMode(Enum):
        SERVER_VAD = "server_vad"
        SEMANTIC_VAD = "semantic_vad"  # 使用 Qwen3.8-Omni-Flash-Realtime 或 Qwen3.5-Omni-Realtime 系列模型时推荐
        MANUAL = "manual"
    
    class OmniRealtimeClient:
    
        def __init__(
                self,
                base_url,
                api_key: str,
                model: str = "",
                voice: str = "Ethan",
                instructions: str = "You are a helpful assistant.",
                turn_detection_mode: TurnDetectionMode = TurnDetectionMode.SERVER_VAD,
                on_text_delta: Optional[Callable[[str], None]] = None,
                on_audio_delta: Optional[Callable[[bytes], None]] = None,
                on_input_transcript: Optional[Callable[[str], None]] = None,
                on_output_transcript: Optional[Callable[[str], None]] = None,
                extra_event_handlers: Optional[Dict[str, Callable[[Dict[str, Any]], None]]] = None
        ):
            self.base_url = base_url
            self.api_key = api_key
            self.model = model
            self.voice = voice
            self.instructions = instructions
            self.ws = None
            self.on_text_delta = on_text_delta
            self.on_audio_delta = on_audio_delta
            self.on_input_transcript = on_input_transcript
            self.on_output_transcript = on_output_transcript
            self.turn_detection_mode = turn_detection_mode
            self.extra_event_handlers = extra_event_handlers or {}
    
            # 当前回复状态
            self._current_response_id = None
            self._current_item_id = None
            self._is_responding = False
            # 输入/输出转录打印状态
            self._print_input_transcript = True
            self._output_transcript_buffer = ""
    
        async def connect(self) -> None:
            """与 Realtime API 建立 WebSocket 连接。"""
            url = f"{self.base_url}?model={self.model}"
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            self.ws = await websockets.connect(url, additional_headers=headers)
    
            # 会话配置
            session_config = {
                "modalities": ["text", "audio"],
                "voice": self.voice,
                "instructions": self.instructions,
                # 配置音频输入/输出格式和采样率
                "audio": {
                    "input": {"format": {"type": "pcm", "sample_rate": 16000}},
                    "output": {"format": {"type": "pcm", "sample_rate": 24000}}
                },
                "input_audio_transcription": {
                    "model": "qwen3-asr-flash-realtime"
                }
            }
    
            if self.turn_detection_mode == TurnDetectionMode.MANUAL:
                session_config['turn_detection'] = None
                await self.update_session(session_config)
            elif self.turn_detection_mode == TurnDetectionMode.SERVER_VAD:
                session_config['turn_detection'] = {
                    "type": "server_vad",
                    "threshold": 0.1,
                    "prefix_padding_ms": 500,
                    "silence_duration_ms": 900
                }
                await self.update_session(session_config)
            elif self.turn_detection_mode == TurnDetectionMode.SEMANTIC_VAD:
                session_config['turn_detection'] = {
                    "type": "semantic_vad",
                    "threshold": 0.1,
                    "prefix_padding_ms": 500,
                    "silence_duration_ms": 900
                }
                await self.update_session(session_config)
            else:
                raise ValueError(f"Invalid turn detection mode: {self.turn_detection_mode}")
    
        async def send_event(self, event) -> None:
            event['event_id'] = "event_" + str(int(time.time() * 1000))
            await self.ws.send(json.dumps(event))
    
        async def update_session(self, config: Dict[str, Any]) -> None:
            """更新会话配置。"""
            event = {
                "type": "session.update",
                "session": config
            }
            await self.send_event(event)
    
        async def stream_audio(self, audio_chunk: bytes) -> None:
            """向 API 流式发送原始音频数据。"""
            # 仅支持 16bit 16kHz 单声道 PCM
            audio_b64 = base64.b64encode(audio_chunk).decode()
            append_event = {
                "type": "input_audio_buffer.append",
                "audio": audio_b64
            }
            await self.send_event(append_event)
    
        async def commit_audio_buffer(self) -> None:
            """提交音频缓冲区以触发处理。"""
            event = {
                "type": "input_audio_buffer.commit"
            }
            await self.send_event(event)
    
        async def append_image(self, image_chunk: bytes) -> None:
            """向图像缓冲区追加图像数据。
            图像数据可以来自本地文件，也可以来自实时视频流。
            注意:
                - 图像格式必须为 JPG 或 JPEG。推荐分辨率为 480P 或 720P，最高支持 1080P。
                - 单张图片经Base64编码后不得超过256KB，建议编码前原始图片大小不超过190KB。
                - 将图像数据编码为 Base64 后再发送。
                - 建议以 1张/秒 的频率向服务端发送图像。
                - 在发送图像数据之前，需要至少发送过一次音频数据。
            """
            image_b64 = base64.b64encode(image_chunk).decode()
            event = {
                "type": "input_image_buffer.append",
                "image": image_b64
            }
            await self.send_event(event)
    
        async def create_response(self) -> None:
            """向 API 请求生成回复（仅在手动模式下需要调用）。"""
            event = {
                "type": "response.create"
            }
            await self.send_event(event)
    
        async def cancel_response(self) -> None:
            """取消当前回复。"""
            event = {
                "type": "response.cancel"
            }
            await self.send_event(event)
    
        async def handle_interruption(self):
            """处理用户对当前回复的打断。"""
            if not self._is_responding:
                return
            # 1. 取消当前回复
            if self._current_response_id:
                await self.cancel_response()
    
            self._is_responding = False
            self._current_response_id = None
            self._current_item_id = None
    
        async def handle_messages(self) -> None:
            try:
                async for message in self.ws:
                    event = json.loads(message)
                    event_type = event.get("type")
                    if event_type == "error":
                        print(" Error: ", event['error'])
                        continue
                    elif event_type == "response.created":
                        self._current_response_id = event.get("response", {}).get("id")
                        self._is_responding = True
                    elif event_type == "response.output_item.added":
                        self._current_item_id = event.get("item", {}).get("id")
                    elif event_type == "response.done":
                        self._is_responding = False
                        self._current_response_id = None
                        self._current_item_id = None
                        if event_type in self.extra_event_handlers:
                            self.extra_event_handlers[event_type](event)
                    elif event_type == "input_audio_buffer.speech_started":
                        print("检测到语音开始")
                        if self._is_responding:
                            print("处理打断")
                            await self.handle_interruption()
                    elif event_type == "input_audio_buffer.speech_stopped":
                        print("检测到语音结束")
                    elif event_type == "response.text.delta":
                        if self.on_text_delta:
                            self.on_text_delta(event["delta"])
                    elif event_type == "response.audio.delta":
                        if self.on_audio_delta:
                            audio_bytes = base64.b64decode(event["delta"])
                            self.on_audio_delta(audio_bytes)
                    elif event_type == "conversation.item.input_audio_transcription.delta":
                        preview = event.get("text", "") + event.get("stash", "")
                        print(f"\r用户: {preview}", end='', flush=True)
                    elif event_type == "conversation.item.input_audio_transcription.completed":
                        transcript = event.get("transcript", "")
                        print()
                        if self.on_input_transcript:
                            await asyncio.to_thread(self.on_input_transcript, transcript)
                            self._print_input_transcript = True
                    elif event_type == "response.audio_transcript.delta":
                        if self.on_output_transcript:
                            delta = event.get("delta", "")
                            if not self._print_input_transcript:
                                self._output_transcript_buffer += delta
                            else:
                                if self._output_transcript_buffer:
                                    await asyncio.to_thread(self.on_output_transcript, self._output_transcript_buffer)
                                    self._output_transcript_buffer = ""
                                await asyncio.to_thread(self.on_output_transcript, delta)
                    elif event_type == "response.audio_transcript.done":
                        print(f"大模型: {event.get('transcript', '')}")
                        self._print_input_transcript = False
                    elif event_type in self.extra_event_handlers:
                        self.extra_event_handlers[event_type](event)
            except websockets.exceptions.ConnectionClosed:
                print(" Connection closed")
            except Exception as e:
                print(" Error in message handling: ", str(e))
        async def close(self) -> None:
            """关闭 WebSocket 连接。"""
            if self.ws:
                await self.ws.close()
    ```
    
-   **选择交互模式**
    
    -   VAD 模式（Voice Activity Detection，自动检测语音起止）
        
        Realtime API 自动判断用户何时开始与停止说话并作出回应。
        
    -   Manual 模式（按下即说，松开即发送）
        
        客户端控制语音起止。用户说话结束后，客户端需主动发送消息至服务端。
        
    
    #### VAD 模式
    
    在`omni_realtime_client.py`的同级目录下新建另一个 python 文件，命名为`vad_mode.py`，并将以下代码复制进文件中：
    
    vad\_mode.py
    
    ```
    # -- coding: utf-8 --
    import os, asyncio, pyaudio, queue, threading
    from omni_realtime_client import OmniRealtimeClient, TurnDetectionMode
    
    # 音频播放器类（处理中断）
    class AudioPlayer:
        def __init__(self, pyaudio_instance, rate=24000):
            self.stream = pyaudio_instance.open(format=pyaudio.paInt16, channels=1, rate=rate, output=True)
            self.queue = queue.Queue()
            self.stop_evt = threading.Event()
            self.interrupt_evt = threading.Event()
            threading.Thread(target=self._run, daemon=True).start()
    
        def _run(self):
            while not self.stop_evt.is_set():
                try:
                    data = self.queue.get(timeout=0.5)
                    if data is None: break
                    if not self.interrupt_evt.is_set(): self.stream.write(data)
                    self.queue.task_done()
                except queue.Empty: continue
    
        def add_audio(self, data): self.queue.put(data)
        def handle_interrupt(self): self.interrupt_evt.set(); self.queue.queue.clear()
        def stop(self): self.stop_evt.set(); self.queue.put(None); self.stream.stop_stream(); self.stream.close()
    
    # 麦克风录音并发送
    async def record_and_send(client):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=3200)
        print("开始录音，请讲话...")
        try:
            while True:
                audio_data = stream.read(3200)
                await client.stream_audio(audio_data)
                await asyncio.sleep(0.02)
        finally:
            stream.stop_stream(); stream.close(); p.terminate()
    
    async def main():
        p = pyaudio.PyAudio()
        player = AudioPlayer(pyaudio_instance=p)
    
        client = OmniRealtimeClient(
            # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
            base_url="wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime",
            api_key=os.environ.get("DASHSCOPE_API_KEY"),
            model="qwen3.5-omni-plus-realtime",
            voice="Ethan",
            instructions="你是小云，风趣幽默的好助手",
            # 使用qwen3.5-omni-realtime系列模型时推荐设为SEMANTIC_VAD
            turn_detection_mode=TurnDetectionMode.SEMANTIC_VAD,
            on_text_delta=lambda t: print(f"\nAssistant: {t}", end="", flush=True),
            on_audio_delta=player.add_audio,
        )
    
        await client.connect()
        print("连接成功，开始实时对话...")
    
        # 并发运行
        await asyncio.gather(client.handle_messages(), record_and_send(client))
    
    if __name__ == "__main__":
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("\n程序已退出。")
    ```
    
    运行`vad_mode.py`，通过麦克风即可与 Realtime 模型实时对话，系统会检测您的音频起始位置并自动发送到服务器，无需您手动发送。
    
    #### Manual 模式
    
    在`omni_realtime_client.py`的同级目录下新建另一个 python 文件，命名为`manual_mode.py`，并将以下代码复制进文件中：
    
    manual\_mode.py
    
    ```
    # -- coding: utf-8 --
    import os
    import asyncio
    import time
    import threading
    import queue
    import pyaudio
    from omni_realtime_client import OmniRealtimeClient, TurnDetectionMode
    
    class AudioPlayer:
        """实时音频播放器类"""
        def __init__(self, sample_rate=24000, channels=1, sample_width=2):
            self.sample_rate = sample_rate
            self.channels = channels
            self.sample_width = sample_width  # 2 bytes for 16-bit
            self.audio_queue = queue.Queue()
            self.is_playing = False
            self.play_thread = None
            self.pyaudio_instance = None
            self.stream = None
            self._lock = threading.Lock()  # 添加锁来同步访问
            self._last_data_time = time.time()  # 记录最后接收数据的时间
            self._response_done = False  # 添加响应完成标志
            self._waiting_for_response = False # 标记是否正在等待服务器响应
            # 记录最后一次向音频流写入数据的时间及最近一次音频块的时长，用于更精确地判断播放结束
            self._last_play_time = time.time()
            self._last_chunk_duration = 0.0
    
        def start(self):
            """启动音频播放器"""
            with self._lock:
                if self.is_playing:
                    return
    
                self.is_playing = True
    
                try:
                    self.pyaudio_instance = pyaudio.PyAudio()
    
                    # 创建音频输出流
                    self.stream = self.pyaudio_instance.open(
                        format=pyaudio.paInt16,  # 16-bit
                        channels=self.channels,
                        rate=self.sample_rate,
                        output=True,
                        frames_per_buffer=1024
                    )
    
                    # 启动播放线程
                    self.play_thread = threading.Thread(target=self._play_audio)
                    self.play_thread.daemon = True
                    self.play_thread.start()
    
                    print("音频播放器已启动")
                except Exception as e:
                    print(f"启动音频播放器失败: {e}")
                    self._cleanup_resources()
                    raise
    
        def stop(self):
            """停止音频播放器"""
            with self._lock:
                if not self.is_playing:
                    return
    
                self.is_playing = False
    
            # 清空队列
            while not self.audio_queue.empty():
                try:
                    self.audio_queue.get_nowait()
                except queue.Empty:
                    break
    
            # 等待播放线程结束（在锁外面等待，避免死锁）
            if self.play_thread and self.play_thread.is_alive():
                self.play_thread.join(timeout=2.0)
    
            # 再次获取锁来清理资源
            with self._lock:
                self._cleanup_resources()
    
            print("音频播放器已停止")
    
        def _cleanup_resources(self):
            """清理音频资源（必须在锁内调用）"""
            try:
                # 关闭音频流
                if self.stream:
                    if not self.stream.is_stopped():
                        self.stream.stop_stream()
                    self.stream.close()
                    self.stream = None
            except Exception as e:
                print(f"关闭音频流时出错: {e}")
    
            try:
                if self.pyaudio_instance:
                    self.pyaudio_instance.terminate()
                    self.pyaudio_instance = None
            except Exception as e:
                print(f"终止PyAudio时出错: {e}")
    
        def add_audio_data(self, audio_data):
            """添加音频数据到播放队列"""
            if self.is_playing and audio_data:
                self.audio_queue.put(audio_data)
                with self._lock:
                    self._last_data_time = time.time()  # 更新最后接收数据的时间
                    self._waiting_for_response = False # 收到数据，不再等待
    
        def stop_receiving_data(self):
            """标记不再接收新的音频数据"""
            with self._lock:
                self._response_done = True
                self._waiting_for_response = False # 响应结束，不再等待
    
        def prepare_for_next_turn(self):
            """为下一轮对话重置播放器状态。"""
            with self._lock:
                self._response_done = False
                self._last_data_time = time.time()
                self._last_play_time = time.time()
                self._last_chunk_duration = 0.0
                self._waiting_for_response = True # 开始等待下一轮响应
    
            # 清空上一轮可能残留的音频数据
            while not self.audio_queue.empty():
                try:
                    self.audio_queue.get_nowait()
                except queue.Empty:
                    break
    
        def is_finished_playing(self):
            """检查是否已经播放完所有音频数据"""
            with self._lock:
                queue_size = self.audio_queue.qsize()
                time_since_last_data = time.time() - self._last_data_time
                time_since_last_play = time.time() - self._last_play_time
    
                # ---------------------- 智能结束判定 ----------------------
                # 1. 首选：如果服务器已标记完成且播放队列为空
                #    进一步等待最近一块音频播放完毕（音频块时长 + 0.1s 容错）。
                if self._response_done and queue_size == 0:
                    min_wait = max(self._last_chunk_duration + 0.1, 0.5)  # 至少等待 0.5s
                    if time_since_last_play >= min_wait:
                        return True
    
                # 2. 备用：如果长时间没有新数据且播放队列为空
                #    当服务器没有明确发出 `response.done` 时，此逻辑作为保障
                if not self._waiting_for_response and queue_size == 0 and time_since_last_data > 1.0:
                    print("\n(超时未收到新音频，判定播放结束)")
                    return True
    
                return False
    
        def _play_audio(self):
            """播放音频数据的工作线程"""
            while True:
                # 检查是否应该停止
                with self._lock:
                    if not self.is_playing:
                        break
                    stream_ref = self.stream  # 获取流的引用
    
                try:
                    # 从队列中获取音频数据，超时0.1秒
                    audio_data = self.audio_queue.get(timeout=0.1)
    
                    # 再次检查状态和流的有效性
                    with self._lock:
                        if self.is_playing and stream_ref and not stream_ref.is_stopped():
                            try:
                                # 播放音频数据
                                stream_ref.write(audio_data)
                                # 更新最近播放信息
                                self._last_play_time = time.time()
                                self._last_chunk_duration = len(audio_data) / (self.channels * self.sample_width) / self.sample_rate
                            except Exception as e:
                                print(f"写入音频流时出错: {e}")
                                break
    
                    # 标记该数据块已处理完成
                    self.audio_queue.task_done()
    
                except queue.Empty:
                    # 队列为空时继续等待
                    continue
                except Exception as e:
                    print(f"播放音频时出错: {e}")
                    break
    
    class MicrophoneRecorder:
        """实时麦克风录音器"""
        def __init__(self, sample_rate=16000, channels=1, chunk_size=3200):
            self.sample_rate = sample_rate
            self.channels = channels
            self.chunk_size = chunk_size
            self.pyaudio_instance = None
            self.stream = None
            self.frames = []
            self._is_recording = False
            self._record_thread = None
    
        def _recording_thread(self):
            """录音工作线程"""
            # 在 _is_recording 为 True 期间，持续从音频流中读取数据
            while self._is_recording:
                try:
                    # 使用 exception_on_overflow=False 避免因缓冲区溢出而崩溃
                    data = self.stream.read(self.chunk_size, exception_on_overflow=False)
                    self.frames.append(data)
                except (IOError, OSError) as e:
                    # 当流被关闭时，读取操作可能会引发错误
                    print(f"录音流读取错误，可能已关闭: {e}")
                    break
    
        def start(self):
            """开始录音"""
            if self._is_recording:
                print("录音已在进行中。")
                return
    
            self.frames = []
            self._is_recording = True
    
            try:
                self.pyaudio_instance = pyaudio.PyAudio()
                self.stream = self.pyaudio_instance.open(
                    format=pyaudio.paInt16,
                    channels=self.channels,
                    rate=self.sample_rate,
                    input=True,
                    frames_per_buffer=self.chunk_size
                )
    
                self._record_thread = threading.Thread(target=self._recording_thread)
                self._record_thread.daemon = True
                self._record_thread.start()
                print("麦克风录音已开始...")
            except Exception as e:
                print(f"启动麦克风失败: {e}")
                self._is_recording = False
                self._cleanup()
                raise
    
        def stop(self):
            """停止录音并返回音频数据"""
            if not self._is_recording:
                return None
    
            self._is_recording = False
    
            # 等待录音线程安全退出
            if self._record_thread:
                self._record_thread.join(timeout=1.0)
    
            self._cleanup()
    
            print("麦克风录音已停止。")
            return b''.join(self.frames)
    
        def _cleanup(self):
            """安全地清理 PyAudio 资源"""
            if self.stream:
                try:
                    if self.stream.is_active():
                        self.stream.stop_stream()
                    self.stream.close()
                except Exception as e:
                    print(f"关闭音频流时出错: {e}")
    
            if self.pyaudio_instance:
                try:
                    self.pyaudio_instance.terminate()
                except Exception as e:
                    print(f"终止 PyAudio 实例时出错: {e}")
    
            self.stream = None
            self.pyaudio_instance = None
    
    async def interactive_test():
        """
        交互式测试脚本：允许多轮连续对话，每轮可以发送音频和图片。
        """
        # ------------------- 1. 初始化和连接 (一次性) -------------------
        api_key = os.environ.get("DASHSCOPE_API_KEY")
        if not api_key:
            print("请设置DASHSCOPE_API_KEY环境变量")
            return
    
        print("--- 实时多轮音视频对话客户端 ---")
        print("正在初始化音频播放器和客户端...")
    
        audio_player = AudioPlayer()
        audio_player.start()
    
        def on_audio_received(audio_data):
            audio_player.add_audio_data(audio_data)
    
        transcription_done = threading.Event()
    
        def on_transcription_completed(transcript):
            transcription_done.set()
    
        def on_response_done(event):
            print("\n(收到响应结束标记)")
            audio_player.stop_receiving_data()
    
        realtime_client = OmniRealtimeClient(
            # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
            base_url="wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime",
            api_key=api_key,
            model="qwen3.8-omni-flash-realtime",
            voice="Tina",
            instructions="你是个人助理小云，请你准确且友好地解答用户的问题，始终以乐于助人的态度回应。", # 设定模型角色
            on_text_delta=lambda text: print(f"助手回复: {text}", end="", flush=True),
            on_audio_delta=on_audio_received,
            on_input_transcript=on_transcription_completed,
            turn_detection_mode=TurnDetectionMode.MANUAL,
            extra_event_handlers={"response.done": on_response_done}
        )
    
        message_handler_task = None
        try:
            await realtime_client.connect()
            print("已连接到服务器。输入 'q' 或 'quit' 可随时退出程序。")
            message_handler_task = asyncio.create_task(realtime_client.handle_messages())
            await asyncio.sleep(0.5)
    
            turn_counter = 1
            # ------------------- 2. 多轮对话循环 -------------------
            while True:
                print(f"\n--- 第 {turn_counter} 轮对话 ---")
                audio_player.prepare_for_next_turn()
    
                recorded_audio = None
                image_paths = []
    
                # --- 获取用户输入：从麦克风录音 ---
                loop = asyncio.get_event_loop()
                recorder = MicrophoneRecorder(sample_rate=16000) # 推荐使用16k采样率进行语音识别
    
                print("准备录音。按 Enter 键开始录音 (或输入 'q' 退出)...")
                user_input = await loop.run_in_executor(None, input)
                if user_input.strip().lower() in ['q', 'quit']:
                    print("用户请求退出...")
                    return
    
                try:
                    recorder.start()
                except Exception:
                    print("无法启动录音，请检查您的麦克风权限和设备。跳过本轮。")
                    continue
    
                print("录音中... 再次按 Enter 键停止录音。")
                await loop.run_in_executor(None, input)
    
                recorded_audio = recorder.stop()
    
                if not recorded_audio or len(recorded_audio) == 0:
                    print("未录制到有效音频，请重新开始本轮对话。")
                    continue
    
                # --- 获取图片输入 (可选) ---
                # 以下图片输入功能已被注释，暂时禁用。若需启用请取消下方代码注释。
                # print("\n请逐行输入【图片文件】的绝对路径 (可选)。完成后，输入 's' 或按 Enter 发送请求。")
                # while True:
                #     path = input("图片路径: ").strip()
                #     if path.lower() == 's' or path == '':
                #         break
                #     if path.lower() in ['q', 'quit']:
                #         print("用户请求退出...")
                #         return
                #
                #     if not os.path.isabs(path):
                #         print("错误: 请输入绝对路径。")
                #         continue
                #     if not os.path.exists(path):
                #         print(f"错误: 文件不存在 -> {path}")
                #         continue
                #     image_paths.append(path)
                #     print(f"已添加图片: {os.path.basename(path)}")
    
                # --- 3. 发送数据并获取响应 ---
                print("\n--- 输入确认 ---")
                print(f"待处理音频: 1个 (来自麦克风), 图片: {len(image_paths)}个")
                print("------------------")
    
                # 3.1 发送录制的音频
                try:
                    print(f"发送麦克风录音 ({len(recorded_audio)}字节)")
                    await realtime_client.stream_audio(recorded_audio)
                    await asyncio.sleep(0.1)
                except Exception as e:
                    print(f"发送麦克风录音失败: {e}")
                    continue
    
                # 3.2 发送所有图片文件
                # 以下图片发送代码已被注释，暂时禁用。
                # for i, path in enumerate(image_paths):
                #     try:
                #         with open(path, "rb") as f:
                #             data = f.read()
                #         print(f"发送图片 {i+1}: {os.path.basename(path)} ({len(data)}字节)")
                #         await realtime_client.append_image(data)
                #         await asyncio.sleep(0.1)
                #     except Exception as e:
                #         print(f"发送图片 {os.path.basename(path)} 失败: {e}")
    
                # 3.3 提交并等待响应
                print("录音结束，等待模型回复...")
                await realtime_client.commit_audio_buffer()
                # 等待转录完成后再触发模型回复，避免输出交错
                await asyncio.to_thread(transcription_done.wait, 10)
                transcription_done.clear()
                await realtime_client.create_response()
    
                print("等待并播放服务器响应音频...")
                start_time = time.time()
                max_wait_time = 60
                while not audio_player.is_finished_playing():
                    if time.time() - start_time > max_wait_time:
                        print(f"\n等待超时 ({max_wait_time}秒), 进入下一轮。")
                        break
                    await asyncio.sleep(0.2)
    
                print("\n本轮音频播放完成！")
                turn_counter += 1
    
        except (asyncio.CancelledError, KeyboardInterrupt):
            print("\n程序被中断。")
        except Exception as e:
            print(f"发生未处理的错误: {e}")
        finally:
            # ------------------- 4. 清理资源 -------------------
            print("\n正在关闭连接并清理资源...")
            if message_handler_task and not message_handler_task.done():
                message_handler_task.cancel()
    
            if 'realtime_client' in locals() and realtime_client.ws:
                await realtime_client.close()
                print("连接已关闭。")
    
            audio_player.stop()
            print("程序退出。")
    
    if __name__ == "__main__":
        try:
            asyncio.run(interactive_test())
        except KeyboardInterrupt:
            print("\n程序被用户强制退出。")
    ```
    
    运行`manual_mode.py`，按 Enter 键开始说话，再按一次获取模型响应的音频。
    

#### WebRTC

#### Python

-   **准备运行环境**
    
    您的 Python 版本需要不低于 3.10。安装以下依赖：
    

```
pip install aiortc aiohttp sounddevice numpy certifi av
```

-   **运行示例**
    
    新建一个 Python 文件，命名为 `webrtc_demo.py`，并将以下代码复制到文件中：
    
    webrtc\_demo.py
    
    ```
    # 依赖安装：pip install aiortc aiohttp sounddevice numpy certifi av
    import asyncio
    import json
    import os
    import queue
    import ssl
    import threading
    
    import aiohttp
    import certifi
    import numpy as np
    import sounddevice as sd
    from aiortc import RTCPeerConnection, RTCConfiguration, RTCSessionDescription
    from aiortc.contrib.media import MediaPlayer
    from av import AudioFrame
    
    # 替换为您的 API Key，或通过环境变量 DASHSCOPE_API_KEY 设置
    API_KEY = os.getenv("DASHSCOPE_API_KEY", "your-api-key")
    MODEL = "qwen3.8-omni-flash-realtime"
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    SIGNALING_URL = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/webrtc/realtime?model=" + MODEL
    
    # --------------- 音频帧解析 ---------------
    
    def _nb_channels(frame: AudioFrame) -> int:
        """获取音频帧的声道数，兼容不同版本的 PyAV"""
        if hasattr(frame.layout, "nb_channels"):
            return int(frame.layout.nb_channels)
        ch = getattr(frame.layout, "channels", 1)
        if isinstance(ch, (tuple, list)):
            return len(ch)
        return int(ch)
    
    def audioframe_to_s16_samples(frame: AudioFrame) -> np.ndarray:
        """
        服务端返回的音频帧是双声道交错排列，直接 reshape 会声道错乱，需要按实际声道数重排为 (采样数, 声道数)。
        aiortc 底层解码库不同版本对同一份音频返回的数组形状不同，这里做统一处理。
        """
        arr = np.asarray(frame.to_ndarray())
        ch = _nb_channels(frame)
        samples = int(frame.samples)
    
        if arr.ndim == 2 and arr.shape[0] == ch and arr.shape[1] == samples:
            return arr.T.copy()
        if arr.ndim == 2 and arr.shape[0] == 1 and arr.shape[1] == samples * ch:
            return arr.reshape(-1).reshape(samples, ch).copy()
        if arr.ndim == 1 and arr.shape[0] == samples * ch:
            return arr.reshape(samples, ch).copy()
    
        flat = arr.reshape(-1)
        if ch > 0 and flat.size % ch == 0:
            return flat.reshape(flat.size // ch, ch).copy()
        raise ValueError(f"unexpected shape={arr.shape}, ch={ch}, samples={samples}")
    
    # --------------- 低延迟音频播放器 ---------------
    
    class RemoteAudioPlayer:
        """
        低延迟音频播放器，每次只取 5ms 的音频块播放，减少延迟。
        支持语音打断：用户开始说话时清空缓存，停止播放模型的旧回复。
        播放时将服务端返回的双声道音频合并为单声道（左右声道取均值）。
        """
        def __init__(self, samplerate=48000, out_channels=1, blocksize=240, max_seconds=0.2):
            self.samplerate = samplerate
            self.out_channels = out_channels
            self.blocksize = blocksize
            self._q = queue.Queue(maxsize=max(5, int(max_seconds * samplerate / blocksize) + 5))
            self._lock = threading.Lock()
            self._rb_size = max(1, int(max_seconds * samplerate))
            self._rb = np.zeros((self._rb_size, out_channels), dtype=np.int16)
            self._rb_w = 0
            self._rb_r = 0
            self._rb_len = 0
            self._stream = None
            self._closed = False
    
        def start(self):
            if self._stream:
                return
    
            def callback(outdata, frames, _time, status):
                if self._closed:
                    outdata[:] = np.zeros((frames, self.out_channels), dtype=np.int16)
                    return
                while True:
                    try:
                        chunk = self._q.get_nowait()
                    except queue.Empty:
                        break
                    with self._lock:
                        self._write_rb(chunk)
                with self._lock:
                    out = self._read_rb(frames)
                outdata[:] = out
    
            self._stream = sd.OutputStream(
                samplerate=self.samplerate,
                channels=self.out_channels,
                dtype="int16",
                blocksize=self.blocksize,
                callback=callback,
            )
            self._stream.start()
    
        def clear(self):
            """清空播放缓存，用于语音打断"""
            try:
                while True:
                    self._q.get_nowait()
            except queue.Empty:
                pass
            with self._lock:
                self._rb_w = 0
                self._rb_r = 0
                self._rb_len = 0
                self._rb[:] = 0
    
        def _write_rb(self, chunk: np.ndarray):
            n = int(chunk.shape[0])
            if n <= 0:
                return
            overflow = max(0, self._rb_len + n - self._rb_size)
            if overflow > 0:
                self._rb_r = (self._rb_r + overflow) % self._rb_size
                self._rb_len -= overflow
            end = self._rb_size - self._rb_w
            if n <= end:
                self._rb[self._rb_w:self._rb_w + n] = chunk
            else:
                self._rb[self._rb_w:] = chunk[:end]
                self._rb[:n - end] = chunk[end:]
            self._rb_w = (self._rb_w + n) % self._rb_size
            self._rb_len += n
    
        def _read_rb(self, frames: int) -> np.ndarray:
            if self._rb_len <= 0:
                return np.zeros((frames, self.out_channels), dtype=np.int16)
            n = min(frames, self._rb_len)
            out = np.zeros((frames, self.out_channels), dtype=np.int16)
            end = self._rb_size - self._rb_r
            if n <= end:
                out[:n] = self._rb[self._rb_r:self._rb_r + n]
            else:
                out[:end] = self._rb[self._rb_r:]
                out[end:n] = self._rb[:n - end]
            self._rb_r = (self._rb_r + n) % self._rb_size
            self._rb_len -= n
            return out
    
        async def push_frame(self, frame: AudioFrame):
            """接收音频帧，自动合并声道后入队"""
            if self._closed:
                return
            pcm = audioframe_to_s16_samples(frame)
            in_ch = pcm.shape[1]
            if self.out_channels == 1:
                if in_ch == 1:
                    out = pcm
                else:
                    out = np.mean(pcm.astype(np.int32), axis=1).astype(np.int16).reshape(-1, 1)
            else:
                if in_ch == self.out_channels:
                    out = pcm
                elif in_ch == 1 and self.out_channels == 2:
                    out = np.repeat(pcm, 2, axis=1)
                else:
                    out = pcm[:, :self.out_channels]
            try:
                self._q.put_nowait(out)
            except queue.Full:
                try:
                    self._q.get_nowait()
                except queue.Empty:
                    pass
                try:
                    self._q.put_nowait(out)
                except queue.Full:
                    pass
    
        async def close(self):
            self._closed = True
            if self._stream:
                self._stream.stop()
                self._stream.close()
                self._stream = None
    
    # --------------- main ---------------
    
    async def main():
        pc = RTCPeerConnection(RTCConfiguration(iceServers=[]))
    
        # 初始化音频播放器（单声道输出，5ms blocksize 低延迟）
        speaker = RemoteAudioPlayer(samplerate=48000, out_channels=1, blocksize=240, max_seconds=0.2)
        speaker.start()
    
        # 初始化麦克风（macOS avfoundation，Linux 请改为 pulse 或 alsa）
        mic = MediaPlayer("none:0", format="avfoundation",
                          options={"sample_rate": "48000", "channels": "1"})
        if not mic.audio:
            raise RuntimeError("未检测到麦克风，请检查 avfoundation 音频设备索引")
        pc.addTrack(mic.audio)
    
        # 客户端创建 DataChannel（名称可自定义），服务端会通过固定名为 "txt" 的通道推送事件
        pc.createDataChannel("oai-events")
    
        remote_dc = None
        got_first_txt_msg = False
    
        def make_session_update() -> dict:
            """构造 session.update 配置：音色、音频格式、VAD 策略、推理参数"""
            return {
                "type": "session.update",
                "session": {
                    "modalities": ["text", "audio"],
                    "voice": "Tina",
                    # 配置音频输入/输出格式和采样率
                    "audio": {
                        "input": {"format": {"type": "pcm", "sample_rate": 16000}},
                        "output": {"format": {"type": "pcm", "sample_rate": 24000}}
                    },
                    "instructions": "你是一个友好的AI助手。",
                    "turn_detection": {"type": "server_vad", "threshold": 0.5, "silence_duration_ms": 800},
                    "max_tokens": 16384,
                    "temperature": 0.9,
                },
            }
    
        # 处理服务端推送的 DataChannel 事件
        @pc.on("datachannel")
        def on_datachannel(ch):
            nonlocal remote_dc, got_first_txt_msg
            print(f"[DC] 收到服务端 DataChannel: {ch.label}")
            if ch.label == "txt":
                remote_dc = ch
    
            @ch.on("message")
            def on_msg(msg):
                nonlocal got_first_txt_msg
                try:
                    evt = json.loads(msg)
                except Exception:
                    return
                print(f"[{ch.label}] {evt.get('type')}")
    
                # 用户开始说话时清空播放缓存，实现语音打断
                if isinstance(evt, dict) and evt.get("type") == "input_audio_buffer.speech_started":
                    speaker.clear()
                    print("[播放] 检测到用户说话，清空播放缓存（打断）")
    
                # 收到 txt 通道首条消息后发送 session.update 配置会话
                if ch.label == "txt" and not got_first_txt_msg:
                    got_first_txt_msg = True
                    if remote_dc and remote_dc.readyState == "open":
                        remote_dc.send(json.dumps(make_session_update(), ensure_ascii=False))
                        print("[DC] 已发送 session.update")
    
        # 接收服务端音频并通过播放器低延迟输出
        @pc.on("track")
        async def on_track(track):
            if track.kind == "audio":
                async def _play():
                    try:
                        while True:
                            frame = await track.recv()
                            await speaker.push_frame(frame)
                    except Exception:
                        pass
                asyncio.create_task(_play())
    
        @pc.on("iceconnectionstatechange")
        def on_ice():
            print(f"[ICE] {pc.iceConnectionState}")
    
        @pc.on("connectionstatechange")
        async def on_conn():
            print(f"[连接] {pc.connectionState}")
            if pc.connectionState in ("failed", "closed", "disconnected"):
                await pc.close()
    
        # SDP 交换：创建 Offer 并 POST 到信令服务端，获取 Answer
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
                timeout=aiohttp.ClientTimeout(total=10),
            ) as resp:
                if not resp.ok:
                    raise Exception(f"SDP 交换失败: {resp.status} {await resp.text()}")
                answer_sdp = await resp.text()
    
        await pc.setRemoteDescription(RTCSessionDescription(sdp=answer_sdp, type="answer"))
        print("SDP 交换完成，等待连接...")
    
        try:
            await asyncio.Event().wait()
        except (KeyboardInterrupt, asyncio.CancelledError):
            pass
        finally:
            print(f"\n退出。最终状态: 连接={pc.connectionState}, ICE={pc.iceConnectionState}")
            await speaker.close()
            try:
                if mic and mic.audio:
                    mic.audio.stop()
            except Exception:
                pass
            await pc.close()
    
    asyncio.run(main())
    ```
    
    运行 `webrtc_demo.py`，通过麦克风即可与 Qwen-Omni-Realtime 模型实时对话，系统会检测您的音频起始位置并自动发送到服务器，无需您手动发送。
    

#### JavaScript

-   **前提条件**
    -   使用支持 WebRTC 的现代浏览器（Chrome、Edge、Firefox、Safari 等）。
    -   浏览器需要麦克风权限。
    -   浏览器无法直接向服务端发起建立连接的请求（受浏览器跨域安全策略限制），因此需要通过终端执行 curl 命令来完成连接建立。
-   **运行示例**
    
    新建一个 HTML 文件，命名为 `webrtc_demo.html`，并将以下代码复制到文件中：
    
    webrtc\_demo.html
    
    ```
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8" />
        <title>WebRTC Realtime 语音对话</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; background: #f5f7fa; color: #1d2129; padding: 24px; line-height: 1.6; }
    
            .container { max-width: 800px; margin: 0 auto; }
    
            h1 { font-size: 22px; font-weight: 600; margin-bottom: 20px; color: #1d2129; }
    
            /* 顶部吸顶栏 */
            .sticky-top { position: sticky; top: 0; z-index: 100; background: #f5f7fa; margin: 0 -24px 16px; padding: 12px 24px; border-bottom: 1px solid transparent; transition: border-color .2s; }
            .sticky-top.scrolled { border-bottom-color: #e5e6eb; }
    
            /* 控制栏 */
            .toolbar { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; margin-bottom: 12px; }
            .toolbar label { display: flex; align-items: center; gap: 6px; font-size: 13px; color: #4e5969; cursor: pointer; }
    
            /* 按钮 */
            button { padding: 8px 18px; font-size: 13px; font-weight: 500; border: 1px solid #c9cdd4; border-radius: 6px; background: #fff; color: #1d2129; cursor: pointer; transition: all .15s; }
            button:hover:not(:disabled) { border-color: #165dff; color: #165dff; }
            button:disabled { opacity: .4; cursor: not-allowed; }
            .btn-primary { background: #165dff; border-color: #165dff; color: #fff; }
            .btn-primary:hover:not(:disabled) { background: #4080ff; border-color: #4080ff; color: #fff; }
            .btn-danger { border-color: #f53f3f; color: #f53f3f; }
            .btn-danger:hover:not(:disabled) { background: #f53f3f; color: #fff; }
    
            /* 状态指示 */
            .status-bar { display: flex; align-items: center; gap: 8px; padding: 10px 14px; border-radius: 8px; background: #fff; border: 1px solid #e5e6eb; font-size: 13px; }
            .status-dot { width: 8px; height: 8px; border-radius: 50%; background: #c9cdd4; flex-shrink: 0; }
            .status-dot.connected { background: #00b42a; }
            .status-dot.connecting { background: #ff7d00; animation: pulse 1s infinite; }
            .status-dot.error { background: #f53f3f; }
            @keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: .4; } }
    
            /* SDP 卡片 */
            .card { background: #fff; border: 1px solid #e5e6eb; border-radius: 10px; padding: 16px; margin-bottom: 16px; }
            .card-title { font-size: 13px; font-weight: 600; color: #4e5969; margin-bottom: 8px; }
            .step-num { display: inline-flex; align-items: center; justify-content: center; width: 20px; height: 20px; border-radius: 50%; background: #165dff; color: #fff; font-size: 11px; font-weight: 600; margin-right: 6px; }
            .card-hint { font-size: 12px; color: #86909c; margin-top: 6px; }
    
            textarea { width: 100%; font-family: "SF Mono", "Fira Code", "Fira Mono", Menlo, Consolas, monospace; font-size: 12px; padding: 10px; border: 1px solid #e5e6eb; border-radius: 6px; resize: vertical; background: #f7f8fa; color: #1d2129; transition: border-color .15s; }
            textarea:focus { outline: none; border-color: #165dff; background: #fff; }
    
            /* 视频 */
            .video-section { margin-bottom: 16px; }
            .video-label { font-size: 13px; color: #86909c; margin-bottom: 6px; }
            video { width: 320px; max-width: 100%; background: #000; border-radius: 8px; display: block; }
    
            /* 事件面板 */
            .events-title { font-size: 14px; font-weight: 600; color: #1d2129; margin-bottom: 10px; }
            .events-container { display: flex; flex-direction: column; gap: 6px; }
            .event-item { background: #fff; border: 1px solid #e5e6eb; border-radius: 8px; overflow: hidden; }
            .event-header { display: flex; align-items: center; gap: 8px; padding: 8px 12px; cursor: pointer; user-select: none; font-size: 12px; }
            .event-header:hover { background: #f7f8fa; }
            .event-arrow { font-size: 14px; font-weight: 700; width: 18px; text-align: center; }
            .event-arrow.server { color: #00b42a; }
            .event-arrow.client { color: #165dff; }
            .event-label { color: #4e5969; }
            .event-time { color: #c9cdd4; margin-left: auto; font-size: 11px; }
            .event-body { display: none; padding: 10px 12px; background: #f7f8fa; border-top: 1px solid #e5e6eb; }
            .event-body pre { margin: 0; font-size: 11px; font-family: "SF Mono", Menlo, Consolas, monospace; color: #4e5969; white-space: pre-wrap; word-break: break-all; }
            .events-empty { font-size: 13px; color: #c9cdd4; padding: 16px 0; text-align: center; }
        </style>
    </head>
    <body>
    <div class="container">
        <h1>WebRTC Realtime 语音对话</h1>
    
        <div class="sticky-top">
            <div class="toolbar">
                <button id="startBtn" class="btn-primary">开始会话</button>
                <button id="setAnswerBtn" disabled>设置 Answer</button>
                <button id="endBtn" class="btn-danger" disabled>结束会话</button>
                <button id="downloadBtn" disabled>下载远端音频</button>
                <label>
                    <input id="sendVideoCheckbox" type="checkbox" />
                    开启视频
                </label>
            </div>
    
            <div class="status-bar">
                <span class="status-dot" id="statusDot"></span>
                <span id="statusText">就绪</span>
            </div>
        </div>
    
        <div class="card">
            <div class="card-title"><span class="step-num">1</span>Offer SDP</div>
            <div style="margin-bottom: 8px;">
                <button id="copyOfferBtn" disabled>复制 Offer SDP</button>
            </div>
            <textarea id="offerBox" rows="6" readonly placeholder="点击“开始会话”后自动生成"></textarea>
            <div class="card-hint">ICE 收集完成后自动生成，复制后通过 curl 命令发送到服务端获取 Answer</div>
        </div>
    
        <div class="card">
            <div class="card-title"><span class="step-num">2</span>curl 命令</div>
            <div style="margin-bottom: 8px;">
                <button id="copyCurlBtn" disabled>复制 curl 命令</button>
            </div>
            <div class="card-hint" style="margin-bottom: 4px;">以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。</div>
            <textarea id="curlBox" rows="6" placeholder="Offer SDP 生成后自动填充 curl 命令"></textarea>
            <div class="card-hint">请将 {WorkspaceId} 替换为您的业务空间ID后，复制此命令到终端执行，将返回的 Answer SDP 粘贴到下方</div>
        </div>
    
        <div class="card">
            <div class="card-title"><span class="step-num">3</span>Answer SDP</div>
            <textarea id="answerBox" rows="6" placeholder="将 curl 返回的 Answer SDP 粘贴到这里"></textarea>
            <div class="card-hint">粘贴后点击上方"设置 Answer"按钮建立连接</div>
        </div>
    
        <div class="video-section" id="videoSection" style="display:none;">
            <div class="video-label">本端视频预览</div>
            <video id="localVideo" autoplay playsinline muted></video>
        </div>
    
        <div class="events-title">事件（DataChannel）</div>
        <div id="events" class="events-container"></div>
    </div>
    
    <script>
        const eventsDiv = document.getElementById('events');
        const startBtn = document.getElementById('startBtn');
        const setAnswerBtn = document.getElementById('setAnswerBtn');
        const endBtn = document.getElementById('endBtn');
        const downloadBtn = document.getElementById('downloadBtn');
        const copyOfferBtn = document.getElementById('copyOfferBtn');
        const statusDot = document.getElementById('statusDot');
        const statusText = document.getElementById('statusText');
    
        const copyCurlBtn = document.getElementById('copyCurlBtn');
        const curlBox = document.getElementById('curlBox');
    
        const sendVideoCheckbox = document.getElementById('sendVideoCheckbox');
        const localVideo = document.getElementById('localVideo');
    
        const offerBox = document.getElementById('offerBox');
        const answerBox = document.getElementById('answerBox');
    
        let pc = null;
        let hiddenRemoteAudioEl = null;
    
        let mediaRecorder = null;
        let recordedChunks = [];
        let audioBlob = null;
    
        let localStream = null;
    
        let sendCanvas = null;
        let sendCanvasCtx = null;
        let sendCanvasStream = null;
        let sendRafId = 0;
    
        let gatedAudioTracks = [];
        let gatedVideoTracks = [];
        let audioSender = null;
        let videoSender = null;
        let audioTrack = null;
        let videoTrack = null;
    
        function setStatus(text, state) {
          statusText.textContent = text;
          statusDot.className = 'status-dot' + (state ? ' ' + state : '');
        }
    
        function gateMedia(on) {
          for (const t of gatedAudioTracks) t.enabled = !!on;
          for (const t of gatedVideoTracks) t.enabled = !!on;
        }
    
        function sendUpdate(channel) {
          const update = {
            event_id: `event_${Date.now()}`,
            type: "session.update",
            session: {
              // 配置音频输入/输出格式和采样率
              audio: {
                input: { format: { type: "pcm", sample_rate: 16000 } },
                output: { format: { type: "pcm", sample_rate: 24000 } }
              },
              input_audio_transcription: { model: "qwen3-asr-flash-realtime" },
              instructions: "You are a helpful assistant.",
              modalities: ["text", "audio"],
              smooth_output: false,
              turn_detection: {
                prefix_padding_ms: 500,
                silence_duration_ms: 800,
                threshold: 0.5,
                type: "server_vad",
              },
            },
          };
          if (channel && channel.readyState === "open") channel.send(JSON.stringify(update));
        }
    
        // ===== 事件面板 =====
        const events = [];
        function nowTs() { return new Date().toLocaleTimeString(); }
    
        function renderEvents() {
          eventsDiv.innerHTML = "";
          if (events.length === 0) {
            const empty = document.createElement("div");
            empty.className = "events-empty";
            empty.textContent = "等待事件...";
            eventsDiv.appendChild(empty);
            return;
          }
    
          for (const item of events) {
            const { event, timestamp } = item;
            const isClient = event?.type?.includes("update") || event?.type?.includes("create");
    
            const wrap = document.createElement("div");
            wrap.className = "event-item";
    
            const header = document.createElement("div");
            header.className = "event-header";
    
            const arrow = document.createElement("span");
            arrow.className = "event-arrow " + (isClient ? "client" : "server");
            arrow.textContent = isClient ? "↓" : "↑";
    
            const label = document.createElement("span");
            label.className = "event-label";
            const who = isClient ? "client" : "server";
            const type = event?.type ?? "message";
            label.textContent = `${who}: ${type}`;
    
            const time = document.createElement("span");
            time.className = "event-time";
            time.textContent = timestamp;
    
            const body = document.createElement("div");
            body.className = "event-body";
            const pre = document.createElement("pre");
            pre.textContent = JSON.stringify(event, null, 2);
            body.appendChild(pre);
    
            header.onclick = () => { body.style.display = body.style.display === "block" ? "none" : "block"; };
    
            header.appendChild(arrow);
            header.appendChild(label);
            header.appendChild(time);
            wrap.appendChild(header);
            wrap.appendChild(body);
    
            eventsDiv.appendChild(wrap);
          }
        }
    
        function clearUIEvents() { events.length = 0; renderEvents(); }
        function pushEventFromDataChannel(eventObj) {
          const ts = eventObj.timestamp || nowTs();
          if (!eventObj.timestamp) eventObj.timestamp = ts;
          events.unshift({ event: eventObj, timestamp: ts });
          renderEvents();
        }
    
        function normalizeSdpForSetRemote(sdp) {
          sdp = String(sdp).trim().replace(/\r?\n/g, "\r\n");
          if (!sdp.endsWith("\r\n")) sdp += "\r\n";
          return sdp;
        }
    
        // ===== WebRTC =====
        startBtn.onclick = () => startSession().catch(err => console.log("startSession error:", err));
        endBtn.onclick = () => endSession();
        setAnswerBtn.onclick = () => setRemoteAnswerFromUI().catch(err => console.log("setRemoteAnswer error:", err));
        copyOfferBtn.onclick = async () => {
          const txt = offerBox.value;
          if (!txt) return;
          await navigator.clipboard.writeText(txt);
          alert("Offer SDP 已复制");
        };
        copyCurlBtn.onclick = async () => {
          const txt = curlBox.value;
          if (!txt) return;
          await navigator.clipboard.writeText(txt);
          alert("curl 命令已复制，请在终端执行");
        };
        downloadBtn.onclick = () => {
          if (audioBlob) downloadBlob(audioBlob, 'remote-audio.webm');
          else alert('没有可下载的录音数据');
        };
    
        async function startSession() {
          if (pc) return;
    
          pc = new RTCPeerConnection({ iceServers: [] });
          clearUIEvents();
          setStatus('正在获取麦克风权限...', 'connecting');
    
          offerBox.value = "";
          answerBox.value = "";
          curlBox.value = "";
          setAnswerBtn.disabled = true;
          copyOfferBtn.disabled = true;
          copyCurlBtn.disabled = true;
    
          endBtn.disabled = false;
          downloadBtn.disabled = true;
    
          pc.onconnectionstatechange = () => {
            if (!pc) return;
            if (pc.connectionState === 'connected') {
              setStatus('已连接，请说话', 'connected');
            } else if (["failed", "closed", "disconnected"].includes(pc.connectionState)) {
              console.log("onconnectionstatechange:", pc.connectionState);
              endSession(true);
            }
          };
    
          pc.ontrack = async (e) => {
            const stream = e.streams[0];
            ensureHiddenAudioEl();
            hiddenRemoteAudioEl.srcObject = stream;
            try { await hiddenRemoteAudioEl.play(); } catch {}
            startRecordingRemoteStream(stream);
          };
    
          const wantVideo = !!sendVideoCheckbox.checked;
    
          const localPreviewFps = 30;
          const sendFps = 2;
    
          const constraints = wantVideo
            ? {
                audio: true,
                video: {
                  facingMode: { ideal: "user" },
                  frameRate: { ideal: localPreviewFps, max: localPreviewFps },
                  width: { ideal: 640 },
                  height: { ideal: 480 },
                }
              }
            : { audio: true };
    
          localStream = await navigator.mediaDevices.getUserMedia(constraints);
    
          const videoSection = document.getElementById('videoSection');
          if (wantVideo) {
            localVideo.srcObject = localStream;
            localVideo.style.display = "block";
            videoSection.style.display = "";
            try { await localVideo.play(); } catch {}
          } else {
            localVideo.srcObject = null;
            localVideo.style.display = "none";
            videoSection.style.display = "none";
          }
    
          gatedAudioTracks = [];
          gatedVideoTracks = [];
    
          localStream.getAudioTracks().forEach(t => {
            pc.addTrack(t, localStream);
            gatedAudioTracks.push(t);
          });
    
          if (wantVideo) {
            if (sendRafId) cancelAnimationFrame(sendRafId);
            sendRafId = 0;
            if (sendCanvasStream) sendCanvasStream.getTracks().forEach(t => t.stop());
            sendCanvasStream = null;
            sendCanvasCtx = null;
            sendCanvas = null;
    
            const settings = localStream.getVideoTracks()[0].getSettings();
            sendCanvas = document.createElement("canvas");
            sendCanvas.width = settings.width || 640;
            sendCanvas.height = settings.height || 480;
            sendCanvasCtx = sendCanvas.getContext("2d", { alpha: false });
    
            sendCanvasStream = sendCanvas.captureStream(sendFps);
            const lowFpsTrack = sendCanvasStream.getVideoTracks()[0];
            pc.addTrack(lowFpsTrack, sendCanvasStream);
            gatedVideoTracks.push(lowFpsTrack);
    
            const pump = () => {
              if (!sendCanvasCtx || !sendCanvas) return;
              try { sendCanvasCtx.drawImage(localVideo, 0, 0, sendCanvas.width, sendCanvas.height); } catch {}
              sendRafId = requestAnimationFrame(pump);
            };
            sendRafId = requestAnimationFrame(pump);
          }
    
          gateMedia(false);
    
          audioSender = pc.getSenders().find(s => s.track?.kind === 'audio');
          videoSender = pc.getSenders().find(s => s.track?.kind === 'video');
          audioTrack = audioSender?.track;
          videoTrack = videoSender?.track;
    
          await audioSender?.replaceTrack(null);
          await videoSender?.replaceTrack(videoTrack ? null : undefined);
    
          const dc = pc.createDataChannel('oai-events');
    
          dc.onopen = () => console.log("DC open");
          dc.onmessage = (e) => {
            handleDcMessage(e.data, dc);
          };
    
          pc.ondatachannel = (event) => {
            const ch = event.channel;
            ch.onmessage = (e) => {
                handleDcMessage(e.data, ch);
            };
          };
    
          function handleDcMessage(data, channel) {
              let obj;
              try { obj = JSON.parse(data); }
              catch (err) {
                pushEventFromDataChannel({ type: "raw", data: String(data), parseError: String(err) });
                return;
              }
              pushEventFromDataChannel(obj);
    
              if (obj?.type === "session.created") {
                console.log("Session created, opening media gate.");
                gateMedia(true);
                if(audioSender) audioSender.replaceTrack(audioTrack);
                if(videoSender && videoTrack) videoSender.replaceTrack(videoTrack);
    
                sendUpdate(channel);
              }
          }
    
          pc.onicegatheringstatechange = () => {
            if (!pc) return;
            if (pc.iceGatheringState === "complete" && pc.localDescription?.sdp) {
              const sdp = pc.localDescription.sdp;
              offerBox.value = sdp;
              copyOfferBtn.disabled = false;
              setAnswerBtn.disabled = false;
    
              const escapedSdp = sdp.replace(/'/g, "'\\''");
              // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
              curlBox.value = `curl -X POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/webrtc/realtime?model=qwen3.8-omni-flash-realtime' \\\n  -H 'Content-Type: application/sdp' \\\n  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \\\n  --data-binary '${escapedSdp}'`;
              copyCurlBtn.disabled = false;
    
              setStatus('Offer SDP 已生成，复制 curl 命令到终端获取 Answer SDP', 'connecting');
              console.log("ICE Gathering Complete. Ready to set remote description.");
            }
          };
    
          const offer = await pc.createOffer();
          await pc.setLocalDescription(offer);
        }
    
        async function setRemoteAnswerFromUI() {
          if (!pc) return alert('请先点击"开始会话"生成 Offer。');
          const txt = answerBox.value.trim();
          if (!txt) return alert("请粘贴 Answer SDP");
    
          const answerSdp = normalizeSdpForSetRemote(txt);
          try {
              await pc.setRemoteDescription({ type: 'answer', sdp: answerSdp });
              setStatus('正在建立连接...', 'connecting');
          } catch (e) {
              alert("设置 Answer 失败: " + e.message);
              console.error(e);
          }
        }
    
        function endSession(silent = false) {
          if (sendRafId) cancelAnimationFrame(sendRafId);
          sendRafId = 0;
    
          if (sendCanvasStream) {
            sendCanvasStream.getTracks().forEach(t => t.stop());
          }
          sendCanvasStream = null;
          sendCanvasCtx = null;
          sendCanvas = null;
    
          try { if (mediaRecorder && mediaRecorder.state !== "inactive") mediaRecorder.stop(); } catch {}
          mediaRecorder = null;
    
          if (localStream) {
            localStream.getTracks().forEach(t => t.stop());
            localStream = null;
          }
          localVideo.srcObject = null;
          localVideo.style.display = "none";
          document.getElementById('videoSection').style.display = "none";
    
          if (pc) {
            try { pc.close(); } catch {}
            pc = null;
          }
    
          gatedAudioTracks = [];
          gatedVideoTracks = [];
    
          if (hiddenRemoteAudioEl) {
            try { hiddenRemoteAudioEl.pause(); } catch {}
            hiddenRemoteAudioEl.srcObject = null;
            hiddenRemoteAudioEl.remove();
            hiddenRemoteAudioEl = null;
          }
    
          endBtn.disabled = true;
          setAnswerBtn.disabled = true;
          copyOfferBtn.disabled = true;
          copyCurlBtn.disabled = true;
          downloadBtn.disabled = !audioBlob;
    
          setStatus('已断开', '');
          if (!silent) console.log("session ended");
        }
    
        function ensureHiddenAudioEl() {
          if (hiddenRemoteAudioEl) return;
          hiddenRemoteAudioEl = document.createElement("audio");
          hiddenRemoteAudioEl.autoplay = true;
          hiddenRemoteAudioEl.playsInline = true;
          hiddenRemoteAudioEl.muted = false;
          hiddenRemoteAudioEl.style.display = "none";
          document.body.appendChild(hiddenRemoteAudioEl);
        }
    
        function startRecordingRemoteStream(remoteStream) {
          const audioTracks = remoteStream.getAudioTracks();
          if (!audioTracks.length) return;
    
          const audioStream = new MediaStream(audioTracks);
          recordedChunks = [];
          audioBlob = null;
          downloadBtn.disabled = true;
    
          try {
            mediaRecorder = new MediaRecorder(audioStream, { mimeType: 'audio/webm' });
          } catch (err) {
            console.log("MediaRecorder create failed:", err);
            return;
          }
    
          mediaRecorder.ondataavailable = (e) => {
            if (e.data && e.data.size > 0) recordedChunks.push(e.data);
          };
    
          mediaRecorder.onstop = () => {
            audioBlob = new Blob(recordedChunks, { type: 'audio/webm' });
            downloadBtn.disabled = !audioBlob || audioBlob.size === 0;
          };
    
          mediaRecorder.start();
        }
    
        function downloadBlob(blob, filename) {
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.style.display = 'none';
          a.href = url;
          a.download = filename;
          document.body.appendChild(a);
          a.click();
          URL.revokeObjectURL(url);
          a.remove();
        }
    
        renderEvents();
    
        const stickyTop = document.querySelector('.sticky-top');
        window.addEventListener('scroll', () => {
          stickyTop.classList.toggle('scrolled', window.scrollY > 10);
        }, { passive: true });
    </script>
    </body>
    </html>
    ```
    
    在浏览器中打开此文件，按以下步骤操作：
    
    1.  点击**开始会话**，页面会自动生成 Offer SDP 和对应的 curl 命令。
    2.  点击**复制 curl 命令**，在终端中执行。命令返回的内容即为 Answer SDP。
    3.  将 Answer SDP 粘贴到页面的 Answer SDP 文本框中，点击**设置 Answer**即可建立连接并开始语音对话。

## 交互流程

#### VAD 模式

将[session.update](raw/model-api-reference/omni-realtime-api/client-events.md)事件的`session.turn_detection.type` 设为`"server_vad"`或`"semantic_vad"`以[启用 VAD 模式](raw/model-api-reference/omni-realtime-api/client-events.md)。适用于语音通话场景。WebSocket 和 WebRTC 均支持 VAD 模式，两者的服务端事件一致，区别在于音频和图片的传输方式不同。

> WebRTC 仅支持 VAD 模式，不支持 Manual 模式。WebRTC 的音频通过 RTP 直接传输，无需发送 `input_audio_buffer.append` 事件；图片通过视频轨道传输，不支持 `input_image_buffer.append` 事件。控制指令和服务端事件通过 DataChannel 传输，事件类型与 WebSocket 一致。

交互流程如下：

1.  客户端发送音频数据。WebSocket 通过 [input\_audio\_buffer.append](raw/model-api-reference/omni-realtime-api/client-events.md) 事件发送；WebRTC 通过音频轨道（RTP）自动传输，无需手动发送事件。
2.  服务端检测到语音开始，通过 DataChannel（WebRTC）或 WebSocket 发送 [input\_audio\_buffer.speech\_started](raw/model-api-reference/omni-realtime-api/server-events.md) 事件。
3.  服务端检测到语音结束，发送[input\_audio\_buffer.speech\_stopped](https://help.aliyun.com/zh/model-studio/server-events#fd08ffdf0a2mt) 事件。
4.  服务端自动提交音频缓冲区，发送[input\_audio\_buffer.committed](https://help.aliyun.com/zh/model-studio/server-events#bd9bfdc258afy) 事件。
5.  服务端开始生成响应，依次发送 [response.created](raw/model-api-reference/omni-realtime-api/server-events.md)、[conversation.item.created](raw/model-api-reference/omni-realtime-api/server-events.md) 等事件。模型的音频回复通过 WebSocket 的 `response.audio.delta` 事件增量返回，或通过 WebRTC 的音频轨道（RTP）直接传输。
6.  响应过程中，服务端通过 `response.audio_transcript.delta` 事件增量返回文字转录，最终发送 `response.done` 事件标志响应完成。

**生命周期**

**客户端事件**

**服务端事件**

会话初始化

[session.update](raw/model-api-reference/omni-realtime-api/client-events.md)

> 会话配置

[session.created](raw/model-api-reference/omni-realtime-api/server-events.md)

> 会话已创建

[session.updated](https://help.aliyun.com/zh/model-studio/server-events#424ef2e774q9p)

> 会话配置已更新

用户音频输入

[input\_audio\_buffer.append](raw/model-api-reference/omni-realtime-api/client-events.md)

> WebSocket：通过此事件添加音频到缓冲区

[input\_image\_buffer.append](raw/model-api-reference/omni-realtime-api/client-events.md)

> WebSocket：通过此事件添加图片到缓冲区

> WebRTC：音频通过 RTP 音频轨道自动传输，图片通过视频轨道传输，无需发送上述事件。

[input\_audio\_buffer.speech\_started](raw/model-api-reference/omni-realtime-api/server-events.md)

> 检测到语音开始

[input\_audio\_buffer.speech\_stopped](https://help.aliyun.com/zh/model-studio/server-events#fd08ffdf0a2mt)

> 检测到语音结束

[input\_audio\_buffer.committed](https://help.aliyun.com/zh/model-studio/server-events#bd9bfdc258afy)

> 服务器收到提交的音频

服务器音频输出

无

[response.created](raw/model-api-reference/omni-realtime-api/server-events.md)

> 服务端开始生成响应

[response.output\_item.added](https://help.aliyun.com/zh/model-studio/server-events#dae2260d40qtu)

> 响应时有新的输出内容

[conversation.item.created](raw/model-api-reference/omni-realtime-api/server-events.md)

> 对话项被创建

[response.content\_part.added](https://help.aliyun.com/zh/model-studio/server-events#de7fa0b877j25)

> 新的输出内容添加到assistant message

[response.audio\_transcript.delta](https://help.aliyun.com/zh/model-studio/server-events#35396453cfood)

> 增量生成的转录文字

[response.audio.delta](https://help.aliyun.com/zh/model-studio/server-events#a25cc50a15car)

> WebSocket：模型增量生成的音频通过此事件返回。WebRTC：音频通过 RTP 音频轨道直接传输，不返回此事件。

[response.audio\_transcript.done](https://help.aliyun.com/zh/model-studio/server-events#f4d1698567bsm)

> 文本转录完成

[response.audio.done](https://help.aliyun.com/zh/model-studio/server-events#9e8eb59c67qnt)

> 音频生成完成

[response.content\_part.done](https://help.aliyun.com/zh/model-studio/server-events#011ad54242wft)

> Assistant message 的文本或音频内容流式输出完成

[response.output\_item.done](https://help.aliyun.com/zh/model-studio/server-events#f580421f45w3h)

> Assistant message 的整个输出项流式传输完成

[response.done](https://help.aliyun.com/zh/model-studio/server-events#f2333c777d9s4)

> 响应完成

`conversation.item.input_audio_transcription.delta`

> 用户语音输入的文字流式转录（需在 session.update 中启用 input\_audio\_transcription）

`conversation.item.input_audio_transcription.completed`

> 用户语音输入的文字转录完成（需在 session.update 中启用 input\_audio\_transcription）

#### Manual 模式

将[session.update](raw/model-api-reference/omni-realtime-api/client-events.md)事件的`session.turn_detection` 设为 `null` 以启用 Manual 模式。此模式下，客户端通过显式发送`input_audio_buffer.commit` 和`response.create`事件请求服务器响应。适用于按下即说场景，如聊天软件中的发送语音。

交互流程如下：

1.  客户端随时发送 [input\_audio\_buffer.append](raw/model-api-reference/omni-realtime-api/client-events.md)与[input\_image\_buffer.append](raw/model-api-reference/omni-realtime-api/client-events.md)事件追加音频与图片至缓冲区。
    
    > 发送 input\_image\_buffer.append 事件前，至少发送过一次 input\_audio\_buffer.append 事件。
    
2.  客户端发送[input\_audio\_buffer.commit](https://help.aliyun.com/zh/model-studio/client-events#1cbea5fa7fkfl)事件提交音频缓冲区与图像缓冲区，告知服务端本轮的用户输入（音频及图片）已全部发送完毕。
    
3.  服务端响应 [input\_audio\_buffer.committed](https://help.aliyun.com/zh/model-studio/server-events#bd9bfdc258afy)事件。
    
4.  客户端发送[response.create](raw/model-api-reference/omni-realtime-api/client-events.md)事件，等待服务端返回模型的输出。
    
5.  服务端响应[conversation.item.created](raw/model-api-reference/omni-realtime-api/server-events.md)事件。
    

**生命周期**

**客户端事件**

**服务端事件**

会话初始化

[session.update](raw/model-api-reference/omni-realtime-api/client-events.md)

> 会话配置

[session.created](raw/model-api-reference/omni-realtime-api/server-events.md)

> 会话已创建

[session.updated](https://help.aliyun.com/zh/model-studio/server-events#424ef2e774q9p)

> 会话配置已更新

用户音频输入

[input\_audio\_buffer.append](raw/model-api-reference/omni-realtime-api/client-events.md)

> 添加音频到缓冲区

[input\_image\_buffer.append](raw/model-api-reference/omni-realtime-api/client-events.md)

> 添加图片到缓冲区

[input\_audio\_buffer.commit](https://help.aliyun.com/zh/model-studio/client-events#1cbea5fa7fkfl)

> 提交音频与图片到服务器

[response.create](raw/model-api-reference/omni-realtime-api/client-events.md)

> 创建模型响应

[input\_audio\_buffer.committed](https://help.aliyun.com/zh/model-studio/server-events#bd9bfdc258afy)

> 服务器收到提交的音频

服务器音频输出

[input\_audio\_buffer.clear](https://help.aliyun.com/zh/model-studio/client-events#3b44f2f2abakw)

> 清除缓冲区的音频

[response.created](raw/model-api-reference/omni-realtime-api/server-events.md)

> 服务端开始生成响应

[response.output\_item.added](https://help.aliyun.com/zh/model-studio/server-events#dae2260d40qtu)

> 响应时有新的输出内容

[conversation.item.created](raw/model-api-reference/omni-realtime-api/server-events.md)

> 对话项被创建

[response.content\_part.added](https://help.aliyun.com/zh/model-studio/server-events#de7fa0b877j25)

> 新的输出内容添加到assistant message 项

[response.audio\_transcript.delta](https://help.aliyun.com/zh/model-studio/server-events#35396453cfood)

> 增量生成的转录文字

[response.audio.delta](https://help.aliyun.com/zh/model-studio/server-events#a25cc50a15car)

> 模型增量生成的音频

[response.audio\_transcript.done](https://help.aliyun.com/zh/model-studio/server-events#f4d1698567bsm)

> 完成文本转录

[response.audio.done](https://help.aliyun.com/zh/model-studio/server-events#9e8eb59c67qnt)

> 完成音频生成

[response.content\_part.done](https://help.aliyun.com/zh/model-studio/server-events#011ad54242wft)

> Assistant message 的文本或音频内容流式输出完成

[response.output\_item.done](https://help.aliyun.com/zh/model-studio/server-events#f580421f45w3h)

> Assistant message 的整个输出项流式传输完成

[response.done](https://help.aliyun.com/zh/model-studio/server-events#f2333c777d9s4)

> 响应完成

## 联网搜索

联网搜索功能使模型能够基于实时检索数据进行回复，适用于股票价格、天气预报等需要即时信息的场景。模型可自主判断是否需要搜索来回应用户的即时问题。

> Qwen3.8-Omni-Flash-Realtime 和 Qwen3.5-Omni-Realtime 系列模型支持联网搜索，且默认关闭，需通过 `session.update` 事件启用。

> 计费请参考[计费说明](https://help.aliyun.com/zh/model-studio/web-search#92ce83df3a599)中的`agent`策略。

### 启用方式

在 `session.update` 事件中添加以下参数：

-   `enable_search`：设置为 `true` 启用联网搜索功能。
-   `search_options.enable_source`：设置为 `true` 返回搜索结果来源列表。

参数详情请参见[session.update](https://help.aliyun.com/zh/model-studio/client-events#26a8302028sjm)。

### 响应格式

启用联网搜索后，`response.done` 事件中的 `usage` 会新增 `plugins` 字段，用于记录搜索计量信息：

```
{
    "usage": {
        "total_tokens": 2937,
        "input_tokens": 2554,
        "output_tokens": 383,
        "input_tokens_details": {
            "text_tokens": 2512,
            "audio_tokens": 42
        },
        "output_tokens_details": {
            "text_tokens": 90,
            "audio_tokens": 293
        },
        "plugins": {
            "search": {
                "count": 1,
                "strategy": "agent"
            }
        }
    }
}
```

### 代码示例

以下示例展示如何在实时对话中启用联网搜索功能。

#### DashScope Python SDK

在 `update_session` 调用中传入 `enable_search` 和 `search_options` 参数：

```
import os
import base64
import time
import json
import pyaudio
from dashscope.audio.qwen_omni import MultiModality, AudioFormat, OmniRealtimeCallback, OmniRealtimeConversation
import dashscope

dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
url = 'wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime'
model = 'qwen3.8-omni-flash-realtime'
voice = 'Tina'

class SearchCallback(OmniRealtimeCallback):
    def __init__(self, pya):
        self.pya = pya
        self.out = None
    def on_open(self):
        self.out = self.pya.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)
    def on_event(self, response):
        if response['type'] == 'response.audio.delta':
            self.out.write(base64.b64decode(response['delta']))
        elif response['type'] == 'conversation.item.input_audio_transcription.delta':
            preview = response.get('text', '') + response.get('stash', '')
            print(f"\r[User] {preview}", end='', flush=True)
        elif response['type'] == 'conversation.item.input_audio_transcription.completed':
            print(f"\r[User] {response['transcript']}")
        elif response['type'] == 'response.audio_transcript.done':
            print(f"[LLM] {response['transcript']}")
        elif response['type'] == 'response.done':
            usage = response.get('response', {}).get('usage', {})
            plugins = usage.get('plugins', {})
            if plugins.get('search'):
                print(f"[Search] count={plugins['search']['count']}, strategy={plugins['search']['strategy']}")

pya = pyaudio.PyAudio()
callback = SearchCallback(pya)
conv = OmniRealtimeConversation(model=model, callback=callback, url=url)
conv.connect()
conv.update_session(
    output_modalities=[MultiModality.AUDIO, MultiModality.TEXT],
    voice=voice,
    instructions="你是个人助理小云",
    enable_search=True,
    search_options={'enable_source': True}
)
mic = pya.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True)
print("联网搜索已启用，对着麦克风说话 (Ctrl+C 退出)...")
try:
    while True:
        audio_data = mic.read(3200, exception_on_overflow=False)
        conv.append_audio(base64.b64encode(audio_data).decode())
        time.sleep(0.01)
except KeyboardInterrupt:
    conv.close()
    mic.close()
    callback.out.close()
    pya.terminate()
    print("\n对话结束")
```

#### DashScope Java SDK

在 `updateSession` 中通过 `parameters` 传入联网搜索配置：

```
import com.alibaba.dashscope.audio.omni.*;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.google.gson.JsonObject;
import javax.sound.sampled.*;
import java.nio.ByteBuffer;
import java.util.*;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.atomic.AtomicBoolean;

public class OmniSearch {
    static class SequentialAudioPlayer {
        private final SourceDataLine line;
        private final Queue<byte[]> audioQueue = new ConcurrentLinkedQueue<>();
        private final Thread playerThread;
        private final AtomicBoolean shouldStop = new AtomicBoolean(false);

        public SequentialAudioPlayer() throws LineUnavailableException {
            AudioFormat format = new AudioFormat(24000, 16, 1, true, false);
            line = AudioSystem.getSourceDataLine(format);
            line.open(format);
            line.start();
            playerThread = new Thread(() -> {
                while (!shouldStop.get()) {
                    byte[] audio = audioQueue.poll();
                    if (audio != null) {
                        line.write(audio, 0, audio.length);
                    } else {
                        try { Thread.sleep(10); } catch (InterruptedException ignored) {}
                    }
                }
            }, "AudioPlayer");
            playerThread.start();
        }

        public void play(String base64Audio) {
            audioQueue.add(Base64.getDecoder().decode(base64Audio));
        }
        public void close() {
            shouldStop.set(true);
            try { playerThread.join(1000); } catch (InterruptedException ignored) {}
            line.drain();
            line.close();
        }
    }

    public static void main(String[] args) {
        try {
            SequentialAudioPlayer player = new SequentialAudioPlayer();
            AtomicBoolean shouldStop = new AtomicBoolean(false);

            OmniRealtimeParam param = OmniRealtimeParam.builder()
                    .model("qwen3.8-omni-flash-realtime")
                    .apikey(System.getenv("DASHSCOPE_API_KEY"))
                    // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
                    .url("wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime")
                    .build();

            OmniRealtimeConversation conversation = new OmniRealtimeConversation(param, new OmniRealtimeCallback() {
                @Override public void onOpen() {
                    System.out.println("连接已建立");
                }
                @Override public void onClose(int code, String reason) {
                    System.out.println("连接已关闭");
                    shouldStop.set(true);
                }
                @Override public void onEvent(JsonObject event) {
                    String type = event.get("type").getAsString();
                    if ("response.audio.delta".equals(type)) {
                        player.play(event.get("delta").getAsString());
                    } else if ("response.audio_transcript.done".equals(type)) {
                        System.out.println("[LLM] " + event.get("transcript").getAsString());
                    } else if ("response.done".equals(type)) {
                        JsonObject response = event.getAsJsonObject("response");
                        if (response != null && response.has("usage")) {
                            JsonObject usage = response.getAsJsonObject("usage");
                            if (usage.has("plugins")) {
                                JsonObject plugins = usage.getAsJsonObject("plugins");
                                if (plugins.has("search")) {
                                    JsonObject search = plugins.getAsJsonObject("search");
                                    System.out.println("[Search] count=" + search.get("count").getAsInt()
                                            + ", strategy=" + search.get("strategy").getAsString());
                                }
                            }
                        }
                    }
                }
            });

            conversation.connect();
            conversation.updateSession(OmniRealtimeConfig.builder()
                    .modalities(Arrays.asList(OmniRealtimeModality.AUDIO, OmniRealtimeModality.TEXT))
                    .voice("Tina")
                    .enableTurnDetection(true)
                    .enableInputAudioTranscription(true)
                    .parameters(Map.of(
                            "instructions", "你是个人助理小云",
                            "enable_search", true,
                            "search_options", Map.of("enable_source", true)
                    ))
                    .build()
            );

            System.out.println("联网搜索已启用，请开始说话（按Ctrl+C退出）...");
            AudioFormat format = new AudioFormat(16000, 16, 1, true, false);
            TargetDataLine mic = AudioSystem.getTargetDataLine(format);
            mic.open(format);
            mic.start();

            ByteBuffer buffer = ByteBuffer.allocate(3200);
            while (!shouldStop.get()) {
                int bytesRead = mic.read(buffer.array(), 0, buffer.capacity());
                if (bytesRead > 0) {
                    byte[] chunk = new byte[bytesRead];
                    System.arraycopy(buffer.array(), 0, chunk, 0, bytesRead);
                    conversation.appendAudio(Base64.getEncoder().encodeToString(chunk));
                }
                Thread.sleep(20);
            }

            conversation.close(1000, "正常结束");
            player.close();
            mic.close();
        } catch (NoApiKeyException e) {
            System.err.println("未找到API KEY: 请设置环境变量 DASHSCOPE_API_KEY");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

#### WebSocket（Python）

在 `session.update` 的 JSON 中添加 `enable_search` 和 `search_options` 字段：

```
import json
import os
import websocket
import base64
import pyaudio
import threading

API_KEY = os.getenv("DASHSCOPE_API_KEY")
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
API_URL = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime?model=qwen3.8-omni-flash-realtime"

pya = pyaudio.PyAudio()
out_stream = pya.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)

def on_open(ws):
    ws.send(json.dumps({
        "type": "session.update",
        "session": {
            "modalities": ["text", "audio"],
            "voice": "Tina",
            "instructions": "你是个人助理小云",
            # 配置音频输入/输出格式和采样率
            "audio": {
                "input": {"format": {"type": "pcm", "sample_rate": 16000}},
                "output": {"format": {"type": "pcm", "sample_rate": 24000}}
            },
            "enable_search": True,
            "search_options": {
                "enable_source": True
            }
        }
    }))
    print("联网搜索已启用，对着麦克风说话...")
    def send_audio():
        mic = pya.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True)
        try:
            while True:
                audio = mic.read(3200, exception_on_overflow=False)
                ws.send(json.dumps({
                    "type": "input_audio_buffer.append",
                    "audio": base64.b64encode(audio).decode()
                }))
        except Exception:
            mic.close()
    threading.Thread(target=send_audio, daemon=True).start()

def on_message(ws, message):
    event = json.loads(message)
    if event["type"] == "response.audio.delta":
        out_stream.write(base64.b64decode(event["delta"]))
    elif event["type"] == "response.audio_transcript.done":
        print(f"[LLM] {event['transcript']}")
    elif event["type"] == "response.done":
        usage = event.get("response", {}).get("usage", {})
        plugins = usage.get("plugins", {})
        if plugins.get("search"):
            print(f"[Search] count={plugins['search']['count']}, strategy={plugins['search']['strategy']}")

def on_error(ws, error):
    print(f"Error: {error}")

headers = ["Authorization: Bearer " + API_KEY]
ws = websocket.WebSocketApp(API_URL, header=headers, on_open=on_open, on_message=on_message, on_error=on_error)
ws.run_forever()
```

## API 参考

-   [客户端事件](raw/model-api-reference/omni-realtime-api/client-events.md)
-   [服务端事件](raw/model-api-reference/omni-realtime-api/server-events.md)
-   [AOQ客户端API](raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)
-   [Realtime API 概述](raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)（WebRTC 协议说明）

## 计费与限流

### 计费规则

Qwen-Omni-Realtime 模型根据不同模态（音频、图像）对应的Token数计费。计费详情请参见百炼控制台。

输出语音时，`qwen3.8-omni-flash-realtime` 的音频及对应文本分别按音频输出和文本输出单价计费；Qwen3.5-Omni-Realtime 系列仅对音频计费，对应文本不计费。

MCP 工具调用不额外收费，模型推理仍按模型价格计费。MCP 的调用流程与使用限制见[MCP 交互流程](https://help.aliyun.com/zh/model-studio/omni-realtime-interaction-process#qwen38-mcp-flow)。

**说明**在多轮实时对话中，模型每次生成响应时，需要将上下文窗口内的所有历史对话内容（包括之前各轮的音频、图片和文本）与本轮新增输入一并作为输入 Token 进行处理。因此，输入 Token 会随对话轮次的增加而逐轮累积，而非仅计算当前轮次的新增输入。

例如，假设一段 10 秒的音频输入转换为 70 个 Token（Qwen3.5-Omni-Realtime 系列模型），在第 3 轮对话时，该音频仍在上下文窗口内，则它依然会被计入第 3 轮的输入 Token。实际计费的输入 Token 数 = 上下文窗口内所有历史轮次的内容 Token 数 + 本轮新增输入的 Token 数。

音频、图片、视频转换为Token数的规则

#### 音频

-   Qwen3.8-Omni-Flash-Realtime、Qwen3.5-Omni-Realtime 系列模型：
    
    -   输入音频计算公式：`总 Token 数 = 音频时长（单位：秒）* 7`
    -   输出音频计算公式：`总 Tokens 数 = 音频时长（单位：秒）* 12.5`
-   Qwen3-Omni-Flash-Realtime系列模型：输入与输出音频的计算公式均为`总 Token 数 = 音频时长（单位：秒）* 12.5`
    
-   Qwen-Omni-Turbo-Realtime系列模型：输入与输出音频的计算公式均为`总 Token 数 = 音频时长（单位：秒）* 25`
    
    若音频时长不足1秒，则按 1 秒计算。
    

`qwen3.8-omni-flash-realtime` 开启空间音频输入时，音频输入 Token 数为普通音频的 2 倍，2 通道和 4 通道的倍数相同。

#### 图片

-   `qwen3.8-omni-flash-realtime`、Qwen3.5-Omni-Realtime 系列模型：每 `32x32` 像素对应 1 个 Token
-   Qwen3-Omni-Flash-Realtime系列模型**：**每`32x32`像素对应 1 个 Token
-   Qwen-Omni-Turbo-Realtime系列模型：每`28x28`像素对应 1 个 Token

一张图最少需要 4 个 Token，最多支持 1280 个 Token；可使用以下代码，传入图像路径和会话时长即可估算图片消耗的 Token 总量：

```
# 使用以下命令安装Pillow库：pip install Pillow
from PIL import Image
import math

# Qwen-Omni-Turbo-Realtime系列模型，缩放因子为28
# factor = 28
# Qwen3.8-Omni-Flash-Realtime、Qwen3.5-Omni-Realtime、Qwen3-Omni-Flash-Realtime系列模型，缩放因子为32
factor = 32

def token_calculate(image_path='', duration=10):
    """
    :param image_path: 图像路径
    :param duration: 会话连接时长
    :return: 图像的Token数
    """
    if len(image_path) > 0:
        # 打开指定的PNG图片文件
        image = Image.open(image_path)
        # 获取图片的原始尺寸
        height = image.height
        width = image.width
        print(f"缩放前的图像尺寸为：高度为{height}，宽度为{width}")
        # 将高度调整为factor的整数倍
        h_bar = round(height / factor) * factor
        # 将宽度调整为factor的整数倍
        w_bar = round(width / factor) * factor
        # 图像的Token下限：4个Token
        min_pixels = factor * factor * 4
        # 图像的Token上限：1280个Token
        max_pixels = 1280 * factor * factor
        # 对图像进行缩放处理，调整像素的总数在范围[min_pixels,max_pixels]内
        if h_bar * w_bar > max_pixels:
            # 计算缩放因子beta，使得缩放后的图像总像素数不超过max_pixels
            beta = math.sqrt((height * width) / max_pixels)
            # 重新计算调整后的高度，确保为factor的整数倍
            h_bar = math.floor(height / beta / factor) * factor
            # 重新计算调整后的宽度，确保为factor的整数倍
            w_bar = math.floor(width / beta / factor) * factor
        elif h_bar * w_bar < min_pixels:
            # 计算缩放因子beta，使得缩放后的图像总像素数不低于min_pixels
            beta = math.sqrt(min_pixels / (height * width))
            # 重新计算调整后的高度，确保为factor的整数倍
            h_bar = math.ceil(height * beta / factor) * factor
            # 重新计算调整后的宽度，确保为factor的整数倍
            w_bar = math.ceil(width * beta / factor) * factor
        print(f"缩放后的图像尺寸为：高度为{h_bar}，宽度为{w_bar}")
        # 计算图像的Token数：总像素除以factor * factor
        token = int((h_bar * w_bar) / (factor * factor))
        print(f"缩放后的token数量为：{token}")
        total_token = token * math.ceil(duration / 2)
        print(f"总Token数为：{total_token}")
        return total_token
    else:
        print("错误：image_path参数为空，无法计算Token数")
        return 0

if __name__ == "__main__":
    total_token = token_calculate(image_path="xxx/test.jpg", duration=10)
```

#### 视频

`qwen3.8-omni-flash-realtime` 的视频基础计量沿用 Qwen3.5-Omni-Realtime，视频画面的像素换算见[图片 Token 规则](#realtime-image-tokens)。

`qwen3.8-omni-flash-realtime` 的视频输入在 `representation_compact="normal"` 时，视频 Token 数为未开启聚合时的 1/4。

### 限流

模型限流规则请参见[限流](raw/model-user-guide/get-started-with-models/rate-limit.md)。

## 常见问题

### 如何在线体验 Qwen-Omni-Realtime 模型？

A：您可以通过以下方式一键部署：

1.  访问[函数计算模板](https://fcnext.console.aliyun.com/applications/create?template=omni-realtime@dev)，**部署类型**选择**直接部署**，**百炼 API-KEY** 填入您的 API Key；单击**创建并部署默认环境**。
2.  等待约一分钟，在**环境详情**的**环境信息**中获取**访问域名**，**将访问域名的**`http`**改成**`https`（示例：[](https://omni-realtime.fcv3.xxxx.cn-hangzhou.fc.devsapp.net)[https://omni-realtime.fcv3.xxxx.cn-hangzhou.fc.devsapp.net](https://omni-realtime.fcv3.xxxx.cn-hangzhou.fc.devsapp.net)），修改后的 HTTPS 链接指向一个可在线体验的 Web 应用，可通过它与模型进行实时视频或语音通话。

**重要**此链接使用自签名证书，仅用于临时测试。首次访问时，浏览器会显示安全警告，这是预期行为，**请勿在生产环境使用**。如需继续，请按浏览器提示操作（如点击“高级” → “继续前往（不安全）”）。

> 通过**资源信息**\-**函数资源**查看项目源代码。

> [函数计算](https://help.aliyun.com/zh/functioncompute/trial-quota-1)与[阿里云百炼](raw/model-user-guide/test-1/new-free-quota.md)均为新用户提供免费额度，可以覆盖简单调试所需成本，额度耗尽后按量计费。只有在访问的情况下会产生费用。

### 怎么向模型输入图片？

A：输入方式取决于接入协议。

**WebSocket**：通过客户端发送[input\_image\_buffer.append](https://help.aliyun.com/zh/model-studio/client-events#c28ed38410nfw)事件。

-   VAD 模式
    
    该模式会根据语音检测情况自动提交音频与图片，请在服务端响应[input\_audio\_buffer.speech\_stopped](https://help.aliyun.com/zh/model-studio/server-events#fd08ffdf0a2mt)前发送[input\_image\_buffer.append](https://help.aliyun.com/zh/model-studio/client-events#c28ed38410nfw)事件。
    
-   Manual 模式
    
    参见[Manual 模式](raw/model-user-guide/model-experience/omni-modal/realtime.md)代码，将图片输入与提交的两部分代码取消注释，即可传入本地图片。
    

**WebRTC**：通过视频轨道（RTP）发送画面帧，无需发送 `input_image_buffer.append` 事件。

若用于视频通话场景，可以对视频抽帧，建议以 1张/秒 的频率向服务端发送图像。[input\_image\_buffer.append](https://help.aliyun.com/zh/model-studio/client-events#c28ed38410nfw) 事件。 DashScope SDK 代码请参见[Omni-Realtime 示例代码](https://github.com/aliyun/alibabacloud-bailian-speech-demo/tree/master/samples/conversation/omni)。

### 收不到 ASR 转录文本（transcript）怎么办？

A：如果您收不到 `conversation.item.input_audio_transcription.completed` 事件，或事件中的 transcript 字段为空，请按以下顺序排查。

1.  **确认已开启输入音频转录**。转录事件由 `session.update` 的 `enable_input_audio_transcription` 参数控制，该参数默认为 `true`。关闭该参数后，服务端不会下发 `conversation.item.input_audio_transcription.completed` 事件，这是预期行为，并非异常，请确认会话配置中该参数为 `true`。
2.  **监听转录失败事件**。除 `completed` 事件外，请同时监听 `conversation.item.input_audio_transcription.failed` 事件。转录失败时，该事件会通过 `error.code`、`error.message` 和 `error.param` 返回失败原因，可据此定位是参数问题还是音频问题。
3.  **升级 DashScope SDK**。较低版本的 DashScope SDK 可能不支持输入音频转录相关参数，导致配置未生效，请将 DashScope SDK 升级到较新版本后重试。
4.  **检查 VAD 配置与网络**。语音活动检测由 `session.turn_detection` 配置，`type` 取值为 `server_vad` 或 `semantic_vad`。VAD 灵敏度与实际环境不匹配（例如在嘈杂环境中阈值过低）会导致音频分段异常，进而影响转录结果，可参见本文档“2. 配置会话”章节调整 `threshold` 与 `silence_duration_ms`。此外，网络不稳定会造成 WebSocket 连接中断，导致转录事件丢失，请确认连接在整个会话期间保持稳定。
5.  **显式指定转录模型**。可通过 `session.update` 的 `input_audio_transcription_model` 参数指定 ASR 转录模型（例如 `qwen3-asr-flash-realtime`）。未显式指定时，服务端使用默认转录模型；当默认模型的转录效果不满足需求时，建议显式指定。

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。

## 音色列表

Qwen-Omni-Realtime模型的音色列表可参见[音色列表](raw/model-user-guide/model-experience/omni-modal/omni-voice-list.md)。
