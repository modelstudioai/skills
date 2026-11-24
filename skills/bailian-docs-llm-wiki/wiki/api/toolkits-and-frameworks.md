# toolkits and [frameworks](frameworks.md)

百炼平台提供多种主流工具包与框架的兼容支持，帮助开发者快速集成大模型能力。当前重点支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（覆盖 Chat、Vision、Embedding、Batch 等场景）及 LangChain 生态，所有接口均基于百炼自有模型实现，无需修改客户端核心逻辑即可迁移。详细能力边界和参数行为请参考各子模块文档。

## 支持的模型/功能

- **[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**：完整支持 `chat/completions`、`embeddings`、`images/generations`（Qwen-VL）、`files`、`batches`（含 Batch Chat 和文件输入模式）、`conversations` 等端点，底层调用 Qwen 系列模型（如 qwen-max、qwen-plus、qwen-vl-plus）[OpenAI兼容-Chat](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- **LangChain 集成**：提供 `BailianLLM`、`BailianEmbeddings` 等原生封装类，支持 `invoke()`、`stream()`、`embed_query()` 等标准方法，适配 LangChain v0.1.x 至 v0.2.x [LangChain](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。  
- **Vision 与多模态**：Qwen-VL 模型通过 `/v1/chat/completions` 接口支持图像输入，兼容 OpenAI 的 `messages[].content` 中 `image_url` 格式，但仅支持 base64 编码（不支持远程 URL）[OpenAI兼容-Vision](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。

## 关键参数

- `model`：必须显式指定（如 `qwen-max`），不支持 OpenAI 的 `gpt-3.5-turbo` 别名；未传时默认行为已废弃，将返回 400 错误。  
- `response_format`：仅 `{"type": "json_object"}` 受支持，且要求模型本身具备 JSON 输出能力（如 `qwen-plus`），`text` 类型为默认值，不可省略。  
- `tools` / `tool_choice`：支持[函数调用](../concepts/function-calling.md)协议，但工具定义需符合百炼 Schema（`function.parameters` 必须为 JSON Schema object，不支持 `null` 或 `anyOf`）；`tool_choice="auto"` 行为与 OpenAI 不完全一致，详见 [OpenAI兼容-Chat](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。  
- `batch_id`：在 Batch 接口中为只读字段，由服务端生成；客户端提交时若携带将被忽略。

## 使用方式

1. **HTTP 调用**：复用 OpenAI SDK（如 `openai==1.35.0+`），只需替换 `base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"` 与 `api_key`（使用百炼 API Key）。  
2. **LangChain**：安装 `langchain-community` 后，导入 `from langchain_community.llms import BailianLLM`，初始化时传入 `model_name` 和 `api_key` 即可 [LangChain](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。  
3. **文件处理**：上传文件需先调用 `/v1/files`（兼容 OpenAI 文件接口），再在 `/v1/batches` 或 `/v1/chat/completions` 中引用 `file_id`；注意百炼不支持 OpenAI 的 `purpose="fine-tune"` [OpenAI兼容-File](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。

## 限制和注意事项

- 所有 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)均**不支持 streaming + function calling 组合**（即 `stream=True` 且 `tools` 非空），该组合将返回 400；此限制在 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md) 和 [OpenAI兼容-Chat](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) 中均有明确说明。  
- `conversations` 接口（用于历史消息管理）目前为只读模拟层，不持久化会话状态，实际仍依赖客户端维护 `messages` 数组；该设计与 [OpenAI兼容-Conversations](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md) 文档描述一致，但不同于 OpenAI 原生行为。  
> **注意**：`/v1/embeddings` 接口的 `input` 字段支持字符串数组或单字符串，但当传入数组时，最大长度为 2048 tokens（按模型 tokenizer 计算），而 [OpenAI兼容-Embedding](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md) 文档中误写为“不限长度”，应以实际 API 响应为准。

## 来源文档

- [工具包/框架](../../raw/model-api-reference/toolkits-and-frameworks.md)


