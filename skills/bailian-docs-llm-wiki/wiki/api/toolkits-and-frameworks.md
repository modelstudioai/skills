# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 OpenAI 兼容的工具集与框架，覆盖文本生成、视觉理解、[向量嵌入](../concepts/embedding.md)、批量处理、会话管理及文件操作等核心场景。开发者可通过统一 SDK（如 OpenAI Python SDK）或 HTTP 接口快速迁移现有应用，无需重写业务逻辑。所有接口均支持标准 OpenAI 请求/响应格式，并针对百炼模型能力进行了增强扩展。

## 支持的模型/功能

百炼兼容接口支持三大类模型能力：  
- **文本生成**：包括 `qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash` 等全系列千问大模型，以及 `deepseek-v4-pro`、`glm-5.3`、`kimi-k3` 等第三方直供模型 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)；  
- **多模态理解**：`qwen3-vl-plus`、`qwen3-vl-flash`、`qwen-vl-ocr` 等视觉模型，支持图像+文本联合推理 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)；  
- **向量化与检索**：`text-embedding-v4`、`qwen3.7-text-embedding` 等 Embedding 模型，支持多语种与高维向量输出 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。  

> **注意**：`Qwen-Audio` 不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；`Qwen-Coder` 仅在 `completions` 接口下可用，不支持 `chat/completions` 调用 [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。

## 关键参数

| 参数 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `base_url` | string | 必填，服务端点。**强烈建议使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）性能与稳定性较低 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) | `https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `model` | string | 必填，模型名称。需严格匹配文档中列出的支持列表，三方模型需先在控制台开通 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) | `qwen3.8-max`, `qwen3-vl-plus`, `text-embedding-v4` |
| `enable_thinking` | boolean | 可选，控制是否启用思考模式（影响 token 计费）。`qwen3.5+` 系列默认开启，**必须作为 `body` 顶层参数传入，不可置于 `extra_body` 中** [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md) | `true`, `false` |
| `previous_response_id` | string | Responses API 专用，用于多轮对话上下文自动注入。**必须传入上一轮响应的顶层 `id`（UUID 格式），而非 `output` 数组内消息的 `id`** [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) | `"0c842a11-c7d1-45da-b7ec-4e668c389xxx"` |
| `purpose` | string | 文件接口专用，决定文件用途。取值为 `file-extract`（文档分析）、`batch`（批量任务输入）、`fine-tune`（调优数据集） [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md) | `"batch"` |

## 使用方式

### 1. 基础调用（Chat/Responses）
使用 OpenAI SDK，仅需替换 `api_key` 和 `base_url`：
```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
# Chat API
client.chat.completions.create(model="qwen3.8-max", messages=[...])
# Responses API（支持内置工具）
client.responses.create(model="qwen3.8-max", input="查天气")
```

### 2. 批量处理
- **单请求同步批处理**（低延迟）：使用 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`，超时最长 3600 秒 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)；  
- **文件异步批处理**（高吞吐）：上传 JSONL 文件后创建 Batch 任务，费用为实时调用的 50% [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。

### 3. 高级会话管理
- **Conversations API**：创建/更新/删除会话实体，自动维护跨设备上下文；  
- **Responses API + `previous_response_id`**：轻量级多轮对话，无需手动拼接历史 [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。

### 4. LangChain 集成
- `langchain_openai.ChatOpenAI`：仅支持 OpenAI 兼容模型子集；  
- `langchain_community.chat_models.tongyi.ChatTongyi`：支持百炼全部文本模型（含部署模型） [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

## 限制和注意事项

- **地域绑定**：API Key 与 `base_url` 地域必须严格一致。例如，北京地域 API Key 无法调用弗吉尼亚 endpoint，否则返回 `invalid_api_key` 错误 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；  
- **路径弃用**：`/api/v2/apps/protocols/compatible-mode/v1/responses` 和 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 已停止维护，**必须迁移至 `/compatible-mode/v1/responses` 和 `/compatible-mode/v1/conversations`**；  
- **模型能力差异**：非阿里云直供模型（如部分 DeepSeek、Kimi）仅在华北2（北京）地域可用，且需在控制台单独开通；  
- **文件配额**：百炼存储空间上限为 10000 个文件 / 100 GB 总大小，超限后上传失败，需手动清理 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)；  
- **Embedding 稀疏向量**：[OpenAI 兼容接口](../concepts/openai-compatible-api.md)不支持 `output_type=sparse`，该参数将被忽略，结果为空；如需稀疏向量，请调用原生 DashScope 接口 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。

## 来源文档

- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)


