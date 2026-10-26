# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式响应的模型调用接口，适用于语音交互、实时对话、多轮上下文增强等场景。它基于 WebSocket 协议实现双向通信，支持增量式 token 返回与客户端主动控制（如中断、暂停）。该接口不兼容传统 REST 同步调用模式，需按事件驱动方式处理。

## 支持的模型与功能

当前 Realtime API 支持以下模型（以 `model` 参数指定）：
- `qwen-max-realtime`、`qwen-plus-realtime`（推荐用于高复杂度实时对话）
- `qwen-turbo-realtime`（轻量级、低延迟场景）

功能包括：流式文本生成、语音输入/输出（需配合 AOQ SDK）、工具调用（function calling）、会话状态保持（session_id 维护）、以及客户端发起的 `interrupt` 和 `pause` 事件。详细能力列表见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，必须为实时专用型号，如 `qwen-plus-realtime`；非实时型号（如 `qwen-plus`）将返回 400 错误 |
| `session_id` | string | 否 | 用于跨请求维持会话上下文；若未提供，服务端自动生成新会话（有效期 30 分钟） |
| `enable_audio` | boolean | 否 | 设为 `true` 时启用音频流传输（需配合 AOQ SDK），默认 `false` |
| `max_tokens` | integer | 否 | 单次响应最大 token 数，范围 1–4096；超过将被截断并触发 `completion_truncated` 事件 |

> **注意**：`temperature` 和 `top_p` 等采样参数在 Realtime API 中**不生效**，模型行为由服务端固定策略控制；此与 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 中“快速开始”章节描述一致，但与旧版 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md) 文档中示例存在矛盾——后者错误展示了 `temperature` 参数传递，应忽略。

## 使用方式

1. 建立 WebSocket 连接：`wss://dashscope.aliyuncs.com/realtime/v1/chat`（需携带 `Authorization: Bearer <api_key>` 头）
2. 发送 `session.create` 事件初始化会话（含 `model`、`session_id` 等）
3. 发送 `user.message` 事件提交用户输入（支持 text 或 audio base64）
4. 监听 `assistant.message.chunk`（流式 token）、`assistant.message.done`（完成）等事件  
完整流程与代码片段参见 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md)。

## 限制和注意事项

- 单连接最大并发请求数：1（Realtime API 不支持复用连接发送多个并行请求）
- 单次 `user.message` 内容长度上限：8192 字符（文本）或 60 秒音频（PCM 16kHz）
- 连接空闲超时：60 秒无事件交互将自动关闭
- 错误重连建议：收到 `connection.closed` 后，应销毁旧连接并新建会话（`session_id` 不可复用）  
更多约束详见 [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-model-connection.md)。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


