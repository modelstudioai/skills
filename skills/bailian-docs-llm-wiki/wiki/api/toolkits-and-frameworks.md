# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)工具包与框架，覆盖文本生成、视觉理解、向量嵌入、批量处理、会话管理等核心场景。开发者可复用现有 OpenAI SDK 代码，仅需调整 `base_url`、`api_key` 和模型名即可快速迁移，无需重写业务逻辑。所有兼容接口均支持主流编程语言（Python/Node.js/Java/Go/C#/JavaScript）及 HTTP 直调。

## 支持的模型/功能

百炼 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)支持以下模型类别与能力：

- **文本生成**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash` 等全系 Qwen 大模型，以及 DeepSeek、GLM、Kimi、MiniMax 等第三方直供模型（详见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）；
- **视觉理解**：`qwen3-vl-plus`、`qwen3-vl-flash`、`qwen-vl-ocr`，支持图文混合输入与结构化输出（详见 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)）；
- **向量嵌入**：`text-embedding-v4`、`qwen3.7-text-embedding` 等，支持多维度、多语种文本向量化（详见 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)）；
- **批量处理**：支持单请求同步等待（Batch Chat）与文件异步提交（Batch File），适用于数据标注、评测等非实时场景（详见 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)）；
- **会话管理**：`Conversations API` 提供跨设备上下文持久化能力，配合 `Responses API` 实现自动历史注入（详见 [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)）；
- **专用任务**：`completions` 接口专用于代码补全与 FIM（Fill-in-the-Middle）场景，仅支持 `qwen-coder-turbo`；`file` 接口支持文档问答（Qwen-Long/Qwen-Doc-Turbo）与批量/微调任务文件上传（详见 [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md) 和 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)）。

> **注意**：`Qwen-Audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议（见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）；`Responses API` 的旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停用，必须迁移到 `/compatible-mode/v1/responses`（见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)）。

## 关键参数

所有 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)共用以下核心参数：

- `base_url`：必须配置为地域专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），其中 `{WorkspaceId}` 需替换为控制台获取的实际业务空间 ID。旧域名（如 `https://dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低，**强烈建议迁移**；
- `api_key`：按地域绑定，北京地域 Key 无法调用弗吉尼亚 endpoint，否则返回 `invalid_api_key` 错误（见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）；
- `model`：必须使用百炼支持的模型名（如 `qwen3.8-max`），非列表中模型可能缺失 Agent 能力或完全不可用；
- `stream` 与 `stream_options`：[流式输出](../concepts/streaming-output.md)需显式设置 `stream=True`，并可通过 `{"include_usage": true}` 在末尾 chunk 返回 token 统计；
- `enable_thinking`：对 `qwen3.5+` 系列模型，默认开启思考模式，显式传入 `enable_thinking=false` 可关闭以降低成本（见 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)）；
- `dimensions`：仅 `text-embedding-v3/v4` 支持该参数，用于指定向量维度（见 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)）。

## 使用方式

### 1. 初始化客户端
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 推荐环境变量方式
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
```

### 2. 按场景选择接口
- **标准对话**：`client.chat.completions.create(model=..., messages=[...])`
- **简化智能体**：`client.responses.create(model=..., input="...")`（支持内置工具）
- **长文档问答**：先 `client.files.create(file=..., purpose="file-extract")`，再在 `messages` 中引用 `file_id`
- **批量处理**：
  - 单请求：`base_url="https://batch.dashscope.aliyuncs.com/compatible-mode/v1"` + `chat.completions.create(...)`
  - 文件异步：`client.files.create(purpose="batch")` → `client.batches.create(input_file_id=..., endpoint="/v1/chat/completions")`
- **向量计算**：`client.embeddings.create(model="text-embedding-v4", input="...")`
- **会话管理**：`client.conversations.create(items=[...])` → 后续请求通过 `previous_response_id` 或 `conversation_id` 关联

### 3. LangChain 集成
- **OpenAI 兼容层**（部分模型）：`langchain_openai.ChatOpenAI(...)`，需配置 `base_url`；
- **DashScope 原生层**（全模型支持）：`langchain_community.chat_models.tongyi.ChatTongyi(...)`，需安装 `dashscope` 包（见 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)）。

## 限制和注意事项

- **地域隔离**：API Key 与 `base_url` 地域必须严格匹配，跨地域调用将被鉴权拒绝（HTTP 401），错误码为 `invalid_api_key`；
- **模型能力差异**：`Responses API` 的 Agent 能力（联网搜索、代码解释器等）仅对 `qwen3.8-*`、`qwen3.7-*` 等直供模型完整支持，第三方模型（如 DeepSeek）仅支持基础 chat 功能；
- **文件限制**：`file-extract` 单文件 ≤150 MB，`batch` 单文件 ≤500 MB，`fine-tune` 单文件 ≤300 MB；总存储上限为 10,000 文件 / 100 GB；
- **Embedding 限制**：OpenAI 兼容接口不支持稀疏向量（`output_type=sparse`），传入该参数将导致 embedding 字段为空（见 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)）；
- **超时控制**：Batch Chat 默认超时 3600 秒，需通过 SDK 的 `timeout` 参数或 HTTP `timeout` header 显式设置；
- **[Token](../concepts/token.md) 计费**：`qwen3.5+` 系列模型默认启用思考模式，`usage.output_tokens_details.reasoning_tokens` 将计入费用，务必评估是否需关闭 `enable_thinking`。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)


