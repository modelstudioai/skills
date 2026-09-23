# Qwen-Audio-TTS/CosyVoice 模型接入方式

介绍 Qwen-Audio-TTS/CosyVoice 的接入入口、SDK 和事件参考。

## 接入方式

**说明**Qwen-Audio-3.0-TTS-Flash、Qwen-Audio-3.0-TTS-Plus 和 CosyVoice 系列模型支持 AOQ（AI over QUIC）、WebSocket 两种传输协议，开发者可以根据业务场景灵活选择。详细接入流程请参见 [Realtime API](raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。

#### AOQ

-   [AOQ 接入](raw/model-api-reference/realtime-api-user-guide/realtime-model-connection/realtime-aoq-access.md)

#### WebSocket

通过 [WebSocket 接入指南](raw/_short/cosyvoice-websocket-api-615049d40629caf7.md)了解连接地址、鉴权及交互流程。

SDK 接入：

-   [Java SDK](raw/_short/cosyvoice-java-sdk-4cad5c0351587943.md)
-   [Python SDK](raw/_short/cosyvoice-python-sdk-c20dfd31499fc83c.md)
-   [Android SDK](raw/_short/cosyvoice-android-sdk-3c17b87965adaf1e.md)
-   [iOS SDK](raw/_short/cosyvoice-ios-sdk-1995754e712f9554.md)
-   [HarmonyOS SDK](raw/_short/cosyvoice-harmonyos-sdk-59292bbe883fea24.md)

## 事件参考

模型参数和事件字段的详细定义请参见：

-   [客户端事件](raw/_short/cosyvoice-client-events-a63a525ab07e6693.md)
-   [服务端事件](raw/_short/cosyvoice-server-events-388da422580d5c78.md)
