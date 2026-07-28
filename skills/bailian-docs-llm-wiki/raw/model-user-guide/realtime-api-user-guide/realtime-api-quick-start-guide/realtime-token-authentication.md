# Token鉴权

介绍 Realtime API 的 Token 鉴权机制，包括 API Key 的获取方式以及 WebSocket、WebRTC、AOQ 三种协议的建连鉴权方法。

## **概述**

Realtime API 使用 **API Key** 进行身份认证。无论您选择 WebSocket、WebRTC 还是 AOQ 协议接入，均通过 HTTP 请求头中的 `Authorization` 字段携带 Bearer Token 完成身份验证。

鉴权发生在**建连阶段**，连接建立后的音视频/数据传输无需重复鉴权。

三种协议的鉴权差异：

**协议**

**鉴权时机**

**鉴权方式**

**说明**

WebSocket

WebSocket 连接握手时

HTTP Header `Authorization: Bearer <API_KEY>`

客户端或服务端直接携带 API Key 建连

WebRTC

SDP 交换 HTTP 请求时

HTTP Header `Authorization: Bearer <API_KEY>`

客户端或服务端携带 API Key 发起 SDP 交换

AOQ

业务 AppServer 请求网关时

HTTP Header `Authorization: Bearer <API_KEY>`

API Key 仅在服务端使用，客户端使用网关返回的 Token

## **获取 API Key**

### **步骤 1：开通百炼服务**

