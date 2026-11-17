# kling/kling-v4-video-generation

支持文生视频和首帧、中间帧、尾帧任意组合的关键帧生视频，固定生成有声视频。

## 推理服务供应商

`kling/kling-v4-video-generation` 模型的推理服务供应商为可灵AI。

## 模型能力

输入模态

输出模态

支持能力

Image、Text

Video

文生视频、关键帧生视频（首帧、中间帧、尾帧可任意组合）

模型固定生成有声视频，支持 `std`（720P）和 `pro`（1080P），视频时长为3～30秒，输出格式为 MP4（H.264）。调用方式见[可灵-视频生成 API](raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)。

## 模型价格

本文仅展示模型调用原价，不包含限时优惠等活动信息，请前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)查看活动优惠。

#### 华北2（北京）

计费项

价格（元）

单位

视频生成（720P）

1.0

每秒

视频生成（1080P）

1.5

每秒

免费额度：无。请求失败不产生费用。

## 限流

#### 华北2（北京）

参数

值

每秒钟调用次数（RPS）

5

同时处理中任务数量（并发数）

10（共享）

同一阿里云百炼 API Key 下，可灵系列的 7 个图像及视频模型共享 10 个并发数，详见[模型限流](https://help.aliyun.com/zh/model-studio/rate-limit#kling-third-party-title)。
