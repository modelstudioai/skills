# toolkits and [frameworks](frameworks.md)

百炼平台提供多种主流工具包与框架的兼容支持，帮助开发者快速集成大模型能力。当前重点支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（覆盖 Chat、Vision、Embedding、Batch 等场景）及 LangChain 生态，所有接口均基于百炼自有模型实现，无需修改业务逻辑即可迁移。详细能力边界和参数行为请参考对应子文档。

## 支持的模型/功能

- **[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**：完整支持 `chat/completions`、`embeddings`、`images/generations`（Qwen-VL）、`files`、`batches`（含 Batch Chat 和文件输入模式）、`conversations` 等端点，底层调用 Qwen 系列模型（如 qwen-max、qwen-plus）或专用多模态模型 [OpenAI兼容-Vision](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。  
- **LangChain 集成**：提供 `BailianChatModel` 和 `BailianEmbeddings` 封装，适配 LangChain v0.1.x 标准接口，支持 streaming、tool calling 等高级特性 [LangChain](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。  
- **批量处理能力**：`batches` 接口支持异步提交 100 条以内请求，适用于离线分析场景；但注意 `batch/chat` 与 `batch/file-input` 的 payload 结构不兼容，需按 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md) 和 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) 分别构造。

## 关键参数

- `model`：必填，值必须为百炼平台已发布的模型名（如 `qwen-max`），不支持 OpenAI 模型名（如 `gpt-4o`）；传入非法 model 将返回 404。  
- `response_format`：仅 `chat/completions` 支持 `{"type": "json_object"}`，但要求模型本身支持 JSON 输出（如 `qwen-plus`），`qwen-max` 当前不支持该格式 [OpenAI兼容-Chat](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- `file_id` / `batch_id`：所有文件与批量操作均使用百炼平台内生成的 ID，不可复用 OpenAI 的 ID；上传文件后需等待 `status: "processed"` 才可引用。

## 使用方式

1. 设置请求头 `Authorization: Bearer <api_key>` 和 `Content-Type: application/json`；  
2. 向 `https://dashscope.aliyuncs.com/api/v1/<endpoint>` 发送 POST 请求（如 `/chat/completions`）；  
3. 对于 LangChain，安装 `langchain-bailian` 包后直接初始化：  
   ```python
   from langchain_bailian.chat_models import BailianChatModel
   llm = BailianChatModel(model_name="qwen-plus", api_key="sk-xxx")
   ```

## 限制和注意事项

- 所有 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)均**不支持** `functions` / `tools` 参数（即原生 function calling），仅支持百炼自有的 `tool_choice` + `tools` schema（参见 [OpenAI兼容-Chat](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）；LangChain 中的 `bind_tools()` 行为将被忽略。  
- `conversations` 接口仅支持单轮上下文管理，不维护长期会话状态，与 OpenAI 的 `thread` 语义不同 [OpenAI兼容-Conversations](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。  
- > **注意**：原始文档中 [OpenAI兼容-Responses](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) 提到支持 `responses` 端点，但该端点已于 2024 年 7 月下线，实际调用将返回 404；请改用标准 `chat/completions` 或 `embeddings` 接口。  
- 文件上传大小上限为 50MB，且仅支持 `.txt`, `.pdf`, `.docx`, `.xlsx`, `.csv`, `.json` 格式；图像类文件需通过 `qwen-vl` 专用接口处理，不可混用 [OpenAI兼容-File](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。

## 来源文档

- [工具包/框架](../../raw/model-api-reference/toolkits-and-frameworks.md)


