# toolkits and [frameworks](frameworks.md)

阿里云百炼平台提供多种 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)与专用工具链，支持开发者快速集成文本生成、多模态理解、[向量化](../concepts/embedding.md)、批量推理、对话状态管理等能力。所有接口均基于标准 OpenAI SDK 调用范式，仅需调整 `base_url`、`api_key` 和模型名称即可迁移现有代码；同时提供百炼原生增强能力（如 Responses API 的内置工具、Conversations 的上下文自动维护），兼顾兼容性与生产力。

## 支持的模型/功能

- **文本生成**：支持 `qwen3.8-max`、`qwen-plus`、`qwen-flash`、`qwen-long` 等全系列千问模型，以及 DeepSeek、GLM、Kimi、MiniMax 等第三方直供模型（详见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）。
- **代码补全**：`completions` 接口专为 FIM（Fill-in-the-Middle）场景优化，支持 `qwen-coder-turbo` 模型，适用于函数签名补全、文档驱动开发等场景 [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。
- **多模态理解**：`qwen-vl-plus`、`qwen3-vl-plus` 等视觉模型支持图像输入，兼容 OpenAI Vision 规范，可处理 `image_url` 或 Base64 编码图片 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。
- **向量嵌入**：`text-embedding-v4`、`qwen3.7-text-embedding` 等模型支持高维稠密向量生成，兼容 OpenAI Embedding 接口，但**不支持稀疏向量输出**（传入 `output_type=sparse` 将返回空 embedding）[OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。
- **长文档与文件分析**：`Qwen-Long` 和 `Qwen-Doc-Turbo` 可通过上传文件（`purpose=file-extract`）实现文档问答与结构化数据提取 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。
- **智能体增强**：`Responses API` 内置联网搜索、网页抓取、代码解释器等工具，支持 `previous_response_id` 自动上下文关联，显著简化 Agent 开发 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。

> **注意**：`Qwen-Audio` 模型明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；`qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出，且 `qwen3.8-max` 等系列模型默认开启思考模式，可能产生额外 `reasoning_tokens` 成本（见 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)）。

## 关键参数

| 参数 | 类型 | 说明 | 注意事项 |
|------|------|------|----------|
| `base_url` | string | 服务端点地址 | 必须与 API Key 所在地域严格匹配（如北京地域 Key 必须配北京 `base_url`），否则返回 `invalid_api_key` 错误；推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）以获得更高稳定性 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) |
| `model` | string | 模型标识符 | 不同接口支持的模型范围不同：`completions` 仅支持 `qwen-coder-turbo`；`chat/completions` 支持全系列文本模型；`embeddings` 仅限向量模型；`responses` 仅限列表中明确标注的模型（如 `qwen3.8-max`） |
| `stream` / `stream_options` | boolean / object | [流式输出](../concepts/streaming.md)控制 | `stream_options={"include_usage": true}` 可在流式响应末尾返回 token 统计；`qwen-vl-plus` 模型**仅支持[流式输出](../concepts/streaming.md)** [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md) |
| `enable_thinking` | boolean | 思考模式开关 | 对 `qwen3.5+` 系列模型有效，必须作为 `body` 顶层参数传入（不可放在 `extra_body` 中），默认 `true`，关闭可降低成本 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) |
| `previous_response_id` | string | 上下文关联 ID | 用于 `Responses API` 多轮对话，必须传入上一轮响应的顶层 `id`（如 `resp_xxx`），而非 `output` 数组内消息的 `id`（如 `msg_xxx`） |

## 使用方式

### 1. 基础调用（SDK）
统一配置 `OpenAI` 客户端：
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 从环境变量读取
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 替换为实际 WorkspaceId
)
```

- **Chat**：`client.chat.completions.create(model="qwen-plus", messages=[...])`
- **Completions**：`client.completions.create(model="qwen-coder-turbo", prompt="<tool_call>{prefix}<tool_call>{suffix}<tool_call>")`
- **Embeddings**：`client.embeddings.create(model="text-embedding-v4", input="...")`
- **Responses**：`client.responses.create(model="qwen3.8-max", input="...")`
- **Conversations**：`client.conversations.create(items=[...])`
- **Files**：`client.files.create(file=Path("doc.pdf"), purpose="file-extract")`

### 2. 批量处理
- **单请求批量**（Batch Chat）：将 `base_url` 改为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`，保持 `chat/completions` 路径，客户端同步等待结果 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。
- **文件批量**（Batch File）：先上传 JSONL 文件（`purpose="batch"`），再调用 `client.batches.create(input_file_id="file-batch-xxx", endpoint="/v1/chat/completions")` [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。

### 3. 框架集成
- **LangChain**：优先使用 `langchain_openai.ChatOpenAI`（兼容部分模型）或 `langchain_community.chat_models.tongyi.ChatTongyi`（支持全部百炼模型）[在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。
- **LangChain4j（Java）**：使用 `OpenAiChatModel.builder()` 配置百炼 `base_url` 和 `apiKey` 即可。

## 限制和注意事项

- **地域绑定强制**：API Key 与 `base_url` 地域必须一致（如北京 Key 不能调用弗吉尼亚 `base_url`），否则返回 HTTP 401 `invalid_api_key`，此规则适用于所有地域（北京、新加坡、弗吉尼亚、东京等）[OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- **FIM 语法约束**：`completions` 接口要求提示词严格使用 `<tool_call>{prefix}<tool_call>{suffix}</tool_call>` 格式，不支持仅后缀补全 [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。
- **文件配额限制**：百炼文件存储上限为 10,000 个文件或总大小 100 GB，超出后上传失败，需手动清理旧文件 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。
- **模型能力差异**：`qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出；`qwen-vl-plus` 仅支持[流式输出](../concepts/streaming.md)；`Qwen-Audio` 完全不兼容 OpenAI 协议。
- **超时设置**：Batch Chat 默认超时 3600 秒（1 小时），需通过 SDK 的 `timeout` 参数或 HTTP `timeout` 显式配置，避免连接中断。

## 来源文档

- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)


