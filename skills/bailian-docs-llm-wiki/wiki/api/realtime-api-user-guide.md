# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式响应的模型调用接口，适用于对话交互、实时语音/文本生成等场景。它支持 WebSocket 和 HTTP/2 双协议，提供 token 级别[流式输出](../concepts/streaming-output.md)与事件驱动控制能力。详细设计目标和适用边界请参见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)。

## 支持的模型与功能

- **当前支持模型**：`qwen-max`、`qwen-plus`、`qwen-turbo`（仅限 `stream=true` 模式）、`qwen2-audio`（音频流式输入/输出）  
- **核心功能**：  
  - 完整消息流（`message_start` → `content_block_delta` → `message_stop`）  
  - 中断控制（`input_interrupt` 事件触发即时停止）  
  - 工具调用（function calling）与结构化输出（需启用 `tool_choice="auto"` 或显式指定）  
  - 多模态输入（图像 base64、音频 PCM 流）——具体格式要求详见 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide.md)  

> **注意**：文档中提及的 `qwen-vl` 模型在 v2024.09 版本后已不再支持 Realtime API，实际可用模型以控制台「API 调用」页的下拉列表为准；该不一致已在 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 的最新修订版中修正。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型 ID，必须为 Realtime API 支持列表中的值 |
| `messages` | array | 是 | 对话历史，格式同标准 Chat API，但 `role="user"` 内容可含 `image_url` 或 `audio` 字段 |
| `stream` | boolean | 是（固定为 `true`） | Realtime API 强制流式，设为 `false` 将返回 400 错误 |
| `temperature` | number | 否 | 默认 `0.7`，范围 `[0.0, 2.0]` |
| `max_tokens` | integer | 否 | 单次响应最大 token 数，硬上限 `8192`（超出将截断） |
| `tools` | array | 否 | 工具定义数组，每个工具需含 `type="function"` 和 `function` 字段 |

## 使用方式

1. **建立连接**：  
   - WebSocket：`wss://dashscope.aliyuncs.com/realtime/v1/chat`（需携带 `Authorization: Bearer <api_key>`）  
   - HTTP/2：`POST https://dashscope.aliyuncs.com/realtime/v1/chat`（Header 中设置 `Content-Type: application/json`）  
2. **发送请求帧**（WebSocket）或请求体（HTTP/2）：JSON 格式，包含上述关键参数  
3. **接收事件流**：按 SSE 格式解析 `data:` 行，事件类型包括 `message_start`、`content_block_delta`、`tool_use`、`message_stop` 等  
4. **中断处理**：客户端可随时发送 `{"type": "input_interrupt"}` 帧终止当前响应（仅 WebSocket 支持）  

完整示例与错误码说明请参考 [快速开始](../../raw/model-api-reference/realtime-api-user-guide.md)。

## 限制和注意事项

- **连接时长**：单次 WebSocket 连接最长 300 秒，超时后服务端主动关闭  
- **并发限制**：免费版账户默认 5 路并发；企业版按配额配置，详情见控制台  
- **输入长度**：总上下文（含 system [prompt](../guides/prompt.md) + messages + tools）token 数 ≤ 32768；超出将拒绝连接并返回 `413 Payload Too Large`  
- **音频输入**：仅 `qwen2-audio` 支持，采样率必须为 16kHz，位深 16bit，单次音频帧 ≤ 64KB  
- **重连策略**：客户端需实现指数退避重连（建议初始间隔 1s，最大 30s），避免因网络抖动频繁建连  

所有协议细节、事件定义及状态码均以 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 为准。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


