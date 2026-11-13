# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，覆盖文本生成、视觉理解、向量嵌入、文件管理、批量推理及会话状态管理等核心场景。开发者可复用现有 OpenAI SDK 代码，仅需调整 `base_url`、`api_key` 和 `model` 参数即可快速迁移。所有接口均支持主流编程语言（Python/Node.js/Java/Go/C#/JS），并提供业务空间专属域名以提升稳定性与性能。

## 支持的模型/功能

- **文本生成**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash` 等全系列 Qwen 模型，以及 DeepSeek、GLM、Kimi、MiniMax 等三方直供模型（详见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）；其中 `qwen3.8-omni-flash` 支持音视频输入处理 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。
- **视觉理解**：`qwen3-vl-plus`、`QVQ`、`Qwen-OCR`，支持图像/视频 URL 或 Base64 编码输入，兼容 OpenAI Vision 规范 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。
- **向量嵌入**：`text-embedding-v4`、`qwen3.7-text-embedding`、`qwen3.7-text-embedding-flash` 等，支持多语种与可配置维度，但**不支持稀疏向量输出**（传入 `output_type=sparse` 将返回空 embedding）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。
- **文档与批量处理**：`Qwen-Long`（长文档问答）、`Qwen-Doc-Turbo`（结构化数据提取）、`batch-test-model`（链路验证）；Batch 接口支持单请求同步模式（Batch Chat）和 JSONL 文件异步模式（Batch File）。
- **会话管理**：`Conversations API` 提供跨设备上下文持久化能力，配合 `Responses API` 的 `previous_response_id` 可实现无状态对话延续。

> **注意**：`Qwen-Audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；该限制在 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) 中明确说明，但未在其他音频相关文档中同步，需特别注意。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `base_url` | 必须使用业务空间专属域名，格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`；旧域名（如 `dashscope.aliyuncs.com`）虽仍可用，但官方强烈建议迁移 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) | `https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `model` | 模型名需严格匹配支持列表，不同接口支持范围不同：`Responses API` 支持 `qwen3.8-omni-flash`，而 `Vision API` 仅支持 `qwen3-vl-plus` 等视觉专用模型 | `qwen3.8-max`, `qwen3-vl-plus`, `text-embedding-v4` |
| `purpose`（文件接口） | 决定文件用途，取值为 `file-extract`（文档分析）、`batch`（批量任务）、`fine-tune`（调优数据集） | `"file-extract"` |
| `enable_thinking`（Batch 场景） | 控制是否启用思考模式；`qwen3.5+` 系列默认开启，**必须作为 `body` 顶层参数传入，不可置于 `extra_body` 中** | `{"model":"qwen3.7-plus","enable_thinking":false,...}` |
| `previous_response_id`（Responses API） | 用于多轮对话上下文关联，**必须传入上一轮响应的顶层 `id`（UUID 格式），而非 `output` 数组内消息的 `id`** | `"0c842a11-c7d1-45da-b7ec-4e668c389xxx"` |

## 使用方式

- **SDK 调用**：统一使用 OpenAI SDK（v1.x），通过 `base_url` 切换服务端点。LangChain 用户可选 `langchain_openai`（部分模型）或 `langchain-community` + `dashscope`（全模型支持）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。
- **HTTP 调用**：所有接口均提供标准 RESTful endpoint，如：
  - Chat：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`
  - Responses：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses`
  - Embeddings：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings`
  - Conversations：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/conversations`
- **文件上传**：通过 `/files` 接口上传，`purpose` 决定后续用途；上传后获得 `file_id`，可用于 `Qwen-Long` 问答、`Batch` 任务或调优训练。
- **批量处理**：
  - **Batch Chat**：单请求同步等待，适用于低频高延迟容忍场景，endpoint 为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`。
  - **Batch File**：JSONL 文件异步提交，适用于大规模批处理，支持 `qwen3.5-omni-plus` 等 256K 上下文模型，但该模型**不支持语音输出**。

## 限制和注意事项

- **地域绑定**：API Key 与 `base_url` 所属地域必须严格一致（如北京地域 Key 不能调用弗吉尼亚 endpoint），否则返回 `invalid_api_key` 错误，而非权限不足提示。
- **文件配额**：百炼存储空间上限为 **10,000 个文件** 或 **100 GB 总大小**，超出后上传失败；需主动清理旧文件释放配额。
- **模型能力差异**：
  - 非阿里云直供模型（如 SiliconFlow DeepSeek）**仅在中国站华北2（北京）地域可用**，且需在控制台手动开通服务。
  - `qwen3.8-omni-flash` 仅在 `Responses API` 中支持音视频输入，`Chat API` 不支持。
- **超时与重试**：
  - Batch Chat 默认超时 3600 秒（1 小时），可通过客户端 `timeout` 参数调整（如 Python SDK 的 `.with_options(timeout=1800.0)`）。
  - `Conversations API` 的 `items` 创建接口每次最多添加 20 条消息，`metadata` 最多 16 对键值对。
- **错误处理**：[OpenAI 兼容接口](../concepts/openai-compatible-api.md)返回标准 OpenAI 错误格式（含 `code`/`message`），但部分底层错误码需查 [错误码文档](raw/model-api-reference/preparations/error-code.md) 解析。

## 来源文档

- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)


