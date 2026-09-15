# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种实时响应机制，允许模型在生成过程中持续、分块地返回结果（如 token、文本片段或结构化事件），而非等待全部内容生成完毕后一次性返回。该机制显著降低端到端延迟，提升用户体验，并支持前端实时渲染、语音合成驱动、长文本渐进式处理等关键场景。

## 在百炼平台的不同场景中如何使用

流式输出在百炼平台的多个 API 层级和产品形态中统一支持，但启用方式与适用约束略有差异：

- **基础模型 API（`/v1/chat/completions`）**：通过请求参数 `stream=true` 启用，响应为 Server-Sent Events（SSE）格式，每条事件包含 `delta`（增量文本）、`finish_reason` 等字段。适用于直接调用 Qwen 系列等托管模型的场景。
  
- **应用调用（Application Call）**：
  - DashScope 原生接口：使用 `enable_stream="true"`（字符串类型）；
  - [OpenAI 兼容接口](openai-compatible-api.md)：使用 `stream=true`（布尔类型）；
  - 注意：二者参数名与类型不一致，需严格按所选协议文档传参。

- **沙箱（Sandbox）环境**：完全支持流式响应，行为与线上模型 API 一致；无需额外配置，只需在请求中设置 `stream=true` 即可。

- **应用组件 API（如 `/apps/{app_id}/chat`）**：支持 `stream=true` 参数，返回标准 SSE 流；适用于集成对话能力的自定义应用。

- **Realtime API（实时多模态）**：原生以流式为默认交互范式，通过 AOQ/WebSocket/WebRTC 协议持续推送 `text`、`audio`、`interim` 等事件帧，不依赖 `stream` 参数开关，而是由协议层保障低延迟、有序、带状态的流式交付。

> ⚠️ 共同约束：所有流式调用均要求显式指定 `max_tokens`（或等效参数如 `max_output_tokens`），否则将返回 `400 Bad Request` 错误。

## 关键参数和配置

| 参数名 | 类型 | 所属接口 | 说明 |
|--------|------|-----------|------|
| `stream` | boolean | 模型 API、应用组件 API、[OpenAI 兼容接口](openai-compatible-api.md) | 设为 `true` 启用 SSE 流式响应；响应头含 `Content-Type: text/event-stream` |
| `enable_stream` | string (`"true"`/`"false"`) | DashScope 原生应用调用接口（`/api/v1/applications/{app_id}/call`） | 必须传字符串，非布尔值；传错类型将导致 400 |
| `max_tokens` / `max_output_tokens` | integer | 全部流式接口 | **必填**；用于预分配资源并防止无限生成；取值需 ≤ 模型 context window 限制（如 `qwen-turbo` 最大 8192） |

其他注意事项：
- 超时控制：流式请求连接空闲超时为 **90 秒**（同步调用为 60 秒），建议客户端实现心跳保活或重连逻辑；
- 错误处理：流式响应中若发生错误（如鉴权失败、配额耗尽），服务端会发送 `error` 事件并终止流，客户端应监听 `event: error` 并解析 `data` 字段；
- 客户端解析：推荐使用标准 SSE 解析器（如浏览器 `EventSource`、Python `sseclient-py`），避免手动按 `\n\n` 切分导致事件丢失。

## 面向开发者：快速上手提示

- ✅ **推荐做法**：首次调试流式功能时，优先使用 `curl` 验证基础通路：
  ```bash
  curl -X POST "https://dashscope.aliyuncs.com/api/v1/chat/completions" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "model": "qwen-max",
          "input": {"messages": [{"role": "user", "content": "请用一句话介绍百炼平台"}]},
          "parameters": {"max_tokens": 100},
          "stream": true
        }'
  ```

- ❌ **常见陷阱**：
  - 忘记传 `max_tokens` → 400 错误；
  - DashScope 原生应用调用误传 `enable_stream=true`（布尔）→ 应为 `"true"`（字符串）；
  - 在 Realtime API 中错误尝试添加 `stream` 参数 → 该协议下无效且可能被忽略；
  - 未处理 `finish_reason` 字段（如 `"stop"`、`"length"`、`"tool_calls"`）→ 无法准确判断生成是否完成或中断原因。

- 🛠️ **生产建议**：
  - 前端：使用 `AbortController` 控制流式请求生命周期，避免内存泄漏；
  - 后端：对流式响应做缓冲与节流（如每 50ms 合并一次 delta），减少 UI 频繁重绘；
  - 日志：记录 `request_id` 和首/末事件时间戳，便于流式性能归因分析。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [preparations](../api/preparations.md)
- [sandbox](../guides/sandbox.md)
- [application call](../api/application-call.md)
- [application component api reference](../api/application-component-api-reference.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


