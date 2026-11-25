# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组遵循 OpenAI REST API 规范（如路径、请求/响应结构、错误格式）的标准化模型服务入口，使开发者无需修改业务逻辑即可复用 OpenAI SDK、LangChain、LlamaIndex 等生态工具，快速接入百炼托管的 Qwen 系列及第三方大模型。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移已有应用**：已集成 `openai` Python SDK 或 `@langchain/openai` 的项目，只需将 `base_url` 替换为百炼专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），并传入百炼 API Key 和支持的模型 ID（如 `qwen4-max`），即可直接调用。
- **智能体（Agent）开发**：通过 `/v1/agents` 和 `/v1/sessions` 等 OpenAI 兼容 Agents API，创建具备[工具调用](tool-calling.md)、长期记忆与环境隔离能力的 AI Agent；底层自动调度 `qwen-plus` 或 `qwen-max` 模型，无需自行编排[函数调用](function-calling.md)逻辑。
- **多模态理解与生成**：使用 `/v1/chat/completions` 接口配合 `qwen3-vl-plus` 或 `qwen4-max`，通过标准 `messages` 数组中的 `image_url` 字段传入图像，实现图文问答、OCR、图表解析等能力。
- **向量检索与嵌入**：调用 `/v1/embeddings` 接口（兼容 OpenAI Embedding 格式），输入文本获取稠密向量，用于 RAG、语义搜索等场景；支持 `text-embedding-v4`、`qwen3.7-text-embedding` 等模型。
- **文件处理与批量推理**：通过 `/v1/files`（上传）、`/v1/batch`（异步批处理）等 OpenAI 兼容 File/Batch 接口，以 JSONL 格式提交批量请求，或上传 PDF/DOCX 文件用于内容提取（`purpose=file-extract`），全程保持 OpenAI 风格参数与响应结构。

> ⚠️ 注意：Qwen-Audio 模型**不支持任何 OpenAI 兼容协议**，仅可通过 DashScope 原生协议调用；所有 OpenAI 兼容接口均不支持音频输入/输出。

## 关键参数和配置

| 参数 | 位置 | 是否必填 | 说明 | 示例值 |
|------|------|----------|------|--------|
| `base_url` | SDK 初始化 / HTTP 请求根路径 | 是 | 百炼专属服务地址，含 Workspace ID 与地域信息 | `https://my-workspace.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `model` | 请求 body | 是 | 必须为控制台已开通且在对应接口支持列表中的模型 ID | `qwen4-max`, `qwen3-vl-plus`, `text-embedding-v4` |
| `messages` | 请求 body | Chat/Responses 接口必填 | 标准 OpenAI 消息数组，`role` 限 `system`/`user`/`assistant`；多模态需按规范嵌入 `image_url` | `[{"role":"user","content":[{"type":"text","text":"描述这张图"},{"type":"image_url","image_url":{"url":"data:image/png;base64,..."}}]}]` |
| `previous_response_id` | 请求 body（Responses API） | 多轮对话时必填 | 上一轮响应的顶层 `id`（UUID），用于无状态上下文恢复 | `"0c842a11-c7d1-45da-b7ec-4e668c389xxx"` |
| `store` | 请求 body（Responses API） | 否（设为 `true` 才可后续检索） | 启用响应持久化，允许通过 `response_id` 查询、删除或复用该次输出 | `true` |
| `purpose` | 请求 body（Files API） | 是（上传时） | 明确文件用途，决定下游任务类型与格式校验 | `"file-extract"`, `"batch"`, `"fine-tune"` |
| `enable_thinking` | 请求 body（部分模型） | 否 | 控制是否启用模型内部推理链（`reasoning_tokens`），`qwen3.5+` 系列默认开启 | `true` |

- **认证方式**：统一使用 `Authorization: Bearer <api_key>`，API Key 需与所选计费方案匹配（[Token](token.md) Plan / Coding Plan / 按量计费均有独立 Key）。
- **地域要求**：`base_url` 中的 `{WorkspaceId}` 和 `region`（如 `cn-beijing`）必须与 API Key 所属地域一致，跨地域调用将返回 `invalid_api_key`。

## 面向开发者，简洁实用

- ✅ **即插即用**：安装最新版 `openai` SDK（≥1.40.0），初始化客户端时仅替换 `base_url` 和 `api_key`，其余代码零改动。
- ✅ **调试友好**：错误响应完全兼容 OpenAI 格式（含 `error.type`、`error.message`、`error.code`），可直接复用现有错误处理逻辑。
- ✅ **平滑演进**：同一 `base_url` 下支持多种子接口（`/chat/completions`、`/embeddings`、`/agents`、`/files`），无需维护多套域名或鉴权逻辑。
- ❌ **不支持项**：`stream_options`（流式控制）、`response_format`（JSON Schema 强约束）、稀疏向量（Embedding 接口）、`Qwen-Audio`、自定义模型权重（Agents API 仅限 `qwen-plus`/`qwen-max`）。
- 📌 **最佳实践**：  
  - 多轮对话优先选用 Responses API（支持 `previous_response_id` + `store`）而非手动拼接 `messages`；  
  - 生产环境务必使用 Workspace ID 构造 `base_url`，避免通用域名限流；  
  - 文件类任务优先采用 OpenAI 兼容 `/v1/files` 而非旧版 DashScope File API。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [openai compatible agents api](../api/openai-compatible-agents-api.md)
- [file management api](../api/file-management-api.md)


