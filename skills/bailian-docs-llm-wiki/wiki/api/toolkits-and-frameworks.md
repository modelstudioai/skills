# toolkits and [frameworks](frameworks.md)

阿里云百炼平台全面兼容 OpenAI 接口规范，开发者只需调整 API Key、BASE_URL 和模型名称三个参数，即可将现有 OpenAI 应用快速迁移至百炼服务。同时，百炼还提供与主流开发框架（如 LangChain、LangChain4j）的深度集成方案，覆盖文本生成、视觉理解、文本向量化、文件管理、批量推理等全场景。

## 兼容接口总览

百炼提供以下 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，每类接口对应不同的使用场景：

| 接口类型 | 适用场景 | 关键特性 |
|---------|---------|---------|
| [Chat Completions](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) | 多轮对话、Function Call | 支持流式/非[流式输出](../concepts/streaming-output.md) |
| [Responses API](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) | 智能体原生功能、内置工具调用 | Chat API 演进版，支持 `previous_response_id` 简化上下文管理 |
| [Completions](../../raw/model-api-reference/toolkits-and-frameworks/completions.md) | 代码补全、文本续写 | 支持 FIM（Fill-in-Middle）模式 |
| [Vision](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md) | 图片理解、视觉问答 | 支持 URL 和 Base64 图片输入 |
| [Embedding](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md) | 文本向量化 | 支持多维度输出（64~2048维） |
| [Files](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md) | 文件上传与管理 | 用于文档分析、Batch 任务、模型调优 |
| [Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md) | 同步批量推理 | 费用为实时调用的 50% |
| [Batch File](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) | 异步大批量处理 | 通过文件提交，费用为实时调用的 50% |
| [Conversations](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md) | 跨设备会话管理 | 配合 Responses API 自动注入历史上下文 |

## 接入配置

### BASE_URL

百炼支持多个地域的服务端点：

| 地域 | SDK base_url |
|-----|-------------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

> **注意**：新加坡地域已推出[业务空间](../concepts/workspace.md)专属域名，建议从 `https://dashscope-intl.aliyuncs.com` 迁移至 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`，其中 `{WorkspaceId}` 可在百炼控制台的[业务空间](../concepts/workspace.md)详情页面查看。

### API Key

通过百炼控制台获取 API Key，不同地域的 API Key 不通用。推荐通过环境变量 `DASHSCOPE_API_KEY` 配置以降低泄露风险。

## 支持的模型

**Chat Completions 接口**支持范围最广：Qwen 大语言模型（商业版、开源版）、Qwen-VL、Qwen-Coder、Qwen-Omni、Qwen-Math、DeepSeek、Kimi、GLM、MiniMax 等。

**Responses API** 支持 qwen3 系列最新模型（如 `qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash` 等）及 `qwen3-coder` 系列。

**Completions 接口**仅支持 `qwen-coder-turbo`，且仅限北京地域。

**Vision 接口**支持 Qwen-VL、QVQ、Qwen-OCR 系列模型。

**Embedding 接口**支持 `text-embedding-v1` 至 `text-embedding-v4`，其中 v4（属于 Qwen3-Embedding）支持 100+ 语种，向量维度可选 64~2048。

> **注意**：三方直供模型（如 SiliconFlow DeepSeek）仅在中国站中国内地地域可用，需先在百炼控制台开通对应服务。Qwen-Audio 不支持 OpenAI 兼容协议，仅支持 DashScope 协议。

## Responses API 与 Chat Completions 的区别

[Responses API](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) 是 Chat Completions API 的演进版本，主要优势包括：

- **内置工具**：联网搜索、网页抓取、代码解释器、图搜图等，无需自行实现
- **更灵活的输入**：支持直接传入字符串，也兼容 Chat 格式消息数组
- **简化上下文管理**：通过 `previous_response_id` 自动关联上下文，无需手动构建消息历史（响应 id 有效期 7 天）

## 批量推理

百炼提供两种批量推理方案，费用均为实时调用的 50%：

**Batch Chat（同步）**：通过修改 `base_url` 为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`，保持与实时 API 一致的调用方式，系统排队处理后同步返回结果。默认超时 3600 秒，适合单条请求的低成本调用。详见 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。

**Batch File（异步）**：通过 JSONL 文件批量提交请求，系统异步处理全部请求后返回结果文件。适合数据标注、模型评测等大批量场景。完整流程为：上传输入文件 → 创建 Batch 任务 → 轮询状态 → 下载结果。详见 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。

> **注意**：qwen3.7、qwen3.6 和 qwen3.5 系列模型默认开启思考模式，会产生额外 tokens 消耗。建议使用混合思考模型时显式设置 `enable_thinking` 参数。在 JSONL 请求体中，`enable_thinking` 必须与 `model` 同级传入。

## 文件管理

[文件接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)支持三种用途：

| purpose 参数 | 用途 | 单文件大小上限 | 支持格式 |
|-------------|------|--------------|---------|
| `file-extract` | 文档分析（Qwen-Long / Qwen-Doc-Turbo） | 150 MB | TXT、DOCX、PDF、XLSX、EPUB、MD、CSV、JSON、图片 |
| `batch` | Batch 任务输入 | 500 MB | JSONL |
| `fine-tune` | 模型调优训练集 | 300 MB | JSONL |

百炼存储空间最大支持 10000 个文件，总大小不超过 100 GB。

## LangChain 集成

百炼可通过两种方式集成到 [LangChain](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)：

**OpenAI 兼容模式**（推荐）：使用 `langchain_openai` 的 `ChatOpenAI` 类，配置百炼的 `base_url` 和 `api_key`，支持百炼兼容的部分模型。Python 和 JavaScript/Node.js 均可用。

```python
from langchain_openai import ChatOpenAI
chatLLM = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-plus",
)
```

**DashScope 原生模式**：使用 `langchain_community` 的 `ChatTongyi` 类，支持百炼全部文本生成模型（包括部署后的模型），同时支持多模态调用。

Java 开发者可使用 LangChain4j 集成，支持 Plain Java 和 Spring Boot 两种方式，需要 Java 17 及以上版本。

## Conversations API

[Conversations API](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md) 提供会话管理能力，配合 Responses API 实现跨设备、跨场景的对话延续。支持的操作包括：

- **创建会话**：可同时添加最多 20 条初始消息
- **查询/更新/删除会话**：通过 `conversation_id` 管理会话生命周期
- **添加消息**：向已有会话追加消息项

会话元数据支持最多 16 对键值对（key 最大 64 字符，value 最大 512 字符）。

## 注意事项与限制

- Completions 接口仅支持中国内地（北京地域），需使用北京地域 API Key
- 多模态 Embedding 模型（如 `qwen3-vl-embedding`）不支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，需使用 DashScope 协议
- QVQ 模型仅支持[流式输出](../concepts/streaming-output.md)
- Batch 场景下 qwen3.7/3.6/3.5 系列单次请求上下文最大支持 256K Token
- `previous_response_id` 有效期为 7 天
- Responses API 旧版路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 即将停止维护，请迁移至 `/compatible-mode/v1/responses`

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


