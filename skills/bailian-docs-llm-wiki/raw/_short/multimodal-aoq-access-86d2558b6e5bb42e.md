# Realtime API

通过 Realtime API 接入多模态交互开发套件（multimodal-dialog），根据业务场景选择传输协议。

## 接入指引

协议对比和选型参见 [Realtime API 概述](raw/model-api-reference/realtime-api-directory/realtime-api-overview.md)。

-   [AOQ 接入](#aoq)
-   [WebRTC 接入](raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
-   [WebSocket 接入](raw/model-api-reference/realtime-api-directory/multimodal-interaction-protocol.md)

## AOQ 接入

先[创建多模态交互应用](raw/_short/multimodal-app-creation-ef194a004f7549d5.md)，获取工作空间 ID 和应用 ID，并[配置应用](raw/_short/multimodal-app-configuration-8919f99b339e17da.md)的模型、音色及交互方式。从 [SDK 下载](raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api/realtime-sdk-download.md)导入对应平台的 AOQ SDK。启用麦克风或摄像头采集时，按需申请客户端权限。

### 获取连接凭证

每次建立新连接前，由业务 AppServer 请求临时凭证。将 `{endpoint}` 替换为应用所在业务空间的[接入域名](raw/model-user-guide/get-started-with-models/regions.md)，并在 AppServer 中配置对应的 [API Key](raw/model-api-reference/preparations/get-api-key.md)。

```
curl -X POST \
  "https://{endpoint}/api/v1/webrtc/inference?model=multimodal-dialog" \
  -H "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "x-dashscope-rtc-transport: moq" \
  -d '{}'
```

可在请求体中填写客户端真实公网 IP（`clientIp`），供网关选择 Relay 接入点。未填写时，网关使用请求来源 IP。

API Key 仅保存在 AppServer。AppServer 将下表中的连接参数返回客户端，响应中的 `sidExpiresInSecs` 表示会话有效期，单位为秒。

网关响应字段

`AoqConnectConfig` 字段

`aoqTokenForClient`

`token`

`sid`

`sid`

`clientRelayCertFingerprint`

`certFingerprint`

`clientRelayEndpoints`

`relayEndpoints`，逐项转换 `endpoint`、`port` 和 `route_index`

`extraInfo.workspaceIdHash`

`workspaceIdHash`

### 建连与交互

1.  **初始化引擎并配置轨道。** 注册连接状态、Data 消息和 SDK 错误回调。音频对话发布 Audio 和 Data 轨，订阅 Audio 和 Data 轨，配置音频编解码及采集、播放。按应用的输入能力配置上行 Video 轨，按应用的输出能力配置下行 Video 轨。建连前关闭媒体上行。
2.  **建立连接并启动会话。** 传入连接参数和轨道配置，等待 SDK 回调连接成功。通过 Data 轨发送 [Start 指令](https://help.aliyun.com/zh/model-studio/multimodal-interaction-protocol#5b2363d40585y)，填写应用和工作空间信息。收到 `Started` 后继续等待 `DialogStateChanged`，确认 `payload.output.state` 为 `Listening` 后再开启音频上行。
3.  **收发媒体与事件。** 音视频通过媒体轨传输，应用事件通过 Data 轨传输。根据[交互协议](raw/model-api-reference/realtime-api-directory/multimodal-interaction-protocol.md)中的 Input Message 构造请求，按 Output Message 解析会话事件和错误。需要视频输入时，按应用能力开启已配置的 Video 轨。
4.  **结束会话。** 停止媒体上行，通过 Data 轨发送 [Stop 指令](https://help.aliyun.com/zh/model-studio/multimodal-interaction-protocol#ed70d4193bihk)。收到 `Stopped` 后停止采集、播放并断开连接，不再使用引擎时释放资源。

各端的连接配置、回调和高级媒体功能参见 [AOQ SDK](raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api.md)及[功能参考](raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api/realtime-api-aoq-sdk-function.md)。
