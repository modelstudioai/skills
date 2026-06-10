# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台为现有 OpenAI 生态应用提供的零改造迁移通道。开发者只需替换 `api_key`、`base_url` 和 `model` 三个参数，即可把基于 OpenAI SDK 编写的代码、接入的第三方工具（Cursor、Cherry Studio、Claude Code、LangChain 等）平滑切换到百炼所托管的千问（Qwen）系列及第三方模型。

## 核心接入模型

所有 OpenAI 兼容接口共享统一的接入三要素：

| 参数 | 说明 |
| --- | --- |
| `api_key` | 阿里云百炼 API Key，可在百炼控制台创建。**各地域的 Key 互不通用**，切换地域需同步更换。 |
| `base_url` | 兼容模式根路径，按地域不同取值（见下文"服务地址"）。 |
| `model` | 百炼模型名称，例如 `qwen-plus`、`qwen3.7-max`、`qwen3-vl-plus`、`text-embedding-v4` 等。 |

调用方式与 OpenAI 官方 SDK 完全一致：通过 `OpenAI(api_key=..., base_url=...)` 构造客户端后，即可使用熟悉的 `chat.completions.create(...)` 等方法。

## 支持的接口类型

百炼基于 OpenAI 协议对外暴露八类接口，覆盖从对话、推理到检索的完整能力：

| 接口 | 端点路径 | 适用场景 |
| --- | --- | --- |
| Chat Completions | `/v1/chat/completions` | 最通用的对话接口，覆盖千问商业版与开源版全系列模型。 |
| Responses | `/v1/responses` | Chat Completions 的演进版，内置联网搜索、代码解释器、网页抓取等工具，并通过 `previous_response_id` 自动关联上下文。 |
| Completions | `/v1/completions` | 文本/代码补全，支持前缀补全与中间填充（FIM）。当前仅 `qwen-coder-turbo` 在北京地域可用。 |
| Vision | `/v1/chat/completions` | 复用 Chat 端点，`messages.content` 以数组形式传入 `text` 与 `image_url`，支持多模态理解。 |
| Embedding | `/v1/embeddings` | 向量检索场景，支持 `text-embedding-v4` 等模型。 |
| Files | `/v1/files` | 文件上传与管理，用于 Batch 或 Assistants 类场景。 |
| Batch | `/compatible-mode/v1/batches` | 大批量异步推理，使用独立的 Batch 域名。 |
| Conversations | `/v1/conversations` | 长对话历史管理，由服务端维护会话状态。 |

> **说明**：Anthropic 兼容的 Messages 接口、以及百炼原生 DashScope 接口属于另外两类并行的调用方式，不在 OpenAI 兼容协议范围内。需要完整功能集（例如更多采样参数、特殊控制字段）时，应优先使用 DashScope 原生接口。

## 服务地址（base_url）

不同地域与用途对应不同的 `base_url`，调用前务必选对：

| 地域 / 用途 | base_url |
| --- | --- |
| 华北 2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |
| Token Plan 团队版 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| Batch（同步 / 文件输入，中国内地） | `https://batch.dashscope.aliyuncs.com/compatible-mode/v1` |

> **迁移提示**：新加坡地域旧版域名 `dashscope-intl.aliyuncs.com` 即将下线，应迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`；Responses / Conversations 的旧版路径 `/api/v2/apps/protocols/compatible-mode/v1/...` 也即将停止维护，应迁移到 `/compatible-mode/v1/...`。

## 典型使用场景

- **迁移已有 OpenAI 应用**：业务代码已经基于 `openai` Python/Node SDK 开发完成，只需替换三参数即可切换到千问模型，无需重写调用逻辑。
- **接入第三方客户端与 IDE 插件**：Cursor、Cherry Studio、Chatbox、Cline、Claude Code、Codex、Kilo CLI、Qwen Code 等工具均以 OpenAI 协议对接百炼，按工具文档填入 `base_url` 与 `api_key` 即可使用。
- **对接 LangChain / LangChain4j 等框架**：通过 `ChatOpenAI` 等标准组件传入百炼的 `base_url` 和 `api_key`，可直接把百炼模型接入 Agent、RAG、工作流编排等场景。
- **调用专用模型**：Qwen-MT（机器翻译）、Qwen-OCR（文字识别）、GUI-Plus（界面交互）等专用模型也通过 `/v1/chat/completions` 接入，借助 `extra_body` 传入领域专属字段（如翻译的 `translation_options`、OCR 的结构化抽取配置）。
- **构建多地域合规部署**：数据不出中国内地选北京地域；数据不经过中国内地选新加坡或德国地域；全球资源池可选美国（弗吉尼亚）或德国地域。同一套代码仅切换 `base_url` 与 `api_key` 即可完成地域迁移。

## 关键参数与配置

- **认证**：推荐将 API Key 写入环境变量 `DASHSCOPE_API_KEY`，避免在代码中硬编码。SDK 初始化时通过 `api_key=os.getenv("DASHSCOPE_API_KEY")` 读取。
- **地域一致性**：`api_key`、`base_url`、HTTP Endpoint 三者必须属于同一地域，混用会返回鉴权或路由错误。
- **Responses 上下文管理**：Responses 接口通过响应顶层的 `id`（UUID）与请求中的 `previous_response_id` 自动串联多轮对话，有效期 7 天，无需手动维护 `messages` 历史。
- **Completions 模式**：`/v1/completions` 支持前缀补全与 FIM（`<|fim_prefix|>{prefix}<|fim_middle|>{suffix}<|fim_middle|>`），但仅 `qwen-coder-turbo` 模型可用，且仅限北京地域。
- **[流式输出](streaming-output.md)**：所有对话类接口均支持 `stream=True`，通过 SSE 返回增量 token，专用模型（MT、OCR、GUI-Plus）同样适用。
- **参数覆盖差异**：OpenAI 兼容接口覆盖大部分常用参数（`temperature`、`top_p`、`max_tokens`、`stop`、`seed`、`presence_penalty` 等），但功能最完整的是 DashScope 原生接口；某些百炼专有参数（例如 Qwen-MT 的 `translation_options`）需放在 `extra_body` 中传入。

## 与其他接口的关系

百炼同时提供 Anthropic 兼容 Messages 接口与 DashScope 原生接口。选型建议：

- 已有 OpenAI 代码或接入 OpenAI 生态工具 → 优先 OpenAI 兼容接口，改动最小。
- 需要自动管理对话历史且使用内置工具（联网、代码解释器） → 选 OpenAI 兼容 Responses 接口。
- 使用 Anthropic 生态（Claude Code、OpenCode、Hermes Agent 等）→ 选 Anthropic 兼容 Messages 接口。
- 需要完整参数集、或调用 OpenAI 协议尚未覆盖的百炼专有功能（例如 Qwen-Deep-Research）→ 选 DashScope 原生接口。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [get started with models](../guides/get-started-with-models.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [specialized model](../api/specialized-model.md)


