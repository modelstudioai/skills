# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种增量式响应机制，允许模型在推理过程中将生成结果分块、实时推送至客户端，而非等待全部内容完成后再一次性返回。该机制显著降低端到端延迟，提升用户交互体验，尤其适用于长文本生成、语音合成、实时对话等对响应速度敏感的场景。

## 在百炼平台的不同场景中，这个概念如何使用

- **RAG API**：通过 `stream=true` 参数启用 SSE（Server-Sent Events）流式响应，服务端按 token 或语义片段逐批返回 `answer` 的增量内容（如 `{"delta": "百炼平台支持..."}`），便于前端实现打字机效果或提前渲染引用切片；适用于知识库问答中答案较长、需快速首屏反馈的场景。

- **Realtime API（WebSocket 协议）**：原生基于流式设计，所有输出均为事件驱动的增量消息（如 `text_delta`、`audio_delta`）。客户端可实时接收文本片段、音频 PCM 数据块，并支持在任意时刻发送 `interrupt` 事件中断当前生成，实现真正的双向实时交互。

- **Qwen API（OpenAI/DashScope 兼容协议）**：通过 `stream=true` 启用 SSE 流式响应，返回符合 OpenAI 格式的 `chunk` 对象（含 `response.output_text.delta` 字段），兼容主流 SDK（如 `openai-python`）的流式处理逻辑，适用于通用文本生成、多轮对话等场景。

- **Omni Realtime API（WebSocket + AOQ）**：流式能力深度集成于会话生命周期中，`session.updated` 后持续推送 `output` 事件，包含 `text`、`audio` 等多模态增量数据；支持细粒度控制（如 `semantic_vad` 触发的流式分段），是语音助手、实时会议摘要等低延迟应用的基础支撑。

- **应用组件 API（RESTful）**：通过 `parameters.stream=true` 开启流式模式，返回标准 SSE 格式响应，每条事件携带 `delta` 字段；注意该模式下不支持 `system` 消息，且请求必须包含至少一条 `user` 消息，适合嵌入自定义应用中构建轻量级流式 UI。

## 关键参数和配置

- **通用开关参数**：  
  - `stream`（布尔值）：所有支持流式的 API 均通过此参数控制是否启用。默认为 `false`；设为 `true` 后，响应头 `Content-Type` 变为 `text/event-stream`，响应体为 SSE 格式（如 `data: {"delta":"hello"}\n\n`）。

- **协议与传输要求**：  
  - RESTful 类 API（RAG、Qwen、应用组件）：使用 HTTP/1.1，需客户端正确处理 SSE 解析（自动重连、event/id 字段解析等）；推荐使用百炼官方 SDK 或成熟 SSE 客户端库。  
  - WebSocket 类 API（Realtime、Omni Realtime）：无需额外参数，流式为默认行为；客户端需监听 `output` 事件并按 `delta` / `final_text` / `audio_delta` 等字段区分内容类型。

- **注意事项**：  
  - 流式响应不改变模型推理逻辑，仅影响输出传输方式；`max_tokens`、`temperature` 等生成参数仍生效。  
  - 流式模式下，部分功能受限（如 RAG API 中 `system` 消息不可用；应用组件 API 中 `system` 消息被忽略）。  
  - 错误仍通过标准 HTTP 状态码（如 `429`）或 WebSocket 错误事件抛出，流式本身不掩盖业务异常。

面向开发者，请优先使用百炼官方 SDK（如 `dashscope` Python SDK、AOQ 客户端库），它们已封装流式连接管理、事件解析、重试与超时逻辑，避免手动处理底层协议细节。

## 关联主题页

- [rag api](../api/rag-api.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [application component api reference](../api/application-component-api-reference.md)


