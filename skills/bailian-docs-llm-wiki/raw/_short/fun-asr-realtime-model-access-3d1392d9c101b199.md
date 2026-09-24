# Qwen-Audio-3.x-ASR-Flash-Streaming/Fun-ASR-Realtime 模型接入方式

介绍 Qwen-Audio-3.x-ASR-Flash-Streaming/Fun-ASR-Realtime 的接入入口、SDK 和事件参考。

## 接入方式

**说明**Qwen-Audio-3.0-ASR-Flash-Streaming/Fun-ASR-Realtime 模型支持 AOQ（AI over QUIC）、WebSocket 两种传输协议，开发者可以根据业务场景灵活选择。详细接入流程请参见 [Realtime API](raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。

#### AOQ

-   [AOQ 接入](raw/model-api-reference/realtime-api-user-guide/realtime-model-connection/realtime-aoq-access.md)

#### WebSocket

通过 [WebSocket 接入指南](raw/_short/fun-asr-realtime-websocket-api-d80484c92992191d.md)了解连接地址、鉴权及交互流程。

SDK 接入：

-   [Python SDK](raw/_short/fun-asr-realtime-python-sdk-c8b5a715c3e66b70.md)
-   [Java SDK](raw/_short/fun-asr-realtime-java-sdk-1f6304ff694438f5.md)
-   [Android SDK](raw/_short/android-sdk-for-fun-asr-real-time-service-c55cca39825ba463.md)
-   [iOS SDK](raw/_short/ios-sdk-for-fun-asr-real-time-service-edf00c4a48ca2236.md)
-   [HarmonyOS SDK](raw/_short/harmonyos-sdk-for-fun-asr-real-time-service-a4bee2f4f80aa68b.md)

## 事件参考

模型参数和事件字段的详细定义请参见：

-   [客户端事件](raw/_short/fun-asr-client-events-997ba24ade1a8a48.md)
-   [服务端事件](raw/_short/fun-asr-server-events-666d2f9990cd5ae1.md)
