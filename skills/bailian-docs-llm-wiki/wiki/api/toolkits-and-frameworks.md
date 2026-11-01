# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 OpenAI 兼容的工具包与框架，覆盖文本生成、多模态理解、向量嵌入、批量推理、对话状态管理等核心场景。所有接口均通过统一的 `compatible-mode/v1` 路径提供，开发者可复用现有 OpenAI SDK 代码，仅需调整 `base_url`、`api_key` 和模型名称即可快速迁移。各接口在功能深度、模型支持范围和上下文管理能力上存在明确分工，需按场景选型。

## 支持的模型/功能

百炼兼容接口覆盖全栈 AI 能力，但不同协议支持的模型范围差异显著：

- **Chat Completions（[OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）**：支持 Qwen 系列（`qwen3.8-max`、`qwen-plus` 等）、Qwen-VL、Qwen-Coder、Qwen-Omni、Qwen-Math，以及 DeepSeek、Kimi、GLM、MiniMax 等三方直供模型（仅限华北2北京地域）。**Qwen-Audio 不支持该协议**。
- **Responses API（[OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)）**：聚焦智能体原生能力，支持 `qwen3.8-max`、`qwen3.7-plus`、`deepseek-v4-pro`、`glm-5.3` 等最新模型，并内置联网搜索、网页抓取、代码解释器等工具；但**非阿里云直供模型仅支持基础能力，Agent 功能受限**。
- **Vision（[OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)）**：专用于多模态理解，支持 `qwen3-vl-plus`、`QVQ`、`Qwen-OCR`，其中 `QVQ` **仅支持[流式输出](../concepts/streaming-output.md)**。
- **Embedding（[OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)）**：支持 `text-embedding-v4`、`qwen3.7-text-embedding` 等向量模型，**不支持多模态 Embedding（如 `qwen3-vl-embedding`）或稀疏向量输出**。
- **Conversations（[OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)）**：用于跨设备/长时间会话管理，与 Responses API 配合使用，**不直接处理模型推理，仅维护消息上下文**。
- **Batch（[OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) 和 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)）**：前者支持 JSONL 文件批量提交（含多模态），后者为单请求同步等待模式；两者均支持 `qwen3.8-max` 等大上下文模型（最高 256K tokens），但 `qwen3.5-omni-plus` 等 Omni 模型**不支持语音输出**。

> **注意**：文档 5 和文档 6 均声明 `qwen3.8`/`qwen3.7` 系列模型默认开启思考模式，且要求 `enable_thinking` 参数必须与 `model` 同级传入；但文档 2 的 Responses API 示例中未体现该参数，实际调用时需显式添加以确保行为一致。

## 关键参数

所有兼容接口共用以下核心参数，但部分参数的语义或约束因协议而异：

- **`base_url`**：必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但**性能与稳定性较低**，强烈建议迁移。
- **`api_key`**：严格按地域绑定，北京地域 API Key 无法调用弗吉尼亚 endpoint，否则返回 `invalid_api_key` 错误。
- **`model`**：必须从对应协议支持的模型列表中选择，跨协议混用（如在 Embedding 接口传 `qwen3-vl-plus`）将失败。
- **`stream` / `stream_options`**：Chat Completions 和 Vision 接口支持流式响应；Responses API 通过 `stream_options={"include_usage": true}` 在末尾 chunk 返回 token 统计。
- **`previous_response_id`（Responses API）**：用于多轮对话，必须传入上一轮响应的顶层 `id`（UUID 格式），而非 `output` 数组内消息的 `id`。
- **`purpose`（Files API）**：上传文件时必需，值为 `file-extract`（文档分析）、`batch`（批量任务）或 `fine-tune`（调优数据集），决定后续使用场景。
- **`enable_thinking`（Batch 场景）**：控制是否启用思考模式，影响 token 成本，必须置于 JSONL `body` 顶层，不可嵌套在 `extra_body` 中。

## 使用方式

开发者可通过 OpenAI SDK（Python/Node.js/Java/Go/C#）或 HTTP 直接调用，通用流程如下：

1. **初始化客户端**：配置 `api_key`（推荐环境变量）和 `base_url`（含 `{WorkspaceId}`）；
2. **构造请求**：按协议选择方法（如 `client.chat.completions.create`、`client.responses.create`、`client.embeddings.create`）并传入参数；
3. **处理响应**：解析标准 OpenAI 格式 JSON，注意 Responses API 返回结构含 `output` 数组和 `output_text` 字段，而 Chat Completions 返回 `choices[0].message.content`；
4. **错误处理**：检查 HTTP 状态码（401/403 表示鉴权失败，404 表示路径错误）及响应体中的 `error.code`（如 `invalid_api_key`）。

LangChain 集成需区分实现：
- **`langchain_openai`**：仅支持 OpenAI 兼容协议的模型（如 `qwen-plus`），依赖 `base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"`；
- **`langchain_community`（`ChatTongyi`/`ChatAlibabaTongyi`）**：支持百炼全部模型（含非兼容协议模型），依赖 `dashscope` SDK，`base_url` 不适用。

## 限制和注意事项

- **地域与密钥强绑定**：API Key 与 `base_url` 所属地域必须一致，跨地域调用必失败，错误信息易被误判为密钥失效。
- **域名迁移强制性**：旧域名（`dashscope.aliyuncs.com`）已逐步淘汰，新功能（如 Responses API 新路径 `/compatible-mode/v1/responses`）仅在专属域名下可用，旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停止维护。
- **文件服务配额**：文件上传接口总容量上限 100 GB，文件数上限 10,000 个，超限时需手动清理。
- **模型能力边界**：Qwen-Audio 仅支持 DashScope 协议；QVQ 模型强制[流式输出](../concepts/streaming-output.md)；Embedding 接口不支持稀疏向量；Omni 模型在 Batch 场景下禁用语音输出。
- **并发与超时**：Batch Chat 默认超时 3600 秒，需在 SDK 客户端显式配置（如 Python 的 `.with_options(timeout=1800.0)`）；Conversations API 无内置超时，依赖客户端设置。
- **测试模型约束**：`batch-test-model` 仅用于链路验证，文件大小 ≤ 1 MB、行数 ≤ 100 行、并发 ≤ 2 个任务。

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


