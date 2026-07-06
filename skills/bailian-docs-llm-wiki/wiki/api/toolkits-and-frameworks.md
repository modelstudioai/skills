# toolkits and [frameworks](frameworks.md)

阿里云百炼提供与 OpenAI 协议兼容的接口族（Chat、Responses、Completions、Embedding、Vision、File、Batch、Conversations）以及 LangChain/LangChain4j 框架适配，开发者通常只需调整 `api_key`、`base_url`、`model` 三个参数即可复用现有 OpenAI 代码或生态工具。本文汇总各兼容接口的接入要点、支持的模型范围与使用限制。

## 统一接入信息

无论使用哪种兼容接口，迁移到百炼时都需要替换以下三项：

- **api_key**：替换为阿里云百炼 [API Key](../concepts/api-key.md)，建议通过环境变量 `DASHSCOPE_API_KEY` 注入以降低泄露风险。新加坡和北京地域的 [API Key](../concepts/api-key.md) 不同，切换地域时需同步更换。
- **base_url**：使用[业务空间](../concepts/workspace.md)专属域名，格式为 `https://{WorkspaceId}.<region>.maas.aliyuncs.com/compatible-mode/v1`。`{WorkspaceId}` 为[业务空间](../concepts/workspace.md) ID，可在百炼控制台「[业务空间](../concepts/workspace.md)详情」页面查看。
- **model**：替换为下文各接口支持的模型名称清单中的值。

百炼为华北2（北京）、新加坡地域推出了[业务空间](../concepts/workspace.md)专属域名，建议从旧域名 `https://dashscope.aliyuncs.com`（北京）和 `https://dashscope-intl.aliyuncs.com`（新加坡）迁移至新域名，以获得更好的推理性能与稳定性。现有旧域名仍可正常使用，详情参见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。

各地域 base_url 速查：

| 地域 | base_url（SDK 配置） |
| --- | --- |
| 华北2（北京） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 日本（东京） | `https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1`（Responses 接口） |

> **注意**：弗吉尼亚地域使用固定域名 `dashscope-us.aliyuncs.com`，不带 `{WorkspaceId}`；其余地域均需替换为真实[业务空间](../concepts/workspace.md) ID。

## 兼容接口一览

百炼兼容的 OpenAI 接口覆盖以下能力，调用路径均为 `compatible-mode/v1` 下的标准 OpenAI 路径：

| 接口 | HTTP 路径 | 典型场景 |
| --- | --- | --- |
| Chat Completions | `POST /chat/completions` | 多轮对话、function call、[流式输出](../concepts/streaming-output.md) |
| Responses | `POST /responses` | 智能体原生能力、内置工具、简化上下文 |
| Completions | `POST /completions` | 代码补全、文本续写（FIM） |
| Embeddings | `POST /embeddings` | 文本向量化 |
| Vision | 走 Chat Completions | 图像/视频理解 |
| File | `POST /files` 等 | 上传/查询/删除文件 |
| Batch（文件） | `POST /batches` | 异步批量推理，费用 50% |
| Batch Chat | `POST /chat/completions`（batch 域名） | 单请求同步批量，费用 50% |
| Conversations | `POST /conversations` | 跨设备会话状态管理 |

## Chat Completions 接口

支持模型：Qwen 大语言模型（商业版、开源版）、Qwen-VL、Qwen-Coder、Qwen-Omni、Qwen-Math、DeepSeek（阿里云直供、硅基流动直供、快手万擎直供）、Kimi（阿里云直供、月之暗面直供）、GLM（阿里云直供）、MiniMax（阿里云直供、稀宇科技直供）。

> 三方直供模型仅在中国站的中国内地地域可用，调用前需先在百炼控制台开通对应服务。
> Qwen-Audio 不支持 OpenAI 兼容协议，仅支持 DashScope 协议。

非流式与流式调用示例及 function call 的完整流程参见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。[流式输出](../concepts/streaming-output.md)可在最后一行通过 `stream_options={"include_usage": True}` 获取 token 用量。

## Responses 接口

作为 Chat Completions 的演进版本，提供智能体原生能力：内置联网搜索、网页抓取、代码解释器、文搜图、图搜图等工具；支持直接传入字符串或 Chat 格式消息数组；通过 `previous_response_id` 关联上一轮上下文，无需手动维护消息历史。

