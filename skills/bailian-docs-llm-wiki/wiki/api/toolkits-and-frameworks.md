# toolkits and [frameworks](frameworks.md)

百炼平台提供多种主流工具包与框架的兼容支持，帮助开发者快速集成大模型能力。当前重点支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（覆盖 Chat、Vision、Embedding、Batch 等场景）及 LangChain 生态，所有接口均基于百炼自有模型实现，无需修改业务逻辑即可迁移。详细能力边界和参数行为请参考对应子文档。

## 支持的模型/功能

- **[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**：完整支持 `chat/completions`、`embeddings`、`images/generations`（Qwen-VL）、`files`、`batches`（含 Batch Chat 和文件输入模式）、`conversations` 等端点，底层调用 Qwen 系列模型（如 qwen-max、qwen-plus、qwen-vl）；  
- **LangChain 集成**：提供 `BailianChatModel` 和 `BailianEmbeddings` 封装类，适配 LangChain v0.1.x 的标准接口；  
- 所有兼容接口均通过 [OpenAI兼容-Chat](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) 统一协议规范定义，实际行为以该文档为准。

## 关键参数

- `model`：必填，需指定百炼平台注册的模型名（如 `qwen-max`），不支持 OpenAI 原生模型名（如 `gpt-4`）；  
- `temperature` / `top_p` / `max_tokens`：语义与 OpenAI 一致，但部分模型对 `max_tokens` 存在硬性上限（例如 qwen-vl 当前最大输出为 2048 tokens）；  
- `response_format`：仅 `chat/completions` 支持 `{"type": "json_object"}`，且要求模型本身启用 JSON 模式（参见 [OpenAI兼容-Responses](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)）；  
- `file_id` / `batch_id`：必须通过百炼平台上传并获取 ID，不可复用 OpenAI 的资源 ID。

## 使用方式

1. 设置 API Endpoint 为 `https://dashscope.aliyuncs.com/compatible-mode/v1`（非 `api.dashscope.ai`）；  
2. 使用百炼 API Key（非 OpenAI Key）进行鉴权；  
3. 对于 LangChain，安装 `langchain-bailian` 包后直接初始化：  
   ```python
   from langchain_bailian.chat_models import BailianChatModel
   llm = BailianChatModel(model_name="qwen-plus")
   ```  
   完整示例见 [LangChain](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

## 限制和注意事项

- Batch 接口仅支持 `chat/completions` 类型任务，不支持 `embeddings` 或 `images/generations` 的批量提交；  
- Vision 接口（`qwen-vl-compatible-with-openai.md`）暂不支持 `system` 角色消息，且图像 URL 必须为公网可访问地址；  
- > **注意**：[OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) 中描述的 `input_file_id` 字段已废弃，当前仅支持 `input_file` 直接传入 Base64 编码内容或公网 URL —— 请以 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md) 的最新字段定义为准；  
- 所有兼容接口均不支持 streaming + function calling 组合使用（即 `stream=true` 时 `functions` 参数将被忽略）。

## 来源文档

- [工具包/框架](../../raw/model-api-reference/toolkits-and-frameworks.md)


