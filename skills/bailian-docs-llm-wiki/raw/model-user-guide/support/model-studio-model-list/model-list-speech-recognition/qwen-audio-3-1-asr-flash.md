# qwen-audio-3.1-asr-flash

Qwen-Audio-3.1-ASR-Flash是一款支持短语音高效识别的大模型，面向高质量、多语种及文化内容转写场景。模型支持多语种与多地区中文方言识别，同时针对中文古诗词的韵律、节奏与文言表达进行优化。具备上下文增强、标点预测与文本规范化能力。同时该版本支持多种方言 ASR/AST 可控输出。原生转写润色能力及工业级多人对话分角色转写能力。

## 推理服务供应商

`qwen-audio-3.1-asr-flash`模型的推理服务供应商为阿里云百炼。

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

0.8

每百万 Token

输出

2.7

每百万 Token

#### 新加坡

部署范围：国际

计费项

价格（元）

单位

输入

1.094

每百万 Token

输出

3.427

每百万 Token

## 限流

#### 华北2（北京）

参数

值

RPM（每分钟请求数）

600

#### 新加坡

部署范围：国际

参数

值

RPM（每分钟请求数）

600

## 调用方式

-   [非实时语音识别](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide)
-   [HTTP API](raw/model-api-reference/audio-api-references/speech-recognition-api-reference/non-real-time-speech-recognition-for-fun-asr-flash/fun-asr-flash-recorded-speech-recognition-http-api.md)
