# Qwen-Livetranslate-Realtime 模型接入方式

介绍 Qwen-Livetranslate-Realtime 的接入入口、SDK 和事件参考。

## 接入方式

**说明**Qwen3.5-Livetranslate-Flash-Realtime 模型支持 AOQ（AI over QUIC）、WebRTC 和 WebSocket 三种传输协议，开发者可以根据业务场景灵活选择。详细接入流程请参见 [Realtime API](raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。

#### AOQ

-   [AOQ 接入](raw/model-api-reference/realtime-api-user-guide/realtime-model-connection/realtime-aoq-access.md)

#### WebSocket

通过以下 SDK 文档了解 WebSocket 接入方法及调用示例。

SDK 接入：

-   [Python SDK](raw/_short/qwen-livetranslate-python-sdk-0419928c3312cc76.md)
-   [Java SDK](raw/_short/qwen-livetranslate-java-sdk-be8175c4887f8470.md)

#### WebRTC

-   [WebRTC 接入](raw/model-api-reference/realtime-api-user-guide/realtime-model-connection/realtime-webrtc-access.md)

## 事件参考

模型参数和事件字段的详细定义请参见：

-   [客户端事件](raw/_short/live-translator-client-events-666da53ef8b3942d.md)
-   [服务端事件](raw/_short/live-translator-server-events-e9db9578a7b303d5.md)
