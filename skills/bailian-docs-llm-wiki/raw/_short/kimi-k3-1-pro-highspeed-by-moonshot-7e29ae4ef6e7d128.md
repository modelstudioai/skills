# kimi/kimi-k3.1-pro-highspeed

kimi/kimi-k3.1-pro-highspeed 是由月之暗面提供推理服务的 Kimi 高速版模型，支持文本和图像输入，上下文长度为 1048576 Token。

## 推理服务供应商

`kimi/kimi-k3.1-pro-highspeed` 模型的推理服务供应商为月之暗面。

## 模型能力

能力项

支持情况

能力项

支持情况

输入模态

**Text** **Image**

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

1048576

上下文长度

1048576

最大输入长度（思考模式下）

1048576

最大输出长度（思考模式下）

1048576

最大思维链长度

1048576

## 模型价格

本文仅展示模型调用原价，不包含限时优惠等活动信息，请前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)查看活动优惠。

#### 华北2（北京）

计费项

价格（元）

单位

输入

26

每百万 Token

输出

136

每百万 Token

输入（缓存命中）

1.3

每百万 Token

## 限流

#### 华北2（北京）

参数

值

RPM（每分钟请求数）

500

TPM（每分钟 Token）

3,000,000

## 使用限制

-   不支持 `parallel_tool_calls` 参数。
-   不支持 `n` 参数。

## 调用方式

使用 OpenAI 兼容接口调用模型，具体方法请参见[Kimi-月之暗面](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)。
