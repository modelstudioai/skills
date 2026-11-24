# realtime api directory

实时 API 目录汇总了百炼平台支持的低延迟、流式交互类音视频模型能力，适用于语音识别、语音合成、多模态理解与生成、实时翻译等场景。所有接口均基于 WebSocket 协议设计，支持逐帧/逐 token 流式响应与双向实时控制。该目录结构化呈现各模型的接入路径、能力边界与调用约束，是开发者集成实时音视频功能的核心参考。

## 支持的模型与功能

当前目录涵盖以下核心实时能力模块：
- **实时多模态交互**：支持音频+文本+（可选）图像输入的联合理解与生成，详见 [实时多模态](../../raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory.md)；
- **实时语音识别（ASR）**：提供高精度、低延迟的流式语音转写，支持多语种与自定义热词，参见 [实时语音识别](../../raw/model-api-reference/realtime-api-directory/realtime-asr-model-apis.md)；
- **实时语音合成（TTS）**：支持情感可控、语速可调的流式音频生成，兼容多种音色与语言，详见 [实时语音合成](../../raw/model-api-reference/realtime-api-directory/realtime-tts-model-apis.md)；
- **Qwen-Audio 系列**：包括 `Qwen-Audio-Realtime`（端到端多模态流式模型）和 `Qwen-Audio-Live`（轻量级直播场景优化模型），其能力差异与适用场景请查阅 [Qwen-Audio-Realtime](../../raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory.md) 和 [Qwen-Audio-Live](../../raw/model-api-reference/realtime-api-directory/qwen-audio-live-api-directory.md)；
- **实时音视频翻译**：支持双语语音流的端到端实时互译，含字幕同步与延迟控制，见 [实时音视频翻译](../../raw/model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory.md)。

> **注意**：`Qwen-Audio-Live` 文档中声明的最低采样率要求为 8kHz，但 [实时语音识别](../../raw/model-api-reference/realtime-api-directory/realtime-asr-model-apis.md) 主流接口实际要求 16kHz。建议以 ASR 文档为准，避免因采样率不匹配导致识别失败。

## 关键参数

所有实时 API 共享以下基础参数（部分模型支持扩展字段）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-audio-realtime-v1`、`asr-realtime-zh-cn`；必须与目录中各子文档明确列出的模型 ID 严格一致 |
| `stream` | boolean | 是 | 固定为 `true`；实时 API 不支持非流式模式 |
| `audio_format` | string | 是（ASR/TTS/翻译） | 如 `pcm`, `wav`, `opus`；需与实际传输格式及 [实时语音识别](../../raw/model-api-reference/realtime-api-directory/realtime-asr-model-apis.md) 中定义的格式列表完全匹配 |
| `sample_rate` | integer | 是（ASR/TTS） | 单位 Hz；常见值为 `16000`；`Qwen-Audio-Live` 文档虽标注支持 `8000`，但实测兼容性受限，推荐统一使用 `16000` |

## 使用方式

1. 建立 WebSocket 连接，URL 格式为 `wss://dashscope.aliyuncs.com/api/v1/realtime/{model}`（`{model}` 替换为具体模型 ID）；  
2. 首帧发送 `session.update` 消息初始化会话（含 `model`, `stream`, `audio_format` 等参数）；  
3. 后续按帧发送 `input.audio`（ASR/翻译）或 `input.text`（TTS/多模态）事件；  
4. 服务端通过 `output.*` 事件流式返回结果，客户端需实现分帧解析与缓冲管理。  
完整协议规范与示例代码请参考 [概述](../../raw/model-api-reference/realtime-api-directory/realtime-api-overview.md)。

## 限制和注意事项

- 单连接最大时长：15 分钟（超时后需重连并新建会话）；  
- 音频帧大小限制：单帧 PCM 数据不得超过 64KB（约 2 秒 16kHz 单声道）；  
- 并发连接数：免费版限 2 路，企业版按配额配置；  
- 所有实时 API **不支持 HTTP 轮询或 RESTful 调用**，仅限 WebSocket；  
- 错误码统一遵循 `4xxx`（客户端错误）与 `5xxx`（服务端错误）范围，详细含义见 [概述](../../raw/model-api-reference/realtime-api-directory/realtime-api-overview.md)；  
- > **注意**：[实时音视频翻译](../../raw/model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory.md) 文档中提及的“双语字幕自动对齐”功能，在 v1.2.0 版本后已移除，当前仅支持单语种输出，新需求请使用 `livetranslate-realtime-v2` 模型。

## 来源文档

- [音视频（实时）](../../raw/model-api-reference/realtime-api-directory.md)


