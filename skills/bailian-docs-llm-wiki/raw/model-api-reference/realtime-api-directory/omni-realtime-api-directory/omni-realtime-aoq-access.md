# Qwen-Omni-Realtime AOQ 接入

Qwen-Omni-Realtime AOQ 接入

AOQ 将音视频媒体与模型事件分轨传输。SDK 负责媒体采集、编解码、传输和播放；应用通过 Data 轨发送模型事件并处理回复。本页使用 Qwen-Omni-Realtime 的媒体方向和事件协议。

## 适用范围

本文面向 Qwen-Omni-Realtime。现有接入说明覆盖：qwen3.8-omni-flash-realtime、qwen3.5-omni-plus-realtime、qwen3.5-omni-flash-realtime。示例模型为 `qwen3.8-omni-flash-realtime`。

-   使用所选地域和业务空间对应的 [API Key](raw/model-api-reference/preparations/get-api-key.md) 与 [API Host](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)（不含协议和路径）。
    
-   北京域名：`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`；新加坡域名：`{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`。
    
-   API Key 只保存在服务端，不放入浏览器或移动端应用。
    
-   使用麦克风采集音频或使用摄像头采集画面时，按平台要求申请相应权限。
    
-   从 [SDK 下载](https://help.aliyun.com/zh/model-studio/realtime-sdk-download#sdkdl-h2-aoq)获取对应平台的 SDK。
    

## 鉴权与连接凭证

**说明**如需提前获取 Token，或了解完整的鉴权流程，请参见[建连鉴权详解](https://help.aliyun.com/zh/model-studio/realtime-api-overview#tkauth-auth-detail-title)。

由业务 AppServer 发起以下请求。请先[配置 API Key 到环境变量](https://help.aliyun.com/zh/model-studio/get-api-key#20b17d4430qvt)。`clientIp` 选填，不填时使用请求网关的 IP。

POST`https://WorkspaceId.cn-beijing.maas.aliyuncs.com/api/v1/webrtc/realtime?model=qwen3.8-omni-flash-realtime`

POST`https://WorkspaceId.ap-southeast-1.maas.aliyuncs.com/api/v1/webrtc/realtime?model=qwen3.8-omni-flash-realtime`

#### 参数说明

`endpoint`

值:

根据业务情况选择接入域名

指定对应的接入域名，详情请参见[选择地域、服务部署范围和接入域名](raw/model-user-guide/get-started-with-models/regions.md)。如果使用[Token Plan](https://help.aliyun.com/zh/model-studio/token-plan-overview)，接入域名中的 `WorkspaceId` 固定为 `token-plan`。

`Content-Type`

值:

`application/json`

指定消息类型

`Authorization`

值:

`Bearer <YOUR_API_KEY>`

填写API Key

`x-dashscope-rtc-transport`

值:

`moq`

指定使用 AOQ 协议

`clientIp`

值:

客户端真实公网 IP

选填。不填写时，默认使用请求百炼网关的 IP；填写后以 clientIp 为准。服务 会根据客户端 IP 分配最佳的 Relay 接入点

```
export ENDPOINT="{WorkspaceId}.cn-beijing.maas.aliyuncs.com"
curl -X POST \
  "https://${ENDPOINT}/api/v1/webrtc/realtime?model=qwen3.8-omni-flash-realtime" \
  -H "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "x-dashscope-rtc-transport: moq" \
  -d '{}'
```

如需指定客户端公网 IP，将请求体中的 `-d '{}'` 替换为 `-d '{"clientIp":"<客户端公网 IP>"}'`。

#### 响应参数说明

`sid`

会话唯一标识

`aoqTokenForClient`

客户端连接令牌，传给 SDK 的 token 字段

`clientRelayEndpoints`

Relay 接入点数组。响应示例中的数组元素包含以下字段：

属性

`endpoint`

Relay 接入点地址。

`port`

Relay 接入点端口。

`route_index`

下方 iOS 示例在该字段缺省时使用数组下标。

`clientRelayCertFingerprint`

Relay TLS 证书指纹

`sidExpiresInSecs`

会话过期时间（秒）

`extraInfo`

附加信息。

属性

`workspaceIdHash`

工作区 ID 哈希。

#### 响应示例

```
{
    "sid": "1d06b55683db49bba67a407902f62d02:1782706970:69aecdc5...",
    "aoqTokenForClient": "ecc1a46015d5496ca4ff7a48281eb739",
    "clientRelayEndpoints": [{"endpoint": "121.199.XX.XX", "port": 8443, "route_index": 0}],
    "clientRelayCertFingerprint": "sha256/99843495...",
    "sidExpiresInSecs": 7200,
    "extraInfo": {"workspaceIdHash": "2021b6f98cea4cff"}
}
```

#### AOQ Client SDK 连接示例

**说明**`clientIp` 为请求体中的选填字段。不填写时，默认使用请求百炼网关的 IP 作为客户端 IP；填写后则以指定的 clientIp 为准。建议由业务 AppServer 获取客户端真实 IP 后填入，以获得最佳的 Relay 接入点。

iOS (Swift)

```
let resp = try JSONDecoder().decode(AllocateResponse.self, from: responseData)

let config = AoqConnectConfig()
config.token = resp.aoqTokenForClient
config.sid = resp.sid
config.certFingerprint = resp.clientRelayCertFingerprint
config.relayEndpoints = resp.clientRelayEndpoints.enumerated().map { index, item in
    let ep = AoqRelayEndpoint()
    // route_index 缺省时按数组下标兜底
    ep.routeIndex = item.routeIndex ?? index
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

Android (Java)

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
        // route_index 缺省时按数组下标兜底
        ep.routeIndex = o.has("route_index") ? o.optInt("route_index", i) : i;
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

OHOS (ArkTS)

```
const obj = JSON.parse(responseText) as Record<string, Object | undefined>;
const cfg: AoqConnectConfig = {
    token: String(obj['aoqTokenForClient'] ?? ''),
    sid: String(obj['sid'] ?? ''),
    certFingerprint: String(obj['clientRelayCertFingerprint'] ?? ''),
    // route_index 缺省时按数组下标兜底
    relayEndpoints: (obj['clientRelayEndpoints'] as Array<any>).map((item, index) => ({
        routeIndex: Number(item['route_index'] ?? index),
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

## 整体流程

![AOQ 接入时序图](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/images/6a4b3c2d1e0f92fa.png)

1.  客户端通过业务 AppServer 获取连接凭证。
2.  创建 SDK 引擎并注册回调。
3.  配置媒体和 Data 轨道，关闭上行媒体发送。
4.  建立 AOQ 连接，等待连接成功。
5.  按模型协议完成配置，收到确认后开启所需媒体发送。
6.  完成交互后断开连接并释放资源。

**说明**

-   音视频媒体数据由 AOQ SDK 接管，负责采集、处理、发送、接收和播放；Data 数据需要调用方遵循目标模型的事件定义进行发送和接收。
    
-   连接成功表示与模型的传输通道已建立，客户端应在模型初始化完成后再开启所需的上行媒体。对于本页示例型号 `qwen3.8-omni-flash-realtime`，发送 `session.update` 后需等待 `session.updated`，再开启媒体发送。
    

## 1\. 获取连接凭证

客户端向业务 AppServer 请求凭证。AppServer 使用本模型的 Realtime 建连地址，并携带 API Key 和 `x-dashscope-rtc-transport: moq` 请求网关。完整地址、请求和字段说明见 [Token 鉴权](#authentication)。

将响应映射到 `AoqConnectConfig`：

网关响应

SDK 配置

`aoqTokenForClient`

`token`

`sid`

`sid`

`clientRelayCertFingerprint`

`certFingerprint`

`clientRelayEndpoints`

`relayEndpoints`，按结构转换各接入点

`extraInfo` 中的 `workspaceIdHash`

`workspaceIdHash`

新建连接时获取新的连接凭证。同一连接内能否复用会话或启动下一轮任务，由目标模型协议决定。

## 2\. 初始化 SDK 并注册回调

创建引擎并注册连接状态、Data 消息和错误回调。以 iOS Swift 为例：

```
let createConfig = AoqCreateConfig()
createConfig.workDir = workDir
createConfig.enableDumpAudio = false
engine = AoqClientEngine.createEngine(createConfig, delegate: self)
```

实现 `AoqEngineDelegate`，在 `onConnectionStatusChange` 中维护连接状态，在 `onDataMsg` 中解析目标模型事件，在 `onError` 中处理 SDK 错误。模型返回的错误事件也需要在 Data 消息处理逻辑中单独处理。SDK 接口及错误说明请参见 [各平台 SDK](raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)和[功能参考](raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api/realtime-api-aoq-sdk-function.md)。

## 3\. 配置 SDK

### 选择四个媒体方向

以下“推”和“拉”均以客户端为视角。按业务实际使用的输入、输出模态配置，不需要的方向不添加媒体轨道。

方向

配置内容

典型用途

推音频

发布 Audio 轨，设置音频编码器，配置内置或外部采集

语音对话

拉音频

订阅 Audio 轨，设置音频解码器，配置播放器或外部播放

语音回复

推视频

发布 Video 轨，配置摄像头或外部视频输入及编码参数

向支持视觉输入的模型发送画面

拉视频

本模型不支持视频输出

不配置视频订阅

Data 轨独立于这四个方向：发布 Data 轨用于发送模型事件，订阅 Data 轨用于接收回复。纯文本输入或输出也需要 Data 轨。

### 本模型的媒体方向

下表列出本模型的媒体方向。模型范围见[适用范围](#%E9%80%82%E7%94%A8%E8%8C%83%E5%9B%B4)，其他接入方式参见[Qwen-Omni-Realtime](raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory/omni-realtime-api.md)。

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

### 配置媒体参数和轨道

音频上行和下行应分别配置：上行使用 `setAudioEncoderConfig`，下行使用 `setAudioDecoderConfig`。这些参数用于网络传输，网关会将音频转换为模型所需的格式。传输编码配置与模型事件中的音频格式参数应分别按 SDK 和目标模型的要求设置。

按方向启动 `startAudioCapture`、`startAudioPlayer` 或 `startVideoCapture`。自定义输入输出见下文高阶能力。

`publishTracks` 表示客户端发送的轨道，`subscribeTracks` 表示客户端接收的轨道：

场景

`publishTracks`

`subscribeTracks`

语音对话

Audio、Data

Audio、Data

带画面输入的语音对话

Audio、Video、Data

Audio、Data

在建连前关闭上行媒体发送，避免模型尚未就绪时收到输入：

```
engine.enableSendMediaStream(.audio, enable: false)
engine.enableSendMediaStream(.video, enable: false)
```

采集、发布轨道和允许发送是不同的操作。关闭发送不等于停止本地采集，也不影响 Data 轨事件收发。未添加的轨道不会因开启发送而自动创建。

## 4\. 建立连接

将凭证与轨道配置填入 `AoqConnectConfig`，调用：

```
engine.connect(connectConfig)
```

等待 `onConnectionStatusChange` 返回 `.connected`，再进入模型初始化流程。`connect` 调用返回不等于连接成功。

## 5\. 按模型协议交互并收发媒体

### 发送和解析模型事件

客户端通过 Data 轨发送事件。以下为 iOS Swift 代码片段，其他接口详见 [iOS SDK 参考](raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api/aoq-ios-sdk-reference.md)：

```
// eventJSON 由目标模型的客户端事件协议构造。
let msg = AoqDataMsg()
msg.data = eventJSON.data(using: .utf8)!
engine.send(msg)
```

在 `onDataMsg` 中解析回复。本模型通过 `type` 字段标识事件类型。完整字段、参数及结束条件应遵循目标模型文档。

### 就绪后开启所需媒体

满足当前模型、当前会话或任务的就绪条件后，仅开启已配置的上行方向。例如，需要语音输入时调用：

```
engine.enableSendMediaStream(.audio, enable: true)
```

需要视频输入时再开启 `.video`。

音视频通过对应媒体轨道传输；模型事件和文本通过 Data 轨传输。例如，Omni 的 AOQ 接入无需使用 `input_audio_buffer.append` 或 `input_image_buffer.append` 重复发送媒体。下行音频由已配置的播放器或外部播放逻辑处理。

## 6\. 结束交互并释放资源

不再使用连接时，由客户端业务层调用AOQ SDK 的断开连接和释放资源接口：

```
engine.disconnect()
AoqClientEngine.destroy()
```

异常断开后清理业务层就绪状态，按[连接状态管理](raw/_short/aoq-connection-management-f4e04b0f678fdee1.md)处理后续连接；重新建连后按模型协议重新初始化。

## Data 通道发送和接收事件

客户端通过 AOQ SDK 的 Data 轨发送和接收模型事件。连接时需要发布和订阅 Data 轨；发送时将模型事件序列化后放入 `AoqDataMsg`，并调用所用平台的 Data 发送接口；接收时在 `onDataMsg` 回调中解析消息。接口详见[各平台 SDK](raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)。

发送事件的名称、字段、参数和调用时机遵循目标模型的**客户端事件定义**；收到消息后的解析方式、状态变更、结果和错误处理遵循该模型的**服务端事件定义**。初始化事件根据模型要求按需发送，后续文本和控制事件按照业务需要发送。

模型/应用

客户端事件定义（发送）

服务端事件定义（接收）

Qwen-Omni-Realtime

[客户端事件](raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory/client-events.md)

[服务端事件](raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory/server-events.md)

模型事件的发送与接收还应遵循以下规则：

-   使用事件的 `type` 字段识别模型事件，关联标识按本模型事件参考处理。
    
-   模型要求的初始化确认、输入提交、响应取消和任务结束等操作，均在 Data 通道中按对应协议处理；它们属于模型交互语义，与断开传输连接是不同操作。
    
-   结束前按本模型事件说明完成输入提交和结果接收；需要完整播放时，处理完本地待播音频再释放连接。
    
-   音视频数据通过媒体轨道传输。引用模型事件文档时，媒体封装和可用交互模式仍遵循本文的接入方式，不直接套用 WebSocket 的媒体发送方式。
    

## 高阶能力

能力

使用场景

文档

独立控制音视频发送

等待模型就绪、暂停上行、按需开启视频

[媒体流发送管理](raw/_short/aoq-media-stream-control-1278a5c1aba30cc3.md)

音频设备与处理

编解码、扬声器、文件混音、音频帧回调

[音频常用功能](raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-audio-features.md)

外部音频输入

使用业务侧音频源

[自定义音频采集](raw/_short/aoq-custom-audio-capture-79471541298aac63.md)

外部音频输出

由业务侧处理或播放输出音频

[自定义音频播放](raw/_short/aoq-custom-audio-playback-d7aa8527189532a2.md)

视频采集与输入

摄像头及业务侧画面输入

[视频常用功能](raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api/realtime-api-aoq-sdk-function/aoq-video-features.md)、[自定义视频输入](raw/_short/aoq-custom-video-input-be576bbf9ade6cc8.md)

媒体发送控制只控制媒体传输。模型响应取消、轮次提交等行为仍需使用目标模型的事件协议。

## 会话配置示例

**说明**以下示例适用于 `qwen3.8-omni-flash-realtime`。音视频通过媒体轨道传输，不使用 WebSocket 的媒体发送事件。

```
{
  "type": "session.update",
  "session": {
    "modalities": [
      "text",
      "audio"
    ],
    "voice": "Tina",
    "turn_detection": {
      "type": "server_vad"
    }
  }
}
```

## AOQ SDK 下载

以下版本更新说明描述 AOQ SDK 的通用能力，本模型的媒体支持范围见上方[本模型的媒体方向](#conn-aoq-model-media-title)。

**版本**

**平台**

**下载**

**更新日期**

**更新说明**

v1.4.0

Android

[AoqClientSdk-release.aar](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f93a6.aar)

[libPluginOpus.zip](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f939f.zip)

2026-10-27

1.  支持从外部输入 H.264 视频。
2.  优化性能。
3.  修复已知的稳定性问题。

iOS

[AoqClientSdk.framework.zip](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9398.zip)

[AoqScreenShare.framework.zip](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f939e.zip)

[PluginOpus.framework.zip](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f939d.zip)

HarmonyOS

[AoqClientSdk.har](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f939c.har)

[libPluginOpus.zip](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9393.zip)

Windows

[AoqClientSdk-windows-x64.zip](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9392.zip)

macOS

[AoqClientSdk.framework.zip](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f93a1.zip)

[PluginOpus.framework.zip](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9391.zip)

Electron

[aoq-electron-sdk-1.4.0-59463182.tgz](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9390.tgz)

也可以通过 npm 安装：

`npm install aoq-electron-sdk@1.4.0-59463182`

Linux

`x86_64`: [AoqClientSdk.zip](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9397.zip)

`arm64`: [AoqClientSdk.zip](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9396.zip)

v1.3.0

Android

[AoqClientSdk-release.aar](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9dab.aar)

[libPluginOpus.zip](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9d8c.zip)

2026-09-18

1.  新增屏幕共享能力。
    
2.  废弃 bitcode。
    
3.  支持远程加载 .so 库。
    
4.  支持从外部设置编码帧最大值。
    
5.  将默认编解码器调整为 Opus。
    
6.  优化性能。
    
7.  修复已知的稳定性问题。
    

iOS

[AoqClientSdk.framework.zip](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9d83.zip)

[AoqScreenShare.framework.zip](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9d82.zip)

[PluginOpus.framework.zip](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9d81.zip)

HarmonyOS

[AoqClientSdk.har](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9d80.har)

[libPluginOpus.zip](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9d87.zip)

Windows

[AoqClientSdk-windows-x64.zip](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9d86.zip)

macOS

[AoqClientSdk.framework.zip](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9d85.zip)

[PluginOpus.framework.zip](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9d84.zip)

Electron

[aoq-electron-sdk-1.3.0-58586345.tgz](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9d9b.tgz)

也可以通过 npm 安装：`npm install aoq-electron-sdk@1.3.0-58586345`

Linux

x86\_64: [AoqClientSdk.zip](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9d9a.zip)

arm64: [AoqClientSdk.zip](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9d99.zip)

v1.2.2

iOS

[AoqClientSdk.framework.zip](https://g-adoc.alcasset.com/media/maas_docs/sfm/common/files/6a4b3c2d1e0f9e68.zip)

2026-09-09

1.  修复 iOS 通话被系统或第三方语音通话打断后，在中断结束时无法恢复通话的问题。
    
2.  优化 iOS 通话起始阶段的回声抑制效果。
    

v1.2.0

Android

[AoqClientSdk-release.aar](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260817/eiejsg/AoqClientSdk-release.aar)

[libPluginOpus.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260817/kvogns/libPluginOpus.zip)

2026-08-17

1.  新增macOS平台支持
    
2.  新增Windows平台支持
    
3.  新增Electron平台支持
    
4.  Linux平台同时支持Python和C++接口
    
5.  新增音量检测功能
    
6.  优化性能
    
7.  修复已知的稳定性问题
    

iOS

[AoqClientSdk.framework.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260817/xojbbu/AoqClientSdk.framework.zip)

[PluginOpus.framework.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260817/hdcfjp/PluginOpus.framework.zip)

HarmonyOS

[AoqClientSdk.har](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260817/txwctz/AoqClientSdk.har)

[libPluginOpus.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260817/ogziwz/libPluginOpus.zip)

Windows

[AoqClientSdk-windows-x64.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260817/ryieyw/AoqClientSdk-windows-x64.zip)

[PluginOpus.dll.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260817/jsooaa/PluginOpus.dll.zip)

macOS

[AoqClientSdk.framework.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260817/xwgbgr/AoqClientSdk.framework.zip)

[PluginOpus.framework.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260817/cusppf/PluginOpus.framework.zip)

Electron

安装包：[aoq-electron-sdk-1.2.0-57407598.tgz](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260817/kgxgow/aoq-electron-sdk-1.2.0-57407598.tgz)

也可以通过npm安装：`npm install aoq-electron-sdk@1.2.0-57407598`

Linux

x86\_64：[AoqClientSdk.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260817/duxbqa/AoqClientSdk.zip)

arm64：[AoqClientSdk.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260817/nknxye/AoqClientSdk.zip)

v1.1.0

Android

[AoqClientSdk-v1.1.0.aar](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260803/mzfhfm/AoqClientSdk-v1.1.0.aar)

[libPluginOpus.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260803/mnwwkr/libPluginOpus.zip)

2026-07-31

1.  支持ASR模型
    
2.  支持TTS模型
    
3.  支持多模态交互套件
    
4.  新增支持Linux平台
    
5.  优化性能
    
6.  解决已知的稳定性问题
    

iOS

[AoqClientSdk-v1.1.0.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260803/bhiqbu/AoqClientSdk-v1.1.0.zip)

[PluginOpus.framework.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260803/shapwe/PluginOpus.framework.zip)

HarmonyOS

[AoqClientSdk-v1.1.0.har](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260803/qtyubq/AoqClientSdk-v1.1.0.har)

[libPluginOpus.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260803/hugetl/libPluginOpus.zip)

Linux

[AoqClientSdk.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260803/swaqde/AoqClientSdk.zip)

v1.0.1

Android

[AoqClientSdk-v1.0.1.aar](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260715/sqsjum/AoqClientSdk-v1.0.1.aar)

[libPluginOpus.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260715/oxzenn/libPluginOpus.zip)

2026-07-09

1.  支持AOQ协议接入模型/应用
    
2.  支持音视频编解码参数
    
3.  支持音视频设备采集及播放
    
4.  支持自定义外部输入音频采集
    
5.  支持自定义外部输入视频采集
    
6.  支持自定义外部输入视频编码
    
7.  支持控制媒体流的发送
    

iOS

[AoqClientSdk-v1.0.1.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260715/vlyumo/AoqClientSdk-v1.0.1.zip)

[PluginOpus.framework.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260715/rbvmfq/PluginOpus.framework.zip)

HarmonyOS

[AoqClientSdk-v1.0.1.har](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260715/zwlikp/AoqClientSdk-v1.0.1.har)

[libPluginOpus.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260715/wvtyrh/libPluginOpus.zip)

**重要**AOQ使用音频插件的方式加载Opus编解码器，如果需要Opus编解码时需要下载Opus插件并加载到工程内。

## 事件参考

-   [客户端事件](raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory/client-events.md)
-   [服务端事件](raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory/server-events.md)

## 场景教程

-   [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
-   [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
