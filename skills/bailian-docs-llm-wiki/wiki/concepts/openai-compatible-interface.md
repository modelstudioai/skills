# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组遵循 OpenAI REST API 规范（v1）的标准化 HTTP 接口，支持使用标准 OpenAI SDK（如 `openai`、`langchain_openai`）直接调用百炼模型服务。它通过统一的请求结构、响应格式与错误码体系，实现零代码改造迁移——开发者仅需替换 `base_url` 和 `model` 参数，即可将原有 OpenAI 应用快速对接 Qwen、DeepSeek、GLM 等百炼托管模型。

## 在百炼平台的不同场景中，这个概念如何使用

OpenAI 兼容接口不是单一接口，而是一套覆盖多任务类型的协议适配层，按能力分层设计，适用于不同开发阶段和集成需求：

- **快速迁移与原型验证**：  
  使用 `/compatible-mode/v1/chat/completions`（Chat Completions）接口，完全兼容 OpenAI 的 `messages` 格式、`stream` 流式、`temperature`/`max_tokens` 等参数，适合已有 LangChain、LlamaIndex 或自研客户端的应用一键切换。

- **开箱即用的智能体能力**：  
  使用 `/compatible-mode/v1/responses`（Responses API），无需手动管理工具调用逻辑或对话历史——系统自动触发联网搜索、网页提取、代码解释器等内置工具，并隐式维护上下文。适用于构建客服助手、研究助理等“免配置”智能体。

- **向量与排序任务标准化接入**：  
  使用 `/compatible-mode/v1/embeddings` 和 `/compatible-api/v1/reranks` 接口，支持 `input` 字符串/数组、`model` 指定（如 `text-embedding-v4`、`qwen3-rerank`），返回与 OpenAI Embedding/Rerank 完全一致的 JSON 结构，便于复用现有 RAG 工具链。

- **文件与批量任务协同**：  
  通过 OpenAI 兼容的 `client.files.create()` 上传文件（用途为 `file-extract` 或 `batch`），再结合 `client.batches.create()` 提交异步批量推理任务，全程使用 OpenAI SDK 原生方法，无需学习新 API。

- **多模态与专用模型扩展**：  
  对支持 OpenAI 兼容协议的多模态模型（如 `qwen3-vl-plus`）、OCR 模型（`qwen3.5-ocr`）或 GUI 模型（`gui-plus`），可直接在 `messages` 中传入 `image_url` 或 `content` 多模态数组，复用 OpenAI Vision API 调用习惯。

> ⚠️ 注意：并非所有百炼模型均支持 OpenAI 兼容协议。例如 `Qwen-Audio`、`qwen-deep-research` 仅支持 DashScope 原生接口；`gte-rerank` 已下线，应改用 `qwen3-rerank`（其 OpenAI 兼容 rerank 接口仍可用）。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 示例值 |
|------|------|------|------|--------|
| `base_url` | string | 是 | 服务端点，**必须匹配业务空间地域与 Workspace ID**，不可使用通用域名 `dashscope.aliyuncs.com` | `https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `model` | string | 是 | 模型标识符，需与所选接口类型匹配（如 Chat 接口填 `qwen-max`，Embedding 接口填 `text-embedding-v4`） | `"qwen3.8-max"`, `"qwen3-vl-plus"`, `"text-embedding-v4"` |
| `workspace_id` | string | 是（部分场景） | 业务空间 ID，用于路由和鉴权，通常嵌入在 `base_url` 中；若使用独立域名则无需额外传参 | `"ws-abc123"` |
| `previous_response_id` | string | 仅 Responses API | 多轮对话必需，传入上一轮响应顶层 `id` 字段（UUID 格式），用于上下文延续 | `"0c842a11-c7d1-45da-b7ec-4e668c389xxx"` |
| `stream` | boolean | 否 | 是否启用 Server-Sent Events（SSE）流式响应，默认 `false`；Responses API 支持，但 `delta.content` 可能含工具中间结果 | `true` |
| `enable_thinking` | boolean | 否（Batch / GUI 场景） | 控制是否启用推理链输出（如 `thinking` 步骤），需与 `model` 同级传入，非全局参数 | `{"model": "gui-plus", "enable_thinking": true}` |

> ✅ 提示：  
> - 所有 OpenAI 兼容接口均使用 `Authorization: Bearer <DASHSCOPE_API_KEY>` 认证；  
> - `messages` 格式严格遵循 OpenAI 标准（`role` 为 `"system"`/`"user"`/`"assistant"`），但 `Responses API` 会忽略其中的历史维护逻辑；  
> - `functions` / `tools` 字段在 OpenAI 兼容接口中**不被解析**（工具调用由平台隐式控制），如需自定义工具 schema，请使用 Anthropic 兼容 Messages 或 DashScope 原生接口。

## 面向开发者，简洁实用

- ✅ **一行切换**：只需修改初始化代码中的 `base_url`，其余 `chat.completions.create()` 调用保持不变。  
- ✅ **SDK 优先**：推荐使用 `openai>=1.0.0` 官方 SDK（Python/Node.js/Java/Go/C# 全支持），自动处理重试、超时、流式解析。  
- ✅ **调试友好**：响应头含 `x-dashscope-request-id`，便于问题定位；错误响应结构与 OpenAI 一致（`{ "error": { "message": "...", "type": "invalid_request_error" } }`）。  
- ⚠️ **避坑提醒**：  
  - 不要混用 OpenAI 兼容接口与 DashScope 原生参数（如 `top_k`、`enable_search`）；  
  - `Responses API` 不支持 `stop`、`logprobs` 等高级参数；  
  - 批量任务（Batches）需先上传文件至 OpenAI 兼容 `files` 接口，再引用 `file_id` 创建 batch；  
  - 生产环境如需精确控制工具行为、token 采样或会话生命周期，建议逐步迁移到 DashScope 原生接口。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [vector and sort](../api/vector-and-sort.md)
- [file management api](../api/file-management-api.md)
- [more models](../api/more-models.md)


