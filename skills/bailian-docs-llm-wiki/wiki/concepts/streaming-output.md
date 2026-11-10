# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种实时响应机制，允许模型服务将生成结果以增量方式分块返回，而非等待完整响应后一次性输出。该机制显著降低端到端延迟，提升用户交互体验，尤其适用于对话界面、实时语音处理、长文本生成等对响应速度敏感的场景。

## 在百炼平台的不同场景中如何使用

- **标准文本生成 API（Qwen 系列）**：  
  通过 `stream=true` 参数启用流式响应。[OpenAI 兼容接口](openai-compatible-interface.md)返回 `delta.content` 字段；DashScope 原生接口返回 `output.text` 的增量片段；Anthropic 兼容接口返回 `content` 数组中的 `text` delta。所有接口均需客户端按事件流（EventStream）解析 `data:` 行。

- **框架集成（Frameworks）**：  
  - LlamaIndex：在 `QwenModel` 初始化或调用时显式设置 `stream=True`（默认为 `False`），配合 `ChatEngine.stream_chat()` 使用；注意其 `AsyncLLM` 尚不支持异步流式。  
  - Spring AI Alibaba：`AlibabaAIClient` 默认启用流式（`stream=true`），`ChatClient` 调用自动返回 `Flux<ChatResponse>`，可直接订阅 token 流。

- **Realtime API（WebSocket 场景）**：  
  所有 Realtime 接口（ASR/TTS/音频对话/多模态）天然基于流式设计。服务端通过 WebSocket 消息持续推送 `response.text.delta`、`response.audio.delta` 或 `input.intermediate` 等事件，无需额外参数开启，但可通过 `enable_intermediate_results` 控制是否返回中间态（如 ASR 的 partial transcript）。

- **应用层控制（Application Support）**：  
  支持两种流式模式协同使用：  
  - `stream=True`：启用基础流式（逐 token 返回）；  
  - `incremental_output=True`（需与 `stream=True` 同时设置）：仅返回本次新增 token，避免重复回传历史内容，适用于前端需精确控制渲染节奏的场景（如打字机效果）。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 说明 | 默认值 |
|--------|------|------|------|--------|
| `stream` | boolean | 否 | 启用流式响应模式 | `false`（Qwen API / LlamaIndex）；`true`（Spring AI Alibaba） |
| `incremental_output` | boolean | 否 | 启用增量式流式（仅返回新 token），必须与 `stream=true` 共同使用 | `false` |
| `enable_intermediate_results` | boolean | 否 | Realtime API 中启用中间结果流（如 ASR 实时转写片段） | `false` |

> ⚠️ 注意：  
> - `incremental_output` 仅 DashScope 原生接口和部分 Realtime 场景支持，[OpenAI 兼容接口](openai-compatible-interface.md)不识别该参数；  
> - 流式响应下，`max_tokens` 仍生效，达到上限时服务端将发送 `done` 事件并终止流；  
> - 错误发生时（如鉴权失败、超时），服务端会立即推送 `error` 事件，客户端应监听并中断流处理。

## 面向开发者：实用建议

- **解析流式响应**：  
  - HTTP 流式：检查响应头 `Content-Type: text/event-stream`，逐行读取 `data: {...}`，忽略空行和注释行（`:` 开头）；  
  - WebSocket 流式：监听 `message` 事件，解析 JSON 中的 `event` 字段（如 `"response.text.delta"`），提取 `delta` 或 `text` 字段拼接。

- **前端渲染优化**：  
  使用 `incremental_output=true` 可避免重复渲染，结合 `AbortController` 支持用户中断请求；推荐对 `response.text.delta` 做防抖合并（如 50ms 内连续 delta 合并为一次更新），减少 DOM 频繁操作。

- **错误处理**：  
  流式请求失败不会返回 HTTP 2xx，而是直接关闭连接或发送 `error` 事件。务必实现 `onerror` / `onclose` 回调，并记录 `RequestId` 用于问题排查。

- **性能提示**：  
  流式不降低单 token 计算开销，但可显著改善感知延迟。若关注首 token 延迟（Time to First [Token](token.md)），请优先调优 `temperature`（降低至 0.1–0.3）、禁用非必要插件（如 `enable_web_search=false`），并选用 `qwen-turbo` 等轻量模型。

## 关联主题页

- [frameworks](../api/frameworks.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [realtime api directory](../api/realtime-api-directory.md)
- [application support](../guides/application-support.md)


