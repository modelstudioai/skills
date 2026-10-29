# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种实时响应机制，服务端在模型推理过程中将结果分块、渐进式地返回给客户端，而非等待完整响应生成后再一次性返回。这种方式显著降低端到端延迟，提升交互自然度，是构建低延迟语音助手、实时知识问答、长文本生成等体验的核心能力。

## 在百炼平台的不同场景中，这个概念如何使用

流式输出在百炼平台中并非单一接口特性，而是贯穿多类服务的通用交互范式，具体体现为以下三种主流形态：

- **WebSocket 实时流（Realtime & Omni-Realtime API）**：面向语音/多模态实时交互场景。客户端通过 WebSocket 长连接与服务端建立双向通道，服务端以结构化事件（如 `response.text.delta`、`response.audio.delta`、`response.content_part.added`）持续推送增量内容。适用于智能客服、会议实时转写、语音交互终端等毫秒级响应要求的场景。

- **SSE 流（Server-Sent Events，Knowledge Base 与 Application Call）**：面向文本问答与智能体调用场景。当请求中启用 `stream=true`，服务端返回 `Content-Type: text/event-stream` 响应，按 SSE 协议推送 `data:` 行格式的 JSON 片段（如 `{"type":"content","delta":"你好"}`）。适用于 RAG 知识库问答、工作流应用调用等需快速呈现首字、支持前端逐字渲染的场景。

- **原生 HTTP 流（Qwen API DashScope 协议）**：部分 DashScope 原生接口（如 `text-generation`）支持 `X-DashScope-SSE: enable` 请求头，返回标准 SSE 流；而 OpenAI 兼容协议（Chat/Responses）则通过 `stream=true` 参数触发相同语义的流式响应（兼容 OpenAI 的 `data:` 格式），便于生态平滑迁移。

> ⚠️ 注意：流式能力需客户端主动启用且服务端模型/接口明确支持——并非所有模型或所有调用路径默认开启流式。例如 Qwen-Audio 不支持 OpenAI 兼容协议，其流式必须通过 DashScope 原生协议或 Omni-Realtime API 实现。

## 关键参数和配置

| 参数名 | 所属场景 | 类型 | 说明 | 推荐值 |
|--------|----------|------|------|--------|
| `stream` | Knowledge Base (`/chat`)、Application Call（OpenAI Responses）、Qwen API（Chat/Responses） | `boolean` | 启用流式响应的开关 | `true` |
| `X-DashScope-SSE` | Application Call（DashScope 协议）、Qwen API（DashScope 协议） | Header | 显式声明启用 SSE 流式传输 | `enable` |
| `incremental_output` | Application Call（DashScope 协议） | `boolean` | 控制流式内容是否为增量 delta（`true`）还是全量追加（`false`） | `true`（推荐） |
| `flow_stream_mode` | 工作流应用（Flow Agent） | `string` | 工作流专用流式格式，影响事件结构与节点粒度 | `message_format_plus`（推荐） |
| WebSocket 连接参数 | Realtime / Omni-Realtime API | Query String | `model`、`api_key` 必填；`sample_rate` 影响音频处理精度 | `model=qwen-audio-realtime-v1`, `api_key=...` |

> ✅ 提示：  
> - Realtime/Omni-Realtime API 中，流式是**默认行为**，无需额外开关，但需正确监听服务端事件（如 `response.text.delta`）并拼接；  
> - Knowledge Base 和 Application Call 中，`stream=true` 是**显式必需参数**，否则返回同步 JSON；  
> - 所有流式响应均需客户端实现事件解析与缓冲管理（如按 `\n\n` 分割 SSE 消息，JSON.parse `data:` 后内容）。

## 面向开发者，简洁实用

- **不要假设首包即完整**：流式响应可能首包为空或仅含元数据（如 `session.created` 或 `event: message_start`），请始终监听后续 `delta` 或 `content_part.added` 事件。
- **及时处理中断**：WebSocket 可能断连，HTTP 流可能超时；务必实现重连逻辑（Realtime API 推荐使用 AOQ SDK 自动重连）与错误降级（如 fallback 到非流式请求）。
- **注意字符编码与分块边界**：SSE 流中 `data:` 行末尾需换行符；WebSocket 事件 payload 为 UTF-8 JSON，避免二进制混淆；音频流（PCM）需按 `sample_rate` 和位深对齐字节边界。
- **性能优化建议**：  
> • Realtime API：音频输入帧 ≤20ms（16kHz 下约 320 字节），避免大帧导致 ASR/VAD 延迟；  
> • Knowledge Base：启用 `stream=true` 时，`top_k` 检索不影响流式生成，但过大的 `top_k`（如 >20）会增加检索耗时，拖慢首字延迟；  
> • Application Call：若需插件参数透传，`biz_params` 应在首次请求中完整传入，流式过程中不可动态变更。

流式输出不是“锦上添花”，而是构建现代 AI 交互体验的基础设施。从第一声语音合成、第一个思考符号、到首句知识回答——它让 AI 的“思考”真正可见、可感、可中断、可交互。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [knowledge base](../guides/knowledge-base.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [bailian application calling](../guides/bailian-application-calling.md)


