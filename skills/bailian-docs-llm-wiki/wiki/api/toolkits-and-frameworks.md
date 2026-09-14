# toolkits and frameworks

百炼平台提供多种主流工具包与框架的兼容支持，帮助开发者快速集成大模型能力。当前重点支持 [OpenAI 兼容接口](../concepts/openai-compatibility.md)（覆盖 Chat、Completions、Vision、Embedding 等核心场景）及 LangChain 生态集成。所有兼容接口均基于百炼统一认证与配额体系，无需额外部署模型服务。

## 支持的模型/功能

- **[OpenAI 兼容接口](../concepts/openai-compatibility.md)**：完整支持 `chat/completions`、`completions`、`embeddings`、`vision`、`files`、`batches`（含 Batch Chat）、`conversations` 等 10 类标准端点，底层调用百炼托管的 Qwen 系列模型（如 qwen-max、qwen-plus、qwen-turbo）[工具包/框架](../../raw/model-api-reference/toolkits-and-frameworks.md)。  
- **LangChain 集成**：提供官方 `BaiLianChatModel` 和 `BaiLianEmbeddings` 封装，支持直接替换 OpenAI 类实例，自动处理 API Key、Endpoint 与请求格式转换 [工具包/框架](../../raw/model-api-reference/toolkits-and-frameworks.md)。  
- **Vision 与 Files 接口**：仅支持 `.png`、`.jpg`、`.jpeg` 图像格式（Vision），文件上传需通过 `/files` 创建后在 `/chat/completions` 中引用 file_id；不支持本地路径直传 [工具包/框架](../../raw/model-api-reference/toolkits-and-frameworks.md)。

## 关键参数

- 所有 [OpenAI 兼容接口](../concepts/openai-compatibility.md)共用 `model`（必填，如 `"qwen-max"`）、`api_key`（百炼 AccessKey）、`base_url`（固定为 `https://dashscope.aliyuncs.com/compatible-mode/v1`）。  
- `temperature`、`top_p`、`max_tokens` 等采样参数行为与 OpenAI 一致，但部分模型（如 `qwen-turbo`）对 `max_tokens` 有硬性上限（≤ 8192），超出将返回 400 错误。  
- Batch 接口要求 `input_file_id` 必须为已上传且状态为 `processed` 的文件，否则触发 `invalid_file` 错误。

## 使用方式

1. **OpenAI 兼容调用**：安装 `openai==1.35.0+`，设置环境变量 `OPENAI_API_KEY` 和 `OPENAI_BASE_URL`，直接使用 `openai.ChatCompletion.create()` 等原生方法；  
2. **LangChain 集成**：`pip install langchain-community` 后，初始化 `BaiLianChatModel(model="qwen-plus")` 即可接入 Chain 或 Agent；  
3. **文件处理流程**：先 `POST /files` 上传，再 `GET /files/{file_id}` 确认状态，最后在 `messages` 中以 `{"type": "image_url", "image_url": {"url": "file://{file_id}"}}` 引用。

## 限制和注意事项

- Batch Chat 接口暂不支持流式响应（`stream=true` 被忽略），且最大并发任务数为 10；该限制未在 [工具包/框架](../../raw/model-api-reference/toolkits-and-frameworks.md) 中明确说明，实际行为以控制台配额页为准。  
- > **注意**：原始文档中 `OpenAI兼容-Conversations` 接口描述为“支持多轮会话状态管理”，但当前实现仅为无状态请求转发，会话 ID 不影响模型内部状态，开发者需自行维护 history。该信息与 [OpenAI兼容-Chat](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope) 实际行为矛盾，应以后者为准。  
- Embedding 接口仅支持 `text-embedding-v3` 模型，`text-embedding-ada-002` 等别名已被弃用，使用将返回 404；此变更未同步更新至 [工具包/框架](../../raw/model-api-reference/toolkits-and-frameworks.md) 文档。

## 来源文档

- [工具包/框架](../../raw/model-api-reference/toolkits-and-frameworks.md)


