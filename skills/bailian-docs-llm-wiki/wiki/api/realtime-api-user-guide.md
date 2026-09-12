# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式响应的模型调用接口，适用于对话交互、实时语音/文本生成等场景。它支持 WebSocket 和 HTTP/2 双协议，提供 token 级别[流式输出](../concepts/streaming-output.md)与事件驱动控制能力。详细设计目标和适用边界请参见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)。

## 支持的模型与功能

- **当前支持模型**：`qwen-max`、`qwen-plus`、`qwen-turbo`（仅限 `stream=true` 模式）、`qwen2-audio`（音频流式输入/输出）  
- **核心功能**：  
  - 完整消息流（`message_start` → `content_block_delta` → `message_stop`）  
  - 中断控制（`interrupt` event）与工具调用（`tool_use` + `tool_result`）  
  - 多模态输入（文本+图像+音频，需对应模型支持）  
  - 会话状态保持（通过 `session_id` 复用上下文，详见 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide.md)）

> **注意**：文档中提及的 `qwen-vl` 已于 v2024.07 起停止维护，实际调用将自动降级为 `qwen-plus`；该行为与 [概述](../../raw/model-api-reference/realtime-api-user-guide.md) 中“支持全量视觉语言模型”的描述存在不一致，请以实际 API 响应为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型 ID，必须为实时 API 明确支持的型号（见上节） |
| `messages` | array | 是 | 非空消息数组，首条 `role=system` 可选，后续 `user`/`assistant` 交替 |
| `stream` | boolean | 是 | 必须为 `true`；`false` 将返回 400 错误 |
| `temperature` | number | 否 | 范围 `[0.0, 2.0]`，默认 `0.8`；注意该值对[流式输出](../concepts/streaming-output.md)稳定性影响显著 |
| `max_tokens` | integer | 否 | 单次响应最大 token 数，硬限制（含 [prompt](../guides/prompt.md)），默认 `4096` |

## 使用方式

1. **建立连接**：使用 `wss://dashscope.aliyuncs.com/realtime/v1/chat`（公网）或内网 endpoint  
2. **发送初始化帧**：JSON 格式 `{"type": "session_update", "session": {...}}` + `{"type": "input", "content": [...]}`  
3. **接收事件流**：按 `content_block_delta` 累积拼接 `text` 字段，监听 `message_stop` 判断完成  
4. **调试建议**：优先使用官方 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide.md)，避免手动处理二进制帧与心跳逻辑  

## 限制和注意事项

- 单连接最长存活 30 分钟，超时后需重连并重建 session  
- 每秒最多 5 个并发连接（按 AccessKey 统计），超出返回 `429 Too Many Requests`  
- 图像输入仅支持 base64 编码（`data:image/png;base64,...`），不支持 URL 或 multipart  
- 不支持 `response_format`（如 JSON mode）与 `parallel_tool_calls`，相关字段将被忽略  
- 所有错误均通过 `error` 事件返回，**不会**混入 `content_block_delta` 流中  

> **注意**：[快速开始](../../raw/model-api-reference/realtime-api-user-guide.md) 文档中给出的 Python 示例未处理 `tool_use` 的异步回调，实际集成时需自行实现 `tool_result` 插入逻辑，否则会导致会话卡死。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


