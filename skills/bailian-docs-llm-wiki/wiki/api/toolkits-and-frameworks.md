# toolkits and [frameworks](frameworks.md)

阿里云百炼提供全面的 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)体系，开发者只需修改 `base_url`、`api_key` 和 `model` 三个参数，即可将现有 OpenAI 应用无缝迁移至百炼平台。同时，百炼还原生支持 LangChain 等主流开发框架的集成，降低大模型应用的开发门槛。

## 兼容接口总览

百炼兼容的 OpenAI 接口覆盖以下能力：

| 接口类型 | 端点路径 | 主要用途 |
|---------|---------|---------|
| [Chat Completions](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) | `/v1/chat/completions` | 对话生成（文本、多模态） |
| [Responses](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) | `/v1/responses` | Chat Completions 的演进版，内置工具与简化上下文管理 |
| [Completions](../../raw/model-api-reference/toolkits-and-frameworks/completions.md) | `/v1/completions` | 文本/代码补全（FIM） |
| [Vision](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md) | `/v1/chat/completions` | 图像与视频理解 |
| [Embeddings](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md) | `/v1/embeddings` | 文本向量化 |
| [Files](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md) | `/v1/files` | 文件上传（文档问答、Batch、调优） |
| [Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md) | Batch 端点 | 单请求批量推理（同步等待，5 折优惠） |
| [Batch File](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) | `/v1/batches` | 文件批量推理（异步，5 折优惠） |
| [Conversations](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md) | `/v1/conversations` | 会话管理（跨设备对话延续） |

## 服务地址（BASE_URL）

不同地域使用不同的 `base_url`：

| 地域 | SDK base_url |
|------|-------------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 日本（东京） | `https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

其中 `{WorkspaceId}` 为业务空间 ID，可在百炼控制台的业务空间详情页面查看。

> **注意**：新加坡地域的旧域名 `https://dashscope-intl.aliyuncs.com` 即将停止维护，建议迁移至业务空间专属域名。各地域的 API Key 不同，切换地域时需同步更换。

Batch Chat 接口使用独立的端点：`https://batch.dashscope.aliyuncs.com/compatible-mode/v1`。

## 支持的模型

### 文本对话（Chat / Responses）

支持 Qwen 大语言模型（商业版、开源版）、Qwen-Coder、Qwen-Omni、Qwen-Math，以及第三方模型（DeepSeek、Kimi、GLM、MiniMax 等）。Responses API 当前支持的模型范围较 Chat Completions 更窄，主要覆盖 `qwen3` 系列。

> **注意**：三方直供模型仅在中国站的中国内地地域可用，需先在百炼控制台开通对应服务。Qwen-Audio 不支持 OpenAI 兼容协议，仅支持 DashScope 协议。

### 代码补全（Completions）

当前仅支持 `qwen-coder-turbo`，且仅限中国内地（北京地域）使用。使用 FIM（Fill-in-Middle）提示词模板 `<|fim_prefix|>{前缀}<|fim_suffix|>{后缀}<|fim_middle|>` 进行代码补全。

### 视觉理解（Vision）

支持 Qwen-VL、QVQ、Qwen-OCR 系列。各地域支持的模型有差异，详见百炼控制台模型广场。

### 文本向量（Embeddings）

| 模型 | 向量维度 | 单行最大 Token | 语种 |
|------|---------|--------------|------|
| text-embedding-v4 | 64~2048（默认 1024） | 8,192 | 100+ 语种 |
| text-embedding-v3 | 64~1024（默认 1024） | 8,192 | 50+ 语种 |
| text-embedding-v2 | 1,536 | 2,048 | 10 语种 |
| text-embedding-v1 | 1,536 | 2,048 | 6 语种 |

> **注意**：多模态 Embedding 模型（如 qwen3-vl-embedding）不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，需使用 DashScope 原生协议。

## 核心接口能力

### Responses API 的独特功能

相比 Chat Completions，[Responses API](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) 提供以下增强能力：

