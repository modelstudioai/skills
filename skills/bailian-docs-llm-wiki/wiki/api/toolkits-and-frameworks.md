# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 [OpenAI 兼容接口](../concepts/openai-compatibility.md)工具包与框架，覆盖文本生成、多模态理解、向量嵌入、批量处理、会话管理等核心场景。开发者可复用现有 OpenAI SDK 代码，仅需调整 `base_url`、`api_key` 和 `model` 即可快速迁移。所有接口均支持 Python、Node.js、Java、Go 等主流语言的 OpenAI SDK 调用，并兼容 HTTP 直连方式。

## 支持的模型/功能

百炼 [OpenAI 兼容接口](../concepts/openai-compatibility.md)支持以下模型类型及对应能力：

- **文本生成**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash`、`deepseek-v4-pro`、`glm-5.3`、`kimi-k3` 等（详见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）；
- **视觉理解**：`qwen3-vl-plus`、`qwen3-vl-flash`、`QVQ`、`Qwen-OCR`，支持图像/视频输入与结构化输出（详见 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)）；
- **向量嵌入**：`text-embedding-v4`、`qwen3.7-text-embedding`、`text-embedding-v2`，支持多语种与可选维度（详见 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)）；
- **代码补全**：`qwen-coder-turbo`，专用于 FIM（Fill-in-the-Middle）模式的代码生成（详见 [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)）；
- **智能体增强**：`qwen3.8-omni-flash`（音视频输入）、`qwen3.8-max`（内置联网搜索、网页抓取、代码解释器等工具），通过 Responses API 实现原生 Agent 能力（详见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)）；
- **长文档处理**：`Qwen-Long`、`Qwen-Doc-Turbo`，依赖文件上传接口（`purpose=file-extract`）实现问答与数据提取（详见 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)）。

> **注意**：`Qwen-Audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议；`qwen3.8-omni-flash` 在 Responses API 中支持音视频输入，但在 Chat Completions API 中未明确声明支持，需以 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) 文档为准。

## 关键参数

| 参数 | 说明 | 示例值 | 注意事项 |
|------|------|--------|----------|
| `base_url` | 服务端点，**必须按地域匹配 Workspace ID** | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `{WorkspaceId}` 需从控制台业务空间详情页获取；旧域名（如 `dashscope.aliyuncs.com`）仍可用但不推荐，性能与稳定性较低（见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)） |
| `api_key` | 地域绑定，**不可跨地域混用** | `sk-xxx` | 使用北京地域 API Key 调用弗吉尼亚 endpoint 将返回 `invalid_api_key` 错误，而非权限不足（见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)） |
| `model` | 模型名称，区分大小写且严格匹配 | `qwen3.8-max`, `text-embedding-v4` | 第三方直供模型（如 SiliconFlow DeepSeek）仅在中国站华北2（北京）地域可用，且需在控制台手动开通（见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)） |
| `enable_thinking` | 控制是否启用思考模式（影响 token 成本） | `true` / `false` | `qwen3.8`/`qwen3.7`/`qwen3.6`/`qwen3.5` 系列默认开启；该参数须置于 JSONL 请求体顶层（与 `model` 同级），不可放入 `extra_body`（见 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)） |
| `dimensions` | 仅 `text-embedding-v3`/`v4` 支持 | `1024` | `text-embedding-v1`/`v2` 不支持此参数；传入将被忽略 |

## 使用方式

### 1. 基础调用（Chat Completions）
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

response = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "你好"}],
    stream=True,
    stream_options={"include_usage": True}
)
```

### 2. 批量处理（Batch File）
- 上传 JSONL 文件（`purpose=batch`）→ 创建 Batch 任务 → 轮询状态 → 下载结果；
- 支持 `qwen3.8-max` 等模型单次请求最大 256K context tokens；
- 测试模型 `batch-test-model` 可用于链路验证（见 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)）。

### 3. 文件处理（Document & Batch）
- 上传文档：`purpose=file-extract`（用于 Qwen-Long/Qwen-Doc-Turbo）；
- 上传批量任务：`purpose=batch`（JSONL 格式，最大 500 MB）；
- 上传微调数据：`purpose=fine-tune`（JSONL 格式，最大 300 MB）（见 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)）。

### 4. LangChain 集成
- **OpenAI 方式**：使用 `langchain_openai.ChatOpenAI`，仅支持部分模型（如 `qwen-plus`），`base_url` 指向 `https://dashscope.aliyuncs.com/compatible-mode/v1`；
- **DashScope 方式**：使用 `langchain_community.chat_models.tongyi.ChatTongyi`，支持全部百炼模型（见 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)）。

### 5. 会话管理（Conversations API）
- 创建会话并注入初始消息（`system`/`user` 角色）；
- 通过 `conversation_id` 复用上下文，避免手动维护 message history；
- 支持元数据存储（最多 16 对 key-value）（见 [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)）。

## 限制和注意事项

- **地域强绑定**：API Key 与 `base_url` 所属地域必须一致，跨地域调用将返回 `invalid_api_key`（HTTP 401），非密钥失效（见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）；
- **模型能力差异**：Responses API 的 Agent 能力（如内置工具）仅对列表中阿里云直供模型完整支持；第三方模型（如 `deepseek-v4-pro`）在 Responses API 中可能受限（见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)）；
- **Embedding 稀疏向量限制**：[OpenAI 兼容接口](../concepts/openai-compatibility.md)不支持 `output_type=sparse`；若需稀疏向量，必须调用原生 DashScope 接口（见 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)）；
- **Batch Chat 超时**：同步批量调用（`/chat/completions`）默认超时 3600 秒，最长不可超过此值；异步 Batch File 则由 `completion_window` 控制（最长 24h）；
- **文件配额**：百炼文件存储上限为 10,000 个文件或 100 GB 总大小，达限时新上传将失败（见 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)）。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)


