# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)工具包与框架，覆盖文本生成、多模态理解、向量嵌入、批量推理、会话管理等核心场景。开发者可复用现有 OpenAI SDK 代码，仅需调整 `base_url`、`api_key` 和模型名即可快速迁移。所有兼容接口均支持主流编程语言（Python/Node.js/Java/Go/C#/curl）及 LangChain 等流行框架。

## 支持的模型/功能

- **文本生成**：`qwen4-max`、`qwen3.8-max`、`qwen3.7-plus`、`qwen-plus`、`qwen-flash` 等全系列千问模型，以及 DeepSeek、GLM、Kimi、MiniMax 等三方直供模型（详见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）。
- **多模态理解**：`qwen3-vl-plus`、`QVQ`、`Qwen-OCR` 支持图像输入；`qwen3.8-omni-flash` 支持音视频输入（详见 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)）。
- **向量嵌入**：`text-embedding-v4`、`text-embedding-v3`、`qwen3.7-text-embedding` 等，支持多语种与可调维度（详见 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)）。
- **批量处理**：支持单请求同步批处理（Batch Chat）和 JSONL 文件异步批处理（Batch File），适用于数据标注、评测等非实时场景（详见 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md) 和 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)）。
- **智能体与上下文管理**：`Responses API` 内置联网搜索、网页抓取等工具；`Conversations API` 提供会话生命周期管理；`previous_response_id` 参数简化多轮对话（详见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) 和 [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)）。
- **文件处理**：`Files API` 支持上传文档用于 Qwen-Long/Qwen-Doc-Turbo 的问答与提取，或作为 Batch 输入源（详见 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)）。

> **注意**：`Qwen-Audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议（见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）；而 `qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出（见 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)），二者能力边界存在差异，需按实际需求选型。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `base_url` | 必填，服务端点。**强烈建议使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（如 `https://dashscope.aliyuncs.com`）虽仍可用但性能与稳定性较低（见各文档“重要”提示） | `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`（Batch Chat）、`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/conversations`（Conversations） |
| `model` | 必填，模型名称。不同接口支持的模型范围不同：Chat Completions 支持最广；Responses API 对 `qwen3.8-omni-flash` 等有特殊支持；Embedding API 仅限向量模型（见各文档“支持的模型”章节） | `qwen4-max`, `text-embedding-v4`, `qwen3-vl-plus` |
| `purpose`（Files API） | 必填，文件用途标识。`file-extract`（文档分析）、`batch`（批量任务输入）、`fine-tune`（调优数据集） | `"file-extract"` |
| `enable_thinking`（Batch） | 可选，控制思考模式开关。`qwen3.8`/`qwen3.7`/`qwen3.6`/`qwen3.5` 系列默认开启，显式设为 `false` 可降低成本（见 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md) 和 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)） | `false` |
| `dimensions`（Embedding） | 可选，指定向量维度（仅 `text-embedding-v3`/`v4` 支持）。`text-embedding-v4` 默认 1024，可设为 2048/1536/768 等（见 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)） | `2048` |

## 使用方式

1. **初始化客户端**：配置 `api_key`（推荐环境变量 `DASHSCOPE_API_KEY`）和对应接口的 `base_url`。
2. **选择调用方式**：
   - **同步请求**（如 Chat Completions、Embedding）：直接调用 `create()` 方法。
   - **流式响应**：传入 `stream=True`（Python）或 `stream: true`（Node.js）。
   - **批量处理**：
     - *单请求批处理*（Batch Chat）：将 `base_url` 指向 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`，其余参数同实时 Chat。
     - *文件批处理*（Batch File）：先调用 `files.create(purpose="batch")` 上传 JSONL，再调用 `batches.create(input_file_id=..., endpoint="/v1/chat/completions")`。
   - **会话管理**：先 `conversations.create()` 创建会话，再通过 `conversations.items.create()` 添加消息，后续请求自动注入历史（见 [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)）。
3. **LangChain 集成**：优先使用 `langchain_openai.ChatOpenAI`（兼容部分模型）或 `langchain_community.chat_models.tongyi.ChatTongyi`（支持全部模型），二者均需配置 `base_url` 和 `api_key`（见 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)）。

## 限制和注意事项

- **地域绑定**：API Key 与创建地域强绑定。使用北京地域的 Key 调用弗吉尼亚 endpoint 将返回 `invalid_api_key` 错误（HTTP 401），而非密钥失效（见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）。
- **域名迁移**：华北2（北京）、新加坡、中国香港地域已启用业务空间专属域名（`{WorkspaceId}.<region>.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽兼容但**不推荐用于生产环境**，因其性能与稳定性不及新域名。
- **文件配额**：Files API 单账户最多存储 10,000 个文件，总大小上限 100 GB；单个 `file-extract` 文件最大 150 MB，`batch` 文件最大 500 MB（见 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)）。
- **Embedding 稀疏向量限制**：[OpenAI 兼容接口](../concepts/openai-compatible-api.md)**不支持** `output_type=sparse`。若需稀疏向量，请改用 DashScope 原生接口（见 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)）。
- **超时设置**：Batch Chat 默认等待 3600 秒（1 小时），可通过 SDK 客户端选项（如 Python 的 `.with_options(timeout=1800)`）或 HTTP `timeout` 参数自定义（见 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)）。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)


