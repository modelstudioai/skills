# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)工具包与框架，覆盖文本生成、视觉理解、[向量嵌入](../concepts/vector-embedding.md)、批量推理、会话管理等核心场景。开发者可复用现有 OpenAI SDK 和生态代码，仅需调整 `base_url`、`api_key` 和模型名称即可快速迁移；同时支持 LangChain 等主流 LLM 应用框架的原生集成。所有兼容接口均基于业务空间专属域名（如 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以保障性能与稳定性。

## 支持的模型/功能

- **文本生成**：`qwen4-max`、`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash` 等全系列千问模型，以及 DeepSeek、GLM、Kimi、MiniMax 等三方直供模型（仅限华北2北京地域）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)  
- **多模态理解**：`qwen3-vl-plus`、`QVQ`、`Qwen-OCR` 支持图像输入与结构化响应 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)  
- **[向量嵌入](../concepts/vector-embedding.md)**：`text-embedding-v4`、`qwen3.7-text-embedding`、`qwen3.7-text-embedding-flash` 等，支持多维度与多语种 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)  
- **批量处理**：支持 Batch File（JSONL 文件上传）与 Batch Chat（单请求同步等待）两种模式，成本降低 50% [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)  
- **会话管理**：`Conversations API` 自动维护跨设备上下文，配合 `Responses API` 实现智能体原生多轮交互 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)  
- **文件操作**：`Files API` 支持文档问答（`purpose=file-extract`）、批量任务（`purpose=batch`）和模型调优（`purpose=fine-tune`）三类用途  

> **注意**：`Qwen-Audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；而 `qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出，但文档 6 未明确标注该限制，需以文档 5 的说明为准。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `base_url` | 必填，业务空间专属域名，**必须匹配 API Key 所在地域** | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `api_key` | 必填，按地域隔离，北京 Key 不可用于调用弗吉尼亚 endpoint | `sk-xxx`（从控制台业务空间详情页获取） |
| `model` | 必填，模型名需严格匹配支持列表，大小写敏感 | `"qwen4-max"`、`"text-embedding-v4"` |
| `stream` | 可选，流式响应开关（Chat Completions / Vision） | `True` |
| `stream_options.include_usage` | 可选，流式末尾返回 token 统计 | `{"include_usage": true}` |
| `previous_response_id` | Responses API 多轮对话必需，传上一轮响应顶层 `id`（非 `output[].id`） | `"0c842a11-c7d1-45da-b7ec-4e668c389xxx"` |

> **注意**：`enable_thinking` 是 Batch 场景下控制思考模式的关键参数，**必须作为 JSONL 请求体 `body` 的顶层字段传入**（与 `model` 同级），不可置于 `extra_body` 中——此规则在文档 5 和文档 6 中重复强调，但文档 6 的示例代码未体现该结构，存在误导风险。

## 使用方式

1. **SDK 初始化**：使用 OpenAI SDK 或 LangChain 封装类，配置 `base_url` 和 `api_key`  
   - OpenAI Python SDK：`OpenAI(api_key=..., base_url=...)`  
   - LangChain：`ChatOpenAI(..., base_url=...)` 或 `ChatTongyi(dashscope_api_key=...)` [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)  
2. **接口调用**：  
   - Chat：`client.chat.completions.create(model=..., messages=...)`  
   - Vision：`messages` 中 `content` 为含 `image_url` 的数组  
   - Embedding：`client.embeddings.create(model=..., input=...)`  
   - Batch File：先 `client.files.create(file=..., purpose="batch")`，再 `client.batches.create(input_file_id=...)`  
   - Conversations：`client.conversations.create(items=[...])` → 获取 `id` → 在后续 `responses.create(previous_response_id=...)` 中复用  
3. **地域对齐**：确保 `base_url` 地域、`api_key` 创建地域、模型开通地域三者一致，否则返回 `invalid_api_key`（HTTP 401）  

## 限制和注意事项

- **域名迁移强制要求**：旧域名 `dashscope.aliyuncs.com` 已逐步停用，**所有新项目必须使用业务空间专属域名**（如 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），否则可能遭遇性能下降或未来不可用 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)  
- **文件配额**：`Files API` 总数上限 10,000 个，总大小上限 100 GB；单文件大小限制依 `purpose` 而异：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB  
- **Batch 超时**：Batch Chat 默认等待 3600 秒（1 小时），超时断连；Batch File 任务最长执行窗口为 `24h`  
- **模型能力差异**：  
  - `Responses API` 的 Agent 内置工具（联网搜索、代码解释器等）**仅对列表中阿里云直供模型完全可用**，三方模型仅支持基础 chat 能力  
  - `Conversations API` 仅存储元数据与初始消息，**不保存历史响应内容**，实际上下文注入依赖 `Responses API` 的 `previous_response_id` 机制  
- **安全实践**：API Key **严禁硬编码**，必须通过环境变量（如 `DASHSCOPE_API_KEY`）注入；生产环境应启用密钥轮换与权限最小化策略

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)


