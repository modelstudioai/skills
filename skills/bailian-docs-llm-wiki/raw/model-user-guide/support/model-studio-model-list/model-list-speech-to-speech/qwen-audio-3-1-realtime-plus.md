# qwen-audio-3.1-realtime-plus

实时双工语音对话模型，支持文本和音频输入输出、工具调用、联网搜索及声音复刻。

推理服务供应商为阿里云百炼。默认音色为 `longanqian_v3.1`。接入方式、支持音色和参数详见[实时语音对话指南](https://help.aliyun.com/zh/model-studio/qwen-audio-realtime-user-guides)。

联网搜索通过 `enable_search` 开启，不能与 Function Calling 同时启用。

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

5.995元

47.963元

47.963元

179.861元

限流：RPM 60，TPM 100,000。
