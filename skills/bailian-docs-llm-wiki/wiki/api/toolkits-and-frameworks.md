# toolkits and [frameworks](frameworks.md)

阿里云百炼通过 **[OpenAI 兼容接口](../concepts/openai-compatible-api.md)** 让原有 OpenAI 应用零改造迁移，仅需替换 `api_key`、`base_url` 和 `model` 三个参数。覆盖范围包括 Chat Completions、Responses、Completions、Vision、Embedding、Files、Batch（同步/文件输入）、Conversations 共八类接口；同时为 LangChain / LangChain4j 等主流框架提供原生集成。本页汇总各兼容接口的支持模型、服务地址、关键参数与使用方式，便于在工具链中快速选型。

## 通用接入：三个参数

所有 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)都共享一致的接入模型：

| 参数 | 取值 |
| --- | --- |
| `api_key` | 阿里云百炼 API Key（**各地域 Key 互不通用**） |
| `base_url` | 见下方"服务地址"小节 |
| `model` | 百炼模型名称（如 `qwen-plus`、`qwen3-vl-plus`、`text-embedding-v4` 等） |

调用方式可参考 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) 中的 Python / Node.js / curl 示例。

### 服务地址（base_url）

| 地域 | base_url（兼容模式根路径） |
| --- | --- |
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |
| Batch（同步/文件输入） | `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`（中国内地） |

> **注意**：新加坡地域旧版域名 `https://dashscope-intl.aliyuncs.com` 即将下线，请迁移至 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`，其中 `{WorkspaceId}` 需替换为真实的 Workspace ID。

> **注意**：Responses 与 Conversations 接口的旧版 URL 路径 `/api/v2/apps/protocols/compatible-mode/v1/...` 即将停止维护，请迁移至新版路径 `/compatible-mode/v1/...`。

## 各兼容接口概览

### 1. Chat Completions（`/v1/chat/completions`）

最常用的对话接口，支持千问商业版（Max/Plus/Flash/Turbo/Coder/Long/Math、QwQ）、开源版（qwen3 系列、qwen3.5/3.6 系列、codeqwen 等）以及多个地域差异化模型。完整模型矩阵（中国内地 / 美国 / 国际 / 全球）与示例代码见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。

### 2. Responses（`/v1/responses`）

Chat Completions 的演进版本，面向智能体场景：

- **内置工具**：联网搜索、网页抓取、代码解释器、文搜图、图搜图等
- **更灵活的输入**：支持字符串或 Chat 格式消息数组
- **简化上下文管理**：通过 `previous_response_id` 自动关联上一轮响应（顶层 `id`，UUID 格式，有效期 7 天），无需手动构建消息历史

支持模型示例：`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.5-plus`、`qwen3.6-flash`、`qwen3-coder-plus`、`qwen3-coder-flash` 等。详见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。

### 3. Completions（`/v1/completions`）

专为文本/代码补全设计，支持两种模式：

- **前缀补全**：`<|fim_prefix|>{prefix}<|fim_suffix|>`
- **中间填充（FIM）**：`<|fim_prefix|>{prefix}<|fim_suffix|>{suffix}<|fim_middle|>`

> **注意**：当前仅支持 `qwen-coder-turbo`，且**仅适用于中国内地（北京地域）**，需要使用北京地域 API Key。暂不支持仅给定后缀生成前缀。

关键参数：`prompt`（必选）、`max_tokens`、`temperature`、`top_p`、`stream`/`stream_options`、`stop`、`seed`、`presence_penalty`。详见 [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。

### 4. Vision（多模态 Chat）

复用 `/v1/chat/completions` 端点，`messages.content` 改为数组，含 `text` 与 `image_url` 两种 type。支持：

- 通义千问 VL：`qwen3-vl-plus`、`qwen3-vl-flash`、`qwen3-vl-235b-a22b-thinking/instruct`、`qwen3-vl-32b-instruct`、`qwen3-vl-30b/8b` 系列、`qwen-vl-max`、`qwen-vl-plus`
- QVQ 推理模型：`qvq-max`、`qvq-plus`（**仅支持[流式输出](../concepts/streaming.md)**）
- OCR 模型：`qwen-vl-ocr` 系列

调用示例与 LangChain（`langchain_openai`）集成方式见 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。

### 5. Embedding（`/v1/embeddings`）

支持 `text-embedding-v1/v2/v3/v4`，其中 v4（基于 Qwen3-Embedding，2048/1536/1024/768/512/256/128/64 多档维度可选）单行最长 8192 Token，覆盖 100+ 语种与多种编程语言。`text-embedding-v3` 与 `v4` 支持通过 `dimensions` 参数自定义输出维度。

> **注意**：多模态 Embedding（如 `qwen3-vl-embedding`、`tongyi-embedding-vision` 系列）**不支持** [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，需走 [多模态向量 API](https://help.aliyun.com/zh/model-studio/multimodal-embedding-api-reference)。

价格与详细参数见 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。

### 6. Files（`/v1/files`）

文件管理接口，通过 `purpose` 区分用途：

| purpose | 用途 | 支持格式 | 单文件上限 |
| --- | --- | --- | --- |
| `file-extract` | Qwen-Long / Qwen-Doc-Turbo 文档问答与数据提取 | TXT、DOCX、PDF、XLSX、EPUB、MOBI、MD、CSV、JSON；BMP、PNG、JPG、GIF、PDF 扫描件 | 150 MB |
| `batch` | Batch 任务输入文件 | JSONL | 500 MB |
| `fine-tune` | 模型调优数据集 | JSONL | 300 MB |

存储配额：最多 10000 个文件，总大小 100 GB，达到任一上限后新上传将失败，需先删除旧文件。完整接口（上传、查询、删除、内容下载）的 Python/Java/curl 示例见 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。

### 7. Batch Chat（同步等待）

`base_url` 切换到 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`，调用方式与实时接口一致，但请求会进入队列异步处理，连接保持到最终结果返回。默认等待 3600 秒，可自定义 60-3600 秒之间。**官网限时 5 折**。详细模型清单（含 `qwen3.7-max`、`deepseek-v3.2`、多模态等）与多语言示例见 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。

