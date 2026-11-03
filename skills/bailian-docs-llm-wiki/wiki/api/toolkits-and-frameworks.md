# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 OpenAI 兼容的工具包与框架接口，覆盖文本生成、[多模态](../concepts/multi-modal.md)理解、[向量嵌入](../concepts/vector-embedding.md)、批量推理、对话管理等核心场景。开发者可通过统一的 OpenAI SDK（Python/Node.js/Java/Go/C#）或 HTTP API 快速迁移现有应用，无需重写业务逻辑。所有接口均支持业务空间专属域名以提升稳定性与性能。

## 支持的模型/功能

- **文本生成**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash` 等全系 Qwen 文本模型，以及 DeepSeek、GLM、Kimi、MiniMax 等三方直供模型（仅限北京地域）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)  
- **[多模态](../concepts/multi-modal.md)理解**：`qwen3-vl-plus`、`QVQ`、`Qwen-OCR` 支持图像输入；`qwen3.8-omni-flash` 支持音视频输入 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)  
- **[向量嵌入](../concepts/vector-embedding.md)**：`text-embedding-v4`、`qwen3.7-text-embedding` 等 6 款模型，支持 201 种语种及可选维度（如 `dimensions=1024`）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)  
- **批量处理**：支持文件批量（JSONL）与单请求同步批量（Batch Chat）两种模式，适用于数据标注、模型评测等非实时场景  
- **对话管理**：`Conversations API` 提供会话生命周期管理（创建/更新/删除/追加消息），配合 `Responses API` 实现自动上下文注入与跨设备延续  

> **注意**：文档 5 和文档 6 对 `qwen3.8-max` 等模型在 Batch 场景下的最大上下文 [Token](../concepts/token.md) 数描述一致（256K），但文档 2 中 `Responses API` 未明确该限制，实际使用时应以 Batch 接口文档为准。

## 关键参数

- **`base_url`**：必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）虽仍可用但不推荐 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)  
- **`api_key`**：严格按地域绑定，北京地域 API Key 不可用于调用弗吉尼亚 endpoint，否则返回 `invalid_api_key` 错误  
- **`model`**：需从各接口支持的模型列表中精确选择（如 Vision 接口仅支持 `qwen3-vl-plus`，Embedding 接口不支持 `qwen3-vl-plus`）  
- **`purpose`（文件接口）**：上传时必填，取值为 `file-extract`（文档分析）、`batch`（批量任务）、`fine-tune`（调优数据集）  
- **`enable_thinking`（Batch）**：`qwen3.5+` 系列模型默认开启思考模式，显式设为 `false` 可避免额外 token 成本，且必须置于 JSONL `body` 顶层，不可放入 `extra_body`  

## 使用方式

1. **初始化客户端**：配置 `api_key`（建议环境变量）和 `base_url`（含 `{WorkspaceId}`）  
2. **选择接口**：  
   - 单次对话 → `chat.completions.create()`（Chat Completions）  
   - 智能体任务 → `responses.create()`（Responses API，内置工具）  
   - 多轮无状态 → `conversations.create()` + `previous_response_id`（Conversations + Responses）  
   - 文件分析 → `files.create(purpose="file-extract")`  
   - 批量处理 → `batches.create()`（文件） 或 `chat.completions.create()`（同步 Batch Chat）  
3. **调用示例**（Python）：  
   ```python
   from openai import OpenAI
   client = OpenAI(
       api_key=os.getenv("DASHSCOPE_API_KEY"),
       base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
   )
   # Responses API（推荐用于智能体）
   resp = client.responses.create(model="qwen3.8-max", input="你好")
   # Conversations API（管理长期会话）
   conv = client.conversations.create(items=[{"role":"system","content":"你很专业"}])
   ```

## 限制和注意事项

- **地域隔离**：API Key 与 `base_url` 地域必须严格匹配，跨地域调用将被鉴权拒绝  
- **模型能力差异**：非阿里云直供模型（如三方 DeepSeek）仅支持基础 Chat Completions，不支持 Responses API 的内置工具、Conversations API 等高级功能  
- **文件配额**：总存储上限 100 GB / 最多 10,000 个文件，超限时需手动清理  
- **Qwen-Audio 例外**：明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)  
- **Embedding 稀疏向量**：[OpenAI 兼容接口](../concepts/openai-compatible-api.md)不支持 `output_type=sparse`，需改用 DashScope 原生接口  
- **旧路径弃用**：`/api/v2/apps/protocols/...` 类路径（如 Conversations、Responses）已停止维护，必须迁移至 `/compatible-mode/v1/...`

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


