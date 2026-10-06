# 函数调用

函数调用（Function Calling）是百炼平台支持的核心能力之一，指大语言模型在生成响应过程中，主动识别用户意图并结构化地选择、参数化调用预定义的外部工具（如搜索、数据库查询、业务 API 等），再将工具返回结果整合进最终输出。该能力使模型从“纯文本生成器”升级为可执行真实动作的智能代理。

## 在百炼平台的不同场景中，这个概念如何使用

- **基础模型 API 调用**：在 `POST /v1/services/aigc/text-generation/generation` 或 `/v1/chat/completions` 接口请求中，通过 `tools` 字段声明一组 JSON Schema 描述的函数（含 `name`、`description`、`parameters`），并在 `messages` 中传入用户问题；模型会返回 `tool_calls` 数组（含 `function.name` 和 `function.arguments`），而非直接生成自然语言答案。开发者需解析该结构，同步/异步执行对应函数，并将结果以 `tool` 角色消息回传，触发模型生成最终回复。

- **智能体（Agent）应用调用**：在 `application call` 场景下（如 `POST /api/v1/apps/{APP_ID}/completion`），函数调用能力已内建于 Agent 2.0 运行时。开发者无需手动处理 `tool_calls` 解析与结果注入——平台自动完成工具发现、参数校验、执行调度及上下文拼接。只需在创建智能体时配置插件（Plugin）或自定义工具（Custom Tool），并在 `biz_params` 中透传必要凭证或上下文变量即可。

- **RAG 与知识库增强场景**：当启用 `retrieval_config` 且模型支持函数调用时，平台可能隐式调用向量检索服务作为“内置工具”，将召回文档片段以 `tool` 消息形式注入对话历史，辅助模型精准引用。此过程对开发者透明，但需注意：显式声明的 `tools` 与隐式 RAG 检索互不冲突，可共存。

- **[OpenAI 兼容接口](openai-compatible-interface.md)（Responses API）**：在 `compatible-mode/v1/responses` 路径下，函数调用行为完全遵循 OpenAI 的 `tool_choice` + `tools` 协议。支持 `tool_choice: "auto"`（默认）、`"none"` 或指定 `{"type": "function", "function": {"name": "xxx"}}`，响应格式（`delta.tool_calls` 流式事件、`message.tool_calls` 完整数组）与 OpenAI 一致，便于现有 LangChain / LlamaIndex 工具链无缝迁移。

> ⚠️ 注意：并非所有模型均支持函数调用。`qwen-max`、`qwen-plus`、`qwen3.8-max` 等主流大模型默认支持；`qwen-turbo`、`qwen-vl` 等轻量或专用模型可能不支持。请以 [模型能力矩阵](../../raw/model-user-guide/get-started-with-models/models.md) 中“Function Calling”列标注为准。

## 关键参数和配置

- `tools`（必需，数组）：定义可用工具列表，每个元素为对象，包含：
  - `type`: 固定为 `"function"`
  - `function.name`: 工具唯一标识符（字符串，仅字母/数字/下划线，建议小写）
  - `function.description`: 工具功能说明（帮助模型理解用途，影响调用准确性）
  - `function.parameters`: 符合 JSON Schema Draft 07 的参数定义对象（支持 `string`、`number`、`boolean`、`object`、`array` 及嵌套，`required` 字段必填）

- `tool_choice`（可选，字符串或对象）：
  - `"auto"`（默认）：模型自主决定是否调用工具及调用哪个
  - `"none"`：禁止调用任何工具，强制模型生成自然语言回复
  - `{"type": "function", "function": {"name": "xxx"}}`：强制调用指定工具（适用于确定性工作流）

- `parallel_tool_calls`（可选，布尔值）：设为 `true` 时允许模型并行发起多个工具调用（需模型支持，如 `qwen-max`）。默认 `false`（串行）。

- `enable_search`（特定场景）：当 `tools` 未显式声明搜索工具，但需启用百炼内置搜索时，可设 `enable_search: true`（仅 `qwen-max`/`qwen-plus` 支持），平台将自动注入等效搜索工具。

- 工具执行后的结果注入：需以 `role: "tool"` 的消息格式回传，包含：
  - `content`: 工具返回的原始字符串或 JSON 序列化结果
  - `tool_call_id`: 必须与原始 `tool_calls[0].id` 严格匹配（用于关联）

## 面向开发者，简洁实用

- ✅ **快速验证**：从最小 `tools` 开始（单个无参函数），用 `curl` 或 Postman 发送请求，观察响应中是否出现 `output.tool_calls` 字段。
- ✅ **参数安全**：`function.parameters` 中敏感字段（如 `api_key`）勿直接暴露在 `description`；应通过 `biz_params` 或 Header 传递，工具实现侧读取。
- ✅ **错误处理**：模型可能生成非法 JSON 参数。务必对 `function.arguments` 做 `JSON.parse()` 容错，并返回结构化错误消息（如 `{"error": "invalid date format"}`）供模型重试。
- ✅ **流式兼容**：启用 `stream=true` 时，`tool_calls` 以 `delta.tool_calls` 形式分块到达，需累积 `index` 并按 `id` 合并完整调用项。
- ❌ **避免陷阱**：不要在 `system` 消息中要求“必须调用工具”——这会干扰模型自主决策；应通过 `description` 和示例消息引导，而非指令压制。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [start using](../guides/start-using.md)
- [application call](../api/application-call.md)
- [application use cases](../guides/application-use-cases.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


