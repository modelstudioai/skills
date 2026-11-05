# toolkits and [frameworks](frameworks.md)

阿里云百炼提供一系列 OpenAI 兼容的工具包与框架接口，覆盖文本生成、多模态理解、向量化、批量处理、对话管理等核心场景。开发者可复用现有 OpenAI 生态代码（如 SDK、LangChain 集成），仅需调整 `base_url`、`api_key` 和模型名即可快速迁移，无需重写业务逻辑。

## 支持的模型/功能

- **文本生成**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash` 等全系 Qwen 文本模型，以及 DeepSeek、GLM、Kimi、MiniMax 等三方直供模型（仅限华北2北京地域）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)  
- **多模态理解**：`qwen3-vl-plus`、`QVQ`、`Qwen-OCR` 支持图像/视频输入；`qwen3.8-omni-flash` 支持音视频输入 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)  
- **向量嵌入**：`text-embedding-v4`、`qwen3.7-text-embedding`、`qwen3.7-text-embedding-flash` 等，支持 64–2048 维可选输出 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)  
- **批量处理**：支持两种模式——文件批量（`/v1/batches`）适用于数千请求异步处理；单请求批量（`/v1/chat/completions` + `batch.dashscope.aliyuncs.com`）适用于单次高延迟容忍调用 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)  
- **智能体与上下文管理**：`Responses API` 内置联网搜索、网页抓取等工具；`Conversations API` 提供会话生命周期管理；`Responses API` 的 `previous_response_id` 可自动关联多轮上下文 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)  

> **注意**：`Qwen-Audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；`qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出，而 `qwen3.5-omni-flash` 同样受限 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `base_url` | 必填，服务端点，**必须匹配 API Key 所在地域** | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `model` | 必填，模型名称，需与所选接口能力匹配 | `qwen3.8-max`（Chat）、`qwen3-vl-plus`（Vision）、`text-embedding-v4`（Embedding） |
| `purpose`（文件接口） | 必填，指定文件用途 | `file-extract`（文档分析）、`batch`（批量任务）、`fine-tune`（调优） |
| `enable_thinking`（Batch） | 可选，控制是否启用思考模式（影响 token 计费） | `true` / `false`，须与 `model` 同级传入，不可置于 `extra_body` 中 |
| `dimensions`（Embedding） | 可选，仅 `text-embedding-v3/v4` 支持，指定向量维度 | `1024` |
| `previous_response_id`（Responses） | 可选，用于多轮对话上下文自动注入 | 上一轮响应的顶层 `id`（UUID 格式，非 `output` 内 `msg_xxx`） |

## 使用方式

1. **配置环境**：将 `DASHSCOPE_API_KEY` 配置为环境变量（强烈推荐），并确认其地域与目标 `base_url` 一致；获取 `WorkspaceId` 请见控制台「业务空间详情」页面。  
2. **选择接口与 SDK**：  
   - Chat/Responses/Vision/Embedding：使用 `openai` SDK（Python/Node.js/Java/Go/C#）或 HTTP 直调；  
   - Conversations/Batch Files：同上，但需注意 endpoint 路径差异；  
   - LangChain 集成：推荐 `langchain_openai`（兼容部分模型）或 `langchain-community` + `dashscope`（支持全部模型）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。  
3. **构造请求**：  
   - Chat/Responses/Vision：按 OpenAI 标准格式组织 `messages` 或 `input`；  
   - Embedding：传入 `input` 字符串或数组；  
   - Batch（文件）：准备 JSONL 文件，每行含 `custom_id`、`method`、`url`、`body`；  
   - Conversations：先 `create` 会话，再 `items.create` 添加消息。  
4. **处理响应**：流式调用需解析 `chat.completion.chunk`；Responses API 返回结构化 `output` 数组；Embedding 返回 `data[].embedding` 数组。

## 限制和注意事项

- **地域强绑定**：API Key 与 `base_url` 地域必须严格一致，跨地域调用（如北京 Key 调弗吉尼亚 endpoint）将返回 `invalid_api_key` 错误，而非权限不足 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- **域名迁移强制要求**：旧域名（`dashscope.aliyuncs.com` 等）虽仍可用，但官方已明确要求迁移至业务空间专属域名（`{WorkspaceId}.<region>.maas.aliyuncs.com`），以保障性能与稳定性，该要求适用于所有接口（Chat、Responses、Vision、Embedding、Conversations）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。  
- **文件配额硬限制**：文件上传服务总大小上限 100 GB、文件数上限 10,000 个，无自动过期机制，超限时需手动清理 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。  
- **Embedding 不支持稀疏向量**：通过 [OpenAI 兼容接口](../concepts/openai-compatibility.md)传入 `output_type=sparse` 将导致 embedding 字段为空（HTTP 200 成功但结果无效），需改用 DashScope 原生接口 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。  
- **三方模型地域限制**：DeepSeek（硅基流动/快手万擎）、Kimi（月之暗面）、GLM、MiniMax 等仅在中国站华北2（北京）地域可用，且需在控制台单独开通服务 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。

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


