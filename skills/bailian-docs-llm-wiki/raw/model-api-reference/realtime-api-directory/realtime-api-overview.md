# Realtime API 概述

了解 Realtime API 的协议选型、各模型的接入方式、AOQ SDK 和 Android Demo。

Realtime API 支持实时多模态交互、语音识别、语音合成、语音对话和音视频翻译。先选择传输协议和支持的模型，再进入对应系列的接入文档。

## 协议选型

Realtime API 支持 **AOQ（AI over QUIC）**、**WebRTC** 和 **WebSocket** 三种传输协议，开发者可以根据业务场景灵活选择。

**维度**

**AOQ**

**WebRTC**

**WebSocket**

适用场景

AI 多模态实时交互、弱网场景、混合数据传输

浏览器端互动、传统音视频通话

服务端集成、快速原型验证

浏览器兼容性

不支持

原生支持

原生支持

接入难度

低

中等

极低

弱网对抗

极致

良好

差

数据类型

音视频 + 文本

音视频 + 文本

文本/音频/图像

建连速度

快

慢

慢

回声消除/降噪

内置

内置

无，需客户端自行处理

AI 场景适配

原生为 AI 多模态数据特征深度定制

传统设计，AI 场景需额外适配

基础，适合纯文本或低实时性场景

端侧平台支持

