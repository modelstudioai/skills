# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)工具包与框架，覆盖文本生成、多模态理解、向量嵌入、批量推理、对话管理等核心场景。开发者可复用现有 OpenAI 生态代码（如 SDK、LangChain 集成），仅需调整 `base_url`、`api_key` 和模型名称即可快速迁移。所有接口均支持标准 OpenAI RESTful 语义与 SDK 调用方式，同时扩展了百炼特有能力（如内置工具、会话上下文自动管理、思考模式控制等）。

## 支持的模型/功能

- **文本生成**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash` 等全系列 Qwen 模型，以及 DeepSeek、GLM、Kimi、MiniMax 等三方直供模型（详见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）。
- **多模态理解**：`qwen3-vl-plus`、`QVQ`、`Qwen-OCR`，支持图像/视频输入与结构化输出（详见 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)）。
- **向量嵌入**：`text-embedding-v4`、`qwen3.7-text-embedding` 等，支持多语种与可配置维度（详见 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)）。
- **批量处理**：支持两种模式——文件批量（JSONL 格式异步处理）和单请求批量（同步等待，成本降低 50%），适用于评测、标注等非实时场景（详见 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) 和 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)）。
- **高级对话管理**：`Conversations API` 提供会话生命周期管理（创建、更新、删除、追加消息），配合 `Responses API` 实现跨设备上下文自动注入与智能体原生能力（如联网搜索、代码解释器）（详见 [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md) 和 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)）。
- **文件管理**：`Files API` 支持上传文档用于长文本问答（Qwen-Long）、数据提取（Qwen-Doc-Turbo）或作为 Batch 输入源（详见 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)）。

> **注意**：`Qwen-Audio` 不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；多模态 Embedding 模型（如 `qwen3-vl-embedding`）亦不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，需调用 DashScope 专用 API。

## 关键参数

- **`base_url`**：必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低。`{WorkspaceId}` 需替换为控制台中实际的业务空间 ID。
- **`api_key`**：严格按地域绑定。北京地域的 API Key 仅能调用北京 endpoint，跨地域调用将返回 `invalid_api_key` 错误（详见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）。
- **`model`**：模型名称需与百炼控制台发布的名称完全一致（如 `qwen3.8-max`，而非 `qwen-max`）。部分模型（如 `qwen3.5-omni-plus`）在 Batch 场景下不支持语音输出。
- **`enable_thinking`**（Batch 场景）：`qwen3.5+` 系列模型默认开启思考模式，显式设置 `enable_thinking=false` 可避免额外 token 开销（详见 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)）。
- **`previous_response_id`**（Responses API）：用于多轮对话，必须传入上一轮响应的顶层 `id`（格式为 `resp_xxx`），而非 `output` 数组内消息的 `id`（格式为 `msg_xxx`）。

## 使用方式

1. **SDK 初始化**：使用 OpenAI SDK（Python/Node.js/Java/Go/C#）或 LangChain 封装（`langchain_openai.ChatOpenAI` 或 `langchain_community.chat_models.tongyi.ChatTongyi`），配置 `api_key` 与 `base_url`。
2. **接口调用**：
   - Chat：`client.chat.completions.create(...)`（流式/非流式）
   - Vision：同上，`messages.content` 包含 `image_url` 字段
   - Embedding：`client.embeddings.create(...)`，支持 `dimensions` 参数（v3/v4）
   - Batch（文件）：先 `client.files.create(purpose="batch")`，再 `client.batches.create(input_file_id=...)`
   - Batch（单请求）：改用 `base_url="https://batch.dashscope.aliyuncs.com/compatible-mode/v1"`
   - Responses：`client.responses.create(...)`，支持 `input` 字符串或 `previous_response_id`
   - Conversations：`client.conversations.create(...)` + `client.conversations.items.create(...)`
3. **LangChain 集成**：推荐 `ChatOpenAI`（兼容性好）或 `ChatTongyi`（支持全部百炼模型），详见 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

## 限制和注意事项

- **地域隔离**：API Key 与 `base_url` 地域必须严格匹配，否则鉴权失败（HTTP 401），错误码为 `invalid_api_key`。
- **文件配额**：`Files API` 总数上限 10,000 个，总大小上限 100 GB，无自动过期机制，需手动清理。
- **Batch 文件大小**：`purpose="batch"` 的 JSONL 文件最大 500 MB；`purpose="file-extract"` 的文档最大 150 MB；`purpose="fine-tune"` 的训练集最大 300 MB。
- **模型能力差异**：非阿里云直供模型（如三方 DeepSeek）仅支持基础 Chat Completions，不支持 Responses API 的内置工具等高级能力。
- **超时控制**：Batch Chat 同步调用默认超时 3600 秒（1 小时），需在 SDK 客户端显式配置（如 Python 的 `.with_options(timeout=1800.0)`）。
- **思考模式成本**：`qwen3.5+` 系列模型在 Batch 场景下默认启用思考模式，`output_tokens_details.reasoning_tokens` 会计费，建议按需关闭 `enable_thinking`。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)


