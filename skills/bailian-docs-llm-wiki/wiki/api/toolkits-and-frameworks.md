# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 [OpenAI 兼容接口](../concepts/openai-compatibility.md)工具包与框架，覆盖文本生成、视觉理解、向量嵌入、批量推理、文件管理、会话状态管理等核心场景。开发者可复用现有 OpenAI SDK 代码，仅需调整 `base_url`、`api_key` 和 `model` 参数即可快速迁移。所有接口均支持标准 OpenAI SDK（Python/Node.js/Java/Go/C#）及 HTTP 调用方式。

## 支持的模型/功能

百炼兼容接口支持以下模型类别与能力：

- **文本生成**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash` 等全系列 Qwen 大语言模型，以及 DeepSeek、GLM、Kimi、MiniMax 等三方直供模型（仅限华北2地域）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；
- **视觉理解**：`qwen3-vl-plus`、`QVQ`、`Qwen-OCR`，支持图像+文本多模态输入与[流式输出](../concepts/streaming.md) [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)；
- **向量嵌入**：`text-embedding-v4`、`qwen3.7-text-embedding` 等，支持多维度配置与 201 种语种 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)；
- **长上下文与文档处理**：`Qwen-Long`、`Qwen-Doc-Turbo`，需通过文件上传接口预处理 PDF/DOCX/TXT 等格式 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)；
- **智能体与工具调用**：`Responses API` 内置联网搜索、网页抓取、代码解释器等原生工具能力，优于基础 Chat Completions [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)；
- **代码补全**：`qwen-coder-turbo-latest` 专用 `completions` 接口，支持 Fill-in-the-Middle（FIM）模式 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。

> **注意**：`Qwen-Audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；`qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出，该限制在 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) 和 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md) 中表述一致，但未在 Responses API 文档中说明，属功能边界差异，非矛盾。

## 关键参数

所有兼容接口共用以下核心参数，行为与 OpenAI 官方一致：

- `model`：必需，模型名称（如 `"qwen3.8-max"`、`"text-embedding-v4"`），须从各接口支持列表中选取；
- `base_url`：必需，**必须使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低；
- `api_key`：必需，**严格按地域绑定**：北京地域 API Key 无法调用弗吉尼亚 endpoint，否则返回 `invalid_api_key` 错误码 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；
- `stream`：布尔值，控制是否启用流式响应，默认 `false`；
- `stream_options`：对象，设 `{"include_usage": true}` 可在流式末尾返回 token 统计；
- `temperature` / `top_p`：二选一设置，避免同时指定；
- `max_tokens`：仅作截断控制，不影响模型内部生成逻辑；
- `seed`：整数，用于确定性输出，取值范围 `0–2^31−1`。

特殊参数：
- `Responses API` 支持 `previous_response_id` 实现自动上下文关联；
- `Conversations API` 支持 `items` 数组初始化会话消息；
- `Embedding API` 支持 `dimensions`（仅 v3/v4）和 `encoding_format`；
- `Batch Chat` 需显式设置客户端超时（如 Python 的 `.with_options(timeout=1800.0)`），最长 3600 秒；
- `Batch File` 的 JSONL 输入中，`enable_thinking` 必须与 `model` 同级，不可置于 `extra_body`。

## 使用方式

### 1. SDK 初始化（通用）
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 强烈建议环境变量配置
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
```
> `{WorkspaceId}` 须替换为控制台「业务空间详情」页获取的实际 ID。

### 2. 接口调用映射
| 功能 | 接口路径 | SDK 方法 | 典型用途 |
|------|----------|----------|----------|
| 标准对话 | `/chat/completions` | `client.chat.completions.create()` | 通用 LLM 调用 |
| 智能体对话 | `/responses` | `client.responses.create()` | 内置工具链、简化历史管理 |
| 向量嵌入 | `/embeddings` | `client.embeddings.create()` | RAG、语义检索 |
| 文件上传 | `/files` | `client.files.create()` | 文档问答、批量任务输入 |
| 批量推理（单请求） | `/chat/completions`（batch domain） | `client.chat.completions.create()`（`base_url=https://batch.dashscope.aliyuncs.com/...`） | 低成本异步单次调用 |
| 批量推理（文件） | `/batches` | `client.batches.create()` | 大规模评测、数据标注 |
| 会话管理 | `/conversations` | `client.conversations.*()` | 跨设备上下文持久化 |

### 3. LangChain 集成
- **OpenAI 兼容层**（`langchain_openai`）：仅支持部分模型（如 `qwen-plus`），适合快速验证 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)；
- **DashScope 原生层**（`langchain-community` + `dashscope`）：支持全部模型（含 `Qwen-Long`、`Qwen-VL`），推荐生产使用。

## 限制和注意事项

- **地域强绑定**：API Key 与 `base_url` 所属地域必须一致，跨地域调用必然失败（HTTP 401 + `invalid_api_key`），此规则适用于所有接口 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；
- **域名迁移强制要求**：华北2（北京）、新加坡、中国香港地域已上线业务空间专属域名，旧域名（`dashscope.aliyuncs.com`）将逐步淘汰，新项目必须使用 `{WorkspaceId}.xxx.maas.aliyuncs.com` 格式；
- **模型能力差异**：非阿里云直供模型（如三方 DeepSeek/Kimi）在 Responses API 中 Agent 能力受限，仅支持基础文本生成；
- **文件服务配额**：总文件数 ≤ 10,000 个，总大小 ≤ 100 GB，无自动过期机制，需手动清理；
- **Batch 超时**：`Batch Chat` 最长等待 3600 秒，`Batch File` 任务最长执行时间由 `completion_window` 指定（如 `"24h"`），超时后状态变为 `expired`；
- **视觉模型限制**：`QVQ` 仅支持[流式输出](../concepts/streaming.md)，非流式调用将失败；
- **Embedding 稀疏向量**：[OpenAI 兼容接口](../concepts/openai-compatibility.md)不支持 `output_type=sparse`，需改用 DashScope 原生接口；
- **[函数调用](../concepts/function-calling.md)（Function Calling）**：仅 `Chat Completions` 和 `Responses` 接口支持，`completions`（文本补全）接口不支持。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)


