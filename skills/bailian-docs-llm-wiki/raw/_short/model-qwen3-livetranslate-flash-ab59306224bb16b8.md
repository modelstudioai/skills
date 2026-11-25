# qwen3-livetranslate-flash

Qwen3-LiveTranslate-Flash，一款高精度、高响应、高鲁棒性的多语言实时音视频同传大模型。依托Qwen3-Omni强大的基座能力、海量多模态数据、跨语言跨模态对齐和视觉增强等技术，Qwen3-LiveTranslate-Flash 实现了离线和实时两种音视频翻译能力，能听懂19种语言，会说10种语言以及8种中文方言。

<a id="推理服务供应商"></a>

<a id="h-490b2834e6"></a>

## 推理服务供应商

`qwen3-livetranslate-flash`模型的推理服务供应商为阿里云百炼。

<a id="模型能力"></a>

<a id="h-77230e94b5"></a>

## 模型能力

| 能力项 | 支持情况 | 能力项 | 支持情况 |
| --- | --- | --- | --- |
| 输入模态 | **Audio** **Video** | 输出模态 | **Text** **Audio** |
| 模型体验 | 不支持 | Function Calling | 不支持 |
| 结构化输出 | 不支持 | 联网搜索 | 不支持 |
| 前缀续写 | 不支持 | 上下文缓存 | 不支持 |
| 批量推理 | 不支持 | 模型调优 | 不支持 |

<a id="上下文限制"></a>

<a id="h-01b911f555"></a>

## 上下文限制

| 参数 | 值 | 参数 | 值 |
| --- | --- | --- | --- |
| 最大输入长度 | 49152 | 最大输出长度 | 4096 |
| 上下文长度 | 53248 |  |  |

<a id="模型价格"></a>

<a id="h-737956cb9b"></a>

## 模型价格

本文仅展示模型调用原价，不包含限时优惠等活动信息，请前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)查看活动优惠。

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

| 计费项 | 价格（元） | 单位 |
| --- | --- | --- |
| 输入：音频 | 10 | 每百万tokens |
| 输入：图片 | 4 | 每百万tokens |
| 输出：文本 | 10 | 每百万tokens |
| 输出：音频 | 40 | 每百万tokens |

<a id="限流"></a>

<a id="h-74ea396da8"></a>

## 限流

<a id="sec-tabs-2"></a>

<a id="华北2-北京-2"></a>

<a id="华北2-北京-2-h4"></a>

#### 华北2（北京）

| 参数 | 值 |
| --- | --- |
| RPM（每分钟请求数） | 100 |
| TPM（每分钟tokens） | 100,000 |

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

部署范围：国际

| 参数 | 值 |
| --- | --- |
| RPM（每分钟请求数） | 100 |
| TPM（每分钟tokens） | 100,000 |

<a id="调用方式"></a>

<a id="invocation"></a>

## 调用方式

-   [接入指南](../model-user-guide/model-experience/omni-modal/qwen3-livetranslate-flash.md)
-   [HTTP API 参考](../model-api-reference/audio-api-directory/qwen3-livetranslate-flash-api.md)

<a id="快照版本"></a>

<a id="h-a3d6551982"></a>

## 快照版本

<a id="qwen3-livetranslate-flash-2025-12-01"></a>

<a id="h-861a902ef6"></a>

### qwen3-livetranslate-flash-2025-12-01

Qwen3-LiveTranslate-Flash，一款高精度、高响应、高鲁棒性的多语言实时音视频同传大模型。依托Qwen3-Omni强大的基座能力、海量多模态数据、跨语言跨模态对齐和视觉增强等技术，Qwen3-LiveTranslate-Flash 实现了离线和实时两种音视频翻译能力，能听懂19种语言，会说10种语言以及8种中文方言。此版本为2025年12月01日的快照版本。

<a id="推理服务供应商-2"></a>

<a id="h-672edebe26"></a>

#### 推理服务供应商

`qwen3-livetranslate-flash-2025-12-01`模型的推理服务供应商为阿里云百炼。

<a id="模型能力-2"></a>

<a id="h-10dc9f554d"></a>

#### 模型能力

| 能力项 | 支持情况 | 能力项 | 支持情况 |
| --- | --- | --- | --- |
| 输入模态 | **Audio** **Video** | 输出模态 | **Text** **Audio** |
| 模型体验 | 不支持 | Function Calling | 不支持 |
| 结构化输出 | 不支持 | 联网搜索 | 不支持 |
| 前缀续写 | 不支持 | 上下文缓存 | 不支持 |
| 批量推理 | 不支持 | 模型调优 | 不支持 |

<a id="上下文限制-2"></a>

<a id="h-f493e4fcd6"></a>

#### 上下文限制

| 参数 | 值 | 参数 | 值 |
| --- | --- | --- | --- |
| 最大输入长度 | 49152 | 最大输出长度 | 4096 |
| 上下文长度 | 53248 |  |  |

<a id="模型价格-2"></a>

<a id="h-e463e1b93b"></a>

#### 模型价格

本文仅展示模型调用原价，不包含限时优惠等活动信息，请前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)查看活动优惠。

<a id="sec-tabs-3"></a>

<a id="华北2-北京-3"></a>

<a id="华北2-北京-3-h4"></a>

#### 华北2（北京）

| 计费项 | 价格（元） | 单位 |
| --- | --- | --- |
| 输入：音频 | 10 | 每百万tokens |
| 输入：图片 | 4 | 每百万tokens |
| 输出：文本 | 10 | 每百万tokens |
| 输出：音频 | 40 | 每百万tokens |

<a id="限流-2"></a>

<a id="h-a1582c2f34"></a>

#### 限流

<a id="sec-tabs-4"></a>

<a id="华北2-北京-4"></a>

<a id="华北2-北京-4-h4"></a>

#### 华北2（北京）

| 参数 | 值 |
| --- | --- |
| RPM（每分钟请求数） | 100 |
| TPM（每分钟tokens） | 100,000 |

<a id="新加坡-2"></a>

<a id="新加坡-2-h4"></a>

#### 新加坡

部署范围：国际

| 参数 | 值 |
| --- | --- |
| RPM（每分钟请求数） | 100 |
| TPM（每分钟tokens） | 100,000 |
