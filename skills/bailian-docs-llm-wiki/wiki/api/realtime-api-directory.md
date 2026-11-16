# realtime api directory

Realtime API 目录汇总了百炼平台支持的低延迟、流式交互类模型能力，覆盖语音识别（ASR）、语音合成（TTS）、音视频翻译、多模态实时对话等场景。所有接口均面向实时性敏感的应用（如智能座舱、远程会议、AI 陪练）设计，要求端到端延迟控制在数百毫秒量级。该目录本身不提供具体接口定义，而是作为功能入口索引，各子能力详见对应文档。

## 支持的模型/功能

当前 Realtime API 目录涵盖以下核心能力模块：
- 实时多模态交互：支持音频+文本+视觉信号联合理解与生成，适用于带摄像头的语音助手场景 [实时多模态](../../raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory.md)  
- 实时语音识别（ASR）：流式返回识别结果，支持热词、标点恢复、语种自适应 [实时语音识别](../../raw/model-api-reference/realtime-api-directory/realtime-asr-model-apis.md)  
- 实时语音合成（TTS）：低延迟音频流输出，支持情感韵律控制与多音色切换 [实时语音合成](../../raw/model-api-reference/realtime-api-directory/realtime-tts-model-apis.md)  
- 实时语音对话（Audio Realtime）：端到端语音输入→理解→生成→合成闭环，内置对话状态管理 [实时语音对话](../../raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory.md)  
- 实时音视频翻译（LiveTranslate）：支持双语字幕同步生成与音频转译，含源语/目标语时间对齐 [实时音视频翻译](../../raw/model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory.md)  
- AOQ SDK：面向嵌入式设备的轻量化实时接入套件，提供 C/C++ 接口封装 [AOQ SDK](../../raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api.md)  
- 多模态交互协议（MIP）：定义跨模态事件（如“用户抬手+说‘播放’”）的标准化交互格式 [多模态交互开发套件](../../raw/model-api-reference/realtime-api-directory/multimodal-interaction-protocol.md)

> **注意**：`audio-realtime-api-directory.md` 中描述的“单轮最大上下文长度为 512 tokens”与 `omni-realtime-api-directory.md` 中“支持动态扩展至 2048 tokens”的说明存在不一致；实际调用时请以最新发布的 [实时多模态](../../raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory.md) 文档为准。

## 关键参数

所有 Realtime API 共享以下基础参数（部分能力支持扩展参数）：
- `model`: 必填，指定模型标识符（如 `qwen2-audio-realtime-v1`, `qwen2-asr-streaming-v1`）  
- `stream`: 必填，固定为 `true`，禁用流式模式将导致 400 错误  
- `response_format`: 可选，支持 `json`（结构化事件）或 `binary`（原始音频流），默认 `json`  
- `sample_rate`: TTS/LiveTranslate 等音频输出接口必填，单位 Hz（如 `16000`, `24000`）  
- `language`: ASR/TTS/LiveTranslate 必填，ISO 639-1 格式（如 `zh`, `en`, `ja`）  

## 使用方式

1. **认证**：使用 `Authorization: Bearer <api_key>` 请求头，API Key 需具备 `realtime` 权限 scope  
2. **连接**：通过 WebSocket（推荐）或 HTTP/2 Server-Sent Events（SSE）建立长连接  
3. **数据帧**：按 [多模态交互开发套件](../../raw/model-api-reference/realtime-api-directory/multimodal-interaction-protocol.md) 定义的二进制帧格式发送音频/文本/事件数据  
4. **响应处理**：服务端以事件流形式返回 `partial`, `final`, `error`, `metadata` 等类型消息，需按序解析并维护本地状态  

## 限制和注意事项

- 单连接最大持续时长：15 分钟（超时后需重连，会话状态不保留）  
- 音频输入采样率必须与模型训练一致（常见为 16kHz 或 24kHz），不支持运行时重采样  
- 实时 ASR 不支持离线模式；若需断网可用，请参考 [实时语音识别](../../raw/model-api-reference/realtime-api-directory/realtime-asr-model-apis.md) 中的边缘部署方案  
- 所有 Realtime API 均不支持 `max_tokens` 或 `temperature` 等通用 LLM 参数，相关控制需通过专用参数（如 `asr_confidence_threshold`, `tts_speed`）实现  
- AOQ SDK 当前仅支持 Linux ARM64 架构，x86_64 支持计划见 [AOQ SDK](../../raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api.md) 更新日志

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-directory.md)


