# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 OpenAI 兼容的工具包与框架接口，覆盖文本生成、多模态理解、[向量嵌入](../concepts/embedding.md)、批量推理、会话管理等核心场景。开发者可通过统一 SDK（如 OpenAI Python/Node.js SDK）或 HTTP 直连方式快速迁移现有应用，无需重写业务逻辑。所有接口均支持标准 OpenAI 请求/响应格式，并在模型能力、上下文管理、文件处理等方面进行了增强。

## 支持的模型/功能

百炼兼容接口支持三大类模型能力：

- **文本生成**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash` 等全系列 Qwen 文本模型，以及 DeepSeek、GLM、Kimi、MiniMax 等三方直供模型（仅限华北2北京地域）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；
- **多模态理解**：`qwen3-vl-plus`、`QVQ`、`Qwen-OCR` 支持图像输入；`qwen3.8-omni-flash` 支持音视频输入 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)；
- **[向量嵌入](../concepts/embedding.md)**：`text-embedding-v4`、`qwen3.7-text-embedding` 等 6 款 Embedding 模型，支持最高 128K token 单行输入与多维度输出 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。

> **注意**：`Qwen-Audio` 不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；`qwen3.8-omni-flash` 在 Responses API 中支持音视频输入，但在 Chat Completions 兼容接口中暂不支持。

此外，还提供：
- **智能体原生能力**：Responses API 内置联网搜索、网页抓取、代码解释器等工具，无需手动定义 function call [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)；
- **长文档处理**：通过 `file-extract` 上传的文件 ID 可用于 `Qwen-Long` 和 `Qwen-Doc-Turbo` 的问答与数据提取；
- **跨设备会话延续**：Conversations API 自动维护上下文状态，支持 `previous_response_id` 关联与 `conversation_id` 生命周期管理。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `base_url` | 必填，服务端点，**必须使用业务空间专属域名**（非旧版 `dashscope.aliyuncs.com`） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `api_key` | 必填，按地域绑定，北京地域 Key 不能调用弗吉尼亚 endpoint | `sk-xxx`（需从对应地域控制台获取） |
| `model` | 必填，模型名称须严格匹配支持列表，大小写敏感 | `qwen3.8-max`, `text-embedding-v4`, `qwen3-vl-plus` |
| `enable_thinking` | 可选（Batch 场景），控制是否启用思考模式，默认 `true`；显式设为 `false` 可降低 token 成本 | `false` |
| `dimensions` | Embedding 接口专用，仅 `text-embedding-v3/v4` 支持，指定向量维度 | `1024` |
| `previous_response_id` | Responses API 专用，传入上一轮响应的顶层 `id`（UUID 格式），非 `output` 内 `msg_xxx` | `"0c842a11-c7d1-45da-b7ec-4e668c389xxx"` |

> **注意**：`enable_thinking` 必须作为 JSONL 请求体的顶层字段（与 `model` 同级），不可置于 `extra_body` 中，否则无效 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。

## 使用方式

### 1. SDK 调用（推荐）
统一使用 OpenAI 官方 SDK（v1.x），仅需配置 `base_url` 和 `api_key`：
```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
# Chat Completions
client.chat.completions.create(model="qwen-plus", messages=[...])
# Responses API（智能体）
client.responses.create(model="qwen3.8-max", input="...")
# Embeddings
client.embeddings.create(model="text-embedding-v4", input="...")
# Conversations
client.conversations.create(items=[...])
```

### 2. HTTP 调用
直接构造请求，`Authorization` 头携带 Bearer Token：
```bash
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen-plus","messages":[{"role":"user","content":"hi"}]}'
```

### 3. LangChain 集成
- **OpenAI 兼容层**（`langchain_openai`）：仅支持部分模型，适合快速验证；
- **DashScope 原生层**（`langchain_community.chat_models.tongyi`）：支持全部百炼模型，含部署模型与多模态能力 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

## 限制和注意事项

- **地域强绑定**：API Key 与 `base_url` 所属地域必须一致，跨地域调用返回 `invalid_api_key`（HTTP 401），而非权限错误；
- **域名迁移强制要求**：旧域名 `dashscope.aliyuncs.com` 已逐步淘汰，所有新项目必须使用 `{WorkspaceId}.<region>.maas.aliyuncs.com` 格式；
- **文件配额限制**：文件接口单个存储空间上限为 10,000 个文件 / 100 GB 总大小，超限后上传失败；
- **Batch 场景 Token 上限**：`qwen3.8`/`qwen3.7` 系列模型单次请求最大支持 256K context tokens，但 `qwen3.5-omni-plus` 不支持语音输出；
- **Embedding 稀疏向量限制**：[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)不支持 `output_type=sparse`，该参数将被忽略且返回空 embedding；
- **QVQ 模型流式强制**：`QVQ` 仅支持[流式输出](../concepts/streaming-output.md)，非流式调用将失败；
- **三方模型地域限制**：DeepSeek（硅基流动）、Kimi（月之暗面）等仅在中国站华北2（北京）可用，调用前需在控制台开通对应服务。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)


