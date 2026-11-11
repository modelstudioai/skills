# realtime api directory

Realtime API 是百炼平台提供的低延迟、流式交互式模型服务接口集合，面向语音识别、语音合成、多模态对话、实时翻译等场景。所有接口均基于 WebSocket 协议实现双向流式通信，支持端到端毫秒级响应。该目录是 Realtime 系列 API 的统一入口，各子能力按功能垂直划分，文档结构与实际服务模块严格对齐。

## 支持的模型与功能

当前 Realtime API 目录涵盖以下核心能力：
- **实时多模态交互**：支持图像+语音+文本联合理解与生成，详见 [实时多模态](../../raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory.md)  
- **实时语音识别（ASR）**：提供高精度、低延迟流式语音转文本，支持多语种与领域适配  
- **实时语音合成（TTS）**：支持情感可控、音色可选的流式音频生成  
- **实时语音对话（Audio Chat）**：端到端语音输入→语义理解→语音输出闭环，适用于智能座舱、IVR 等场景  
- **实时音视频翻译（LiveTranslate）**：支持双语实时字幕与语音同传，含源语/目标语双路音频流  
- **AOQ SDK 集成接口**：面向移动端的轻量封装，简化连接管理与事件监听，详见 [AOQ SDK](../../raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api.md)  
- **多模态交互协议（MIP）**：定义跨模态消息格式与状态机，是构建复合交互应用的基础规范，详见 [多模态交互开发套件](../../raw/model-api-reference/realtime-api-directory/multimodal-interaction-protocol.md)

> **注意**：[实时语音对话](raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory.md) 文档中描述的 `audio_chat_v1` 接口已废弃，新项目请使用 `realtime_conversation_v2`（见 [实时多模态](../../raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory.md)），旧文档未同步更新。

## 关键参数

所有 Realtime API 均通过 WebSocket 连接初始化，必需参数包括：
- `model`: 模型标识符（如 `qwen2-audio-realtime`, `qwen2-omni-realtime`），必须与所选能力匹配  
- `api_key`: 用于鉴权，需在控制台申请并启用对应模型权限  
- `stream`: 布尔值，必须为 `true`（Realtime API 不支持非流式调用）  
- `response_format`: 可选，指定返回结构（`json` 或 `binary`，后者用于原始音频流）  
- `temperature` / `top_p`: 仅部分模型支持，用于控制生成随机性（参见 [实时多模态](../../raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory.md)）

## 使用方式

1. 建立 WebSocket 连接：`wss://dashscope.aliyuncs.com/realtime/v1/{endpoint}`，其中 `endpoint` 对应具体能力（如 `asr`, `tts`, `omni`）  
2. 发送 `session.update` 消息初始化会话，携带上述关键参数  
3. 按协议发送 `input.audio`、`input.text` 或 `input.image` 等事件帧  
4. 接收 `output.*` 类型响应帧（如 `output.text.delta`, `output.audio.chunk`）  
5. 主动发送 `session.terminate` 或等待超时自动断连  

完整交互流程与事件类型定义，请参考 [概述](../../raw/model-api-reference/realtime-api-directory/realtime-api-overview.md)。

## 限制和注意事项

- 单连接最大持续时长为 30 分钟；超时后需重建连接  
- 音频输入采样率须为 16kHz，PCM 编码，单通道；不支持 MP3/WAV 封装  
- TTS 输出音频默认为 24kHz PCM，若需其他格式需自行转码  
- 实时翻译（LiveTranslate）要求源语与目标语必须在支持语种列表内，且不可动态切换语种对（见 [实时音视频翻译](../../raw/model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory.md)）  
- 所有 Realtime API 均不支持 HTTP 轮询或 RESTful 调用方式，仅限 WebSocket 流式交互

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-directory.md)


