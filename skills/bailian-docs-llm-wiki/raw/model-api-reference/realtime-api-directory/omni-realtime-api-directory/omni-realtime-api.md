# 实时多模态

Qwen-Omni-Realtime 可结合语音和画面进行实时对话。模型接收文本、流式音频和视觉输入，可返回文本和音频。

`qwen3.8-omni-flash-realtime`、`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime` 均支持 WebSocket、WebRTC 和 AOQ。历史型号 `qwen3-omni-flash-realtime-2025-09-15` 的 WebSocket 资料参见 [Python SDK](raw/_short/omni-realtime-python-sdk-0d3c931c58118ee5.md)和[客户端事件](raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory/client-events.md)。

## 协议选型

选择协议时，可先查看 [Realtime API 接入方式选择](https://help.aliyun.com/zh/model-studio/realtime-api-overview#rtov-protocol-selection)。各型号支持的输入、输出和事件字段见对应的接入与事件参考。

-   通过 [WebSocket](raw/_short/omni-realtime-websocket-access-3f16ac0799ebc899.md) 发送图片或视频帧时，需先发送至少一次音频输入事件，再发送图像事件。
    
    浏览器原生支持 WebSocket。接入模型时仍需满足鉴权要求，长期 API Key 应保存在服务端。
    
-   [WebRTC](raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory/omni-realtime-webrtc-access.md) 通过音频轨道收发语音、通过视频轨道发送画面，模型事件走 DataChannel。仅支持用语音活动检测（VAD）自动划分轮次。
    
-   [AOQ（AI over QUIC）](raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory/omni-realtime-aoq-access.md) 使用 Client SDK 收发音频和发送画面，模型事件走独立的 Data 轨。
    
    Client SDK 支持 Android、iOS、HarmonyOS、Windows、macOS、Electron 和 Linux。接入文档提供各平台的下载入口和 API 参考。
    

三种协议均可用于 Token Plan。可用模型和地域以 [Token Plan 个人版](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview#tpp01-h-models)及[团队版](https://help.aliyun.com/zh/model-studio/token-plan-team-overview#tpt01-h-models)的说明为准。

## 事件及其他参考

-   [客户端事件](raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory/client-events.md)
-   [服务端事件](raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory/server-events.md)

## 音色

-   [音色复刻 API](https://help.aliyun.com/zh/model-studio/qwen-omni-voice-cloning#h2-create)
