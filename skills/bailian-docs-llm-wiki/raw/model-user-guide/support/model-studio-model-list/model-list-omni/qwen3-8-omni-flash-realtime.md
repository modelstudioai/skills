# qwen3.8-omni-flash-realtime

面向实时音视频交互，支持文本与音频输出、多通道音频和工具调用。

## 推理服务供应商

`qwen3.8-omni-flash-realtime` 模型的推理服务供应商为阿里云百炼。

## 模型能力

支持地域：华北2（北京）、新加坡。需使用对应地域的 [API Key](raw/model-api-reference/preparations/get-api-key.md)。

能力项

支持情况

能力项

支持情况

输入模态

文本、流式音频、视频（连续图像帧）

输出模态

文本、音频

Function Calling

支持[自定义工具调用](raw/model-user-guide/model-experience/text-generation-model/tool-calls/qwen-function-calling.md)

MCP

支持远程 MCP 工具，详见[MCP 交互流程](https://help.aliyun.com/zh/model-studio/omni-realtime-interaction-process#qwen38-mcp-flow)

多通道音频

WebSocket 接入支持 1、2、4 声道；多通道使用 16 kHz PCM

视频聚合

通过 `session.video.input.representation_compact` 配置，默认为 `none`，可设为 `normal`

音色

默认 `Tina`，音色参数与试听见[音色列表](https://help.aliyun.com/zh/model-studio/omni-voice-list#qwen38-voices)

支持 WebSocket、WebRTC 和 AOQ 接入，调用示例和 SDK 配置见[实时调用指南](https://help.aliyun.com/zh/model-studio/realtime#7e1da95c25ej6)。

通过 WebSocket 接入时，必须使用绑定业务空间的 WebSocket 地址，配置方法见[建立连接](https://help.aliyun.com/zh/model-studio/realtime#bdaa43cdd7hsd)。

## 上下文限制

参数

值

参数

值

全部输入 Token 总数上限

196608

音频历史

最多 100 轮，累计 600 秒

视频历史

最多 50 轮，累计 240 秒

最大输出 Token 数

65536

超过历史轮次或媒体累计时长上限时，自动丢弃更早的历史信息。媒体累计时长不是整个会话的持续时间。

## 模型价格

模型调用价格请参见[模型价格](raw/model-user-guide/test-1/model-pricing.md)。

输出语音时，`qwen3.8-omni-flash-realtime` 的音频及对应文本分别按音频输出和文本输出单价计费；Qwen3.5-Omni-Realtime 系列仅对音频计费，对应文本不计费。

免费额度：100 万 Token，仅适用于华北2（北京）地域。有效期为自开通百炼、模型发布或申请通过之日起 90 天内（以较晚者为准），详见[免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota#977b13081ab56)。

#### 华北2（北京）

计费项

价格（元）

单位

输入：音频

6

每百万 Token

输出：音频

12

每百万 Token

输入：文本/图片/视频

1.5

每百万 Token

输出：文本

4.5

每百万 Token

#### 新加坡

计费项

价格（元）

单位

输入：音频

6.781

每百万 Token

输出：音频

13.636

每百万 Token

输入：文本/图片/视频

1.677

每百万 Token

输出：文本

5.104

每百万 Token

## 限流

北京、新加坡的限流均为 60 RPM、1,000,000 TPM。模型调用的限流说明请参见[限流](raw/model-user-guide/get-started-with-models/rate-limit.md)。
