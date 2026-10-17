# 流式输出

流式输出（Streaming）是指模型响应以增量方式、分块返回给客户端的机制，而非等待整个推理完成后再一次性返回全部结果。它通过 `text/event-stream`（SSE）协议传输，使前端可实时渲染生成内容（如逐字显示、进度反馈），显著提升用户交互体验与响应感知速度。

## 在百炼平台的不同场景中，这个概念如何使用

- **文本生成类模型**（如 `qwen3.7-plus`、`qwen3.8-max`）：全面支持流式输出，适用于聊天界面、代码补全、长文摘要等需低延迟反馈的场景。[OpenAI 兼容接口](openai-compatible-interface.md)（`/chat/completions`）、Anthropic 兼容接口（`/messages`）及原生 DashScope API 均可通过 `stream=true` 启用。
  
- **[多模态](multimodal.md)模型**：  
  - `qwen3.8-omni-flash`（全模态）支持流式文本输出，但音视频输入处理本身不流式；  
  - 视觉理解（`qwen3.7-vl-plus`）、OCR（`qwen3.5-ocr`）等模型**不支持流式输出**，仅返回完整结构化结果；  
  - 视频生成（`wanx-video`）、3D 生成（`tripo`）、语音转语音（`speech-to-speech`）等**明确不支持流式输出**，调用时传入 `stream=true` 将被忽略或报错。

- **工具调用（Function Calling）**：当启用 `tools` 且模型需多步执行（如联网搜索 + 推理）时，流式响应会按执行阶段分块返回（如先返回 `tool_calls`，再返回最终 `content`），便于前端分阶段展示状态。

- **控制台与 SDK**：  
  - 百炼控制台「模型体验」页对支持流式的模型自动启用流式预览；  
  - `dashscope` Python SDK（v1.20.0+）提供 `StreamIterator` 封装，自动解析 SSE；  
  - OpenAI SDK（`openai>=1.0`）原生支持 `stream=True`，返回 `Stream[ChatCompletionChunk]` 对象。

## 关键参数和配置

- `stream`：布尔类型，必填参数（显式指定）。设为 `true` 即启用流式输出；设为 `false` 或省略则为非流式（默认行为）。所有兼容协议均统一支持该字段。

- `max_tokens`：影响流式输出长度上限。流式响应会在达到 `max_tokens` 或模型自然结束时终止，**不会截断中间 token**，但可能提前结束（如因超时或配额限制）。

- [Token](token.md) Plan 配额：流式响应的 token 消耗按实际生成量实时累计计费（输入 + 已返回的输出 token），**非按最终总长度结算**。例如返回 300 tokens 后中断，即消耗 300 输出 token。

- 注意事项：  
  - 流式响应不支持 `cache_control: {type: "ephemeral"}` 缓存标记；  
  - `response_format={"type": "json_object"}` 等结构化约束在流式下**不可用**（JSON 必须完整解析，无法分块验证）；  
  - 若请求绑定 [Token](token.md) Plan，流式调用同样受 `daily_quota` 和 `burst_limit` 实时约束，超限将立即中断流并返回 `429`。

## 面向开发者，简洁实用

- ✅ **推荐做法**：对用户可见的文本生成任务（尤其是对话、创作类），始终优先启用 `stream=true`，并配合前端防抖与错误重试逻辑。  
- ⚠️ **避坑提示**：不要在流式请求中设置 `response_format="json_object"`；视觉/视频/语音类模型勿强行启用流式；`speech-to-speech` 模型传 `stream=true` 将静默失败。  
- 🛠️ **调试建议**：使用 `curl -N` 或 Postman 的 SSE 模式直接测试响应流；SDK 中务必使用 `.on("chunk", ...)` 或 `for chunk in response:` 迭代处理，避免 `.text` 或 `.content` 等阻塞调用。  
- 📈 **性能注意**：流式不降低模型端推理延迟，但可减少首字节时间（TTFB）感知——实际 TTFB 取决于模型首 token 生成速度，`qwen3.8-flash` 等低延迟模型效果更显著。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [token plan guide](../guides/token-plan-guide.md)
- [model experience](../guides/model-experience.md)


