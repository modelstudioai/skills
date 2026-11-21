# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 REST API，严格遵循 OpenAI 的请求/响应协议（如 `/v1/chat/completions`、`/v1/embeddings` 等路径与字段结构），使开发者无需修改客户端代码即可将现有 OpenAI 集成快速迁移到百炼平台，底层调用 Qwen 系列及多模态专用模型。

## 在百炼平台的不同场景中如何使用

- **通用大模型调用**：通过 `POST /v1/chat/completions` 调用 `qwen-max`、`qwen-plus`、`qwen-turbo` 等文本模型，支持标准 `messages` 输入、流式响应（`stream: true`）和基础采样参数（`temperature`、`top_p`、`max_tokens`）。  
- **多模态任务**：Qwen-VL、GUI-Plus、Qwen-OCR 等模型同样支持 OpenAI 兼容接口，`messages[].content` 可传入含 `text` 和 `image_url`（base64 编码）的数组，无需切换协议。  
- **向量与排序服务**：Embedding（`/v1/embeddings`）和 Rerank（`/v1/rerank`）能力均提供 OpenAI 兼容端点，适配 `input`、`model`、`dimensions`（部分模型）、`instruct`（Rerank）等关键参数，与 LangChain、LlamaIndex 等生态无缝对接。  
- **批量与异步处理**：支持 `/v1/batches` 提交 `.jsonl` 批处理任务（每行一个 chat/completions 请求），文件需先通过 `/v1/files` 上传；也支持 Embedding 异步批处理（`/v1/embeddings/batch`）。  
- **智能体（Agent）开发**：`/v1/agents/chat/completions` 提供增强版兼容接口，额外支持 `session_id`（自动维护多轮上下文）、`environment_id`（知识库与工具沙箱隔离），适用于构建有状态、可扩展的 AI Agent 应用。  
- **工具链集成**：原生支持 LangChain 的 `BailianLLM`、`BailianEmbeddings` 等封装类，调用 `invoke()`、`stream()`、`embed_query()` 即自动路由至对应 OpenAI 兼容端点，零配置迁移。

> ⚠️ 注意：并非所有百炼模型都支持 OpenAI 兼容接口——例如 `qwen-deep-research` 仅支持 DashScope SDK，不开放该协议；具体支持情况请查阅各模型文档。

## 关键参数和配置

| 参数 | 是否必填 | 说明 | 兼容性备注 |
|------|----------|------|------------|
| `model` | ✓ | 必须显式指定百炼模型名（如 `"qwen-plus"`、`"qwen3.7-text-embedding"`），**不支持 OpenAI 别名（如 `gpt-3.5-turbo`）**；未传将返回 400 错误。 | 全部接口强制要求 |
| `messages` | ✓（chat 类） | 标准 OpenAI 消息数组，`role` 为 `"system"`/`"user"`/`"assistant"`；多模态模型中 `content` 支持混合 `text` + `image_url`（base64）。 | `system` 消息可用于注入提示或工具 schema |
| `tools` / `tool_choice` | ✗ | 支持[函数调用](function-calling.md)协议，但工具定义需符合百炼 Schema（非 OpenAI 原始嵌套结构）；`tool_choice` 支持 `"auto"`/`"none"`/`{"type":"function","function":{"name":"xxx"}}`。 | Agents API 完整支持；普通 Chat Completions 接口仅返回自然语言摘要，不返回结构化 tool_calls |
| `stream` | ✗ | 布尔值，默认 `false`；设为 `true` 启用 SSE 流式响应，字段为 `delta.content`。 | 所有 chat 类接口均支持 |
| `response_format` | ✗ | 仅支持 `{"type": "json_object"}`（需模型具备 JSON 输出能力，如 `qwen-plus`），`text` 为默认且不可省略。 | Agents API 中该参数被忽略 |
| `n` | ✗ | **始终被忽略，固定为 1**；如需并行生成，请使用 DashScope 原生接口。 | 全部 OpenAI 兼容接口统一限制 |
| `max_tokens` | ✗ | 默认 2048，上限依模型而定（如 `qwen-max` 为 8192）；超出将截断。 | 与 OpenAI 行为一致 |
| `batch_id`（Batch） | ✗（返回时） | Batch 接口创建后返回的 ID，**有效期为 7 天**（超期 `GET /v1/batches/{id}` 返回 404）。 | 区别于 OpenAI 的 `expired` 状态 |

> 🔒 认证方式：统一使用 Bearer Token，Header 中携带 `Authorization: Bearer <your_api_key>`，API Key 需在百炼控制台「API 密钥管理」中创建。

## 面向开发者：简洁实用指南

- ✅ **快速迁移**：将 OpenAI 请求 URL 中的 `https://api.openai.com/v1/...` 替换为百炼地址 `https://dashscope.aliyuncs.com/api/v1/...`，复用原有请求体与认证头，即可运行。  
- ✅ **推荐域名**：生产环境请使用业务空间专属域名 `https://{WorkspaceId}.{region}.maas.aliyuncs.com`（在控制台「业务空间详情」获取），性能与稳定性优于通用域名。  
- ✅ **调试建议**：首次调用失败时，优先检查 `model` 是否拼写正确、是否属于 OpenAI 兼容模型列表（如 `qwen-deep-research` 不支持）、`messages` 是否为空或超长（单次上限 32768 tokens）。  
- ❌ **明确不支持**：`logit_bias`、`user` 字段、`n > 1`、远程图片 URL（仅支持 base64）、跨会话状态保持（除 Agents API 外需自行维护 history）。  
- 📦 **SDK 优先**：推荐使用官方 `dashscope` Python SDK 或 LangChain 封装类（`BailianLLM`），自动处理重试、流式解析、错误映射，比裸 curl 更健壮。  

> 💡 提示：所有 OpenAI 兼容接口均计入百炼平台统一配额与计费体系，调用量可在控制台「用量监控」中实时查看。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [openai compatible agents api](../api/openai-compatible-agents-api.md)
- [more models](../api/more-models.md)
- [vector and sort](../api/vector-and-sort.md)


