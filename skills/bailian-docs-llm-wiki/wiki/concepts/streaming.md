# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种响应模式，允许模型服务将结果分块、渐进式地返回给客户端，而非等待全部计算完成后再一次性返回完整响应。该机制显著降低端到端延迟，提升用户体验，尤其适用于长文本生成、语音合成、实时对话等对响应速度敏感的场景。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用（Model Experience）**：通过 `/v1/models/{model_id}/invoke` 接口发起请求时，设置 `parameters.stream = true`（或在 JSON body 中显式声明 `"stream": true`），即可启用流式响应。仅对 `text-generation`、`text-to-speech` 和 `omni-modal` 任务生效；`embedding`、`rerank` 等确定性任务强制同步返回，不支持流式。

- **Qwen API（OpenAI/Anthropic 兼容协议）**：在 `chat/completions`、`responses` 或 `messages` 请求中，传入 `"stream": true` 即可开启流式。响应为标准 Server-Sent Events（SSE）格式，每帧包含 `data: {...}`，开发者需按行解析并拼接 `delta` 字段（如 `content`、`audio_url` 或 `tool_calls` 的增量部分）。

- **框架集成（LlamaIndex / Spring AI Alibaba）**：通过框架封装参数控制流式行为：LlamaIndex 使用 `streaming=True` 初始化 LLM，Spring AI Alibaba 使用 `chatOptions.stream(true)`。框架自动处理 SSE 解析与事件聚合，开发者只需订阅 `onChunk` 或 `onResponse` 回调即可获取实时片段。

- **实时 API（Realtime API Directory）**：所有实时能力（ASR、TTS、Audio Realtime、Omni Realtime）**默认且仅支持流式**，基于 WebSocket 协议实现双向实时帧传输。客户端无需额外配置 `stream` 参数，但必须使用 WebSocket 客户端连接，并按协议解析 `response.text.delta`、`output.audio` 等事件帧。

- **工具包与 SDK**：官方 Python/Node.js SDK 均内置流式支持。例如 Python SDK 中调用 `client.chat.completions.create(..., stream=True)` 后，返回一个可迭代对象，`for chunk in response:` 即可逐块消费；Node.js SDK 提供 `on('chunk')` 事件监听器。

## 关键参数和配置

| 参数 | 类型 | 说明 | 是否必需 | 备注 |
|------|------|------|----------|------|
| `stream` | boolean | 启用流式响应的开关 | 否（默认 `false`） | HTTP 接口需显式设为 `true`；WebSocket 实时 API 强制启用，忽略此参数 |
| `response_format`（可选） | object | 控制流式输出结构，如 `{"type": "json_object"}` | 否 | 仅部分模型支持，启用后 `delta` 内容将按 JSON Schema 校验并分块输出 |
| `max_tokens`（文本类） | integer | 限制单次流式响应的最大 token 数 | 否 | 防止无限生成，建议设置合理上限（如 `512`） |
| `audio_format`（TTS/Realtime） | string | 指定音频编码格式（如 `pcm16`、`mp3`） | 是（TTS 场景） | 影响流式音频帧的二进制格式与解码方式 |

> ⚠️ 注意：  
> - 流式响应头中固定包含 `Content-Type: text/event-stream`；  
> - 所有流式接口均要求客户端具备 SSE 或 WebSocket 解析能力，不支持简单 `fetch().then()` 直接读取 `.text()`；  
> - 若请求中 `stream=true` 但模型或任务类型不支持（如 `embedding`），平台将返回 `400 Bad Request` 并提示 `"stream is not supported for this task"`。

## 面向开发者，简洁实用

- ✅ **快速启用**：只需在请求 body 中加一行 `"stream": true`，无需修改 endpoint 或认证逻辑。  
- ✅ **统一解析**：所有 HTTP 流式响应均遵循 SSE 标准（`data: {...}\n\n`），推荐使用 SDK 内置流式迭代器，避免手动解析换行与 JSON 转义。  
- ✅ **错误处理**：流式过程中若发生错误（如超时、鉴权失败），服务端会发送 `event: error` 帧并终止连接；客户端应监听 `event.error` 并重试。  
- ✅ **性能提示**：流式不降低总计算耗时，但显著改善首字节时间（Time to First Token, TTFT）和感知延迟；建议搭配 `temperature=0.3~0.7` 和 `top_p=0.9` 使用，平衡稳定性与多样性。  
- ❌ **不适用场景**：需要原子性结果校验（如金融摘要）、离线批量处理、或下游系统无法处理增量数据时，请使用同步模式。

## 关联主题页

- [model experience](../guides/model-experience.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [frameworks](../api/frameworks.md)
- [realtime api directory](../api/realtime-api-directory.md)


