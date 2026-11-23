# qwen-audio-3.1-live

Qwen-Audio-3.1-Live 支持实时双工语音对话。应用或后台模型处理任务时，语音模型仍可与用户交谈，并播报任务进度和结果。Client 模式由应用处理任务，Responses 模式由百炼调用指定的后台模型。两种模式都可通过函数调用接入业务工具。

qwen-audio-3.1-live 模型的推理服务供应商为阿里云百炼。

## 模型能力

能力项

支持情况

能力项

支持情况

输入模态

文本、音频

输出模态

文本、音频

模型体验

不支持

Function Calling

[支持](https://help.aliyun.com/zh/model-studio/qwen-audio-live#live-function-calling)

结构化输出

不支持

联网搜索

不支持内置搜索

前缀续写

不支持

上下文缓存

不支持

批量推理

不支持

模型调优

不支持

模型面向前台实时语音交互，重点提供低延迟、自然流畅的实时对话能力；复杂推理等任务可通过与后台模型协同完成。

## 输入限制

前台模型的系统指令和函数配置文本合计最多 65,536 Token。

## 模型价格

按会话时长（秒）计费。连接建立后，单次会话至少按 3 秒计费。超过 3 秒时，按实际会话时长计费。发送文字消息、静音或空闲的时间也计入会话时长。百炼调用后台模型时，按该模型的实际 Token 用量另行计费。详见[计费说明](https://help.aliyun.com/zh/model-studio/model-pricing#qwen-audio-live-pricing)。

#### 华北2（北京）

模型 ID

单价（元/秒）

`qwen-audio-3.1-live`

0.003330

#### 新加坡

模型 ID

单价（元/秒）

`qwen-audio-3.1-live`

0.005177

## 限流

WebSocket 最多同时保持 5 条连接。详见[限流说明](https://help.aliyun.com/zh/model-studio/rate-limit#qwen-audio-live-rate-limit)。

## 调用方式

-   [接入指南](raw/model-user-guide/model-experience/speech-and-audio/speech-to-speech/qwen-audio-live.md)
-   [API 参考](raw/model-api-reference/realtime-api-directory/qwen-audio-live-api-directory.md)
