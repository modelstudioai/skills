# 函数调用

函数调用（Function Calling）是百炼平台中大模型主动识别用户意图、生成结构化工具调用请求，并交由外部系统执行的关键能力。它使模型能脱离纯文本生成，安全、可控地接入搜索、代码解释、数据库查询、OCR解析等真实世界能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **API 直接调用**：在 DashScope 或 Anthropic 兼容接口中，通过 `tools` 参数声明可用函数列表，模型会在 `output.choices[0].message.tool_calls`（DashScope）或 `content` 中的 `tool_use` 块（Anthropic）返回结构化调用请求；[OpenAI 兼容接口](openai-compatible-interface.md)虽支持 `functions`/`function_call` 字段，但**不原生解析和验证工具参数**，需开发者自行封装解析逻辑。
- **意图理解模型**：`tongyi-intent-detect-v3` 支持 `INTENT_MODE`，当系统消息包含 `Response in INTENT_MODE.` 时，模型直接输出 `<tool_call name="xxx">{"arg1": "val"}</tool_call>` 格式，便于正则提取与路由。
- **Agent 开发**：
  - Flow Agent 和 Sandbox 支持在流程图或 Python 代码中显式配置 `tools` 列表，模型将基于上下文自主决策是否调用及传参；
  - Managed Agent 不开放自定义工具，其内置插件（如夸克搜索、代码解释器）已预集成，无需手动声明函数。
- **应用级插件集成**：在 RAG 或 Agent 应用中，自定义插件需严格遵循 OpenAI-style function calling 协议（含 `name`、`description`、`parameters` JSON Schema），百炼运行时据此校验参数并发起 HTTP 调用；注意：仅 `Authorization` Header 可透传，其余自定义 Header 将被丢弃。

## 关键参数和配置

- `tools`: 必填（启用函数调用时），为函数定义数组，每个元素包含：
  - `name`: 字符串，函数唯一标识（须与后端实现一致）；
  - `description`: 字符串，模型用于理解用途的简要说明；
  - `parameters`: 符合 JSON Schema 的对象，定义参数名、类型、是否必需、枚举值等（推荐使用 `type: "object"` + `properties`）。
- `tool_choice`: 可选，控制调用策略：
  - `"auto"`（默认）：模型自主决定是否调用；
  - `"none"`：禁止调用任何函数；
  - `{"type": "function", "function": {"name": "xxx"}}`：强制调用指定函数。
- `enable_search` / `enable_code_interpreter`: DashScope 专属布尔开关，用于快速启用平台内置搜索或代码解释器（等价于预注册对应 `tools`）。
- `system` 消息提示：对部分模型（如 `tongyi-intent-detect-v3`）必须显式写入 `Response in INTENT_MODE.` 才触发函数调用格式输出。

> ⚠️ 注意：函数调用结果不会自动注入后续对话历史；若需多步协同（如“查天气→转述给用户”），开发者须手动将 `tool_calls` 请求发送至工具服务，并将 `tool_response` 作为 `role: "tool"` 消息追加回 `messages` 数组后再次调用模型。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [more models](../api/more-models.md)
- [agent development](../guides/agent-development.md)
- [application support](../guides/application-support.md)


