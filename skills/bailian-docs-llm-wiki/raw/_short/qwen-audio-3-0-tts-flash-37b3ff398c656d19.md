# qwen-audio-3.0-tts-flash

Qwen-Audio-3.0-TTS-Flash是面向实时交互场景优化的高性能语音合成大模型。相比前一版本，模型支持更多小语种和中文方言，提升了方言发音的正宗程度，并增强了 free-style 指令遵循能力和细粒度标签控制能力，可更灵活地控制情绪、语气、角色、语速、音量等表达方式。同时，模型在噪声、混响等复杂声学条件下具备更强鲁棒性，提升了音质、清晰度和整体表现力。Flash 版本重点优化实时合成体验，适用于语音助手、实时对话、智能客服等低延迟交互场景。

<a id="推理服务供应商"></a>

<a id="h-490b2834e6"></a>

## 推理服务供应商

`qwen-audio-3.0-tts-flash`模型的推理服务供应商为阿里云百炼。

<a id="模型能力"></a>

<a id="h-77230e94b5"></a>

## 模型能力

| 能力项 | 支持情况 | 能力项 | 支持情况 |
| --- | --- | --- | --- |
| 输入模态 | **Text** | 输出模态 | **Audio** |
| 模型体验 | 不支持 | Function Calling | 不支持 |
| 结构化输出 | 不支持 | 联网搜索 | 不支持 |
| 前缀续写 | 不支持 | 上下文缓存 | 不支持 |
| 批量推理 | 不支持 | 模型调优 | [支持（邀测）](../model-user-guide/model-training/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-qwen-audio-tts.md) |

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

本文仅展示模型调用原价，不包含限时优惠等活动信息，请前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)查看活动优惠。

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
| 语音合成 | 1.12413 | 每万字符 |

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

-   [客户端事件](qwen-audio-tts-client-events-26c1ffacfaed1e62.md)
-   [WebSocket 接入](qwen-audio-tts-websocket-api-6f9e2d20cf04ea96.md)
-   [AOQ 接入](../model-api-reference/realtime-api-directory/realtime-tts-model-apis/qwen-audio-tts-api/qwen-audio-tts-aoq-access.md)
-   [非实时 HTTP API](qwen-audio-tts-http-api-ee05f9b13900b687.md)
-   [Qwen-Audio-TTS音色列表](../model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md#f399ce27bcc8flash)
