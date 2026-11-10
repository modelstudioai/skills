# realtime api directory

Realtime API 是百炼平台提供的低延迟、流式交互式模型服务接口集合，面向语音识别、合成、对话、翻译及多模态实时交互等场景。所有接口均基于 WebSocket 协议实现双向流式通信，支持毫秒级响应与持续上下文维护。开发者需通过统一认证和连接管理接入，具体能力按功能域划分。

## 支持的模型/功能

Realtime API 当前覆盖以下核心能力方向：
- 实时多模态交互：支持图像+语音+文本联合理解与生成，详见 [实时多模态](../../raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory.md)  
- 实时语音识别（ASR）：提供高精度、低延迟流式转写，支持多语种与自定义热词  
- 实时语音合成（TTS）：支持情感化、多音色流式音频生成，参见 [实时语音合成](../../raw/model-api-reference/realtime-api-directory/realtime-tts-model-apis.md)  
- 实时语音对话（Audio Chat）：端到端语音输入→理解→生成→TTS输出闭环，文档位于 [实时语音对话](../../raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory.md)  
- 实时音视频翻译：支持双语实时字幕与语音同传，能力说明见 [实时音视频翻译](../../raw/model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory.md)  
- AOQ SDK 与多模态交互协议：面向嵌入式与边缘设备的轻量接入方案，参考 [AOQ SDK](../../raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api.md) 和 [多模态交互开发套件](../../raw/model-api-reference/realtime-api-directory/multimodal-interaction-protocol.md)

> **注意**：[实时语音对话](../../raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory.md) 中描述的 `input_mode: "audio"` 已于 v2.3 版本弃用，当前仅支持 `input_mode: "stream"`；该变更未在 [概述](../../raw/model-api-reference/realtime-api-directory/realtime-api-overview.md) 中同步更新，请以实际接口文档为准。

## 关键参数

所有 Realtime API 共享以下基础连接与控制参数：
- `model`: 必填，指定模型 ID（如 `qwen-audio-realtime-v1`, `qwen-omni-realtime-v2`），不同功能域模型不可混用  
- `temperature`: 浮点数，控制生成随机性（0.0–1.0），默认 `0.7`  
- `max_output_tokens`: 单次响应最大 token 数，上限依模型而异（ASR/TTS 类接口不适用）  
- `enable_intermediate_results`: 布尔值，启用中间结果流（如 ASR 的 partial transcript）  
- `audio_format`: 音频编码格式（`pcm`, `opus`, `mp3`），必须与 `sample_rate` 匹配  

## 使用方式

1. 建立 WebSocket 连接：向 `wss://dashscope.aliyuncs.com/realtime/v1/<endpoint>` 发起连接（`<endpoint>` 对应各子功能，如 `asr`, `tts`, `omni`）  
2. 发送 `session.update` 消息初始化会话，携带认证 `api_key` 及上述关键参数  
3. 按协议分帧发送音频/文本数据（如 ASR 发送 `input.audio`，TTS 接收 `output.audio`）  
4. 处理服务端返回的 `event` 消息（`response.text.delta`, `response.audio.delta`, `error` 等）  
完整交互流程与消息结构详见 [概述](../../raw/model-api-reference/realtime-api-directory/realtime-api-overview.md)

## 限制和注意事项

- 单连接最大持续时长为 30 分钟，超时后需重连并重建会话  
- 音频流要求严格时间对齐：采样率误差不得超过 ±50Hz，静音填充需显式标记（`input.audio.silence`）  
- TTS 接口不支持实时变调或动态语速调整，相关参数（`pitch`, `rate`）仅在会话初始化时生效  
- 所有 Realtime API 均不支持 HTTP fallback，必须使用 WebSocket；HTTP 接口仅用于鉴权与元数据查询  
- 错误码 `429001` 表示并发连接超限（默认每 key 最多 10 路并发），需检查连接复用策略  

> **注意**：[实时语音识别](../../raw/model-api-reference/realtime-api-directory/realtime-asr-model-apis.md) 中列出的 `language: "auto"` 检测能力在部分方言场景下准确率显著下降，建议明确指定 `language: "zh-CN"` 或 `"en-US"` 等标准代码。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-directory.md)


