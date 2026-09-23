# qwen-audio-3.1-asr-flash-streaming

Qwen-Audio-3.1-ASR-Flash-Streaming端到端实时语音识别大模型，面向实时会议、直播字幕与智能交互等场景，具备低延迟、高精度的流式语音转写能力。模型支持多语种与多地区中文方言识别、中英文自由切换、热词及上下文增强、标点预测与文本规范化，并具备较强的噪声鲁棒性，可适应复杂声学环境。同时该版本支持多种方言 ASR/AST 可控输出。

## 推理服务供应商

`qwen-audio-3.1-asr-flash-streaming`模型的推理服务供应商为阿里云百炼。

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

8192 Token

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

每百万 Token

输出

4.5

每百万 Token

#### 新加坡

部署范围：国际

计费项

价格（元）

单位

输入

6.781

每百万 Token

输出

5.104

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

-   [实时语音识别](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide)
-   [WebSocket API](raw/_short/fun-asr-realtime-websocket-api-d80484c92992191d.md)
