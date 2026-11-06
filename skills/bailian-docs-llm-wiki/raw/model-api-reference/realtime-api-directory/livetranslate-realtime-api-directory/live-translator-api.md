# 实时音视频翻译

本目录提供 Qwen-LiveTranslate-Realtime 的 API 参考。系列指南列出的型号为 `qwen3.8-livetranslate-flash-realtime`、`qwen3.5-livetranslate-flash-realtime`、`qwen3.5-livetranslate-flash-realtime-2026-05-19`。Qwen-LiveTranslate-Realtime 系列支持 WebSocket、WebRTC 和 AOQ；各型号的配置和事件字段参见对应接入与事件文档。`qwen3.5-livetranslate-flash-realtime` 当前能力与快照版 `qwen3.5-livetranslate-flash-realtime-2026-05-19` 相同。媒体模态及事件字段的适用范围以对应接入和事件参考为准。

## 协议选型

以下对比描述协议的一般特性。表中的数据类型是协议可传输的类型，具体模型支持的输入和输出以接入文档为准。接入难度、弱网表现和建连速度为定性参考，实际体验受网络环境、设备和实现方式影响。

维度

[WebSocket 接入](raw/_short/livetranslate-realtime-websocket-access-69ee95b6726440dc.md)

[WebRTC 接入](raw/_short/livetranslate-realtime-webrtc-access-ddb4e390439cd632.md)

[AOQ 接入](raw/model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/livetranslate-realtime-aoq-access.md)

适用场景

服务端集成、快速原型验证

浏览器端互动、传统音视频通话

AI 多模态实时交互、弱网场景、混合数据传输

浏览器兼容性

原生支持

原生支持

不支持

接入难度

极低

中等

低

弱网对抗

差

良好

极致

协议传输的数据

文本、音频、图像

音视频、文本

音视频、文本

建连速度

慢

慢

快

回声消除与降噪

客户端自行处理

内置

内置

AI 场景适配

基础，适合纯文本或低实时性场景

传统设计，AI 场景需额外适配

原生为 AI 多模态数据特征定制

端侧平台

支持 WebSocket 的环境

浏览器、移动端

Android、iOS、HarmonyOS；其他 SDK 版本见接入页

浏览器原生支持 WebSocket，但接入模型时还需满足鉴权要求，不要在浏览器或移动端放置长期 API Key。

AOQ（AI over QUIC）Client SDK 提供 Android、iOS、HarmonyOS、Windows、macOS、Electron 和 Linux 版本，下载及各平台 API 参见 [AOQ 接入](raw/model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/livetranslate-realtime-aoq-access.md)。

## 事件及其他参考

-   [客户端事件](raw/model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-client-events.md)
-   [服务端事件](raw/model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-server-events.md)

## 音色

-   [预建音色 API](https://help.aliyun.com/zh/model-studio/voice-clone-design-http-api#h2-create)
-   [音色配置](raw/_short/livetranslate-realtime-voice-cloning-api-508d4787359474b9.md)

三种协议均可用于 Token Plan。可用模型和地域以 [Token Plan 个人版](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview#tpp01-h-models)及[团队版](https://help.aliyun.com/zh/model-studio/token-plan-team-overview#tpt01-h-models)的说明为准。
