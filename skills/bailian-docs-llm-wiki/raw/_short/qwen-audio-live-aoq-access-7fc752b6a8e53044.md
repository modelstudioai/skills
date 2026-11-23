# Qwen-Audio-Live AOQ 接入

使用控制 WebSocket 获取临时凭证并建立 AOQ 媒体连接。

先通过控制 WebSocket 建立会话并获取临时凭证。AOQ 连接就绪后，通过 AOQ 收发音频，会话期间保持控制 WebSocket。

从 [SDK 下载](https://help.aliyun.com/zh/model-studio/realtime-sdk-download#sdkdl-h2-aoq)获取终端平台对应的 AOQ Client SDK。macOS 可下载 v1.4.0 的 SDK 和 Opus 插件。

## 建立 WebSocket 连接

按 [WebSocket 接入](raw/model-api-reference/realtime-api-directory/qwen-audio-live-api-directory/qwen-audio-live-websocket-access.md) 中的地址和鉴权说明建立连接。在 `session.update` 的 `session` 对象中加入以下配置。

```
{"transport":{"type":"aoq","aoq":{"ws_audio":false}}}
```

## 建立 AOQ 媒体连接

1.  等待 `session.updated`。AOQ 连接信息在返回的 `session` 对象内，依次展开 `transport` 和 `aoq`。每次建立新会话都要重新获取凭证。请勿记录到日志。
2.  将同一次会话返回的 `sid`、`aoqTokenForClient`、`clientRelayCertFingerprint` 和 `clientRelayEndpoints` 传给 AOQ Client SDK。将 `extraInfo` 中的 `workspaceIdHash` 也传给 SDK。每个 Relay 地址包含 `endpoint`、`port` 和 `route_index`。
3.  收到 `session.updated` 后，请在 5 分钟内使用返回的 `sid` 和临时凭证发起 AOQ 连接。收到连接成功回调后，启动音频采集和发送，并通过 SDK 播放下行音频。会话期间保持 WebSocket 连接。
4.  结束时停止采集和播放，断开 AOQ，再关闭 WebSocket 会话。

排查音频收发时，可从 `session.updated` 的 `session.transport.aoq.sid` 读取 AOQ 会话 ID。`session.id` 标识业务会话。

## 接收服务端事件

媒体连接就绪后，可从控制 WebSocket 接收服务端事件，也可通过 AOQ 的数据轨接收。使用 AOQ 接收事件时，订阅数据轨并处理 SDK 的数据消息回调。macOS SDK 的回调是 `onDataMsg:`。如果两路收到相同 `event_id` 的事件，只处理一次。

## 音频传输

通过 AOQ 发送上行语音。若通过 WebSocket 发送 `session.input_audio.append`，服务会返回 `audio_requires_aoq_media`。

`aoq` 对象中的 `ws_audio` 默认为 `false`。设为 `true` 后，服务还会通过 WebSocket 发送一份下行音频。业务接入见[任务委派与工具](https://help.aliyun.com/zh/model-studio/qwen-audio-live-delegation)。会话和任务事件见 [客户端事件](raw/model-api-reference/realtime-api-directory/qwen-audio-live-api-directory/qwen-audio-live-client-events.md) 和 [服务端事件](raw/model-api-reference/realtime-api-directory/qwen-audio-live-api-directory/qwen-audio-live-server-events.md)。
