# toolkits and [frameworks](frameworks.md)

阿里云百炼平台提供与 OpenAI 完全兼容的 API 接口体系，开发者只需修改 `base_url`、`api_key` 和 `model` 三个参数即可将现有 OpenAI 应用迁移至百炼。同时百炼深度集成 LangChain 等主流框架，覆盖文本生成、视觉理解、向量化、代码补全、批量推理等全场景。

## 兼容接口概览

百炼提供以下 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)：

| 接口类型 | 用途 | 关键特性 |
|---------|------|---------|
| Chat Completions | 文本对话 | 支持流式、function call、多轮对话 |
| Responses API | 智能体原生对话 | 内置工具、简化上下文管理、`previous_response_id` 自动关联 |
| Completions | 代码/文本补全 | FIM（Fill-in-Middle）模式 |
| Vision | 图像/视频理解 | 支持 URL 和 Base64 输入 |
| Embedding | 文本向量化 | 多维度可选（64~2048） |
| Files | 文件管理 | 用于长文档问答、批量推理、模型调优 |
| Batch (File) | 异步批量推理 | 费用为实时调用的 50% |
| Batch Chat | 同步批量推理 | 保持同步调用方式，费用 5 折 |
| Conversations | 会话管理 | 跨设备对话延续 |

## 服务地址配置

所有接口统一使用[业务空间](../concepts/workspace.md)专属域名，格式为：

```
https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1
```

支持的地域：

- **华北2（北京）**：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
- **新加坡**：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`
- **美国（弗吉尼亚）**：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`
- **日本（东京）**：`https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1`
- **德国（法兰克福）**：`https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1`

其中 `{WorkspaceId}` 为[业务空间](../concepts/workspace.md) ID，可在百炼控制台的[业务空间](../concepts/workspace.md)详情页面查看。

> **注意**：百炼推荐使用业务空间专属域名替代旧域名 `dashscope.aliyuncs.com`，专属域名能提供更高的性能和稳定性。同时 Responses API 的旧版路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 即将停止维护，请迁移至 `/compatible-mode/v1/responses`。

## Chat Completions 接口

这是最常用的对话接口，支持 Qwen 全系列、DeepSeek、Kimi、GLM、MiniMax 等模型。详细使用方法参见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。