### 8. Batch File（文件输入异步）

通过上传 JSONL 文件批量提交请求，系统全部完成或达到最长等待时间后返回结果文件 ID，**费用为实时调用的 50%**。流程：

1. `client.files.create(file=..., purpose="batch")` 上传输入文件（文件 ID 可复用）
2. `client.batches.create(input_file_id=..., endpoint="/v1/chat/completions", completion_window="24h")` 创建任务
3. 轮询 `client.batches.retrieve(batch_id)`，直到 `status ∈ {completed, failed, expired, cancelled}`
4. 通过 `output_file_id` / `error_file_id` 下载结果

> **注意**：`endpoint` 必须与 JSONL 中每行的 `url` 保持一致：测试模型用 `/v1/chat/ds-test`，Embedding 用 `/v1/embeddings`，其余文本/多模态用 `/v1/chat/completions`。可先用 `batch-test-model` 跑通链路（≤1 MB、≤100 行、最多并发 2 个、不计费）。

支持模型详见 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。

### 9. Conversations（`/v1/conversations`）

跨设备 / 长时中断场景下管理会话状态的服务端 API，搭配 Responses API 自动注入历史上下文。提供 5 类操作：

| 操作 | 方法/路径 | 说明 |
| --- | --- | --- |
| 创建 | `POST /v1/conversations` | 可同时携带最多 20 条初始 `items` |
| 读取 | `GET /v1/conversations/{conversation_id}` | 返回 `id`、`metadata`、`created_at` |
| 更新 | `POST /v1/conversations/{conversation_id}` | 完全覆盖 `metadata` |
| 删除 | `DELETE /v1/conversations/{conversation_id}` | 会话被删，消息项保留 |
| 添加消息 | `POST /v1/conversations/{conversation_id}/items` | 支持 `system`/`developer`/`user`/`assistant` 角色 |

`metadata` 最多 16 对键值，key ≤ 64 字符，value ≤ 512 字符。详细示例见 [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。

## 关键参数与共性约束

- **思考模式**：`qwen3.7`、`qwen3.6`、`qwen3.5` 系列默认开启思考模式，会产生思考 Token 增加成本。建议显式设置 `enable_thinking`（`true`/`false`）。
- **Batch 顶层参数**：JSONL 请求体中 `enable_thinking` 必须放在 `body` 顶层（与 `model` 同级），**不能**放进 `extra_body`。
- **超长上下文**：Batch 场景下 `qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-plus/flash`、`qwen3.5-plus/flash` 单次请求最大支持 256K Token。
- **[流式输出](../concepts/streaming.md)**：通过 `stream=True` 启用；如需在末尾返回 Token 使用统计，加 `stream_options={"include_usage": true}`。
- **确定性输出**：传入相同 `seed` 并保持其他参数不变，模型尽量返回一致结果（取值范围 0 ~ 2³¹−1）。
- **采样控制**：`temperature` 与 `top_p` 二选一即可，无需同时设置。

## 框架集成

### LangChain（Python）

两种集成路径：

- **`langchain_openai.ChatOpenAI`**：走 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，**仅支持** OpenAI 兼容模式所列模型；`pip install langchain_openai` 后传入 `api_key`、`base_url`、`model` 即可。
- **`langchain_community.chat_models.tongyi.ChatTongyi`**：走 DashScope 原生接口，**支持百炼全部文本生成模型**（含部署后模型）；`pip install langchain-community dashscope`，通过 `dashscope_api_key` 鉴权，支持 `streaming=True`。

LangChain JavaScript 同时提供 `@langchain/openai` 的 `ChatOpenAI` 与 `@langchain/community` 的 `ChatAlibabaTongyi` 两种实现。完整示例见 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

### LangChain4j（Java）

通过 `dev.langchain4j:langchain4j-open-ai`（Plain Java / Spring Boot）接入 OpenAI 兼容模式。

> **注意**：LangChain4j 1.0.0-beta3 起需要 Java 17+，使用 Java 11 编译会报 `Unsupported class file major version 61`。

## 错误码与调试建议

- 所有兼容接口出错时返回标准 OpenAI 错误结构（`error.message` / `error.type` / `error.code`），常见如 `invalid_api_key`、超时等可对照 [百炼错误码文档](https://help.aliyun.com/zh/model-studio/error-code) 排查。
- 切换地域时 **API Key 必须同步更换**，否则会出现 401 / 鉴权类错误。
- 推荐通过环境变量 `DASHSCOPE_API_KEY` 注入凭证，避免硬编码导致泄露。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)




