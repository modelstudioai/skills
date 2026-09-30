# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式双向通信接口，适用于语音交互、实时对话、音视频场景下的模型调用。它基于 WebSocket 协议实现，支持服务端主动推送事件（如 `audio_chunk`、`tool_call`、`interrupt`），并允许客户端在会话中动态插入指令或中断。该接口不兼容传统 REST 调用方式，需使用专用 SDK 或原生 WebSocket 客户端接入。

## 支持的模型与功能

当前 Realtime API 仅支持 `qwen-audio-realtime-v1` 和 `qwen2.5-audio-realtime-v1` 两类音频实时模型，暂不支持纯文本模型或视觉模型。核心功能包括：实时音频流输入/输出、ASR+LLM+TTS 端到端协同、工具调用（`tool_use`）、会话中断与恢复、以及客户端上下文注入（如 `update_context` 事件）。详细能力说明见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 的子章节。

> **注意**：原始文档中 [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-model-connection.md) 提到“支持 `qwen-vl-realtime`”，但该模型已在 v2.3.0 版本中下线，实际调用将返回 `404 model_not_found`。请以 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md) 文档中声明的支持列表为准。

## 关键参数

建立连接时必须提供以下参数（均通过 WebSocket URL 查询参数传递）：
- `model`: 模型 ID（必填，如 `qwen-audio-realtime-v1`）
- `api_key`: 百炼平台 API Key（必填，需具备 `realtime_api` 权限）
- `voice`: 合成语音类型（可选，如 `zhitian_emo`，默认 `qwen_tts`）
- `temperature`: 采样温度（0.0–1.0，默认 0.7）

所有事件载荷（如 `input_audio`、`response_text_delta`）均采用 JSON 格式，字段命名严格区分大小写。完整事件定义参见 [概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。

## 使用方式

1. **建立连接**：向 `wss://dashscope.aliyuncs.com/realtime/v1/audio` 发起 WebSocket 连接，附带上述查询参数；  
2. **初始化会话**：发送 `session_update` 事件配置系统提示词、工具列表等；  
3. **输入音频**：将 PCM 编码的单声道 16kHz 音频分块（每块 ≤ 200ms）为 `input_audio` 事件发送；  
4. **处理响应**：监听 `response_audio_delta`（二进制 Opus 帧）、`response_text_delta`、`tool_call` 等事件；  
5. **控制流**：通过 `conversation_item_create` 插入文本消息，或 `interrupt` 终止当前响应。

推荐使用官方 AOQ SDK（Python/JS），其自动处理重连、心跳、编解码和事件路由。SDK 使用示例详见 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)。

## 限制和注意事项

- 单连接最大持续时长为 30 分钟，超时后需重建连接；  
- 音频输入需严格满足 `PCM, 16-bit, little-endian, mono, 16kHz` 格式，否则触发 `input_audio_format_error`；  
- 同一 `api_key` 下并发连接数上限为 10，超出将拒绝新连接（HTTP 429）；  
- `session_update` 中设置的 `max_output_tokens` 仅对首次响应生效，后续需通过 `response_content_part_add` 动态调整；  
- 所有音频流事件（`input_audio`, `response_audio_delta`）必须在连接建立后 5 秒内开始发送，否则连接将被服务端静默关闭。

调试建议：启用 `debug: true` 参数（仅限测试环境），并在连接 URL 中添加 `?log_level=debug` 以获取详细握手日志。更多排错指引见 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md)。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


