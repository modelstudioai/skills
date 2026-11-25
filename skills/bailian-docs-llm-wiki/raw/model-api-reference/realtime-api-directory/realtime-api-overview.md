# Realtime API 概述

了解 Realtime API 支持的模型、接入方式、鉴权流程及现有教程和 Demo。

Realtime API 支持实时多模态交互、语音识别、语音合成、语音对话和音视频翻译。先查找所需模型支持的接入方式，再根据应用场景选择并进入对应的接入文档。

<a id="模型与协议支持"></a>

<a id="rtov-s02h2"></a>

## 模型与协议支持

<a id="选择模型"></a>

下表列出各模型和应用支持的协议。点击“支持”查看对应的接入文档。

<table><thead><tr><th><strong>模型/应用类型</strong></th><th><strong>模型</strong></th><th><strong>WebSocket</strong></th><th><strong>WebRTC</strong></th><th><strong>AOQ</strong></th></tr></thead><tbody><tr><td><p><a href="omni-realtime-api-directory.md">实时全模态</a></p></td><td><p>qwen3.8-omni-flash-realtime、qwen3.5-omni-plus-realtime、qwen3.5-omni-flash-realtime</p></td><td><p><a href="omni-realtime-api-directory/omni-realtime-websocket-access.md">支持</a></p></td><td><p><a href="omni-realtime-api-directory/omni-realtime-webrtc-access.md">支持</a></p></td><td><p><a href="omni-realtime-api-directory/omni-realtime-aoq-access.md">支持</a></p></td></tr><tr><td rowspan="2"><p><a href="realtime-tts-model-apis.md">实时语音合成</a></p></td><td><p>qwen-audio-3.1-tts-plus、qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-flash、qwen-audio-3.0-tts-plus</p></td><td><p><a href="../../_short/qwen-audio-tts-websocket-api-6f9e2d20cf04ea96.md">支持</a></p></td><td><p>不支持</p></td><td><p><a href="realtime-tts-model-apis/qwen-audio-tts-api/qwen-audio-tts-aoq-access.md">支持</a></p></td></tr><tr><td><p>CosyVoice系列模型</p></td><td><p><a href="../../_short/cosyvoice-websocket-api-5929268331632771.md">支持</a></p></td><td><p>不支持</p></td><td><p><a href="../../_short/cosyvoice-aoq-access-c0e8e4035486f433.md">支持</a></p></td></tr><tr><td><p><a href="realtime-asr-model-apis.md">实时语音识别</a></p></td><td><p>qwen-audio-3.1-asr-flash-message、qwen-audio-3.1-asr-flash-streaming、qwen-audio-3.0-asr-flash-streaming、Fun-ASR-Realtime系列模型</p></td><td><p><a href="../../_short/qwen-asr-message-websocket-api-8b78d8662335cafa.md">Qwen-Audio-ASR-Message</a></p><p><a href="../../_short/qwen-audio-asr-streaming-websocket-api-779f1056a08e5525.md">Qwen-Audio-ASR-Streaming</a></p><p><a href="../../_short/fun-asr-realtime-websocket-api-ba4d50025cae8d1c.md">Fun-ASR-Realtime</a></p></td><td><p>不支持</p></td><td><p><a href="../../_short/qwen-asr-message-aoq-access-7699c2c24f2a0149.md">Qwen-Audio-ASR-Message</a></p><p><a href="../../_short/qwen-audio-asr-streaming-aoq-access-7b2cf295190f6172.md">Qwen-Audio-ASR-Streaming</a></p><p><a href="../../_short/fun-asr-realtime-aoq-access-18b59bd85ad6d915.md">Fun-ASR-Realtime</a></p></td></tr><tr><td><p><a href="audio-realtime-api-directory.md">实时语音对话</a></p></td><td><p>qwen-audio-3.1-realtime-plus、qwen-audio-3.1-realtime-flash、qwen-audio-3.0-realtime-plus、qwen-audio-3.0-realtime-flash</p></td><td><p><a href="audio-realtime-api-directory/audio-realtime-websocket-access.md">支持</a></p></td><td><p><a href="audio-realtime-api-directory/audio-realtime-webrtc-access.md">支持</a></p></td><td><p><a href="audio-realtime-api-directory/audio-realtime-aoq-access.md">支持</a></p></td></tr><tr><td><p><a href="qwen-audio-live-api-directory.md">Qwen-Audio-Live</a></p></td><td><p><code>qwen-audio-3.1-live</code></p></td><td><p><a href="qwen-audio-live-api-directory/qwen-audio-live-websocket-access.md">支持</a></p></td><td><p><a href="../../_short/qwen-audio-live-webrtc-access-2a873a21a2d29a3b.md">支持</a></p></td><td><p><a href="../../_short/qwen-audio-live-aoq-access-7fc752b6a8e53044.md">支持</a></p></td></tr><tr><td><p><a href="livetranslate-realtime-api-directory.md">实时语音翻译</a></p></td><td><p>Qwen-Livetranslate-Realtime 系列模型</p></td><td><p><a href="../../_short/livetranslate-realtime-websocket-access-c83c6ed44456849c.md">支持</a></p></td><td><p><a href="../../_short/livetranslate-realtime-webrtc-access-ddb4e390439cd632.md">支持</a></p></td><td><p><a href="livetranslate-realtime-api-directory/livetranslate-realtime-aoq-access.md">支持</a></p></td></tr><tr><td><p><a href="../../application-user-guide/agent-development/application-gallery/multimodal-products/multimodal-products-overview.md">多模态开发套件</a></p></td><td><p>multimodal-dialog</p></td><td><p><a href="../more-about-models/multimodal-interaction-protocol.md">支持</a></p></td><td><p><a href="../../model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md">支持</a></p></td><td><p><a href="../../_short/multimodal-aoq-access-86d2558b6e5bb42e.md#aoq">支持</a></p></td></tr></tbody></table>

