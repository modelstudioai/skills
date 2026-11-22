# realtime api directory

实时 API 目录是百炼平台面向低延迟、流式交互场景提供的统一入口，涵盖语音识别、语音合成、音视频对话、实时翻译及[多模态](../concepts/multi-modal.md)交互等核心能力。所有接口均基于 WebSocket 协议设计，支持端到端流式传输与双向实时交互。开发者需通过 [音视频（实时）](../../raw/model-api-reference/realtime-api-directory.md) 文档索引获取各子模块的详细规范。

## 支持的模型与功能

当前目录下包含以下六大类实时能力：
- 实时语音识别（ASR）：支持多语种、带标点与说话人分离的流式识别  
- 实时语音合成（TTS）：低延迟音频流生成，支持情感与语速调节  
- 实时语音对话（Audio Realtime）：端到端双工语音对话，集成 ASR+LLM+TTS  
- 实时音视频翻译（LiveTranslate）：跨语言音视频流实时转译（含字幕与音频输出）  
- 实时[多模态](../concepts/multi-modal.md)（Omni Realtime）：融合语音、文本、图像输入的流式[多模态](../concepts/multi-modal.md)理解与响应  
- 多模态交互协议（MIP）：定义客户端与服务端间帧结构、事件类型与错误码的标准化协议  

各能力的具体模型列表与版本信息请参阅 [音视频（实时）](../../raw/model-api-reference/realtime-api-directory.md) 中的子链接，例如 [实时多模态](../../raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory.md) 和 [实时语音对话](../../raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory.md)。

## 关键参数

所有实时 API 均通过 WebSocket 连接初始化，必需参数包括：
- `model`: 模型标识符（如 `qwen2-audio-realtime-v1`），必须与 [实时语音对话](../../raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory.md) 等子文档中声明的合法值一致  
- `api_key`: 用于鉴权，需在控制台申请并绑定对应模型权限  
- `stream`: 布尔值，强制为 `true`（实时 API 不支持非流式调用）  
- `input_format` / `output_format`: 指定音频编码（如 `pcm`, `opus`）和采样率，须与 SDK 或客户端实际发送格式严格匹配  

> **注意**：部分旧版文档（如早期 `realtime-asr-model-apis.md`）中列出的 `sample_rate` 默认值为 `16000`，但自 v2.3 起，`qwen2-asr-realtime-v1` 模型已要求显式传入 `sample_rate: 48000`，以兼容高清麦克风输入。请以 [实时语音识别](../../raw/model-api-reference/realtime-api-directory/realtime-asr-model-apis.md) 的最新修订版为准。

## 使用方式

1. 建立 WebSocket 连接：向 `wss://dashscope.aliyuncs.com/realtime/v1/{endpoint}` 发起连接（`endpoint` 如 `audio`、`asr`、`omni`）  
2. 发送 `session.update` 控制帧配置参数（含 `model`, `input_format` 等）  
3. 持续发送 `input.audio` 或 `input.text` 帧；接收 `output.audio`、`output.text`、`event` 等响应帧  
4. 使用官方 SDK 可大幅简化流程：推荐优先采用 [WebSocket SDK](../../raw/model-api-reference/realtime-api-directory/realtime-websocket-sdk.md)，其内置重连、心跳、帧序列校验与错误映射  

## 限制和注意事项

- 单连接最大持续时长：15 分钟（超时后需重建连接）  
- 音频输入流需连续，中断超过 3 秒将触发 `session.interrupted` 事件  
- 同一 `api_key` 下，同一 `model` 的并发连接数上限为 10（企业版可申请提升）  
- 所有音频数据必须为原始 PCM（小端序，16-bit）或 Opus 编码，不支持 MP3/WAV 容器封装  
- [AOQ SDK](../../raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api.md) 为实验性轻量级替代方案，目前仅支持 ASR 与 TTS，不兼容多模态交互协议（MIP），生产环境请使用标准 WebSocket SDK  

> **注意**：[多模态交互开发套件](../../raw/model-api-reference/realtime-api-directory/multimodal-interaction-protocol.md) 中定义的 `input.image` 帧暂不支持 JPEG 编码，仅接受 base64 编码的 PNG 数据——该限制未在部分示例代码中明确体现，务必以该文档为准。

## 来源文档

- [音视频（实时）](../../raw/model-api-reference/realtime-api-directory.md)


