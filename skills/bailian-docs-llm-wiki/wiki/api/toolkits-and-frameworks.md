# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 OpenAI 兼容的接口协议，覆盖文本生成、视觉理解、向量嵌入、批量处理、会话管理等核心场景。开发者可复用现有 OpenAI SDK 和工具链，仅需调整 `base_url`、`api_key` 和 `model` 参数即可快速迁移，无需重写业务逻辑。所有兼容接口均支持主流编程语言（Python/Node.js/Java/Go/C#/JS）及 LangChain 等主流框架集成。

## 支持的模型/功能

百炼 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)覆盖以下能力矩阵：

- **文本生成**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.6-flash`、`deepseek-v4-pro`、`glm-5.3`、`kimi-k3` 等全系列千问及第三方直供模型，支持 `chat.completions`、`responses`、`conversations` 三类交互范式 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；
- **多模态理解**：`qwen3-vl-plus`、`qwen3.5-omni-plus`、`qwen-vl-ocr` 等模型支持图像/视频/文档输入，兼容 OpenAI Vision 规范 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)；
- **向量嵌入**：`text-embedding-v4`、`qwen3.7-text-embedding`、`text-embedding-v2` 等模型支持文本向量化，但**不支持稀疏向量输出**（传入 `output_type=sparse` 将返回空 embedding）[OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)；
- **长上下文与文档处理**：`qwen-long`、`qwen-doc-turbo` 通过文件 ID 实现文档问答与数据提取，依赖 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md) 上传预处理文件；
- **批量推理**：支持两种模式——单请求同步批处理（`/chat/completions` + `batch.dashscope.aliyuncs.com` endpoint）和 JSONL 文件异步批处理（`/batches`），后者成本降低 50% [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md) 与 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。

> **注意**：`qwen3.8-omni-flash` 仅支持音视频输入生成文本回复，不支持纯文本 `chat.completions` 调用；而 `qwen-audio` 完全不支持 OpenAI 兼容协议，必须使用 DashScope 原生接口 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。

## 关键参数

所有 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)共用以下核心参数：

- `base_url`：**必须显式配置**为业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名 `dashscope.aliyuncs.com` 已逐步停用，性能与稳定性无保障；
- `api_key`：按地域绑定，北京地域 API Key **不可用于调用弗吉尼亚 endpoint**，否则返回 `invalid_api_key` 错误 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；
- `model`：严格匹配文档中列出的模型名（如 `qwen3.8-max`），大小写敏感，拼写错误将导致 404；
- `enable_thinking`：对 `qwen3.5+` 系列模型，该参数控制思考模式开关（`true`/`false`），默认开启，开启后产生额外 `reasoning_tokens` 成本，**必须置于 JSONL 请求体顶层，不可嵌套在 `extra_body` 中** [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)；
- `previous_response_id`：仅 `responses` API 支持，用于自动关联上下文，**必须传入上一轮响应的顶层 `id`（UUID 格式），而非 `output` 数组内消息的 `id`** [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。

## 使用方式

### 1. 初始化客户端
```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
```

### 2. 按场景选择接口
| 场景 | 接口路径 | 示例调用 |
|--------|-----------|------------|
| 实时对话 | `/chat/completions` | `client.chat.completions.create(model="qwen-plus", messages=[...])` |
| 智能体交互（内置工具） | `/responses` | `client.responses.create(model="qwen3.8-max", input="搜索最新AI论文")` |
| 长期会话管理 | `/conversations` + `/items` | `client.conversations.create()` → `client.conversations.items.create(conv_id, items=[...])` |
| 批量异步处理 | `/batches` | `client.batches.create(input_file_id="file-batch-xxx", endpoint="/v1/chat/completions")` |
| 向量嵌入 | `/embeddings` | `client.embeddings.create(model="text-embedding-v4", input="hello")` |

### 3. LangChain 集成
- **OpenAI 兼容层**：使用 `langchain_openai.ChatOpenAI`，仅支持部分模型（如 `qwen-plus`），适合快速验证 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)；
- **DashScope 原生层**：使用 `langchain_community.chat_models.tongyi.ChatTongyi`，支持全部模型（含部署模型）及多模态输入，推荐生产环境使用 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

## 限制和注意事项

- **地域一致性**：API Key、`base_url` 地域、模型可用性三者必须严格一致。例如新加坡地域 `base_url` 仅支持 `qwen3.8-max`、`qwen3.7-plus`，不支持 `qwen3.5-flash` [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)；
- **文件上传配额**：`files.create()` 总数上限 10000 个，总大小上限 100 GB，超限后上传失败，需主动清理 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)；
- **[Token](../concepts/token.md) 限制**：`qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出；`qwen3.8-max` 等大模型单次请求最大上下文为 256K tokens，超出将被截断 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)；
- **过时路径**：`/api/v2/apps/protocols/compatible-mode/v1/responses` 和 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 已废弃，必须迁移到 `/compatible-mode/v1/{responses,conversations}` [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)；
- **流式响应差异**：`responses` API 的 `output_text` 字段仅在非流式调用中存在，流式调用需解析 `output` 数组中的 `type="message"` 条目 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。

## 来源文档

- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)


