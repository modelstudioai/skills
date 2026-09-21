# qwen-audio-3.1-tts-flash

Qwen-Audio-3.1-TTS-Flash是面向实时交互场景的高性能语音合成大模型，支持多种语言和方言，支持流式语音合成。该模型具有free-style指令遵循能力和细粒度标签控制能力，可更灵活地控制情绪、语气、角色、语速、音量等表达方式。同时，模型在声音复刻场景中，对含有噪声、混响的参考音频具有更强的鲁棒性，提升了音质、清晰度和整体表现力。Flash版本重点优化实时合成体验，适用于语音助手、实时对话、智能客服等低延迟交互场景。

## 推理服务供应商

`qwen-audio-3.1-tts-flash`模型的推理服务供应商为阿里云百炼。

## 模型能力

能力项

支持情况

能力项

支持情况

输入模态

**Text**

输出模态

**Audio**

模型体验

支持

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

—

最大输出长度

—

上下文长度

—

## 模型价格

本文仅展示模型调用原价，不包含限时优惠等活动信息，请前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)查看活动优惠。

#### 华北2（北京）

计费项

价格（元）

单位

输入

1.5

每百万 Token

输出

12

每百万 Token

## 限流

#### 华北2（北京）

参数

值

RPS（每秒请求数）

3

## 调用方式

-   [实时语音合成（WebSocket）](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide)
-   [非实时语音合成（HTTP）](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide)
-   [Qwen-Audio-TTS音色列表](https://help.aliyun.com/zh/model-studio/qwen-audio-tts-voice-list#qwen-tts31-voices)
