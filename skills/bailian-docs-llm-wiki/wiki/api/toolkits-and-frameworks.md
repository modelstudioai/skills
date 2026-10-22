# toolkits and [frameworks](frameworks.md)

阿里云百炼提供一系列 OpenAI 兼容的工具包与框架接口，覆盖 Chat、Responses、Vision、Embedding、Conversations、Batch（含文件输入与 Batch Chat）、File 等核心能力，支持开发者无缝迁移现有 OpenAI 应用。所有接口均基于统一的 `compatible-mode/v1` 路径规范，并推荐使用业务空间专属域名以获得更高性能与稳定性。[OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) 是基础能力入口，其余接口在此基础上扩展特定场景。

## 支持的模型/功能

- **Chat Completions**：支持 Qwen 系列（`qwen3.8-max`, `qwen-plus`, `qwen-flash` 等）、DeepSeek、GLM、Kimi、MiniMax 等数十种文本生成模型；支持 `function_call`、流式响应、`stream_options={"include_usage": true}`；但 **Qwen-Audio 不支持 OpenAI 兼容协议**，仅支持 DashScope 原生协议。
- **Responses API**：专为智能体（Agent）设计，内置联网搜索、网页抓取、代码解释器等工具，支持 `previous_response_id` 自动上下文管理；支持模型包括 `qwen3.8-max`, `qwen3.7-plus`, `deepseek-v4-pro`, `glm-5.3`, `kimi-k3` 等；**非阿里云直供模型仅支持基础兼容能力，Agent 功能受限**。
- **Vision**：支持 `qwen3-vl-plus`, `QVQ`, `Qwen-OCR`，兼容 OpenAI 多模态消息格式（`image_url` + `text`）；其中 **QVQ 模型仅支持[流式输出](../concepts/streaming-output.md)**。
- **Embedding**：支持 `text-embedding-v1` 至 `v4`、`qwen3.7-text-embedding` 等，支持多语种及高维向量（最高 2048 维）；**多模态 Embedding 模型（如 `qwen3-vl-embedding`）不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**。
- **Conversations**：用于跨设备/长时间对话状态管理，支持创建、查询、更新、删除会话及追加消息项；需配合 Responses API 使用以实现上下文注入。
- **Batch（文件输入）**：通过 JSONL 文件批量提交请求，适用于评测、标注等非实时场景；支持文本、多模态（`qwen3-vl-plus`）、向量（`text-embedding-v4`）等模型；**测试模型 `batch-test-model` 仅限 1 MB / 100 行，且并发上限为 2 个任务**。
- **Batch Chat**：同步阻塞式批量调用，单请求最大上下文支持 256K tokens；支持 `qwen3.8-max`, `qwen3.5-omni-plus` 等；**`qwen3.5-omni-plus` 和 `qwen3.5-omni-flash` 在 Batch 场景下不支持语音输出**。
- **File**：用于上传文档（`purpose=file-extract`）、批量任务输入（`purpose=batch`）或调优数据集（`purpose=fine-tune`）；支持 TXT/DOCX/PDF/XLSX/图片等格式；单文件上限：文档分析 150 MB，Batch 输入 500 MB，调优数据集 300 MB。

> **注意**：文档 5（OpenAI兼容-Batch Chat）与文档 9（OpenAI兼容-Batch（文件输入））对 `qwen3.5-omni-plus` 的语音支持描述存在矛盾——前者称“不支持语音输出”，后者未提及限制。实际行为以 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) 中明确声明为准，即该模型在 Batch 场景下不支持语音输出。

## 关键参数

- **`base_url`**：必须替换为业务空间专属域名，格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`；北京、新加坡、中国香港地域已强制推荐迁移，旧域名（如 `dashscope.aliyuncs.com`）虽仍可用但性能与稳定性较低。
- **`api_key`**：严格按地域绑定，**北京地域 API Key 无法调用弗吉尼亚 endpoint，否则返回 `invalid_api_key` 错误**（非密钥失效，而是地域不匹配）。
- **`model`**：需从各接口支持的模型列表中精确选择，例如 Vision 接口不可用 `qwen3.8-max`，Embedding 接口不可用 `qwen3-vl-plus`。
- **`purpose`（File 接口）**：决定文件用途，取值为 `file-extract`（文档问答）、`batch`（批量推理输入）、`fine-tune`（调优数据集），三者对文件格式与大小要求不同。
- **`enable_thinking`（Batch 场景）**：`qwen3.5+` 系列模型默认开启思考模式，显式设为 `false` 可避免额外 token 成本；该参数须置于 JSONL `body` 顶层，**不可放在 `extra_body` 内**。
- **`previous_response_id`（Responses API）**：必须传入上一轮响应的顶层 `id`（UUID 格式，如 `resp_xxx`），而非 `output` 数组内消息的 `id`（如 `msg_xxx`）。

## 使用方式

- **SDK 调用**：安装 `openai` 或 `langchain_openai` 后，初始化客户端时指定 `api_key` 与 `base_url`，调用对应方法（如 `client.chat.completions.create`、`client.responses.create`、`client.files.create`）。LangChain 用户可选 `ChatOpenAI`（部分模型）或 `ChatTongyi`（全模型支持）。
- **HTTP 调用**：构造 `POST` 请求，Header 包含 `Authorization: Bearer $DASHSCOPE_API_KEY` 和 `Content-Type: application/json`，Body 为标准 OpenAI JSON 结构；Endpoint 需匹配接口类型（如 `/chat/completions`、`/responses`、`/files`、`/conversations`）。
- **地域配置**：务必确保 `base_url` 地域、`api_key` 创建地域、模型可用地域三者一致；跨地域调用将被鉴权拒绝。
- **环境变量**：强烈建议将 `DASHSCOPE_API_KEY` 配置为环境变量，避免硬编码泄露风险。
- **调试建议**：使用 `batch-test-model` 进行 JSONL 格式与链路验证；首次调用失败时，优先检查 `base_url`、`api_key` 地域匹配性及模型是否在当前接口支持列表中。[OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) 提供了完整的响应结构示例，可用于比对解析逻辑。

## 限制和注意事项

- **域名迁移强制性**：华北2（北京）、新加坡、中国香港地域的旧域名（`dashscope.aliyuncs.com` 等）虽暂未下线，但官方已明确建议迁移至业务空间专属域名，以保障服务稳定性与性能。[OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md) 中的示例仍使用旧域名，实际部署应替换为 `{WorkspaceId}` 新域名。
- **三方模型地域限制**：DeepSeek（硅基流动直供）、Kimi（月之暗面直供）等三方直供模型**仅在中国站华北2（北京）地域可用**，且需在控制台单独开通服务。
- **文件存储配额**：File 接口总文件数上限 10,000 个，总大小上限 100 GB；达到任一上限后新上传将失败，需手动清理。
- **超时与重试**：Batch Chat 默认等待超时 3600 秒（1 小时），需在 SDK 客户端显式配置 `timeout` 参数（如 Python 的 `.with_options(timeout=1800.0)`）；HTTP 调用需自行处理连接超时。
- **错误码处理**：通用错误（如 `invalid_api_key`、`404 Not Found`）需按 [错误码文档](raw/model-api-reference/preparations/error-code.md) 排查；Embedding 接口若传入 `output_type=sparse`，将返回 HTTP 200 但 embedding 字段为空，属预期行为而非错误。
- **流式响应兼容性**：QVQ 模型仅支持[流式输出](../concepts/streaming-output.md)，非流式调用将失败；其他模型流式/非流式均支持。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)


