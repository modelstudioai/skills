# 流式输出

流式输出（Streaming Output）是指模型服务在生成响应过程中，将结果以增量方式分块、实时推送至客户端，而非等待全部内容生成完毕后一次性返回。这种方式显著降低用户感知延迟，提升交互体验，尤其适用于长文本生成、实时对话、前端渐进式渲染等场景。

## 在百炼平台的不同场景中如何使用

- **基础模型调用（LLM）**：所有支持流式的文本生成模型（如 `qwen3.8-max`、`qwen-plus`）均通过设置 `stream: true` 启用流式响应，返回格式为 Server-Sent Events（SSE），每帧包含一个 token 或小段文本（`delta.content`）。  
- **应用构建（Application / Agent）**：在智能体或 RAG 应用中，启用 `stream: true` 可实现对话流式回显；进一步设置 `incremental_output: true` 可确保每帧仅返回新增 token，避免重复传输历史内容，减少带宽与前端解析开销。  
- **[多模态](multi-modal.md)模型**：视觉理解（Qwen-VL）、语音合成（TTS）等部分模态支持流式，但视频生成、3D 模型生成、ASR 等异步任务暂不支持流式输出（需轮询任务状态）。  
- **协议兼容性**：OpenAI 兼容（Chat/Responses）、Anthropic 兼容（Messages）及原生 DashScope 协议均统一支持 `stream` 参数，语义一致，开发者可复用现有流式处理逻辑。

## 关键参数和配置

| 参数 | 类型 | 说明 | 是否必需 | 默认值 |
|------|------|------|----------|--------|
| `stream` | boolean | 启用流式响应。设为 `true` 时，响应头为 `Content-Type: text/event-stream`，响应体为 SSE 格式 | 否 | `false` |
| `incremental_output` | boolean | 仅在 `stream: true` 时生效；控制是否启用增量式 token 输出（即每帧只含新生成内容，不含历史内容） | 否 | `false` |

> **注意**：  
> - 客户端必须正确解析 SSE（如使用 `EventSource` 或 `fetch().body.getReader()`），否则易出现丢帧、乱序或解析失败；  
> - 若未设置 `X-DashScope-SSE: enable` 请求头（REST API 场景），部分服务端可能降级为普通 JSON 响应（即使 `stream: true`），建议显式携带该 header；  
> - `incremental_output: true` 不影响模型内部生成逻辑，仅改变响应 payload 的组织方式，推荐在 Web 前端、移动端等对带宽和渲染效率敏感的场景中启用。

## 面向开发者的提示

- ✅ 推荐使用官方 `dashscope` SDK（v1.20.0+）或百炼 Python SDK，内置流式迭代器（如 `for chunk in response:`），自动处理 SSE 解析与错误重试；  
- ✅ 流式响应中，最终结果可通过检测 `finish_reason` 字段（如 `"stop"` 或 `"length"`）判断生成结束，勿依赖空帧或超时；  
- ❌ 不要对流式响应做同步阻塞式读取（如 `response.text`），应使用异步流式读取接口；  
- ⚠️ 免费额度与计费按实际输出 token 数计量，流式与非流式计费规则一致，无额外成本。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [application support](../guides/application-support.md)
- [model experience](../guides/model-experience.md)


