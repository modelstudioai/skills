# toolkits and [frameworks](frameworks.md)

阿里云百炼平台全面兼容 OpenAI 接口规范，开发者只需调整 `api_key`、`base_url` 和 `model` 三个参数，即可将现有 OpenAI 应用无缝迁移到百炼服务。此外，百炼还深度集成了 LangChain（Python/JavaScript/Java）等主流开发框架，为不同技术栈的开发者提供多种接入方式。

## 兼容接口总览

百炼提供以下 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，覆盖文本生成、视觉理解、向量化、文件管理、批量推理和会话管理等核心场景：

| 接口 | 端点路径 | 典型用途 |
|------|---------|---------|
| Chat Completions | `/compatible-mode/v1/chat/completions` | 文本对话、多轮会话 |
| Responses | `/compatible-mode/v1/responses` | 智能体原生功能，内置工具调用 |
| Completions | `/compatible-mode/v1/completions` | 代码补全、文本续写 |
| Vision | `/compatible-mode/v1/chat/completions` | 图像/视频理解 |
| Embeddings | `/compatible-mode/v1/embeddings` | 文本向量化 |
| Files | `/compatible-mode/v1/files` | 文件上传与管理 |
| Batch Chat | `batch.dashscope.aliyuncs.com/compatible-mode/v1/chat/completions` | 低成本同步批量推理 |
| Batch File | `/compatible-mode/v1/batches` | 异步文件批量推理 |
| Conversations | `/compatible-mode/v1/conversations` | 跨设备会话管理 |

## 服务地址与认证

所有接口统一使用百炼 API Key 进行认证，通过 `Authorization: Bearer <API_KEY>` 请求头或 SDK 的 `api_key` 参数传入。各地域的 BASE_URL 如下：

- **华北2（北京）**：`https://dashscope.aliyuncs.com/compatible-mode/v1`
- **美国（弗吉尼亚）**：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`
- **新加坡**：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`
- **德国（法兰克福）**：`https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1`（仅 Responses 接口支持）

> **注意**：新加坡地域旧版域名 `https://dashscope-intl.aliyuncs.com` 即将下线，请尽快迁移至 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`。不同地域的 API Key 不通用，需分别获取。

## Chat Completions 接口

这是最常用的对话接口，支持千问全系列文本模型，包括商业版（Max、Plus、Flash、Turbo、Coder、Long 等）和开源版模型。支持流式与非流式两种输出模式。详见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。

基础调用示例（Python）：

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

[流式输出](../concepts/streaming.md)只需添加 `stream=True` 参数，可通过 `stream_options={"include_usage": True}` 在最后一行获取 token 用量。

## Responses 接口

作为 Chat Completions 的演进版本，Responses 接口提供更简洁的智能体开发体验，具备以下优势：

- **内置工具**：联网搜索、网页抓取、代码解释器等，无需额外配置
- **灵活输入**：支持直接传入字符串，也兼容 Chat 格式消息数组
- **简化上下文**：通过 `previous_response_id` 自动关联多轮对话历史（有效期 7 天），无需手动维护消息列表

支持 qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.5-plus、qwen3.6-flash、qwen3.5-flash 等模型及部分开源模型。详见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。

> **注意**：Responses 接口的旧版 URL 路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 即将停止维护，请迁移至 `/compatible-mode/v1/responses`。

## Completions 接口（文本补全）

专为代码补全和文本续写场景设计，当前仅支持 `qwen-coder-turbo` 模型，且仅限中国内地（北京地域）使用。通过 `<|fim_prefix|>` 和 `<|fim_suffix|>` 标记实现前缀补全和中间填充两种模式。详见 [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。

关键参数包括 `temperature`（控制多样性，范围 [0, 2.0)）、`top_p`（核采样阈值，范围 (0, 1.0]）、`max_tokens`（最大返回 Token 数）、`stop`（停止序列）等。

## Vision 接口（视觉理解）

通义千问视觉模型兼容 OpenAI Vision 接口，支持图像和视频理解。支持的模型包括 qwen3-vl-plus、qwen3-vl-flash 系列、QVQ 系列（qvq-max、qvq-plus）以及 OCR 系列模型。详见 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。

图像输入支持 URL 和 Base64 两种方式，通过 `messages` 中的 `image_url` 类型传入。

> **注意**：QVQ 模型仅支持[流式输出](../concepts/streaming.md)。

## Embedding 接口（文本向量化）

支持 text-embedding-v1 到 v4 四个版本，其中 v4（属 Qwen3-Embedding 系列）支持 100+ 语种，向量维度可选 64 到 2048。v3 和 v4 支持通过 `dimensions` 参数指定输出维度。详见 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。

| 模型 | 默认维度 | 单行最大 Token | 单价（每千 Token） |
|------|---------|--------------|-----------------|
| text-embedding-v4 | 1,024 | 8,192 | 0.0005 元 |
| text-embedding-v3 | 1,024 | 8,192 | 0.0005 元 |
| text-embedding-v2 | 1,536 | 2,048 | 0.0007 元 |

> **注意**：多模态 Embedding 模型（如 qwen3-vl-embedding）不支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，需使用专用的多模态向量 API。

## 文件接口

文件上传接口用于文档分析（Qwen-Long/Qwen-Doc-Turbo）、批量推理任务和模型调优数据集。通过 `purpose` 参数区分用途：

- `file-extract`：文档分析，支持 TXT/DOCX/PDF/XLSX 等，单文件最大 150 MB
- `batch`：批量推理，仅限 JSONL 格式，单文件最大 500 MB
- `fine-tune`：模型调优，仅限 JSONL 格式，单文件最大 300 MB

存储空间限制为 10,000 个文件、总大小不超过 100 GB。详见 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。

## 批量推理

百炼提供两种批量推理方式，费用均为实时调用的 **50%**：

### Batch Chat（同步）

保持与实时 API 一致的同步调用方式，只需将 `base_url` 替换为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`。请求进入队列后，服务端在处理完成时通过保持的连接返回结果，默认超时 3600 秒。适合单条请求的低成本调用。详见 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。