支持模型包括 `qwen3-max`、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.5-plus`、`qwen3.6-flash`、`qwen3.5-flash`、`qwen-plus`、`qwen-flash`、`qwen3-coder-plus` 等系列（含历史日期版本号）。

> **注意**：Responses API 的旧版路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 即将停止维护，请使用新版路径 `/compatible-mode/v1/responses`。
> `previous_response_id` 应传入上一轮响应的顶层 `id`（UUID 格式），而非 `output` 数组内消息的 `id`；当前响应 id 有效期为 7 天。

多轮对话与基础调用示例参见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。

## Completions 接口

专为文本补全场景设计，适合代码补全与内容续写。**仅适用于中国内地（北京地域）**，需使用北京地域 [API Key](../concepts/api-key.md)。

支持模型：`qwen-coder-turbo`。

两种补全模式：

- 前缀生成后续：提示词模板 `<|fim_prefix|>{prefix_content}<|fim_suffix|>`
- 前缀+后缀生成中间内容：提示词模板 `<|fim_prefix|>{prefix_content}<|fim_suffix|>{suffix_content}<|fim_middle|}`

> 暂不支持通过给定后缀生成前缀内容。
> `max_tokens` 仅截断返回内容，不影响模型生成过程；`temperature` 取值范围 [0, 2.0)，`top_p` 取值范围 (0, 1.0]，二者建议只设置其一。

参数表与输出字段定义参见 [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)。

## Vision 接口

通义千问视觉模型兼容 OpenAI 接口规范，调用走标准 Chat Completions 路径，通过 `content` 数组传入 `text` 与 `image_url` 项。

支持模型：Qwen-VL、QVQ、Qwen-OCR。各地域支持的模型有差异，以百炼控制台模型市场为准。

> QVQ 模型仅支持[流式输出](../concepts/streaming-output.md)。

可通过 OpenAI SDK 或 `langchain_openai` SDK 调用，`langchain_openai` 使用 `invoke` 方法实现非[流式输出](../concepts/streaming-output.md)。详情参见 [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)。

## Embedding 接口

支持模型：`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1`。

- `text-embedding-v4` 属于 Qwen3-Embedding 系列，支持 2,048/1,536/1,024（默认）/768/512/256/128/64 维度，单行最大 8,192 token，最大 10 行，支持 100+ 语种。
- `text-embedding-v3` 支持 1,024（默认）/768/512/256/128/64 维度，50+ 语种。
- `text-embedding-v2` 固定 1,536 维，最大 25 行，单行 2,048 token。

> [多模态](../concepts/multimodal.md) Embedding 模型（如 `qwen3-vl-embedding`、`tongyi-embedding-vision` 系列）不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)。
> `dimensions` 参数仅 `text-embedding-v3` 及 `text-embedding-v4` 支持。

各模型享有百炼开通后 90 天内的免费 token 额度，Batch 调用价格约为实时调用的 50%。调用示例与异常响应参见 [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)。

## 文件接口

文件上传接口用于在 Qwen-Long、Qwen-Doc-Turbo 中进行文档问答与数据提取，或作为批量推理、[模型调优](../concepts/fine-tuning.md)任务的输入文件。支持上传、查询、删除操作，可通过 OpenAI SDK（Python、Java）或 HTTP API 调用。

存储配额：最大文件数 10,000 个，总大小 100 GB，无有效期限制。达到上限时新上传会失败，需删除旧文件释放配额。

`purpose` 取值与场景：

| purpose | 用途 | 格式与大小限制 |
| --- | --- | --- |
| `file-extract` | 文档分析（Qwen-Long / Qwen-Doc-Turbo） | TXT/DOCX/PDF/XLSX/EPUB/MOBI/MD/CSV/JSON 及图片，单文件 ≤ 150 MB |
| `batch` | 批量推理输入 | jsonl，单文件 ≤ 500 MB |
| `fine-tune` | [模型调优](../concepts/fine-tuning.md)数据集/训练集 | jsonl，单文件 ≤ 300 MB |

详情参见 [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。

## Batch 批量推理

### 文件输入（异步）

通过文件批量提交请求，系统异步处理，全部完成或达到最长等待时间后返回结果，费用为实时调用的 50%。适用于数据分析、模型[评测](../concepts/evaluation.md)等时效性要求不高但需大批量处理的场景。

服务端点：中国内地 `https://dashscope.aliyuncs.com/compatible-mode/v1`；国际（新加坡）`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`。

北京地域支持文本生成模型（千问 Max/Plus/Flash/Long 稳定版本及部分 `latest` 版本，deepseek-r1、deepseek-v3.2、deepseek-v3）、[多模态](../concepts/multimodal.md)模型（千问 VL Plus/Flash/OCR）、文本向量模型（text-embedding-v1~v4）。新加坡地域支持 qwen-max、qwen-plus、qwen-turbo。

[工作流](../concepts/workflow.md)程：准备 jsonl 输入文件 → 上传得到 file_id → 创建 Batch 任务得到 batch_id → 轮询状态 → 下载输出/错误文件。文件上传返回的 file_id 可重复使用，输入内容不变时无需重新上传。

> 在 Batch 场景下，`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.6-flash`、`qwen3.5-plus`、`qwen3.5-flash` 单次请求上下文 [Token](../concepts/token.md) 数最大支持 256K。
> `qwen3.7`、`qwen3.6`、`qwen3.5` 系列默认开启思考模式，会产生思考 tokens 增加成本，建议显式设置 `enable_thinking`（`true`/`false`）。
> `enable_thinking` 为 JSONL `body` 的顶层参数，须与 `model` 同级传入，不能放在 `extra_body` 中。

