# 流式输出

流式输出（Streaming Output）是百炼平台中一种低延迟、增量式的数据返回机制，服务端在模型推理过程中边生成边发送结果片段，而非等待全部内容完成后再一次性返回。它适用于对实时性敏感的交互场景（如语音助手、实时会议摘要、长文本生成），可显著降低端到端响应延迟，并支持客户端即时渲染、中断控制与自然停顿。

## 在百炼平台的不同场景中，这个概念如何使用

流式输出在百炼平台中以三种协议形态统一支持，适配不同技术栈和业务需求：

- **WebSocket 流式（Realtime 类 API）**：用于 `omni realtime api` 和 `realtime api user guide` 所述的实时语音/[多模态](multi-modal.md)交互。服务端通过结构化事件（如 `text.delta`、`audio.delta`、`tool_call.delta`）持续推送增量内容，客户端按事件类型解析并合成最终响应。典型用于语音助手、智能客服等需亚秒级反馈的场景。

- **SSE 流式（Server-Sent Events）**：用于 `audio api references` 和 `model experience` 中的 RESTful 接口（如 `/v1/models/{model}/invoke`）。当请求中设置 `"parameters": {"stream": true}` 时，响应头为 `Content-Type: text/event-stream`，每行以 `data: {...}` 格式携带 JSON 片段（如 `{"type":"content","delta":"你好"}` 或 `{"type":"finish","usage":{"output_tokens":12}}`）。适用于 Web 前端、CLI 工具等支持 SSE 的环境。

- **OpenAI 兼容流式（Toolkits & Frameworks）**：在 [OpenAI 兼容接口](openai-compatible-api.md)（如 `chat.completions.create()`）中，通过 `stream=True` 参数启用。返回标准 OpenAI 流式格式（`{"choices":[{"delta":{"content":"..."}}]}`），兼容各类开源 SDK 和 LLM 工具链（LangChain、LlamaIndex 等），便于快速迁移已有应用。

> ⚠️ 注意：`qwen-audio` 系列模型（如 ASR/TTS）**不支持 OpenAI 兼容协议**，仅可通过 DashScope 原生 WebSocket 或 RESTful SSE 接口启用流式；全模态模型（如 `qwen3.8-omni-flash`）在 [OpenAI 兼容接口](openai-compatible-api.md)中暂不支持流式，需使用 `model experience` 或 `omni realtime api`。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 | 是否必需 |
|------|------|------|------|----------|
| `stream` | `parameters` 对象内（所有 RESTful / Model Experience 接口） | `boolean` | 启用流式响应；设为 `true` 时返回 SSE；`false` 或省略则为非流式 JSON | 否（默认 `false`） |
| `stream` | [OpenAI 兼容接口](openai-compatible-api.md)函数参数（如 `chat.completions.create(stream=True)`） | `boolean` | 同上，语义一致 | 否（默认 `false`） |
| — | WebSocket 连接建立时（Realtime API） | — | 流式为默认行为，无需显式开关；所有响应均以事件流形式下发 | — |
| `enable_interim_results` | `realtime api user guide` 的 query string 或 session config | `boolean` | ASR 场景专用：控制是否返回中间识别结果（如 `"我今天"` → `"我今天想"`）；仅影响 `text` 事件，不影响 `audio` 流 | 否（默认 `false`） |
| `smooth_output` | `omni realtime api` 的 `session.update` 参数（Qwen3.8+ 预发布模型） | `boolean` | 控制文本输出风格：`true` 启用口语化分段（适合 TTS 播放），`false` 返回紧凑书面语 | 否（默认 `false`） |

> ✅ 实用提示：
> - 流式响应超时固定为 **60 秒**（不可配置），超时后连接关闭，需由客户端实现重连逻辑；
> - 所有流式接口均**不支持跨 session 上下文继承**，如需多轮对话，请复用同一 WebSocket 连接（Realtime）或在 `model experience` 中显式维护 `messages` 历史；
> - 解析流式响应时，请始终检查 `type` 字段（如 `content`/`tool_call`/`finish`）或 OpenAI 的 `finish_reason`，避免将中间片段误判为终态。

## 面向开发者，简洁实用

- **首选方案**：  
  - 实时语音/音视频交互 → 用 `omni realtime api`（WebSocket）；  
  - 通用文本/[多模态](multi-modal.md)流式 → 用 `model experience`（SSE） + `stream=true`；  
  - 快速集成/已有 OpenAI 生态 → 用 `toolkits and frameworks`（OpenAI 兼容）。

- **调试建议**：  
  使用 `curl -N` 或浏览器 DevTools 的 Network → EventStream 查看原始流；避免用 `json.loads()` 直接解析整条响应——应逐行读取、剥离 `data:` 前缀、再 `json.loads()` 单帧。

- **错误防御**：  
  流式响应中可能混入 `error` 事件（Realtime）或 `{"error":{...}}`（SSE），务必监听并处理；不要假设流一定以 `finish` 结束——网络中断、超时、模型异常均可能导致连接意外关闭。

- **性能注意**：  
  流式不降低单 token 计算开销，但可减少用户感知延迟；若追求极致吞吐（如批量离线生成），请改用非流式接口。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [audio api references](../api/audio-api-references.md)
- [model experience](../guides/model-experience.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


