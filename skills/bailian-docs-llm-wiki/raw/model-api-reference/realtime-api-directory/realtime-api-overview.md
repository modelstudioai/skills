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

确认[调用地域和接入域名](raw/model-user-guide/get-started-with-models/regions.md)，获取该地域和业务空间对应的 [API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)。

**说明**首次使用时，按控制台提示开通服务。创建后请立即复制并妥善保存 API Key，通过环境变量管理，勿嵌入客户端或提交到代码仓库。

使用 AOQ 时，按客户端平台下载 [AOQ SDK](https://help.aliyun.com/zh/model-studio/realtime-sdk-download#sdkdl-h2-aoq)。

### 鉴权方式

Realtime API 使用 API Key 进行身份认证。无论选择 AOQ、WebRTC 还是 WebSocket 协议接入，均通过 HTTP 请求头中的 `Authorization` 字段携带 Bearer Token 完成身份验证。

WebRTC 和 WebSocket 在建连时鉴权；AOQ 在 AppServer 请求连接凭证时使用 API Key 鉴权，客户端随后使用临时 Token 建连。连接建立后的数据传输无需重复鉴权。

### 建连鉴权详解

#### AOQ

AOQ 采用**服务端代理鉴权**模式：API Key 仅在业务 AppServer 侧使用，客户端通过网关返回的临时 Token 建连，避免 API Key 暴露在客户端。

#### 获取连接凭证

AOQ 支持即时鉴权和预鉴权两种方式：即时鉴权在业务需要建连时获取凭证，随即建立媒体连接；预鉴权提前获取并缓存凭证，业务需要时再建连，减少建连时等待信令 HTTP 请求的耗时。

#### 即时鉴权

业务需要媒体连接时，由 AppServer 请求连接凭证并返回客户端，客户端随即调用 `connect(config)` 建连。

![AOQ 即时鉴权与媒体建连时序](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/images/6a4b3c2d1e0f90b0.png)

#### 预鉴权

AppServer 提前请求连接凭证，客户端缓存完整连接参数，业务需要媒体连接时再调用 `connect(config)`。

Token 的默认有效期为 5 分钟；如需延长，请联系售后支持。Token 过期后，需重新获取连接凭证。

![AOQ 预鉴权与按需媒体建连时序](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/images/6a4b3c2d1e0f90bc.png)

#### 请求路径

模型系列

建连请求路径

Qwen-Omni-Realtime、Qwen-Audio-Realtime、Qwen-Livetranslate-Realtime

`/api/v1/webrtc/realtime`

Qwen-Audio-TTS、CosyVoice、Qwen-Audio-ASR-Streaming、Qwen-Audio-ASR-Message、Fun-ASR-Realtime

`/api/v1/webrtc/inference`

#### 请求说明

参数

位置与类型

说明

`{endpoint}`

URL · `string`

必填。使用所选地域和业务空间的[接入域名](raw/model-user-guide/get-started-with-models/regions.md)。使用 Token Plan 时，域名中的 `WorkspaceId` 固定为 `token-plan`。

`model`

查询参数 · `string`

必填。待调用的模型 ID，建连路径按上表中的模型系列选择。

`Authorization`

请求头 · `string`

必填。格式为 `Bearer <API_KEY>`，使用与接入域名对应的 API Key。

`Content-Type`

请求头 · `string`

必填。固定为 `application/json`。

`x-dashscope-rtc-transport`

请求头 · `string`

必填。固定为 `moq`，指定使用 AOQ 协议。

`clientIp`

请求体 · `string`

选填。客户端真实公网 IP，用于选择 Relay 接入点；不传时使用请求来源 IP。

`serverPassiveConnect`

请求体 · `boolean`

选填。传 `true` 时使用预鉴权模式；不传时使用即时鉴权模式。此参数仅用于请求网关，无需在 `AoqConnectConfig` 中新增字段。

以下以 qwen3.8-omni-flash-realtime 为例，使用对应的 `{endpoint}` 和环境变量 `DASHSCOPE_API_KEY`。调用 Inference 路径的模型时，将请求路径改为 `/api/v1/webrtc/inference`，并设置对应的 `model`。

#### 即时鉴权请求

```
curl -X POST \
  "https://{endpoint}/api/v1/webrtc/realtime?model=qwen3.8-omni-flash-realtime" \
  -H "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "x-dashscope-rtc-transport: moq" \
  -d '{}'
```

#### 预鉴权请求

```
curl -X POST \
  "https://{endpoint}/api/v1/webrtc/realtime?model=qwen3.8-omni-flash-realtime" \
  -H "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "x-dashscope-rtc-transport: moq" \
  -d '{"serverPassiveConnect":true}'
```

#### 返回说明

字段

类型

说明与 SDK 映射

`sid`

`string`

会话唯一标识，填入 `AoqConnectConfig.sid`。

`aoqTokenForClient`

`string`

客户端临时连接 Token，填入 `AoqConnectConfig.token`。

`clientRelayEndpoints`

`array`

Relay 接入点数组，填入 `relayEndpoints`。每项包含 `endpoint`、`port` 和 `route_index`；将 `route_index` 映射为 SDK 的 `routeIndex`，缺省时使用数组下标。

`clientRelayCertFingerprint`

`string`

Relay TLS 证书指纹，填入 `AoqConnectConfig.certFingerprint`。

`sidExpiresInSecs`

`integer`

会话有效期，单位为秒。不能用它代替预获取 Token 的可用时间。

`extraInfo.workspaceIdHash`

`string`

业务空间 ID 的哈希值，填入 `AoqConnectConfig.workspaceIdHash`。

两种模式的响应结构相同。下例为即时鉴权的响应示例，字段值以实际返回为准。

```
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

#### WebRTC

WebRTC 通过 HTTP POST 请求完成 SDP 交换，鉴权在此阶段完成。客户端将 Offer SDP 发送至服务端，服务端返回 Answer SDP。

-   [Qwen-Omni-Realtime](https://help.aliyun.com/zh/model-studio/omni-realtime-webrtc-access#authentication)
-   [Qwen-Audio-Realtime](https://help.aliyun.com/zh/model-studio/audio-realtime-webrtc-access#authentication)
-   [Qwen-LiveTranslate-Realtime](https://help.aliyun.com/zh/model-studio/livetranslate-realtime-webrtc-access#authentication)

#### WebSocket

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
