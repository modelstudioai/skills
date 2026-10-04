# toolkits and [frameworks](frameworks.md)

阿里云百炼平台提供多种 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)及配套工具链，支持开发者快速迁移现有应用。核心能力覆盖文本生成（Chat/Responses/Completions）、多模态理解（Vision）、向量化（Embedding）、文件管理、批量推理（Batch）及会话状态管理（Conversations），所有接口均通过统一的 `compatible-mode/v1` 协议层提供，适配主流 SDK 和框架（如 OpenAI SDK、LangChain）。

## 支持的模型/功能

- **文本生成**：支持 `qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash` 等全系列 Qwen 文本模型，以及 DeepSeek、GLM、Kimi 等第三方直供模型；其中 `qwen3.8-omni-flash` 支持音视频输入 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。
- **多模态理解**：`qwen3-vl-plus`、`qwen3-vl-flash`、`qwen-vl-ocr` 等视觉模型支持图像/视频理解与 OCR，兼容 OpenAI Vision 接口规范 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。
- **[向量嵌入](../concepts/embedding.md)**：`text-embedding-v4`、`qwen3.7-text-embedding` 等 Embedding 模型支持多语种、可调维度向量化，但**不支持稀疏向量输出**（传入 `output_type=sparse` 将返回空 embedding）[OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。
- **长文档与结构化处理**：`Qwen-Long` 和 `Qwen-Doc-Turbo` 通过文件 ID 实现文档问答与数据提取，依赖 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。
- **批量处理**：支持两种模式：
  - **文件批量（Batch File）**：上传 JSONL 文件异步执行，适用于评测、标注等高吞吐场景 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)；
  - **单请求批量（Batch Chat）**：同步调用但后台异步执行，成本降低 50%，适用于非实时任务 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。
- **会话管理**：`Conversations API` 提供跨设备上下文持久化能力，配合 `Responses API` 自动注入历史消息，解决手动维护消息列表易丢失的问题 [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。

> **注意**：`Qwen-Audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；`completions` 接口当前**仅支持 `qwen-coder-turbo` 模型**，且仅限华北2（北京）地域，与其他接口的模型支持范围存在显著差异 [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。

## 关键参数

- **`base_url`**：必须使用业务空间专属域名以获得最佳性能，格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`（如 `cn-beijing`、`ap-southeast-1`）。旧域名（`dashscope.aliyuncs.com`）仍可用但不推荐 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。
- **`model`**：需严格匹配文档中列出的模型名称，例如 `qwen3.8-max`、`qwen3-vl-plus`、`text-embedding-v4`；第三方模型（如 `deepseek-v4-pro`）需在控制台开通后方可使用。
- **`enable_thinking`**：对 `qwen3.5+` 系列模型，默认开启思考模式，将产生额外 `reasoning_tokens` 并增加费用；必须作为 JSONL 请求体顶层参数显式传入（不可置于 `extra_body` 内）[OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。
- **`previous_response_id`**：用于 `Responses API` 多轮对话，必须传入上一轮响应的顶层 `id`（UUID 格式），而非 `output` 数组内消息的 `id` [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。
- **`purpose`**：文件接口必需参数，取值为 `file-extract`（文档分析）、`batch`（批量推理输入）、`fine-tune`（调优数据集）[OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。

## 使用方式

- **SDK 调用**：统一使用 OpenAI SDK（Python/Node.js/Java 等），仅需替换 `api_key` 和 `base_url`。LangChain 用户可选 `langchain_openai`（部分模型）或 `langchain-community` + `dashscope`（全模型支持）[在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。
- **HTTP 调用**：所有接口均提供标准 RESTful endpoint，如：
  - Chat：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`
  - Responses：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses`
  - Embeddings：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings`
  - Conversations：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/conversations`
- **[流式输出](../concepts/streaming-output.md)**：`stream=true` 参数支持边生成边返回，`stream_options={"include_usage": true}` 可在最后一帧返回 token 统计。
- **地域与密钥绑定**：API Key 严格按地域隔离，北京地域 Key 不可用于调用弗吉尼亚 endpoint，否则返回 `invalid_api_key` 错误 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。

## 限制和注意事项

- **地域限制**：`completions` 接口**仅支持华北2（北京）地域**；`Qwen-Audio` 不支持任何 OpenAI 兼容协议；部分第三方模型（如 SiliconFlow DeepSeek）仅在中国站北京地域可用 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- **文件配额**：文件服务总大小上限 100 GB，最多 10,000 个文件；单个 `file-extract` 文件最大 150 MB，`batch` 文件最大 500 MB，`fine-tune` 文件最大 300 MB [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。
- **Batch 限制**：`Batch Chat` 单次请求最长等待 3600 秒（1 小时）；`Batch File` 中 `qwen3.5-omni-plus` 不支持语音输出，且 `qwen3.8-max` 等模型在 Batch 场景下上下文 [Token](../concepts/token.md) 上限为 256K [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。
- **模型能力差异**：非阿里云直供模型（如三方直供 DeepSeek、Kimi）仅支持基础 Chat 功能，Agent 工具调用等高级能力受限；`qwen3.8-omni-flash` 是唯一支持音视频输入的模型 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。
- **路径弃用**：`/api/v2/apps/protocols/compatible-mode/v1/responses` 和 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 等旧版路径已停止维护，必须迁移至 `/compatible-mode/v1/{endpoint}` [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。

## 来源文档

- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)


