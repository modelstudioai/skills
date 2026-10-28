# qwen-audio-3.1-realtime-flash

实时双工语音对话模型，支持文本和音频输入输出、工具调用、联网搜索及声音复刻。

## 推理服务供应商

阿里云百炼。

## 模型能力

能力项

说明

输入模态

文本、音频

输出模态

文本、音频

Function Calling

支持

联网搜索

支持

声音复刻

支持

接入协议

WebSocket、WebRTC、AOQ

默认音色

`longanqian_v3.1`

思考模式

不支持 `enable_thinking`

交互模式

`server_vad`、`smart_turn`、`smart_turn_v2`（推荐）、push-to-talk

说话人增强

支持（`smart_turn`、`smart_turn_v2` 模式）

联网搜索通过 `enable_search` 开启，可与 Function Calling 同时启用。

## 上下文限制

参数

上限（Token）

上下文长度

262,144

最大输入长度

245,760

最大输出长度

16,384

音频历史上下文限制

上限

最大轮次

50

累计音频时长

300 秒

## 价格

仅输出文本时，按文本输出单价计费；输出文本和音频时，仅对音频收取输出费用，伴随文本不另收输出费。

价格单位：元/百万 Token。

#### 华北2（北京）

模型 ID

文本输入

音频输入

文本输出

音频输出

`qwen-audio-3.1-realtime-flash`

1.5元

6元

4.5元

12元

#### 新加坡

模型 ID

文本输入

音频输入

文本输出

音频输出

`qwen-audio-3.1-realtime-flash`

1.677元

6.781元

5.104元

13.636元

## 限流

WebSocket 的 RPM 按连接请求次数统计，与模型响应次数无关；没有单独的并发连接数限制。

#### 华北2（北京）

模型 ID

RPM

TPM

WebSocket 并发连接数

`qwen-audio-3.1-realtime-flash`

60

100,000

无单独限制

#### 新加坡

模型 ID

RPM

TPM

WebSocket 并发连接数

`qwen-audio-3.1-realtime-flash`

60

100,000

无单独限制

## 调用方式

-   [实时语音对话指南](raw/model-user-guide/model-experience/speech-to-speech/qwen-audio-realtime-user-guides.md)
-   [模型接入方式](raw/_short/qwen-audio-realtime-model-access-82f1eed54dbb343f.md)
-   [客户端事件](raw/_short/fun-audiochat-client-events-613371219df1f107.md)
