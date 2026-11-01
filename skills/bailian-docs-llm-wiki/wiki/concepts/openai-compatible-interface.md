# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台提供的一组标准化 API，严格遵循 OpenAI RESTful 协议规范（如 `/chat/completions`、`/embeddings` 等路径与请求/响应结构），使开发者无需修改核心逻辑即可复用现有 OpenAI SDK（Python/Node.js/Java/Go/C#）或工具链，快速接入百炼托管的 Qwen 及第三方大模型服务。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移与轻量对话**：使用 `/compatible-mode/v1/chat/completions` 端点，适用于已有 OpenAI 代码的平滑迁移、原型验证、CLI 工具（如 Cline、Kilo）、IDE 插件（如 Cursor、Qoder）等场景。支持 `qwen3.8-max`、`qwen-plus`、`deepseek-v4`、`glm-5.3` 等主流文本模型，但**不支持 Qwen-Audio、Qwen-MT-Image、QVQ 等非文本模型**。

- **智能体（Agent）开发**：使用 `/compatible-mode/v1/responses` 端点，是百炼重点演进方向。内置联网搜索、网页抓取、代码解释器、知识库检索等工具能力，支持 `previous_response_id` 实现多轮上下文管理、`store: true` 自动缓存会话状态，显著降低复杂 Agent 的工程复杂度。

- **多模态理解**：通过 `/compatible-mode/v1/vision/chat/completions` 调用 `qwen3-vl-plus`、`QVQ` 等视觉模型，支持 `image_url`（URL 或 Base64 Data URI）输入；注意 `QVQ` 仅支持[流式输出](streaming-output.md)。

- **向量嵌入**：调用 `/compatible-mode/v1/embeddings`，支持 `text-embedding-v4`、`qwen3.7-text-embedding` 等模型，用于 RAG、语义检索等场景；**不支持多模态嵌入（如 `qwen3-vl-embedding`）或稀疏向量输出**。

- **批量处理**：使用 `/compatible-mode/v1/batch`（JSONL 文件异步提交）或 `/compatible-mode/v1/batch-chat`（同步批量请求），适用于离线分析、评测、数据清洗等任务，支持最高 256K tokens 上下文的大模型（如 `qwen3.8-max`）。

- **会话状态管理**：配合 `/compatible-mode/v1/conversations` 接口，实现跨设备、长时间生命周期的对话上下文持久化，与 `/responses` 协同构建企业级聊天应用。

> ⚠️ 注意：所有 OpenAI 兼容接口均**必须使用业务空间专属域名**（格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`），旧域名 `dashscope.aliyuncs.com` 已不推荐，性能与稳定性较低。

## 关键参数和配置

- **`base_url`**：必需，必须为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1` 格式（例如 `https://my-workspace.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）。`{WorkspaceId}` 需替换为真实业务空间 ID，`{region}` 如 `cn-beijing`、`ap-southeast-1` 等。

- **`api_key`**：必需，使用 `DASHSCOPE_API_KEY`，通过 `Authorization: Bearer <key>` 请求头传入。API Key 与地域强绑定，北京地域 Key 不可用于新加坡 endpoint。

- **`model`**：必需，值必须严格匹配百炼官方发布的模型名（区分大小写、无空格），例如：
  - 文本：`qwen3.8-max`、`qwen3.7-plus`、`glm-5.3`
  - 多模态：`qwen3-vl-plus`、`qwen3.5-omni-plus`
  - 嵌入：`text-embedding-v4`、`qwen3.7-text-embedding`
  - 翻译：`qwen-mt-plus`（仅限 `/chat/completions`）

- **`messages`**：标准 OpenAI 格式数组，如 `[{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]`。部分模型（如 `QwQ`）不建议设置 `system`，`QVQ` 设置无效。

- **`stream`**：布尔值，默认 `false`。启用后返回 SSE 流式响应；`/responses` 支持 `stream_options={"include_usage": true}` 在末尾 chunk 返回 token 统计。

- **`previous_response_id`**（仅 `/responses`）：字符串，值为上一轮响应的顶层 `id`（UUID 格式），用于多轮对话状态延续。**不可使用 `output` 内消息的 `id`**。

- **`enable_thinking`**（部分模型必需）：布尔值，`qwen3.8`/`qwen3.7` 系列默认开启思考模式，该参数需与 `model` 同级显式传入（如 `{"model": "qwen3.8-max", "enable_thinking": true, ...}`），否则可能触发降级行为。

- **`extra_body`**（SDK 封装场景）：Python SDK 中用于传递协议扩展字段，例如 `qwen-mt-plus` 的 `translation_options`、`qwen3-vl-plus` 的 `fps`/`min_pixels` 等多模态参数。

- **`purpose`**（文件上传场景）：必需，值为 `file-extract`（文档解析）、`batch`（批量任务）或 `fine-tune`（微调数据集）。

## 面向开发者，简洁实用

✅ **推荐做法**  
- 初始化 OpenAI 客户端时，优先使用 `base_url = "https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1"` + `api_key`；  
- 对话类需求：简单场景用 `/chat/completions`，复杂 Agent 用 `/responses`；  
- 多模态任务：确认模型是否在 [Vision 接口支持列表](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md) 中；  
- 批量任务：优先选 `/batch`（异步+高吞吐），小批量可选 `/batch-chat`（同步+低延迟）；  
- 调试时用 cURL 或 Postman，确保 `Content-Type: application/json` 和 `Authorization` 头正确。

❌ **常见错误**  
- 混用 `base_url` 地域与 `api_key` 地域 → `401 Incorrect API key provided`；  
- 在 `/chat/completions` 中调用 `qwen-audio` 或 `qwen-mt-image` → `404 model not found`；  
- `previous_response_id` 传错层级（用了 `output[0].id` 而非响应顶层 `id`）→ 上下文丢失；  
- 忘记 `enable_thinking: true` 导致 `qwen3.8-max` 思考能力未生效 → 输出简短、缺乏推理链。

💡 提示：所有 OpenAI 兼容接口均可直接使用官方 `openai` Python 包（v1.0+），只需替换 `client = OpenAI(base_url=..., api_key=...)` —— 无需引入百炼特有 SDK。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [frameworks](../api/frameworks.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)


