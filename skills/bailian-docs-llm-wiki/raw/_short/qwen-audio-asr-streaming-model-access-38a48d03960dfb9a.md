# Qwen-Audio-ASR-Streaming 模型接入方式

介绍 Qwen-Audio-ASR-Streaming 的接入入口、SDK 和事件参考。

## 接入方式

**说明**Qwen-Audio-3.0-ASR-Flash-Streaming 模型支持 AOQ（AI over QUIC）、WebSocket 两种传输协议，开发者可以根据业务场景灵活选择。详细接入流程请参见 [Realtime API](raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。

#### AOQ

-   [AOQ 接入](raw/model-api-reference/realtime-api-user-guide/realtime-model-connection/realtime-aoq-access.md)

#### WebSocket

通过 [WebSocket 接入指南](raw/_short/qwen-audio-asr-streaming-websocket-api-af0499578aae1ad5.md)了解连接地址、鉴权及交互流程。

SDK 接入：

-   [Python SDK](raw/_short/qwen-audio-asr-streaming-python-sdk-d09b6005cff4b207.md)
-   [Java SDK](raw/_short/qwen-audio-asr-streaming-java-sdk-0a79c28a0694d86f.md)
-   [Android SDK](raw/_short/qwen-audio-asr-streaming-android-sdk-f4b72c6ecfb0efa3.md)
-   [iOS SDK](raw/_short/qwen-audio-asr-streaming-ios-sdk-4296b78affca1c0c.md)
-   [HarmonyOS SDK](raw/_short/qwen-audio-asr-streaming-harmonyos-sdk-5e1fe47bfe0e04b3.md)

## 事件参考

模型参数和事件字段的详细定义请参见：

-   [客户端事件](raw/_short/qwen-audio-asr-streaming-client-events-1bae8548d2be6bc5.md)
-   [服务端事件](raw/_short/qwen-audio-asr-streaming-server-events-b134164fc4410c2a.md)
