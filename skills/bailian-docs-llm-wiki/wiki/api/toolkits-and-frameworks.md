# toolkits and [frameworks](frameworks.md)

阿里云百炼提供一系列 OpenAI 兼容的工具包与框架接口，覆盖文本生成、多模态理解、向量嵌入、批量推理、会话管理等核心场景。开发者可复用现有 OpenAI 生态代码（如 SDK、LangChain 集成），仅需调整 `base_url`、`api_key` 和模型名称即可快速迁移，无需重写业务逻辑。

## 支持的模型/功能

- **文本与智能体能力**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash` 等全系 Qwen 文本模型，以及 `deepseek-v4-pro`、`glm-5.3`、`kimi-k3` 等三方直供模型；其中 Responses API 提供内置联网搜索、网页抓取、代码解释器等 Agent 原生能力 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。
- **多模态理解**：`qwen3-vl-plus`、`QVQ`、`Qwen-OCR` 支持图像输入与图文混合推理；`qwen3.8-omni-flash` 支持音视频输入 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。
- **向量嵌入**：`text-embedding-v4`、`qwen3.7-text-embedding` 等支持多语种、多维度配置，但**不支持稀疏向量输出**（传入 `output_type=sparse` 将返回空 embedding）[OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。
- **长文档与结构化处理**：`Qwen-Long`（长上下文问答）、`Qwen-Doc-Turbo`（文档数据提取）通过文件 ID 调用 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。
- **会话状态管理**：Conversations API 支持跨设备创建、更新、删除会话及追加消息项，配合 Responses API 的 `previous_response_id` 实现无状态上下文延续 [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。

> **注意**：`Qwen-Audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；该限制在 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) 中已明确说明，与其他文档无冲突。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `base_url` | 必填，地域专属业务空间域名，**非通用 dashscope.aliyuncs.com** | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `model` | 必填，模型名称须严格匹配支持列表，大小写敏感 | `"qwen3.8-max"`, `"text-embedding-v4"` |
| `purpose`（文件接口） | 必填，决定文件用途：`file-extract`（文档分析）、`batch`（批量任务）、`fine-tune`（调优） | `"file-extract"` |
| `enable_thinking`（Batch） | 可选布尔值，控制是否启用思考模式；`qwen3.5+` 系列默认开启，建议显式设置 | `false` |
| `dimensions`（Embedding） | 可选，仅 `text-embedding-v3/v4` 支持，指定向量维度 | `1024` |

## 使用方式

1. **环境准备**：安装对应 SDK（如 `pip install -U openai langchain_openai`），并**将 `DASHSCOPE_API_KEY` 配置为环境变量**（避免硬编码泄露风险）。
2. **初始化客户端**：传入 `api_key` 和 `base_url`，`base_url` 中 `{WorkspaceId}` 需替换为控制台获取的真实 ID。
3. **调用接口**：
   - Chat Completions：`client.chat.completions.create(...)`
   - Responses：`client.responses.create(...)`（支持 `input` 字符串或 `previous_response_id`）
   - Embeddings：`client.embeddings.create(...)`
   - Files：`client.files.create(file=..., purpose="...")`
   - Conversations：`client.conversations.create(...)` + `client.conversations.items.create(...)`
   - Batch（文件）：先上传 JSONL 文件（`purpose="batch"`），再 `client.batches.create(input_file_id=...)`
   - Batch（单请求）：使用 `base_url="https://batch.dashscope.aliyuncs.com/compatible-mode/v1"` 直接调用 `chat.completions.create(...)`

> **注意**：文档 5（Batch 文件）与文档 6（Batch Chat）对 `base_url` 的要求存在表面矛盾——前者示例使用 `https://dashscope.aliyuncs.com/compatible-mode/v1`，后者明确要求 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`。实际应以文档 6 为准：**Batch Chat 单请求必须使用 `batch.dashscope.aliyuncs.com` 域名**；而 Batch 文件上传仍使用标准 `dashscope.aliyuncs.com` 或业务空间域名，仅任务创建时 endpoint 指向 `/v1/chat/completions` 等路径。

## 限制和注意事项

- **地域绑定**：API Key 与 `base_url` 所属地域强绑定。北京地域 Key 无法调用弗吉尼亚 endpoint，否则返回 `invalid_api_key` 错误（非密钥失效）[OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- **域名迁移**：华北2（北京）、新加坡、中国香港地域已启用业务空间专属域名（`{WorkspaceId}.<region>.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但**新项目必须迁移**以获得更高性能与稳定性。
- **文件配额**：文件服务总容量上限 100 GB，最多 10,000 个文件；单个 `file-extract` 文件 ≤ 150 MB，`batch` 文件 ≤ 500 MB，`fine-tune` 文件 ≤ 300 MB。
- **Batch 超时**：Batch Chat 单请求最长等待 3600 秒（1 小时），需在 SDK 客户端显式配置 `timeout` 参数（如 Python 的 `.with_options(timeout=1800.0)`）。
- **三方模型限制**：DeepSeek、Kimi、GLM 等三方直供模型**仅在中国站华北2（北京）地域可用**，且需在控制台单独开通服务授权。

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


