# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 API 协议层，严格遵循 OpenAI REST API 的路径、请求/响应结构、参数命名与语义规范（如 `/v1/chat/completions`），使开发者无需修改业务逻辑即可复用现有 OpenAI 生态工具链（如 `openai` SDK、LangChain、LlamaIndex、Dify 等）调用百炼托管的 Qwen 系列及第三方大模型。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型推理**：作为最常用的接入方式，支持 `chat/completions`（多轮对话）、`embeddings`（向量生成）、`completions`（单轮文本补全，当前仅限 `qwen-coder-turbo`）等核心端点，覆盖文本、视觉（VL 模型）、嵌入、长文档理解等能力。
- **智能体与工作流集成**：通过 OpenAI 兼容的 `Responses API`（`/v1/responses`）调用已发布的智能体应用，支持内置工具（`web_search`, `code_interpreter`）、上下文自动注入（`previous_response_id`）和异步任务（`background=true`）。
- **开发框架对接**：为 LlamaIndex、Spring AI Alibaba 等主流框架提供开箱即用的适配器（如 `BaiLianLLM`），只需配置 `base_url` 和 `model` 即可替代原生 OpenAI 客户端。
- **终端与 IDE 工具接入**：支持 Cursor、Cherry Studio、Qoder、Hermes Agent 等桌面/IDE 工具，开发者仅需替换 `base_url` 和 `api_key`，即可在不修改插件配置的前提下切换至百炼服务。
- **批量与生产部署**：配合 `enable_thinking`（启用深度思考）、`stream_options.include_usage`（流式返回 token 统计）等参数，满足高并发、可观测、可计费的生产级需求。

> ⚠️ 注意：`Qwen-Audio` 模型**不支持** OpenAI 兼容协议，必须使用 DashScope 原生接口；`QVQ` 和 `QwQ` 模型的 `system` 消息无效，`qwen3.5-audio` 仅 DashScope 原生可用。

## 关键参数和配置

| 参数 | 类型 | 是否必填 | 说明 | 示例值 |
|------|------|----------|------|--------|
| `base_url` | string | 是 | 服务端点，**必须匹配 API Key 所在地域与套餐类型**。推荐使用业务空间专属域名（性能更优）。格式：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1` | `https://my-workspace.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `model` | string | 是 | 模型 ID，大小写敏感，须严格匹配所选套餐支持列表（如 [Token](token.md) Plan 个人版不支持 `qwen3-vl-plus`） | `"qwen3.8-max"`, `"qwen3-vl-plus"`, `"text-embedding-v4"` |
| `messages` | array | 是（`chat/completions`） | 标准 OpenAI 消息数组，`content` 支持 `text`、`image_url`（含 `url`/`detail`）、`video_url` 等结构化输入 | `[{"role":"user","content":[{"type":"text","text":"描述这张图"},{"type":"image_url","image_url":{"url":"https://..."}}]}]` |
| `stream` | boolean | 否 | 启用流式响应（SSE），默认 `false` | `true` |
| `stream_options` | object | 否 | 流式增强选项，设 `{"include_usage": true}` 可在末尾 chunk 获取 `usage` 字段 | `{"include_usage": true}` |
| `enable_thinking` | boolean | 否 | 对 `qwen3` 系列思考模型（如 `qwen3.8-max`）为必填项，否则报错；部分工具需显式开启 | `true` |
| `dimensions` | integer | 否（仅 embedding） | 指定向量维度（仅 `text-embedding-v3/v4` 支持） | `1024` |

- **认证方式**：通过 HTTP Header `Authorization: Bearer {DASHSCOPE_API_KEY}` 传递；
- **地域绑定**：API Key 与 `base_url` 中的地域（如 `cn-beijing`）必须一致，否则返回 `401 Unauthorized`；
- **Workspace ID**：仅按量计费需手动替换 `{WorkspaceId}` 占位符；[Token](token.md) Plan / Coding Plan 使用预置域名（如 `token-plan.cn-beijing.maas.aliyuncs.com`）。

## 面向开发者，简洁实用

- ✅ **快速迁移**：将原有 OpenAI 代码中的 `client = OpenAI(api_key="sk-...")` 替换为：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://my-workspace.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  ```
- ✅ **即用即查**：所有兼容接口均返回标准 OpenAI JSON Schema（含 `id`, `choices[0].message`, `usage`），错误码统一为 `4xx/5xx` + `error.message/code`；
- ✅ **调试友好**：支持 Postman/curl 直接测试（注意设置 `Content-Type: application/json` 和 `Authorization` Header）；
- ❌ **避免踩坑**：
  - 不要混用协议参数（如在 `/chat/completions` 中传 `max_tokens` —— 该参数不被支持）；
  - 不要对 `QVQ` 模型设置 `system` 消息；
  - 不要用 [Token](token.md) Plan 的 Key 调用 Dify/Postman —— 属于违规，可能导致 Key 封禁。

如需完整参数约束、模型支持列表或多模态输入规范，请参考 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 文档。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [application call](../api/application-call.md)
- [frameworks](../api/frameworks.md)


