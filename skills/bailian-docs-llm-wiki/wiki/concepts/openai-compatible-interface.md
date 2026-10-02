# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台提供的一套标准化 RESTful API 协议，完全遵循 OpenAI 官方 API 的路径、请求/响应结构、参数命名与语义规范（如 `/chat/completions`、`/embeddings`、`/responses` 等），使开发者能直接复用 OpenAI SDK（Python/Node.js/Java 等）、主流 AI 工具链（Cursor、Dify、Postman）及现有代码逻辑，无需修改业务逻辑即可调用百炼托管的千问（Qwen）全系列模型及第三方直供模型。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速接入与迁移**：开发者只需将原有 OpenAI 调用中的 `base_url` 替换为百炼地域专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），并配置百炼颁发的 `api_key`，即可零改造调用 `qwen3.7-plus`、`qwen3.8-max`、`qwen3-vl-plus`、`text-embedding-v4`、`qwen3-rerank` 等全部支持模型，适用于文本生成、多模态理解、向量嵌入、重排序等任务。
  
- **多工具协同开发**：支持 CLI（Qwen Code、Kilo CLI）、IDE [插件](plugin.md)（Cline、Qoder）、桌面客户端（Cherry Studio）、低代码平台（Dify）等工具直接对接。例如在 Dify 中配置 OpenAI 兼容 Provider 时，填入百炼 Base URL 和 Key，即可将 `qwen3.7-plus` 作为 LLM 节点；在 Cursor 中切换模型 ID 即可启用 Qwen-VL 视觉能力（需工具本身支持图像输入）。

- **统一协议下的能力分层**：同一兼容协议下，不同端点承载差异化能力：
  - `/chat/completions`：标准对话生成，支持 `messages` 数组（含 `text`/`image_url`/`video_url`）、系统提示、[流式输出](streaming-output.md)；
  - `/embeddings`：同步文本向量化，兼容 `input` 字符串或数组，支持 `dimensions` 参数（部分模型）；
  - `/rerank`：文本重排序，`qwen3-rerank` 模型采用扁平化参数结构（`query` + `documents` 同级）；
  - `/responses`：增强型智能响应，内置工具链（联网搜索、网页抓取、代码解释器等），支持 `reasoning.effort` 控制思考深度；
  - `/completions`：专用于代码补全（FIM），仅限 `qwen-coder-turbo`；
  - `/conversations`：会话上下文持久化，实现跨请求历史自动注入。

- **生产环境适配**：支持按量付费、[Token](token.md) Plan、Coding Plan 三类计费方案，每类对应独立的 Base URL 和 API Key 绑定策略；业务空间专属域名保障隔离性与性能，旧域名（如 `dashscope.aliyuncs.com`）已不推荐使用。

> ⚠️ 注意：并非所有百炼模型均支持 OpenAI 兼容协议。`Qwen-Audio` 明确不支持，必须使用 DashScope 原生协议；部分视频模型（如需自定义 `max_frames`）或高级音频能力也仅限原生接口。

## 关键参数和配置

| 参数 | 必填 | 说明 | 示例值 |
|------|------|------|--------|
| `base_url` | ✅ | 必须匹配地域、计费方案与业务空间。格式固定为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`。北京地域示例：`https://abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://myws.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `api_key` | ✅ | 百炼控制台创建的密钥，**严格绑定地域与计费方案**。北京 [Token](token.md) Plan 的 Key 不能用于新加坡按量付费域名。 | `sk-xxx` |
| `model` | ✅ | 百炼官方支持的模型 ID，大小写敏感，不可拼错。第三方模型需使用完整命名（如 `kimi/kimi-k3`）。 | `"qwen3.7-plus"`, `"text-embedding-v4"`, `"qwen3-rerank"` |
| `stream` | ❌（可选） | 启用流式响应，设为 `true`。配合 `stream_options={"include_usage": true}` 可在末尾 chunk 返回 token 统计。 | `true` |
| `dimensions` | ❌（按模型支持） | 仅 `text-embedding-v4`、`qwen3.7-text-embedding`、`qwen3-vl-embedding` 等明确文档支持的模型可用，值必须为文档列出的合法维度（如 `2560`, `1024`, `768`）。 | `1024` |
| `enable_thinking` | ❌（按模型默认） | 对 `qwen3.5+` 系列模型，默认开启深度思考。显式传 `false` 可关闭以降低成本（适用于简单任务）。 | `false` |
| `reasoning.effort` | ❌（仅 `/responses`） | 控制推理强度，取值 `"low"` / `"medium"` / `"xhigh"`，影响响应质量与延迟。 | `"xhigh"` |

> 💡 提示：`system` 提示需置于 `messages[0]`；图像输入使用 `{"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}` 格式；`encoding_format=base64` 在同步 Embedding 接口中**实际不可靠**，建议使用默认 `float`。

## 面向开发者，简洁实用

- ✅ **即刻上手**：复制粘贴 OpenAI SDK 示例代码，仅改两行——`base_url` 和 `model`，5 分钟完成接入。
- ✅ **无缝迁移**：已有 OpenAI 项目（如 LangChain、LlamaIndex 应用）无需重构，通过环境变量 `OPENAI_BASE_URL` 和 `OPENAI_API_KEY` 即可切换至百炼。
- ✅ **按需选型**：  
  - 要通用对话 → 用 `/chat/completions` + `qwen3.7-plus`；  
  - 要带工具的智能体 → 用 `/responses` + `qwen3.8-max`；  
  - 要 RAG 向量库 → 用 `/embeddings` + `text-embedding-v4`；  
  - 要搜索结果精排 → 用 `/rerank` + `qwen3-rerank`。
- ❌ **避坑提醒**：  
  - 不要混用 Key 与 Base URL 的计费方案（如 [Token](token.md) Plan Key + Coding Plan URL）；  
  - 不要对 `Qwen-Audio` 使用 OpenAI 接口（会返回 404 或不支持错误）；  
  - 不要硬编码 `base_url`，务必从控制台获取真实 `WorkspaceId` 并动态注入。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [vector and sort](../api/vector-and-sort.md)