测试模型 `batch-test-model` 跳过推理直接返回固定成功响应，用于全链路闭环验证；测试文件 ≤ 1 MB、≤ 100 行，最大并行任务 2 个，不产生推理费用。`endpoint` 参数须与输入文件中 `url` 字段一致：测试模型填 `/v1/chat/ds-test`，Embedding 填 `/v1/embeddings`，其他填 `/v1/chat/completions`。

完整流程代码参见 [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。

### Batch Chat（同步单请求）

保持与实时 API 一致的同步调用方式，客户端发起请求并保持连接等待，处理完成后通过同一连接一次性返回结果，费用为实时推理的 50%。仅支持提交单个请求，多请求需走文件方式。

端点：SDK `base_url` 为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`，HTTP 为 `POST https://batch.dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`。

北京地域支持文本生成模型（qwen3.7-max/plus、qwen3.6-plus/flash、qwen3.5-plus/flash、qwen3-max、qwen-plus、qwen-flash、deepseek-v3.2）及图像与视频理解模型（qwen3.7-plus、qwen3.6-plus/flash、qwen3.5-plus/flash、qwen3-vl-plus/flash）。

默认等待超时 3600 秒（1 小时），可自定义 60–3600 秒。支持 Python、Java、Node.js、Go、C#。详情参见 [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)。

## Conversations 接口

配合 Responses API 自动注入历史上下文，无需手动同步消息，实现跨设备、长时间中断的对话延续。提供 create/retrieve/update/delete conversation 及 items 增删等操作。

- Create：`POST /conversations`，可同时添加最多 20 条初始消息项；`metadata` 最多 16 对键值对，key ≤ 64 字符，value ≤ 512 字符。
- Update：`POST /conversations/{conversation_id}`，`metadata` 会完全覆盖原有元数据。
- Delete：`DELETE /conversations/{conversation_id}`，仅删除会话本身，会话中的消息项不会被删除。
- Create Items：`POST /conversations/{conversation_id}/items`，向会话添加消息项。

> **注意**：旧版 URL 路径 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 即将停止维护，请使用新版路径 `/compatible-mode/v1/conversations`。

支持 Python、Node.js、cURL，详情参见 [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)。

## 在 LangChain 中使用

百炼可通过 LangChain 生态接入，提供两种 Chat Model 实现：

- **OpenAI 兼容（ChatOpenAI）**：只支持百炼的部分模型，base_url 指向 `https://dashscope.aliyuncs.com/compatible-mode/v1`。
- **DashScope 原生（ChatTongyi / ChatAlibabaTongyi）**：支持百炼所有文本生成模型（含部署后的模型），需安装 `langchain-community` 与 `dashscope`。

| 语言 | OpenAI 兼容依赖 | DashScope 原生依赖 |
| --- | --- | --- |
| Python | `pip install langchain_openai` | `pip install langchain-community dashscope` |
| JavaScript | `npm install @langchain/openai @langchain/core` | `npm install @langchain/community @langchain/core` |
| Java | `langchain4j-open-ai` 1.0.0-beta3 | （LangChain4j） |

> LangChain4j 1.0.0-beta3 需要 Java 17 及以上版本，使用 Java 11 会报 `Unsupported class file major version 61` 错误。Java 端支持 Plain Java 与 Spring Boot 两种实现方式。

各语言的模型调用、工具调用等进阶用法参见 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)。

## 限制与注意事项

- **地域与模型差异**：各地域支持的模型范围不同，以百炼控制台模型市场为准；三方直供模型仅中国内地可用，调用前需在控制台开通。
- **域名迁移**：北京、新加坡地域建议迁移至[业务空间](../concepts/workspace.md)专属域名以提升性能与稳定性，旧域名仍可用但弗吉尼亚等地域使用固定域名。
- **Batch 思考模式**：qwen3.7/3.6/3.5 系列默认开启思考模式会增加成本，须显式设置 `enable_thinking` 且为 body 顶层参数。
- **超时控制**：Batch Chat 同步连接最长 3600 秒，超时自动断开返回错误。
- **Completions 地域**：Completions 接口仅适用于中国内地（北京），需北京地域 [API Key](../concepts/api-key.md)。
- **[多模态](../concepts/multimodal.md) Embedding**：`qwen3-vl-embedding`、`tongyi-embedding-vision` 等[多模态](../concepts/multimodal.md)向量模型不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，需走[多模态](../concepts/multimodal.md)向量接口。
- **[API Key](../concepts/api-key.md) 安全**：推荐通过环境变量 `DASHSCOPE_API_KEY` 注入，避免在代码中硬编码。
- **模型调用失败**：如返回报错信息，参见百炼错误码文档排查。

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











