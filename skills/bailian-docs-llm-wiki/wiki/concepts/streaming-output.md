# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种实时响应机制，允许模型在生成过程中逐 token（或逐 chunk）返回结果，而非等待全部内容生成完毕后一次性返回。该机制显著降低端到端延迟，提升用户交互体验，尤其适用于对话类应用、长文本生成、语音合成等对响应速度敏感的场景。

## 在百炼平台的不同场景中，这个概念如何使用

流式输出在百炼平台中并非全局默认能力，而是按模型类型和调用协议有选择地支持：

- **文本生成（LLM）**：所有主流 Qwen 系列模型（如 `qwen3-32b`、`qwen4-max`）均支持流式输出，适用于 Chat、Responses、Anthropic Messages 等协议，以及原生 DashScope API。
- **语音合成（TTS）**：`qwen-audio` 等 TTS 模型支持流式音频分片返回（如 PCM 或 MP3 片段），便于实现低延迟播放。
- **不支持的场景**：
  - 视觉生成（图像/视频）、语音识别（ASR）、向量服务（embedding/rerank）、全模态（omni-modal）模型**不支持流式输出**；调用其 `/invoke-stream` 端点将直接返回 `400 Bad Request`。
  - 异步任务（如图像生成、视频生成）本身为长耗时作业，采用轮询或事件回调机制，与流式输出无关。

调用方式取决于所选协议：
- **DashScope 原生 API**：使用专用流式端点 `POST /v1/models/{model}/invoke-stream`，并设置请求头 `Accept: text/event-stream`。
- **OpenAI 兼容 API（Chat Completions）**：在请求体中设置 `"stream": true`，响应为 Server-Sent Events（SSE）格式。
- **Anthropic Messages API**：同样通过 `"stream": true` 启用，响应结构兼容 Anthropic 标准 SSE。

> ⚠️ 注意：流式响应需客户端具备 SSE 解析能力；若使用 `curl` 调试，建议添加 `-N` 参数禁用缓冲（`curl -N ...`），否则可能阻塞首帧。

## 关键参数和配置

| 参数 | 类型 | 说明 | 是否必需 | 默认值 |
|------|------|------|----------|--------|
| `stream` | boolean | 启用流式响应模式 | 是（启用流式时） | `false` |
| `incremental_output` | boolean | 在 `stream=true` 下启用增量式输出（即每次仅返回新增 token，而非全量重传） | 否 | `false` |
| `Accept` 请求头 | string | 必须设为 `text/event-stream`（DashScope 原生流式调用） | 是（DashScope 流式） | — |

- `incremental_output=true` 可显著减少网络带宽占用和前端渲染开销，推荐在 Web 应用中启用；
- 所有流式响应均以 SSE 格式返回，每行以 `data:` 开头，末尾含双换行符（`\n\n`）；
- 流式响应中仍包含完整 `usage` 字段（token 统计）和 `request_id`，但位于最终的 `data: [DONE]` 之前；
- 若请求中同时指定 `stream=false` 和 `stream=true`（如多处赋值），以最后解析的布尔值为准；建议显式声明一次。

## 面向开发者，简洁实用

- ✅ **快速启用**：只需在请求体加 `"stream": true`（OpenAI/Anthropic 协议）或改用 `/invoke-stream` 端点（DashScope 协议），无需修改模型或输入格式。
- ✅ **安全可靠**：流式响应与同步响应共享同一鉴权、限流、配额和错误码体系（如 `429 Too Many Requests`、`401 Unauthorized`），行为一致。
- ✅ **调试友好**：使用 `curl -N -H "Accept: text/event-stream"` 可直接观察 token 逐个生成过程；SDK 中推荐使用 `dashscope.Client.stream()`（Python）或 `StreamResponse`（Java）封装类。
- ❌ **避免踩坑**：
  - 不要对非流式支持模型（如 `wanx2.1-t2i-turbo`）调用流式接口；
  - 不要在流式请求中遗漏 `Accept: text/event-stream`（DashScope 原生）或 `Content-Type: application/json`；
  - 前端处理 SSE 时，务必监听 `error` 事件并实现重连逻辑（网络中断时自动恢复）；
  - `incremental_output` 仅影响 `output.text` 字段的更新方式，不影响 `output.choices[0].delta.content` 的语义（OpenAI 协议下已天然增量）。

流式输出是构建高性能 AI 应用的关键能力。启用它，让响应“动起来”。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [model experience](../guides/model-experience.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [application support](../guides/application-support.md)
- [more about models](../api/more-about-models.md)


