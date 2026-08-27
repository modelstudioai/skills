# qwen3.8-2.4t-a95b

Qwen3.8-2.4T-A95B 是通义千问最新旗舰系列的开源版本，2026 年 8 月发布。采用稀疏 MoE 架构，总参数 2.4 万亿，每步激活约 950 亿，配合混合注意力机制，支持 100 万 Token 上下文。核心基准：GPQA Diamond 92.6、PaperBench 93.0、OSWorld 86.1、BabyVision 82.0，CodeArena 全球第 4。

## 推理服务供应商

`qwen3.8-2.4t-a95b`模型的推理服务供应商为阿里云百炼。

## 模型能力

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

支持

结构化输出

支持

联网搜索

支持

前缀续写

支持

上下文缓存

支持

批量推理

不支持

模型调优

不支持

## 上下文限制

参数

值

参数

值

最大输入长度

991808

最大输出长度

131072

上下文长度

1000000

最大输入长度（思考模式下）

983616

最大输出长度（思考模式下）

131072

最大思维链长度

131072

## 模型价格

本文仅展示模型调用原价，不包含限时优惠等活动信息，请前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)查看活动优惠。

#### 华北2（北京）

计费项

价格（元）

单位

输入

12

每百万tokens

输出

36

每百万tokens

输入（缓存命中）

1.5

每百万tokens

显式缓存创建

15

每百万tokens

显式缓存命中

1

每百万tokens

#### 新加坡

部署范围：国际

计费项

价格（元）

单位

输入

14.988

每百万tokens

输出

44.965

每百万tokens

输入（缓存命中）

1.874

每百万tokens

显式缓存创建

18.736

每百万tokens

显式缓存命中

1.274

每百万tokens

## 限流

本模型采用[动态限流](raw/model-user-guide/get-started-with-models/quota-management.md)机制，TPM 按百炼月消费分档调整。

#### 华北2（北京）

参数

值

RPM（每分钟请求数）

5000

TPM（每分钟tokens）

5,000,000

#### 新加坡

部署范围：国际

参数

值

RPM（每分钟请求数）

5000

TPM（每分钟tokens）

5,000,000
