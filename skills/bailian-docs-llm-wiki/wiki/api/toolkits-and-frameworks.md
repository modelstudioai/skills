# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 OpenAI 兼容的工具包与框架，覆盖文本生成、多模态理解、向量嵌入、批量推理、会话管理等核心场景。开发者可复用现有 OpenAI 生态代码（如 SDK、LangChain 集成），仅需调整 `base_url`、`api_key` 和模型名即可快速迁移。所有接口均支持标准 OpenAI REST API 语义与 SDK 调用模式。

## 支持的模型/功能

- **文本生成**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash` 等全系列 Qwen 模型，以及 DeepSeek、GLM、Kimi、MiniMax 等三方直供模型（详见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）。
- **多模态理解**：`qwen3-vl-plus`、`QVQ`、`Qwen-OCR` 支持图像/视频输入；`qwen3.8-omni-flash` 支持音视频输入（详见 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)）。
- **向量嵌入**：`text-embedding-v4`、`qwen3.7-text-embedding`、`qwen3.7-text-embedding-flash` 等，支持多语种与可选维度（详见 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)）。
- **批量处理**：支持两种模式——文件批量（JSONL 输入）和单请求同步批量（Batch Chat），适用于评测、标注等非实时场景（详见 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) 和 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)）。
- **会话与上下文管理**：`Conversations API` 提供会话生命周期管理（创建/更新/删除），配合 `Responses API` 的 `previous_response_id` 实现跨设备、跨中断的上下文自动注入（详见 [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md) 和 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)）。
- **文件处理**：`Files API` 支持上传文档用于 Qwen-Long/Qwen-Doc-Turbo 的问答、批量推理输入或调优数据集（详见 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)）。

> **注意**：`Qwen-Audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议（见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）。另，`Responses API` 的旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停止维护，必须迁移到 `/compatible-mode/v1/responses`（见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)）。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `base_url` | 必填。地域专属业务空间域名，**强烈建议使用新域名**以获得更高性能与稳定性。格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`。`{WorkspaceId}` 在控制台「业务空间详情」中获取。 | `https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `api_key` | 必填。API Key **严格按地域绑定**：北京地域 Key 只能调用北京 endpoint，新加坡 Key 只能调用新加坡 endpoint。混用将返回 `invalid_api_key` 错误（见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）。 | `sk-xxx` |
| `model` | 必填。模型名需与所选接口能力匹配。例如：`qwen3-vl-plus` 仅适用于 Vision 接口；`text-embedding-v4` 仅适用于 Embedding 接口；`batch-test-model` 仅用于 Batch 文件测试。 | `qwen3.8-max`, `text-embedding-v4`, `qwen3-vl-plus` |
| `purpose` (Files API) | 必填。指定文件用途，影响后续处理逻辑：`file-extract`（文档分析）、`batch`（批量任务输入）、`fine-tune`（调优数据集）。 | `file-extract`, `batch`, `fine-tune` |
| `previous_response_id` (Responses API) | 可选。传入上一轮 `responses.create()` 返回的顶层 `id`（UUID 格式），用于自动关联上下文。有效期 7 天。 | `0c842a11-c7d1-45da-b7ec-4e668c389xxx` |
| `enable_thinking` (Batch) | 可选。`qwen3.5+` 系列模型默认开启思考模式，显式设为 `false` 可避免额外 `reasoning_tokens` 成本。须作为 `body` 顶层参数，不可置于 `extra_body` 内。 | `true`, `false` |

## 使用方式

1. **初始化客户端**：配置 `api_key`（推荐环境变量）和 `base_url`（务必替换 `{WorkspaceId}`）。
   ```python
   from openai import OpenAI
   client = OpenAI(
       api_key=os.getenv("DASHSCOPE_API_KEY"),
       base_url="https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
   )
   ```

2. **选择接口与方法**：
   - 文本对话：`client.chat.completions.create(...)`
   - 响应式智能体：`client.responses.create(...)`（支持内置工具）
   - 向量嵌入：`client.embeddings.create(...)`
   - 批量文件处理：`client.files.create(purpose="batch")` + `client.batches.create(...)`
   - 会话管理：`client.conversations.create(...)` + `client.conversations.items.create(...)`
   - 视觉理解：`client.chat.completions.create(...)`（`messages` 中含 `image_url`）

3. **LangChain 集成**：优先选用 `langchain_openai`（兼容部分模型）或 `langchain-community`（支持全部模型及部署实例）。注意 `ChatTongyi` / `ChatAlibabaTongyi` 使用 DashScope 原生协议，`ChatOpenAI` 使用 OpenAI 兼容协议（见 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)）。

## 限制和注意事项

- **地域隔离**：API Key 与 `base_url` 地域必须严格一致，跨地域调用将被鉴权拒绝（HTTP 401，`invalid_api_key`），而非密钥失效（见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）。
- **模型能力差异**：非阿里云直供模型（如三方 DeepSeek、Kimi）仅支持基础 Chat Completions 能力，`Responses API` 的内置工具（联网搜索、代码解释器等）不可用（见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)）。
- **文件配额**：Files API 总存储上限为 100 GB 或 10,000 个文件，任一达到即阻塞新上传（见 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)）。
- **Embedding 输出限制**：[OpenAI 兼容接口](../concepts/openai-compatibility.md)不支持稀疏向量（`output_type=sparse`），传入该参数将导致 embedding 结果为空（见 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)）。
- **Batch 超时**：Batch Chat 默认等待 3600 秒（1 小时），超时后连接断开并报错；Batch File 任务最长等待时间也为 24 小时（见 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md) 和 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)）。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)


