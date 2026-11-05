# qwen-mt-uni

Qwen-MT-Uni 是一款面向图片、文本、音频及各类文档的全模态翻译模型，通过统一的格式识别、智能路由、内容抽取、跨模态翻译与原格式重构链路，实现多类型输入的一体化高保真翻译。

## 推理服务供应商

`qwen-mt-uni` 模型的推理服务供应商为阿里云百炼。

## 模型能力

能力项

支持情况

能力项

支持情况

输入模态

**Text / Document / Image / Audio**

输出模态

**Text / Document / Image / Audio**

模型体验

不支持

Function Calling

不支持

结构化输出

不支持

联网搜索

不支持

前缀续写

不支持

上下文缓存

不支持

批量推理

不支持

模型调优

不支持

## 上下文限制

参数

值

单文件大小上限

100 MB

文档页数上限

200 页

音频时长

3 秒 ~ 60 分钟

## 模型价格

本文仅展示模型调用原价，不包含限时优惠等活动信息，请前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)查看活动优惠。

#### 华北2（北京）

输入模态

输入单价（元/百万 Token）

文本

65

文档

20

图片

32

音频

400

免费额度：100万 Token（自开通百炼、模型发布或申请通过之日起 90 天内有效，以较晚者为准）。

## 限流

#### 华北2（北京）

参数

值

RPM（每分钟请求数）

162

TPM（每分钟消耗 Token 数）

2,592,000

异步并发数

3

异步排队数

500

## API 参考

调用方式与请求响应参数请参见 [Qwen-MT-Uni API 参考](raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。
