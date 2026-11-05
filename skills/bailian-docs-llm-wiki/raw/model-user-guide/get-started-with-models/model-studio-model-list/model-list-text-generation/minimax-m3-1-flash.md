# MiniMax/MiniMax-M3.1-Flash

MiniMax M3.1 Flash 是面向 Agentic 任务的高性能多模态模型，支持 100 万 Token 上下文窗口，在复杂任务、软件开发和网络安全等场景中兼顾效果、推理速度与使用成本。

## 推理服务供应商

`MiniMax/MiniMax-M3.1-Flash` 模型的推理服务供应商为 MiniMax。

## 模型能力

能力项

支持情况

输入模态

**Image** **Text** **Video**

输出模态

**Text**

深度思考

支持，始终开启

Function Calling

支持

上下文缓存

支持

## 上下文限制

参数

值

上下文窗口

1,000,000 Token

## 模型价格

本文仅展示模型调用原价，不包含限时优惠等活动信息，请前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)查看活动优惠。

#### 华北2（北京）

计费项

价格（元）

单位

输入

1

每百万 Token

输出

4

每百万 Token

输入（缓存命中）

0.1

每百万 Token

## 限流

#### 华北2（北京）

参数

值

RPM（每分钟请求数）

200

TPM（每分钟tokens）

10,000,000

实际服务可能同时按 RPS（RPM/60）与 TPS（TPM/60）执行每秒限流，具体规则请参见[限流](raw/model-user-guide/get-started-with-models/rate-limit.md)。

## 使用限制

-   不支持 `stop`。传入后不会按指定停止词截断输出；请求可能仍成功且返回 `finish_reason: "stop"`，但这不表示指定停止词已生效。
-   不支持通过 `parallel_tool_calls` 控制工具调用的并行性。设置为 `false` 也不能保证串行调用，模型仍可能在一轮中返回多个 `tool_calls`。
-   `tool_choice` 仅支持 `auto`。其他取值可能报错或不生效，例如指定函数名称不能保证模型调用该函数。

## 调用方式

使用 OpenAI 兼容接口调用模型，具体方法以及与 MiniMax-M3 的参数差异请参见[MiniMax-稀宇科技](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)。
