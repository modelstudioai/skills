# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)及专用工具链，覆盖文本生成、[多模态](../concepts/multi-modal.md)理解、向量嵌入、批量处理、对话状态管理等核心场景。开发者可复用现有 OpenAI SDK 代码，仅需调整 `base_url`、`api_key` 和模型名即可快速迁移；同时支持 LangChain 等主流框架集成，兼顾灵活性与工程效率。

## 支持的模型/功能

- **文本生成**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash` 等全系 Qwen 文本模型，以及 DeepSeek、GLM、Kimi 等第三方直供模型（详见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）。
- **[多模态](../concepts/multi-modal.md)理解**：`qwen3-vl-plus`、`qwen3-vl-flash`、`qwen-vl-ocr` 等视觉模型，支持图像/视频输入与结构化输出（详见 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)）。
- **长上下文与文档处理**：`qwen-long`、`qwen-doc-turbo` 支持基于文件 ID 的问答与信息抽取；`qwen-coder-turbo` 专用于代码补全（FIM 模式）（详见 [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)）。
- **向量嵌入**：`text-embedding-v4`、`qwen3.7-text-embedding` 等全系列 Embedding 模型，支持多语种与高维向量（详见 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)）。
- **智能体与工具调用**：`qwen3.8-max` 等模型通过 Responses API 原生支持联网搜索、网页抓取、代码解释器等内置工具（详见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)）。
- **对话状态管理**：Conversations API 提供会话生命周期管理（创建、更新、删除、追加消息），配合 Responses API 实现跨设备上下文延续（详见 [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)）。

> **注意**：`Qwen-Audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；`qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出，且 `qwen3.5-omni-flash` 同样受限（见 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) 与 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)）。

## 关键参数

| 参数 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `base_url` | string | 必填。服务端点，**必须匹配 API Key 所在地域**。推荐使用业务空间专属域名以获得更高稳定性（如北京：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）。旧版 `dashscope.aliyuncs.com` 域名仍可用但不推荐。 | `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`（Batch Chat）<br>`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（Responses/Chat/Vision） |
| `model` | string | 必填。模型名称，需严格匹配支持列表，大小写敏感。不同接口支持范围不同（如 `qwen-coder-turbo` 仅支持 `completions` 接口）。 | `"qwen3.8-max"`, `"qwen3-vl-plus"`, `"text-embedding-v4"` |
| `enable_thinking` | boolean | 可选（Batch 场景关键）。控制是否启用思考模式（产生 reasoning tokens）。`qwen3.5+` 系列默认开启，建议显式设置为 `false` 以控本（见 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)）。 | `false` |
| `previous_response_id` | string | Responses API 专用。传入上一轮响应的顶层 `id`（UUID 格式），用于自动上下文注入，替代手动维护 message history（见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)）。 | `"0c842a11-c7d1-45da-b7ec-4e668c389xxx"` |
| `purpose` | string | 文件接口专用。决定文件用途：`file-extract`（文档分析）、`batch`（批量推理输入）、`fine-tune`（调优数据集）（见 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)）。 | `"file-extract"` |

## 使用方式

### 1. OpenAI SDK 集成（推荐）
所有兼容接口均支持标准 OpenAI SDK（Python/Node.js/Java/Go/C# 等）。核心步骤：
- 安装 SDK：`pip install -U openai`（Python）或对应语言包；
- 配置 `api_key`（建议环境变量 `DASHSCOPE_API_KEY`）；
- 设置 `base_url` 为对应接口的专属地址（如 Batch Chat 用 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`）；
- 调用对应方法：`client.chat.completions.create()`、`client.responses.create()`、`client.embeddings.create()`、`client.files.create()`、`client.conversations.create()` 等。

示例（Responses API 基础调用）：
```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
response = client.responses.create(model="qwen3.8-max", input="你好")
print(response.output_text)
```

### 2. LangChain 集成
- **OpenAI 方式**：使用 `langchain_openai.ChatOpenAI`，仅支持部分模型，配置同 SDK（见 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)）。
- **DashScope 原生方式**：使用 `langchain_community.chat_models.tongyi.ChatTongyi`，支持全部百炼文本模型及部署模型，需额外安装 `dashscope` 包。

### 3. HTTP 直连
适用于无 SDK 环境。构造 `POST` 请求，`Authorization: Bearer $DASHSCOPE_API_KEY`，`Content-Type: application/json`，Body 为标准 JSON。各接口 endpoint 见对应文档（如 `/compatible-mode/v1/responses`, `/compatible-mode/v1/chat/completions`, `/compatible-mode/v1/embeddings`）。

## 限制和注意事项

- **地域绑定强制**：API Key 与 `base_url` 地域必须严格一致。例如，北京地域 Key 不能调用弗吉尼亚 `base_url`，否则返回 `invalid_api_key`（HTTP 401），而非密钥失效（见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）。
- **路径已迁移**：Responses API 旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 和 Conversations API 旧路径 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 已停止维护，**必须迁移至新版 `/compatible-mode/v1/{endpoint}`**。
- **模型能力差异**：非阿里云百炼直供模型（如部分第三方模型）仅支持基础兼容能力，Agent 功能（内置工具、复杂 reasoning）受限（见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)）。
- **文件配额**：文件上传服务总容量上限 100 GB，文件数上限 10,000 个。达上限后新上传失败，需手动清理（见 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)）。
- **Embedding 稀疏向量限制**：[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)不支持 `output_type=sparse`，传入该参数将导致 embedding 结果为空（HTTP 200），需改用 DashScope 原生接口（见 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)）。

## 来源文档

- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)


