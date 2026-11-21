# toolkits and [frameworks](frameworks.md)

百炼平台提供多种主流工具包与框架的兼容支持，帮助开发者快速集成大模型能力。当前重点支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（覆盖 Chat、Vision、Embedding、Batch 等场景）及 LangChain 生态，所有接口均基于百炼自有模型实现，无需修改客户端核心逻辑即可迁移。详细能力边界和参数行为请参考各子模块文档。

## 支持的模型/功能

- **[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**：完整支持 `chat/completions`、`embeddings`、`images/generations`（Qwen-VL）、`files`、`batches`（含 Batch Chat 和文件输入模式）、`conversations` 等端点，底层调用 Qwen 系列模型（如 qwen-max、qwen-plus、qwen-vl-plus）[OpenAI兼容-Chat](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- **LangChain 集成**：提供 `BailianLLM`、`BailianEmbeddings` 等原生封装类，支持 `invoke()`、`stream()`、`embed_query()` 等标准方法，适配 LangChain v0.1.x 至 v0.2.x [LangChain](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。  
- **Vision 与多模态**：Qwen-VL 模型通过 `/v1/chat/completions` 接口支持图像输入，兼容 OpenAI 的 `messages[].content` 中 `image_url` 格式，但仅支持 base64 编码（不支持远程 URL）[OpenAI兼容-Vision](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。

## 关键参数

- `model`：必须显式指定（如 `qwen-max`），不支持 OpenAI 的 `gpt-3.5-turbo` 别名；未传时默认行为已废弃，将返回 400 错误。  
- `response_format`：仅 `{"type": "json_object"}` 受支持，且要求模型本身具备 JSON 输出能力（如 `qwen-plus`），`text` 类型为默认值，不可省略。  
- `tools` / `tool_choice`：支持[函数调用](../concepts/function-calling.md)协议，但工具定义需符合百炼 Schema（非 OpenAI 的 `function` 字段嵌套结构），详见 [OpenAI兼容-Chat](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- `batch_id`：Batch 接口返回的 ID 仅在创建后 7 天内有效，超期后 `GET /v1/batches/{id}` 返回 404，而非 OpenAI 的 `expired` 状态。

## 使用方式

1. **OpenAI 兼容调用**：将 `https://api.openai.com/v1/...` 替换为百炼 API 地址 `https://dashscope.aliyuncs.com/api/v1/...`，复用原有 `Authorization: Bearer <api_key>`，无需修改请求体结构。  
2. **LangChain 快速接入**：
   ```python
   from langchain_community.llms import BailianLLM
   llm = BailianLLM(model_name="qwen-plus", api_key="sk-xxx")
   llm.invoke("你好")  # 自动路由至 /v1/chat/completions
   ```
   注意：`BailianLLM` 默认启用流式响应（`streaming=True`），若需禁用需显式传 `streaming=False`。  
3. **Batch 提交**：使用 `POST /v1/batches` 提交 `.jsonl` 文件（每行一个 `/v1/chat/completions` 请求），文件需通过 `files` 接口预上传并获取 `file_id` —— 此流程与 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) 描述一致，但 `file_id` 有效期为 24 小时（非 OpenAI 的 7 天）。

## 限制和注意事项

- 所有 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**不支持** `logit_bias`、`user` 字段、`n > 1` 的多候选生成（仅 `n=1` 有效）。  
- Embedding 接口仅支持 `text-embedding-v3` 模型，`input` 最大长度为 8192 tokens；`dimensions` 参数固定为 1024，忽略客户端传入值 [OpenAI兼容-Embedding](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。  
- > **注意**：[OpenAI兼容-Conversations](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md) 文档中提及的 `conversation_id` 持久化能力，当前仅对百炼控制台调试页生效，API 层面不维护会话状态，开发者需自行管理 history。  
- > **注意**：原始文档中 `openai-file-interface.md` 描述支持 `purpose="fine-tune"`，但该功能尚未上线，实际调用将返回 `{"error": {"code": "unsupported_purpose", ...}}`，请勿在生产环境使用。  
- LangChain 的 `BailianEmbeddings` 类暂不支持 `batch_size > 100`，超出将触发 `429 Too Many Requests`，建议设为 `50`。

## 来源文档

- [工具包/框架](../../raw/model-api-reference/toolkits-and-frameworks.md)