移动端、桌面端和 Linux，详见 [AOQ SDK 下载](https://help.aliyun.com/zh/model-studio/realtime-sdk-download#sdkdl-h2-aoq)

浏览器、移动端

全平台（任何支持 WebSocket 的环境）

Token Plan

支持

支持

支持

开发者可根据实际需求选择协议方案：

-   **AOQ 方案**：适合对延迟、弱网对抗、多模态数据传输有极致要求的 AI 实时交互场景，同时内置回声消除和降噪能力，尤其是移动端原生应用。
-   **WebRTC 方案**：适合需要浏览器原生支持、已有 WebRTC 基础设施的传统音视频通话场景，内置回声消除和降噪能力。
-   **WebSocket 方案**：适合服务端集成、快速原型验证、对接入门槛要求极低的场景。通过 DashScope SDK 可快速实现实时语音对话。

## 模型与协议支持

下表列出各模型和应用支持的协议。点击「支持」查看对应的接入文档。

**模型/应用类型**

**模型**

**AOQ**

**WebRTC**

**WebSocket**

[实时全模态](raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory.md)

qwen3.8-omni-flash-realtime、qwen3.5-omni-plus-realtime、qwen3.5-omni-flash-realtime

[支持](raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory/omni-realtime-aoq-access.md)

[支持](raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory/omni-realtime-webrtc-access.md)

[支持](raw/_short/omni-realtime-websocket-access-3f16ac0799ebc899.md)

[实时语音合成](raw/model-api-reference/realtime-api-directory/realtime-tts-model-apis.md)

qwen-audio-3.1-tts-plus、qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-flash、qwen-audio-3.0-tts-plus

[支持](raw/model-api-reference/realtime-api-directory/realtime-tts-model-apis/qwen-audio-tts-api/qwen-audio-tts-aoq-access.md)

不支持

[支持](raw/_short/qwen-audio-tts-websocket-api-6f9e2d20cf04ea96.md)

CosyVoice系列模型

[支持](raw/_short/cosyvoice-aoq-access-c0e8e4035486f433.md)

不支持

[支持](raw/_short/cosyvoice-websocket-api-5929268331632771.md)

[实时语音识别](raw/model-api-reference/realtime-api-directory/realtime-asr-model-apis.md)

qwen-audio-3.1-asr-flash-message、qwen-audio-3.1-asr-flash-streaming、qwen-audio-3.0-asr-flash-streaming、Fun-ASR-Realtime系列模型

[支持](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide#c09d428f2crac)

不支持

[支持](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide#rt03_websocket_h3)

[实时语音对话](raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory.md)

qwen-audio-3.1-realtime-plus、qwen-audio-3.1-realtime-flash、qwen-audio-3.0-realtime-plus、qwen-audio-3.0-realtime-flash

[支持](raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory/audio-realtime-aoq-access.md)

[支持](raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory/audio-realtime-webrtc-access.md)

[支持](raw/_short/audio-realtime-websocket-access-5f0da4977f0f021b.md)

[实时语音翻译](raw/model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory.md)

Qwen-Livetranslate-Realtime 系列模型

[支持](raw/model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/livetranslate-realtime-aoq-access.md)

[支持](raw/_short/livetranslate-realtime-webrtc-access-ddb4e390439cd632.md)

[支持](raw/_short/livetranslate-realtime-websocket-access-69ee95b6726440dc.md)

[多模态开发套件](raw/application-user-guide/agent-development/application-gallery/multimodal-products/multimodal-products-overview.md)

multimodal-dialog

[支持](https://help.aliyun.com/zh/model-studio/multimodal-aoq-access#aoq)

[支持](raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)

[支持](raw/model-api-reference/realtime-api-directory/multimodal-interaction-protocol.md)

**说明**模型的名称、上下文、价格、快照版本等信息请参见[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/)；并发限流条件请参考[限流](raw/model-user-guide/get-started-with-models/rate-limit.md)。

## 接入准备

确认[调用地域和接入域名](raw/model-user-guide/get-started-with-models/regions.md)，获取该地域和业务空间对应的 [API Key](raw/model-api-reference/preparations/get-api-key.md)。

在上表点击所选模型和协议对应的「支持」，按接入文档完成鉴权、建连和事件交互。使用 AOQ 时，按客户端平台下载 [AOQ SDK](https://help.aliyun.com/zh/model-studio/realtime-sdk-download#sdkdl-h2-aoq)。

### 鉴权方式

Realtime API 使用 API Key 进行身份认证。无论选择 AOQ、WebRTC 还是 WebSocket 协议接入，均通过 HTTP 请求头中的 `Authorization` 字段携带 Bearer Token 完成身份验证。

鉴权仅发生在**建连阶段**，连接建立后的数据传输无需重复鉴权。

### 获取 API Key

#### 步骤 1：开通百炼服务

1.  访问[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/)并登录您的阿里云账号。
2.  如果是首次使用，按照页面提示完成服务开通。

#### 步骤 2：创建 [API Key](raw/model-api-reference/preparations/get-api-key.md)

1.  在控制台左侧导航栏中，选择 **API Key**。
2.  点击 **创建 API Key**，选择关联的业务空间。
3.  创建完成后，请**立即复制并妥善保存** API Key。

**重要****安全提示**：API Key 是您访问服务的唯一凭证，请勿将其硬编码到客户端代码中或提交到代码仓库。建议通过环境变量或后端服务下发的方式管理。

### 建连鉴权详解

#### AOQ 协议鉴权

AOQ 采用**服务端代理鉴权**模式：API Key 仅在业务 AppServer 侧使用，客户端通过网关返回的临时 Token 建连，避免 API Key 暴露在客户端。

模型系列

建连请求路径

Qwen-Omni-Realtime、Qwen-Audio-Realtime、Qwen-Livetranslate-Realtime

`/api/v1/webrtc/realtime`

Qwen-Audio-TTS、CosyVoice、Qwen-Audio-ASR-Streaming、Qwen-Audio-ASR-Message、Fun-ASR-Realtime

`/api/v1/webrtc/inference`

![Token鉴权](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3935914871/p1088069.jpg)

-   [Qwen-Omni-Realtime](https://help.aliyun.com/zh/model-studio/omni-realtime-aoq-access#authentication)
-   [Qwen-Audio-Realtime](https://help.aliyun.com/zh/model-studio/audio-realtime-aoq-access#authentication)
-   [Qwen-LiveTranslate-Realtime](https://help.aliyun.com/zh/model-studio/livetranslate-realtime-aoq-access#authentication)

#### WebRTC 协议鉴权

WebRTC 通过 HTTP POST 请求完成 SDP 交换，鉴权在此阶段完成。客户端将 Offer SDP 发送至服务端，服务端返回 Answer SDP。

-   [Qwen-Omni-Realtime](https://help.aliyun.com/zh/model-studio/omni-realtime-webrtc-access#authentication)
-   [Qwen-Audio-Realtime](https://help.aliyun.com/zh/model-studio/audio-realtime-webrtc-access#authentication)
-   [Qwen-LiveTranslate-Realtime](https://help.aliyun.com/zh/model-studio/livetranslate-realtime-webrtc-access#authentication)

#### WebSocket 协议鉴权

WebSocket 的鉴权方式最为简单，在建立连接时直接通过 HTTP Header 携带 API Key 即可。

-   [Qwen-Omni-Realtime](raw/_short/omni-realtime-websocket-access-3f16ac0799ebc899.md)
-   [Qwen-Audio-Realtime](raw/_short/audio-realtime-websocket-access-5f0da4977f0f021b.md)
-   [Qwen-LiveTranslate-Realtime](raw/_short/livetranslate-realtime-websocket-access-69ee95b6726440dc.md)

## 体验 Demo

使用 Android Demo 验证 AOQ 接入效果。扫描二维码下载 APK，安装后配置 API Key 和 `workspaceId`，即可体验 Demo 支持的部分模型。

![AOQ Android Demo 下载二维码](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/images/6a4b3c2d1e0f92cd.png)

## 最佳实践

-   [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
-   [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
-   [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
-   [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
-   [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
-   [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
-   [通过WebRTC使用多模态交互套件实现实时通话](raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
