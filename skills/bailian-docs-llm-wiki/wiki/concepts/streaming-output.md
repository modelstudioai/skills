# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种实时响应机制，允许模型或应用在生成结果过程中，将输出内容按 token、chunk 或语义单元分段推送至客户端，而非等待全部计算完成后再返回完整响应。该机制显著降低端到端延迟，提升用户交互体验，尤其适用于长文本生成、多轮对话、RAG问答等对响应速度敏感的场景。

## 在百炼平台的不同场景中如何使用

流式输出在百炼平台多个核心能力层中统一支持，但启用条件与行为细节因服务类型而异：

- **模型调用（Model Experience）**：通过 `/v1/models/{model_id}/invoke` 接口，在 `parameters.stream = true` 时启用。仅文本生成（LLM）和全模态（Omni-modal）模型支持；视觉生成、语音（ASR/TTS）、向量（embedding/rerank）类模型不支持，误设将返回 `400 Bad Request`。响应格式为 `text/event-stream`（SSE），需按标准 SSE 协议解析 `data:` 行。

- **智能体与工作流应用调用（Application Call / Bailian Application Calling）**：在 `POST /api/v1/apps/{APP_ID}/completion` 或 `/api/v1/applications/{application_id}/call` 中设置 `stream = true`。支持增量输出（推荐同时设置 `incremental_output = true` 避免重复拼接），工作流还支持 `flow_stream_mode = "message_format_plus"` 以获取更结构化的节点级流式事件。

- **知识库问答（Knowledge Base QA）**：调用 `/v1/knowledge_bases/{kb_id}/qa` 时传入 `"stream": true`，可同时流式返回检索片段（`retrieval_results`）和模型生成答案（`answer`），便于前端实现“边检索边思考”的渐进式呈现。

- **Qwen 系列 API（OpenAI/Anthropic/DashScope 协议）**：  
  - OpenAI 兼容 Chat Completions：设置 `"stream": true`，遵循 OpenAI SSE 格式（含 `choices[0].delta.content`）；  
  - Responses API：`"stream": true` 启用流式响应，支持 `previous_response_id` 多轮上下文延续；  
  - DashScope 原生协议：`parameters.stream = true`，响应含 `output.text` 增量字段及 `is_last: false/true` 标识。

> ⚠️ 注意：所有场景下，**异步调用（如 `background=true`）均不支持流式输出**；流式必须配合同步 HTTP 请求使用。

## 关键参数和配置

| 参数名 | 所属场景 | 类型 | 默认值 | 说明 |
|--------|----------|------|--------|------|
| `stream` | 全场景通用 | boolean | `false` | 启用流式响应的核心开关。必须显式设为 `true`，否则返回完整 JSON 响应。 |
| `incremental_output` | Application Call（DashScope 协议） | boolean | `false` | 流式模式下是否返回增量内容（如仅新生成 token），避免客户端重复拼接。**强烈推荐设为 `true`**。 |
| `flow_stream_mode` | 工作流应用 | string | `"message_format"` | 控制流式事件结构：`"message_format_plus"`（推荐）返回带 `node_id` 和 `event_type` 的结构化 chunk；`"message_format"` 仅返回原始文本流。 |
| `timeout` | Application Call | integer | — | 流式请求建议显式设置（如 `300`），防止长尾请求无限挂起；超时后返回 `504 Gateway Timeout`。 |

> ✅ 最佳实践：  
> - 客户端务必设置合理的 `timeout`（建议 ≥ 60s）并实现 SSE 连接重试逻辑；  
> - 解析时忽略空行、注释行（`:` 开头），只处理 `data:` 行；  
> - 检查每个 chunk 中的 `is_last`（DashScope）、`finish_reason`（OpenAI）或 `done` 字段，确认流是否结束；  
> - 对于含工具调用（function calling）的流式响应，需按 `tool_calls` 数组的 `index` 字段顺序合并 delta 内容。

## 面向开发者，简洁实用

- **一句话启用**：在请求体 `parameters`（模型调用）或顶层对象（应用/知识库调用）中添加 `"stream": true`。  
- **三步解析流**：① 设置 `Accept: text/event-stream`；② 按行读取，提取 `data:` 后的 JSON 字符串；③ `JSON.parse()` 后检查 `output.text`（DashScope）或 `choices[0].delta.content`（OpenAI）字段。  
- **避坑提示**：  
  - 不要对 `rerank` 或 `embedding` 模型设 `stream=true`；  
  - 工作流流式需配合 `flow_stream_mode` 使用，否则可能丢失节点信息；  
  - 知识库流式响应中，`retrieval_results` 可能在 `answer` 之前或穿插返回，需按 `event_type` 区分处理。  
- **调试建议**：使用 `curl -N` 或 Postman 的 SSE 插件直接观察原始流；生产环境务必添加连接保活与错误降级（如自动 fallback 到非流式）。

## 关联主题页

- [model experience](../guides/model-experience.md)
- [application call](../api/application-call.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [knowledge base](../guides/knowledge-base.md)
- [bailian application calling](../guides/bailian-application-calling.md)


