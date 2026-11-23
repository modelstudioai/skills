# 函数调用

函数调用（Function Calling）是百炼平台中智能体（Agent）实现工具驱动推理的核心机制：模型根据用户输入自主判断是否需要、以及调用哪些外部工具，并按严格定义的参数结构生成标准化的调用请求；平台负责路由、执行、结果注入与上下文融合，最终由模型整合工具输出生成自然语言响应。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非单一接口能力，而是贯穿多个 Agent 架构层级的横切行为模式，具体体现为：

- **Agent 运行时（`/v1/agents/run`）**：通过 `tools` 数组声明工具集合，模型自动选择并生成 `tool_calls`；调用结果以结构化 JSON 形式返回，不暴露原始 HTTP 细节。  
- **[OpenAI 兼容接口](openai-compatible-api.md)（`/compatible-mode/v1/chat/completions`）**：完全复用 OpenAI 的 `tools` + `tool_choice` 语义，支持 `"auto"`、`"none"` 或指定函数名；响应中 `finish_reason: "tool_calls"` 明确标识调用发生，`message.tool_calls` 包含完整调用指令。  
- **Managed Agents（托管式 Agent）**：工具以预注册的类型化能力（如 `"file_search"`、`"web_search"`）接入，开发者无需编写 schema，平台自动映射为内部函数调用，降低定义门槛。  
- **Agent Store 能力集成**：MCP 服务和 Skill 均作为“可调用函数”的物理载体——MCP 提供标准化协议端点（`/mcp`、`/sse`），Skill 封装 ZIP 内的可执行逻辑；二者均需在应用配置中显式启用，方能被模型识别为可用函数。  
- **自定义插件（Application Support）**：支持注册任意 HTTP API 为函数，平台自动解析其 OpenAPI 3.0 描述，生成符合百炼调用规范的函数签名；但仅允许透传 `Authorization` Header，其余 Header 被剥离。  
- **Flow Agent 应用调用**：虽未暴露底层 `tool_calls` 字段，但当应用绑定 MCP 或 Skill 后，函数调用行为由平台隐式完成，开发者只需关注 `app_id` 和 `input`，无需感知调用细节。

> ✅ 关键共识：所有场景下，“函数”本质是**带名称、描述和 JSON Schema 参数的可执行能力单元**；模型不直接发起 HTTP 请求，而是生成符合 schema 的调用声明，由百炼运行时统一调度执行。

## 关键参数和配置

| 参数 | 所属场景 | 类型 | 说明 | 必填性 |
|------|----------|------|------|--------|
| `tools` | 所有 Agent 接口（`/v1/agents/run`, `/chat/completions`, Managed Agents） | array | 工具定义列表，每个元素含 `name`（合法 Python 标识符）、`description`、`parameters`（JSON Schema Draft-07） | 否（无则退化为普通对话） |
| `tool_choice` | [OpenAI 兼容接口](openai-compatible-api.md) | string / object | 控制调用策略：`"auto"`（默认）、`"none"` 或 `{"type": "function", "function": {"name": "xxx"}}` | 否 |
| `name`（工具内） | 所有场景 | string | 函数唯一标识符，必须为合法 Python 标识符（字母/数字/下划线，不以数字开头）；否则返回 `422 Unprocessable Entity` | 是 |
| `parameters`（工具内） | 所有场景 | object | 严格遵循 JSON Schema Draft-07；不支持 `additionalProperties: true` 等宽松校验，缺失必填字段将触发 `validation_error` | 是（若定义了参数） |
| `enable_session` + `session_id` | [OpenAI 兼容接口](openai-compatible-api.md) | boolean / string | 启用会话状态后，函数调用上下文（如前序结果）可跨轮次复用；`session_id` 需客户端维护 | 条件必填（启用会话时） |

> ⚠️ 注意：`temperature`、`top_p` 等采样参数对函数调用决策**无直接影响**；模型是否调用函数主要取决于 `tools` 定义质量、`system_prompt` 中的工具说明清晰度，以及用户 query 的明确性。

## 面向开发者，简洁实用

- **定义函数，先写好 `name` 和 `description`**：`description` 是模型理解能力的关键，需用一句话说清“做什么、输入什么、输出什么、何时用”，避免模糊表述（如“处理数据” → “从 Excel 表格中提取销售额大于100万的客户姓名和邮箱”）。  
- **参数 Schema 要最小化、强约束**：只声明必需字段，用 `type`、`enum`、`minLength` 等严格限定；避免 `anyOf` 或嵌套过深，否则易触发校验失败。  
- **调试首选 `max_iterations=3` + `verbose=true`（需技术支持开通）**：快速定位模型为何未调用函数（是没看到？参数不匹配？还是根本没理解需求？）。  
- **函数名即契约**：`name` 一旦发布，不可随意变更；下游系统（如 MCP 服务、Skill 后端）必须严格按此名称响应，否则平台无法匹配结果。  
- **不要自己拼接 HTTP 请求**：所有函数调用均由百炼运行时完成；你只需提供正确 `tools`，接收结构化结果，专注业务逻辑整合。

## 关联主题页

- [get started with agents](../guides/get-started-with-agents.md)
- [managed agents api](../api/managed-agents-api.md)
- [flow agent api](../api/flow-agent-api.md)
- [openai compatible agents api](../api/openai-compatible-agents-api.md)
- [agent store](../guides/agent-store.md)
- [application support](../guides/application-support.md)


