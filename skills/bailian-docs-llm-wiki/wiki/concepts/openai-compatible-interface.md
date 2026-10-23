# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台提供的一组标准化 REST API，严格遵循 OpenAI 的协议规范（如 `/v1/chat/completions`、`/v1/embeddings`、`/v1/responses` 等路径及请求/响应格式），使开发者无需修改业务逻辑即可复用 OpenAI SDK、LangChain、LlamaIndex 等生态工具，快速接入千问（Qwen）系列及第三方大模型能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **通用对话与原型验证**：使用 `Chat Completions` 接口（`POST /v1/chat/completions`）进行标准多轮对话，兼容主流聊天客户端（如 Cursor、Dify、Cherry Studio）和 IDE 插件，仅需配置 `base_url` 和 `api_key` 即可运行。
- **智能体（Agent）开发**：优先选用 `Responses API`（`POST /v1/responses`），它在 OpenAI 语义基础上扩展了 `previous_response_id`（自动上下文拼接）、`store`（响应持久化）、内置工具调用（`web_search`、`code_interpreter`）等关键能力，专为复杂 Agent 场景设计。
- **[向量嵌入](embedding.md)与排序**：通过标准 `/v1/embeddings` 和 `/v1/rerank` 接口调用 `text-embedding-v4`、`rerank-v3` 等模型，支持批量文本向量化、跨模态嵌入及检索结果重排序，完全兼容 OpenAI Embedding SDK 行为。
- **应用集成与低代码编排**：在 Dify、Hermes Agent 等工作流平台中，将百炼的 OpenAI 兼容 Endpoint 作为后端模型服务配置，直接复用 `function_call`、`tool_choice` 等字段实现插件调度与状态管理。
- **跨框架迁移**：使用 LangChain 的 `ChatOpenAI` 或 `OpenAIEmbeddings` 类时，只需替换 `openai_api_base` 为百炼专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），即可零代码迁移现有项目。

## 关键参数和配置

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `base_url` | 必填。必须为业务空间专属域名 + `/compatible-mode/v1` 路径，例如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`。不可使用通用 `dashscope.aliyuncs.com`。 | 域名中的 `{WorkspaceId}` 需从控制台获取；地域需与模型部署地一致（如华北2）。 |
| `model` | 必填。模型名称须严格匹配支持列表，如 `qwen3.8-max`、`text-embedding-v4`、`rerank-v3`。三方模型（如 `deepseek-v4.*`）仅限华北2地域且需控制台开通。 | `qwen3.8-omni-flash` 是唯一明确支持音视频输入的模型（通过 `input_audio`/`input_video` 字段）；`Qwen-Audio` 不支持 OpenAI 协议。 |
| `input`（Responses） / `messages`（Chat & Embedding） | 输入内容载体。Responses 支持字符串或 `messages` 数组；Chat 和 Embedding 强制数组格式；Embedding 的 `input` 可为字符串或字符串数组。 | `system` 消息在 Chat 接口中仅支持首条 `messages[0]`；部分客户端（如 Codex）会忽略 `role: system`，建议改用用户消息前置说明。 |
| `previous_response_id` | 仅 Responses API 支持。传入上一轮响应的 `id`（UUID），服务端自动加载历史上下文并拼接。不能与 `conversation` 或自定义 `messages` 同时使用。 | 配合 `store: true`（默认）生效；设为 `false` 时该参数无效。 |
| `stream` | 全协议支持。设为 `true` 启用 SSE 流式响应。Responses 的 delta 字段为 `response.output_text.delta`；Chat/Embedding 使用标准 `data: {...}` 格式。 | 工具需支持解析 `text/event-stream`；不支持的工具（如旧版 Codex）将静默丢弃中间 chunk。 |
| `tools` | Responses 和 Anthropic 协议支持。Responses 中可声明内置工具（`web_search`, `code_interpreter`）或自定义 function；Chat Completions 也支持 `function_call` 协议，但返回结构略有差异。 | Responses 的工具调用响应含 `tool_calls` 和 `tool_results` 字段，便于 Agent 自动执行。 |
| `stream_options={"include_usage": true}` | 流式响应末尾追加 token 统计（`usage` 字段），便于监控与计费。 | 仅 Responses 和 Chat API 支持；Embedding 和 Rerank 接口不支持。 |

## 面向开发者，简洁实用

- ✅ **快速上手**：用官方 OpenAI SDK（Python/Node.js/Java/Go/C#）一行代码切换：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  # 所有标准方法均可直接调用
  client.chat.completions.create(model="qwen3.8-max", messages=[{"role":"user","content":"你好"}])
  client.embeddings.create(model="text-embedding-v4", input=["hello world"])
  client.responses.create(model="qwen3.8-max", input="搜索最新AI论文")
  ```

- ✅ **避坑提示**：
  - 不要混用协议：`responses.create()` 与 `chat.completions.create()` 的输入结构、工具字段、上下文管理机制完全不同，按场景选型；
  - 多模态输入请优先使用 Responses API，并确认模型支持（仅 `qwen3.8-omni-flash` 明确支持音视频）；
  - `system` 消息在多数客户端中不可靠，生产环境建议将系统指令写入首条 `user` 消息；
  - 流式响应务必检查工具是否支持 `text/event-stream` 解析，否则无法获取实时输出；
  - 所有请求受 `input_tokens + output_tokens ≤ 32768` 限制（具体依模型而异），超长文本需预处理分块。

- ✅ **调试建议**：
  - 使用 Postman 或 curl 直连测试，确保 `base_url` 路径含 `/compatible-mode/v1`；
  - 查看响应头 `X-RateLimit-Remaining` 和 `X-Request-ID` 辅助排障；
  - 开启 `stream_options={"include_usage": true}` 获取精确 token 消耗，避免预算超支。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [application call](../api/application-call.md)
- [vector and sort](../api/vector-and-sort.md)


