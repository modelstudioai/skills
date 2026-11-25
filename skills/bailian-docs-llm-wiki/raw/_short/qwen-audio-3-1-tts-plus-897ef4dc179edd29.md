# qwen-audio-3.1-tts-plus

Qwen-Audio-3.1-TTS-Plus 是面向精品音色和内容创作的高质量、专业级语音合成大模型，支持多种语言和方言及流式语音合成。模型支持 free-style 指令遵循和细粒度标签控制，可灵活控制情绪、语气、角色、语速、音量等表达方式。在声音复刻场景中，模型对含噪声、混响的参考音频具有更强的鲁棒性，提升了音质、清晰度和整体表现力。Plus 版本侧重音质与高分辨率，适用于品牌标杆音色、有声内容创作、影视配音、角色演绎等对音质要求较高的专业场景。

<a id="推理服务供应商"></a>

<a id="h-490b2834e6"></a>

## 推理服务供应商

`qwen-audio-3.1-tts-plus`模型的推理服务供应商为阿里云百炼。

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

本文仅展示模型调用原价，不包含限时优惠等活动信息，请前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)查看活动优惠。

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

| 计费项 | 价格（元） | 单位 |
| --- | --- | --- |
| 语音合成 | 1.4 | 每万字符 |

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

| 计费项 | 价格（元） | 单位 |
| --- | --- | --- |
| 语音合成 | 2.19 | 每万字符 |

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

| 参数 | 值 |
| --- | --- |
| RPM（每分钟请求数） | 180 |

<a id="调用方式"></a>

<a id="invocation"></a>

## 调用方式

-   [客户端事件](qwen-audio-tts-client-events-26c1ffacfaed1e62.md)
-   [WebSocket 接入](qwen-audio-tts-websocket-api-6f9e2d20cf04ea96.md)
-   [AOQ 接入](../model-api-reference/realtime-api-directory/realtime-tts-model-apis/qwen-audio-tts-api/qwen-audio-tts-aoq-access.md)
-   [非实时 HTTP API](qwen-audio-tts-http-api-ee05f9b13900b687.md)
-   [Qwen-Audio-TTS音色列表](../model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md#qwen-tts31-plus-voices)
