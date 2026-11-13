# 实时音视频翻译

Qwen-LiveTranslate-Realtime 可实时翻译语音，并结合画面辅助理解。模型输出目标语种的译文，部分目标语种还支持译音。

该系列支持 WebSocket、WebRTC 和 AOQ。系列指南列有 `qwen3.8-livetranslate-flash-realtime`、`qwen3.5-livetranslate-flash-realtime` 和快照版 `qwen3.5-livetranslate-flash-realtime-2026-05-19`。`qwen3.5-livetranslate-flash-realtime` 当前能力与该快照版相同。

## 协议选型

选择协议时，可先查看 [Realtime API 接入方式选择](https://help.aliyun.com/zh/model-studio/realtime-api-overview#rtov-protocol-selection)。各型号支持的输入、输出和事件字段见对应的接入与事件参考。

-   使用 [WebSocket](raw/_short/livetranslate-realtime-websocket-access-69ee95b6726440dc.md) 时，通过音频事件发送语音，可添加图像辅助翻译。
    
    浏览器原生支持 WebSocket。接入模型时仍需满足鉴权要求，长期 API Key 应保存在服务端。
    
-   [WebRTC](raw/_short/livetranslate-realtime-webrtc-access-ddb4e390439cd632.md) 通过音频轨道发送原声和接收译音，通过 DataChannel 收发模型事件。
    
-   [AOQ（AI over QUIC）](raw/model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/livetranslate-realtime-aoq-access.md) 使用 Client SDK 分轨传输媒体和模型事件。
    
    Client SDK 支持 Android、iOS、HarmonyOS、Windows、macOS、Electron 和 Linux。接入文档提供各平台的下载入口和 API 参考。
    

WebRTC 和 AOQ 的画面输入取决于所用型号和场景。

三种协议均可用于 Token Plan。可用模型和地域以 [Token Plan 个人版](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview#tppo-h-models)及[团队版](https://help.aliyun.com/zh/model-studio/token-plan-team-overview#tpto-h-models)的说明为准。

## 事件及其他参考

-   [客户端事件](raw/model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-client-events.md)
-   [服务端事件](raw/model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-server-events.md)

## 音色

-   [预建音色 API](https://help.aliyun.com/zh/model-studio/qwen-omni-voice-cloning#h2-create)
-   [音色配置](raw/_short/livetranslate-realtime-voice-cloning-api-508d4787359474b9.md)
