# Tripo/Tripo-ImageToSplat

Tripo根据单张图片生成 3D Gaussian Splat（.splat 格式）。Gaussian Splatting 是一种新型 3D 表示方式，适用于高质量实时渲染与真实感场景重建。输出的 .splat 文件可用主流 Gaussian Splat 查看器与渲染器加载。

<a id="推理服务供应商"></a>

<a id="h-490b2834e6"></a>

## 推理服务供应商

`Tripo/Tripo-ImageToSplat`模型的推理服务供应商为Tripo。

<a id="模型能力"></a>

<a id="h-77230e94b5"></a>

## 模型能力

| 能力项 | 支持情况 | 能力项 | 支持情况 |
| --- | --- | --- | --- |
| 输入模态 | **Image** | 输出模态 | **3D-Generation** |
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

<a id="h-6af6eab13e"></a>

## 模型价格

本文仅展示模型调用原价，不包含限时优惠等活动信息，请前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)查看活动优惠。价格以积分计，**1积分折合0.07元**。

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

| 计费项 | 价格（积分） | 单位 |
| --- | --- | --- |
| 图片生成Gaussian Splat | 30 | 每次 |

<a id="限流"></a>

<a id="h-c40c678050"></a>

## 限流

<a id="sec-tabs-2"></a>

<a id="华北2-北京-2"></a>

<a id="华北2-北京-2-h4"></a>

#### 华北2（北京）

| 参数 | 值 |
| --- | --- |
| RPM（每分钟请求数） | 300 |
| 默认并发数 | 5 |

<a id="调用方式"></a>

<a id="h-5d3a9e71c4"></a>

## 调用方式

-   [Tripo-图片生成Gaussian Splat](../../../../_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)
