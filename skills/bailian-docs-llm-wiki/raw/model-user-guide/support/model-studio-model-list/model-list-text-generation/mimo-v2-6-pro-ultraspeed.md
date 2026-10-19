# xiaomi/mimo-v2.6-pro-ultraspeed

MiMo-V2.6-Pro-UltraSpeed 是小米旗舰模型 MiMo-V2.6-Pro 的高速版本。该模型基于同一 1 万亿参数 MiMo-V2.6-Pro 检查点构建，在保持与原模型同等质量的前提下，输出速度提升约 10 倍。模型支持 100 万 token 上下文窗口，具备原生多模态能力。针对智能体工作流做了专项优化，在代码、视觉、通用问答与科研场景下均拥有顶尖性能，擅长处理复杂、长周期任务，可在各类智能体测试框架中展现出色的泛化能力。

## 推理服务供应商

`xiaomi/mimo-v2.6-pro-ultraspeed`模型的推理服务供应商为小米Mimo。

## 模型能力

能力项

支持情况

能力项

支持情况

输入模态

**Text** **Image** **Video** **Audio**

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

不支持

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

131072

上下文长度

1048576

最大输入长度（思考模式下）

1048576

最大输出长度（思考模式下）

131072

最大思维链长度

131072

## 模型价格

本文仅展示模型调用原价，不包含限时优惠等活动信息，请前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)查看活动优惠。

#### 华北2（北京）

计费项

价格（元）

单位

输入

30

每百万tokens

输出

60

每百万tokens

输入（缓存命中）

0.25

每百万tokens

## 限流

#### 华北2（北京）

参数

值

RPM（每分钟请求数）

100

TPM（每分钟tokens）

5,000,000

## 调用方式

-   [MiMo-小米](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
-   [多模态输入](https://help.aliyun.com/zh/model-studio/mimo#h-mimo-multimodal)
