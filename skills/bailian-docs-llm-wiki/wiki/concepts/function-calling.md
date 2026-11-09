# 函数调用

函数调用（Function Calling）是百炼平台中大模型主动识别用户意图、自主规划并执行外部工具能力的核心机制。它不是传统编程意义上的函数调用，而是由模型基于自然语言输入，动态生成结构化工具请求（含工具名称与参数），交由平台调度执行，并将结果注入上下文以完成最终响应的端到端协同过程。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非统一接口，而是根据使用路径呈现三种典型形态，开发者需按场景选择：

- **智能体（Agent）中的隐式函数调用**：在 `Managed Agent` 或 `Flow Agent` 中启用插件（如 `code_interpreter`、`quark_search`）或 MCP 服务（如 `WebSearch`、`Amap Maps`）后，模型自动判断是否需要调用、调用哪个工具、传入哪些参数。开发者无需编写调用逻辑，只需配置工具列表与权限，模型在推理链中自主触发——这是最常用、最符合“智能体”语义的函数调用方式。

- **工作流（Workflow）中的显式函数调用**：在工作流画布中，将插件或 MCP 服务作为独立节点拖入，手动配置输入映射（如从上一节点提取的 `city` 字段 → 工具参数 `location`）。此时调用完全由编排逻辑控制，不依赖模型决策，适用于确定性高、需精确控制参数和错误处理的场景（如订单状态查询、数据库写入）。

- **API 层的声明式函数调用**：通过 DashScope 原生接口或 Assistant API（如 `/v1/agents/{agent_id}/invoke` 或 OpenAI 兼容的 `tools` + `tool_choice` 字段），在请求体中显式声明可用工具集合（`tools`）及调用策略（`tool_choice: "auto"` / `"required"` / `{"type": "function", "function": {"name": "xxx"}}`）。模型据此生成符合 OpenAI Tool Calling Schema 的 `tool_calls`，平台解析后分发执行。此方式适合需要细粒度控制调用时机与工具集的 SDK 集成场景。

> ⚠️ 注意：`OpenAI 兼容 Responses` 接口**不支持**自定义 `tools` 字段，其工具能力（搜索、代码解释）为内置且不可配置；若需可控函数调用，请优先选用 DashScope 原生接口或 Agent API。

## 关键参数和配置

函数调用行为由以下关键参数共同决定，不同场景下配置位置不同：

| 参数 | 所属层级 | 类型 | 说明 | 是否必填 |
|------|----------|------|------|-----------|
| `tools` | 请求体（API）、应用配置（Agent/Workflow） | array | 工具定义列表，每个元素包含 `type`（`function` 或 `mcp`）、`function.name`、`function.description`、`function.parameters`（JSON Schema） | 是（启用调用时） |
| `tool_choice` | 请求体（API） | string / object | 控制调用策略：`"auto"`（模型自主决定）、`"required"`（必须调用至少一个）、或指定具体工具名 | 否（默认 `auto`） |
| `enable_search` / `enable_code_interpreter` | DashScope 接口请求体 | boolean | 显式开关内置工具（仅 DashScope 原生接口支持）；`OpenAI 兼容 Responses` 中该参数无效 | 否（DashScope 接口需显式设为 `true` 才启用） |
| `biz_params` | Agent/Workflow API 请求体 | object | 用于透传业务参数（如用户 ID、租户上下文）或用户级鉴权 [Token](token.md)，供自定义插件/MCP 服务读取 | 否（按需） |
| `tools`（应用级） | 智能体/工作流控制台配置 | — | 在「编排」页添加的插件或 MCP 服务列表，即运行时实际可用的 `tools` 集合 | 是（启用工具能力时） |

> ✅ 最佳实践：生产环境推荐使用 **DashScope 原生接口 + 显式 `tools` 定义**，因其参数可预测、行为一致、调试友好；低代码场景则直接在 **Agent 应用配置页添加工具**，由平台自动注入 `tools` 并管理生命周期。

## 面向开发者，简洁实用

- **不要手动拼接工具 URL 或构造 HTTP 请求**：百炼平台已封装完整调用链（模型→参数提取→鉴权→请求→结果解析→上下文注入），你只需提供标准工具描述（JSON Schema）和业务参数。
- **工具参数描述越精准，调用成功率越高**：`function.description` 应明确用途、输入约束与典型示例；`parameters` 的 JSON Schema 中，`required` 字段、`type` 和 `description` 缺一不可。
- **警惕 [Token](token.md) 开销**：每次函数调用会增加输入 [Token](token.md)（工具定义 + 原始 query）和输出 Token（工具返回结果作为新 context），长对话中需监控总长度（Qwen 系列上限 32768 tokens）。
- **调试技巧**：开启 `stream=true` 时，观察响应流中 `delta.tool_calls` 字段，可实时验证模型是否正确识别调用意图；若未触发，优先检查 `tools` 描述是否模糊或参数 schema 是否缺失 `required`。
- **错误定位**：常见失败原因包括——工具未在当前应用中启用（权限/配置遗漏）、`parameters` schema 与实际 API 不匹配、自定义插件鉴权失败（检查 `biz_params` 或 Header 配置）、MCP 服务地址不可达（确认 `url` 和 `type` 匹配）。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [llm application](../guides/llm-application.md)
- [get started with agents](../guides/get-started-with-agents.md)
- [plug in](../guides/plug-in.md)
- [agent store](../guides/agent-store.md)


