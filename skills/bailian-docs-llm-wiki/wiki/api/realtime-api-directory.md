# realtime api directory

Realtime API 目录提供低延迟、流式交互的实时 AI 能力接入入口，覆盖语音识别（ASR）、语音合成（TTS）、多模态理解与生成、音视频实时翻译及端到端语音对话等核心场景。所有接口均基于 WebSocket 协议设计，支持双向流式数据传输与事件驱动响应。该目录是 [Realtime API (raw/model-api-reference/realtime-api-directory.md)](../../raw/model-api-reference/realtime-api-directory.md) 的顶层导航结构，各子能力文档详见其下级链接。

## 支持的模型与功能

- **实时语音识别（ASR）**：支持中英文混合识别、标点预测、语速自适应，模型包括 `qwen2-audio-asr-base` 和 `qwen2-audio-asr-pro`  
- **实时语音合成（TTS）**：提供多音色、情感可控、低延迟[流式输出](../concepts/streaming-output.md)，支持 `qwen2-tts-stream-v1` 等模型  
- **实时语音对话（Audio Realtime）**：端到端双工对话能力，集成 ASR+LLM+TTS 流水线，适用于智能座舱、客服机器人等场景  
- **实时音视频翻译（LiveTranslate）**：支持 12 种语言间音视频流实时互译，含唇动同步与延迟优化选项  
- **多模态实时交互**：融合音频、文本、图像输入的联合理解与响应，详见 [实时多模态](../../raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory.md)  
- **AOQ SDK 集成支持**：提供轻量级客户端 SDK，封装连接管理、重连、缓冲与事件分发，参考 [AOQ SDK](../../raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api.md)

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen2-audio-asr-base`；必须与所选能力类型匹配，详见各子文档 |
| `audio_encoding` | string | 否（默认 `pcm`） | 支持 `pcm`, `wav`, `opus`；注意 [实时语音识别](../../raw/model-api-reference/realtime-api-directory/realtime-asr-model-apis.md) 中 `opus` 需显式声明采样率 |
| `sample_rate` | integer | 否（默认 `16000`） | 仅当 `audio_encoding` 为 `pcm` 或 `wav` 时生效；`opus` 编码需在容器头中携带，API 不校验该字段 |
| `enable_interim_results` | boolean | 否（默认 `false`） | 是否返回中间识别结果；启用后可能增加带宽消耗与服务端负载 |

> **注意**：`sample_rate` 在 [实时语音合成](../../raw/model-api-reference/realtime-api-directory/realtime-tts-model-apis.md) 文档中被标记为“强制要求”，但实际服务端对 TTS 输入无采样率依赖——该描述已过时，以当前 API 行为为准。

## 使用方式

1. 建立 WebSocket 连接：`wss://dashscope.aliyuncs.com/realtime/v1/{service}`，其中 `{service}` 取值如 `asr`, `tts`, `audio` 等  
2. 发送 `session.update` 消息初始化会话，携带 `model`、`audio_encoding` 等参数  
3. 持续发送 `input.audio`（二进制帧）或 `input.text`（JSON）事件  
4. 接收 `output.*` 事件（如 `output.transcript`, `output.audio`）及 `error` 事件  
5. 主动发送 `session.terminate` 或等待超时自动断连  

完整协议规范与事件格式定义见 [多模态交互开发套件](../../raw/model-api-reference/realtime-api-directory/multimodal-interaction-protocol.md)，该文档亦涵盖错误码映射与重连策略。

## 限制和注意事项

- 单连接最大持续时长：15 分钟（含静默期），超时后需重建连接  
- 音频流输入速率需严格匹配 `sample_rate`，否则触发 `audio_rate_mismatch` 错误  
- 实时语音对话（`audio` 服务）不支持 `input.text` 与 `input.audio` 混合输入；若需文本触发，请使用 `audio` + `text_input_mode: "enabled"` 配置（参见 [实时语音对话](../../raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory.md)）  
- 所有 Realtime API 均不支持 HTTP 回调，仅通过 WebSocket 流式响应；若需异步通知，请自行实现客户端状态机  
- 免费调用额度按连接数而非请求数计费，频繁短连接将快速耗尽配额

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-directory.md)


