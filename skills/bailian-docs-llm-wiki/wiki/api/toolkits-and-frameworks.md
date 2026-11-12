# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)工具包与框架，覆盖文本生成、多模态理解、向量嵌入、批量推理、会话管理等核心场景。开发者可复用现有 OpenAI SDK 代码，仅需调整 `base_url`、`api_key` 和模型名称即可快速迁移。所有接口均支持主流编程语言（Python/Node.js/Java/Go/C#）及 HTTP 直调。

## 支持的模型/功能

- **文本与对话**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash` 等全系列 Qwen 文本模型，支持 `chat.completions`、`responses`、`conversations` 三类接口；其中 `responses` API 内置联网搜索、网页抓取、代码解释器等智能体原生能力 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。
- **多模态**：`qwen3-vl-plus`、`QVQ`、`Qwen-OCR` 支持视觉理解；`qwen3.8-omni-flash` 支持音视频输入；`qwen3.5-omni-plus` 支持全模态推理 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。
- **向量嵌入**：`text-embedding-v4`、`qwen3.7-text-embedding` 等模型支持文本向量化，但**不支持稀疏向量输出**（传入 `output_type=sparse` 将返回空 embedding）[OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。
- **文件与批量处理**：`Qwen-Long`、`Qwen-Doc-Turbo` 支持文档问答；`batch-test-model` 用于链路验证；`qwen3.8-max` 等模型在 Batch 场景下支持最高 256K 上下文 [Token](../concepts/token.md) [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。
- **LangChain 集成**：通过 `langchain_openai`（部分模型）或 `langchain_community.chat_models.tongyi`（全模型支持）接入，后者还支持部署后模型调用 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

> **注意**：`Qwen-Audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；而 `qwen3.8-omni-flash` 在 `responses` 接口下支持音视频输入，但在 `chat.completions` 下未明确声明支持——二者能力边界需按接口文档分别确认。

## 关键参数

- **`base_url`**：必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低。`{WorkspaceId}` 需从控制台业务空间详情页获取。
- **`api_key`**：严格按地域绑定。北京地域 API Key 不可用于调用弗吉尼亚 endpoint，否则返回 `invalid_api_key` 错误（非密钥失效，而是地域不匹配）[OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- **`model`**：必须从各接口文档明确列出的支持列表中选择。例如 `responses` API 仅支持 `qwen3.8-max`、`deepseek-v4-pro` 等特定模型，非列表内模型将缺失 Agent 能力 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。
- **`enable_thinking`**：对 `qwen3.5+` 系列模型为顶层 `body` 参数（与 `model` 同级），不可置于 `extra_body` 中；默认开启，关闭可降低成本 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。
- **`previous_response_id`**：用于 `responses` 多轮对话，必须传入上一轮响应的顶层 `id`（UUID 格式 `resp_xxx`），而非 `output` 数组内消息的 `msg_xxx` ID [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。

## 使用方式

- **SDK 调用**：统一使用 OpenAI 官方 SDK（如 `openai==1.49.0`），仅替换 `base_url` 和 `model`。例如：
  - `chat.completions.create()` → 标准流式/非流式对话；
  - `responses.create()` → 自动上下文管理 + 内置工具；
  - `conversations.create()` → 创建会话并注入初始消息；
  - `files.create(purpose="file-extract")` → 上传文档供 Qwen-Long 分析 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。
- **HTTP 调用**：直接构造 POST 请求，`Authorization: Bearer $DASHSCOPE_API_KEY`，`Content-Type: application/json`，endpoint 与 SDK `base_url` + 路径一致（如 `/v1/chat/completions`）。
- **LangChain 集成**：优先选用 `ChatTongyi`（Java/Python）或 `ChatAlibabaTongyi`（JS）以获得全模型支持；若仅需 OpenAI 兼容模型，可用 `ChatOpenAI` 并配置 `base_url` [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。
- **Batch 场景**：
  - 文件批量：上传 `purpose="batch"` 的 JSONL 文件，每行含 `custom_id`、`method`、`url`、`body`；
  - 单请求批量：将 `base_url` 切换为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`，其余参数不变 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。

## 限制和注意事项

- **地域隔离**：API Key 与 endpoint 地域强绑定，跨地域调用必失败，错误码恒为 `invalid_api_key` [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- **文件配额**：文件服务总容量上限 100 GB，最多 10,000 个文件；达上限后上传失败，需手动清理 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。
- **模型能力差异**：三方直供模型（如 SiliconFlow DeepSeek）仅在北京地域可用，且需在控制台单独开通服务；`qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- **路径弃用**：`/api/v2/apps/protocols/compatible-mode/v1/responses` 和 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 已停止维护，必须迁移到 `/compatible-mode/v1/responses` 和 `/compatible-mode/v1/conversations` [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。
- **超时设置**：Batch Chat 默认等待 3600 秒，需在 SDK 客户端显式配置（如 Python 的 `.with_options(timeout=1800.0)`），HTTP 调用需设置客户端超时 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。

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


