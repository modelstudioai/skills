# kling/kling-v4-omni-reference-video-generation

支持文生视频、关键帧生视频、参考生视频和视频编辑，固定生成有声视频。

<a id="推理服务供应商"></a>

<a id="h-490b2834e6"></a>

## 推理服务供应商

`kling/kling-v4-omni-reference-video-generation` 模型的推理服务供应商为可灵AI。

<a id="模型能力"></a>

<a id="h-77230e94b5"></a>

## 模型能力

| 输入模态 | 输出模态 | 支持能力 |
| --- | --- | --- |
| Image、Text、Video | Video | 文生视频、关键帧生视频、参考生视频、视频编辑 |

模型固定生成有声视频，支持 `std`（720P）和 `pro`（1080P），视频时长为3～30秒，输出格式为 MP4（H.264）。调用方式见[可灵-视频生成 API](../model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)。

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
| 视频生成（720P 无参考视频） | 1.0 | 每秒 |
| 视频生成（1080P 无参考视频） | 1.5 | 每秒 |
| 视频生成（720P 有参考视频） | 0.6 | 每秒 |
| 视频生成（1080P 有参考视频） | 0.9 | 每秒 |

无视频输入时，计费时长等于生成视频时长；有视频输入时，计费时长等于 max（输入视频总时长，生成视频时长）+ 生成视频时长。免费额度：无。请求失败不产生费用。

<a id="限流"></a>

<a id="h-1742581931"></a>

## 限流

<a id="sec-tabs-2"></a>

<a id="华北2-北京-2"></a>

<a id="华北2-北京-2-h4"></a>

#### 华北2（北京）

| 参数 | 值 |
| --- | --- |
| 每秒钟调用次数（RPS） | 5 |
| 同时处理中任务数量（并发数） | 10（共享） |

同一阿里云百炼 API Key 下，可灵系列的 7 个图像及视频模型共享 10 个并发数，详见[模型限流](../model-user-guide/get-started-with-models/rate-limit.md#kling-third-party-title)。
