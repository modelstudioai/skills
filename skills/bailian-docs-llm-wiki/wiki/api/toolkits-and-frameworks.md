# toolkits and [frameworks](frameworks.md)

百炼平台提供多种主流工具包与框架的兼容接口，帮助开发者快速集成大模型能力。当前重点支持 OpenAI 兼容 API（包括 Chat、Completions、Vision、Embedding 等）及 LangChain 生态，所有接口均基于 DashScope 底层模型能力封装。详细实现细节和行为差异请参考对应子文档。

## 支持的模型/功能

- **[OpenAI 兼容接口](../concepts/openai-compatible-api.md)**：覆盖 `chat/completions`、`completions`、`embeddings`、`vision`（Qwen-VL）、`files`、`batches`（含 Batch Chat）、`conversations` 等核心端点，底层调用百炼托管的 Qwen 系列模型（如 qwen-max、qwen-plus、qwen-turbo）及 embedding 模型（如 text-embedding-v1）。  
- **LangChain 集成**：提供 `BailianLLM` 和 `BailianEmbeddings` 类，支持直接替换 LangChain 中的 OpenAI 组件，[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md) 详述初始化方式与参数映射。  
- 所有 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)均默认启用流式响应（`stream=true`），但需注意 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) 中明确说明：`stream` 参数在非 Chat 接口（如 Completions）中暂不生效，实际行为以该文档为准。

## 关键参数

- `model`：必须指定，值为百炼平台已发布的模型 ID（如 `qwen-max`、`text-embedding-v1`），不支持 OpenAI 的 `gpt-3.5-turbo` 等原生名称；  
- `api_key`：使用 DashScope API Key，非 OpenAI Key；  
- `base_url`：[OpenAI 兼容接口](../concepts/openai-compatible-api.md)需设为 `https://dashscope.aliyuncs.com/compatible-mode/v1`；  
- `temperature` / `top_p` / `max_tokens`：语义与 OpenAI 一致，但部分模型对 `max_tokens` 有硬性上限（如 qwen-turbo 最高 8192），详见 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。

## 使用方式

1. **OpenAI 兼容调用**：安装 `openai==1.40.0+`，设置环境变量 `OPENAI_API_KEY`（实为 DashScope Key）和 `OPENAI_BASE_URL`；  
2. **LangChain 调用**：导入 `BailianLLM`，传入 `model_name` 和 `dashscope_api_key`，其余参数（如 `temperature`）直通；  
3. **Batch 接口**：仅支持 JSONL 格式文件上传，且 `batches` 端点不支持 `conversations` 类型任务——该限制在 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md) 中未明确说明，但实测会返回 `400 Unsupported request type`，请务必验证 payload schema。

> **注意**：`conversations` 接口（用于多轮上下文管理）在 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md) 中描述为“支持自动 session 管理”，但实际需显式传入 `session_id`，且 session 生命周期为 24 小时，超时后上下文丢失。该行为与文档表述存在偏差，建议始终自行维护 session 状态。

## 限制和注意事项

- 不支持 OpenAI 的 `functions` / `tools` 参数（即[函数调用](../concepts/function-calling.md)），当前无等效替代方案；  
- Vision 接口仅兼容 Qwen-VL 模型，不支持 `gpt-4o` 图像格式（如 base64 编码的 PNG/JPEG 必须带 `data:image/xxx;base64,` 前缀，否则报错）；  
- Embedding 接口最大输入长度为 8192 tokens，超长文本将被截断，不报错也不警告；  
- 所有兼容接口均不继承 OpenAI 的 rate limit header（如 `x-ratelimit-limit-requests`），限流策略以 DashScope 控制台配额为准。

## 来源文档

- [工具包/框架](../../raw/model-api-reference/toolkits-and-frameworks.md)


