# qwen-audio-3.1-realtime-plus

实时双工语音对话模型，支持文本和音频输入输出、工具调用、联网搜索及声音复刻。

推理服务供应商为阿里云百炼。默认音色为 `longanqian_v3.1`。接入方式、支持音色和参数详见[实时语音对话指南](raw/model-user-guide/model-experience/speech-and-audio/speech-to-speech/qwen-audio-realtime-user-guides.md)。

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

## 模型价格与限流

仅输出文本时，按文本输出单价计费；输出文本和音频时，仅对音频收取输出费用，伴随文本不另收输出费。

WebSocket 的 RPM 按连接请求次数统计，与模型响应次数无关；没有单独的并发连接数限制。

#### 华北2（北京）

单价单位：每百万 Token。

模型 ID

文本输入

音频输入

文本输出

音频输出

`qwen-audio-3.1-realtime-plus`

5元

40元

40元

150元

限流：RPM 60，TPM 100,000。

#### 新加坡

单价单位：每百万 Token。

模型 ID

文本输入

音频输入

文本输出

音频输出

`qwen-audio-3.1-realtime-plus`

5.833元

46.667元

46.667元

175.002元

限流：RPM 60，TPM 100,000。

## 调用方式

-   [接入指南](raw/model-user-guide/model-experience/speech-and-audio/speech-to-speech/qwen-audio-realtime-user-guides.md)
-   [API 参考](raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory/voice-conversation-api-references.md)
