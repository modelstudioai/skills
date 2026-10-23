# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)及配套工具链，覆盖文本生成、多模态理解、[向量嵌入](../concepts/embedding.md)、批量推理、会话管理等核心场景。开发者可复用现有 OpenAI SDK 代码，仅需调整 `base_url`、`api_key` 和模型名称即可快速迁移；同时支持 LangChain 等主流框架的原生集成。所有兼容接口均基于业务空间专属域名（`{WorkspaceId}.<region>.maas.aliyuncs.com`）提供更高性能与稳定性。

## 支持的模型/功能

- **文本生成**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash` 等全系 Qwen 文本模型，以及 DeepSeek、GLM、Kimi、MiniMax 等三方直供模型（仅限华北2北京地域）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)  
- **多模态理解**：`qwen3-vl-plus`、`QVQ`、`Qwen-OCR` 支持图像/视频输入；`qwen3.8-omni-flash` 支持音视频输入 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)  
- **[向量嵌入](../concepts/embedding.md)**：`text-embedding-v4`、`qwen3.7-text-embedding` 等，支持 201 种语种及可选维度（如 1024、2048）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)  
- **智能体与工具调用**：Responses API 内置联网搜索、网页抓取、代码解释器等工具；Chat Completions API 支持 `function_call` 协议 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)  
- **长文档与结构化处理**：`Qwen-Long`（长上下文问答）、`Qwen-Doc-Turbo`（文档数据提取）、`Qwen-VL-OCR`（图文识别）  

> **注意**：`Qwen-Audio` 不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；`qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出，且 `qwen3.8-max` 等系列模型默认开启思考模式，需显式设置 `enable_thinking=false` 关闭以避免额外 token 成本。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `base_url` | 必填，业务空间专属域名，**非通用 dashscope.aliyuncs.com** | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `model` | 必填，模型名称需严格匹配支持列表 | `qwen3.8-max`, `text-embedding-v4`, `qwen3-vl-plus` |
| `purpose`（文件接口） | 文件用途标识，决定后续使用场景 | `file-extract`（文档分析）、`batch`（批量任务）、`fine-tune`（调优） |
| `previous_response_id`（Responses API） | 多轮对话上下文关联 ID，传入上一轮响应顶层 `id`（UUID 格式） | `"0c842a11-c7d1-45da-b7ec-4e668c389xxx"` |
| `dimensions`（Embedding） | 仅 `text-embedding-v3/v4` 支持，指定向量维度 | `1024` |
| `stream_options={"include_usage": true}` | 流式响应末尾返回 token 使用统计 | — |

## 使用方式

- **SDK 调用**：统一使用 OpenAI SDK（Python/Node.js/Java/Go/C#），仅需配置 `base_url` 和 `api_key`。例如：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  # Chat Completions
  client.chat.completions.create(model="qwen3.8-max", messages=[...])
  # Responses API（智能体）
  client.responses.create(model="qwen3.8-max", input="你能做什么？")
  # Embedding
  client.embeddings.create(model="text-embedding-v4", input="hello")
  # Conversations（会话管理）
  client.conversations.create(items=[{"role":"system","content":"..."}])
  ```
- **LangChain 集成**：推荐两种路径：
  - `langchain_openai.ChatOpenAI`：兼容部分模型，适合快速迁移 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)  
  - `langchain_community.chat_models.tongyi.ChatTongyi`：支持全部百炼文本模型及部署模型，功能更完整  
- **HTTP 直连**：所有接口均提供标准 REST endpoint，如 `POST /compatible-mode/v1/chat/completions`、`POST /compatible-mode/v1/responses`、`POST /compatible-mode/v1/embeddings`  
- **文件与批量**：通过 `files.create(purpose="batch")` 上传 JSONL 文件，再调用 `batches.create()` 启动[异步任务](../concepts/asynchronous-task.md)；或使用 `/batch/chat/completions` 同步等待结果（Batch Chat）  

## 限制和注意事项

- **地域绑定**：API Key 与 `base_url` 所属地域必须一致（如北京 Key 只能调用北京 `base_url`），跨地域调用返回 `invalid_api_key` 错误 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)  
- **域名迁移**：旧域名 `dashscope.aliyuncs.com` 已逐步淘汰，**必须迁移至业务空间专属域名**（`{WorkspaceId}.<region>.maas.aliyuncs.com`），否则可能遭遇性能下降或服务不稳定  
- **文件配额**：文件存储上限为 10,000 个文件或 100 GB 总大小，无自动过期机制，需手动清理 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)  
- **Batch 限制**：`batch-test-model` 仅用于链路验证，文件 ≤ 1 MB、行数 ≤ 100、并发 ≤ 2；正式任务需使用真实模型  
- **Embedding 稀疏向量**：[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**不支持** `output_type=sparse`，该参数将被忽略且 embedding 字段为空，需改用 DashScope 原生接口  
- **Vision 模型流式限制**：`QVQ` 模型仅支持[流式输出](../concepts/streaming-output.md)，非流式调用将失败 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)

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


