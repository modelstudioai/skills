# toolkits and [frameworks](frameworks.md)

阿里云百炼平台全面兼容 OpenAI 接口规范，开发者只需调整 API Key、BASE_URL 和模型名称，即可将现有 OpenAI 应用迁移至百炼服务。同时，百炼还支持通过 LangChain 等主流开发框架进行集成，覆盖文本对话、视觉理解、向量化、文件管理、批量推理等完整能力矩阵。

## 接口兼容概览

百炼提供以下 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，每个接口对应不同的使用场景：

| 接口类型 | 主要用途 | 代表模型 |
|---------|---------|---------|
| Chat Completions | 文本对话、function call | Qwen 系列、DeepSeek、Kimi、GLM、MiniMax |
| Responses API | 智能体原生功能（内置工具、简化上下文） | qwen3.7-max/plus、qwen3.6-plus/flash 等 |
| Completions | 代码补全、文本续写 | qwen-coder-turbo |
| Vision | 图像/视频理解 | Qwen-VL、QVQ、Qwen-OCR |
| Embedding | 文本向量化 | text-embedding-v1/v2/v3/v4 |
| Files | 文件上传与管理 | 配合 Qwen-Long、Batch、Fine-tune 使用 |
| Batch (Chat) | 低成本同步批量推理 | 大部分千问模型 |
| Batch (File) | 异步文件批量推理 | 千问 Max/Plus/Flash/Long 等 |
| Conversations | 跨设备会话管理 | 配合 Responses API 使用 |

详细的接口说明可参考 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) 和 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。

## 通用配置

所有 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)共享相同的基础配置，迁移时只需修改三个参数：

- **BASE_URL**：根据地域选择对应的服务端点
- **API Key**：替换为百炼平台的 API Key（不同地域 Key 不同）
- **模型名称**：替换为百炼支持的模型名称

### 服务端点（BASE_URL）

| 地域 | SDK base_url |
|------|-------------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

> **注意**：新加坡地域旧版域名 `https://dashscope-intl.aliyuncs.com` 即将下线，请迁移至新版域名。

### 基本调用示例

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你好"}
    ]
)
print(completion.choices[0].message.content)
```

## Responses API

Responses API 是 Chat Completions API 的演进版本，提供了更简洁的智能体原生功能，详见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。相比 Chat Completions 的核心优势：

- **内置工具**：联网搜索、网页抓取、代码解释器等，无需自行实现
- **更灵活的输入**：支持直接传入字符串，也兼容 Chat 格式的消息数组
- **简化上下文管理**：通过 `previous_response_id` 自动关联历史对话，无需手动构建消息列表

```python
response = client.responses.create(
    model="qwen3.7-plus",
    input="你能做些什么？"
)
print(response.output_text)
```

多轮对话时，通过 `previous_response_id` 参数传入上一轮响应的顶层 `id` 即可自动关联上下文，响应 ID 有效期为 7 天。

## Completions 接口（代码补全）

[completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md) 专为文本补全场景设计，当前支持 `qwen-coder-turbo` 模型，仅限中国内地（北京地域）。支持两种模式：

- **前缀补全**：给定前缀生成后续内容
- **中间填充**：给定前缀与后缀生成中间内容（FIM）

使用 `<|fim_prefix|>`、`<|fim_suffix|>`、`<|fim_middle|>` 标记控制补全位置。关键参数包括 `temperature`、`top_p`、`max_tokens`、`stop` 等。

## 视觉理解（Vision）

通义千问视觉模型（Qwen-VL、QVQ、Qwen-OCR）兼容 OpenAI Vision 接口。通过 `image_url` 字段传入图片 URL 即可进行图像理解，详见 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。

> **注意**：QVQ 模型仅支持[流式输出](../concepts/streaming.md)。Qwen-Audio 不支持 OpenAI 兼容协议，仅支持 DashScope 协议。

## 文本向量化（Embedding）

百炼提供 text-embedding-v1 至 v4 四代向量模型，其中 v4（Qwen3-Embedding）支持 100+ 语种，向量维度可在 64 至 2048 之间灵活配置。详见 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。

```python
completion = client.embeddings.create(
    model="text-embedding-v4",
    input="需要向量化的文本",
    dimensions=1024,
    encoding_format="float"
)
```

> **注意**：多模态 Embedding 模型（如 qwen3-vl-embedding）不支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，需使用 DashScope 专用接口。

## 文件管理（Files API）

[OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md) 支持上传、查询、删除文件，通过 `purpose` 参数区分用途：

| purpose | 用途 | 单文件上限 | 支持格式 |
|---------|------|-----------|---------|
| `file-extract` | 文档分析（Qwen-Long/Qwen-Doc-Turbo） | 150 MB | TXT、DOCX、PDF、XLSX、MD、CSV、JSON、图片等 |
| `batch` | 批量推理输入 | 500 MB | JSONL |
| `fine-tune` | 模型调优训练数据 | 300 MB | JSONL |

百炼存储空间支持最大 10000 个文件，总大小不超过 100 GB。

## 批量推理

百炼提供两种批量推理方式，费用均为实时调用的 **50%**：

### Batch Chat（同步批量）

发送单个请求，服务端排队处理后同步返回结果。将 `base_url` 改为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1` 即可，默认超时 3600 秒。适合不需要实时响应但希望保持同步调用方式的场景，详见 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。

### Batch File（异步批量）

通过 JSONL 文件批量提交多个请求，系统异步处理后返回结果文件。工作流程为：上传输入文件 → 创建 Batch 任务 → 轮询状态 → 下载结果。适合数据标注、模型评测等大批量场景，详见 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。

> **注意**：`qwen3.7`、`qwen3.6`、`qwen3.5` 系列模型默认开启思考模式，会产生额外思考 tokens。建议显式设置 `enable_thinking` 参数（`true` 开启/`false` 关闭）。在 JSONL 请求体中，`enable_thinking` 须与 `model` 同级传入。

## Conversations API

[OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md) 提供跨设备、跨场景的会话管理能力，配合 Responses API 使用。支持创建、查询、更新、删除会话，以及向会话中添加消息项。通过 Conversations API 创建会话后，在 Responses API 调用中传入 `conversation_id` 即可自动注入历史上下文。

## LangChain 集成

百炼支持通过 LangChain 框架进行集成，提供两种方式，详见[在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)：

### OpenAI 兼容模式

通过 `langchain_openai`（Python）或 `@langchain/openai`（JavaScript）调用，支持部分百炼模型：

```python
from langchain_openai import ChatOpenAI

chatLLM = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-plus",
)
```

Java 端可通过 LangChain4j 的 `OpenAiChatModel` 集成，支持 Plain Java 和 Spring Boot 两种方式。

### DashScope 原生模式

通过 `langchain-community`（Python）或 `@langchain/community`（JavaScript）调用，支持百炼所有文本生成模型，包括部署后的自定义模型：

```python
from langchain_community.chat_models.tongyi import ChatTongyi

chatLLM = ChatTongyi(
    model="qwen-plus",
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY"),
)
```

## 限制与注意事项

- 三方直供模型（SiliconFlow DeepSeek、月之暗面 Kimi 等）仅在中国站的中国内地地域可用，需先在百炼控制台开通对应服务
- 各地域支持的模型存在差异，请以百炼控制台模型广场为准
- Completions 接口仅限北京地域使用
- Batch 场景下部分模型单次请求上下文最大支持 256K tokens
- Responses API 的 `previous_response_id` 有效期为 7 天

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)






