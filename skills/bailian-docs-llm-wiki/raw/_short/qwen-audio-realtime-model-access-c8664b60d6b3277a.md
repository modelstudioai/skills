# Qwen-Audio-Realtime 模型接入方式

介绍 Qwen-Audio-Realtime 的接入入口、SDK 和事件参考。

## 接入方式

**Note**Qwen-Audio-3.1-Realtime-Plus、Qwen-Audio-3.1-Realtime-Flash、Qwen-Audio-3.0-Realtime-Plus 和 Qwen-Audio-3.0-Realtime-Flash 模型支持 AOQ（AI over QUIC）、WebRTC 和 WebSocket 三种传输协议，开发者可以根据业务场景灵活选择。详细接入流程请参见 [实时语音对话 API 参考](raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory/voice-conversation-api-references.md)。

#### WebSocket

通过 [WebSocket 接入指南](raw/_short/audio-realtime-websocket-access-5f0da4977f0f021b.md)了解连接地址、鉴权及交互流程。

SDK 接入：

-   [Android SDK](raw/_short/android-sdk-for-qwen-audio-realtime-service-49fdd3ca6879995b.md)
-   [iOS SDK](raw/_short/ios-sdk-for-qwen-audio-realtime-service-b5b40af2342b3f72.md)
-   [HarmonyOS SDK](raw/_short/harmonyos-sdk-for-qwen-audio-realtime-service-c830ce5a0546c776.md)

#### WebRTC

-   [WebRTC 接入](raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory/audio-realtime-webrtc-access.md)

#### AOQ

-   [AOQ 接入](raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory/audio-realtime-aoq-access.md)

## 事件参考

模型参数和事件字段的详细定义请参见：

-   [客户端事件](raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory/fun-audiochat-client-events.md)
-   [服务端事件](raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory/qwen-audio-realtime-server-events.md)
