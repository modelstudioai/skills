# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式双向通信接口，适用于语音交互、实时翻译、多轮对话等需要端到端实时响应的场景。它基于 WebSocket 协议实现，支持模型推理过程中的增量输出与客户端事件注入（如中断、暂停、工具调用反馈）。该 API 不同于标准 RESTful `/v1/chat/completions` 接口，需专用连接生命周期管理。

## 支持的模型与功能

当前 Realtime API 仅支持以下模型：  
- `qwen-audio-realtime-v1`（音频流式输入/输出）  
- `qwen2.5-realtime-v1`（文本流式交互，支持 tool calling 与 stateful session）  

不支持 `qwen-max`、`qwen-plus` 等通用大模型变体。所有可用模型列表及能力说明详见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 的“接入模型与应用”章节。> **注意**：文档中提及的 `qwen-realtime-v0` 已于 2024-09 起下线，实际调用将返回 `404`，请以 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) 中的模型列表为准。

## 关键参数

建立 WebSocket 连接时需在 URL query string 中传入以下必需参数：  
- `model`: 模型 ID（如 `qwen2.5-realtime-v1`），必须与 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 文档中“支持的模型”一致  
- `api_key`: 百炼平台生成的短期有效凭证（有效期 1 小时，不可复用）  
- `session_id`（可选）：用于恢复会话状态，需与前次 `session_id` 匹配且未过期（最长保留 24 小时）  

消息体（JSON 格式）中关键字段包括：  
- `type`: 事件类型（`input_audio`, `input_text`, `tool_result`, `cancel` 等）  
- `content`: 对应内容（如 base64 编码的 PCM 音频片段或 UTF-8 文本）  
- `stream_id`: 客户端生成的唯一标识，用于关联请求与响应流  

## 使用方式

1. **建立连接**：向 `wss://dashscope.aliyuncs.com/realtime/v1` 发起 WebSocket 握手，携带 query 参数；  
2. **发送初始事件**：连接成功后立即发送 `{"type": "session_update", "content": {...}}` 初始化会话配置；  
3. **双向流式交互**：按需发送 `input_audio` / `input_text`，接收 `output_text_delta` / `output_audio_delta` 等增量响应；  
4. **终止连接**：发送 `{"type": "session_terminate"}` 或直接关闭 socket。  

完整流程与示例代码见 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md)。AOQ 客户端 SDK 提供了自动重连、音频编解码封装等能力，推荐生产环境使用 —— 具体集成方式参见 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)。

## 限制和注意事项

- 单连接最大持续时间：30 分钟（超时后服务端强制关闭）；  
- 音频输入采样率必须为 16kHz、单声道、16-bit PCM，否则触发 `invalid_audio_format` 错误；  
- 同一 `session_id` 不支持并发连接，第二次连接将使前一个连接失效；  
- `tool_result` 事件必须在收到对应 `tool_call` 响应后的 10 秒内返回，超时则会话中断；  
- 所有错误响应均通过 `error` 类型事件推送，**不会**返回 HTTP 状态码，需监听 WebSocket message 事件解析。  

> **注意**：原始文档 [概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中提到“支持自定义语音唤醒词”，该功能尚未上线，当前版本仅支持固定唤醒词 `嘿，通义`（中文）或 `Hey, Tongyi`（英文），请勿在 `session_update` 中配置 `wake_word` 字段。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


