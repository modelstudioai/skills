# antdigital/Ling-3.1-flash

antdigital/Ling-3.1-flash 是由蚂蚁数科提供推理服务的 Ling 模型，总参数约 560B，每个 Token 激活约 25B 参数，上下文窗口上限为 1M，适用于通用智能体、搜索、日常办公和软件研发等任务。仅支持文本输入。

## 推理服务供应商

`antdigital/Ling-3.1-flash` 模型的推理服务供应商为蚂蚁数科。

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

不支持

Function Calling

支持

结构化输出

支持

联网搜索

不支持

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

1048576

最大输出长度

262144

上下文长度

1048576

最大输入长度（思考模式下）

1048576

最大输出长度（思考模式下）

262144

最大思维链长度

262144

## 模型价格

本文仅展示模型调用原价，不包含限时优惠等活动信息，请前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)查看活动优惠。

#### 华北2（北京）

计费项

价格（元）

单位

输入

2

每百万 Token

输出

6

每百万 Token

输入（缓存命中）

0.4

每百万 Token

## 限流

#### 华北2（北京）

参数

值

RPM（每分钟请求数）

300

TPM（每分钟 Token）

10,000,000

## 调用方式

使用 OpenAI 兼容接口调用模型，具体方法请参见[Ling-蚂蚁数科](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/antdigital.md)。
