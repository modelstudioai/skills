# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 OpenAI 兼容的工具集与框架接口，覆盖文本生成、多模态理解、向量嵌入、批量处理、会话管理等核心场景。开发者可通过统一 SDK（如 OpenAI Python/Node.js SDK）或 HTTP 直连方式快速迁移现有应用，仅需调整 `base_url`、`api_key` 和 `model` 三个参数即可接入。所有接口均支持业务空间专属域名以提升稳定性与性能。

## 支持的模型/功能

百炼兼容接口覆盖全栈能力：
- **文本生成**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash` 等 Qwen 系列主力模型，以及 DeepSeek、GLM、Kimi、MiniMax 等三方直供模型（详见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）；
- **多模态理解**：`qwen3-vl-plus`、`QVQ`、`Qwen-OCR` 支持图像/视频输入（详见 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)）；
- **向量嵌入**：`text-embedding-v4`、`qwen3.7-text-embedding` 等支持多语种与可调维度（详见 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)）；
- **智能体与上下文管理**：`Responses API` 内置联网搜索、代码解释器等工具；`Conversations API` 支持跨设备会话持久化；`Responses API` 的 `previous_response_id` 可自动关联多轮上下文（详见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) 和 [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)）；
- **文件与批量处理**：`Files API` 支持文档上传用于 Qwen-Long/Qwen-Doc-Turbo 推理；`Batch API` 提供异步批量处理与同步 Batch Chat 两种模式，成本降低 50%（详见 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md) 和 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)）。

> **注意**：`Qwen-Audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议（见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）；`qwen3.8-omni-flash` 在 Responses API 中支持音视频输入，但在 Chat Completions API 中未明确声明该能力，建议优先使用 Responses API 调用。

## 关键参数

- **`base_url`**：必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（如 `https://dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低；
- **`api_key`**：严格按地域绑定，北京地域 API Key 无法调用弗吉尼亚 endpoint，否则返回 `invalid_api_key` 错误（见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）；
- **`model`**：不同接口支持的模型范围不同。例如 Responses API 明确列出 `qwen3.8-omni-flash`，而 Chat Completions API 文档未提及其音视频支持；Embedding API 不支持 `output_type=sparse` 参数（见 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)）；
- **`enable_thinking`**：在 Batch 场景下，`qwen3.8`/`qwen3.7` 等系列模型默认开启思考模式，需显式传入顶层 `body.enable_thinking=false` 关闭以控制 token 成本（见 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)）；
- **`previous_response_id`**：Responses API 多轮对话中，必须传入上一轮响应的顶层 `id`（UUID 格式），而非 `output` 数组内消息的 `id`（见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)）。

## 使用方式

- **SDK 调用**：推荐使用 OpenAI SDK（Python/Node.js/Java/Go/C#）或 LangChain 封装（`langchain_openai` / `langchain-community`）。LangChain 提供双路径：`ChatOpenAI` 仅支持部分模型，`ChatTongyi`（或 `ChatAlibabaTongyi`）支持全部百炼文本模型（见 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)）；
- **HTTP 调用**：直接构造 POST 请求，`Authorization: Bearer $DASHSCOPE_API_KEY`，`Content-Type: application/json`，endpoint 依接口而定（如 `/chat/completions`、`/responses`、`/embeddings`）；
- **文件操作**：通过 `files.create(purpose="file-extract")` 上传文档，再将 `file_id` 传入 Qwen-Long 或 Qwen-Doc-Turbo 模型请求；
- **批量任务**：`Batch File API` 适用于高吞吐低时效场景（异步），`Batch Chat API` 适用于单请求长等待场景（同步），二者 endpoint 不同（`/batches` vs `/chat/completions`）；
- **会话管理**：先 `conversations.create()` 创建会话并注入 system message，后续通过 `conversations.items.create()` 追加消息，实现上下文隔离与复用。

## 限制和注意事项

- **地域与 Key 绑定**：API Key 与 endpoint 地域强一致，跨地域调用必失败（见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）；
- **文件配额**：`Files API` 总数上限 10,000 个，总大小上限 100 GB，无自动过期机制，需手动清理（见 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)）；
- **模型能力差异**：非阿里云直供模型（如三方 DeepSeek/Kimi）在 Responses API 中 Agent 能力受限，仅支持基础 chat（见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)）；
- **URL 迁移强制性**：`/api/v2/apps/protocols/compatible-mode/v1/responses` 和 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 已废弃，新版必须使用 `/compatible-mode/v1/responses` 和 `/compatible-mode/v1/conversations`（见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) 和 [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)）；
- **[流式输出](../concepts/streaming-output.md)兼容性**：`QVQ` 模型仅支持[流式输出](../concepts/streaming-output.md)，非流式调用将失败（见 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)）。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)


