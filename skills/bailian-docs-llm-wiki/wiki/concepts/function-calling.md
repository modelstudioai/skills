# 函数调用

函数调用（Function Calling）是百炼平台中让大模型具备**主动识别用户意图、结构化生成工具请求、并协同外部系统执行动作**的核心能力。它不是简单的文本输出，而是模型在推理过程中自动生成符合预定义 Schema 的 JSON 工具调用指令，交由运行时环境解析、执行并注入结果回对话流。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非单一接口特性，而是贯穿多类模型与交互范式的横切能力，具体体现为：

- **通用大模型（Qwen-Max/Plus/Turbo）**：通过 `tools` + `tool_choice` 参数声明可用函数列表，模型在生成响应前可自主决定是否调用、调用哪个函数及传入参数。DashScope 原生接口支持最完整的控制（如 `tool_choice="auto"` / `"required"` / `{"type": "function", "function": {"name": "xxx"}}`），且流式响应中可逐帧返回工具调用中间步骤；Anthropic 兼容接口完整支持 `tool_use` 语义；OpenAI 兼容的 `chat/completions` 接口**不原生支持**，需自行解析模型输出的 JSON 字符串。

- **实时多模态交互（Qwen-Omni-Realtime）**：支持 `type=function` 工具定义，与 `type=mcp` 并存（但不可与 `enable_search` 同时启用）。VAD 触发语音输入后，模型可在文本响应中嵌入函数调用，服务端自动拦截、执行并追加 `conversation.item.created`（role=`tool`）事件，实现“说一句话，查一次天气，播一段音频”的无缝链路。

- **专用模型（意图理解、GUI-Plus 等）**：  
  - `tongyi-intent-detect-v3` 提供 `INTENT_MODE`，将用户输入直接映射为标准化函数调用（如 `{"name": "route_to_sales", "parameters": {}}`），毫秒级完成对话路由；  
  - `gui-plus` 系列要求在 system message 中声明 `<tools>` 和 `<tool_call>` 输出格式，模型输出严格遵循该结构，确保 UI 操作指令可被自动化引擎精准解析执行。

- **Agent 编排与 RAG 应用**：函数调用是 Agent 的“手脚”。当 `context.rag.enabled=true` 或 `context.connector.ids` 配置生效时，模型可结合检索到的知识或 Connector 拉取的实时数据，动态生成函数调用（如 `get_user_order_status(order_id=xxx)`），实现“查知识 → 调 API → 综合回答”的闭环。

> ⚠️ 注意：所有函数调用均**不共享会话状态**——每次调用独立执行，返回结果后由平台自动拼入消息历史；若需跨调用状态传递，请在 `parameters` 中显式携带上下文字段，或使用 `context.memory` 模块持久化关键信息。

## 关键参数和配置

| 参数 | 类型 | 说明 | 必填性 | 支持接口 |
|------|------|------|--------|----------|
| `tools` | array | 工具定义列表，每个元素为 OpenAPI 3.0 兼容的 JSON Schema（含 `name`, `description`, `parameters`） | 否（无工具则不触发） | DashScope、Anthropic、OpenAI-Responses、Omni-Realtime、Intent-Detect、GUI-Plus |
| `tool_choice` | string / object | 控制调用策略：<br>• `"auto"`（默认，模型自主决策）<br>• `"none"`（禁用）<br>• `"required"`（必须调用一个）<br>• `{"type": "function", "function": {"name": "xxx"}}`（指定函数） | 否（默认 `auto`） | DashScope、Anthropic（`tool_choice`）、Omni-Realtime（`tool_choice`）；*OpenAI-Responses 使用隐式调度，不暴露此参数* |
| `enable_search` | boolean | 启用联网搜索（自动触发 `web_search` 工具） | 否 | DashScope、Omni-Realtime、Qwen-Deep-Research；⚠️ 与 `tools` 不可共存（二者互斥） |
| `system` message | string | **必须明确提示模型启用函数调用**，例如：<br>`"You are a helpful assistant. Use the provided functions to answer user questions."`<br>或针对 Intent 模型：<br>`"Response in INTENT_MODE."` | 是（否则模型忽略 `tools`） | 全部支持函数调用的接口 |

## 面向开发者，简洁实用

- ✅ **快速验证**：用 `qwen-turbo` + DashScope 接口，`tools=[{"name":"get_time","description":"获取当前时间","parameters":{"type":"object"}}]`，发送 `"现在几点？"`，观察响应中 `output.choices[0].message.tool_calls` 字段。
- ✅ **错误排查**：若未触发调用，先检查 `system` message 是否含明确指令；再确认 `tools` Schema 是否语法合法（推荐用 [JSON Schema Validator](https://jsonschemalint.com/) 校验）；最后检查模型是否支持（`qwen-turbo` 支持，但部分旧版 OCR 模型不支持）。
- ✅ **生产建议**：  
  - 优先选用 DashScope 接口——功能最全、流式调试友好、文档最准；  
  - 工具名（`name`）用小写字母+下划线，避免空格与特殊字符；  
  - `parameters` 中必填字段标注 `"required": ["field1", "field2"]`，模型将严格校验；  
  - 多工具场景下，`tool_choice="required"` 可强制模型选择，避免“不调用”导致流程中断。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [agent context](../guides/agent-context.md)
- [more models](../api/more-models.md)
- [application support](../guides/application-support.md)


