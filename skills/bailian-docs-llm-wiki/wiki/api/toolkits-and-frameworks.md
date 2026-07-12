# toolkits and [frameworks](frameworks.md)

阿里云百炼提供与 OpenAI 兼容的多套 API 接口和第三方框架集成方案，开发者只需修改 `base_url`、`api_key` 和 `model` 三个参数即可将现有 OpenAI 应用迁移至百炼平台。本页汇总了百炼支持的 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)类型、批量推理方案和 LangChain 等主流框架的集成方式。

## 兼容接口总览

百炼提供以下 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，覆盖从文本对话到文件管理的完整场景：

| 接口类型 | 说明 | 典型用途 |
|---------|------|---------|
| Chat Completions | 标准对话接口，支持流式/非流式、function call | 通用对话、工具调用 |
| Responses | Chat Completions 的演进版，内置联网搜索等工具 | 智能体场景、简化上下文管理 |
| Completions | 文本补全接口，支持 FIM（fill-in-middle） | 代码补全、内容续写 |
| Embedding | 文本向量化接口 | 文本检索、语义相似度 |
| Files | 文件上传/查询/删除 | 文档问答、Batch 输入、模型调优 |
| Conversations | 会话管理接口，配合 Responses API 使用 | 跨设备对话延续 |
| Batch（文件输入） | 通过文件异步批量处理，费用为实时调用的 50% | 数据标注、模型评测 |
| Batch Chat | 同步批量对话接口，费用为实时调用的 50% | 无需实时响应的批量对话 |

## 服务地址配置

所有 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)使用统一的 BASE_URL 模式。通过 SDK 调用时配置 `base_url`，通过 HTTP 调用时拼接完整 endpoint。

```
# SDK base_url（以北京地域为例）
https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1

# 各地域 base_url
北京：      https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1
新加坡：    https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
日本（东京）：https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1
德国（法兰克福）：https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1
美国（弗吉尼亚）：https://dashscope-us.aliyuncs.com/compatible-mode/v1
```

其中 `{WorkspaceId}` 为[业务空间](../concepts/workspace.md) ID，可在百炼控制台的[业务空间](../concepts/workspace.md)详情页面查看。

> **注意**：百炼为华北2（北京）、新加坡地域推出了[业务空间](../concepts/workspace.md)专属域名，建议从旧域名 `dashscope.aliyuncs.com` / `dashscope-intl.aliyuncs.com` 迁移至新域名以获得更好的性能和稳定性。详见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。

## 支持的模型

### Chat Completions 接口

支持 Qwen 大语言模型（商业版、开源版）、Qwen-VL、Qwen-Coder、Qwen-Omni、Qwen-Math，以及 DeepSeek、Kimi、GLM、MiniMax 等第三方直供模型。

> **注意**：三方直供模型仅在中国站的中国内地地域可用，需在百炼控制台开通对应服务后方可调用。Qwen-Audio 不支持 OpenAI 兼容协议，仅支持 DashScope 协议。

### Responses 接口

支持 qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.5-plus、qwen3.6-flash、qwen3.5-flash 等 Qwen3 系列模型，以及 qwen-plus、qwen-flash、qwen3-coder-plus 等。

### Completions 接口

当前仅支持 qwen-coder-turbo，且仅限华北2（北京）地域。详见 [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。

### Embedding 接口

支持 text-embedding-v1 至 v4 四个版本。其中 v4（属于 Qwen3-Embedding 系列）支持 2048/1536/1024/768/512/256/128/64 等多种向量维度，最大单行 8192 Token，支持 100+ 语种。详见 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。

> **注意**：[多模态](../concepts/multimodal.md) Embedding 模型（如 qwen3-vl-embedding）不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，需使用 DashScope 专用接口。

## 核心接口使用方式

### Chat Completions 基础调用

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你好"}
    ],
    stream=True,
    stream_options={"include_usage": True}
)
for chunk in completion:
    print(chunk.model_dump_json())
