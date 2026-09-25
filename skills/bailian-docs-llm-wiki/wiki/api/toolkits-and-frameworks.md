# toolkits and [frameworks](frameworks.md)

阿里云百炼提供多套 OpenAI 兼容的工具包与框架接口，覆盖文本生成、视觉理解、向量嵌入、文件处理、批量推理及会话管理等核心场景。开发者可复用现有 OpenAI SDK 代码，仅需调整 `base_url`、`api_key` 和模型名即可快速迁移。所有接口均支持主流编程语言（Python/Node.js/Java/Go/C#/JavaScript）及 HTTP 直调。

## 支持的模型/功能

- **文本生成**：支持 `qwen3.8-max`、`qwen3.7-plus`、`deepseek-v4-pro`、`glm-5.3` 等数十种大语言模型，涵盖 Max/Plus/Flash/Omni 系列；[OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) 提供内置工具（联网搜索、代码解释器等）和自动上下文关联能力。
- **视觉理解**：`qwen3-vl-plus`、`qwen3-vl-flash`、`qwen-vl-ocr` 等模型支持图像/视频输入，兼容 OpenAI Vision 规范，但 [QVQ 模型仅支持流式输出](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。
- **向量嵌入**：`text-embedding-v4`、`qwen3.7-text-embedding` 等模型支持多语种、多维度向量化，但注意 [OpenAI 兼容接口不支持稀疏向量输出](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。
- **长文档与文件处理**：`Qwen-Long` 和 `Qwen-Doc-Turbo` 支持通过文件 ID 进行问答与数据提取；文件上传接口支持 `file-extract`（文档分析）、`batch`（批量任务）、`fine-tune`（调优数据集）三种用途。
- **批量处理**：提供两种模式——`Batch File API`（异步、JSONL 文件输入、成本降低 50%）和 `Batch Chat API`（同步、单请求、保持连接等待结果），二者在模型支持范围和参数配置上存在差异，详见下文限制说明。
- **会话管理**：`Conversations API` 支持跨设备会话创建、元数据更新与消息项追加，配合 `Responses API` 实现无状态上下文延续。

> **注意**：文档 6（Batch File）与文档 7（Batch Chat）对同一模型（如 `qwen3.8-max`）的上下文 [Token](../concepts/token.md) 上限描述一致（256K），但文档 7 明确要求 `enable_thinking` 参数须置于 JSONL `body` 顶层，而文档 6 未强调此约束，实际使用时应以文档 7 的规范为准，避免因参数位置错误导致思考模式未生效或报错。

## 关键参数

| 参数 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `base_url` | string | 必填。推荐使用业务空间专属域名（性能更优），格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`；旧域名（如 `dashscope.aliyuncs.com`）仍可用但不推荐。 | `https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `model` | string | 必填。模型名需严格匹配支持列表，大小写敏感；第三方直供模型（如 SiliconFlow DeepSeek）仅在中国站华北2（北京）地域可用。 | `qwen3.8-max`, `text-embedding-v4` |
| `enable_thinking` | boolean | 部分 Qwen3 系列模型默认开启思考模式，显式设置 `false` 可关闭以降低成本。**必须作为 `body` 顶层参数传入，不可置于 `extra_body` 中**。 | `true`, `false` |
| `previous_response_id` | string | 仅 `Responses API` 使用。传入上一轮响应的顶层 `id`（UUID 格式），用于自动关联上下文；**不可传 `output` 数组内消息的 `id`**。 | `"0c842a11-c7d1-45da-b7ec-4e668c389xxx"` |
| `purpose` | string | 文件接口必填。决定文件用途：`file-extract`（文档分析）、`batch`（批量任务）、`fine-tune`（调优数据集）。 | `"file-extract"` |

## 使用方式

1. **环境准备**：  
   - 获取并配置 [API Key](../../raw/model-api-reference/preparations/get-api-key.md) 到环境变量（推荐）或代码中；  
   - 安装对应 SDK：`pip install -U openai`（基础）、`pip install langchain_openai`（LangChain）、`pip install dashscope`（原生）。

2. **SDK 调用示例（通用流程）**：  
   ```python
   from openai import OpenAI
   client = OpenAI(
       api_key=os.getenv("DASHSCOPE_API_KEY"),
       base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
   )
   # 根据接口类型调用不同方法：
   # - Chat: client.chat.completions.create(...)
   # - Responses: client.responses.create(...)
   # - Embeddings: client.embeddings.create(...)
   # - Files: client.files.create(...)
   # - Conversations: client.conversations.create(...)
   # - Batches: client.batches.create(...)  # Batch File
   ```

3. **HTTP 调用示例（通用流程）**：  
   ```bash
   curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/{endpoint} \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"model":"qwen3.8-max","input":"Hello"}'
   ```
   其中 `{endpoint}` 替换为 `chat/completions`、`responses`、`embeddings`、`files`、`conversations` 或 `batches`。

4. **LangChain 集成**：  
   - 推荐使用 `langchain_openai.ChatOpenAI`（兼容部分模型）或 `langchain_community.chat_models.tongyi.ChatTongyi`（支持全部百炼模型）；详细配置见 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

## 限制和注意事项

- **地域与 API Key 绑定**：API Key 严格按地域创建，**北京地域 Key 不可用于调用弗吉尼亚 endpoint**，否则返回 `invalid_api_key` 错误（HTTP 401），而非权限不足。请确保 Key 与 `base_url` 地域一致。
- **模型能力差异**：  
  - `Qwen-Audio` **不支持** OpenAI 兼容协议，仅支持 DashScope 原生协议；  
  - `qwen3.8-omni-flash` 支持音视频输入，但需通过 Omni 专用路径调用，非标准 `/chat/completions`；  
  - 三方直供模型（如 DeepSeek、Kimi）仅在华北2（北京）地域开通，且需在控制台手动授权。
- **Batch 接口关键区别**：  
  - `Batch File API`（文档 6）是异步、JSONL 文件驱动，适用于海量请求；  
  - `Batch Chat API`（文档 7）是同步、单请求驱动，适用于单次高成本推理；  
  - 二者 `base_url` 不同：前者用 `https://dashscope.aliyuncs.com/compatible-mode/v1`，后者用 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`。混淆将导致 404。
- **服务端点迁移**：  
  - `Responses API` 旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停用，请迁至 `/compatible-mode/v1/responses`；  
  - `Conversations API` 旧路径 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 即将停用，请迁至 `/compatible-mode/v1/conversations`。
- **文件配额**：百炼存储空间上限为 **10,000 个文件** 或 **100 GB 总大小**，任一达到即拒绝新上传；`file-extract` 单文件最大 150 MB，`batch` 单文件最大 500 MB，`fine-tune` 单文件最大 300 MB。

## 来源文档

- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)


