# realtime api directory

Realtime API 是百炼平台提供的低延迟、流式交互式模型服务接口集合，面向语音识别、合成、对话、翻译及多模态实时交互等场景。所有接口均基于 WebSocket 协议设计，支持双向流式数据传输与事件驱动响应。开发者需通过统一的 Realtime API 入口接入，并按具体能力选择子模块 [Realtime API](../../raw/model-api-reference/realtime-api-directory.md)。

## 支持的模型与功能

当前 Realtime API 目录涵盖以下核心能力模块：
- **实时多模态交互**：支持图像+语音+文本联合理解与生成，适用于智能座舱、AR 等场景，协议定义见 [实时多模态](../../raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory.md)；
- **实时语音识别（ASR）**：提供毫秒级延迟的流式语音转写，支持热词、语种自适应等高级配置；
- **实时语音合成（TTS）**：支持情感控制、语速/音调调节及端到端流式音频输出；
- **实时语音对话（Audio Chat）**：集成 ASR + LLM + TTS 的端到端语音对话流水线，底层模型可选 Qwen2-Audio 或 Qwen-VL-Realtime；
- **实时音视频翻译（LiveTranslate）**：支持双语实时字幕、语音同传与目标语言音频流输出；
- **AOQ SDK 与多模态交互开发套件**：提供客户端 SDK 和标准化交互协议，降低终端接入复杂度，详见 [AOQ SDK](../../raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api.md) 和 [多模态交互开发套件](../../raw/model-api-reference/realtime-api-directory/multimodal-interaction-protocol.md)。

> **注意**：`audio-realtime-api-directory.md` 中描述的“单模型全链路”模式已被 `omni-realtime-api-directory.md` 中的统一多模态协议逐步替代；新项目应优先采用 Omni 协议，旧版 Audio Chat 接口仍兼容但不再新增功能。

## 关键参数

所有 Realtime API 请求均通过 WebSocket 连接建立，关键连接与消息参数包括：
- `model`: 必填，指定具体能力模型，如 `qwen2-audio-realtime`、`qwen-vl-realtime`、`asr-qwen2` 等（详见各子目录文档）；
- `stream`: 布尔值，必须为 `true`，Realtime API 不支持非流式调用；
- `response_format`: 可选，控制响应结构，支持 `json`（默认）或 `delta`（增量 token 流）；
- `input_format` / `output_format`: 音频类接口需显式声明编码格式（如 `pcm16`、`opus`），参见 [实时语音识别](../../raw/model-api-reference/realtime-api-directory/realtime-asr-model-apis.md) 与 [实时语音合成](../../raw/model-api-reference/realtime-api-directory/realtime-tts-model-apis.md) 文档；
- `enable_intermediate_results`: 仅 ASR/TTS 支持，启用后返回中间识别/合成结果。

## 使用方式

1. **建立 WebSocket 连接**：向 `wss://dashscope.aliyuncs.com/realtime/v1/<endpoint>` 发起连接，其中 `<endpoint>` 根据能力类型取值（如 `asr`、`tts`、`chat`、`omni`）；
2. **发送初始化消息（`session.update`）**：携带 `model`、`stream` 及其他配置参数；
3. **发送数据帧（`input.audio` / `input.text` / `input.image`）**：按协议分片推送原始数据（如 PCM 音频 chunk）；
4. **接收响应事件（`response.output` / `response.audio` / `event.error`）**：解析流式事件并处理业务逻辑。

完整交互流程与示例代码请参考 [Realtime API](../../raw/model-api-reference/realtime-api-directory.md) 主文档及各子模块说明。

## 限制和注意事项

- 单连接最大持续时长为 30 分钟，超时后需重连并重新初始化 session；
- 音频输入采样率须严格匹配模型要求（常见为 16kHz PCM，16-bit little-endian），不支持自动重采样；
- 同一 `app_id` 下并发 WebSocket 连接数上限为 100，超出将触发 `429 Too Many Connections`；
- `livetranslate-realtime-api-directory.md` 中提及的“离线缓存翻译结果”功能暂未上线，实际调用时该字段被忽略；
- 所有 Realtime API 均需使用 DashScope SDK v3.10.0+ 或手动实现符合 [多模态交互开发套件](../../raw/model-api-reference/realtime-api-directory/multimodal-interaction-protocol.md) 的协议栈，旧版 HTTP 封装方式已废弃。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-directory.md)