```

### Responses 接口调用

Responses API 是 Chat Completions 的演进版本，支持内置工具（联网搜索、代码解释器等）、字符串直接输入和通过 `previous_response_id` 简化多轮对话上下文管理。

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
response = client.responses.create(
    model="qwen3.7-plus",
    input="你能做些什么？"
)
print(response.output_text)
```

详见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。

> **注意**：Responses API 的旧版路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 即将停止维护，请迁移至新版路径 `/compatible-mode/v1/responses`。

### 文件接口

文件上传接口用于 Qwen-Long 文档问答、Qwen-Doc-Turbo 数据提取、Batch 任务输入和模型调优数据集上传。通过 `purpose` 参数区分用途：`file-extract`（文档分析）、`batch`（批量推理）、`fine-tune`（模型调优）。详见 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。

## 批量推理方案

百炼提供两种批量推理方案，费用均为实时调用的 50%：

### Batch（文件输入）

通过 JSONL 文件批量提交请求，系统异步处理后返回结果。适用于数据标注、模型评测等时效性要求不高的场景。支持文本生成模型、[多模态](../concepts/multimodal.md)模型和文本向量模型。详见 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。

### Batch Chat

保持与实时 API 一致的同步调用方式，只需将 `base_url` 修改为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1` 即可切换到批量推理。请求默认等待超时时间为 3600 秒。详见 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。

## LangChain 集成

百炼支持通过 OpenAI 兼容模式或 DashScope 原生模式集成到 LangChain 框架中。

### Python

- **OpenAI 兼容模式**：使用 `langchain_openai` 包的 `ChatOpenAI` 类，配置百炼的 `base_url` 和 `api_key`
- **DashScope 原生模式**：使用 `langchain_community` 包的 `ChatTongyi` 类，支持百炼所有文本生成模型

### JavaScript/Node.js

- **OpenAI 兼容模式**：使用 `@langchain/openai` 包的 `ChatOpenAI` 类
- **DashScope 原生模式**：使用 `@langchain/community` 包的 `ChatAlibabaTongyi` 类

### Java (LangChain4j)

支持 Plain Java 和 Spring Boot 两种方式，通过 `langchain4j-open-ai` 依赖使用 OpenAI 兼容模式，或通过 `langchain4j-community-dashscope` 使用 DashScope 原生模式。

> **注意**：LangChain4j 1.0.0-beta3 需要 Java 17 及以上版本。

详见 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

## Conversations 会话管理

Conversations API 配合 Responses API 使用，支持创建、查询、更新、删除会话以及管理会话消息项。通过 `previous_response_id` 自动注入历史上下文，无需手动维护消息列表，适合跨设备或长时间中断的对话场景。详见 [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。

## 关键参数说明

通用请求参数（适用于 Chat Completions / Completions）：

| 参数 | 说明 |
|------|------|
| `model` | 模型名称 |
| `temperature` | 采样温度，取值 [0, 2.0)，越高越多样 |
| `top_p` | 核采样阈值，取值 (0, 1.0]，与 temperature 二选一设置 |
| `max_tokens` | 最大返回 Token 数（不影响生成过程，仅截断输出） |
| `stream` | 是否[流式输出](../concepts/streaming.md) |
| `stream_options` | 流式时设 `{"include_usage": true}` 在末尾展示 Token 用量 |
| `stop` | 停止生成的字符串或 token_id |
| `seed` | 设置后使生成结果更具确定性 |

## 限制和注意事项

- 所有接口均需要有效的百炼 API Key，各地域的 API Key 不同
- Batch 场景下，qwen3.7/3.6/3.5 系列模型默认开启思考模式，建议显式设置 `enable_thinking` 参数
- Batch（文件输入）的输入文件需为 JSONL 格式，单个文件最大 500 MB
- 文件上传存储空间上限为 10000 个文件，总大小不超过 100 GB
- Responses API 的 `previous_response_id` 有效期为 7 天

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)




