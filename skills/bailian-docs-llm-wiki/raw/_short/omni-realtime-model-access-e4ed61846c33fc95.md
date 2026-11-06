# Qwen-Omni-Realtime 模型接入方式

介绍 Qwen-Omni-Realtime 的接入入口、SDK 和事件参考。

## 接入方式

**Note**Qwen3.8-Omni-Flash-Realtime、Qwen3.5-Omni-Plus-Realtime 和 Qwen3.5-Omni-Flash-Realtime 模型支持 AOQ（AI over QUIC）、WebRTC 和 WebSocket 三种传输协议，开发者可以根据业务场景灵活选择。详细接入流程请参见 [Realtime API](raw/model-api-reference/realtime-api-directory/realtime-api-overview.md)。

#### AOQ

-   [AOQ 接入](raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory/omni-realtime-aoq-access.md)

#### WebSocket

通过 [WebSocket 接入指南](raw/_short/omni-realtime-interaction-process-144f8455755c1f0a.md)了解连接地址及交互流程。

SDK 接入：

-   [Python SDK](raw/_short/omni-realtime-python-sdk-0d3c931c58118ee5.md)
-   [Java SDK](raw/_short/omni-realtime-java-sdk-5b43428f0b0df256.md)

#### WebRTC

-   [WebRTC 接入](raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory/omni-realtime-webrtc-access.md)

## 事件参考

模型参数和事件字段的详细定义请参见：

-   [客户端事件](raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory/client-events.md)
-   [服务端事件](raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory/server-events.md)
