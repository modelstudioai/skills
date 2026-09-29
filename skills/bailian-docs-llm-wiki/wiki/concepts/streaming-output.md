# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种响应模式，允许模型推理结果以增量方式（如 token、事件或数据块）实时返回，而非等待整个响应生成完毕后一次性返回。该机制显著降低端到端延迟，提升用户交互体验，并支持前端实现打字机效果、实时思考链展示、语音合成驱动等动态场景。

## 在百炼平台的不同场景中，这个概念如何使用

- **Managed Agents API**：通过 `stream=true` 参数启用 Server-Sent Events（SSE）流式响应，服务端按执行阶段推送 `event: step`（单步工具调用/推理）、`event: final_output`（最终结果）等结构化事件，适用于需监控 Agent 执行过程的长任务。
- **Application Call（应用调用）**：在 DashScope 原生或 OpenAI 兼容 Responses API 中设置 `stream=true`，返回逐 token 的文本流；配合 `incremental_output=true` 可进一步优化多轮上下文下的增量渲染逻辑。
- **Qwen 模型 API**：所有接口（OpenAI Chat/Responses、Anthropic Messages、DashScope 原生）均支持 `stream=true`，返回标准 SSE 格式（`data: {...}`）或 JSON Lines（`{"delta": {"content": "x"}}`），适用于通用文本生成、代码补全等低延迟需求场景。
- **Realtime API 与 Omni Realtime API**：基于 WebSocket 的原生流式协议，不依赖 HTTP 流，而是以事件（如 `output_text_delta`、`transcript`、`tts_audio`）形式实时双向传输中间结果，专为语音/音视频实时交互设计，支持毫秒级响应和用户动态干预。

> ⚠️ 注意：`stream=true` 在异步后台任务（如 `background=true`）中不可用；流式模式下不返回完整 JSON 结构体，需按事件类型解析响应流。

## 关键参数和配置

| 参数 | 类型 | 默认值 | 说明 | 适用场景 |
|------|------|--------|------|----------|
| `stream` | boolean | `false` | 启用流式响应。设为 `true` 后，HTTP 接口返回 `text/event-stream`，WebSocket 接口启用事件推送。 | 所有 HTTP API（Managed Agents、Application Call、Qwen API） |
| `stream_options.intermediate_results` | boolean | `true` | 控制是否返回中间 token（仅 Realtime API）。设为 `false` 时仅返回最终结果。 | Realtime API |
| `incremental_output` | boolean | `false` | 优化流式内容分片策略，确保多轮对话中每段输出语义完整（如避免截断句子）。推荐与 `stream=true` 同时启用。 | Application Call（Responses API） |

- **HTTP 流式响应头**：`Content-Type: text/event-stream; charset=utf-8`，建议客户端设置超时容忍（如 30s+）并处理连接中断重试。
- **WebSocket 流式要求**：必须维持长连接，服务端按事件类型（`type` 字段）推送结构化消息，客户端需注册对应事件处理器（如监听 `response_text` 或 `tts_audio`）。
- **错误处理**：流式过程中若发生错误，HTTP 流会发送 `event: error`，WebSocket 会推送 `type: "error"` 事件，均携带 `code` 和 `message` 字段，**不应忽略中间错误直接等待结束**。

## 面向开发者，简洁实用

- ✅ **优先启用流式**：只要前端支持（现代浏览器、SDK 或移动端），所有生成类请求都应默认开启 `stream=true`，尤其对 >1s 响应的场景。
- ✅ **解析要健壮**：HTTP 流需按行分割、识别 `data:` 前缀；WebSocket 消息需校验 `type` 字段再处理 payload，避免因字段缺失崩溃。
- ✅ **结合业务做节流**：对打字机效果，可聚合连续 `delta.content` 直到遇到标点或空格再渲染；对语音合成，直接消费 `tts_audio` 二进制流并喂入播放器。
- ❌ **勿混用同步与流式逻辑**：流式响应无 `200 OK` 后的完整 JSON body，不要尝试 `JSON.parse()` 整个响应体。
- ❌ **勿在流式中依赖 `max_tokens` 截断**：流式输出长度由模型自主控制，`max_tokens` 仅作上限提示，实际输出可能提前终止（如遇到 stop token）。

流式输出不是“高级功能”，而是百炼平台面向生产环境的默认交互范式。从第一个 token 开始交付价值，才是 AI 应用体验的起点。

## 关联主题页

- [managed agents api](../api/managed-agents-api.md)
- [application call](../api/application-call.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)


