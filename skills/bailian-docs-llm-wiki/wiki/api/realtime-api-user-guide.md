# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式双向通信接口，适用于语音交互、实时对话、音视频场景下的模型调用。它基于 WebSocket 协议实现，支持服务端主动推送事件（如 `audio_chunk`、`tool_call`、`interrupt`），并允许客户端在会话中动态插入指令或中断。该接口不兼容传统 REST 调用方式，需使用专用 SDK 或原生 WebSocket 客户端接入。

## 支持的模型与功能

当前 Realtime API 仅支持以下模型：`qwen-audio-20241015`、`qwen-vl-20241015` 和 `qwen2-audio-20241101`（详见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)）。所有模型均默认启用音频流式输入/输出、多轮上下文保持、工具调用（Tool Calling）及实时中断响应能力。视觉模型（如 `qwen-vl-20241015`）额外支持帧级图像上传与同步推理，但暂不支持纯文本会话模式——即必须携带 `input.audio` 或 `input.video` 字段，否则连接将被拒绝。

> **注意**：原始文档中 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) 示例使用了已下线的 `qwen-audio-20240715` 模型，实际调用请以 [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-model-connection.md) 中列出的当前可用模型为准。

## 关键参数

建立连接时需在 WebSocket URL 中携带以下必需查询参数：

- `model`: 模型 ID（如 `qwen2-audio-20241101`），必须与 [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-model-connection.md) 所列一致  
- `api_key`: 有效百炼平台 API Key（非 AccessKey）  
- `response_format`: 可选，取值为 `json`（默认）或 `binary`（用于原始 PCM 音频流）  
- `stream`: 固定为 `true`，不可省略  

首次发送的 `session.update` 消息中，`turn_detection` 配置决定语音断句策略；`tools` 数组定义可调用函数，其 schema 必须符合 OpenAI 兼容格式。

## 使用方式

1. 构造 WebSocket 连接 URL：`wss://dashscope.aliyuncs.com/realtime/v1?model={model}&api_key={key}&stream=true`  
2. 发送 `session.update` 初始化会话（含系统提示、工具定义等）  
3. 发送 `input.audio` 或 `input.video` 帧数据（Base64 编码或二进制分片）  
4. 处理服务端返回的 `output.audio`、`response.text.delta`、`tool_use` 等事件  

推荐使用官方 AOQ 客户端 SDK（Python/JS），其自动处理重连、帧编码、事件解析和中断信号转发。SDK 使用方法详见 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)。

## 限制和注意事项

- 单次会话最长持续 300 秒，超时后连接关闭且不自动续期  
- 音频输入采样率必须为 16kHz、单声道、PCM 编码（`int16`），否则触发 `invalid_input_format` 错误  
- 同一 `api_key` 并发连接数上限为 10，超出将返回 `429 Too Many Connections`  
- 不支持 HTTP/2 或 Server-Sent Events（SSE）替代方案；REST 封装层（如 `/v1/realtime/chat`）仅为文档占位，实际不可用  

> **注意**：[概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中提及“支持自定义语音合成音色”，该能力尚未上线，当前所有 `output.audio` 均使用固定 TTS 声音，此描述已过时。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


