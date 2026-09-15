# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 OpenAI 兼容的工具包与框架接口，覆盖文本生成、视觉理解、文件处理、批量推理、对话管理、向量嵌入等核心场景。开发者可复用现有 OpenAI SDK 代码，仅需调整 `base_url`、`api_key` 和 `model` 即可快速迁移；同时支持 LangChain 等主流生态框架集成，降低大模型应用开发门槛。

## 支持的模型/功能

百炼兼容接口支持三大类能力：  
- **通用文本生成**：包括 `qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash` 等全系 Qwen 文本模型，以及 DeepSeek（v4-pro/v4-flash）、GLM-5、Kimi-K3 等三方直供模型（仅限华北2北京地域）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；  
- **多模态理解**：`qwen-vl-plus`、`qwen-vl-flash`、`QVQ`、`Qwen-OCR` 支持图像输入与结构化输出 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)；  
- **专用能力接口**：`completions` 接口专用于代码补全（FIM 填空），当前仅支持 `qwen-coder-turbo` 模型 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)；`Responses API` 内置联网搜索、网页抓取等智能体原生工具，显著提升复杂任务效果；`Conversations API` 提供会话级上下文管理，支持跨设备延续对话。

> **注意**：`Qwen-Audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；`qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出，且 `qwen3.5-omni-flash` 同样受限。

## 关键参数

所有兼容接口共用以下关键参数配置：
- `base_url`：必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（如 `https://dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低；  
- `api_key`：严格按地域绑定，北京地域 API Key 不可用于调用弗吉尼亚 endpoint，否则返回 `invalid_api_key` 错误；  
- `model`：需从各接口明确支持的模型列表中选择，例如 `Responses API` 仅支持 `qwen3.8-max` 等特定版本，而 `completions` 接口仅支持 `qwen-coder-turbo`；  
- `stream` 与 `stream_options`：流式调用时，`stream_options={"include_usage": true}` 可在最后一 chunk 返回 token 统计；  
- `dimensions`：仅 `text-embedding-v3/v4` 支持该参数，用于指定向量维度；  
- `enable_thinking`：对 `qwen3.5+` 系列模型，该参数需作为 `body` 顶层字段显式传入（不可置于 `extra_body`），控制思考模式开关以优化成本。

## 使用方式

### 接口调用路径
| 接口类型 | SDK 调用方法 | HTTP Endpoint |
|----------|--------------|----------------|
| Chat Completions | `client.chat.completions.create(...)` | `POST /chat/completions` |
| Responses | `client.responses.create(...)` | `POST /responses` |
| Conversations | `client.conversations.create(...)` | `POST /conversations` |
| Embeddings | `client.embeddings.create(...)` | `POST /embeddings` |
| Files | `client.files.create(...)` | `POST /files` |
| Batch (file-based) | `client.batches.create(...)` | `POST /batches` |
| Batch (sync chat) | `client.chat.completions.create(...)` + `batch.dashscope.aliyuncs.com` | `POST /chat/completions` |

### 开发者集成建议
- **LangChain 集成**：推荐优先使用 `langchain_openai.ChatOpenAI`（兼容部分模型）或 `langchain_community.chat_models.tongyi.ChatTongyi`（支持全部百炼模型）；Java 开发者应选用 `langchain4j-open-ai` 并确保 Java 17+ 环境 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)；  
- **批量处理**：高吞吐、低时效性场景（如数据标注）应选用 `Batch Chat`（单请求同步等待）或 `Batch File`（JSONL 文件异步提交），后者成本更低且支持 256K 上下文；  
- **文件上传**：`purpose` 参数决定用途：`file-extract`（文档问答）、`batch`（批量推理输入）、`fine-tune`（调优数据集），对应不同格式与大小限制（如 `file-extract` 单文件 ≤150 MB，`batch` 单文件 ≤500 MB）。

## 限制和注意事项

- **地域与域名强绑定**：API Key、`base_url`、模型开通地域三者必须一致；新加坡地域模型不可用北京 API Key 调用；  
- **模型能力差异**：非阿里云直供模型（如第三方 DeepSeek）在 `Responses API` 下 Agent 能力（内置工具）受限；`Qwen-VL` 系列模型在流式调用时行为与纯文本模型不同，需注意响应结构；  
- **参数兼容性陷阱**：`completions` 接口不支持 `messages` 字段，仅接受 `prompt` 字符串；`Embedding` 接口传入 `output_type=sparse` 将静默返回空 embedding，而非报错；  
- **超时与重试**：`Batch Chat` 默认超时 3600 秒，需在 SDK 客户端显式配置（如 Python 的 `.with_options(timeout=1800.0)`）；`Conversations API` 中 `previous_response_id` 必须传入上一轮响应的顶层 `id`（UUID 格式），而非 `output` 数组内消息的 `id`；  
- **配额与生命周期**：文件存储上限为 10000 个文件 / 100 GB，无自动过期机制；`Conversations` 中 `items` 最多 20 条，`metadata` 键值对最多 16 对。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)


