# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 OpenAI 兼容的工具包与框架接口，覆盖文本生成、视觉理解、嵌入向量、批量处理、文件管理及智能体原生能力等场景。开发者可复用现有 OpenAI SDK 代码，仅需调整 `base_url`、`api_key` 和模型名即可快速迁移，无需重写业务逻辑。所有兼容接口均支持主流编程语言（Python/Node.js/Java/Go/C#/JavaScript）及 HTTP 直调。

## 支持的模型/功能

百炼 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)支持三大类能力：  
- **通用对话**：通过 `chat/completions` 接口调用 Qwen 系列（如 `qwen3.8-max`、`qwen-plus`）、DeepSeek、GLM、Kimi 等模型，支持 `function_call`、[流式输出](../concepts/streaming-output.md)、系统提示等完整 Chat API 功能 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；  
- **多模态理解**：`qwen-vl-plus`、`qwen3-vl-plus`、`QVQ`、`Qwen-OCR` 等视觉模型支持图像输入（URL 或 Base64），兼容 OpenAI Vision 规范 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)；  
- **专用能力接口**：`completions` 接口专用于代码补全（如 `qwen-coder-turbo`）；`responses` 接口提供内置工具链（联网搜索、网页抓取等）和上下文自动管理；`embeddings` 接口支持 `text-embedding-v4`、`qwen3.7-text-embedding` 等向量模型；`files` 接口统一管理文档分析、批量任务与微调数据集 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。

> **注意**：`Qwen-Audio` 不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；多模态 Embedding 模型（如 `qwen3-vl-embedding`）亦不支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，需使用 DashScope 专用 API。

## 关键参数

所有 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)共用以下核心参数：  
- `base_url`：必须按地域配置专属域名（如北京为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低；  
- `api_key`：严格按地域绑定，北京地域 API Key 无法调用弗吉尼亚 endpoint，否则返回 `invalid_api_key` 错误；  
- `model`：需从各接口支持的模型列表中选择，例如 `responses` 接口仅支持 `qwen3.8-max` 等特定版本，而 `completions` 接口仅支持 `qwen-coder-turbo`；  
- `stream` 与 `stream_options={"include_usage": true}`：控制[流式输出](../concepts/streaming-output.md)及 [Token](../concepts/token.md) 统计是否在末尾返回；  
- `enable_thinking`：对 `qwen3.x` 系列模型为顶层参数（与 `model` 同级），用于显式开关思考模式，避免隐式成本增加。

## 使用方式

### SDK 调用（推荐）
安装对应 SDK 后，初始化客户端时传入 `base_url` 和环境变量 `DASHSCOPE_API_KEY`：  
- **OpenAI SDK**：适用于 `chat/completions`、`completions`、`embeddings`、`files`、`batch` 等接口，示例见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；  
- **LangChain 集成**：`langchain_openai` 适配部分模型，`langchain_community.chat_models.tongyi`（或 `@langchain/community/chat_models/alibaba_tongyi`）支持全部百炼文本模型，含流式、工具调用等高级特性 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)；  
- **Batch Chat**：将 `base_url` 替换为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1` 即可切换为同步批量模式，超时时间需显式设置（最长 3600 秒）[OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。

### HTTP 直调
直接构造 `POST` 请求，Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，Body 为 JSON 格式参数。Endpoint 路径需与接口类型匹配（如 `/chat/completions`、`/embeddings`、`/responses`），详见各文档的 cURL 示例。

## 限制和注意事项

- **地域隔离**：API Key 与 `base_url` 地域必须严格一致，跨地域调用必鉴权失败；  
- **文件上传限制**：`files` 接口按 `purpose` 区分用途——`file-extract`（文档分析）单文件 ≤150 MB，`batch`（批量任务）≤500 MB，`fine-tune`（微调）≤300 MB；总存储上限为 100 GB / 10000 文件；  
- **Batch 与 Batch Chat 差异**：`Batch`（文件输入）为异步任务，适合万级请求；`Batch Chat` 为同步长连接，仅支持单请求，响应延迟最高 3600 秒；  
- **模型能力差异**：`responses` 接口的 Agent 工具能力仅对阿里云直供模型（如 `qwen3.8-max`）完整支持，第三方模型（如 `deepseek-v4-pro`）仅保留基础兼容性；  
- **Embedding 特殊约束**：`text-embedding-v4` 的 `dimensions` 参数仅在 OpenAI 兼容接口中生效，`output_type=sparse` 不被支持，需改用 DashScope 原生接口。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)


