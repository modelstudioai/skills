# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 API 协议层，严格遵循 OpenAI REST API 的路径、请求/响应格式、参数命名与错误规范（如 `/v1/chat/completions`、SSE 流式事件、`error.type` 结构），使开发者能复用现有 OpenAI SDK（Python/Node.js/Java/Go 等）和业务代码，零改造接入百炼全系列模型与能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移与多模型切换**：已使用 OpenAI SDK 的项目，只需将 `base_url` 替换为百炼的兼容端点（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），并指定支持的模型名（如 `"qwen3.8-max"`），即可调用文本生成、多模态理解、[向量嵌入](vector-embedding.md)等能力，无需重写逻辑。
- **开发工具链集成**：VS Code、Cursor、ZCode、Claude Code 等主流 AI 编程客户端均原生支持 OpenAI 协议，通过配置对应计费方案的 Base URL 和 API Key，即可直接启用 Qwen 系列模型，实现代码补全、解释、调试等场景。
- **智能体（Agents）构建**：`/v1/agents` 等 Agents API 完全兼容 OpenAI Agent SDK 生态，支持创建、会话管理、工具调用（`tools`/`tool_choice`）等语义，便于快速搭建具备记忆与执行能力的生产级 Agent。
- **文件与批量处理**：`/v1/files`（文件上传/管理）、`/v1/batch`（异步批量推理）等接口沿用 OpenAI 文件与批处理规范，支持 `file_id` 引用、状态轮询、结果下载等标准流程。
- **多模态与结构化输出**：视觉模型（如 `qwen3-vl-plus`）通过 `/v1/chat/completions` 接收 `content` 中含 `image_url` 或 `image_data` 的消息；JSON Schema 输出通过 `response_format={"type": "json_object"}` 启用（需配合 `response_schema`）。

> ⚠️ 注意：OpenAI 兼容接口**不支持百炼特有功能**，如临时 API Key、业务空间专属鉴权上下文、DashScope 原生 `seed` 参数、`thinking_budget`、`enable_search`（需改用 Responses API）等。如需这些能力，请选用 DashScope 原生协议。

## 关键参数和配置

| 参数 | 说明 | 示例值 | 注意事项 |
|------|------|--------|----------|
| `base_url` | **必填**，服务入口地址。必须使用业务空间专属域名（推荐）或 DashScope 兼容域名 | `https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `{WorkspaceId}` 需替换为控制台获取的真实 ID；地域（如 `cn-beijing`）必须与 API Key 所属地域一致，否则返回 `401 InvalidApiKey` |
| `model` | **必填**，模型标识符。不同接口支持范围不同 | `"qwen3.7-plus"`, `"qwen3-vl-plus"`, `"text-embedding-v4"` | 三方模型（DeepSeek/Kimi/GLM）仅限华北2（北京）且需控制台手动开通；`auto` 模型路由仅适用于 [Token](token.md) Plan 场景 |
| `api_key` | **必填**，认证凭证。通过控制台获取，按计费方案区分类型 | `sk-xxx`（[Token](token.md) Plan）、`ak-xxx`（按量计费）、`ck-xxx`（Coding Plan） | **严禁硬编码**；生产环境建议使用临时 API Key（最长 1800 秒） |
| `response_format` | JSON 结构化输出控制 | `{"type": "json_object"}` | 仅支持 `"json_object"`；`response_schema` 必须为有效 JSON Schema 对象（非字符串） |
| `previous_response_id` | Responses API 多轮对话专用，用于自动注入历史上下文 | `"0c842a11-c7d1-45da-b7ec-4e668c389xxx"` | 值为上一轮响应顶层 `id` 字段（UUID），有效期 7 天；传错将导致上下文丢失 |
| `enable_thinking` | Batch 场景下显式关闭思考模式以节省 token | `{"enable_thinking": false}` | **必须作为 JSONL 请求体顶层字段**，不可放在 `extra_body` 内 |

> ✅ 提示：所有 OpenAI 兼容接口均支持标准流式响应（`stream: true`），事件格式严格遵循 OpenAI SSE 规范（`data: {...}\n\n`），可直接被 `openai.Stream` 或 `OpenAIStream` 等生态库消费。

## 面向开发者，简洁实用

- **起步最快方式**：  
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key="sk-xxx",  # 替换为你的 API Key
      base_url="https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  response = client.chat.completions.create(
      model="qwen3.7-plus",
      messages=[{"role": "user", "content": "你好"}]
  )
  print(response.choices[0].message.content)
  ```

- **验证是否生效**：检查响应头 `x-request-id` 是否存在、响应体含 `id`/`object`/`created` 字段，且错误响应符合 OpenAI 格式（含 `error.message` 和 `error.type`）。

- **避坑清单**：  
  - ❌ 不要将 `base_url` 写成 `https://dashscope.aliyuncs.com/api/v1/...`（这是 DashScope 原生路径）；  
  - ❌ 不要在 `messages.content` 中传纯字符串给多模态模型（如 `qwen3-vl-plus`），必须用数组结构；  
  - ❌ 不要期望 `temperature` 在 Agents API 中生效（该接口固定解码策略）；  
  - ✅ 优先使用业务空间专属域名，性能更优、流量隔离、长期可用。  

如需百炼特有能力（联网搜索、自动历史管理、思考预算控制等），请切换至 [DashScope 原生协议](../../raw/model-api-reference/preparations.md) 或 [Responses API](../../raw/qwen-api-reference/qwen-api-reference.md)。

## 关联主题页

- [preparations](../api/preparations.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [openai compatible agents api](../api/openai-compatible-agents-api.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [file management api](../api/file-management-api.md)


