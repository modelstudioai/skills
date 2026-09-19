# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 OpenAI 兼容的工具包与框架接口，覆盖文本生成、[多模态](../concepts/multimodal.md)理解、向量嵌入、批量处理、会话管理等核心场景。开发者可复用现有 OpenAI SDK 代码，仅需调整 `base_url`、`api_key` 和模型名即可快速迁移；同时支持 LangChain 等主流生态框架，降低大模型应用集成门槛。

## 支持的模型/功能

百炼兼容接口支持三大类能力：  
- **通用对话**：通过 `chat/completions`（[OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）和增强型 `responses`（[OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)）实现标准及智能体原生交互；  
- **专用任务**：`completions` 接口专用于代码补全（FIM 模式），仅支持 `qwen-coder-turbo`；`embeddings` 接口支持多维度文本向量化（如 `text-embedding-v4`、`qwen3.7-text-embedding-flash`）；`vision` 接口支持图文理解（如 `qwen3-vl-plus`、`qwen3-vl-flash`）；  
- **状态管理**：`conversations` 接口提供跨设备会话持久化能力，配合 `responses` 自动注入历史上下文；`files` 接口统一管理文档分析、批量推理与微调所需文件资源。

> **注意**：`qwen-audio` 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；`qwen3.8-omni-flash` 在 `responses` 接口中支持音视频输入，但在 `chat/completions` 中未明确声明支持，需以实际调用为准。

## 关键参数

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `base_url` | 必填服务端点，格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1` | `{WorkspaceId}` 需从控制台获取；旧域名（如 `dashscope.aliyuncs.com`）仍可用但性能与稳定性较低，[强烈建议迁移](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) |
| `model` | 模型名称，区分大小写且严格匹配 | `qwen3.8-max` 等新系列模型在 `responses` 接口有完整 Agent 能力，但在 `chat/completions` 中部分功能受限；`qwen-coder-turbo` 仅支持 `completions` 接口 |
| `enable_thinking` | 控制思考模式开关（`true`/`false`），影响 token 计费 | 默认开启，`qwen3.5`~`qwen3.8` 系列均适用；必须作为请求体顶层参数传入，不可置于 `extra_body` 内 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) |
| `dimensions` | 向量维度（仅 `text-embedding-v3`/`v4` 支持） | `text-embedding-v2`/`v1` 不支持该参数，传入将被忽略 |
| `previous_response_id` | `responses` 接口多轮对话的关键上下文锚点 | 必须传入上一轮响应的顶层 `id`（UUID 格式），而非 `output` 数组内消息的 `id` [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) |

## 使用方式

### 基础调用流程
1. **配置环境**：安装对应 SDK（如 `pip install -U openai langchain_openai`），将 `DASHSCOPE_API_KEY` 配置至环境变量；  
2. **初始化客户端**：设置 `base_url`（按地域选择，如北京：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）；  
3. **发起请求**：根据场景选择接口路径（`/chat/completions`、`/responses`、`/embeddings` 等）并传入参数。

### 多框架适配示例
- **纯 OpenAI SDK**：直接替换 `base_url` 和 `model` 即可调用 `chat.completions.create()`、`embeddings.create()` 等方法；  
- **LangChain**：推荐使用 `langchain_openai.ChatOpenAI`（兼容部分模型）或 `langchain_community.chat_models.tongyi.ChatTongyi`（支持全部百炼模型）[在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)；  
- **批量处理**：  
  - 单请求批处理：使用 `batch.dashscope.aliyuncs.com` 域名调用 `/chat/completions`（[OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)）；  
  - 多请求批处理：上传 JSONL 文件后调用 `/batches`（[OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)）。

## 限制和注意事项

- **地域绑定**：API Key 与 `base_url` 所属地域强绑定，北京 Key 无法调用弗吉尼亚 endpoint，否则返回 `invalid_api_key` 错误 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)；  
- **模型能力差异**：`responses` 接口支持内置工具（联网搜索、代码解释器等），而 `chat/completions` 仅支持基础 function calling；`qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出；  
- **文件限制**：`files` 接口按 `purpose` 区分用途——`file-extract`（最大 150 MB）、`batch`（最大 500 MB）、`fine-tune`（最大 300 MB）；总存储上限为 100 GB / 10000 文件；  
- **超时与重试**：`batch chat` 默认等待 3600 秒，需显式设置 `timeout` 参数（如 Python 的 `with_options(timeout=1800.0)`）；`responses` 接口 `previous_response_id` 有效期为 7 天；  
- **废弃路径**：`/api/v2/apps/protocols/compatible-mode/v1/responses` 和 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 已停用，必须迁移到 `/compatible-mode/v1/{responses,conversations}`。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)


