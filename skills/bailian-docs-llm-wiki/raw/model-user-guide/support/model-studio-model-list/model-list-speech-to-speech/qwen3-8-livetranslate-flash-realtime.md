# qwen3.8-livetranslate-flash-realtime

Qwen3.8-LiveTranslate-Flash-Realtime 是多语言实时音视频同传模型，支持音频和图像输入、文本和音频输出，可识别 60 种源语言，并支持 29 种语言的语音输出。

## 推理服务供应商

`qwen3.8-livetranslate-flash-realtime`模型的推理服务供应商为阿里云百炼。

## 模型能力

**能力项**

**支持情况**

**能力项**

**支持情况**

输入模态

**Audio, Image**

输出模态

**Text, Audio**

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

**参数**

**值**

**参数**

**值**

最大输入长度

49152

最大输出长度

4096

上下文长度

53248

## 模型价格

本文仅展示模型调用原价，不包含限时优惠等活动信息，请前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)查看活动优惠。

#### 华北2（北京）

**计费项**

**价格（元）**

**单位**

音频输入

40

每百万 Token

图片输入

3.3

每百万 Token

文本输出

100

每百万 Token

音频输出

160

每百万 Token

#### 新加坡

服务部署范围：国际

**计费项**

**价格（元）**

**单位**

音频输入

54.688

每百万 Token

图片输入

4.01

每百万 Token

文本输出

145.835

每百万 Token

音频输出

218.752

每百万 Token

## 限流

#### 华北2（北京）

**参数**

**值**

RPM（每分钟请求数）

10

TPM（每分钟 Token 数）

100,000

#### 新加坡

服务部署范围：国际

**参数**

**值**

RPM（每分钟请求数）

10

TPM（每分钟 Token 数）

100,000

## 调用方式

通过 WebSocket Realtime API 调用，模型 ID 为 `qwen3.8-livetranslate-flash-realtime`。连接地址和示例参见[实时翻译使用指南](https://help.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime#a36e6dc44fucp)。

本模型使用 `session.output_modalities` 配置输出模态。流式译文使用 `response.text.delta` 或 `response.audio_transcript.delta` 事件返回。参数和事件与 `qwen3.5-livetranslate-flash-realtime` 存在差异，详见[客户端事件](https://help.aliyun.com/zh/model-studio/live-translator-client-events#af43722339yva)和[服务端事件](https://help.aliyun.com/zh/model-studio/live-translator-server-events#text-delta)。
