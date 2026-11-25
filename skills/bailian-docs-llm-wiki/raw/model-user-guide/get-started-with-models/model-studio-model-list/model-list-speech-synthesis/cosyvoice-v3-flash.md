# cosyvoice-v3-flash

合成能力：CosyVoice-v3-Flash是通义实验室CosyVoice系列高性能的语音合成大模型，较之前版本在自然度、音质、韵律、情感表现力上有更好的表现。该模型支持文本至语音的实时流式合成。克隆能力：CosyVoice-v3-Flash也是通义实验室CosyVoice系列语音克隆大模型，较之前版本提升了发音准确性、音色相似度，并且增加了更多小语种支持（德、西、法、意、俄）。仅需提供5-20s的参考音频，即可迅速生成高度相似且听感自然的定制声音。

<a id="推理服务供应商"></a>

<a id="h-490b2834e6"></a>

## 推理服务供应商

`cosyvoice-v3-flash`模型的推理服务供应商为阿里云百炼。

<a id="模型能力"></a>

<a id="h-77230e94b5"></a>

## 模型能力

| 能力项 | 支持情况 | 能力项 | 支持情况 |
| --- | --- | --- | --- |
| 输入模态 | **Text** | 输出模态 | **Audio** |
| 模型体验 | 不支持 | Function Calling | 不支持 |
| 结构化输出 | 不支持 | 联网搜索 | 不支持 |
| 前缀续写 | 不支持 | 上下文缓存 | 不支持 |
| 批量推理 | 不支持 | 模型调优 | 不支持 |

<a id="上下文限制"></a>

<a id="h-01b911f555"></a>

## 上下文限制

| 参数 | 值 | 参数 | 值 |
| --- | --- | --- | --- |
| 最大输入长度 | — | 最大输出长度 | — |
| 上下文长度 | — |  |  |

<a id="模型价格"></a>

<a id="h-2d8300ccf8"></a>

## 模型价格

本文仅展示模型调用原价，不包含限时优惠等活动信息，请前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)查看活动优惠。

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

| 计费项 | 价格（元） | 单位 |
| --- | --- | --- |
| 语音合成 | 1 | 每万字符 |

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

部署范围：国际

| 计费项 | 价格（元） | 单位 |
| --- | --- | --- |
| 语音合成 | 0.9541 | 每万字符 |

<a id="限流"></a>

<a id="h-e5f4959165"></a>

## 限流

<a id="sec-tabs-2"></a>

<a id="华北2-北京-2"></a>

<a id="华北2-北京-2-h4"></a>

#### 华北2（北京）

| 参数 | 值 |
| --- | --- |
| RPM（每分钟请求数） | 180 |

<a id="新加坡-2"></a>

<a id="新加坡-2-h4"></a>

#### 新加坡

部署范围：国际

| 参数 | 值 |
| --- | --- |
| RPM（每分钟请求数） | 180 |

<a id="调用方式"></a>

## 调用方式

-   [客户端事件](../../../../_short/cosyvoice-client-events-480a8821d2d60e18.md)
-   [WebSocket 接入](../../../../_short/cosyvoice-websocket-api-5929268331632771.md)
-   [AOQ 接入](../../../../_short/cosyvoice-aoq-access-c0e8e4035486f433.md)
-   [非实时 HTTP API](../../../../_short/cosyvoice-tts-http-api-63e05680db50f996.md)
-   [CosyVoice音色列表](../../../model-experience/speech-and-audio/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md#39a40bbc5dxp3)