- **内置工具**：联网搜索、网页抓取、代码解释器、文搜图、图搜图等
- **简化输入**：支持直接传入字符串，无需构造消息数组
- **自动上下文管理**：通过 `previous_response_id` 自动关联上一轮对话，响应 ID 有效期 7 天

### Conversations API

[Conversations API](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md) 配合 Responses API 使用，支持 Create / Retrieve / Update / Delete 会话及 Create Items 添加消息，适用于需要跨设备或长时间维护对话上下文的场景。

### 文件接口

通过 `purpose` 参数区分文件用途：

- `file-extract`：文档分析（Qwen-Long / Qwen-Doc-Turbo），支持 TXT、PDF、DOCX 等，单文件最大 150 MB
- `batch`：Batch 任务输入，JSONL 格式，单文件最大 500 MB
- `fine-tune`：模型调优数据，JSONL 格式，单文件最大 300 MB

存储空间上限：10,000 个文件，总大小不超过 100 GB。

### 批量推理

百炼提供两种批量推理方式，费用均为实时调用的 **50%**：

1. **[Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)**：同步调用方式，修改 `base_url` 即可使用，默认超时 3600 秒
2. **[Batch File](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)**：通过 JSONL 文件批量提交，异步处理后返回结果，适用于大批量场景

> **注意**：qwen3.7、qwen3.6、qwen3.5 系列模型默认开启思考模式，会产生额外的思考 tokens 成本。建议显式设置 `enable_thinking` 参数（`true`/`false`）。在 JSONL 请求体中，`enable_thinking` 须与 `model` 同级传入。

## 快速开始示例

使用 OpenAI SDK 调用百炼 Chat Completions 接口：

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
        {"role": "user", "content": "你是谁？"}
    ]
)
print(completion.choices[0].message.content)
```

[流式输出](../concepts/streaming.md)只需添加 `stream=True` 和 `stream_options={"include_usage": True}`。

## LangChain 集成

百炼支持通过 [LangChain](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md) 框架进行集成，提供两种方式：

### OpenAI 兼容模式

适用于 Python（`langchain_openai`）、JavaScript（`@langchain/openai`）和 Java（LangChain4j）。只需将 `base_url` 指向百炼端点：

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-plus",
)
```

### DashScope 原生模式

支持百炼全量模型（包括部署后的自定义模型），通过 `langchain-community` 的 `ChatTongyi`（Python）或 `ChatAlibabaTongyi`（JavaScript）调用。

> **注意**：LangChain4j 1.0.0-beta3 需要 Java 17 及以上版本。

## 关键参数说明

| 参数 | 说明 | 适用接口 |
|------|------|---------|
| `temperature` | 控制生成多样性，取值 [0, 2.0) | Chat / Responses / Completions |
| `top_p` | 核采样概率阈值，取值 (0, 1.0] | Chat / Responses / Completions |
| `max_tokens` | 返回的最大 Token 数（截断而非限制生成） | Chat / Completions |
| `stream` | 是否[流式输出](../concepts/streaming.md) | Chat / Responses / Completions |
| `seed` | 确定性生成种子，取值 0~2^31-1 | Chat / Completions |
| `previous_response_id` | 关联上一轮响应（7 天有效） | Responses |
| `enable_thinking` | 开启/关闭思考模式 | Chat / Batch |
| `dimensions` | 指定向量维度（v3/v4 支持） | Embeddings |

> **注意**：`temperature` 与 `top_p` 均可控制生成多样性，建议只设置其中一个。

## 限制与注意事项

- Responses API 的旧版路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 即将停止维护，请迁移至 `/compatible-mode/v1/responses`
- Completions 接口当前仅支持北京地域，且仅限 `qwen-coder-turbo` 模型
- Batch 场景下部分模型单次请求上下文最大支持 256K Token
- 文件 ID 上传后可重复使用，无需每次重新上传
- 错误码处理请参考百炼错误码文档

## 来源文档

- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)


