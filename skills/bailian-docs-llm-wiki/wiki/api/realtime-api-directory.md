# realtime api directory

实时 API 目录汇总了百炼平台支持的低延迟、流式交互类音视频模型能力，涵盖语音识别（ASR）、语音合成（TTS）、多模态理解与生成、实时翻译等场景。所有接口均面向流式输入/输出设计，适用于会议转录、智能客服、实时字幕、语音助手等对端到端延迟敏感的应用。开发者需结合具体模型文档确认能力边界与调用细节。

## 支持的模型与功能

当前实时 API 覆盖以下核心能力类别：
- 实时语音识别（ASR）：支持中文、英文及多语种流式识别，含标点恢复与说话人分离选项  
- 实时语音合成（TTS）：提供高自然度、低延迟的流式音频生成，支持音色控制与语速调节  
- 实时多模态交互（Omni-Realtime）：融合语音、文本、图像（如摄像头帧）的联合理解与响应  
- 实时音视频翻译（LiveTranslate）：支持双语语音流的端到端同传翻译，含源语识别+目标语合成一体化链路  
- 专用音频模型：包括 [Qwen-Audio-Realtime](../../raw/model-api-reference/realtime-api-directory.md) 和 [Qwen-Audio-Live](../../raw/model-api-reference/realtime-api-directory.md)，分别面向高精度离线音频处理与强鲁棒性在线直播场景  

> **注意**：[Qwen-Audio-Live](../../raw/model-api-reference/realtime-api-directory.md) 文档中声明支持“弱网重传”，但最新 SDK v2.4.0 实测该机制默认关闭，需显式设置 `enable_retransmission=true` 才生效；请以 [实时多模态](../../raw/model-api-reference/realtime-api-directory.md) 的参数说明为准。

## 关键参数

通用关键参数（各子 API 共享）：
- `model`: 必填，模型标识符（如 `qwen-audio-realtime-v1`, `qwen-asr-realtime-zh`）  
- `stream`: 布尔值，必须为 `true`（实时 API 不支持非流式调用）  
- `response_format`: 可选，指定返回格式（`json` 或 `wav`/`mp3`，仅 TTS/LiveTranslate 生效）  
- `audio_input_format`: ASR/TTS 类接口必填，如 `pcm-16k-1ch`、`opus-48k-2ch`  
- `max_latency_ms`: 推荐设置（单位毫秒），用于服务端调度优化，非硬性超时  

## 使用方式

1. 通过 `POST /v1/realtime/chat/completions` 统一入口发起请求（认证方式与标准 Chat API 一致）  
2. 请求体以 `multipart/form-data` 或二进制流方式上传音频分片（chunk），每片建议 ≤ 200ms 音频数据  
3. 响应以 Server-Sent Events（SSE）流式返回，事件类型包括 `audio`, `text`, `segment`, `error` 等  
4. 客户端需按序拼接 `audio` 事件载荷，并监听 `segment` 事件获取语义完整单元（如一句话）  

详细协议规范与示例代码见 [实时语音识别](../../raw/model-api-reference/realtime-api-directory.md) 中的“请求/响应结构”章节。

## 限制和注意事项

- 单次会话最长持续 30 分钟，超时后连接自动关闭，需重建会话  
- 音频采样率必须严格匹配模型要求（如 `qwen-asr-realtime-zh` 仅接受 `16k` 单声道 PCM，不兼容 `48k` 或立体声）  
- 实时多模态接口（`qwen-omni-realtime-v1`）暂不支持图像帧与音频帧的时间戳对齐校验，需客户端自行同步  
- 所有实时 API 均不支持 `system` 消息字段，角色设定需通过 `user`/`assistant` 消息中的指令文本表达  
- 错误码 `429 Too Many Requests` 表示流式并发数超限（默认单账号 5 路并发），可通过工单申请提升配额

## 来源文档

- [音视频（实时）](../../raw/model-api-reference/realtime-api-directory.md)


