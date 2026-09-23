# Qwen-Audio-Realtime 模型接入方式

介绍 Qwen-Audio-Realtime 的接入入口、SDK 和事件参考。

## 接入方式

**说明**Qwen-Audio-3.1-Realtime-Plus、Qwen-Audio-3.0-Realtime-Plus 和 Qwen-Audio-3.0-Realtime-Flash 模型支持 AOQ（AI over QUIC）、WebRTC 和 WebSocket 三种传输协议，开发者可以根据业务场景灵活选择。详细接入流程请参见 [Realtime API](raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。

#### AOQ

-   [AOQ 接入](raw/model-api-reference/realtime-api-user-guide/realtime-model-connection/realtime-aoq-access.md)

#### WebSocket

通过 [WebSocket 接入指南](raw/_short/fun-audiochat-realtime-websocket-api-66b5ba4f8a668f28.md)了解连接地址、鉴权及交互流程。

SDK 接入：

-   [Android SDK](raw/_short/android-sdk-for-qwen-audio-realtime-service-ca199805bd8bb70c.md)
-   [iOS SDK](raw/_short/ios-sdk-for-qwen-audio-realtime-service-8355a9429e58321f.md)
-   [HarmonyOS SDK](raw/_short/harmonyos-sdk-for-qwen-audio-realtime-service-b0a55b87b24035d2.md)

#### WebRTC

-   [WebRTC 接入](raw/model-api-reference/realtime-api-user-guide/realtime-model-connection/realtime-webrtc-access.md)

## 事件参考

模型参数和事件字段的详细定义请参见：

-   [客户端事件](raw/_short/fun-audiochat-client-events-613371219df1f107.md)
-   [服务端事件](raw/_short/qwen-audio-realtime-server-events-570d84e54a56325a.md)