### Batch File（异步文件输入）

通过上传 JSONL 文件批量提交请求，系统异步处理后返回结果。适合大批量数据处理场景。工作流程为：上传输入文件 → 创建 Batch 任务 → 轮询状态 → 下载结果。详见 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。

> **注意**：在 Batch 场景下，qwen3.7-max、qwen3.7-plus、qwen3.6-plus 等模型的单次请求上下文 Token 数最大支持 256K。qwen3.7、qwen3.6 和 qwen3.5 系列模型默认开启思考模式，建议显式设置 `enable_thinking` 参数。

## Conversations 接口

配合 Responses API 使用，提供跨设备、跨会话的对话管理能力。支持创建、查询、更新、删除会话以及向会话添加消息项。通过在 Responses API 调用时传入 `conversation_id`，可自动注入历史上下文。详见 [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。

## LangChain 集成

百炼支持通过 LangChain 框架接入，提供 OpenAI 兼容模式和 DashScope 原生两种方式：

### Python

- **OpenAI 兼容**：`pip install langchain_openai`，使用 `ChatOpenAI` 类，指定百炼的 `base_url` 和 `api_key`
- **DashScope 原生**：`pip install langchain-community dashscope`，使用 `ChatTongyi` 类，支持百炼所有文本生成模型（含部署后的模型）

### JavaScript/TypeScript

- **OpenAI 兼容**：`npm install @langchain/openai @langchain/core`，使用 `ChatOpenAI` 类
- **DashScope 原生**：`npm install @langchain/community @langchain/core`，使用 `ChatAlibabaTongyi` 类

### Java（LangChain4j）

通过 `langchain4j-open-ai` 依赖使用 OpenAI 兼容模式，支持 Plain Java 和 Spring Boot 两种方式。

> **注意**：LangChain4j 1.0.0-beta3 需要 Java 17 及以上版本。

详见 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

## 限制与注意事项

- 各地域 API Key 不通用，切换地域时需同步更换 API Key
- 建议将 API Key 配置到环境变量（`DASHSCOPE_API_KEY`），避免硬编码泄露风险
- [OpenAI 兼容接口](../concepts/openai-compatible-api.md)仅支持部分模型，完整模型列表需查阅各接口文档
- DashScope 原生 SDK 支持的模型范围更广，包括所有已部署模型
- 新加坡地域需在 URL 中替换 `{WorkspaceId}` 为实际的[业务空间](../concepts/workspace.md) ID

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


