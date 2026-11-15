# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，覆盖文本生成、视觉理解、向量嵌入、批量处理、会话管理等核心场景。开发者可复用现有 OpenAI SDK 和工具链，仅需调整 `base_url`、`api_key` 和模型名称即可快速迁移。所有接口均支持主流编程语言（Python/Node.js/Java/Go/C#/curl），并遵循 OpenAI REST API 规范与 SDK 行为。

## 支持的模型/功能

百炼支持的 OpenAI 兼容能力按功能维度划分：

- **Chat Completions**：标准对话接口，支持 `qwen3.8-max`、`qwen3.7-plus`、`qwen-vl-plus`、`deepseek-v4-pro`、`glm-5.3` 等数十种文本与多模态模型，详见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- **Responses API**：增强型智能体接口，内置联网搜索、网页抓取、代码解释器等工具，支持 `qwen4-max-preview`、`qwen3.8-omni-flash`、`deepseek-v4.1-flash` 等模型，适用于复杂任务编排 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。
- **Vision**：视觉理解专用接口，支持 `qwen3-vl-plus`、`QVQ`、`Qwen-OCR`，兼容 OpenAI 的 `image_url` 消息格式 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。
- **Embedding**：向量嵌入接口，支持 `text-embedding-v4`、`qwen3.7-text-embedding` 等 6 种模型，输出维度可配置（如 1024、2048），但**不支持稀疏向量输出** [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。
- **Conversations**：会话状态管理接口，用于跨设备/长时间中断的上下文延续，配合 Responses API 实现自动历史注入 [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。
- **Batch**：异步批量处理接口，分为文件输入（JSONL）和单请求同步等待两种模式，成本降低 50%，适用于数据标注、模型评测等非实时场景 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) 和 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。

> **注意**：`Qwen-Audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；多模态 Embedding 模型（如 `qwen3-vl-embedding`）也不支持 OpenAI 接口，需调用 DashScope 专用 API。

## 关键参数

所有 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)共用以下核心参数：

- `base_url`：必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低，**强烈建议迁移**。
- `api_key`：API Key 严格按地域绑定，北京地域 Key 无法调用弗吉尼亚 endpoint，否则返回 `invalid_api_key` 错误。
- `model`：模型名称需严格匹配文档列表，例如 `qwen3.8-max` 不可写作 `qwen38-max` 或 `qwen-max`（后者仅在新加坡地域可用）。
- `enable_thinking`：对 `qwen3.5`–`qwen3.8` 系列模型，默认开启思考模式，显式设为 `false` 可避免额外 token 开销；该参数须置于请求体顶层，不可嵌套在 `extra_body` 中。
- `previous_response_id`（Responses API）或 `conversation_id`（Conversations API）：用于上下文关联，前者为上一轮 `responses.create()` 返回的顶层 `id`（UUID 格式），后者为 `conversations.create()` 创建的会话 ID。

## 使用方式

### SDK 调用（推荐）

1. 安装对应 SDK：`pip install -U openai`（通用）或 `pip install langchain_openai`（LangChain 集成）；
2. 初始化客户端时传入 `base_url` 和 `api_key`（建议从环境变量读取）；
3. 调用对应方法：
   - Chat：`client.chat.completions.create(model=..., messages=[...])`
   - Responses：`client.responses.create(model=..., input="...")`
   - Embeddings：`client.embeddings.create(model=..., input="...")`
   - Conversations：`client.conversations.create(items=[...])`
   - Batch Chat：`client.chat.completions.create(...)` + `base_url="https://batch.dashscope.aliyuncs.com/compatible-mode/v1"`

### HTTP 调用

直接构造 POST 请求，Header 包含 `Authorization: Bearer $DASHSCOPE_API_KEY` 和 `Content-Type: application/json`，Body 为标准 OpenAI JSON 格式。各 endpoint 列表见各文档的“服务地址”章节。

### LangChain 集成

- **OpenAI 方式**：使用 `langchain_openai.ChatOpenAI`，仅支持部分百炼模型（如 `qwen-plus`），但兼容性高；
- **DashScope 方式**：使用 `langchain_community.chat_models.tongyi.ChatTongyi`（Python）或 `@langchain/community/chat_models/alibaba_tongyi`（JS），支持全部百炼文本模型及部署模型 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

## 限制和注意事项

- **地域绑定**：API Key 与 `base_url` 地域必须一致，跨地域调用将被鉴权拒绝（HTTP 401），错误码恒为 `invalid_api_key`。
- **Token 限制**：Batch 场景下，`qwen3.8-max` 等主流模型单次请求最大上下文为 256K tokens；`text-embedding-v4` 单行最大 8,192 tokens，`qwen3.7-text-embedding` 为 128,000 tokens。
- **文件上传**：`purpose=file-extract`（文档分析）单文件上限 150 MB；`purpose=batch`（批量输入）上限 500 MB；`purpose=fine-tune`（微调）上限 300 MB。
- **流式响应**：`qwen3-vl-plus` 等视觉模型仅支持[流式输出](../concepts/streaming-output.md)；`Responses API` 的 `stream_options={"include_usage": true}` 可在最后一 chunk 返回 token 统计。
- **[函数调用](../concepts/function-calling.md)（Function Calling）**：仅 `Chat Completions` 和 `Responses API` 支持，需在 `tools` 参数中明确定义函数 schema，并在 `tool_choice` 中指定策略（`auto`/`required`/`none`）。
- **过时路径**：`/api/v2/apps/protocols/compatible-mode/v1/responses` 和 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 已废弃，必须迁移到 `/compatible-mode/v1/responses` 和 `/compatible-mode/v1/conversations`。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)


