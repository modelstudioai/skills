# toolkits and [frameworks](frameworks.md)

阿里云百炼提供一系列 OpenAI 兼容的工具包与框架接口，覆盖文本生成、多模态理解、向量嵌入、批量推理、对话管理等核心场景。开发者可复用现有 OpenAI SDK 代码，仅需调整 `base_url`、`api_key` 和模型名称即可快速迁移，无需重写业务逻辑。所有接口均支持标准 OpenAI 请求/响应格式，并针对百炼平台特性（如 Workspace ID 域名、地域绑定鉴权、专属工具能力）进行了增强。

## 支持的模型/功能

百炼兼容接口支持多种模型类型与高级功能：

- **文本生成**：`qwen3.8-max`、`qwen3.7-plus`、`qwen-coder-turbo` 等全系列千问模型，以及 DeepSeek、GLM、Kimi、MiniMax 等第三方直供模型（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）。
- **多模态理解**：`qwen3-vl-plus`、`qwen3-vl-flash`、`qwen-vl-ocr` 支持图像输入与结构化输出（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)）。
- **向量嵌入**：`text-embedding-v4`、`qwen3.7-text-embedding` 等支持多维度、多语种文本向量化（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)）。
- **批量处理**：`Batch Chat` 与 `Batch File` 接口支持异步批量请求，成本降低 50%，适用于数据标注、评测等非实时场景（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)）。
- **智能体增强**：`Responses API` 内置联网搜索、网页抓取、代码解释器等工具，支持自动工具调用与思考链（reasoning tokens）；`Conversations API` 提供会话级上下文管理，实现跨设备对话延续。

> **注意**：`Qwen-Audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议（见 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）。此外，`completions` 接口（文档 5）当前**仅限华北2（北京）地域**且**仅支持 `qwen-coder-turbo` 模型**，与其他接口的地域/模型覆盖范围存在显著差异。

## 关键参数

所有兼容接口共用以下核心参数，但行为细节因接口而异：

- `base_url`：必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（如 `https://dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）。
- `api_key`：严格按地域绑定，北京地域 API Key 不可用于调用弗吉尼亚 endpoint，否则返回 `invalid_api_key` 错误（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）。
- `model`：需从各接口明确列出的支持列表中选择，例如 `Responses API` 要求使用 `qwen3.8-max` 等特定版本，而 `completions` 接口仅接受 `qwen-coder-turbo`。
- `stream` 与 `stream_options`：[流式输出](../concepts/streaming-output.md)通用参数，`stream_options={"include_usage": true}` 可在最后一 chunk 返回 token 使用统计。
- `enable_thinking`：仅 `Batch Chat` 和 `Batch File` 接口支持，用于显式控制思考模式开关（默认开启），影响 token 计费（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)）。

## 使用方式

### 初始化客户端
统一使用 OpenAI SDK 初始化，替换 `base_url` 和 `api_key`：
```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
```

### 接口调用示例
- **Chat Completions**（标准对话）：`client.chat.completions.create(model="qwen3.8-max", messages=[...])`
- **Responses**（智能体增强）：`client.responses.create(model="qwen3.8-max", input="你能做什么？")`
- **Embeddings**（向量化）：`client.embeddings.create(model="text-embedding-v4", input="文本")`
- **Files**（文件上传）：`client.files.create(file=Path("doc.pdf"), purpose="file-extract")`
- **Batch Chat**（同步批量）：将 `base_url` 切换为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1` 后调用 `chat.completions.create`
- **Batch File**（异步批量）：先 `files.create(purpose="batch")`，再 `batches.create(input_file_id=..., endpoint="/v1/chat/completions")`
- **Conversations**（会话管理）：`client.conversations.create(items=[{"role":"system","content":"..."}])`

### LangChain 集成
推荐两种方式：
- `langchain_openai.ChatOpenAI`：仅支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)覆盖的模型（如 `qwen-plus`），配置 `base_url` 即可（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)）。
- `langchain_community.chat_models.tongyi.ChatTongyi`：支持百炼全部模型（含部署模型），使用原生 DashScope 协议，需安装 `dashscope` 包。

## 限制和注意事项

- **地域与密钥强绑定**：API Key 与 `base_url` 所属地域必须一致，跨地域调用必然失败（HTTP 401），错误码为 `invalid_api_key`（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）。
- **模型能力差异**：`Responses API` 的 Agent 能力（内置工具）仅对列表中阿里云直供模型完全生效；第三方模型（如 SiliconFlow DeepSeek）在该接口下仅支持基础补全（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)）。
- **文件服务配额**：`Files API` 总文件数上限 10,000 个，总大小上限 100 GB；单个 `file-extract` 文件最大 150 MB，`batch` 文件最大 500 MB（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)）。
- **Batch 超时机制**：`Batch Chat` 默认等待 3600 秒，超时后连接断开并返回错误；`Batch File` 任务最长运行 24 小时（`completion_window="24h"`）。
- **Embedding 稀疏向量限制**：[OpenAI 兼容接口](../concepts/openai-compatible-api.md)不支持 `output_type=sparse`，传入该参数将导致 embedding 字段为空（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)）。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)


