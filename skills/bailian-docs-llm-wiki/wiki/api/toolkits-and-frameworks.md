# toolkits and [frameworks](frameworks.md)

阿里云百炼提供一系列 OpenAI 兼容的工具包与框架接口，覆盖文本生成、多模态理解、向量化、批量推理、会话管理及文件处理等核心场景。开发者可复用现有 OpenAI SDK 和生态代码，仅需调整 `base_url`、`api_key` 和模型名即可快速迁移。所有接口均支持主流编程语言（Python/Node.js/Java/Go/C# 等）及 HTTP 直调，并通过业务空间专属域名提升稳定性与性能。

## 支持的模型/功能

- **文本与智能体能力**：`qwen4-max`、`qwen3.8-max`、`qwen3.7-plus` 等全系列千问模型，以及 `deepseek-v4-pro`、`glm-5.3`、`kimi-k3` 等三方直供模型，均支持 OpenAI Chat Completions API；其中 `qwen3.8-max` 及更高版本还支持 Responses API 的内置工具（联网搜索、代码解释器、文搜图等）和自动上下文注入能力 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。
- **多模态理解**：`qwen3-vl-plus`、`qwen3.5-omni-plus`、`qwen-vl-ocr` 等视觉模型兼容 OpenAI Vision 接口，支持图像 URL 与 Base64 编码输入 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。
- **[向量嵌入](../concepts/vector-embedding.md)**：`text-embedding-v4`、`qwen3.7-text-embedding` 等 Embedding 模型支持 OpenAI Embeddings API，但**不支持稀疏向量输出**（传入 `output_type=sparse` 将返回空 embedding）[OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。
- **长文档与结构化数据**：`qwen-long`、`qwen-doc-turbo` 支持通过文件 ID 进行文档问答与数据提取；`qwen3.5-omni-plus` 在 Batch 场景下支持 256K 上下文，但**不支持语音输出** [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。
- **会话状态管理**：Conversations API 提供跨设备、跨会话的上下文持久化能力，配合 Responses API 实现无状态客户端的智能对话延续 [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。

> **注意**：文档 4（Chat 接口兼容）称“Qwen-Audio 不支持 OpenAI 兼容协议”，而文档 1（Responses 接口兼容）明确列出 `qwen3.8-omni-flash` 可用于音视频输入。二者存在功能覆盖矛盾——实际以 Responses API 为音视频处理的唯一 OpenAI 兼容入口，Chat API 不支持音视频。

## 关键参数

| 参数 | 说明 | 示例值 | 注意事项 |
|------|------|--------|----------|
| `base_url` | 必填，服务端点。**必须使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名（`dashscope.aliyuncs.com`）已逐步弃用 | `https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `{WorkspaceId}` 需替换为控制台获取的真实 ID；地域与 API Key 必须严格匹配，跨地域调用将返回 `invalid_api_key` 错误 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) |
| `model` | 必填，模型名称。不同接口支持范围不同：Chat/Responses/Batch Chat 支持 `qwen4-max` 等通用模型；Vision 接口仅支持 `qwen3-vl-plus` 等视觉模型；Embedding 接口仅支持 `text-embedding-v4` 等向量模型 | `"qwen3.7-plus"`, `"qwen3-vl-plus"`, `"text-embedding-v4"` | 三方模型（如 DeepSeek、Kimi）仅在华北2（北京）地域可用，且需在控制台手动开通服务 |
| `enable_thinking` | 可选（Batch 场景关键），控制是否启用思考模式。`qwen3.5+` 系列默认开启，显式设为 `false` 可避免额外 reasoning tokens 成本 | `{"enable_thinking": false}` | **必须作为 JSONL 请求体顶层字段传入**，不可置于 `extra_body` 内；该参数在 Batch Chat 和 Batch File 接口中均生效 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) |
| `previous_response_id` | Responses API 多轮对话专用，用于自动注入历史上下文。值为上一轮响应的顶层 `id`（UUID 格式），非 `output[].id` | `"0c842a11-c7d1-45da-b7ec-4e668c389xxx"` | 有效期为 7 天；若传入错误格式（如 `msg_xxx`）将导致上下文丢失 |

## 使用方式

- **SDK 调用**：统一使用 OpenAI 官方 SDK（`openai` / `@langchain/openai` / `langchain_openai`），仅需配置 `base_url` 和 `api_key`。LangChain 用户还可选用 `langchain-community` 中的 `ChatTongyi`，支持全部百炼文本模型（含未开放 OpenAI 兼容的部署模型）[在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。
- **HTTP 调用**：所有接口均提供标准 RESTful endpoint，如：
  - Chat：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`
  - Responses：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses`
  - Conversations：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/conversations`
  - Embeddings：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings`
- **文件操作**：通过 `/files` 接口上传文件，`purpose` 字段区分用途：
  - `file-extract`：用于 `qwen-long`/`qwen-doc-turbo` 文档分析（单文件 ≤150 MB）
  - `batch`：用于批量推理任务（单文件 ≤500 MB）
  - `fine-tune`：用于模型调优（单文件 ≤300 MB）[OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。
- **批量处理**：
  - **Batch Chat**：单请求同步等待（最长 3600 秒），适用于低频、高成本任务，端点为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`；
  - **Batch File**：JSONL 文件异步提交，支持千级并发，费用为实时调用的 50%，适用于大规模评测与标注 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。

## 限制和注意事项

- **地域绑定强制**：API Key 与 `base_url` 所属地域必须一致（如北京 Key + 北京 `base_url`），否则返回 `invalid_api_key`（HTTP 401），**并非密钥失效** [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
- **路径迁移**：所有接口的旧版路径（如 `/api/v2/apps/protocols/compatible-mode/v1/responses`）已停止维护，必须迁移至新版 `/compatible-mode/v1/{endpoint}`。
- **模型能力差异**：非阿里云直供模型（如 SiliconFlow DeepSeek、月之暗面 Kimi）仅支持基础 Chat 功能，**不支持 Responses API 的内置工具、Conversations 上下文管理等高级特性**；Qwen-Audio 完全不兼容 OpenAI 协议，仅支持 DashScope 原生接口。
- **Batch 特定约束**：
  - `qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出；
  - `enable_thinking` 参数必须置于 JSONL `body` 顶层，否则无效；
  - 测试模型 `batch-test-model` 仅限验证链路，有 1 MB / 100 行 / 2 并发等硬性限制。
- **Embedding 限制**：[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**不支持稀疏向量**（`output_type=sparse` 返回空结果），如需该能力，必须调用 DashScope 原生接口。

## 来源文档

- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)


