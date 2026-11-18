# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种实时响应机制，允许模型在生成过程中逐 token（或逐 chunk）向客户端推送结果，而非等待全部内容生成完毕后一次性返回。该机制显著降低用户感知延迟，提升交互体验，尤其适用于对话界面、代码补全、语音合成等对实时性敏感的场景。

## 在百炼平台的不同场景中如何使用

- **Model Experience 统一调用接口**（`/v1/models/{model_id}/invoke`）：通过请求体中设置 `"stream": true` 启用；响应为 `text/event-stream` 格式，每条 `data:` 行包含一个 JSON 对象（如 `{"output": {"text": "Hello"}, "usage": {...}}`），需按 Server-Sent Events（SSE）协议解析。
- **Qwen API（OpenAI 兼容 / Anthropic 兼容 / DashScope 原生）**：各协议均支持流式，参数名统一为 `stream=true`（OpenAI/Anthropic）或 `stream=True`（DashScope SDK）。例如 [OpenAI 兼容接口](openai-compatible-interface.md) `/v1/chat/completions` 中启用后，返回 `choices[0].delta.content` 增量字段。
- **Application Support（Agent/RAG 应用）**：支持 `stream=True` 与 `incremental_output=True` 双模式：前者返回完整历史片段（含已生成内容重发），后者仅返回本次新增 token，更适合前端增量渲染与 Markdown 实时高亮。
- **Framework 集成（LlamaIndex / Spring AI Alibaba）**：LlamaIndex 的 `QwenLLM` 支持 `stream=True` 参数；Spring AI Alibaba 的 `StreamingChatClient` 自动适配流式语义，调用 `stream()` 方法即可获取 `Flux<ChatResponse>`。
- **多模态限制注意**：文本与语音类模型（如 `qwen2.5-7b-chat`, `qwen-audio`）普遍支持流式；但部分全模态模型（如 `wanx-vl-3.0`）暂不支持 `stream: true`，启用将返回 `400 Unsupported Operation` 错误。

## 关键参数和配置

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `stream` | boolean | `false` | 全局开关，启用后返回 SSE 流；必须显式设为 `true` 才生效。所有协议与 SDK 均识别此字段。 |
| `incremental_output` | boolean | `false` | 仅 Application Support 场景有效；设为 `true` 时，流式响应中 `output.text` 仅含本次新增内容（非累计），避免前端重复渲染。 |
| `timeout`（客户端） | duration | SDK 默认 30s | 流式请求易受网络波动影响，建议显式设置超时（如 `60s`），防止连接长期挂起。 |
| `max_retries`（SDK） | integer | 2（指数退避） | 流式连接中断时，SDK 可自动重试（需配合 `stream` 使用）；生产环境建议保留默认值。 |

> ⚠️ 注意：流式响应不支持 `system` 消息重试缓存；若使用 `previous_response_id` 或会话缓存，需确保上游逻辑兼容增量更新语义。

## 面向开发者：简洁实用提示

- ✅ **必做**：前端解析流式响应时，务必按 SSE 规范处理 `data:` 行，忽略 `event:`、`id:` 等可选字段；推荐使用成熟库（如 `EventSource` 浏览器原生 API 或 `fetch-event-source`）。
- ✅ **必做**：流式调用需保持 HTTP 连接活跃，服务端默认超时 60 秒；若生成耗时长（如长文摘要），请增大客户端 `timeout` 并处理 `AbortError`。
- ❌ **禁止**：不要在流式响应中依赖 `usage.total_tokens` 的实时准确性——该字段仅在最终 `done` 事件中完整准确，中间 chunk 的 `usage` 为当前累计估算值。
- 💡 **技巧**：结合 `incremental_output=true` 与前端防抖（debounce），可实现平滑的打字机效果；对 Markdown 内容，建议每次只对新增片段做语法高亮，而非全量重渲染。
- 📦 **调试**：使用 `curl -N` 或 Postman 的 Stream 开关可快速验证流式行为；SDK 日志开启 `DEBUG` 级别可查看原始 SSE 数据流。

## 关联主题页

- [preparations](../api/preparations.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [model experience](../guides/model-experience.md)
- [application support](../guides/application-support.md)
- [frameworks](../api/frameworks.md)


