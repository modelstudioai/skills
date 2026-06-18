# toolkits and [frameworks](frameworks.md)

阿里云百炼平台提供与 OpenAI 全面兼容的 API 接口体系，开发者只需修改 `base_url`、`api_key` 和 `model` 三个参数，即可将已有的 OpenAI 生态应用无缝迁移至百炼。同时，百炼还深度集成了 LangChain 等主流开发框架，支持 Python、Node.js、Java、Go、C# 等多种语言的 SDK 调用。

## 兼容接口总览

百炼提供以下 [OpenAI 兼容接口](../concepts/openai-compatible.md)，覆盖从文本生成到向量化的完整模型调用链路：

| 接口 | 用途 | 典型场景 |
|------|------|----------|
| [Chat Completions](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) | 对话式文本生成 | 聊天、问答、function call |
| [Responses](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) | Chat Completions 的演进版本 | 内置工具调用、简化上下文管理 |
| [Completions](../../raw/model-api-reference/toolkits-and-frameworks/completions.md) | 文本/代码补全 | 代码补全（FIM）、内容续写 |
| [Vision](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md) | 视觉理解 | 图像描述、视频分析、OCR |
| [Embedding](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md) | 文本向量化 | RAG、语义检索、文本分类 |
| [Files](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md) | 文件管理 | 文档问答、Batch 输入、模型调优数据集 |
| [Batch (文件输入)](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) | 异步批量推理 | 数据标注、模型评测（费用为实时调用的 50%） |
| [Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md) | 同步批量推理 | 同 Batch 但保持同步调用方式（限时 5 折） |
| [Conversations](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md) | 会话管理 | 跨设备/跨场景对话延续 |

## 服务地址与认证

### BASE_URL 配置

各地域的 SDK `base_url` 如下：

| 地域 | base_url |
|------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 日本（东京） | `https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

其中 `{WorkspaceId}` 为[业务空间](../concepts/workspace.md) ID，可在百炼控制台的[业务空间](../concepts/workspace.md)详情页面查看。

> **注意**：新加坡地域已推出[业务空间](../concepts/workspace.md)专属域名，建议从旧域名 `https://dashscope-intl.aliyuncs.com` 迁移至新域名以获得更好的性能和稳定性。

Batch Chat 接口使用独立的端点：`https://batch.dashscope.aliyuncs.com/compatible-mode/v1`。

### API Key

各地域的 API Key 不同，需分别在对应地域的百炼控制台获取。推荐将 API Key 配置到环境变量 `DASHSCOPE_API_KEY` 中，避免硬编码泄露风险。

## 支持的模型

### 文本生成（Chat / Responses）

支持千问全系列模型：Qwen Max / Plus / Flash / Long / Coder，以及第三方模型 DeepSeek、Kimi、GLM、MiniMax 等。Responses API 当前支持 `qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.5-plus`、`qwen3.6-flash`、`qwen3.5-flash`、`qwen-plus`、`qwen-flash`、`qwen3-coder-plus`、`qwen3-coder-flash` 等型号。

> **注意**：三方直供模型仅在中国站的中国内地地域可用，需先在百炼控制台开通对应服务。Qwen-Audio 不支持 OpenAI 兼容协议，仅支持 DashScope 协议。

### 代码补全（Completions）

当前仅支持 `qwen-coder-turbo`，且仅限中国内地（北京地域）。

### 视觉理解（Vision）

支持 Qwen-VL、QVQ、Qwen-OCR 系列。QVQ 模型仅支持[流式输出](../concepts/streaming.md)。

### 文本向量（Embedding）

| 模型 | 向量维度 | 单行最大 Token | 支持语种 |
|------|----------|---------------|----------|
| text-embedding-v4 | 64~2048 可选（默认 1024） | 8,192 | 100+ 语种 |
| text-embedding-v3 | 64~1024 可选（默认 1024） | 8,192 | 50+ 语种 |
| text-embedding-v2 | 1,536 | 2,048 | 10 语种 |
| text-embedding-v1 | 1,536 | 2,048 | 6 语种 |

> **注意**：多模态 Embedding 模型（如 qwen3-vl-embedding）不支持 [OpenAI 兼容接口](../concepts/openai-compatible.md)，需使用 DashScope 专用接口。

## 快速开始

