# qwen-audio-3.1-captioner

Qwen-Audio-3.1-Captioner 是面向音频全信息理解、复杂声学场景分析与大规模数据处理优化的新一代音频全要素转写与分离模型。该模型在传统语音转写的基础上，重点增强了对说话人，时间戳，环境音、音效、音乐等多维音频信息的感知与摘要能力，并具备强劲的说话人与背景音频分离能力。

<a id="推理服务供应商"></a>

## 推理服务供应商

qwen-audio-3.1-captioner 模型的推理服务供应商为阿里云百炼。

<a id="模型能力"></a>

## 模型能力

| 能力项 | 支持情况 | 能力项 | 支持情况 |
| --- | --- | --- | --- |
| 输入模态 | 音频 | 输出模态 | 文本、音频 |
| 模型体验 | 不支持 | Function Calling | 不支持 |
| 结构化输出（JSON Mode） | 不支持 | 联网搜索 | 不支持 |
| 前缀续写 | 不支持 | 上下文缓存 | 不支持 |
| 批量推理 | 不支持 | 模型调优 | 不支持 |

<a id="上下文限制"></a>

## 上下文限制

<table><thead><tr><th><strong>参数</strong></th><th><strong>值</strong></th><th><strong>参数</strong></th><th><strong>值</strong></th></tr></thead><tbody><tr><td><p>最大输入长度</p></td><td><ul><li></li></ul></td><td><p>最大输出长度</p></td><td><ul><li></li></ul></td></tr><tr><td><p>上下文长度</p></td><td><ul><li></li></ul></td><td><ul><li></li></ul></td><td><ul><li></li></ul></td></tr></tbody></table>

<a id="模型价格"></a>

## 模型价格

本文仅展示模型调用原价，不包含限时优惠等活动信息，请前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)查看活动优惠。

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

| 计费项 | 价格（元） | 单位 |
| --- | --- | --- |
| 输入 | 0.8 | 每百万 Token |
| 输出 | 2.7 | 每百万 Token |

<a id="限流"></a>

## 限流

<a id="sec-tabs-2"></a>

<a id="华北2-北京-2"></a>

<a id="华北2-北京-2-h4"></a>

#### 华北2（北京）

| 参数 | 值 |
| --- | --- |
| 每分钟调用次数（RPM） | 600 |

<a id="调用方式"></a>

## 调用方式

-   [HTTP API](../model-api-reference/audio-api-directory/qwen-audio-asr-captioner-http-api.md)
