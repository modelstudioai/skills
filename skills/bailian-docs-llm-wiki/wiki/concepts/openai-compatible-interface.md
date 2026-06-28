# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼提供的一组与 OpenAI 官方协议保持字段级一致的 API 入口，开发者无需改写业务逻辑，只需替换 `api_key`、`base_url`、`model` 三项即可将现有 OpenAI SDK 代码或第三方工具直接接入百炼模型服务。

## 覆盖的接口族

百炼兼容的 OpenAI 接口统一挂在 `compatible-mode/v1` 路径下，覆盖以下能力：

| 接口 | HTTP 路径 | 典型场景 |
| --- | --- | --- |
| Chat Completions | `POST /chat/completions` | 多轮对话、function call、[流式输出](streaming-output.md) |
| Responses | `POST /responses` | 智能体原生能力、内置工具、简化上下文 |
| Completions | `POST /completions` | 代码补全、文本续写（FIM） |
| Embeddings | `POST /embeddings` | 文本向量化 |
| Vision | 走 Chat Completions | 图像/视频理解 |
| File | `POST /files` 等 | 上传/查询/删除文件 |
| Batch | `POST /batches` | 异步批量推理，费用 50% |
| Batch Chat | `POST /chat/completions`（batch 域名） | 单请求同步批量，费用 50% |
| Conversations | `POST /conversations` | 跨设备会话状态管理 |

其中 Chat Completions 与 Responses 是最常用的两类：前者与 OpenAI 客户端库直接兼容，迁移成本最低；后者是前者的演进版本，内置联网搜索、网页抓取、代码解释器、文搜图、图搜图等工具，并支持通过 `previous_response_id` 自动关联上下文，无需手动维护消息历史。

## 在百炼各场景中的使用

- **文本生成模型调用**：Qwen 全系列（商业版、开源版）、Qwen-VL、Qwen-Coder、Qwen-Omni、Qwen-Math，以及 DeepSeek、Kimi、GLM、MiniMax 等第三方模型均可通过 Chat Completions 接口调用，API 格式一致。
- **专用模型调用**：意图理解 `tongyi-intent-detect-v3`、翻译 `qwen-mt-plus`、OCR `qwen3.5-ocr`、界面交互 `gui-plus` 等专用模型同样走 OpenAI 兼容接口（`qwen-deep-research` 例外，仅支持 Python DashScope SDK）。
- **客户端工具接入**：Claude Code、OpenCode、Codex、Qwen Code、Kilo CLI 等终端 AI 编程工具，以及各类桌面客户端、IDE 插件、低代码平台、HTTP 工具，均通过 OpenAI 兼容协议接入百炼。
- **套餐化接入**：按量计费、Coding Plan、[Token](token.md) Plan 团队版三种计费方案共用同一套兼容协议，仅 Base URL 与 [API Key](api-key.md) 来源不同。

## 关键参数与配置

接入时需替换的三项核心参数：

- **api_key**：替换为百炼 [API Key](api-key.md)，建议通过环境变量 `DASHSCOPE_API_KEY` 注入。不同地域、不同套餐（按量计费 / Coding Plan / [Token](token.md) Plan 团队版）的 [API Key](api-key.md) 互不通用，混用会报 `401 Incorrect API key provided` 或导致额度不抵扣。
- **base_url**：使用[业务空间](workspace.md)专属域名，格式为 `https://{WorkspaceId}.<region>.maas.aliyuncs.com/compatible-mode/v1`。`{WorkspaceId}` 为[业务空间](workspace.md) ID，可在百炼控制台「[业务空间](workspace.md)详情」页面查看。

各地域 base_url 速查：

| 地域 | base_url |
| --- | --- |
| 华北2（北京） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 日本（东京） | `https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1`（固定域名，不带 WorkspaceId） |

套餐专属 Base URL：

| 方案 | OpenAI 兼容 Base URL |
| --- | --- |
| Coding Plan | `https://coding.dashscope.aliyuncs.com/v1` |
| [Token](token.md) Plan 团队版 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |

- **model**：替换为百炼支持的模型名称，如 `qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash`、`deepseek-v4-pro`、`kimi-k2.7-code`、`glm-5.2` 等。美国（弗吉尼亚）地域使用带 `-us` 后缀的模型名（如 `qwen-plus-us`）可限定美国境内推理。

其他常用请求参数：`messages`（对话消息列表）、`stream`（是否[流式输出](streaming-output.md)，流式可在最后一行通过 `stream_options={"include_usage": True}` 获取 token 用量）、`temperature`、`tools`（function call）。专用模型还有各自专属参数，例如 Qwen-MT 通过 `extra_body.translation_options` 控制翻译行为，Qwen-OCR 的 `messages.content` 为多模态数组并支持 `min_pixels`/`max_pixels`，GUI-Plus 通过 `extra_body.vl_high_resolution_images` 与 `computer_use` 工具操控桌面。

## 限制与注意事项

- **功能完整度**：兼容接口为保证协议一致性，可能不暴露百炼原生的全部参数；如需最全的采样参数、插件或业务字段，建议改用 DashScope 原生接口。
- **工具能力差异**：联网搜索、代码解释器、网页内容提取等为 Responses 接口专属内置能力，Chat Completions 接口不内置这些工具，需自行通过 function call 协议接入。
- **对话历史管理**：仅 Responses 接口自动维护历史，迁移到 Chat Completions 等接口时需自行管理上下文长度与轮次，避免超出模型上下文窗口。
- **协议不支持**：Qwen-Audio 不支持 OpenAI 兼容协议，仅支持 DashScope 协议；`qwen-deep-research` 仅支持 Python DashScope SDK。
- **地域与套餐隔离**：各地域的 API Key、接入域名、模型列表相互独立，不能跨地域混用；三种计费方案的 API Key 与 Base URL 也不能混用。
- **路径迁移**：Responses API 的旧版路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 即将停止维护，请使用新版路径 `/compatible-mode/v1/responses`。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [get started with models](../guides/get-started-with-models.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [more models](../api/more-models.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [token plan guide](../guides/token-plan-guide.md)


