# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 OpenAI 兼容的工具包与框架接口，覆盖文本生成、多模态理解、向量化、批量推理、会话管理等核心场景。开发者可复用现有 OpenAI 生态（如 SDK、LangChain、LangChain4j）快速迁移，仅需调整 `base_url`、`api_key` 和模型名称即可接入，无需重写业务逻辑。所有兼容接口均支持标准 OpenAI 请求/响应格式，并在稳定性、性能和地域扩展性上持续优化。

## 支持的模型/功能

百炼 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)覆盖全栈能力：

- **文本生成**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash` 等 Qwen 系列主流模型，以及 DeepSeek、GLM、Kimi、MiniMax 等三方直供模型（仅限华北2北京地域）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；
- **多模态理解**：`qwen3-vl-plus`、`QVQ`、`Qwen-OCR` 支持图像/视频输入；`qwen3.8-omni-flash` 支持音视频输入 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)；
- **向量嵌入**：`text-embedding-v4`、`qwen3.7-text-embedding`、`text-embedding-v2` 等，支持 64–2048 维可选输出，覆盖 201 种语种 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)；
- **长文档与结构化处理**：`Qwen-Long`（长上下文问答）、`Qwen-Doc-Turbo`（文档数据提取）通过文件 ID 调用；
- **智能体与工具调用**：`Responses API` 内置联网搜索、网页抓取、代码解释器等原生工具能力，`Chat Completions API` 支持标准 `function_call` 协议；
- **会话持久化**：`Conversations API` 提供跨设备上下文同步，配合 `Responses API` 的 `previous_response_id` 实现无状态对话延续。

> **注意**：`Qwen-Audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；`qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出，该限制未在 Conversations 或 Vision 文档中提及，属功能不一致。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `base_url` | 必填，服务端点，**必须匹配 API Key 所属地域** | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `model` | 必填，模型名称，区分大小写且严格匹配文档列表 | `"qwen3.8-max"`, `"text-embedding-v4"` |
| `purpose`（文件接口） | 必填，指定文件用途 | `"file-extract"`（文档分析）、`"batch"`（批量任务）、`"fine-tune"`（调优） |
| `dimensions`（Embedding） | 可选，仅 `text-embedding-v3/v4` 支持，指定向量维度 | `1024` |
| `enable_thinking`（Batch） | 可选，控制是否启用思考模式（影响 token 计费），须与 `model` 同级传入 | `false` |
| `previous_response_id`（Responses） | 可选，用于多轮对话上下文关联，传入上一轮响应的顶层 `id`（UUID 格式） | `"0c842a11-c7d1-45da-b7ec-4e668c389xxx"` |

> **注意**：`enable_thinking` 参数在 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) 和 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md) 中均强调“必须为 `body` 顶层参数”，但部分旧版示例代码将其置于 `extra_body`，存在误导风险。

## 使用方式

### 1. SDK 配置（通用）
```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 推荐环境变量配置
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
```
- `{WorkspaceId}` 从控制台「业务空间详情」获取；
- 各地域 API Key **不可混用**：北京 Key 仅能调用北京 `base_url`，否则返回 `invalid_api_key`（非密钥失效）。

### 2. 接口调用映射
| 功能 | OpenAI 方法 | 百炼 endpoint | 说明 |
|------|-------------|----------------|------|
| 文本生成 | `client.chat.completions.create()` | `/chat/completions` | 支持流式、`function_call`、多模态 `image_url` |
| Responses（智能体） | `client.responses.create()` | `/responses` | 支持 `input: str`、`previous_response_id`、内置工具 |
| 文件上传 | `client.files.create()` | `/files` | `purpose` 决定用途（`file-extract`/`batch`/`fine-tune`） |
| 批量推理（文件） | `client.batches.create()` | `/batches` | 异步，JSONL 输入，费用为实时调用 50% |
| 批量推理（单请求） | `client.chat.completions.create()` | `/chat/completions`（`batch.dashscope.aliyuncs.com`） | 同步等待，最长 3600 秒超时 |
| 会话管理 | `client.conversations.*()` | `/conversations` | 创建/查询/更新/删除会话及消息项 |
| 向量嵌入 | `client.embeddings.create()` | `/embeddings` | 支持 `dimensions`、`encoding_format` |

### 3. LangChain 集成
- **OpenAI 方式**（部分模型）：使用 `langchain_openai.ChatOpenAI`，`base_url` 指向百炼兼容地址 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)；
- **DashScope 方式**（全模型）：使用 `langchain_community.chat_models.tongyi.ChatTongyi`，需安装 `dashscope` 包，支持部署模型。

## 限制和注意事项

- **地域强绑定**：API Key 与 `base_url` 地域必须一致，跨地域调用必鉴权失败（HTTP 401 + `invalid_api_key`），非密钥错误；
- **域名迁移强制要求**：旧域名 `dashscope.aliyuncs.com` / `dashscope-intl.aliyuncs.com` 已逐步淘汰，**必须迁移至业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），否则可能遭遇性能下降或服务中断；
- **文件配额**：文件存储上限为 **10,000 个文件** 或 **100 GB 总大小**，达任一上限后上传失败；
- **Batch 限制**：
  - `qwen3.8`/`qwen3.7`/`qwen3.6`/`qwen3.5` 系列默认开启思考模式，未显式设置 `enable_thinking=false` 将产生额外 `reasoning_tokens` 成本；
  - `qwen3.5-omni-plus`/`qwen3.5-omni-flash` 不支持语音输出；
- **Embedding 限制**：`output_type=sparse` 仅 DashScope 原生接口支持，[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)传入该参数将返回空 embedding（HTTP 200）；
- **Vision 模型限制**：`QVQ` 仅支持[流式输出](../concepts/streaming-output.md)，非流式调用将失败；
- **Responses API 路径废弃**：旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停用，必须使用 `/compatible-mode/v1/responses`。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)


