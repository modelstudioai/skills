# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，覆盖文本生成、视觉理解、向量嵌入、批量处理、对话管理等核心场景，支持主流 SDK（如 OpenAI Python/Node.js SDK、LangChain）无缝集成。所有兼容接口均基于统一的 `compatible-mode/v1` 路径设计，通过切换 `base_url` 和 `model` 即可快速迁移现有代码。

## 支持的模型/功能

- **文本与智能体**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash` 等全系 Qwen 文本模型；`deepseek-v4-pro`、`glm-5.3`、`kimi-k3` 等三方直供模型（仅限华北2北京地域）；[OpenAI Responses API](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) 提供内置联网搜索、网页抓取等 Agent 工具能力。
- **多模态**：`qwen3-vl-plus`、`QVQ`、`Qwen-OCR` 支持图像理解；`qwen3.8-omni-flash` 支持音视频输入；`qwen3.5-omni-plus` 支持全模态推理（但不支持语音输出）。
- **向量嵌入**：`text-embedding-v4`、`qwen3.7-text-embedding` 等 6 款 Embedding 模型，支持 64–2048 维度可选；[Embedding 接口](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md) 不支持稀疏向量输出（`output_type=sparse` 会返回空结果）。
- **文件与批量**：`Qwen-Long` 和 `Qwen-Doc-Turbo` 支持文档问答；`batch-test-model` 用于链路验证；[Batch 文件接口](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) 支持 JSONL 格式批量提交，费用为实时调用的 50%。
- **对话管理**：[Conversations API](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md) 提供会话生命周期管理（创建、更新、删除、追加消息），配合 Responses API 的 `previous_response_id` 实现跨设备上下文延续。

> **注意**：`Qwen-Audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；`qwen3.8-omni-flash` 在 Responses API 中支持音视频输入，但在 Chat Completions 兼容接口中未明确说明该能力，需以实际调用为准。

## 关键参数

- **`base_url`**：必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（如 `https://dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低。
- **`api_key`**：严格按地域绑定，北京地域 API Key 无法调用弗吉尼亚 endpoint，否则返回 `invalid_api_key` 错误码 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- **`model`**：需从各接口支持的模型列表中精确选择，例如 Vision 接口仅支持 `qwen3-vl-plus`、`QVQ`、`Qwen-OCR`；Embedding 接口不支持 `qwen3-vl-embedding` 等多模态向量模型 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。
- **`enable_thinking`**：在 Batch 场景下，`qwen3.8`/`qwen3.7`/`qwen3.6`/`qwen3.5` 系列模型默认开启思考模式，需显式设置该参数（`true`/`false`）控制 token 成本，且必须置于 JSONL 请求体顶层，不可放在 `extra_body` 内 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。
- **`previous_response_id`**：Responses API 多轮对话必需，须传入上一轮响应的顶层 `id`（UUID 格式），而非 `output` 数组内消息的 `id` [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。

## 使用方式

- **SDK 调用**：安装 `openai` 或 `langchain_openai` 后，初始化客户端时指定 `base_url` 和 `api_key`，调用对应方法（如 `client.chat.completions.create`、`client.responses.create`、`client.conversations.create`）。LangChain 集成推荐优先使用 `ChatOpenAI`（兼容部分模型）或 `ChatTongyi`（支持全部百炼模型） [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。
- **HTTP 调用**：构造标准 REST 请求，`Authorization: Bearer $DASHSCOPE_API_KEY`，`Content-Type: application/json`，endpoint 与 SDK `base_url` + 路径一致（如 `/chat/completions`、`/responses`、`/conversations`）。
- **文件操作**：`purpose` 参数决定用途——`file-extract`（文档分析）、`batch`（批量任务输入）、`fine-tune`（调优数据集），各用途有独立文件大小限制（150 MB / 500 MB / 300 MB） [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。
- **流式响应**：所有 Chat 接口均支持 `stream=True`，Vision 模型（如 QVQ）**仅支持[流式输出](../concepts/streaming-output.md)**；Responses API 流式需设置 `stream_options={"include_usage": True}` 获取 token 统计。

## 限制和注意事项

- **地域隔离**：API Key 与 endpoint 地域强绑定，跨地域调用必失败；德国（法兰克福）、日本（东京）等新地域仅在 Responses 和 Conversations API 中提供 endpoint，Chat Completions 和 Vision 接口文档未覆盖。
- **模型能力差异**：非阿里云直供模型（如三方 DeepSeek、Kimi）在 Responses API 中 Agent 能力受限；`qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出。
- **路径弃用**：Responses API 旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses`、Conversations API 旧路径 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 已停止维护，必须迁移到 `/compatible-mode/v1/{resource}` [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。
- **配额与超时**：Batch Chat 默认超时 3600 秒（1 小时），需在客户端显式配置 timeout（如 Python SDK 的 `.with_options(timeout=1800.0)`）；文件存储上限为 10000 个文件 / 100 GB，达上限后上传失败。
- **安全实践**：强烈建议将 `DASHSCOPE_API_KEY` 配置为环境变量，避免硬编码；生产环境禁用 `curl` 或 SDK 示例中的明文 key 写法。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)


