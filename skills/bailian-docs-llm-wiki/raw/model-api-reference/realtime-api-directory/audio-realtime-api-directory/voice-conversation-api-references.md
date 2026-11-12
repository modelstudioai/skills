# 实时语音对话

Qwen-Audio-Realtime 用于实时语音对话。模型支持文本和流式音频输入，可返回文本和音频。

`qwen-audio-3.1-realtime-plus`、`qwen-audio-3.1-realtime-flash`、`qwen-audio-3.0-realtime-plus`、`qwen-audio-3.0-realtime-flash` 均支持 WebSocket、WebRTC 和 AOQ。

## 协议选型

选择协议时，可先查看 [Realtime API 接入方式选择](https://help.aliyun.com/zh/model-studio/realtime-api-overview#rtov-protocol-selection)。各型号支持的输入、输出和事件字段见对应的接入与事件参考。

-   [WebSocket](raw/_short/audio-realtime-websocket-access-5f0da4977f0f021b.md) 通过事件收发音频和文本。
    
    浏览器原生支持 WebSocket。接入模型时仍需满足鉴权要求，长期 API Key 应保存在服务端。
    
-   [WebRTC](raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory/audio-realtime-webrtc-access.md) 通过音频轨道收发语音，通过 DataChannel 收发文本和模型事件。
    
-   [AOQ（AI over QUIC）](raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory/audio-realtime-aoq-access.md) 使用 Client SDK 传输音频，通过独立的 Data 轨收发文本和模型事件。
    
    Client SDK 支持 Android、iOS、HarmonyOS、Windows、macOS、Electron 和 Linux。接入文档提供各平台的下载入口和 API 参考。
    

三种协议均可用于 Token Plan。可用模型和地域以 [Token Plan 个人版](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview#tpp01-h-models)及[团队版](https://help.aliyun.com/zh/model-studio/token-plan-team-overview#tpt01-h-models)的说明为准。

## 事件及其他参考

-   [客户端事件](raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory/fun-audiochat-client-events.md)
-   [服务端事件](raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory/qwen-audio-realtime-server-events.md)

## 音色

-   [音色复刻 API](https://help.aliyun.com/zh/model-studio/voice-clone-design-http-api#h3-create-enrollment)
-   [音色配置](raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory/audio-realtime-voice-cloning-api.md)