1.  访问[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing#/home)并登录您的阿里云账号。
    
2.  如果是首次使用，按照页面提示完成服务开通。
    

### **步骤 2：创建 API Key**

1.  在控制台左侧导航栏中，选择 **API Key 管理**。
    
2.  点击 **创建 API Key**，选择关联的业务空间。
    
3.  创建完成后，请**立即复制并妥善保存** API Key。
    

**重要**

**安全提示**：API Key 是您访问服务的唯一凭证，请勿将其硬编码到客户端代码中或提交到代码仓库。建议通过环境变量或后端服务下发的方式管理。

## **建连鉴权详解**

### **AOQ 协议鉴权**

AOQ 采用**服务端代理鉴权**模式：API Key 仅在业务 AppServer 侧使用，客户端使用网关返回的临时 Token 建连，避免 API Key 暴露在客户端。

![Token鉴权](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3935914871/p1088069.jpg)

#### **百炼网关请求 curl 示例**

```
curl -X POST \
  "https://{endpoint}/api/v1/webrtc/realtime?model=qwen3.5-omni-plus-realtime" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  -H "x-dashscope-rtc-transport: moq" \
  -d '{"clientIp": ${客户端真实IP}}'
```

#### **请求字段说明**

**配置项**

**值**

**说明**

endpoint

根据业务情况选择接入域名

指定对应的接入域名，详情请参见[选择地域、服务部署范围和接入域名](https://help.aliyun.com/zh/model-studio/regions/)

Content-Type

`application/json`

\-

Authorization

`Bearer <API_KEY>`

必填

x-dashscope-rtc-transport

`moq`

**指定使用 AOQ 协议**

clientIp

选填。客户端真实公网 IP

不填写时，使用请求百炼网关的 IP 作为客户端 IP；若填写，则以 clientIp 作为客户端 IP。Realtime API 会参考客户端 IP 提供最佳的 Relay 接入点信息

#### **响应示例**

```
{
    "sid": "1d06b55683db49bba67a407902f62d02:1782706970:69aecdc5...",
    "aoqTokenForClient": "ecc1a46015d5496ca4ff7a48281eb739",
    "clientRelayEndpoints": [{"endpoint": "121.199.XX.XX", "port": 8443}],
    "clientRelayCertFingerprint": "sha256/99843495...",
    "sidExpiresInSecs": 7200,
    "extraInfo": {"workspaceIdHash": "2021b6f98cea4cff"}
}
```

#### **响应字段说明**

**字段**

**说明**

sid

会话唯一标识

aoqTokenForClient

客户端连接令牌，传给 SDK 的 token 字段

clientRelayEndpoints

Relay 接入点数组（endpoint + port）

clientRelayCertFingerprint

Relay TLS 证书指纹

sidExpiresInSecs

会话过期时间（秒）

extraInfo.workspaceIdHash

工作区 ID 哈希

#### **AOQ Client SDK 连接示例**

## **iOS (Swift)**

```
let resp = try JSONDecoder().decode(AllocateResponse.self, from: responseData)

let config = AoqConnectConfig()
config.token = resp.aoqTokenForClient
config.sid = resp.sid
config.certFingerprint = resp.clientRelayCertFingerprint
config.relayEndpoints = resp.clientRelayEndpoints.map { item in
    let ep = AoqRelayEndpoint()
    ep.endpoint = item.endpoint
    ep.port = item.port
    return ep
}
config.workspaceIdHash = resp.extraInfo?.workspaceIdHash ?? ""

let audioTrack = AoqTrackParam()
audioTrack.trackType = .audio
let dataTrack = AoqTrackParam()
dataTrack.trackType = .data
config.publishTracks = [audioTrack, dataTrack]
config.subscribeTracks = [audioTrack, dataTrack]

engine.connect(config)
```

## **Android (Java)**

```
JSONObject obj = new JSONObject(responseText);
AoqClientEngine.AoqConnectConfig cfg = new AoqClientEngine.AoqConnectConfig();
cfg.token = obj.optString("aoqTokenForClient", "");
cfg.sid = obj.optString("sid", "");
cfg.certFingerprint = obj.optString("clientRelayCertFingerprint", "");

JSONArray arr = obj.optJSONArray("clientRelayEndpoints");
if (arr != null) {
    for (int i = 0; i < arr.length(); i++) {
        JSONObject o = arr.optJSONObject(i);
        AoqClientEngine.AoqRelayEndpoint ep = new AoqClientEngine.AoqRelayEndpoint();
        ep.endpoint = o.optString("endpoint", "");
        ep.port = o.optInt("port", 0);
        cfg.relayEndpoints.add(ep);
    }
}

JSONObject ext = obj.optJSONObject("extraInfo");
cfg.workspaceIdHash = ext != null ? ext.optString("workspaceIdHash", "") : "";

AoqClientEngine.AoqTrackParam audio = new AoqClientEngine.AoqTrackParam();
audio.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeAudio;
AoqClientEngine.AoqTrackParam data = new AoqClientEngine.AoqTrackParam();
data.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeData;
cfg.publishTracks.add(audio);
cfg.publishTracks.add(data);
cfg.subscribeTracks.add(audio);
cfg.subscribeTracks.add(data);

engine.connect(cfg);
```

## **OHOS (ArkTS)**

```
const obj = JSON.parse(responseText) as Record<string, Object | undefined>;
const cfg: AoqConnectConfig = {
    token: String(obj['aoqTokenForClient'] ?? ''),
    sid: String(obj['sid'] ?? ''),
    certFingerprint: String(obj['clientRelayCertFingerprint'] ?? ''),
    relayEndpoints: (obj['clientRelayEndpoints'] as Array<any>).map(item => ({
        endpoint: String(item['endpoint'] ?? ''),
        port: Number(item['port'] ?? 0)
    })),
    workspaceIdHash: String((obj['extraInfo'] as any)?.['workspaceIdHash'] ?? ''),
    publishTracks: [
        { trackType: AoqTrackType.AoqTrackTypeAudio },
        { trackType: AoqTrackType.AoqTrackTypeData }
    ],
    subscribeTracks: [
        { trackType: AoqTrackType.AoqTrackTypeAudio },
        { trackType: AoqTrackType.AoqTrackTypeData }
    ]
};
engine.connect(cfg);
```

**说明**

`clientIp` 为请求体中的非必填字段。不填写时，使用请求百炼网关的 IP 作为客户端 IP；若填写，则以 clientIp 作为客户端 IP。建议由业务 AppServer 在服务端获取客户端真实 IP 后填入，以获得最佳的 Relay 接入点。

## **WebRTC 协议鉴权**

WebRTC 通过 HTTP POST 请求完成 SDP 交换，鉴权在此阶段完成。客户端将 Offer SDP 发送给服务端，服务端返回 Answer SDP。

**配置项**

**值**

**说明**

请求方法

POST

\-

请求地址

`https://{endpoint}/api/v1/webrtc/realtime?model={model_name}`

替换 endpoint 和 model\_name

Content-Type

`application/sdp`

请求体为 SDP 字符串

Authorization

`Bearer <API_KEY>`

必填

响应

HTTP 200，返回 Answer SDP

失败返回 4xx

**说明**

WebRTC 功能目前为白名单开放，请联系商务经理获取 Endpoint。

```
const pc = new RTCPeerConnection();
const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
stream.getAudioTracks().forEach(t => pc.addTrack(t, stream));
pc.createDataChannel('oai-events');

const offer = await pc.createOffer();
await pc.setLocalDescription(offer);

// 等待 ICE 收集完成后发送
const resp = await fetch(API_URL, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/sdp',
    'Authorization': `Bearer ${API_KEY}`,
  },
  body: pc.localDescription.sdp,
});
const answerSdp = await resp.text();
await pc.setRemoteDescription({ type: 'answer', sdp: answerSdp });
```

## **WebSocket 协议鉴权**

WebSocket 鉴权最为简单，客户端在建立 WebSocket 连接时直接通过 HTTP Header 携带 API Key。

**配置项**

**值**

**说明**

连接地址

`wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model={model_name}`

华北2（北京）

Authorization

`Bearer <API_KEY>`

必填

```
import websocket, os
API_KEY = os.getenv("DASHSCOPE_API_KEY")
URL = "wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=qwen3.5-omni-plus-realtime"
ws = websocket.WebSocketApp(URL, header=["Authorization: Bearer " + API_KEY])
ws.run_forever()
```

**说明**

您也可以使用 [DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk) 方式接入。
