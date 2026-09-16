# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台提供的一组标准化 RESTful API，严格遵循 OpenAI 官方 API 协议规范（如 `/v1/chat/completions`、`/v1/embeddings`、`/v1/responses` 等路径），支持使用标准 OpenAI SDK（Python、Node.js 等）或通用 HTTP 客户端直接调用，无需修改业务代码即可将现有应用快速迁移到百炼模型服务。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移已有应用**：开发者可复用 OpenAI SDK（如 `openai==1.40.0+`）、LangChain、LlamaIndex 等主流框架，仅需替换 `base_url` 和 `api_key`，即可调用 Qwen、DeepSeek、GLM、Kimi 等数十种模型，零代码改造接入。
- **智能体（Agent）开发**：`/v1/responses` 接口专为 Agent 场景设计，原生支持内置工具链（`web_search`、`code_interpreter`、`web_crawler`、`knowledge_retrieval`），配合 `tool_choice` 和 `tools` 参数实现自动规划与执行，是构建生产级 AI 应用的首选协议。
- **多模态理解**：`/v1/chat/completions` 支持 Vision 模式，输入 `messages` 中嵌入 `image_url`（支持 HTTPS URL 或 data URI），兼容 `qwen3-vl-plus`、`QVQ`、`qwen3.5-omni` 等模型；注意 `Qwen-Audio` 不支持该协议，需使用 DashScope 原生接口。
- **向量化与文件处理**：`/v1/embeddings` 提供文本嵌入能力（如 `text-embedding-v4`）；`/v1/files` 支持文档上传与用途标记（`file-extract` 用于 RAG、`batch` 用于批量推理）；所有操作均复用同一套认证与域名体系。
- **应用级集成**：通过 OpenAI 兼容的 `responses` 接口调用已发布的智能体或工作流应用，支持 `memory_id`（[长期记忆](long-term-memory.md)）、`rag_options`（知识库检索）、`background=true`（异步任务）等高级参数，实现端到端 AI 应用编排。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 注意事项 |
|------|------|------|------|----------|
| `base_url` | string | ✅ | 业务空间专属域名，格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`。旧域名（如 `dashscope.aliyuncs.com`）已不推荐。 | `{WorkspaceId}` 和 `{region}`（如 `cn-beijing`）必须与 API Key 绑定地域一致；跨地域调用将返回 `invalid_api_key`。 |
| `api_key` | string | ✅ | 百炼平台颁发的 API Key，按方案隔离（Token Plan、Coding Plan、按量计费 Key 互不通用）。 | Token Plan Key 仅对 `token-plan.cn-beijing.maas.aliyuncs.com` 有效；按量计费 Key 必须与 `base_url` 中的 WorkspaceId 所属账号一致。 |
| `model` | string | ✅ | 模型标识符，必须与 [查询模型列表](/api/v1/models) 返回值完全一致（如 `qwen3.8-max`、`qwen-coder-turbo`、`text-embedding-v4`）。 | 不同接口支持模型不同：`completions` 仅支持 `qwen-coder-turbo`；`embeddings` 不支持稀疏向量；`responses` 是唯一完整支持 Agent 工具的接口。 |
| `messages` / `input` | array/string | ✅（依接口） | `chat/completions` 和 `responses` 使用 `messages` 数组（含 `role`/`content`/`image_url` 等）；`responses` 也接受字符串形式的 `input`。 | 多模态输入需按类型组织：`{"type": "text", "text": "..."}` 或 `{"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}`。 |
| `stream` | boolean | ❌（默认 `false`） | 启用流式响应（SSE 格式），适用于对话 UI、实时思考展示等场景。 | `responses` 异步模式（`background=true`）不支持 `stream=true`；`QVQ` 模型仅支持[流式输出](streaming-output.md)。 |
| `tools` + `tool_choice` | object/array | ❌（Agent 场景必填） | 定义可用工具（内置或自定义 function），`tool_choice` 控制调用策略（`"auto"`/`"required"`/`{"type": "function", "function": {"name": "xxx"}}`）。 | 仅 `responses` 接口完整支持百炼内置工具；`chat/completions` 仅支持基础 function calling，无联网搜索等增强能力。 |
| `extra_body` | object | ❌ | 传递百炼特有扩展参数，如 `{"enable_thinking": true, "has_thoughts": true}`（开启并返回思考过程）、`{"workspace": "sub-workspace-id"}`（调用子空间）。 | `enable_thinking` 必须与 `model` 同级传入，不可放在 `extra_body` 内部，否则无效。 |

> 💡 **提示**：所有 OpenAI 兼容接口均统一使用 `Authorization: Bearer <API_KEY>` 认证，无需额外 header；流式响应需正确处理 SSE 数据块（以 `data:` 开头，空行分隔）；错误响应结构与 OpenAI 一致（`{ "error": { "message": "...", "type": "..." } }`），便于统一错误处理。

---  
*最后更新：2024年10月*

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [application call](../api/application-call.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [more about models](../api/more-about-models.md)


