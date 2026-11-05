# 流式输出

流式输出（Streaming Output）是指模型服务将响应内容以增量、分块（chunk）的方式持续返回给客户端，而非等待整个响应生成完毕后一次性返回完整结果。这种方式显著降低端到端延迟，提升用户感知的响应实时性，是构建低延迟交互应用（如实时对话、语音助手、长文本生成）的关键能力。

## 在百炼平台的不同场景中如何使用

流式输出在百炼平台中并非单一接口特性，而是贯穿多个调用协议与产品形态的通用能力，具体使用方式因场景而异：

- **Qwen API（模型直调）**：  
  OpenAI 兼容协议下，通过 `stream=true` 参数启用；DashScope 原生协议需额外设置请求头 `X-DashScope-SSE: enable`；Anthropic 兼容协议默认支持流式（`messages` 接口），无需显式开关。所有协议均返回 `text_delta` 类型的 SSE 或 JSONL 响应块，客户端需按序拼接。

- **Application Call（智能体/工作流调用）**：  
  支持同步流式（`stream=true`）与增量流式（`incremental_output=true`）。后者确保每个 chunk 仅包含本次新增内容（不重复前序），适合前端逐字渲染；工作流还支持 `flow_stream_mode=message_format_plus`，可分离工具调用、思考链与最终回复事件。

- **Realtime API（实时音视频流）**：  
  **强制流式**，无非流式选项。通过 WebSocket 二进制帧+JSON 事件帧混合传输，服务端持续推送 `event: "text_delta"`、`event: "audio_chunk"` 等类型帧，客户端需实时解码、缓冲与合成。

- **Omni Realtime API（多模态实时交互）**：  
  同样为强制流式，但支持更细粒度的模态控制：当 `modalities=["text","audio"]` 时，文本与音频 chunk 可并行到达；VAD（语音活动检测）触发的静音间隙会暂停 `text_delta` 输出，保障语义连贯性。

- **Frameworks（框架集成）**：  
  LlamaIndex 和 Spring AI Alibaba 均透传底层流式能力。例如 LlamaIndex 中调用 `llm.stream("...")` 即触发百炼流式请求，返回 `StreamingResponse` 迭代器；Spring AI 的 `chatClient.stream(...)` 同理，开发者无需处理协议细节。

## 关键参数和配置

| 参数 / 配置项 | 所属场景 | 说明 | 示例值 |
|----------------|------------|------|----------|
| `stream` | Qwen API、Application Call、Frameworks | 启用流式响应的布尔开关 | `true` |
| `X-DashScope-SSE: enable` | DashScope 原生协议（Qwen/API/Application） | 必须配合 `stream=true` 使用，否则返回 400 | Header 值 |
| `incremental_output` | Application Call（DashScope 协议） | 控制是否增量输出（`true`：每 chunk 仅新内容；`false`：累计内容） | `true` |
| `flow_stream_mode` | Application Call（工作流） | 工作流专用流式格式，推荐 `message_format_plus`（结构化事件） | `"message_format_plus"` |
| `modalities` | Omni Realtime API | 指定输出模态组合，决定流式内容类型 | `["text","audio"]` |
| `turn_detection.type` | Omni Realtime API | VAD 类型影响 `text_delta` 的分块节奏与停顿行为 | `"semantic_vad"` |

> ⚠️ 注意：  
> - Anthropic 兼容协议中 `stream` 参数无效，流式为默认行为；  
> - Realtime 与 Omni Realtime API **不接受 `stream=false`**，所有调用均为流式；  
> - 流式响应中若含思考链（`thought`）、工具调用（`function_call`）等中间产物，其字段名与结构依协议而异（详见各 API 参考文档）。

## 面向开发者：简洁实用建议

- ✅ **首选增量流式**：对 UI 渲染类应用（如聊天框打字效果），务必启用 `incremental_output=true`（Application Call）或使用框架的 `stream()` 方法，避免重复拼接。
- ✅ **正确处理流式终止**：所有流式响应均以 `event: "done"`（SSE）或 `{"object":"chat.completion.chunk","finish_reason":"stop"}`（OpenAI 兼容）标识结束，**不可依赖空 chunk 或超时判断**。
- ✅ **错误处理需流式感知**：流式过程中可能返回 `event: "error"` 或含 `"error"` 字段的 chunk，客户端应监听并中断当前流，而非等待结束。
- ❌ **避免在流式中修改 session 状态**：`session_id`、`memory_id` 等状态参数应在首次请求时设定，流式过程中服务端不支持动态更新上下文。
- 🛠️ **调试技巧**：使用 `curl -N` 或 Postman 的 SSE 模式直接测试；Realtime/Omni Realtime 建议优先使用 AOQ SDK（自动处理重连、心跳、编码适配）。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [frameworks](../api/frameworks.md)