基本调用示例（Python）：

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
    stream=True  # 可选流式输出
)
```

支持的高级特性：
- **[流式输出](../concepts/streaming.md)**：设置 `stream=True`，通过 `stream_options={"include_usage": True}` 获取 token 统计
- **Function Call**：定义 `tools` 列表，模型自动选择并调用工具
- **多轮对话**：手动维护 messages 数组

> **注意**：Qwen-Audio 不支持 OpenAI 兼容协议，仅支持 DashScope 协议。三方直供模型（如 SiliconFlow DeepSeek）仅在中国站中国内地地域可用，调用前需先在控制台开通服务。

## Responses API

作为 Chat Completions API 的演进版本，Responses API 提供更简洁的智能体原生功能。详情参见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。

相较 Chat Completions 的优势：
- **内置工具**：联网搜索、网页抓取、代码解释器、文搜图、图搜图
- **灵活输入**：支持直接传入字符串，也兼容 messages 数组
- **简化上下文**：通过 `previous_response_id` 自动关联上一轮对话，无需手动构建历史

```python
response = client.responses.create(
    model="qwen3.7-plus",
    input="你能做些什么？"
)
print(response.output_text)
```

支持的模型包括 qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.5-plus、qwen3.6-flash、qwen3.5-flash、qwen3-coder-plus 等。

## Completions 接口（代码补全）

专为代码补全场景设计，支持前缀补全和前后缀填充（FIM）模式。当前支持 `qwen-coder-turbo` 模型。

```python
completion = client.completions.create(
    model="qwen-coder-turbo",
    prompt="<|fim_prefix|>def quick_sort(arr):<|fim_suffix|>",
)
```

FIM 模板格式：
- 仅前缀：`<|fim_prefix|>{prefix}<|fim_suffix|>`
- 前缀+后缀：`<|fim_prefix|>{prefix}<|fim_suffix|>{suffix}<|fim_middle|>`

> **注意**：Completions 接口仅适用于中国内地（北京地域），需使用北京地域的 API Key。

## Vision 接口

视觉模型支持图像和视频理解，兼容 OpenAI Vision 接口规范。支持 Qwen-VL、QVQ、Qwen-OCR 系列模型。

```python
completion = client.chat.completions.create(
    model="qwen3-vl-plus",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "这是什么"},
            {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
        ]
    }],
    stream=True
)
```

## Embedding 接口

百炼提供 text-embedding-v1 至 v4 系列向量模型。最新的 text-embedding-v4（Qwen3-Embedding 系列）支持 100+ 语种，向量维度可选 64~2048。详见 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。

```python
completion = client.embeddings.create(
    model="text-embedding-v4",
    input="待向量化的文本",
    dimensions=1024  # 仅 v3/v4 支持指定维度
)
```

> **注意**：多模态 Embedding 模型（如 qwen3-vl-embedding、tongyi-embedding-vision 系列）不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，需使用专用的多模态向量接口。

## 批量推理

百炼提供两种批量推理方式，均享受 50% 费用折扣：

### Batch（文件输入）

通过上传 JSONL 文件异步批量处理请求，适合数据分析、模型评测等场景。详见 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。

### Batch Chat（同步方式）

保持与实时 API 一致的同步调用方式，只需将 `base_url` 修改为：

```
https://batch.dashscope.aliyuncs.com/compatible-mode/v1
```

请求进入队列排队后同步返回结果，默认超时 3600 秒。

## 文件接口

文件接口用于上传文件，支持三种用途：
- `file-extract`：用于 Qwen-Long / Qwen-Doc-Turbo 文档问答（单文件最大 150 MB）
- `batch`：用于批量推理输入（单文件最大 500 MB）
- `fine-tune`：用于模型调优数据集（单文件最大 300 MB）

百炼存储空间最大支持 10000 个文件，总大小不超过 100 GB。

## Conversations API

配合 Responses API 使用，提供跨设备、跨会话的对话延续能力。通过 `conversation_id` 自动注入历史上下文，无需手动同步消息。详见 [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。

## LangChain 集成

百炼支持通过 LangChain 框架调用模型，提供两种集成方式：

### OpenAI 兼容模式

通过 `langchain_openai` 包直接使用，适用于支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)的模型。详见 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-plus",
)
```

### DashScope 原生模式

通过 `langchain-community` 的 `ChatTongyi` 类使用，支持百炼所有文本生成模型（包括部署后的自定义模型）。

支持的语言和框架：
- **Python**：`langchain_openai`（OpenAI 模式）/ `langchain_community`（DashScope 模式）
- **JavaScript/TypeScript**：`@langchain/openai` / `@langchain/community`
- **Java**：LangChain4j（需 Java 17+），支持 Plain Java 和 Spring Boot

## 关键参数说明

| 参数 | 说明 | 备注 |
|------|------|------|
| `temperature` | 控制生成多样性，范围 [0, 2.0) | 与 top_p 二选一 |
| `top_p` | 核采样阈值，范围 (0, 1.0] | 与 temperature 二选一 |
| `max_tokens` | 最大返回 [Token](../concepts/token.md) 数 | 不影响生成过程，仅截断输出 |
| `stream` | 是否[流式输出](../concepts/streaming.md) | 默认 false |
| `stop` | 停止生成的触发词 | 支持字符串或数组 |
| `seed` | 确定性生成种子 | 范围 0 到 2^31-1 |
| `enable_thinking` | 启用思考模式 | qwen3.5/3.6/3.7 系列默认开启 |

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


