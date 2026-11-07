# 流式输出

流式输出（Streaming Output）是指模型服务在推理过程中，将生成结果以增量、分块的方式持续返回给客户端，而非等待全部内容生成完毕后一次性响应。这种方式显著降低端到端延迟，提升用户感知响应速度，特别适用于长文本生成、实时语音识别、对话交互等对实时性敏感的场景。

## 在百炼平台的不同场景中如何使用

流式输出在百炼平台中并非全局通用能力，其支持范围与行为因模型类型和调用协议而异：

- **文本生成模型**（如 `qwen3.8-max`、`qwen3.7-plus`）：完全支持流式输出，适用于 Chat Completions、Responses API 和原生 DashScope `/v1/models/{model_id}/invoke` 接口。响应格式为 `text/event-stream`，每条 SSE 事件携带一个 `delta` 片段（含 `content`、`tool_calls` 等字段），客户端需按标准 SSE 协议解析。
  
- **语音识别（ASR）模型**：`qwen-audio-3.0-asr-flash`、`fun-asr-flash` 等支持流式识别，但有前置条件——例如 `qwen-audio-3.0-asr-flash` 要求输入音频时长 ≥60 秒才触发分片返回；短音频仍以同步方式返回完整结果。需通过 HTTP Header `X-DashScope-SSE: enable` 显式启用。

- **语音合成（TTS）与视觉/向量模型**：**不支持流式输出**。TTS 返回的是完整音频二进制流（`audio/mpeg` 等），视觉生成返回图像 URL 或 base64 数据，向量服务（embedding/rerank）仅返回结构化 JSON 响应。这些接口即使设置 `stream=true`，也会被静默忽略或返回错误。

- **全模态（Omni-modal）模型**：当前白名单模型中，仅 `qwen3.8-omni-flash` 支持流式文本输出（即多模态输入 + 文本流式输出），但音视频帧本身不流式传输，仍以单次上传方式提交。

> ⚠️ 注意：流式响应**不支持重试或断点续传**；若连接中断，需重新发起请求。客户端必须实现完整的 SSE 连接管理（包括自动重连、event ID 追踪、超时控制）。

## 关键参数和配置

| 参数 / 配置项 | 类型 | 说明 | 适用场景 |
|--------------|------|------|----------|
| `stream`（请求体参数） | `boolean` | 设为 `true` 启用流式响应。是 OpenAI 兼容、Anthropic 兼容及 DashScope 原生接口的统一开关。默认 `false`。 | 所有支持流式的模型（文本、部分 ASR） |
| `X-DashScope-SSE`（HTTP Header） | `string` | DashScope 原生协议专用 Header，值为 `enable` 时强制启用 SSE 流式；部分 ASR 模型（如 `qwen-audio-asr`）**必须设置此 Header 才生效**，仅设 `stream=true` 不足。 | DashScope 原生 ASR/TTS 接口 |
| `Content-Type`（响应头） | `string` | 流式响应固定为 `text/event-stream; charset=utf-8`。客户端必须据此识别并启用 SSE 解析器。 | 所有流式接口 |
| `max_tokens`（推荐配合使用） | `integer` | 设置合理上限可防止无限生成导致流式挂起；尤其在未设置 `stop` 时，建议显式指定。 | 文本生成类流式请求 |
| `temperature` / `top_p` | `number` | 流式不影响采样逻辑，但低 `temperature`（如 0.1）可提升 token 序列稳定性，减少流式过程中的语义跳变。 | 文本生成类流式请求 |

> ✅ 最佳实践：  
> - 使用 OpenAI SDK 时，直接传入 `stream=True`，SDK 自动处理 SSE 解析；  
> - 使用原生 HTTP 请求时，务必设置 `Accept: text/event-stream` 请求头，并使用 `fetch` 的 `ReadableStream` 或 `EventSource` 接收；  
> - 对 ASR 流式，优先选用 `qwen-audio-3.0-asr-flash` 并确保音频 ≥60 秒，避免空流或超时失败。

## 关联主题页

- [model experience](../guides/model-experience.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [audio api directory](../api/audio-api-directory.md)