> **说明**
>
> 模型的名称、上下文、价格、快照版本等信息请参见[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/)；并发限流条件请参考[限流](../../model-user-guide/get-started-with-models/rate-limit.md)。

<a id="按模型查找-websocket-sdk"></a>

<a id="websocket-sdk"></a>

## 按模型查找 WebSocket SDK

| 模型 | 开发语言和平台 |
| --- | --- |
| Qwen-Omni-Realtime | [Python](../../_short/realtime-websocket-python-sdk-qwen-omni-realtime-e50924065f85dda8.md) · [Java](../../_short/omni-realtime-java-sdk-13dfd16f685872d7.md) · [C#](../../_short/omni-realtime-csharp-sdk-f5e5dc6601296458.md) |
| Qwen-Audio-ASR-Streaming | [Python](../../_short/qwen-audio-asr-streaming-websocket-sdk-python-d3f6f03216a64996.md) · [Java](../../_short/qwen-audio-asr-streaming-websocket-sdk-java-923284a83b541f4a.md) · [Node.js](../../_short/qwen-audio-asr-streaming-websocket-sdk-nodejs-8175ebf0edea3f44.md) · [C#](../../_short/qwen-audio-asr-streaming-websocket-sdk-csharp-d4cdd1f28e10e1ee.md) · [Android](../../_short/qwen-audio-asr-streaming-websocket-sdk-android-a883b456b530c951.md) · [iOS](../../_short/qwen-audio-asr-streaming-websocket-sdk-ios-5a7e89574b8cdbfe.md) · [HarmonyOS](../../_short/qwen-audio-asr-streaming-websocket-sdk-harmonyos-c35c7ad324ec7afe.md) · [Flutter](../../_short/qwen-audio-asr-streaming-websocket-sdk-flutter-bae77e53068468b6.md) |
| Qwen-Audio-ASR-Message | [Python](../../_short/qwen-asr-message-websocket-sdk-python-06f03701cdddda13.md) · [Java](../../_short/qwen-asr-message-websocket-sdk-java-4524c054fb74f217.md) · [Node.js](../../_short/qwen-asr-message-websocket-sdk-nodejs-627576e97b262b0a.md) · [C#](../../_short/qwen-asr-message-websocket-sdk-csharp-7aa85c2b1a5a929c.md) · [Android](../../_short/qwen-asr-message-websocket-sdk-android-b9e8e19722b5d570.md) · [iOS](../../_short/qwen-asr-message-websocket-sdk-ios-fb447b88c464d9d4.md) · [HarmonyOS](../../_short/qwen-asr-message-websocket-sdk-harmonyos-98cb0f5731fef1cb.md) · [Flutter](../../_short/qwen-asr-message-websocket-sdk-flutter-1042f8131f3deccc.md) |
| Fun-ASR-Realtime | [Python](../../_short/fun-asr-realtime-websocket-sdk-python-56ba4399a24fcf69.md) · [Java](../../_short/fun-asr-realtime-websocket-sdk-java-ec987af1c2fd19d4.md) · [C#](../../_short/fun-asr-realtime-csharp-sdk-cb1c36fb275d548c.md) · [Android](../../_short/fun-asr-realtime-websocket-sdk-android-263995507ca5b758.md) · [iOS](../../_short/fun-asr-realtime-websocket-sdk-ios-1698818bdb0dee85.md) · [HarmonyOS](../../_short/fun-asr-realtime-websocket-sdk-harmonyos-4bd03211debbdd3f.md) · [Flutter](../../_short/fun-asr-realtime-websocket-sdk-flutter-237f299ab91e973a.md) |
| Qwen-ASR-Realtime | [Python](../../_short/realtime-websocket-python-sdk-qwen-asr-realtime-281dee62f7074a94.md) · [Java](../../_short/qwen-asr-realtime-java-sdk-d0faa50c48463b79.md) |
| Paraformer | [Python](../../_short/realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md) · [Java](../../_short/paraformer-real-time-speech-recognition-java-sdk-7a1a7974a8aacc5d.md) · [C#](../../_short/paraformer-realtime-csharp-sdk-0af0d0018568b776.md) · [Android](../../_short/android-sdk-for-paraformer-real-time-service-9e7815d0b3adcb41.md) · [iOS](../../_short/ios-sdk-for-paraformer-real-time-service-28718b821c8d6e25.md) · [HarmonyOS](../../_short/harmonyos-sdk-for-paraformer-real-time-service-642577184b92b90f.md) · [Flutter](../../_short/realtime-websocket-flutter-sdk-paraformer-ce62061a08ebbb55.md) |
| Qwen-Audio-TTS | [Python](../../_short/qwen-audio-tts-websocket-sdk-python-74a72caa32997dec.md) · [Java](../../_short/qwen-audio-tts-websocket-sdk-java-ec88c8d98488df37.md) · [Node.js](../../_short/qwen-audio-tts-nodejs-sdk-e49b9390f1cc4802.md) · [C#](../../_short/qwen-audio-tts-websocket-sdk-csharp-4b86003f8b25dbbd.md) · [Android](../../_short/qwen-audio-tts-websocket-sdk-android-deab75c7b0d9709a.md) · [iOS](../../_short/qwen-audio-tts-websocket-sdk-ios-20133baf35bd9806.md) · [HarmonyOS](../../_short/qwen-audio-tts-websocket-sdk-harmonyos-3937eb409e9f327d.md) · [Flutter](../../_short/qwen-audio-tts-websocket-sdk-flutter-44fc29e41055a783.md) |
| CosyVoice | [Python](../../_short/cosyvoice-websocket-sdk-python-47e109e34183e539.md) · [Java](../../_short/cosyvoice-websocket-sdk-java-a4920147be4869ef.md) · [C#](../../_short/cosyvoice-websocket-sdk-csharp-c2c2b009e6d5a87f.md) · [Android](../../_short/cosyvoice-websocket-sdk-android-a3c227256eefa5f2.md) · [iOS](../../_short/cosyvoice-websocket-sdk-ios-906cc4f70118010a.md) · [HarmonyOS](../../_short/cosyvoice-websocket-sdk-harmonyos-340ad797fa66e3f1.md) · [Flutter](../../_short/cosyvoice-websocket-sdk-flutter-14e4f441e1c1f2d6.md) |
| Qwen-TTS-Realtime | [Python](../../_short/realtime-websocket-python-sdk-qwen-tts-realtime-3dc71548ffc651f8.md) · [Java](../../_short/qwen-tts-realtime-java-sdk-9494aeb08ebf2190.md) |
| Sambert | [Python](../../_short/realtime-websocket-python-sdk-sambert-74c648d694dcfd04.md) · [Java](../../_short/sambert-java-sdk-79ed7a3fed2f3f90.md) · [C#](../../_short/sambert-csharp-sdk-3727135a614c5624.md) · [Android](../../_short/sambert-android-sdk-8827dfd4fba2386d.md) · [iOS](../../_short/sambert-ios-sdk-3a58fd71fde42af6.md) · [HarmonyOS](../../_short/sambert-harmonyos-sdk-6ffde1be395ffb11.md) · [Flutter](../../_short/realtime-websocket-flutter-sdk-sambert-d02804b097bac96d.md) |
| Qwen-Audio-Realtime | [Node.js](../../_short/qwen-audio-realtime-nodejs-sdk-a2a0cc33ba0a85a8.md) · [C#](../../_short/qwen-audio-realtime-csharp-sdk-7c78b8d6a3bc97a4.md) · [Android](../../_short/android-sdk-for-qwen-audio-realtime-service-fbe978d80b5ee150.md) · [iOS](../../_short/ios-sdk-for-qwen-audio-realtime-service-11c3579f6cded913.md) · [HarmonyOS](../../_short/harmonyos-sdk-for-qwen-audio-realtime-service-c258297df757a167.md) · [Flutter](../../_short/realtime-websocket-flutter-sdk-qwen-audio-realti-8fa612950516022e.md) |
| Qwen-LiveTranslate-Realtime | [Python](../../_short/realtime-websocket-python-sdk-qwen-livetranslate-8af00207378f749b.md) · [Java](../../_short/qwen-livetranslate-java-sdk-7300d52ae3d2839e.md) · [C#](../../_short/qwen-livetranslate-csharp-sdk-7dc0bd18d993e44e.md) · [Flutter](../../_short/realtime-websocket-flutter-sdk-qwen-livetranslat-ed4e5a3a77d23fdf.md) |

**C# 通用参考** [SDK简介](https://help.aliyun.com/zh/model-studio/csharp-sdk) · [接口与事件](https://help.aliyun.com/zh/model-studio/csharp-sdk-methods-and-events)

<a id="接入方式选择"></a>

<a id="rtov-protocol-selection"></a>

<a id="协议选型"></a>

## 接入方式选择

Realtime API 支持 WebSocket、WebRTC 和 AOQ（AI over QUIC）三种接入方式。可用方式及输入、输出能力以所选模型的接入文档为准。

| 维度 | WebSocket | WebRTC | AOQ |
| --- | --- | --- | --- |
| 适用场景 | 实时语音和多模态交互、服务端集成、快速原型验证 | 浏览器实时音视频交互、已有 WebRTC 基础设施的应用 | 需要弱网优化及音视频、模型事件协同传输的原生应用 |
| 浏览器兼容性 | 原生支持；需满足对应接口的鉴权要求 | 原生支持 | 当前 AOQ SDK 不提供浏览器接入 |
| 回声消除/降噪 | 由客户端使用的音频采集与处理组件提供 | 由浏览器或 WebRTC 客户端提供，依平台与配置而定 | 以所用平台的 AOQ SDK 音频配置为准 |
| 端侧平台支持 | 全平台（任何支持 WebSocket 的环境） | 浏览器、移动端 | 移动端、桌面端和 Linux，详见 [AOQ SDK 下载](../more-about-models/realtime-api-aoq-api/realtime-sdk-download.md#sdkdl-h2-aoq) |
| Token Plan | 支持 | 支持 | 支持 |

-   **WebSocket**：适用于实时语音和多模态交互、服务端集成及原型验证。通过 DashScope SDK 可快速实现实时语音对话。
-   **WebRTC**：适用于需要浏览器原生支持或已有 WebRTC 基础设施的实时音视频交互。
-   **AOQ**：AOQ 基于 QUIC，面向弱网下的实时交互进行优化，支持音视频与模型事件分轨传输，适用于需要集成媒体采集、编解码和播放能力的原生应用。

<a id="接入准备"></a>

<a id="conn-connection-options"></a>

## 接入准备

<a id="接入概览"></a>

<a id="选择接入方式"></a>

<a id="接入方式"></a>

<a id="前提条件"></a>

<a id="e0343a5555n5u"></a>

<a id="通过-aoq-接入"></a>

<a id="conn-aoq-title"></a>

<a id="conn-aoq-seq-title"></a>

<a id="conn-aoq-create-title"></a>

<a id="conn-aoq-audio-title"></a>

<a id="conn-aoq-token-title"></a>

<a id="conn-aoq-codec-title"></a>

<a id="conn-aoq-session-title"></a>

<a id="conn-aoq-updated-title"></a>

<a id="conn-aoq-disconnect-title"></a>

<a id="aoq-接入"></a>

<a id="通过-webrtc-接入"></a>

<a id="conn-rtc-title"></a>

<a id="conn-rtc-seq-title"></a>

<a id="conn-rtc-connect-title"></a>

<a id="conn-rtc-config-title"></a>

<a id="conn-rtc-media-title"></a>

<a id="conn-rtc-demo-title"></a>

<a id="conn-rtc-demo-prereq-title"></a>

<a id="conn-rtc-demo-run-title"></a>

<a id="conn-rtc-auth-params"></a>

<a id="conn-rtc-initialize"></a>

<a id="conn-rtc-media-example"></a>

<a id="conn-rtc-channel-create"></a>

<a id="conn-rtc-connect-code"></a>

<a id="conn-rtc-event-example"></a>

<a id="conn-rtc-release"></a>

<a id="conn-rtc-data-channel"></a>

<a id="conn-rtc-data-code"></a>

<a id="webrtc-接入"></a>

<a id="通过-websocket-接入"></a>

<a id="conn-ws-title"></a>

<a id="websocket-接入"></a>

<a id="tkauth-get-apikey-title"></a>

<a id="步骤-1-开通百炼服务"></a>

<a id="tkauth-get-apikey-step1-title"></a>

<a id="步骤-2-创建-api-key"></a>

<a id="tkauth-get-apikey-step2-title"></a>

<a id="获取-api-key"></a>

确认[调用地域和接入域名](../../model-user-guide/get-started-with-models/regions.md)，获取该地域和业务空间对应的 [API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)。

> **说明**
>
> 首次使用时，按控制台提示开通服务。创建后请立即复制并妥善保存 API Key，通过环境变量管理，勿嵌入客户端或提交到代码仓库。

使用 AOQ 时，按客户端平台下载 [AOQ SDK](../more-about-models/realtime-api-aoq-api/realtime-sdk-download.md#sdkdl-h2-aoq)。

<a id="鉴权方式"></a>

<a id="tkauth-authentication-methods"></a>

### 鉴权方式

Realtime API 使用 API Key 进行身份认证。无论选择 AOQ、WebRTC 还是 WebSocket 协议接入，均通过 HTTP 请求头中的 `Authorization` 字段携带 Bearer Token 完成身份验证。

WebRTC 和 WebSocket 在建连时鉴权；AOQ 在 AppServer 请求连接凭证时使用 API Key 鉴权，客户端随后使用临时 Token 建连。连接建立后的数据传输无需重复鉴权。

<a id="建连鉴权详解"></a>

<a id="tkauth-auth-detail-title"></a>

### 建连鉴权详解

<a id="aoq-协议鉴权"></a>

<a id="tkauth-aoq-title"></a>

<a id="webrtc-协议鉴权"></a>

<a id="tkauth-webrtc-title"></a>

<a id="websocket-协议鉴权"></a>

<a id="tkauth-websocket-title"></a>

<a id="sec-tabs"></a>

<a id="websocket"></a>

<a id="websocket-h4"></a>

#### WebSocket

WebSocket 在建立连接时通过 HTTP 请求头携带 API Key 进行鉴权，具体要求参见对应模型的接入文档。

-   [Qwen-Omni-Realtime](omni-realtime-api-directory/omni-realtime-websocket-access.md)
-   [Qwen-Audio-TTS](../../_short/qwen-audio-tts-websocket-api-6f9e2d20cf04ea96.md)
-   [CosyVoice](../../_short/cosyvoice-websocket-api-5929268331632771.md)
-   [Qwen-Audio-ASR-Message](../../_short/qwen-asr-message-websocket-api-8b78d8662335cafa.md)
-   [Qwen-Audio-ASR-Streaming](../../_short/qwen-audio-asr-streaming-websocket-api-779f1056a08e5525.md)
-   [Fun-ASR-Realtime](../../_short/fun-asr-realtime-websocket-api-ba4d50025cae8d1c.md)
-   [Qwen-Audio-Realtime](audio-realtime-api-directory/audio-realtime-websocket-access.md)
-   [Qwen-LiveTranslate-Realtime](../../_short/livetranslate-realtime-websocket-access-c83c6ed44456849c.md)
-   [多模态开发套件](../more-about-models/multimodal-interaction-protocol.md)

<a id="webrtc"></a>

<a id="webrtc-h4"></a>

#### WebRTC

Qwen-Audio-Live 使用控制 WebSocket 提交 Offer SDP，在建立 WebSocket 连接时鉴权。见 [Qwen-Audio-Live WebRTC 接入](../../_short/qwen-audio-live-webrtc-access-2a873a21a2d29a3b.md)。

以下模型通过 HTTP POST 交换 SDP，并在这一阶段鉴权。客户端发送 Offer SDP，服务端返回 Answer SDP。

-   [Qwen-Omni-Realtime](omni-realtime-api-directory/omni-realtime-webrtc-access.md#authentication)
-   [Qwen-Audio-Realtime](audio-realtime-api-directory/audio-realtime-webrtc-access.md#authentication)
-   [Qwen-LiveTranslate-Realtime](../../_short/livetranslate-realtime-webrtc-access-ddb4e390439cd632.md#authentication)

<a id="aoq"></a>

<a id="aoq-h4"></a>

#### AOQ

AOQ 采用**服务端代理鉴权**模式：API Key 仅在业务 AppServer 侧使用，客户端通过网关返回的临时 Token 建连，避免 API Key 暴露在客户端。

<a id="参数说明"></a>

<a id="响应示例"></a>

<a id="响应参数说明"></a>

<a id="aoq-client-sdk-连接示例"></a>

<a id="aoq-token-prefetch"></a>

#### 获取连接凭证

业务需要媒体连接时，由 AppServer 请求连接凭证并返回客户端，客户端随即调用 `connect(config)` 建连。

![AOQ 即时鉴权与媒体建连时序](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/images/6a4b3c2d1e0f90b0.png)

<a id="aoq-request-paths"></a>

#### 请求路径

| 模型系列 | 建连请求路径 |
| --- | --- |
| Qwen-Omni-Realtime、Qwen-Audio-Realtime、Qwen-Livetranslate-Realtime | `/api/v1/webrtc/realtime` |
| Qwen-Audio-TTS、CosyVoice、Qwen-Audio-ASR-Streaming、Qwen-Audio-ASR-Message、Fun-ASR-Realtime | `/api/v1/webrtc/inference` |

<a id="tkauth-aoq-request-fields-title"></a>

#### 请求说明

| 参数 | 位置与类型 | 说明 |
| --- | --- | --- |
| `{endpoint}` | URL · `string` | 必填。使用所选地域和业务空间的[接入域名](../../model-user-guide/get-started-with-models/regions.md)。使用 Token Plan 时，域名中的 `WorkspaceId` 固定为 `token-plan`。 |
| `model` | 查询参数 · `string` | 必填。待调用的模型 ID，建连路径按上表中的模型系列选择。 |
| `Authorization` | 请求头 · `string` | 必填。格式为 `Bearer <API_KEY>`，使用与接入域名对应的 API Key。 |
| `Content-Type` | 请求头 · `string` | 必填。固定为 `application/json`。 |
| `x-dashscope-rtc-transport` | 请求头 · `string` | 必填。固定为 `moq`，指定使用 AOQ 协议。 |
| `clientIp` | 请求体 · `string` | 选填。客户端真实公网 IP，用于选择 Relay 接入点；不传时使用请求来源 IP。 |

以下以 qwen3.8-omni-flash-realtime 为例，使用对应的 `{endpoint}` 和环境变量 `DASHSCOPE_API_KEY`。调用 Inference 路径的模型时，将请求路径改为 `/api/v1/webrtc/inference`，并设置对应的 `model`。

<a id="code-block"></a>

```bash
curl -X POST \
  "https://{endpoint}/api/v1/webrtc/realtime?model=qwen3.8-omni-flash-realtime" \
  -H "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "x-dashscope-rtc-transport: moq" \
  -d '{}'
```

<a id="tkauth-aoq-response-fields-title"></a>

#### 返回说明

| 字段 | 类型 | 说明与 SDK 映射 |
| --- | --- | --- |
| `sid` | `string` | 会话唯一标识，填入 `AoqConnectConfig.sid`。 |
| `aoqTokenForClient` | `string` | 客户端临时连接 Token，填入 `AoqConnectConfig.token`。 |
| `clientRelayEndpoints` | `array` | Relay 接入点数组，填入 `relayEndpoints`。每项包含 `endpoint`、`port` 和 `route_index`；将 `route_index` 映射为 SDK 的 `routeIndex`，缺省时使用数组下标。 |
| `clientRelayCertFingerprint` | `string` | Relay TLS 证书指纹，填入 `AoqConnectConfig.certFingerprint`。 |
| `sidExpiresInSecs` | `integer` | 会话有效期（秒）。过期后需重新获取，否则建立连接将失败。 |
| `extraInfo.workspaceIdHash` | `string` | 业务空间 ID 的哈希值，填入 `AoqConnectConfig.workspaceIdHash`。 |

<a id="tkauth-aoq-response-title"></a>

以下为响应示例，字段值以实际返回为准。

<a id="code-block-2"></a>

```json
{
  "sid": "<session_id>",
  "aoqTokenForClient": "<token>",
  "clientRelayEndpoints": [
    {"endpoint": "192.0.2.1", "port": 8443, "route_index": 0}
  ],
  "clientRelayCertFingerprint": "sha256/<fingerprint>",
  "sidExpiresInSecs": 7200,
  "extraInfo": {"workspaceIdHash": "<workspace_id_hash>"}
}
```

<a id="tkauth-aoq-sdk-title"></a>

<a id="开发资源"></a>

<a id="0a7555f0aasb3"></a>

<a id="最佳实践"></a>

<a id="教程与体验"></a>

## 开发资源

<a id="webrtc-教程"></a>

<a id="conn-rtc-best-practices"></a>

### WebRTC 教程

-   [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
-   [通过WebRTC使用多模态交互套件实现实时通话](../../model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)

<a id="aoq-教程与-demo"></a>

<a id="conn-aoq-best-practices"></a>

<a id="aoq-教程与-android-demo"></a>

### AOQ 教程与 Demo

-   [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
-   [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
-   [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)
-   [使用 AOQ 接入 qwen3.8-livetranslate-flash-realtime 实现实时语音翻译](../../_short/real-time-translation-using-aoq-access-qwen-live-9b4d3056b2eade2b.md)
-   [使用 AOQ 接入 qwen-audio-3.1-tts-flash 实现语音合成](../../_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
-   [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
-   [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)

<a id="conn-demo-title"></a>

<a id="体验-demo"></a>

使用 Android Demo 验证 AOQ 接入效果。扫描二维码下载 APK，安装后配置 API Key 和 `workspaceId`，即可体验 Demo 支持的部分模型。

![AOQ Android Demo 下载二维码](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/images/6a4b3c2d1e0f92cd.png)
