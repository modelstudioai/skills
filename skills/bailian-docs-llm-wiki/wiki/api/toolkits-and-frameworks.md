# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 OpenAI 兼容的工具包与框架接口，覆盖文本生成、视觉理解、[向量嵌入](../concepts/embedding.md)、批量推理、文件管理、会话状态管理等核心场景。开发者可复用现有 OpenAI 生态代码（如 SDK、LangChain 集成），仅需调整 `base_url`、`api_key` 和模型名即可快速迁移。所有兼容接口均支持[流式输出](../concepts/streaming-output.md)、[Token](../concepts/token.md) 统计、错误码标准化等生产级特性。

## 支持的模型/功能

百炼 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)支持以下模型类别与能力：

- **文本生成**：`qwen3.8-max`、`qwen3.7-plus`、`qwen-coder-turbo` 等全系列 Qwen 文本模型，以及 DeepSeek、GLM、Kimi、MiniMax 等三方直供模型（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）；
- **视觉理解**：`qwen3-vl-plus`、`QVQ`、`Qwen-OCR`，支持图像 URL 与 Base64 输入（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)）；
- **[向量嵌入](../concepts/embedding.md)**：`text-embedding-v4`、`qwen3.7-text-embedding` 等，支持多维度、多语种文本向量化（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)）；
- **长文档与结构化数据**：`Qwen-Long`（[长上下文](../concepts/long-context.md)问答）、`Qwen-Doc-Turbo`（文档信息抽取），通过文件 ID 关联（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)）；
- **智能体增强**：`Responses API` 内置联网搜索、网页抓取、代码解释器等工具，支持 `previous_response_id` 自动上下文注入（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)）；
- **会话持久化**：`Conversations API` 提供跨设备会话创建、消息追加与元数据管理（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)）。

> **注意**：`Qwen-Audio` 不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；`completions` 接口当前仅支持 `qwen-coder-turbo` 模型（见 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)），与其他接口的通用模型列表存在明显范围差异。

## 关键参数

| 参数 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `base_url` | string | 必填。服务端点，**必须匹配 API Key 所在地域**。业务空间专属域名性能更优，推荐使用（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `model` | string | 必填。模型名称，需严格匹配支持列表，大小写敏感 | `"qwen3.8-max"`, `"qwen3-vl-plus"`, `"text-embedding-v4"` |
| `stream` | boolean | 可选。启用[流式输出](../concepts/streaming-output.md)（`true`）或等待完整响应（`false`，默认） | `true` |
| `stream_options` | object | 可选。流式时设 `{"include_usage": true}` 在末 chunk 返回 token 统计 | `{"include_usage": true}` |
| `enable_thinking` | boolean | 可选（Batch 场景）。控制是否启用思考模式（影响 token 成本），须与 `model` 同级传入（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)） | `false` |
| `dimensions` | integer | 可选（Embedding）。指定向量维度（仅 `text-embedding-v3/v4` 支持） | `1024` |

## 使用方式

### 1. SDK 调用（推荐）
安装对应 SDK 并配置环境变量：
```bash
pip install -U openai langchain_openai  # Python
npm install @langchain/openai @langchain/community  # JavaScript
```

初始化客户端时指定 `base_url` 和 `api_key`：
```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
```

调用示例：
- Chat：`client.chat.completions.create(model="qwen3.8-max", messages=[...])`
- Embedding：`client.embeddings.create(model="text-embedding-v4", input="...")`
- Vision：`client.chat.completions.create(model="qwen3-vl-plus", messages=[{"content": [{"type":"image_url","image_url":{"url":"..."}}]}])`
- Responses：`client.responses.create(model="qwen3.8-max", input="...")`
- Conversations：`client.conversations.create(items=[...])`

### 2. LangChain 集成
- **OpenAI 兼容层**（`langchain_openai.ChatOpenAI`）：仅支持部分模型（如 `qwen-plus`），适合快速验证（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)）；
- **DashScope 原生层**（`langchain_community.chat_models.tongyi.ChatTongyi`）：支持全部百炼模型，包括部署模型与多模态能力。

### 3. HTTP 直连
直接构造 `POST` 请求，`Authorization: Bearer <API_KEY>`，`Content-Type: application/json`，body 包含 `model` 和输入字段（如 `messages`、`input`、`prompt`）。

## 限制和注意事项

- **地域强绑定**：API Key 与 `base_url` 地域必须一致。例如，北京地域 Key 不能调用弗吉尼亚 `base_url`，否则返回 `invalid_api_key`（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）；
- **文件接口配额**：文件存储上限为 10,000 个文件或 100 GB 总大小，超限后上传失败（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)）；
- **Batch 超时**：`Batch Chat` 默认等待 3600 秒，超时断连；`Batch File` 任务最长处理窗口为 `24h`（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)）；
- **模型能力差异**：`Responses API` 的 Agent 工具能力仅对列表中阿里云直供模型（如 `qwen3.8-max`）完整支持，三方模型（如 `deepseek-v4-pro`）仅基础兼容（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)）；
- **Embedding 稀疏向量**：[OpenAI 兼容接口](../concepts/openai-compatible-api.md)不支持 `output_type=sparse`，传入该参数将返回空 embedding（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)）；
- **旧路径弃用**：`/api/v2/apps/protocols/compatible-mode/v1/responses` 和 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 已停止维护，必须迁移至 `/compatible-mode/v1/{responses,conversations}`（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)）。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)


