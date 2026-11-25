# qwen-audio-3.0-realtime-flash

千问实时语音对话大模型3.0 是一款登顶全球权威评测的下一代实时双工语音大模型，它在全球权威第三方评测平台 Artificial Analysis Speech-to-Speech子项中取得综合排名第一。千问实时语音对话大模型3.0兼顾了模型智商与双工对话节奏,在保持流畅、自然的实时交互体验的同时,语音推理能力不打折扣;并通过并行推理和全向流式等工程优化,将端到端响应时延控制在低水平,实现"又快又聪明"的对话体验。极速版更注重极致的响应速度

<a id="推理服务供应商"></a>

<a id="h-490b2834e6"></a>

## 推理服务供应商

`qwen-audio-3.0-realtime-flash`模型的推理服务供应商为阿里云百炼。

<a id="模型能力"></a>

<a id="h-77230e94b5"></a>

## 模型能力

| 能力项 | 支持情况 | 能力项 | 支持情况 |
| --- | --- | --- | --- |
| 输入模态 | **Audio** **Text** | 输出模态 | **Audio** **Text** |
| 模型体验 | 不支持 | Function Calling | 支持 |
| 结构化输出 | 不支持 | 联网搜索 | 支持 |
| 前缀续写 | 不支持 | 上下文缓存 | 不支持 |
| 批量推理 | 不支持 | 模型调优 | 不支持 |

<a id="上下文限制"></a>

<a id="h-cc185df703"></a>

## 上下文限制

| 参数 | 值 | 参数 | 值 |
| --- | --- | --- | --- |
| 最大输入长度 | 16384 | 最大输出长度 | 8192 |
| 上下文长度 | 40960 | 最大输入长度（思考模式下） | 16384 |
| 最大输出长度（思考模式下） | 8192 | 最大思维链长度 | 1024 |

<a id="模型价格"></a>

<a id="h-148cd5886a"></a>

## 模型价格

本文仅展示模型调用原价，不包含限时优惠等活动信息，请前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)查看活动优惠。

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

| 计费项 | 价格（元） | 单位 |
| --- | --- | --- |
| 输入：音频 | 6 | 每百万tokens |
| 输入：文本 | 1.5 | 每百万tokens |
| 输出：文本 | 4.5 | 每百万tokens |
| 输出：文本+音频（输出的文本不计费） | 12 | 每百万tokens |

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

部署范围：国际

| 计费项 | 价格（元） | 单位 |
| --- | --- | --- |
| 输入：音频 | 6.781 | 每百万tokens |
| 输入：文本 | 1.677 | 每百万tokens |
| 输出：文本 | 5.104 | 每百万tokens |
| 输出：文本+音频（输出的文本不计费） | 13.636 | 每百万tokens |

<a id="限流"></a>

<a id="h-61cfd6863b"></a>

## 限流

<a id="sec-tabs-2"></a>

<a id="华北2-北京-2"></a>

<a id="华北2-北京-2-h4"></a>

#### 华北2（北京）

| 参数 | 值 |
| --- | --- |
| RPM（每分钟请求数） | 60 |
| TPM（每分钟tokens） | 100,000 |

<a id="新加坡-2"></a>

<a id="新加坡-2-h4"></a>

#### 新加坡

部署范围：国际

| 参数 | 值 |
| --- | --- |
| RPM（每分钟请求数） | 60 |
| TPM（每分钟tokens） | 100,000 |

<a id="调用方式"></a>

<a id="invocation"></a>

## 调用方式

-   [接入指南](../model-user-guide/model-experience/speech-and-audio/speech-to-speech/qwen-audio-realtime-user-guides.md)
-   [API 参考](../model-api-reference/realtime-api-directory/audio-realtime-api-directory/voice-conversation-api-references.md)
