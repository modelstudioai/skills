# toolkits and [frameworks](frameworks.md)

阿里云百炼平台提供多种 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)与配套工具链，支持开发者无缝迁移现有应用。核心能力覆盖文本生成（Chat/Completions/Responses）、多模态理解（Vision）、向量化（Embedding）、文件管理、批量处理（Batch）及会话状态管理（Conversations），并兼容主流开发框架如 LangChain 和 OpenAI SDK。所有接口均需配合业务空间专属域名（`{WorkspaceId}.<region>.maas.aliyuncs.com`）使用，以获得最佳性能与稳定性。

## 支持的模型/功能

百炼支持的 OpenAI 兼容能力按场景划分为以下几类：

- **通用文本生成**：通过 `chat/completions` 接口支持 Qwen 系列（`qwen3.8-max`、`qwen3.7-plus` 等）、DeepSeek、GLM、Kimi、MiniMax 等数十种模型，详见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；  
- **智能体增强对话**：`responses` 接口专为 Agent 场景设计，内置联网搜索、网页抓取、代码解释器等工具，仅限阿里云直供模型（如 `qwen3.8-max`、`deepseek-v4-pro`）完整支持其 Agent 能力，[OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) 明确指出“非列表中阿里云百炼直供文本生成模型仅支持基础兼容能力，Agent 能力（内置工具等）受限”；  
- **视觉理解**：`chat/completions` 兼容 Vision 模式，支持 `qwen3-vl-plus`、`QVQ`、`Qwen-OCR` 等模型，输入支持 `image_url`（URL 或 data URI），但需注意 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md) 中强调“QVQ模型仅支持[流式输出](../concepts/streaming-output.md)”；  
- **文本补全（FIM）**：`completions` 接口专用于代码/内容续写，当前仅支持 `qwen-coder-turbo`，且**仅限华北2（北京）地域**，文档明确说明“本文档仅适用于华北2（北京）地域”；  
- **向量嵌入**：`embeddings` 接口支持 `text-embedding-v4`、`qwen3.7-text-embedding` 等，但**不支持稀疏向量输出**（传入 `output_type=sparse` 将返回空 embedding），详见 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)；  
- **文件管理**：`files` 接口支持 `purpose=file-extract`（文档问答）、`purpose=batch`（批量任务）、`purpose=fine-tune`（调优数据集），单文件上限依用途而异（150 MB / 500 MB / 300 MB）；  
- **批量处理**：提供两种模式——`batch`（文件批量提交，异步执行）和 `batch chat`（单请求同步等待），前者支持 JSONL 多模态输入，后者需切换至专用 endpoint `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`；  
- **会话状态管理**：`conversations` 接口用于创建、检索、更新和删除会话实体，配合 `responses` 的 `previous_response_id` 实现跨设备上下文延续。

> **注意**：文档 2（Responses API）与文档 9（Batch Chat）均提及 `enable_thinking` 参数需与 `model` 同级传入，但文档 2 的示例未展示该参数用法，而文档 9 明确要求“不能放在 `extra_body` 中”。实际调用时应严格遵循文档 9 的层级要求，避免因参数位置错误导致思考模式未生效或报错。

## 关键参数

| 参数 | 类型 | 必选 | 说明 | 来源约束 |
|------|------|------|------|----------|
| `base_url` | string | 是 | 必须使用业务空间专属域名，格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`；旧域名（如 `dashscope.aliyuncs.com`）仍可用但不推荐 | 所有接口均强调迁移至新域名，见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)、[OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) 等 |
| `api_key` | string | 是 | 按地域绑定：北京地域 API Key 仅可调用北京 endpoint，跨地域调用将返回 `invalid_api_key` 错误 | [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) 的“跨地域调用”小节明确此限制 |
| `model` | string | 是 | 模型名需严格匹配支持列表，例如 `qwen3.8-max`（Responses）、`qwen-coder-turbo`（Completions）、`text-embedding-v4`（Embedding） | 不同接口支持模型不同，如 `completions` 仅支持 `qwen-coder-turbo`，见 [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md) |
| `stream` / `stream_options` | boolean / object | 否 | [流式输出](../concepts/streaming-output.md)需设 `stream=true`；若需末尾 Token 统计，必须传 `{"include_usage": true}` | 所有流式示例均采用此写法，如 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) 的流式调用示例 |
| `enable_thinking` | boolean | 否 | 仅 Batch 场景下控制思考模式（影响 token 成本），必须作为 `body` 顶层字段，不可嵌套 | 文档 2 与文档 9 均强调此约束，但文档 2 示例缺失，实际应以文档 9 为准 |

## 使用方式

1. **环境准备**：安装对应 SDK（如 `pip install -U openai langchain_openai`），配置 `DASHSCOPE_API_KEY` 到环境变量；  
2. **初始化客户端**：指定 `base_url`（含 `{WorkspaceId}`）和 `api_key`，例如：
   ```python
   from openai import OpenAI
   client = OpenAI(
       api_key=os.getenv("DASHSCOPE_API_KEY"),
       base_url="https://your-workspace-id.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
   )
   ```  
3. **按接口调用**：
   - Chat：`client.chat.completions.create(model=..., messages=[...])`；  
   - Responses：`client.responses.create(model=..., input="...")`；  
   - Vision：`messages` 中 `content` 为包含 `image_url` 的数组；  
   - Embedding：`client.embeddings.create(model=..., input="...")`；  
   - Files：`client.files.create(file=Path("x.txt"), purpose="file-extract")`；  
   - Batch（文件）：先上传 JSONL 文件获 `file_id`，再 `client.batches.create(input_file_id=..., endpoint="/v1/chat/completions")`；  
   - Batch Chat：改用 `base_url="https://batch.dashscope.aliyuncs.com/compatible-mode/v1"`；  
   - Conversations：`client.conversations.create(items=[...])` 创建会话，后续请求通过 `conversation_id` 关联；  
4. **LangChain 集成**：优先选用 `langchain_openai.ChatOpenAI`（兼容部分模型）或 `langchain_community.chat_models.tongyi.ChatTongyi`（支持全部模型），详见 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

## 限制和注意事项

- **地域强绑定**：API Key 与 endpoint 地域必须一致，北京 Key 无法调用弗吉尼亚 endpoint，否则返回 `invalid_api_key`（HTTP 401），而非密钥失效；  
- **模型能力差异**：三方直供模型（如 SiliconFlow DeepSeek）仅在北京地域可用，且需在控制台手动开通服务；Qwen-Audio 不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；  
- **Endpoint 迁移强制要求**：`/api/v2/apps/protocols/compatible-mode/v1/responses` 和 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 已废弃，必须迁移到 `/compatible-mode/v1/responses` 和 `/compatible-mode/v1/conversations`；  
- **Batch 场景 Token 限制**：`qwen3.8-max` 等系列模型在 Batch 下支持最大 256K 上下文 Token，但 `qwen3.5-omni-plus` 不支持语音输出；  
- **Completions 接口地域限制**：仅支持华北2（北京）地域，且仅 `qwen-coder-turbo` 模型可用；  
- **Embedding 稀疏向量限制**：[OpenAI 兼容接口](../concepts/openai-compatible-api.md)不支持 `output_type=sparse`，需调用原生 DashScope 接口；  
- **QVQ 模型流式强制**：视觉模型 `QVQ` 仅支持[流式输出](../concepts/streaming-output.md)，非流式调用将失败；  
- **Conversations 数据隔离**：`Delete conversation` 仅删除会话元数据，不删除其关联的消息项。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)


