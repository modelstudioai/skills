# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)工具包与框架，覆盖文本生成、多模态理解、向量嵌入、批量推理、会话管理等核心场景。开发者可复用现有 OpenAI SDK 代码，仅需调整 `base_url`、`api_key` 和模型名称即可快速迁移。所有兼容接口均支持主流编程语言（Python/Node.js/Java/Go/C#）及 HTTP 直调，并统一遵循 OpenAI REST API 规范。

## 支持的模型/功能

百炼 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)按能力维度划分为多个子系统，各系统支持的模型范围不同：

- **Chat Completions**：支持 Qwen 系列（`qwen4-max`、`qwen3.8-max` 等）、DeepSeek（`deepseek-v4-pro` 等）、GLM（`glm-5.3`）、Kimi（`kimi-k3`）及三方直供模型（如 SiliconFlow DeepSeek），但 [Qwen-Audio 不支持 OpenAI 兼容协议](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)，仅支持 DashScope 原生协议。
- **Responses API**：专为智能体（Agent）设计，内置联网搜索、网页抓取等工具，支持 `qwen4-max`、`qwen3.8-omni-flash`（音视频输入）、`deepseek-v4.1-flash` 等模型；非列表中模型仅支持基础能力，Agent 功能受限 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。
- **Vision（视觉）**：支持 `qwen3-vl-plus`、`QVQ`、`Qwen-OCR`，其中 QVQ 模型**仅支持[流式输出](../concepts/streaming-output.md)**，需显式启用思考模式 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。
- **Embedding（向量）**：支持 `text-embedding-v4`、`qwen3.7-text-embedding` 等，但**不支持稀疏向量输出**（`output_type=sparse` 会被忽略）；多模态 Embedding（如 `qwen3-vl-embedding`）完全不兼容 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。
- **File / Batch / Conversations**：文件接口支持 `Qwen-Long`（长文档问答）、`Qwen-Doc-Turbo`（数据提取）及 Batch 任务；Conversations API 需配合 Responses 使用以实现跨设备上下文延续。

> **注意**：文档 5（Batch 文件输入）与文档 6（Batch Chat）对同一模型（如 `qwen3.8-max`）的上下文 Token 上限描述存在矛盾——文档 5 称“最大支持 256K”，而文档 6 未明确上限值。实际使用应以控制台最新文档或 API 返回的 `400` 错误提示为准，建议在生产环境通过小规模测试验证 Token 容量。

## 关键参数

所有兼容接口共用以下核心参数，配置错误将导致鉴权失败或 404：

- `base_url`：必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- `api_key`：**严格按地域绑定**。北京地域 endpoint 必须使用北京地域创建的 API Key，跨地域调用将返回 `invalid_api_key`（HTTP 401），而非密钥失效 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- `model`：模型名称需与百炼控制台发布的名称完全一致（如 `qwen3.8-max`，非 `qwen-3.8-max`），大小写敏感。
- `workspace_id`：`{WorkspaceId}` 占位符需替换为真实 ID，可在控制台「业务空间详情」页获取。
- `enable_thinking`：仅 Batch 场景下生效，用于显式开关思考模式（默认开启），须作为 `body` 顶层参数传入，不可置于 `extra_body` 中。

## 使用方式

### SDK 调用（推荐）
1. 安装对应 SDK：`pip install -U openai`（通用）或 `pip install langchain_openai`（LangChain 集成）；
2. 初始化客户端时指定 `base_url` 和 `api_key`（强烈建议从环境变量读取）；
3. 调用对应方法：
   - Chat：`client.chat.completions.create(...)`
   - Responses：`client.responses.create(...)`（支持 `input` 字符串或 `previous_response_id` 自动续写）
   - Vision：`client.chat.completions.create(...)`（`messages` 中含 `image_url`）
   - Embedding：`client.embeddings.create(...)`
   - File：`client.files.create(file=..., purpose="file-extract")`
   - Batch：`client.batches.create(input_file_id=..., endpoint="/v1/chat/completions")`
   - Conversations：`client.conversations.create(...)` + `client.conversations.items.create(...)`

### HTTP 直调
- 方法：`POST {base_url}/{endpoint}`
- Header：`Authorization: Bearer ${DASHSCOPE_API_KEY}`，`Content-Type: application/json`
- Endpoint 示例：
  - Chat：`/chat/completions`
  - Responses：`/responses`
  - Embedding：`/embeddings`
  - Conversations：`/conversations`

### LangChain 集成
- **OpenAI 方式**：使用 `langchain_openai.ChatOpenAI`，仅支持部分模型，依赖 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md) [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)；
- **DashScope 方式**：使用 `langchain_community.chat_models.tongyi.ChatTongyi`，支持全部百炼模型（含部署模型），需安装 `dashscope` 包。

## 限制和注意事项

- **地域隔离**：API Key 与 endpoint 地域必须严格匹配，跨地域调用必然失败，无例外。
- **文件配额**：文件接口总存储上限为 10,000 个文件 / 100 GB，达上限后上传失败，需手动清理。
- **Batch 超时**：Batch Chat 默认等待 3600 秒（1 小时），超时断连；Batch 文件处理最长等待时间由 `completion_window` 参数控制（如 `"24h"`）。
- **模型能力差异**：`qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出；`Qwen-VL` 系列在 Responses API 中不适用，需用 Vision 接口。
- **调试建议**：遇到 `401` 错误，优先检查地域匹配；`404` 错误，确认 `base_url` 路径（如 Responses API 已废弃 `/api/v2/.../responses` 老路径）；`422` 错误，验证 `model` 名称是否拼写正确。

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


