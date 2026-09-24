# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)及配套工具链，覆盖文本生成、视觉理解、[向量嵌入](../concepts/vector-embedding.md)、批量处理、会话管理等核心场景。开发者可复用现有 OpenAI SDK 代码，仅需调整 `base_url`、`api_key` 和模型名即可快速迁移；同时支持 LangChain 等主流框架集成，降低大模型应用开发门槛。

## 支持的模型/功能

百炼兼容接口覆盖以下能力维度：

- **通用文本生成**：通过 `chat/completions`（[OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）和 `responses`（[OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)）支持 Qwen 系列（如 `qwen3.8-max`, `qwen3.7-plus`）、DeepSeek、GLM、Kimi 等数十种模型，其中 `responses` 接口额外提供内置联网搜索、网页抓取、代码解释器等智能体原生能力。
- **视觉理解**：`qwen-vl-plus`、`qwen-vl-flash`、`qwen-ocr` 等模型通过 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md) 支持多模态输入（文本+图像 URL 或 base64），适用于图文问答、OCR 场景。
- **文本补全**：`completions` 接口专用于代码补全与内容续写，当前仅支持 `qwen-coder-turbo` 模型，支持前缀补全（Prefix）与前后缀填充（FIM）两种模式。
- **[向量嵌入](../concepts/vector-embedding.md)**：`text-embedding-v4`、`qwen3.7-text-embedding` 等模型通过 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md) 提供多语种稠密向量，支持自定义维度（如 `dimensions=1024`），但**不支持稀疏向量输出**（传入 `output_type=sparse` 将返回空 embedding）。
- **文件与批量处理**：`files` 接口支持上传文档用于 Qwen-Long/Qwen-Doc-Turbo 的问答或作为 Batch 输入；`batch` 接口支持单请求同步等待（[OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)）或 JSONL 文件异步批量处理（[OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)），成本为实时调用的 50%。
- **会话管理**：`conversations` 接口（[OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)）提供跨设备上下文持久化能力，配合 `responses` 的 `previous_response_id` 可实现无状态对话延续。

> **注意**：`qwen-audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议（见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）；`completions` 接口当前**仅限华北2（北京）地域**，且仅支持 `qwen-coder-turbo`（见 [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)），与其他接口的地域覆盖范围不一致。

## 关键参数

所有 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)共用以下关键参数，行为与 OpenAI 官方一致，但存在百炼特有约束：

- **`base_url`**：必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低。`{WorkspaceId}` 需从控制台获取。
- **`api_key`**：严格按地域绑定，北京 API Key 无法调用弗吉尼亚 endpoint，否则返回 `invalid_api_key`（HTTP 401），而非权限错误（见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）。
- **`model`**：必须使用文档明确列出的模型名（如 `qwen3.8-max`），非列表中模型可能缺失 Agent 能力或完全不可用。
- **`stream` & `stream_options`**：流式响应支持 `{"include_usage": true}` 在末尾 chunk 返回 token 统计，但 `qwen-vl-plus` 等视觉模型[流式输出](../concepts/streaming-output.md)格式与纯文本略有差异（见 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)）。
- **`enable_thinking`**：对 `qwen3.5+` 系列模型，默认开启思考模式，显式设置 `enable_thinking=false` 可关闭以降低成本（见 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) 和 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)）。
- **`dimensions`**：仅 `text-embedding-v3`/`v4` 支持，用于指定向量维度（如 `1024`），其他 embedding 模型忽略该参数。

## 使用方式

### SDK 集成
- **OpenAI SDK**：推荐方式，安装 `openai>=1.0.0` 后，初始化 `OpenAI` 客户端时传入 `base_url` 和 `api_key` 即可调用所有兼容接口（`chat.completions`, `embeddings`, `files`, `batches`, `conversations`, `responses`）。示例：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  # 调用 chat
  client.chat.completions.create(model="qwen-plus", messages=[...])
  # 调用 embedding
  client.embeddings.create(model="text-embedding-v4", input="hello")
  # 调用 batch
  client.batches.create(input_file_id="file-id", endpoint="/v1/chat/completions", ...)
  ```

- **LangChain**：提供双路径支持：
  - `langchain_openai.ChatOpenAI`：仅支持 OpenAI 兼容模型子集（如 `qwen-plus`），配置同上。
  - `langchain_community.chat_models.tongyi.ChatTongyi`：支持百炼全部文本模型（含部署模型），需安装 `dashscope` 包并使用 `dashscope_api_key` 参数（见 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)）。

### HTTP 直连
所有接口均提供标准 RESTful endpoint，例如：
- Chat: `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`
- Embedding: `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings`
- Files: `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/files`
- Conversations: `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/conversations`
- Responses: `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses`

请求头需包含 `Authorization: Bearer $DASHSCOPE_API_KEY` 和 `Content-Type: application/json`。

## 限制和注意事项

- **地域隔离**：API Key 与 endpoint 地域强绑定，跨地域调用必失败（HTTP 401），且不同地域支持的模型列表存在差异（如三方模型仅北京可用），务必在对应地域控制台创建 Key 并确认模型可用性。
- **域名迁移强制要求**：旧域名（`dashscope.aliyuncs.com`）已逐步淘汰，新项目必须使用 `{WorkspaceId}.<region>.maas.aliyuncs.com` 格式；`responses` 和 `conversations` 接口的旧路径（`/api/v2/apps/...`）已停止维护，必须迁移到 `/compatible-mode/v1/{endpoint}`。
- **功能边界**：
  - `completions` 接口不支持后缀补全（仅 Prefix/FIM），且仅限北京地域。
  - `qwen-audio` 不支持任何 OpenAI 兼容协议。
  - `embedding` 接口不支持 `output_type=sparse`，传入将导致 embedding 字段为空。
  - `batch` 接口对 `qwen3.5-omni-plus` 等模型禁用语音输出。
- **配额与超时**：
  - `files` 接口总存储上限 100 GB / 10,000 文件，无自动过期。
  - `batch` 同步调用（Batch Chat）默认超时 3600 秒，需在 SDK 中显式配置（如 Python 的 `.with_options(timeout=1800)`）。
- **安全实践**：强烈建议将 `DASHSCOPE_API_KEY` 配置为环境变量，避免硬编码到源码中（所有文档均强调此风险）。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)