以 OpenAI Python SDK 为例，典型调用流程如下：

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 非流式调用
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你是谁？"}
    ]
)
print(completion.choices[0].message.content)
```

流式调用只需添加 `stream=True`，并可通过 `stream_options={"include_usage": True}` 在最后一条 chunk 中获取 token 用量。

### Function Call

百炼 Chat Completions 接口完整支持 OpenAI 的 function call 协议，可定义 `tools` 列表并由模型自动选择调用，支持多轮工具调用。详见[原始文档](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。

### Responses API

作为 Chat Completions 的演进版本，[Responses API](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) 提供更简洁的接口设计：

- 支持直接传入字符串作为输入（无需构造 messages 数组）
- 通过 `previous_response_id` 自动关联上下文，无需手动维护消息历史（响应 ID 有效期 7 天）
- 内置联网搜索、网页抓取、代码解释器等工具

> **注意**：Responses API 的旧版路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 即将停止维护，请迁移至 `/compatible-mode/v1/responses`。

### Conversations API

配合 Responses API 使用，[Conversations API](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md) 提供服务端会话管理能力，支持创建、查询、更新、删除会话以及向会话添加消息项，实现跨设备的对话延续。

## 批量推理

百炼提供两种批量推理方式，均享受 50% 的费用优惠：

- **Batch (文件输入)**：通过上传 JSONL 文件批量提交请求，异步处理后下载结果。适合大批量、对时效性要求不高的场景。支持 `batch-test-model` 进行免费链路测试。
- **Batch Chat**：保持与实时 API 一致的同步调用方式，仅需将 `base_url` 改为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`。请求默认等待超时 3600 秒。

> **注意**：`qwen3.7`、`qwen3.6` 和 `qwen3.5` 系列模型默认开启思考模式，会产生额外的思考 token 成本。在 Batch 场景下建议显式设置 `enable_thinking` 参数。

## 代码补全（Completions）

[Completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)专为代码补全设计，使用 FIM（Fill-in-the-Middle）模板：

```
<|fim_prefix|>{前缀内容}<|fim_suffix|>{后缀内容}<|fim_middle|>
```

支持仅给前缀生成后续内容，也支持同时给定前缀和后缀生成中间内容。

## 文件管理

[文件接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)支持三种用途：

| purpose | 用途 | 单文件大小限制 |
|---------|------|----------------|
| `file-extract` | Qwen-Long / Qwen-Doc-Turbo 文档问答 | 150 MB |
| `batch` | Batch 任务输入文件 | 500 MB |
| `fine-tune` | 模型调优训练数据 | 300 MB |

存储空间上限为 10,000 个文件、总大小 100 GB。

## LangChain 集成

百炼提供两种 LangChain 集成方式，详见[集成指南](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)：

### 通过 OpenAI 兼容模式

使用 `langchain_openai` 包的 `ChatOpenAI`，配置百炼的 `base_url` 和 `api_key`。支持 Python、JavaScript、Java（LangChain4j）。

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-plus",
)
```

### 通过 DashScope 原生集成

使用 `langchain-community` 包的 `ChatTongyi`（Python）或 `ChatAlibabaTongyi`（JavaScript），支持百炼所有文本生成模型以及自定义部署模型。

## 关键参数说明

Chat Completions 接口的常用参数：

| 参数 | 说明 |
|------|------|
| `temperature` | 采样温度，控制多样性，取值 [0, 2.0) |
| `top_p` | 核采样概率阈值，取值 (0, 1.0]。与 temperature 二选一设置 |
| `max_tokens` | 返回的最大 Token 数（截断而非限制生成） |
| `stream` | 是否[流式输出](../concepts/streaming.md) |
| `stop` | 停止生成的字符串或 token_id |
| `seed` | 固定随机种子以获得确定性输出 |
| `presence_penalty` | 控制内容重复度，取值 [-2.0, 2.0] |

## 限制与注意事项

- 各地域支持的模型有所差异，具体以百炼控制台模型市场为准
- Batch 场景下部分模型单次请求最大支持 256K 上下文 Token
- Completions 接口的 `max_tokens` 不影响生成过程，仅截断返回内容
- QVQ 模型仅支持[流式输出](../concepts/streaming.md)
- LangChain4j 1.0.0-beta3 需要 Java 17 及以上版本

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


