# 流式输出

流式输出（Streaming Output）是百炼平台中一种实时、增量返回模型响应内容的能力，允许客户端在模型生成过程中持续接收部分结果（如 token、文本片段、音频帧或思考步骤），而非等待整个响应完成后再一次性返回。该机制显著降低端到端延迟，提升用户体验，并为前端实现打字机效果、实时语音合成、渐进式思考链展示等交互场景提供底层支持。

## 在百炼平台的不同场景中，这个概念如何使用

流式输出在百炼平台中并非单一功能，而是贯穿多个 API 层级和产品形态的通用能力，其启用方式与行为表现因场景而异：

- **Application Call（智能体/工作流调用）**：  
  通过 `stream=true` 参数开启流式模式。此时响应以 Server-Sent Events（SSE）格式逐块返回；若为工作流应用，还需配合 `flow_stream_mode=message_format_plus`（推荐）并在控制台对应节点开启“流式输出”开关，才能确保各节点输出被正确组装并流式下发。

- **Qwen 系列模型直调（DashScope / OpenAI 兼容 / Anthropic 兼容协议）**：  
  统一使用 `stream=true` 参数。DashScope 协议下可进一步通过 `incremental_output=true` 控制是否以 delta 增量方式返回（`true` 时每 chunk 仅含新增 token；`false` 时为全量追加，需客户端自行拼接）；OpenAI 兼容协议中 `stream=true` 即默认 delta 模式，符合标准 OpenAI Streaming 格式。

- **Omni Realtime API（多模态实时交互）**：  
  基于 WebSocket 双向流，天然支持流式。服务端主动推送 `output.text.delta`、`output.audio.delta`、`output.vision.delta` 等事件，无需显式传参开启——只要建立连接即默认启用全链路流式处理（ASR→LLM→TTS）。

- **Realtime API（统一实时接入层）**：  
  同样默认流式，不依赖 `stream` 参数。具体行为由所选协议（AOQ/WebRTC/WebSocket）和 `session.modalities` 配置决定。例如设置 `["text", "audio"]` 后，服务端将并行推送文本增量和音频 PCM 片段。

> ⚠️ 注意：`stream=true` 在 Responses API 中与 `background=true` 互斥——后台异步任务不支持流式；`flow_stream_mode` 仅对工作流应用生效，且与 `incremental_output` 作用域不同，不可混用。

## 关键参数和配置

| 参数 | 所属场景 | 类型 | 说明 | 推荐值 |
|------|----------|------|------|--------|
| `stream` | 全部同步 API（Application Call / Qwen / Omni Realtime 初始化） | `boolean` | 启用流式响应的核心开关 | `true` |
| `incremental_output` | DashScope 协议专属（Application Call / Qwen 直调） | `boolean` | 控制流式 chunk 内容格式：`true` → delta（仅新增内容）；`false` → full（全量追加） | `true`（推荐，减少带宽与解析开销） |
| `flow_stream_mode` | Application Call 中的工作流应用专用 | `string` | 工作流节点级流式策略：`message_format_plus`（推荐）、`message_format`、`full_thoughts`（不推荐） | `"message_format_plus"` |
| `enable_interim_results` | Omni Realtime API | `boolean` | 是否推送 ASR 中间识别结果（非最终文本） | `false`（按需开启，用于实时字幕等场景） |

- **HTTP Header 补充**：所有流式请求建议设置 `Accept: text/event-stream`（SSE）或使用 WebSocket 协议，避免被网关缓存或截断。
- **超时配置**：流式请求需延长 `read_timeout`（如设为 300 秒），防止连接因长时间无数据而中断。

## 面向开发者，简洁实用

- ✅ **必做**：始终检查响应 Content-Type 是否为 `text/event-stream`（SSE）或确认 WebSocket 连接已就绪；使用官方 SDK（如 `dashscope` Python SDK 的 `Stream` 迭代器）自动处理 chunk 解析与重连。
- ✅ **推荐**：前端优先采用 `incremental_output=true` + delta 解析，避免手动拼接；对工作流应用，务必在控制台节点配置页勾选“启用流式输出”。
- ❌ **避免**：在 `background=true`（异步任务）中设置 `stream=true`（将被忽略）；混用 `flow_stream_mode` 和 `incremental_output` 控制同一请求；在未启用流式开关的节点上调用工作流流式接口（返回空或错误）。
- 🛠️ **调试技巧**：用 `curl -N` 或浏览器 DevTools 的 Network → EventStream 查看原始 SSE 流；WebSocket 场景使用 `wscat` 工具快速验证连接与事件收发。

## 关联主题页

- [application call](../api/application-call.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [more about models](../api/more-about-models.md)


