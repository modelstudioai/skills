# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 OpenAI 兼容的工具包与框架接口，覆盖文本生成、视觉理解、向量嵌入、文件处理、批量推理及会话管理等核心场景。开发者可复用现有 OpenAI SDK 代码，仅需调整 `base_url`、`api_key` 和 `model` 参数即可快速迁移。所有接口均支持主流编程语言（Python/Node.js/Java/Go/C#/Bash）及 HTTP 直调。

## 支持的模型/功能

- **文本生成**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash` 等全系 Qwen 大模型，以及 `deepseek-v4-pro`、`glm-5.3`、`kimi-k3` 等第三方直供模型 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)；  
- **视觉理解**：`qwen3-vl-plus`、`qwen3-vl-flash`、`QVQ`、`Qwen-OCR`，支持图像/视频输入与多模态推理 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)；  
- **向量嵌入**：`text-embedding-v4`、`qwen3.7-text-embedding`、`qwen3.7-text-embedding-flash`，支持最高 128K [Token](../concepts/token.md) 单行输入与多维度输出 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)；  
- **文档与长上下文**：`Qwen-Long`（长文档问答）、`Qwen-Doc-Turbo`（结构化数据提取），依赖文件上传接口预处理 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)；  
- **代码补全**：`qwen-coder-turbo` 专用于 FIM（Fill-in-the-Middle）场景，支持前缀+后缀联合补全；  
- **批量处理**：支持单请求同步批处理（`Batch Chat`）与 JSONL 文件异步批处理（`Batch File`），成本降低 50%；  
- **会话管理**：`Conversations API` 提供跨设备上下文持久化能力，配合 `Responses API` 实现自动历史注入。

> **注意**：`Qwen-Audio` 不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；`Qwen-Coder` 系列模型在 `completions` 接口下仅支持 `qwen-coder-turbo`，其他 coder 模型未被明确列出 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。

## 关键参数

| 参数 | 类型 | 说明 | 适用接口 |
|------|------|------|----------|
| `base_url` | string | 必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）已不推荐 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) | 所有兼容接口 |
| `model` | string | 模型名需严格匹配文档列表，例如 `qwen3.8-max`、`qwen3-vl-plus`、`text-embedding-v4`；三方模型（如 `deepseek-v4-pro`）仅限华北2（北京）地域可用 | 所有兼容接口 |
| `enable_thinking` | boolean | 控制是否启用思考模式（产生 reasoning tokens），默认 `true`；必须作为 JSONL 请求体顶层字段传入，不可置于 `extra_body` 内 | Batch 接口 |
| `previous_response_id` | string | `Responses API` 中用于自动关联上下文的上一轮响应 ID（顶层 `id`，非 `output` 数组内 `msg_xxx`） | Responses API |
| `purpose` | string | 文件上传时必需，取值为 `file-extract`（文档分析）、`batch`（批量任务）、`fine-tune`（调优数据集） | 文件接口 |

## 使用方式

1. **环境准备**：获取对应地域的 API Key 并配置至环境变量 `DASHSCOPE_API_KEY`，安装 OpenAI SDK（`pip install -U openai`）或 LangChain 适配器（`pip install langchain_openai`）；  
2. **端点配置**：将 SDK 的 `base_url` 设为业务空间专属地址（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），`{WorkspaceId}` 需替换为控制台获取的实际 ID；  
3. **接口调用**：
   - 文本对话：`client.chat.completions.create(...)`（Chat API）或 `client.responses.create(...)`（Responses API）；  
   - 视觉理解：`messages` 中 `content` 数组包含 `{"type": "image_url", "image_url": {"url": "..."} }`；  
   - 向量嵌入：`client.embeddings.create(model="text-embedding-v4", input="...", dimensions=1024)`；  
   - 文件上传：`client.files.create(file=Path("doc.pdf"), purpose="file-extract")`；  
   - 批量处理：`client.batches.create(input_file_id="file-batch-xxx", endpoint="/v1/chat/completions", completion_window="24h")`；  
   - 会话管理：先 `client.conversations.create(...)` 创建会话，再通过 `conversation_id` 调用 `client.conversations.items.create(...)` 追加消息。  

## 限制和注意事项

- **地域绑定**：API Key 与 `base_url` 地域必须严格一致（如北京 Key 只能调北京 endpoint），跨地域调用将返回 `401 invalid_api_key` 错误；  
- **文件配额**：文件存储上限为 10,000 个文件或 100 GB 总大小，超限时上传失败；单文件大小限制因 `purpose` 而异：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB；  
- **Batch 时效性**：`Batch Chat` 同步等待最长 3600 秒（1 小时），超时断连；`Batch File` 异步任务最长等待 24 小时；  
- **Embedding 稀疏向量**：[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)不支持 `output_type=sparse`，传入该参数将返回空 embedding 结果；  
- **旧路径弃用**：`/api/v2/apps/protocols/compatible-mode/v1/responses` 和 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 已停止维护，必须迁移至 `/compatible-mode/v1/{endpoint}`；  
- **模型能力差异**：非阿里云直供模型（如部分第三方 DeepSeek、Kimi）仅支持基础 Chat Completions 功能，Agent 工具调用、思考模式等高级能力受限 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。

## 来源文档

- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)


