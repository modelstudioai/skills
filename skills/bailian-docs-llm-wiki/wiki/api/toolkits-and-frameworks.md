# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，覆盖文本生成、多模态理解、向量化、批量处理、会话管理等核心场景，支持开发者复用现有 OpenAI 生态代码快速迁移。所有接口均基于统一的 `compatible-mode/v1` 路径设计，但不同能力模块（如 Chat、Responses、Conversations）在功能边界、模型支持和参数语义上存在明确区分，需按实际需求选用。

## 支持的模型/功能

- **Chat Completions**：支持 Qwen 系列（`qwen3.8-max`、`qwen3.7-plus` 等）、DeepSeek、GLM、Kimi、MiniMax 等数十种文本与多模态模型，但 [Qwen-Audio 不支持 OpenAI 兼容协议](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)，仅支持 DashScope 原生协议。
- **Responses API**：专为智能体（Agent）场景优化，内置联网搜索、网页抓取、代码解释器等工具，当前仅支持 `qwen3.8-*`、`qwen3.7-*`、`deepseek-v4-*`、`glm-5.*`、`kimi-k3` 等直供模型；非列表中模型仅支持基础兼容能力，Agent 功能受限 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。
- **Vision（图像理解）**：支持 `qwen3-vl-plus`、`QVQ`、`Qwen-OCR`，其中 QVQ 模型**仅支持[流式输出](../concepts/streaming.md)**，使用方式见 [视觉推理文档](../../raw/model-user-guide/model-experience/vision-model/visual-reasoning.md)。
- **Embedding**：支持 `text-embedding-v1` 至 `v4`、`qwen3.7-text-embedding` 及其 Flash 版本；**多模态 Embedding（如 `qwen3-vl-embedding`）不支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)**，须调用 DashScope 原生 API [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。
- **Files & Batch**：文件上传接口（`/files`）支持 `file-extract`（用于 Qwen-Long/Qwen-Doc-Turbo）、`batch`（用于批量推理）、`fine-tune`（用于调优数据集）三类用途；Batch 接口分两种形态：文件输入式（`/batches`）和同步式（`/chat/completions` with `base_url=https://batch.dashscope.aliyuncs.com`），后者仅支持单请求 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。
- **Conversations**：提供会话生命周期管理（创建、查询、更新、删除）及消息项追加能力，配合 Responses API 实现跨设备上下文延续，**旧版路径 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 已废弃**，必须迁移到 `/compatible-mode/v1/conversations`。
- **Completions（FIM）**：专用于代码补全，当前仅支持 `qwen-coder-turbo` 模型，且**仅限华北2（北京）地域**，不支持其他地域或模型。

> **注意**：文档 1 和文档 2 均提及“业务空间专属域名迁移”，但文档 1 列出的德国（法兰克福）、中国香港地域 endpoint 在文档 2 的 Responses API 部分未被覆盖；文档 2 明确列出法兰克福（`eu-central-1`）和中国香港（`cn-hongkong`）的 Responses endpoint，而文档 1 的 Chat 接口描述中缺失这两地。实际开发应以文档 2 的 Responses 地域列表为准，Chat 接口若需在法兰克福或香港调用，需确认对应地域是否已同步开通 Chat 兼容 endpoint。

## 关键参数

- **`base_url`**：必须按地域和功能选择正确 endpoint：
  - Chat / Vision / Embedding / Files / Completions：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`
  - Responses / Conversations：同上，但 endpoint path 为 `/responses` 或 `/conversations`
  - Batch Chat（同步式）：固定为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`
  - Batch File（异步式）：`https://dashscope.aliyuncs.com/compatible-mode/v1`（北京）或 `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`（新加坡）
- **`{WorkspaceId}`**：业务空间 ID，仅在 `maas.aliyuncs.com` 域名下需要，从控制台“业务空间详情”获取；`dashscope.aliyuncs.com` 类域名无需替换。
- **`api_key`**：严格按地域绑定，**北京地域 API Key 无法调用弗吉尼亚 endpoint**，否则返回 `invalid_api_key` 错误 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- **`model`**：必须使用文档明确列出的模型名，例如 `qwen3-vl-plus`（Vision）、`text-embedding-v4`（Embedding）、`qwen-coder-turbo`（Completions）；`qwen3.8-max` 在 Chat 和 Responses 中均可用，但 Responses 中启用 Agent 工具时行为更丰富。
- **`purpose`（Files）**：决定文件用途，值必须为 `file-extract`、`batch` 或 `fine-tune`，不可混用。
- **`enable_thinking`（Batch）**：`qwen3.5+` 系列模型默认开启思考模式，**必须作为 JSONL 请求体顶层参数传入**，不能放在 `extra_body` 内，否则无效。
- **`stream_options={"include_usage": true}`**：仅对流式响应生效，在最后一 chunk 返回 token 统计。

## 使用方式

1. **初始化客户端**：设置 `api_key`（推荐环境变量）和 `base_url`（按功能+地域选择）。
2. **选择接口方法**：
   - 简单对话 → `client.chat.completions.create()`
   - Agent 智能体 → `client.responses.create()`（支持 `previous_response_id` 自动续写）
   - 图像理解 → `client.chat.completions.create()` with `messages.content` 包含 `image_url`
   - 向量化 → `client.embeddings.create()`
   - 文件上传 → `client.files.create(file=..., purpose="...")`
   - 批量异步 → `client.files.create(purpose="batch")` → `client.batches.create(input_file_id=...)`
   - 批量同步 → `client.chat.completions.create()` with `base_url=https://batch.dashscope.aliyuncs.com`
   - 会话管理 → `client.conversations.create()` / `.retrieve()` / `.update()` / `.delete()`
   - 代码补全 → `client.completions.create()`（仅 `qwen-coder-turbo`）
3. **传参调用**：按接口要求传入 `model`、`input`/`messages`/`prompt`、`stream` 等必要参数。
4. **处理响应**：非流式直接解析 `response.choices[0].message.content`；流式遍历 `chunk` 并检查 `chunk.choices[0].delta.content`；Responses API 响应结构为嵌套 `output` 数组，主文本在 `output_text` 字段或 `output[].content[].text` 中。

## 限制和注意事项

- **地域隔离**：API Key 与 endpoint 地域强绑定，跨地域调用必鉴权失败，错误码 `invalid_api_key` 表示地域不匹配，而非密钥失效。
- **模型能力差异**：同一模型名在不同接口中能力不同，例如 `qwen3.8-max` 在 Chat 接口中不支持内置工具，而在 Responses 接口中支持；`qwen3.8-omni-flash` 在 Responses 中可处理音视频输入，但在 Chat 中需额外适配。
- **Endpoint 迁移强制性**：`/api/v2/apps/protocols/...` 类旧路径（如 Conversations、Responses）**已停止维护**，必须迁移到 `/compatible-mode/v1/...` 新路径。
- **文件配额**：百炼存储空间上限为 10,000 个文件或 100 GB 总大小，超限后上传失败，需手动清理。
- **Batch 超时**：Batch Chat（同步式）最长等待 3600 秒（1 小时），超时断连；Batch File（异步式）`completion_window` 最长支持 `24h`。
- **LangChain 集成**：`langchain_openai` 仅支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)所列模型；如需调用全部百炼模型（如部署模型、Qwen-VL），应使用 `langchain-community` 的 `ChatTongyi` 或 `ChatAlibabaTongyi` [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。
- **Qwen-Audio 与多模态 Embedding**：二者均**不支持 OpenAI 兼容协议**，必须使用 DashScope 原生接口。

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
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)


