# toolkits and [[frameworks|frameworks]]

阿里云百炼平台提供全面兼容 OpenAI 接口规范的 SDK 与 REST API，并深度集成 LangChain 等主流应用开发框架。开发者仅需切换基础端点与凭证，即可无缝迁移现有代码或构建包含多轮记忆、异步批处理、文件解析的智能体工作流。本文档汇总了平台支持的接口能力、核心参数、框架接入方法及运行约束。

## 支持的模型与功能

平台按能力划分为以下核心接口类别，具体可用模型清单请参考 [[模型总览]]：

| 接口类型 | 核心能力 | 典型应用场景 |
|:---|:---|:---|
| **Chat / Completions** | 标准文本生成、代码补全、指令跟随 | 对话机器人、代码辅助续写、内容生成 |
| **Responses** | 简化上下文管理（`previous_response_id`）、内置工具调用 | 智能体交互、复杂多步任务、无需手动维护 History |
| **Vision / OCR** | 图像/视频理解、多模态内容解析 | 视觉问答、票据/文档文字提取 [[视觉理解]] |
| **Embedding** | 文本向量化、多语种语义表示 | 检索增强生成(RAG)、聚类分析 [[文本向量]] |
| **Files & Conversations** | 文件上传存储（`file-extract`/`batch`）、跨设备会话状态管理 | 长文档问答、上下文隔离的多会话业务 |
| **Batch (同步/异步)** | 单请求长轮询同步返回、文件驱动异步批处理 | 离线数据标注、大规模模型评测 [[批量推理]] |

## 关键参数

配置模型调用时，以下参数为核心控制点：

- **基础连接**：`base_url`（按地域配置）、`api_key`、`model`
- **生成控制**：`temperature`、`top_p`（二者择一设置即可）、`max_tokens`、`stop`、`seed`
- **上下文管理**：
  - Chat 模式：需客户端完整拼装 `messages` 数组。
  - Responses 模式：传入上一响应的顶层 `id` 作为 `previous_response_id`，有效期为 7 天。
- **思考模式**：部分 Qwen3 系列默认开启深度思考。可通过 `enable_thinking` 参数显式控制（`true`/`false`）。开启后将产生额外思考 Token。
- **文件处理**：上传时需指定 `purpose`（`file-extract` 用于文档分析，`batch` 用于批量推理）。
- **[[streaming-output|流式输出]]**：`stream=true` 配合 `stream_options={"include_usage": true}` 可在末尾 chunk 返回 Token 统计。

## 使用方式

### OpenAI SDK / HTTP 调用
安装最新版 `openai` SDK 后，只需覆盖 `base_url` 与认证信息即可调用。各语言（Python/Node.js/Java/Go/C#）调用范式一致。
- SDK 基础端点：`https://dashscope.aliyuncs.com/compatible-mode/v1`（北京）
- 响应式 API 端点：`/compatible-mode/v1/responses`
- 详细接入指南见 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-[[frameworks|frameworks]]/compatibility-of-openai-with-dashscope.md)。

### 框架集成（LangChain）
支持通过两种路径在 LangChain 中接入百炼：
1. **OpenAI 兼容模式**：使用 `ChatOpenAI`，配置百炼 `base_url` 即可。仅支持 OpenAI 兼容清单内的模型。
2. **DashScope 原生模式**：使用 `ChatTongyi` / `ChatAlibabaTongyi`，支持百炼全量文本模型及私有化部署模型。
完整示例与依赖安装说明请参考 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-[[frameworks|frameworks]]/use-bailian-in-langchain.md)。

### Responses 与 Conversations 进阶调用
- **自动上下文关联**：调用 `client.responses.create()` 时传入 `previous_response_id` 可免维护历史数组。
- **会话持久化**：通过 `/conversations` 接口创建/检索/更新会话元数据，适用于跨终端断线续聊场景。
实现细节见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。

## 限制和注意事项

> **注意**：旧版接口路径（如 `https://cn-hongkong.dashscope.aliyuncs.com/compatible-mode/v1`、`/api/v2/apps/protocols/compatible-mode/v1/...`）已下线或即将停止维护。请统一迁移至新版 `{WorkspaceId}.地域.maas.aliyuncs.com` 或 `/compatible-mode/v1/` 标准路径。

> **注意**：Batch 接口存在两种形态，请勿混淆：
> 1. **Batch Chat（同步/长轮询）**：保持 HTTP 连接等待结果，默认超时 3600 秒，适用于单条耗时任务。
> 2. **Batch File（异步/文件输入）**：上传 JSONL 后异步执行，最长支持 24 小时窗口，完成后下载结果文件。
> 两者端点不同，后者需配合 `client.files.create(purpose="batch")` 使用。

- **资源配额**：百炼文件存储上限为 10,000 个文件 / 100 GB 总量。`file-extract` 单文件限 150 MB，Batch 输入限 500 MB。
- **API Key 隔离**：北京与新加坡/国际地域的 API Key 相互独立，切换 `base_url` 时必须同步替换对应 Key，否则触发鉴权失败。
- **计费提示**：思考模式（Thinking/Reasoning）输出的 Token 独立计费；Batch 异步任务费用为实时调用的 50%。
- **异常排查**：调用失败时响应体包含 `error.code` 与 `error.message`，完整映射关系请查阅 [[错误码排查]] 页面。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)

