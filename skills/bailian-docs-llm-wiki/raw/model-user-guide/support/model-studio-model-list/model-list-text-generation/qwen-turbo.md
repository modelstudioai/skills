# qwen-turbo

Qwen3系列Turbo模型，实现思考模式和非思考模式的有效融合，可在对话中切换模式。推理能力以更小参数规模比肩QwQ-32B、通用能力显著超过Qwen2.5-Turbo，达到同规模业界SOTA水平。该模型版本功能等同于快照模型 qwen-turbo-2025-04-28。

## 推理服务供应商

`qwen-turbo`模型的推理服务供应商为阿里云百炼。

## 模型能力

## 华北2（北京）

能力项

支持情况

能力项

支持情况

输入模态

**Text**

输出模态

**Text**

模型体验

支持

Function Calling

不支持

结构化输出

支持

联网搜索

不支持

前缀续写

不支持

上下文缓存

支持

批量推理

不支持

模型调优

不支持

## 新加坡

部署范围：国际

能力项

支持情况

能力项

支持情况

输入模态

**Text**

输出模态

**Text**

模型体验

支持

Function Calling

不支持

结构化输出

支持

联网搜索

不支持

前缀续写

支持

上下文缓存

支持

批量推理

支持

模型调优

不支持

## 上下文限制

参数

值

参数

值

最大输入长度

98304

最大输出长度

16384

上下文长度

131072

## 模型价格

本文仅展示模型调用原价，不包含限时优惠等活动信息，请前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)查看活动优惠。

## 华北2（北京）

计费项

价格（元）

单位

输入

0.3

每百万tokens

输出

0.6

每百万tokens

输入（思考）

0.3

每百万tokens

输出（思考）

3

每百万tokens

输入（缓存命中）

0.06

每百万tokens

输入（思考模式缓存命中）

0.06

每百万tokens

思考模式输出（Batch File）

1.5

每百万tokens

输入（Batch File）

0.15

每百万tokens

输出（Batch File）

0.3

每百万tokens

输入（思考模式 Batch File）

0.15

每百万tokens

调优

30

每百万tokens

## 新加坡

部署范围：国际

计费项

价格（元）

单位

输入

0.367

每百万tokens

输出

1.468

每百万tokens

输入（思考）

0.367

每百万tokens

输出（思考）

3.67

每百万tokens

输入（缓存命中）

0.073

每百万tokens

输入（思考模式缓存命中）

0.073

每百万tokens

思考模式输出（Batch File）

1.835

每百万tokens

输入（Batch File）

0.183

每百万tokens

输出（Batch File）

0.734

每百万tokens

输入（思考模式 Batch File）

0.183

每百万tokens

## 限流

## 华北2（北京）

参数

值

RPM（每分钟请求数）

1200

TPM（每分钟tokens）

5,000,000

## 新加坡

部署范围：国际

参数

值

RPM（每分钟请求数）

600

TPM（每分钟tokens）

5,000,000
