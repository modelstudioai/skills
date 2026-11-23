# 函数调用

函数调用（Function Calling）是百炼平台中智能体（Agent）与外部能力交互的核心机制，指模型在推理过程中自主识别用户意图、生成结构化工具调用请求（`tool_calls`），并由平台调度执行预注册函数（如 MCP 服务、Skill、自定义 HTTP 接口等）的能力。该机制将大模型的“规划”能力与确定性程序逻辑解耦，实现安全、可控、可审计的 AI 自动化。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用不是独立接口，而是贯穿多个 Agent 运行时层的统一语义能力，具体体现为：

- **OpenAI 兼容 Agents API**：通过标准 `tools` 数组声明函数签名（支持 `function` 类型），配合 `tool_choice` 控制调用策略；响应中若含 `tool_calls` 字段，即表示模型已触发函数调用，需开发者或平台自动执行后续步骤（如调用 MCP 服务、解析 Skill 输入）。
  
- **Managed Agents API**：不暴露原始 `tool_calls`，而是封装为更高阶的 **Skill 调用** 和 **Webhook 触发**。当用户输入匹配 Skill 的 `description` 或满足 Webhook 配置条件时，平台自动路由至对应能力，开发者无需解析 JSON Schema 或拼接调用参数。

- **Flow Agent（可视化编排）**：以「工具节点」形式呈现，支持拖拽接入 MCP 服务或 Skill，并通过图形化参数映射（如将前序节点输出字段绑定到 `weather.city`）完成函数调用配置；调用逻辑由平台运行时自动注入上下文并处理返回结果。

- **Sandbox Agent（代码沙箱）**：开发者需在 `Agent.run()` 中手动解析 `messages[-1].tool_calls`（若存在），调用 `bailian-sdk` 提供的 `call_tool()` 方法执行指定函数（如 `mcp.call("websearch", {"query": "杭州天气"})`），并把结果以 `tool_message` 格式回传给模型继续推理。

- **Agent Store（能力中心）**：函数调用的“供给侧”。MCP 服务和 Skill 本质是被调用的函数实体——前者提供标准化的远程 API 接口（`streamablehttp`/`stdio`），后者提供声明式的本地文件处理逻辑；二者均需通过 `agent store` 注册、授权、配置后，才能被上述任一 Agent 模式调用。

> ✅ 关键共识：无论哪种模式，函数调用均由模型主动发起（非 Prompt 硬编码），且调用目标必须提前在平台侧注册/启用；未注册的函数名将导致 `invalid_tool_call` 错误。

## 关键参数和配置

| 参数/配置项 | 所属场景 | 说明 | 注意事项 |
|-------------|----------|------|----------|
| `tools` | OpenAI 兼容 Agents API、Sandbox | JSON Schema 数组，定义可调用函数的名称、描述、参数类型与约束 | 必须严格遵循 OpenAI 工具格式；Schema 过长会占用 token 预算，建议精简 `description` |
| `tool_choice` | OpenAI 兼容 Agents API | 控制调用策略：`"auto"`（默认，由模型决策）、`"none"`（禁用）、`{"type":"function","function":{"name":"xxx"}}`（强制指定） | 强制指定时，若模型无法生成匹配参数，将报错而非降级为文本回复 |
| `mcpServers` / `SKILL.md` | Agent Store | MCP 服务的连接配置（含协议、地址、环境变量）；Skill 的元数据描述（`name`, `description`, `input_schema`） | `description` 直接影响模型调用准确率，需包含典型触发词、输入示例、边界说明 |
| `enable_rag`（间接影响） | Managed/Flow Agent | 启用 RAG 时，知识库检索结果可能作为 `tool_message` 注入上下文，影响后续函数调用决策 | 并非直接控制函数调用，但改变模型可用信息，从而改变调用行为 |
| `max_iterations` | Flow/Sandbox Agent | 限制单次请求中函数调用+模型推理的总循环次数 | 默认 `10`，但 Managed Agent 实际硬限为 `5`；超限将终止流程并返回 `max_iterations_exceeded` |

## 面向开发者，简洁实用

- **调试优先**：所有 Agent 模式均支持 `X-Bailian-Debug: true` 请求头，返回完整调用链日志（含 `tool_calls` 原始内容、MCP/Skill 执行耗时、错误堆栈），务必在开发期开启。
- **错误处理必做**：函数调用失败（如网络超时、参数校验失败、权限不足）会返回 `tool_calls` + `error` 字段，需在代码中显式捕获并构造 `tool_message` 回传，否则流程中断。
- **安全红线**：禁止在 Sandbox 中通过 `subprocess` 或 `os.system` 动态执行未注册函数；所有外部调用必须经由 `bailian-sdk` 的 `call_tool()` 或平台预置节点完成，确保审计可追溯。
- **性能提示**：MCP 服务冷启动延迟高，高频调用场景请选用「极速模式」部署；Skill ZIP 包超过 5MB 会显著增加加载时间，建议拆分大依赖。
- **兼容性确认**：`qwen-max` 等通用模型**不支持函数调用**；必须使用带 `-agent-v1` 后缀的专用 Agent 模型（如 `qwen-plus-agent-v1`）或 Managed Agent 底层托管模型。

## 关联主题页

- [managed agents api](../api/managed-agents-api.md)
- [openai compatible agents api](../api/openai-compatible-agents-api.md)
- [agent development](../guides/agent-development.md)
- [agent store](../guides/agent-store.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


