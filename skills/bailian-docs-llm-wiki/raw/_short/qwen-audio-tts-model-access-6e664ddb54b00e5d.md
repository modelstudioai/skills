# Qwen-Audio-TTS 模型接入方式

介绍 Qwen-Audio-TTS 的接入入口、SDK 和事件参考。

## 接入方式

**说明**Qwen-Audio-3.0-TTS-Flash、Qwen-Audio-3.0-TTS-Plus 系列模型支持 AOQ（AI over QUIC）、WebSocket 两种传输协议，开发者可以根据业务场景灵活选择。详细接入流程请参见 [Realtime API](raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。

#### AOQ

-   [AOQ 接入](raw/model-api-reference/realtime-api-user-guide/realtime-model-connection/realtime-aoq-access.md)

#### WebSocket

通过 [WebSocket 接入指南](raw/_short/qwen-audio-tts-websocket-api-52aafa9f25e1c813.md)了解连接地址、鉴权及交互流程。

SDK 接入：

-   [Java SDK](raw/_short/qwen-audio-tts-java-sdk-a8824c674989f110.md)
-   [Python SDK](raw/_short/qwen-audio-tts-python-sdk-33fc56a178dfcd65.md)
-   [Android SDK](raw/_short/qwen-audio-tts-android-sdk-009ccd9eb6369f71.md)
-   [iOS SDK](raw/_short/qwen-audio-tts-ios-sdk-e258fc8147361a20.md)
-   [HarmonyOS SDK](raw/_short/qwen-audio-tts-harmonyos-sdk-be07ffd1f69fddb0.md)

## 事件参考

模型参数和事件字段的详细定义请参见：

-   [客户端事件](raw/_short/qwen-audio-tts-client-events-81541f7ec0ef1c33.md)
-   [服务端事件](raw/_short/qwen-audio-tts-server-events-f064dbfbbe02327e.md)
