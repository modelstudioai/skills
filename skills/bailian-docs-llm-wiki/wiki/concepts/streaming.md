# 流式输出

流式输出（Streaming）是百炼平台模型服务提供的一种响应模式，允许模型在生成过程中持续、分块地返回结果，而非等待全部内容生成完毕后一次性返回。这种模式显著降低首 token 延迟（Time to First Token, TTFT），提升用户交互实时性，是语音助手、实时对话、长文本生成等低延迟场景的核心能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **标准 RESTful 接口（`/v1/chat/completions`）**：通过请求参数 `stream=true` 启用。适用于 `qwen-max`、`qwen-plus`、`qwen-turbo` 等通用文本模型。响应为 Server-Sent Events（SSE）格式，每行一个 `data: {...}` JSON 对象，包含增量的 `delta.content` 字段；最终块含 `finish_reason`（如 `"stop"` 或 `"length"`）和完整 `usage` 统计。

- **Realtime API（WebSocket 协议）**：原生流式设计，不依赖 `stream` 参数。所有响应（如 `response_chunk`、`speech_started`、`input_audio_buffer.speech_stopped`）均以 JSONL 格式实时推送，支持音频/视频帧级流式输入与模型推理结果的毫秒级对齐，适用于 `qwen-audio-realtime-v1`、`qwen-video-realtime-v1` 及 Omni 系列实时模型。

- **Omni Realtime API（多模态实时交互）**：强制流式，无非流式选项。通过 `session.update` 配置 `modalities: ["text", "audio"]` 后，文本输出与 TTS 音频流并行下发，支持 `smooth_output` 等高级流控策略，实现自然口语化中断与续说。

- **SDK 调用（DashScope / OpenAI 兼容 SDK）**：Python SDK 中 `dashscope.Generation.call(..., stream=True)` 或 OpenAI SDK 的 `client.chat.completions.create(..., stream=True)` 自动处理 SSE 解析，返回可迭代的 `Stream` 对象，开发者可逐 chunk 消费 `chunk.choices[0].delta.content`。

- **开发工具集成（如 Chatbox、QwenPaw、Cline）**：多数工具默认启用流式（如 Chatbox），部分需手动开启（如 Codex 的「Enable streaming」开关）。工具负责渲染增量内容，但底层仍依赖百炼服务端的 `stream=true` 响应。

> ⚠️ 注意：部分模型（如 `qwen3.7-plus`、`qwen3.8-omni-flash-realtime`）**强制要求** `stream=true`，否则返回 `400-InvalidParameter` 错误；非流式调用不被支持。

## 关键参数和配置

| 参数 | 类型 | 说明 | 示例/约束 |
|------|------|------|-----------|
| `stream` | boolean | 启用流式响应的开关。REST 接口必填（`true`/`false`）；Realtime/Omni 接口隐式启用，不可设为 `false`。 | `true`（推荐生产环境默认启用） |
| `incremental_output` | boolean | 仅 Omni/Realtime 场景相关。当 `enable_thinking=true` 时，**必须设为 `true`**；部分模型（如 `qwen3.7-plus`）仅支持 `true`。 | `true`（不可省略） |
| `result_format` | string | 影响流式 chunk 结构。思考模式模型（`enable_thinking=true`）**必须为 `"message"`**，否则报错。 | `"message"`（非 JSON Schema 模式下唯一合法值） |
| `max_latency_ms` | integer | Realtime API 专用，软性延迟上限（单位 ms），影响流式 chunk 的合并粒度。值越小，TTFT 越低，但可能增加网络开销。 | `100–2000`（默认 `300`） |

- **流式响应解析要点**：
  - REST 接口：响应头 `Content-Type: text/event-stream`；需按行解析 `data: {...}`，忽略空行和注释行（`:` 开头）；
  - Realtime/Omni：响应为纯 JSONL（每行一个 JSON 对象），无 `data:` 前缀，直接 `json.loads(line)`；
  - 所有场景下，首个 chunk 包含 `choices[0].delta.role`（通常为 `"assistant"`），后续 chunk 的 `delta.content` 为增量文本，最终块含 `finish_reason` 和 `usage`。

## 面向开发者，简洁实用

- ✅ **推荐做法**：生产环境一律启用 `stream=true`，配合前端/客户端增量渲染，避免用户长时间白屏；
- ✅ **错误规避**：调用 `qwen3.7-plus` 等模型时，务必显式传 `stream=true` 和 `result_format="message"`，否则 400 报错；
- ✅ **调试技巧**：用 `curl -N` 或 Python `requests.get(..., stream=True)` 手动测试流式响应，验证 chunk 解析逻辑；
- ❌ **禁止操作**：在 Realtime/Omni 场景下尝试设置 `stream=false`；在思考模式下使用 `response_format={"type":"json_object"}`（与流式不兼容）；
- 📈 **性能提示**：流式不改变 `max_tokens` 限制——超限仍会截断，且 `usage.completion_tokens` 为最终总 token 数，非累计值。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [preparations](../api/preparations.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)


