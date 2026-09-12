# toolkits and frameworks

百炼平台提供多种主流工具包与框架的兼容支持，帮助开发者快速集成大模型能力。当前重点支持 [OpenAI 兼容接口](../concepts/openai-compatibility.md)（覆盖 Chat、Completions、Vision、Embedding 等核心场景）及 LangChain 生态集成。所有兼容性实现均基于 [工具包/框架](../../raw/model-api-reference/toolkits-and-frameworks.md) 文档定义，开发者应以该文档为权威依据。

## 支持的模型与功能

- **[OpenAI 兼容接口](../concepts/openai-compatibility.md)**：完整支持 `chat/completions`、`completions`、`embeddings`、`vision`（Qwen-VL）、`files`（上传/检索）、`batches`（异步批量处理）、`conversations`（历史会话管理）等端点，底层调用百炼托管的 Qwen 系列模型（如 qwen-max、qwen-plus、qwen-turbo）。  
- **LangChain 集成**：提供 `BailianChatModel` 和 `BailianEmbeddings` 等原生封装类，支持直接接入 LangChain 的 LLMChain、RetrievalQA 等标准组件。详细用法见 [工具包/框架](../../raw/model-api-reference/toolkits-and-frameworks.md) 中的 LangChain 小节。  
- > **注意**：部分 OpenAI 兼容端点（如 `conversations`）在 [工具包/框架](../../raw/model-api-reference/toolkits-and-frameworks.md) 中标注为“Beta”，其行为与 OpenAI 官方 API 存在语义差异（例如会话状态不跨请求持久化），实际使用前请务必验证业务逻辑。

## 关键参数

- 所有 [OpenAI 兼容接口](../concepts/openai-compatibility.md)统一使用 `Authorization: Bearer <api_key>` 认证，Endpoint 域名为 `https://dashscope.aliyuncs.com/api/v1`。  
- 必填参数与 OpenAI 保持一致（如 `model`、`messages`、`input`），但 `model` 值必须为百炼平台已开通的模型 ID（如 `"qwen-turbo"`），不可使用 OpenAI 模型名（如 `"gpt-4"`）。  
- LangChain 中需显式传入 `dashscope_api_key` 和 `model_name`，且 `model_name` 必须与 [工具包/框架](../../raw/model-api-reference/toolkits-and-frameworks.md) 所列模型列表严格匹配。

## 使用方式

- **HTTP 直连**：按 OpenAI 标准格式构造请求，替换 URL 和 `model` 字段即可，无需修改请求体结构。参考各子接口文档（如 [OpenAI兼容-Chat](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope)）。  
- **LangChain 调用**：安装 `langchain-community` 后，导入 `BailianChatModel` 并初始化，后续用法与 `ChatOpenAI` 完全一致。示例代码详见 [工具包/框架](../../raw/model-api-reference/toolkits-and-frameworks.md)。  
- 批量任务（`batches`）需先上传文件（`/files`），再提交任务（`/batches`），结果通过轮询 `/batches/{id}` 获取；该流程与 OpenAI Batch API 行为一致，但响应字段命名略有差异（如 `output_file_id` → `result_file_id`）。

## 限制和注意事项

- OpenAI 兼容接口**不支持** `functions` / `tools` 参数（即[函数调用](../concepts/function-calling.md)能力），该能力需通过百炼原生 `tool_call` 接口实现。  
- Vision 接口仅支持 Base64 编码图像，不支持远程 URL；Embedding 接口最大输入长度为 8192 tokens（与 Qwen2-Embedding 一致）。  
- LangChain 封装暂不支持流式响应（`stream=True`），若需流式，建议直接调用 OpenAI 兼容的 `/chat/completions?stream=true` 端点。  
- 所有兼容接口的配额、计费、错误码均遵循百炼平台规则，与 OpenAI 独立结算；具体限额请查阅控制台配额页或 [工具包/框架](../../raw/model-api-reference/toolkits-and-frameworks.md) 中的“限制说明”章节。

## 来源文档

- [工具包/框架](../../raw/model-api-reference/toolkits-and-frameworks.md)


