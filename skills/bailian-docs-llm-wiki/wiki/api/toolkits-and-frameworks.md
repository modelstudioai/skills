# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 OpenAI 兼容的工具集与框架接口，覆盖文本生成、视觉理解、向量嵌入、批量处理、会话管理、文件上传等核心场景。开发者可复用现有 OpenAI SDK 代码，仅需调整 `base_url`、`api_key` 和模型名即可快速迁移，无需重写业务逻辑。

## 支持的模型/功能

百炼支持的 OpenAI 兼容能力按接口类型划分，覆盖广泛模型与功能：

- **Chat Completions**：支持 `qwen3.8-max`、`qwen3.7-plus`、`qwen-vl-plus`、`deepseek-v4-pro`、`glm-5.3`、`kimi-k3` 等主流文本与多模态模型；Qwen-Audio 明确不支持该协议 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- **Responses API**（智能体原生）：专为 Agent 场景优化，内置联网搜索、网页抓取、代码解释器等工具，支持 `qwen3.8-omni-flash` 处理音视频输入 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。
- **Vision（图像理解）**：支持 `qwen3-vl-plus`、`QVQ`、`Qwen-OCR`，兼容 OpenAI 的 `image_url` 结构化输入格式 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。
- **Embedding**：支持 `text-embedding-v4`、`qwen3.7-text-embedding-flash` 等，但**不支持稀疏向量输出**（传入 `output_type=sparse` 将返回空 embedding）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。
- **Completions（FIM）**：仅限华北2（北京）地域，当前仅支持 `qwen-coder-turbo` 模型，用于代码补全与中段填充（Fill-in-the-Middle）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。
- **Conversations & Batch**：Conversations API 用于跨设备上下文管理；Batch 接口分两种形态——`Batch Chat`（单请求同步等待）与 `Batch File`（JSONL 文件异步处理），后者费用为实时调用的 50% [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。

> **注意**：文档 7（Batch File）与文档 8（Batch Chat）对 `qwen3.5-omni-plus` 的语音输出支持描述矛盾：文档 7 称“不支持语音输出”，文档 8 同样声明“不支持语音输出”，二者一致；但文档 2（Responses API）未提及此限制，且明确列出 `qwen3.8-omni-flash` 支持音视频输入。此处以 Omni 系列模型实际能力为准，语音输出能力取决于具体模型变体，非所有 Omni 模型均支持。

## 关键参数

所有 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)共用以下核心参数，行为与 OpenAI 原生一致：

- `model`：必需，模型名称（如 `"qwen3.8-max"`），必须从对应接口支持的模型列表中选取。
- `base_url`：必需，**必须使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- `api_key`：必需，**严格按地域绑定**：北京 endpoint 必须配北京地域创建的 API Key，跨地域使用将返回 `invalid_api_key` 错误 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- `stream` / `stream_options`：控制[流式输出](../concepts/streaming-output.md)，`stream_options={"include_usage": true}` 可在流结束时返回 token 统计。
- `temperature` / `top_p`：二选一设置，避免同时指定导致行为不可控。
- `max_tokens`：仅作截断用，不影响模型内部生成长度。

此外，特定接口有扩展参数：
- **Responses API**：`input`（接受字符串或消息数组）、`previous_response_id`（自动注入上下文）、`tool_choice`。
- **Completions API**：`prompt`（含 `<tool_call>`/`<tool_call>` 分隔符）、`stop`（支持字符串或 token ID 数组）。
- **Batch Chat**：需显式设置客户端超时（如 Python 中 `with_options(timeout=1800.0)`），最长 3600 秒 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。
- **Embedding API**：`dimensions`（仅 `text-embedding-v3/v4` 支持）、`encoding_format`（默认 `"float"`）。

## 使用方式

### 1. 初始化客户端
统一使用 OpenAI SDK（v1.x），配置 `base_url` 和 `api_key`：
```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
```
`{WorkspaceId}` 需替换为控制台「业务空间详情」页获取的实际 ID。

### 2. 按场景调用
- **标准对话**：`client.chat.completions.create(model=..., messages=[...])`
- **智能体任务**：`client.responses.create(model=..., input="...")` 或 `input=[{"role":"user","content":"..."}]`
- **向量计算**：`client.embeddings.create(model="text-embedding-v4", input="...")`
- **文件上传**：`client.files.create(file=Path("doc.pdf"), purpose="file-extract")`
- **批量处理**：
  - 单请求：改用 `base_url="https://batch.dashscope.aliyuncs.com/compatible-mode/v1"`
  - 多请求：先 `client.files.create(..., purpose="batch")`，再 `client.batches.create(input_file_id=..., endpoint="/v1/chat/completions")`
- **会话管理**：`client.conversations.create(items=[...])` → 获取 `id` → 后续请求通过 `previous_response_id` 或 `conversation_id` 关联

### 3. LangChain 集成
推荐双路径：
- **OpenAI 兼容层**（`langchain_openai.ChatOpenAI`）：仅支持部分模型，适合快速验证 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。
- **DashScope 原生层**（`langchain_community.chat_models.tongyi.ChatTongyi`）：支持全部百炼模型，包括部署后模型。

## 限制和注意事项

- **地域强绑定**：API Key 与 `base_url` 所属地域必须一致，否则鉴权失败（HTTP 401，错误码 `invalid_api_key`），与 Key 是否有效无关 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- **域名迁移强制要求**：华北2（北京）、新加坡、中国香港地域已启用业务空间专属域名（含 `{WorkspaceId}`），旧域名虽兼容但**不保证长期可用性**，生产环境必须迁移。
- **模型能力差异**：第三方直供模型（如 SiliconFlow DeepSeek）仅在北京地域可用，且需在控制台单独开通服务 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- **文件限制**：`file-extract` 用途单文件 ≤150 MB；`batch` 用途单文件 ≤500 MB；`fine-tune` 用途单文件 ≤300 MB；总存储上限 100 GB / 10000 文件 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。
- **Batch 超时**：`Batch Chat` 最长等待 3600 秒；`Batch File` 任务最长执行 24 小时（`completion_window="24h"`）。
- **Qwen-Audio 不兼容**：明确不支持 OpenAI Chat 协议，仅支持 DashScope 原生协议 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)


