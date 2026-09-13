# toolkits and frameworks

百炼平台提供多种主流工具包与框架的兼容接口，便于开发者复用已有代码和生态。当前重点支持 OpenAI 兼容 API（覆盖 Chat、Completions、Vision、Embedding 等核心能力）及 LangChain 集成。所有接口均基于 DashScope 底层模型能力封装，需通过 `Authorization: Bearer <api_key>` 认证。

## 支持的模型/功能

- **[OpenAI 兼容接口](../concepts/openai-compatibility.md)**：完整支持 `chat/completions`、`completions`、`embeddings`、`vision`（Qwen-VL）、`files`、`batches`（含 Batch Chat）、`conversations` 等端点，对应底层模型包括 Qwen 系列（如 qwen-max、qwen-plus）、Qwen-VL 和 text-embedding-v1。  
- **LangChain 集成**：提供 `BailianChatModel` 和 `BailianEmbeddings` 等原生封装类，适配 LangChain v0.1.x 的 `Runnable` 与 `BaseLLM` 接口规范。详情见 [LangChain](../../raw/model-api-reference/toolkits-and-frameworks.md)。  
- 所有 [OpenAI 兼容接口](../concepts/openai-compatibility.md)均映射至百炼实际可用模型，例如 `/v1/chat/completions` 默认路由到 `qwen-max`，但可通过 `model` 参数显式指定（如 `qwen-plus`）。该行为在 [OpenAI兼容-Chat](../../raw/model-api-reference/toolkits-and-frameworks.md) 和 [OpenAI兼容-Completions](../../raw/model-api-reference/toolkits-and-frameworks.md) 中均有说明。

## 关键参数

- `model`：必需，取值必须为百炼平台当前启用的模型 ID（如 `qwen-max`），不支持 OpenAI 原生模型名（如 `gpt-4`）。  
- `temperature` / `top_p` / `max_tokens`：语义与 OpenAI 一致，但部分模型对 `max_tokens` 有硬性上限（如 `qwen-plus` 最高支持 8192）。  
- `response_format`：仅 `chat/completions` 支持 `{"type": "json_object"}`，需配合 `qwen-max` 或 `qwen-plus` 使用；其他模型返回 400 错误。  
- `file_id` / `batch_id`：用于文件与批量接口，ID 须通过 `/files` 或 `/batches` 创建后获取，详见 [OpenAI兼容-File](../../raw/model-api-reference/toolkits-and-frameworks.md) 和 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks.md)。

## 使用方式

- **HTTP 调用**：所有 [OpenAI 兼容接口](../concepts/openai-compatibility.md)统一使用 `https://dashscope.aliyuncs.com/api/v1/` 基地址，Header 中设置 `Content-Type: application/json` 和 `Authorization: Bearer <api_key>`。  
- **SDK 调用**：推荐使用 `dashscope` Python SDK（≥1.20.0），自动识别 `openai` 兼容模式：  
  ```python
  from openai import OpenAI
  client = OpenAI(api_key="sk-xxx", base_url="https://dashscope.aliyuncs.com/api/v1/")
  response = client.chat.completions.create(model="qwen-max", messages=[{"role":"user","content":"Hello"}])
  ```  
- **LangChain**：安装 `langchain-community` 后直接导入：  
  ```python
  from langchain_community.chat_models import BailianChatModel
  llm = BailianChatModel(model_name="qwen-plus", api_key="sk-xxx")
  ```

## 限制和注意事项

- 所有 OpenAI 兼容接口**不支持流式响应（`stream=true`）的 Server-Sent Events (SSE) 格式**，仅返回标准 JSON 响应（`stream=false` 强制生效）。此限制未在 [OpenAI兼容-Chat](../../raw/model-api-reference/toolkits-and-frameworks.md) 文档中明确说明，但实测与服务端行为一致。  
- `batches` 接口当前仅支持 `chat/completions` 类型任务，不支持 `completions` 或 `embeddings` 批量提交——这与 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks.md) 描述一致，但 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks.md) 标题易引发歧义，实际不支持非 chat 类型。  
- > **注意**：LangChain 文档中提及的 `BailianChatModel` 在 `langchain-community>=0.2.0` 中已重命名为 `DashScopeChatModel`，旧类名仅兼容至 `0.1.13`。请以 [LangChain](../../raw/model-api-reference/toolkits-and-frameworks.md) 当前链接文档为准，并检查所用版本。

## 来源文档

- [工具包/框架](../../raw/model-api-reference/toolkits-and-frameworks.md)


