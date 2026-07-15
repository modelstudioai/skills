# toolkits and [frameworks](frameworks.md)

阿里云百炼的通义千问等模型提供了一套与 OpenAI 高度兼容的接口体系，覆盖 Chat Completions、Responses、Completions、Embedding、文件、Batch、Conversations 等能力，并可直接接入 LangChain/LangChain4j 等主流框架。对于已有 OpenAI 应用，通常只需替换 `api_key`、`base_url` 与 `model` 三项即可完成迁移，无需改动业务逻辑。

## 迁移三要素与服务地址

将 OpenAI 应用迁移到百炼的核心是配置以下三项（详见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)）：

- **`api_key`**：替换为[百炼 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。**各地域的 API Key 不同**，切换地域时需同步更换。建议配置到环境变量 `DASHSCOPE_API_KEY` 以降低泄露风险。
- **`base_url`**：OpenAI SDK 调用统一使用 `/compatible-mode/v1` 路径；HTTP 调用在其后追加具体资源路径（如 `/chat/completions`、`/responses`、`/embeddings`、`/files`）。
- **`model`**：替换为百炼支持的模型名称。

各地域 SDK `base_url`：

| 地域 | base_url |
| --- | --- |
| 华北2（北京） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 日本（东京） | `https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |

其中 `{WorkspaceId}` 为业务空间 ID，可在百炼控制台**业务空间详情**页面查看。

> **注意**：百炼为北京、新加坡地域推出了业务空间专属域名，性能与稳定性更佳，建议从旧域名迁移：北京 `https://dashscope.aliyuncs.com` → `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`；新加坡 `https://dashscope-intl.aliyuncs.com` → `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`。现有域名仍可正常使用。

> **注意**：Responses 与 Conversations 接口的旧版路径 `/api/v2/apps/protocols/compatible-mode/v1/...` 即将停止维护，请尽快迁移至新版 `/compatible-mode/v1/...` 路径。

## 各兼容接口一览

### Chat Completions（对话补全）

最常用的兼容接口，支持非流式、流式（`stream=True`，配合 `stream_options={"include_usage": True}` 返回 Token 统计）与 function call（工具调用）。支持模型广泛：Qwen 大语言模型（商业版/开源版）、Qwen-VL、Qwen-Coder、Qwen-Omni、Qwen-Math，以及 DeepSeek、Kimi、GLM、MiniMax 等三方模型。

> **注意**：三方直供模型仅在中国站的中国内地地域可用，调用前需先在百炼控制台开通对应服务。Qwen-Audio 不支持 OpenAI 兼容协议，仅支持 DashScope 协议。

### Responses（智能体原生接口）

作为 Chat Completions 的演进版本，Responses API 内置联网搜索、网页抓取、代码解释器、文搜图/图搜图等工具，输入更灵活（可直接传字符串），并通过 `previous_response_id` 自动管理多轮上下文，无需手动拼接消息历史。详见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。

- 支持模型示例：`qwen3-max`、`qwen3.7-plus`、`qwen-plus`、`qwen-flash`、`qwen3-coder-plus` 等。
- `previous_response_id` 需传入上一轮响应的顶层 `id`（`resp_xxx`），而非 `output` 数组内消息的 `id`；当前响应 `id` 有效期为 **7 天**。

### Conversations（会话管理）

提供会话的创建、查询、更新、删除及消息项管理。配合 Responses API 可自动注入历史上下文，实现跨设备、跨会话的对话延续。初始消息项 `items` 最多 20 条，`metadata` 最多 16 对键值对（key ≤ 64 字符、value ≤ 512 字符）。删除会话时其消息项不会被删除。

### Completions（文本补全）

专为代码补全、内容续写设计，当前仅支持 `qwen-coder-turbo`，且**仅适用于中国内地（北京地域）**。通过 `<|fim_prefix|>...<|fim_suffix|>...<|fim_middle|>` 模板可实现「前缀生成后续」或「前缀+后缀生成中间」两种补全（暂不支持仅凭后缀生成前缀）。关键参数包括 `max_tokens`、`temperature`、`top_p`、`stop`、`seed`、`presence_penalty` 等，详见 [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。

### Embedding（文本向量）

兼容 OpenAI Embedding 规范，支持 `text-embedding-v1/v2/v3/v4`。其中 v3、v4 支持通过 `dimensions` 参数指定向量维度（v4 可选 64~2048 多档，默认 1024）。

> **注意**：多模态 Embedding 模型（如 qwen3-vl-embedding、tongyi-embedding-vision 系列）不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，需改用[多模态向量接口](https://help.aliyun.com/zh/model-studio/multimodal-embedding-api-reference)。

### Vision（视觉理解）

Qwen-VL、QVQ、Qwen-OCR 兼容 OpenAI Chat 接口，通过 `content` 数组中的 `image_url` 传入图片。各地域支持的模型有差异。QVQ 模型仅支持[流式输出](../concepts/streaming.md)。

### 文件接口与 Batch

文件上传接口（`client.files.create`）通过 `purpose` 区分用途，详见 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)：

| purpose | 用途 | 单文件大小上限 |
| --- | --- | --- |
| `file-extract` | Qwen-Long / Qwen-Doc-Turbo 文档问答与数据提取 | 150 MB |
| `batch` | 批量推理输入（jsonl） | 500 MB |
| `fine-tune` | 模型调优数据集（jsonl） | 300 MB |

百炼存储空间上限为 10000 个文件、总计 100 GB，达到任一上限后新上传会失败，需删除文件释放配额。上传返回的文件 ID（如 `file-batch-xxx`）可重复使用。

百炼提供两种批量推理方式，费用均约为实时调用的 **50%**：

- **Batch（文件输入）**：上传 jsonl 文件异步批处理，适合大批量、时效性要求不高的场景（数据分析、模型评测）。可先用测试模型 `batch-test-model` 做全链路验证（文件 ≤ 1 MB、≤ 100 行、最大并行 2 个任务，不产生推理费用）。
- **Batch Chat**：保持与实时 API 一致的同步调用方式，仅需将 `base_url` 改为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`，单次仅支持一个请求；默认等待超时 3600 秒（可设 60~3600 秒）。

> **注意**：Batch 场景下 `enable_thinking` 须作为请求 body 的顶层参数（与 `model` 同级）传入，不能放在 `extra_body` 中；`qwen3.7`/`qwen3.6`/`qwen3.5` 系列默认开启思考模式，会产生额外思考 Token 成本，建议显式设置。

## 框架集成（LangChain）

百炼可通过两条路径接入 LangChain（Python / JavaScript / Java），详见 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)：

- **OpenAI 兼容路径**：使用 `langchain_openai.ChatOpenAI`（JS 为 `@langchain/openai`，Java 为 `langchain4j-open-ai`），配置 `base_url` 指向 `compatible-mode/v1`。**仅支持 OpenAI 兼容模式覆盖的部分模型**。
- **DashScope 原生路径**：使用 `ChatTongyi`（`langchain-community` + `dashscope`）或 JS 的 `ChatAlibabaTongyi`，**支持百炼所有文本生成模型（含部署后的模型）**。

> **注意**：LangChain4j 1.0.0-beta3 需要 Java 17 及以上版本，使用 Java 11 编译会报 `Unsupported class file major version 61` 错误。

## 限制与注意事项

- **地域隔离**：API Key 与 `base_url` 均按地域区分，跨地域调用必须成对更换；不同接口/模型在各地域的可用性存在差异，以[百炼控制台](https://bailian.console.aliyun.com/)为准。
- **协议差异**：并非所有模型都支持 OpenAI 兼容协议（如 Qwen-Audio、多模态 Embedding），此类模型需使用 DashScope 原生协议。
- **端点区别**：普通请求走各地域 `compatible-mode/v1`，而 Batch Chat 使用独立的 `batch.dashscope.aliyuncs.com` 域名。
- 调用失败时请参考[错误码](https://help.aliyun.com/zh/model-studio/error-code)排查。

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


