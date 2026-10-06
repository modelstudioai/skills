# omni realtime api

omni realtime api 是百炼平台提供的低延迟、流式多模态交互接口，支持语音、文本、图像等多类型输入的实时处理与响应。该 API 采用 WebSocket 协议实现双向通信，适用于实时对话、音视频分析、交互式智能体等场景。其设计强调端到端时延可控、事件驱动、状态可追踪。

## 支持的模型与功能

当前仅支持 `qwen2-audio-7b` 和 `qwen2-vl-7b` 两个实时推理模型，分别面向音频和视觉-语言联合理解任务。模型能力包括：实时语音转写（ASR）、语音指令识别、图像内容描述、多轮上下文感知的图文混合问答。所有功能均通过统一 WebSocket 连接按事件流交付，不支持 HTTP 同步调用。详细模型能力边界请参见 [实时多模态](../../raw/model-api-reference/omni-realtime-api.md) 文档。

## 关键参数

建立连接时需在 WebSocket URL 中携带以下必需查询参数：
- `model`: 模型标识符（如 `qwen2-audio-7b`），必须与实际请求内容模态匹配；
- `stream`: 固定为 `true`，不支持关闭流式模式；
- `api_key`: 百炼平台生成的短期有效凭证（有效期 10 分钟），需通过 `Authorization: Bearer <token>` 头传递；
- `max_tokens` 和 `temperature` 等生成参数需在 `input` 事件 payload 中以 JSON 形式传入，不可在 URL 中设置。  
完整参数定义与默认值详见 [模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)。

## 使用方式

1. 客户端发起 WebSocket 连接，URL 格式为：`wss://dashscope.aliyuncs.com/api/v1/omni/realtime?model=...&stream=true`；  
2. 连接建立后，发送 `input` 事件（含音频二进制帧或 base64 编码图像 + 文本 prompt）；  
3. 服务端按序返回 `output`、`progress`、`error` 等[服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)，客户端须实现事件分发与超时重试逻辑；  
4. 连接空闲超时为 60 秒，超时后服务端将主动关闭连接。

## 限制和注意事项

- 单次连接最长持续 5 分钟，超时后需重建连接；  
- 音频输入采样率必须为 16kHz，单帧时长建议 20–40ms，过长帧会导致 ASR 延迟升高；  
- 图像输入分辨率上限为 1920×1080，超出部分将被中心裁剪；  
> **注意**：原始文档中提及“支持 `qwen2-omni-7b` 全模态模型”，但该模型尚未上线生产环境，当前实际可用模型仅限 `qwen2-audio-7b` 和 `qwen2-vl-7b`，请以 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 中定义的 `model` 枚举值为准。  
- 所有事件类型（包括 `input`、`output`、`session.update`）均需严格遵循 JSON Schema 校验，字段缺失或类型错误将触发 `error` 事件并终止会话。

## 来源文档

- [实时多模态](../../raw/model-api-reference/omni-realtime-api.md)


