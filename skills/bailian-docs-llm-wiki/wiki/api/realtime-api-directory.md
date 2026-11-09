# realtime api directory

Realtime API 是百炼平台提供的低延迟、流式交互式模型服务接口集合，面向语音识别、语音合成、多模态对话、实时翻译等场景。所有接口均基于 WebSocket 协议实现双向流式通信，支持毫秒级响应与持续上下文维护。该目录是实时类 API 的统一入口，各子模块按功能垂直划分，便于开发者按需集成。

## 支持的模型与功能

Realtime API 当前覆盖以下核心能力：
- **实时多模态交互**：支持图像+语音+文本联合理解与生成，适用于智能座舱、具身智能等场景，详见 [实时多模态](../../raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory.md)；
- **实时语音识别（ASR）**：提供高精度、低延迟流式语音转写，支持多语种与领域热词定制；
- **实时语音合成（TTS）**：支持情感化、多音色流式音频生成，时延可控制在 300ms 内；
- **实时语音对话（Audio Realtime）**：端到端语音对话系统，内置 ASR+LLM+TTS 链路，支持打断、静音检测与角色音色切换；
- **实时音视频翻译（LiveTranslate）**：支持双语同传、字幕同步与画面区域标注，适用于跨国会议与直播场景；
- **AOQ SDK**：轻量级客户端 SDK，封装连接管理、重连、缓冲与事件回调，降低接入复杂度，参考 [AOQ SDK](../../raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api.md)；
- **多模态交互协议（MIP）**：定义跨模态消息结构与状态机规范，是构建自定义多模态应用的基础，详见 [多模态交互开发套件](../../raw/model-api-reference/realtime-api-directory/multimodal-interaction-protocol.md)。

> **注意**：[实时语音对话](../../raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory.md) 文档中声明的 `max_turns` 默认值为 10，但最新 SDK 实现中已移除此限制，实际由服务端会话策略动态控制；请以 [AOQ SDK](../../raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api.md) 的运行时行为为准。

## 关键参数

所有 Realtime API 均通过 WebSocket 连接初始化，关键请求参数包括：
- `model`: 必填，指定模型标识符（如 `qwen2-audio-realtime-v1`, `qwen2-omni-realtime-v1`）；
- `api_key`: 认证凭证，需通过百炼控制台获取；
- `stream`: 布尔值，必须设为 `true`；
- `enable_intermediate_results`: 控制是否返回中间识别/生成结果（仅 ASR/TTS/TTS 支持）；
- `voice`: TTS 或 Audio Realtime 场景下指定发音人 ID（如 `zhiyan`、`xiaoyan`）；
- `language`: ASR/LiveTranslate 场景下指定输入/目标语言代码（如 `zh`, `en`, `ja`）。

## 使用方式

1. 建立 WebSocket 连接：向 `wss://dashscope.aliyuncs.com/realtime/v1/{endpoint}` 发起连接（`endpoint` 对应具体能力，如 `asr`, `tts`, `audio`）；
2. 发送 `session.update` 消息初始化会话参数；
3. 流式发送音频帧（Base64 编码 PCM 数据）或文本事件；
4. 接收服务端推送的 `response.text.delta`、`response.audio.delta`、`event.error` 等结构化事件；
5. 主动发送 `session.end` 或等待超时自动断连。

完整流程与事件格式请参阅 [实时多模态](../../raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory.md) 中的“交互流程”章节。

## 限制和注意事项

- 单连接最大时长：30 分钟（含空闲时间），超时后需重建连接；
- 音频采样率固定为 16kHz，单声道，PCM 格式（S16LE）；
- 每秒音频帧大小建议 ≤ 64KB，过大将触发服务端限流；
- 所有 Realtime API **不支持 HTTP 轮询调用**，仅限 WebSocket 流式交互；
- 多模态交互中图像帧需经 Base64 编码后作为 `image_url` 字段传入，暂不支持二进制流上传；
- 错误码 `429 Too Many Requests` 表示当前账号 QPS 超限，需检查配额或联系技术支持。

> **注意**：[实时语音识别](../../raw/model-api-reference/realtime-api-directory/realtime-asr-model-apis.md) 文档中提及的 `punctuation_prediction` 参数在 v2.3+ 版本中已弃用，新会话应使用 `enable_punctuation` 替代，兼容性说明见 [实时多模态](../../raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory.md) 的“参数变更日志”小节。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-directory.md)


