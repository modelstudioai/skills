# toolkits and [frameworks](frameworks.md)

阿里云百炼提供一系列 OpenAI 兼容的工具包与框架接口，覆盖文本生成、多模态理解、向量嵌入、批量推理、文件管理及会话状态管理等核心场景。开发者可复用现有 OpenAI SDK 代码，仅需调整 `base_url`、`api_key` 和 `model` 参数即可快速迁移，显著降低集成成本。

## 支持的模型/功能

百炼支持的 OpenAI 兼容能力按功能维度划分如下：

- **通用对话（Chat）**：支持 `qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash` 等全系列 Qwen 文本模型，以及 `qwen-vl-plus`、`qwen3-vl-flash` 等视觉模型，完整兼容 `chat/completions` 接口，包括[流式输出](../concepts/streaming-output.md)、`function_call` 和 `tool_calls` [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- **智能体原生响应（Responses）**：专为 Agent 场景优化，内置联网搜索、网页抓取、代码解释器等工具，支持 `qwen3.8-omni-flash` 处理音视频输入，并通过 `previous_response_id` 自动管理上下文 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。  
- **文本补全（Completions）**：面向代码续写、FIM（Fill-in-the-Middle）等场景，当前仅支持 `qwen-coder-turbo` 模型，需使用特殊分隔符 `<tool_call>{prefix}<tool_call>{suffix}<tool_call>` [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。  
- **多模态理解（Vision）**：兼容 `qwen3-vl-plus`、`qwen3-vl-flash`、`qwen-vl-ocr` 等模型，支持 `image_url`（含 OSS URL 与 data URI）和结构化 `content` 数组输入 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。  
- **向量嵌入（Embedding）**：支持 `text-embedding-v4`、`qwen3.7-text-embedding` 等多版本模型，提供 64–2048 维可选向量，但**不支持稀疏向量输出**（传入 `output_type=sparse` 将返回空 embedding）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。  
- **文件管理（Files）**：用于文档问答（`Qwen-Long`）、数据提取（`Qwen-Doc-Turbo`）、批量任务（`purpose=batch`）及模型调优（`purpose=fine-tune`），单文件上限依用途不同为 150 MB（`file-extract`）至 500 MB（`batch`）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。  
- **批量处理（Batch）**：包含两种模式：  
  - **Batch Chat**：同步调用风格，单请求等待返回，适用于低并发、高延迟容忍场景；  
  - **Batch File**：异步文件提交，支持 JSONL 格式批量请求，费用为实时调用的 50% [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。  
- **会话管理（Conversations）**：提供 `conversations` CRUD 接口，配合 Responses API 实现跨设备、长时间中断的上下文延续，避免手动维护消息历史 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。

> **注意**：文档 10 中列出的 `Qwen-Audio` 明确声明“不支持 OpenAI 兼容协议”，而文档 1 的 Responses API 支持列表中却包含 `qwen3.8-omni-flash`（该模型具备音频能力）。二者存在隐含矛盾——实际应以 Responses API 的 Omni 能力为准，`qwen3.8-omni-flash` 可通过 Responses 接口处理音视频，但**不支持标准 OpenAI `chat/completions` 的 audio 输入格式**。

## 关键参数

| 参数 | 作用 | 注意事项 |
|------|------|----------|
| `base_url` | 指定服务端点 | 必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）已逐步停用；地域与 API Key 必须严格匹配，跨地域调用将返回 `invalid_api_key` 错误 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。 |
| `model` | 指定调用模型 | 不同接口支持的模型范围不同：`completions` 仅支持 `qwen-coder-turbo`；`embeddings` 不支持多模态模型；`batch` 场景下 `qwen3.8-max` 等模型默认开启思考模式，需显式设置 `enable_thinking=false` 关闭以控本。 |
| `stream` / `stream_options` | 控制输出方式 | `stream=true` 启用流式；`stream_options={"include_usage": true}` 可在流式末尾返回 token 统计。 |
| `previous_response_id` | Responses API 上下文关联 | 必须传入上一轮响应的顶层 `id`（UUID 格式），而非 `output` 数组内消息的 `id` [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。 |
| `purpose` (Files) | 文件用途标识 | `file-extract`（文档分析）、`batch`（批量任务）、`fine-tune`（调优数据集），决定文件处理逻辑与大小限制。 |
| `dimensions` (Embeddings) | 向量维度 | 仅 `text-embedding-v3` 和 `text-embedding-v4` 支持该参数；`qwen3.7-text-embedding` 等模型需通过 `dimension` 查询参数指定（非请求体）。 |

## 使用方式

1. **环境准备**：获取并配置 API Key 到环境变量（推荐），安装对应 SDK（如 `pip install -U openai langchain_openai`）；  
2. **初始化客户端**：设置 `base_url` 为业务空间专属地址，`api_key` 为对应地域密钥；  
3. **选择接口与模型**：根据场景选用 `chat.completions`、`responses.create`、`embeddings.create` 等方法，并传入兼容模型名；  
4. **构造请求体**：  
   - 对于 `chat/completions`，使用标准 `messages` 数组；  
   - 对于 `responses`，可直接传 `input: string` 或 `messages`，并利用 `previous_response_id`；  
   - 对于 `files`，使用 `client.files.create(file=..., purpose=...)`；  
   - 对于 `conversations`，先 `client.conversations.create()`，再 `client.conversations.{conversation_id}/items` 追加消息；  
5. **处理响应**：解析 `choices[0].message.content`（Chat）、`output_text`（Responses）、`data[0].embedding`（Embeddings）等字段。

LangChain 集成推荐优先使用 `langchain_openai.ChatOpenAI`（兼容性好、文档完善），若需调用百炼全量模型（如部署模型或 `Qwen-Omni`），则使用 `langchain_community.chat_models.tongyi.ChatTongyi` [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

## 限制和注意事项

- **地域绑定强制**：API Key 与 `base_url` 所属地域必须一致，北京 Key 无法调用弗吉尼亚 endpoint，错误码为 `invalid_api_key`（非密钥失效）；  
- **模型能力隔离**：`completions` 接口仅支持 `qwen-coder-turbo`，其他模型调用将报错；`qwen3.8-omni-flash` 的音视频能力**仅在 Responses API 可用**，不兼容标准 Chat 接口；  
- **Batch 与 Thinking 模式**：`qwen3.8`/`qwen3.7` 系列模型在 Batch 场景下默认启用思考模式，会产生额外 `reasoning_tokens`，务必通过 `enable_thinking=false` 关闭（需置于 JSONL `body` 顶层，不可放 `extra_body`）；  
- **Embedding 稀疏向量限制**：[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**完全不支持** `output_type=sparse`，调用将返回空结果；如需稀疏向量，请改用 DashScope 原生接口；  
- **文件配额**：百炼存储空间上限为 10,000 个文件或 100 GB 总容量，超限后上传失败，需主动清理；  
- **Conversations 生命周期**：会话本身无自动过期机制，但其关联的消息项（`items`）在 `delete conversation` 时**不会被删除**，需单独管理。

## 来源文档

- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)


