# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 OpenAI 兼容的工具包与框架接口，覆盖文本、视觉、向量、批量推理、会话管理等核心场景。开发者可复用现有 OpenAI SDK 代码，仅需调整 `base_url`、`api_key` 和 `model` 参数即可快速迁移。所有接口均支持主流编程语言（Python/Node.js/Java/Go/C#/etc）及 HTTP 直调。

## 支持的模型/功能

- **文本生成**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash` 等全系列 Qwen 模型，以及 DeepSeek、GLM、Kimi、MiniMax 等三方直供模型（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）。
- **视觉理解**：`qwen3-vl-plus`、`QVQ`、`Qwen-OCR`，支持图像 URL 与 Base64 输入（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)）。
- **向量嵌入**：`text-embedding-v4`、`qwen3.7-text-embedding` 等，支持多语种与可选维度（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)）。
- **批量处理**：支持文件输入（JSONL）和单请求同步 Batch Chat 两种模式，成本降低 50%（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)）。
- **智能体增强**：Responses API 内置联网搜索、网页抓取、代码解释器等工具；Conversations API 提供跨设备上下文持久化能力。
- **文件管理**：`files.create` 支持 `file-extract`（文档问答）、`batch`（批量任务）、`fine-tune`（调优数据集）三类用途。

> **注意**：`Qwen-Audio` 不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议（见 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）；`qwen3.8-omni-flash` 处理音视频输入时需使用 Omni 专用调用指南，而非标准 `/chat/completions`。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `base_url` | 必填，地域专属业务空间域名，**非旧版 `dashscope.aliyuncs.com`** | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `api_key` | 必填，**严格按地域绑定**：北京地域 Key 不能调用弗吉尼亚 endpoint（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)） | `sk-xxx`（从控制台业务空间详情页获取） |
| `model` | 必填，模型名需与所选接口能力匹配（如 Vision 接口仅支持 `qwen3-vl-plus`） | `qwen3.8-max`, `qwen3-vl-plus`, `text-embedding-v4` |
| `purpose`（文件接口） | 必填，决定文件用途：`file-extract` / `batch` / `fine-tune` | `file-extract` |
| `enable_thinking`（Batch） | 可选布尔值，控制是否启用思考模式（影响 token 成本），须与 `model` 同级传入 | `false` |

## 使用方式

1. **初始化客户端**：配置 `api_key`（推荐环境变量）与 `base_url`（含 `{WorkspaceId}` 占位符）；
2. **选择接口**：
   - 文本/视觉/Embedding：调用 `client.chat.completions.create()` / `client.embeddings.create()`；
   - 批量任务：使用 `client.files.create(purpose="batch")` + `client.batches.create()`（文件输入）或直接 `client.chat.completions.create()`（同步 Batch Chat）；
   - 会话管理：通过 `client.conversations.create()` 创建会话，再用 `client.conversations.items.create()` 追加消息；
   - Responses API：调用 `client.responses.create(input="...")`，支持 `previous_response_id` 自动续写；
3. **流式/非流式**：`stream=True` 启用[流式输出](../concepts/streaming-output.md)；Responses API 的 `stream_options={"include_usage": True}` 可在末尾返回 token 统计。

## 限制和注意事项

- **地域隔离**：API Key 与 `base_url` 地域必须严格一致，跨地域调用将返回 `invalid_api_key` 错误（HTTP 401），而非权限不足（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）。
- **域名迁移**：华北2（北京）、新加坡、中国香港已启用业务空间专属域名（`{WorkspaceId}.xxx.maas.aliyuncs.com`），旧域名虽可用但**性能与稳定性较低，强烈建议迁移**。
- **文件配额**：文件存储上限为 10,000 个文件且总大小 ≤ 100 GB；单文件大小限制依 `purpose` 而异：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB。
- **Batch 特性**：`qwen3.8`/`qwen3.7`/`qwen3.6`/`qwen3.5` 系列模型默认开启思考模式，若无需思考 token，务必显式设置 `enable_thinking=False`（该参数不可置于 `extra_body` 中）。
- **LangChain 集成**：`langchain_openai` 仅支持部分模型（如 `qwen-plus`），而 `langchain_community.chat_models.tongyi.ChatTongyi` 支持全部百炼文本模型（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)）。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)


