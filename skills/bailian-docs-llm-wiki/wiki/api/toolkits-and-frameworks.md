# toolkits and [frameworks](frameworks.md)

阿里云百炼提供了一整套 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（Chat、Responses、Vision、Embedding、Completions、Files、Batch、Conversations），开发者只需替换 `base_url`、`api_key` 和 `model` 三个参数，即可将原有 OpenAI 代码或 LangChain 等框架应用迁移到百炼服务。本文汇总各兼容接口的支持范围、接入方式与关键限制。

## 服务地址与鉴权

所有 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)统一使用 `https://<host>/compatible-mode/v1` 作为 base_url，按地域区分：

| 地域 | SDK base_url |
| --- | --- |
| 华北2（北京） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 日本（东京） | `https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福，仅 Responses API） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

其中 `{WorkspaceId}` 为[业务空间](../concepts/workspace.md) ID，可在百炼控制台「[业务空间](../concepts/workspace.md)详情」页查看。各地域的 [API Key](../concepts/api-key.md) 不通用，切换地域需同步更换 Key。详见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。

> **注意**：北京和新加坡地域已推出[业务空间](../concepts/workspace.md)专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com` / `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`），旧域名 `dashscope.aliyuncs.com` / `dashscope-intl.aliyuncs.com` 仍可用但建议迁移。此外 Responses API 旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 与 Conversations 旧路径即将停止维护，应迁移到 `/compatible-mode/v1/...` 新路径，参见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。

## 各接口能力概览

### Chat Completions（对话）

- **支持模型**：Qwen 商业版/开源版、Qwen-VL、Qwen-Coder、Qwen-Omni、Qwen-Math，以及 DeepSeek、Kimi、GLM、MiniMax 等第三方直供模型（三方直供仅限中国站中国内地，需先在控制台开通）。
- **不支持**：Qwen-Audio 仅支持 DashScope 协议，不走 OpenAI 兼容。
- 支持非流式/流式（`stream=True` + `stream_options={"include_usage": True}` 可在末尾返回 token 用量）、function call（`tools` 参数，支持多轮工具调用）。

### Responses API（Chat 的演进版本）

- 支持 `qwen3-max`、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.5-plus`、`qwen3.7-flash`、`qwen3.6-flash`、`qwen3.5-flash`、`qwen3-coder-plus/flash/next`、`qwen-plus`、`qwen-flash` 等模型。
- 输入更灵活：可直接传字符串，也兼容 Chat 消息数组；通过 `previous_response_id` 自动关联上下文（响应 id 有效期 7 天），无需手动维护消息历史。
- 内置联网搜索、网页抓取、代码解释器、文搜图、图搜图等工具。

### Vision（视觉理解）

- 支持 Qwen-VL、QVQ、Qwen-OCR 系列，各地域可用模型有差异，以控制台模型广场为准。
- 通过 `messages[].content` 中的 `image_url` 类型传入图片 URL 或 Base64；QVQ 仅支持[流式输出](../concepts/streaming.md)。示例见 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。

### Embedding（文本向量）

- 支持 `text-embedding-v1` ~ `text-embedding-v4`。v4/v3 支持 `dimensions` 参数指定向量维度（v4 可选 64~2048，默认 1024；v2 固定 1536 维）。
- v4 单行最大 8,192 [Token](../concepts/token.md)、最多 10 行；v2/v1 单行最大 2,048 [Token](../concepts/token.md)、最多 25 行。
- [多模态](../concepts/multimodal.md) Embedding 模型（如 qwen3-vl-embedding）**不支持** [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，需走 DashScope。详见 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。

### Completions（文本补全）

- 仅支持 `qwen-coder-turbo`，且仅适用于华北2（北京）地域。
- 使用 FIM 模板：前缀补全 `<|fim_prefix|>{prefix}<|fim_suffix|>`；前后缀补中间 `<|fim_prefix|>{prefix}<|fim_suffix|>{suffix}<|fim_middle|>`。不支持仅给后缀生成前缀。参数说明见 [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。

### Files（文件管理）

通过 `client.files.create(file=..., purpose=...)` 上传，按 `purpose` 区分用途：

| purpose | 用途 | 单文件上限 |
| --- | --- | --- |
| `file-extract` | Qwen-Long / Qwen-Doc-Turbo 文档问答与数据提取（支持 TXT/DOCX/PDF/XLSX/EPUB/MD/CSV/JSON 及图片） | 150 MB |
| `batch` | 批量推理输入（JSONL） | 500 MB |
| `fine-tune` | 模型调优数据集（JSONL） | 300 MB |

存储空间上限：10,000 个文件、总计 100 GB，无有效期限制；达到上限需删除旧文件后才能继续上传。文件 ID 可复用，无需重复上传。

### Batch（批量推理，费用为实时调用的 50%）

两种形态：

1. **Batch File API（文件输入）**：上传 JSONL → 创建任务 → 轮询状态 → 下载结果/错误文件。JSONL 每行格式为 `{"custom_id", "method": "POST", "url": "/v1/chat/completions", "body": {...}}`。北京地域支持千问 Max/Plus/Flash/Long、DeepSeek、[多模态](../concepts/multimodal.md)（qwen3-vl 等）、OCR、qwen3.5-omni-plus 及 text-embedding-v1~v4；新加坡仅支持 qwen-max/plus/turbo。可先用 `batch-test-model` 做全链路测试（不产生推理费用）。详见 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。
2. **Batch Chat（同步调用）**：保持与实时 API 一致的同步调用方式，仅需将 base_url 改为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`。默认等待超时 3600 秒，可自定义 60~3600 秒；超时则断开连接返回错误。目前仅华北2（北京）地域。参见 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。

> **注意**：Batch 场景下 qwen3.7/3.6/3.5 系列单次请求上下文最大 256K，且这些模型默认开启思考模式（会产生额外 reasoning tokens），建议显式设置 `enable_thinking`；在 JSONL 中该参数须与 `model` 同级放在 `body` 顶层，不能放入 `extra_body`。

### Conversations（会话管理）

配合 Responses API 实现服务端上下文托管，适用于跨设备/长时间中断的对话延续。提供 Create / Retrieve / Update / Delete conversation 以及 Items 增删查接口。创建会话时 `items` 最多 20 条初始消息，`metadata` 最多 16 对键值对（key ≤ 64 字符，value ≤ 512 字符）。目前支持北京和新加坡地域。详见 [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。

## 在 LangChain 中使用百炼

两种接入路径，详见 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)：

| 方式 | 依赖 | 模型覆盖 |
| --- | --- | --- |
| OpenAI 兼容（`ChatOpenAI` / `@langchain/openai` / LangChain4j） | `langchain_openai` 等 | 仅 OpenAI 兼容模式支持的部分模型 |
| DashScope 原生（`ChatTongyi` / `ChatAlibabaTongyi`） | `langchain-community` + `dashscope` | 百炼所有文本生成模型（含部署后的模型） |

Python 示例（OpenAI 兼容路径）：

```python
from langchain_openai import ChatOpenAI
import os

llm = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-plus",
)
```

> **注意**：LangChain4j 1.0.0-beta3 需要 Java 17+，低版本编译会报 `Unsupported class file major version 61`。

## 通用注意事项

- [API Key](../concepts/api-key.md) 建议配置到环境变量 `DASHSCOPE_API_KEY`，避免硬编码泄露。
- 流式调用建议设置 `stream_options={"include_usage": True}` 以获取 token 统计。
- 错误排查统一参考百炼错误码文档；异常响应通过 `error.code` / `error.message` 指明原因。
- 各地域支持的模型列表有差异，以百炼控制台模型广场为准。

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




