# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种实时响应机制，允许模型服务将生成结果以增量方式分块推送至客户端，而非等待全部内容完成后再一次性返回。该机制显著降低端到端延迟，提升用户交互体验，尤其适用于长文本生成、实时对话、工具调用中间反馈等场景。

## 在百炼平台的不同场景中，这个概念如何使用

- **Qwen 文本生成 API**：所有接口（OpenAI 兼容 Chat Completions、Anthropic 兼容 Messages、DashScope 原生）均支持流式响应。启用后，服务按 token 或语义单元（如搜索摘要、代码执行结果）逐帧推送 `delta.content`，最终以 `finish_reason` 帧结束。`OpenAI 兼容 Responses` 接口的流式响应可能包含工具调用中间结果（如联网搜索摘要），而 DashScope 接口仅流式返回最终生成文本。

- **Model Experience 统一调用层**：`/v1/models/{model}/invoke` 端点支持 `stream=true`，仅对文本生成与语音生成类模型生效（视觉/向量模型不支持）。响应为标准 Server-Sent Events（SSE）格式，每帧含 `data:` 字段，解析后可获取 `delta`（增量内容）或 `finish_reason`（终止原因）。

- **Application Call（智能体/工作流调用）**：  
  - DashScope 协议需在请求 Header 中显式设置 `X-DashScope-SSE: enable`；  
  - OpenAI 兼容 Responses 协议则直接在 JSON 请求体中传 `"stream": true`；  
  启用后，智能体执行过程中的思考链（`enable_thinking=true`）、工具调用步骤、RAG 检索片段等均可实时流式透出，便于前端实现“打字机”效果或分阶段 UI 渲染。

- **Framework 集成（LlamaIndex / Spring AI Alibaba）**：  
  - LlamaIndex 的 `stream_chat()` 方法原生封装流式逻辑，返回 `StreamingChatResponse` 迭代器；  
  - Spring AI Alibaba 的 `ChatClient` 支持 `Mono<ChatResponse>` 异步流式消费，需配合 `Flux` 或 `collectList()` 处理多帧数据。  
  框架层自动处理 SSE 解析、重连与错误恢复，开发者只需关注 `delta.content` 的累积与渲染。

- **Flow Agent API（应用调用接口）**：应用调用类接口（非组件管理类）同样支持流式响应，行为与 `Application Call` 一致，即底层智能体执行过程可分块返回，适用于需实时感知执行进度的运维监控或低延迟客服场景。

## 关键参数和配置

| 参数/配置项 | 位置 | 类型 | 说明 |
|-------------|------|------|------|
| `stream` | 请求体（JSON） | `boolean` | [OpenAI 兼容接口](openai-compatible-interface.md)（Responses、Chat Completions）及 Model Experience 的必设开关，默认 `false`。设为 `true` 即启用流式。 |
| `X-DashScope-SSE` | 请求 Header | `string` | DashScope 原生协议（含 Application Call、Flow Agent 应用调用）的启用标识，值必须为 `enable`。仅此 Header 生效，`stream` 字段在 DashScope 请求体中被忽略。 |
| `Accept` | 请求 Header | `string` | 建议显式设置为 `text/event-stream`，确保服务端返回标准 SSE 格式。 |
| `X-DashScope-WorkSpace` | 请求 Header | `string` | 若应用部署在子业务空间，流式调用时仍需携带该 Header，否则可能因鉴权失败中断流。 |

> ⚠️ 注意：流式响应不改变计费逻辑——仍按实际生成的总 token 数计费；且所有流式接口均要求客户端具备 SSE 解析能力（如 `EventSource`、`fetch + ReadableStream` 或 SDK 封装）。

## 面向开发者，简洁实用

- **快速启用**：只需加一个参数（`"stream": true`）或一个 Header（`X-DashScope-SSE: enable`），无需修改模型逻辑或重写业务流程。  
- **安全兜底**：流式响应始终以 `finish_reason` 帧终结（如 `"stop"`、`"length"`、`"content_filter"`），务必监听该帧以判断生成是否完成或异常终止。  
- **错误处理**：网络中断时，建议实现重连逻辑（如指数退避 + `last_event_id` 恢复），SDK（如 `dashscope` Python v1.20.0+）已内置基础重试。  
- **性能提示**：流式不降低单 token 生成延迟，但显著改善首字节时间（TTFB）和用户感知延迟；若追求极致吞吐，非流式批量调用仍更高效。  
- **调试建议**：使用 `curl -N` 或 Postman 的 SSE 模式直接测试流式接口，观察原始 `data:` 帧结构，避免过早依赖框架封装掩盖细节。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [frameworks](../api/frameworks.md)
- [flow agent api](../api/flow-agent-api.md)
- [model experience](../guides/model-experience.md)
- [application call](../api/application-call.md)


