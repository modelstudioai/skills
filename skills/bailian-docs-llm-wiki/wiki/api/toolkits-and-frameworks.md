# toolkits and [frameworks](frameworks.md)

阿里云百炼提供一系列 OpenAI 兼容的工具包与框架接口，覆盖文本生成、[多模态](../concepts/multi-modal.md)理解、向量嵌入、批量推理、对话管理及文件处理等核心场景。开发者可复用现有 OpenAI SDK 和工程实践，仅需调整 `base_url`、`api_key` 和模型名称即可快速迁移；同时支持 LangChain 等主流 LLM 应用框架，降低集成门槛。

## 支持的模型/功能

百炼兼容接口支持三大类能力：

- **通用文本生成**：包括 `qwen4-max`、`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash` 等全系列千问模型，以及 DeepSeek（v4.1）、GLM（5.3）、Kimi（k3）等三方直供模型（仅限华北2北京地域）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- **[多模态](../concepts/multi-modal.md)能力**：`qwen3-vl-plus`、`QVQ`、`Qwen-OCR` 支持图像理解；`qwen3.5-omni-plus`、`qwen3.5-omni-flash` 支持音视频输入；`qwen3.8-omni-flash` 可处理音视频并生成文本回复 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。  
- **专用功能接口**：`qwen-long` 和 `qwen-doc-turbo` 支持文档问答与数据提取；`text-embedding-v4`、`qwen3.7-text-embedding` 等向量模型支持语义检索；`conversations` 与 `responses` 接口分别提供会话状态持久化和智能体原生上下文管理能力 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。

> **注意**：`Qwen-Audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；而 `qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出，该限制在 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) 和 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md) 中均被重复强调，属一致约束。

## 关键参数

所有兼容接口共用以下核心参数，但行为存在关键差异：

- **`base_url`**：必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低，官方强烈建议迁移 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- **`api_key`**：严格按地域绑定，北京地域 API Key 无法调用弗吉尼亚 endpoint，错误码为 `invalid_api_key`（非密钥失效），需在对应地域控制台创建 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- **`model`**：不同接口支持的模型范围不同。例如 `responses.create()` 支持 `qwen4-max`、`deepseek-v4-pro` 等数十个模型，而 `files.create(purpose="file-extract")` 仅适用于 `qwen-long` 和 `qwen-doc-turbo`；`embeddings.create()` 则限定为 `text-embedding-*` 和 `qwen3.7-text-embedding*` 系列。  
- **`enable_thinking`**：对 `qwen3.5+` 系列模型，默认开启思考模式，将产生额外 `reasoning_tokens` 并增加成本。该参数须作为 `body` 顶层字段传入（不可置于 `extra_body`），且仅在 Batch 场景（JSONL 输入）中生效 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。

## 使用方式

### SDK 调用（推荐）
- **OpenAI SDK**：适用于所有兼容接口（Chat、Responses、Vision、Embedding、Files、Batch、Conversations）。需安装 `openai>=1.0.0`，配置 `base_url` 和 `api_key`，调用对应方法（如 `client.chat.completions.create`、`client.responses.create`、`client.files.create`）。
- **LangChain 集成**：提供双路径支持：
  - `langchain_openai.ChatOpenAI`：仅支持 OpenAI 兼容模型子集（如 `qwen-plus`），配置 `base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"`；
  - `langchain_community.chat_models.tongyi.ChatTongyi`（Python）或 `@langchain/community/chat_models/alibaba_tongyi.ChatAlibabaTongyi`（JS）：支持百炼全部文本模型，使用原生 DashScope 协议 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

### HTTP 直连
- 所有接口均提供标准 RESTful endpoint，如：
  - Chat：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`
  - Responses：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses`
  - Embedding：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings`
  - Conversations：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/conversations`

### 文件与批量处理
- **文件上传**：通过 `client.files.create(file=..., purpose="file-extract"|"batch"|"fine-tune")` 上传，返回 `file_id` 供后续模型调用 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。  
- **批量推理**：支持两种模式：
  - `Batch Chat`（同步）：单请求阻塞等待，适合低并发、中等延迟容忍场景，endpoint 为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`；
  - `Batch File`（异步）：上传 JSONL 文件，系统后台处理后返回结果文件，适合高吞吐、离线分析场景，费用为实时调用的 50% [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。

## 限制和注意事项

- **地域与密钥强绑定**：跨地域调用必然失败（HTTP 401 + `invalid_api_key`），且 `qwen3.8-max` 等模型在新加坡地域的 Batch 支持范围小于北京地域，务必查阅各文档的“适用范围”章节确认 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。  
- **协议不兼容项**：
  - `Qwen-Audio` 不支持 OpenAI 兼容协议；
  - `text-embedding-v4` 通过 OpenAI 接口不支持 `output_type=sparse`，传入后 embedding 字段为空；
  - `conversations` 接口的旧版路径 `/api/v2/apps/protocols/...` 已废弃，新版为 `/compatible-mode/v1/conversations`。  
- **资源配额**：文件服务总容量上限 100 GB、文件数上限 10,000 个；`previous_response_id`（用于 `responses` 多轮）有效期为 7 天；`conversations` 的 `metadata` 键值对最多 16 对，key ≤ 64 字符，value ≤ 512 字符。  
- **流式响应细节**：`stream_options={"include_usage": True}` 仅在流式结束 chunk 中返回 `usage`，非流式响应则直接包含在主对象中；`qwen3-vl-plus` 等视觉模型[流式输出](../concepts/streaming-output.md)时，`delta.content` 为分片文本，最终 `finish_reason="stop"` 后附带完整 token 统计。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)


