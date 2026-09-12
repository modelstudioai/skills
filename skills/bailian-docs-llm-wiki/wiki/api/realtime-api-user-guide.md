# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式响应的模型调用接口，适用于语音识别、实时对话、流式生成等对时延敏感的场景。它基于 WebSocket 协议实现双向通信，支持服务端逐 token 推送响应，并允许客户端在流中动态中断或插入控制指令。该接口与标准 RESTful `/v1/chat/completions` 在语义和参数设计上保持高度一致，但协议层和生命周期管理有显著差异。

## 支持的模型/功能

当前 Realtime API 支持以下模型（以 `model_id` 形式指定）：
- `qwen-max`, `qwen-plus`, `qwen-turbo`（通用文本生成）
- `qwen-audio`（语音转文本，需配合音频帧流）
- `qwen-vl`（[多模态](../concepts/multi-modal.md)理解，需传入 base64 编码图像）

> **注意**：`qwen2.5-72b` 等部分大模型虽在 [Realtime API (raw/model-api-reference/realtime-api-user-guide.md)](../../raw/model-api-reference/realtime-api-user-guide.md) 的旧版文档中被列为“实验性支持”，但自 v2024.08.15 起已正式移除；实际可用模型请以控制台「API 调用」页的下拉列表为准。

不支持的功能包括：[函数调用](../concepts/function-calling.md)（function calling）、并行 tool use、response_format 为 json_schema 的结构化输出（JSON 模式仅限非流式 REST 接口）。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型 ID，如 `qwen-turbo`；必须与 Realtime API 兼容模型列表匹配 |
| `messages` | array | 是 | 消息数组，格式同 OpenAI；首条 `user` 消息可含 `audio` 或 `image_url` 字段（视模型而定） |
| `stream` | boolean | 是 | 必须为 `true`；设为 `false` 将返回 400 错误 |
| `max_tokens` | integer | 否 | 最大生成 token 数，默认 2048，硬上限为 8192 |
| `temperature` | number | 否 | 采样温度，范围 [0.0, 2.0]，默认 0.8 |

所有参数均需在 WebSocket 连接建立后的 `session.create` 帧中以 JSON 格式发送。更多字段定义详见 [Realtime API (raw/model-api-reference/realtime-api-user-guide.md)](../../raw/model-api-reference/realtime-api-user-guide.md)。

## 使用方式

1. **建立 WebSocket 连接**：  
   请求 URL 为 `wss://dashscope.aliyuncs.com/realtime/v1/<model_id>`（例如 `wss://dashscope.aliyuncs.com/realtime/v1/qwen-turbo`），需携带 `Authorization: Bearer <api_key>` 和 `X-DashScope-Date` 时间戳头。

2. **发送初始化帧**：  
   连接成功后，立即发送 `session.create` 控制帧，包含 `model`、`messages` 等参数。

3. **接收响应帧**：  
   服务端按 token 流式返回 `content.delta`、`content.done`、`error` 等事件帧；客户端应监听 `content.delta` 并拼接完整响应。

4. **终止会话（可选）**：  
   发送 `session.cancel` 帧可主动中断生成；连接关闭前建议发送 `session.close`。

详细交互流程与帧格式示例见 [快速开始](https://help.aliyun.com/zh/model-studio/realtime-api-quick-start-guide)，其内容与 [Realtime API (raw/model-api-reference/realtime-api-user-guide.md)](../../raw/model-api-reference/realtime-api-user-guide.md) 中的协议规范完全一致。

## 限制和注意事项

- 单连接最大持续时间：300 秒（含握手与空闲期），超时将自动断连；
- 单次会话最大输入 tokens：16384（含 system message 和历史上下文）；
- 音频流要求：`qwen-audio` 仅接受 16kHz 单声道 PCM 数据，每帧 ≤ 4096 字节，且必须在 `session.create` 后 5 秒内开始推送；
- 不支持跨连接复用 session ID；每次新会话均为独立上下文；
- 客户端 SDK（如 AOQ）已封装重连、心跳、帧序列校验逻辑，推荐优先使用 —— 参考 [AOQ客户端SDK](https://help.aliyun.com/zh/model-studio/realtime-api-aoq-api) 文档。

> **注意**：原始文档中提及的 “支持 HTTP long-polling 回退机制” 已于 2024 年 Q2 下线；Realtime API 当前**仅支持 WebSocket**，任何关于 HTTP 轮询的描述均属过时信息。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)



