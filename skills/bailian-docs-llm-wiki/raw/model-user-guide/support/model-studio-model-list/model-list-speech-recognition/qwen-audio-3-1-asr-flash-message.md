# qwen-audio-3.1-asr-flash-message

Qwen-Audio-3.1-ASR-Flash-Message 是面向语音消息、输入法和企业业务场景优化的生成式语音识别模型，支持中文、英文及多语言识别，重点优化印尼语、日语、泰语、菲律宾语、越南语、韩语和马来语。模型支持流式上屏、P0/P1 热词、文本归一化、结合前文转写和业务上下文识别，以及可开关的原生润色，并增强了多人声、背景对话、远场及环境噪声下的识别稳定性。支持自动识别或指定目标语种，中文方言可输出方言原文或转换为普通话文本。

## 推理服务供应商

`qwen-audio-3.1-asr-flash-message`模型的推理服务供应商为阿里云百炼。

## 模型能力

能力项

支持情况

能力项

支持情况

输入模态

**Audio**

输出模态

**Text**

模型体验

不支持

Function Calling

不支持

结构化输出

支持

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

参数

值

最大输入长度

7168 Token

最大输出长度

1024 Token

上下文长度

8192 Token

## 模型价格

本文仅展示模型调用原价，不包含限时优惠等活动信息，请前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)查看活动优惠。

#### 华北2（北京）

计费项

价格（元）

单位

输入

6

每百万Token

输出

4.5

每百万Token

#### 新加坡

部署范围：国际

计费项

价格（元）

单位

输入

6.781

每百万Token

输出

5.104

每百万Token

## 限流

#### 华北2（北京）

参数

值

RPM（每分钟请求数）

1200

#### 新加坡

部署范围：国际

参数

值

RPM（每分钟请求数）

1200

## 调用方式

-   [实时语音识别](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide)
-   [WebSocket API](raw/_short/fun-asr-realtime-websocket-api-d80484c92992191d.md)
