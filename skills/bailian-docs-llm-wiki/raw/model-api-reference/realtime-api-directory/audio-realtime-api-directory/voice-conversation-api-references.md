# Qwen-Audio-Realtime

Qwen-Audio-Realtime 用于实时语音对话。模型支持文本和流式音频输入，可返回文本和音频。

`qwen-audio-3.1-realtime-plus`、`qwen-audio-3.1-realtime-flash`、`qwen-audio-3.0-realtime-plus`、`qwen-audio-3.0-realtime-flash` 均支持 WebSocket、WebRTC 和 AOQ。

<a id="协议选型"></a>

## 协议选型

选择协议时，可先查看 [Realtime API 接入方式选择](../realtime-api-overview.md#rtov-protocol-selection)。各型号支持的输入、输出和事件字段见对应的接入与事件参考。

-   [WebSocket](audio-realtime-websocket-access.md) 通过事件收发音频和文本。
    
    浏览器原生支持 WebSocket。接入模型时仍需满足鉴权要求，长期 API Key 应保存在服务端。
    
-   [WebRTC](audio-realtime-webrtc-access.md) 通过音频轨道收发语音，通过 DataChannel 收发文本和模型事件。
    
-   [AOQ（AI over QUIC）](audio-realtime-aoq-access.md) 使用 Client SDK 传输音频，通过独立的 Data 轨收发文本和模型事件。
    
    Client SDK 支持 Android、iOS、HarmonyOS、Windows、macOS、Electron 和 Linux。接入文档提供各平台的下载入口和 API 参考。
    

三种协议均可用于 Token Plan。可用模型和地域以 [Token Plan 个人版](../../../token-plan-user-guide/token-plan-personal/token-plan-personal-overview.md#tppo-h-models)及[团队版](../../../token-plan-user-guide/token-plan-team-edition/token-plan-team-overview.md#tpto-h-models)的说明为准。

<a id="事件及其他参考"></a>

## 事件及其他参考

-   [客户端事件](fun-audiochat-client-events.md)
-   [服务端事件](qwen-audio-realtime-server-events.md)

<a id="音色"></a>

## 音色

-   [音色复刻 API](../../../_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md#h3-create-enrollment)
-   [音色配置](audio-realtime-voice-cloning-api.md)
