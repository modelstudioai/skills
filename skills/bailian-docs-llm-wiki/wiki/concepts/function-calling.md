# 函数调用

函数调用（Function Calling）是百炼平台中大模型主动识别用户意图、生成结构化工具请求，并交由外部系统执行的关键能力。它使模型不再仅输出文本，而是能动态调用预定义函数（如搜索、计算、查数据库），再将结果注入上下文继续推理，从而构建具备真实行动力的智能体。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非统一接口能力，而是根据使用场景和接入协议呈现不同形态与约束：

- **DashScope 原生接口**：通过 `tools` 数组声明函数列表（含 `name`、`description`、`parameters` JSON Schema），配合 `tool_choice` 控制调用策略（`auto`/`required`/`none`）。模型返回 `tool_calls` 字段，开发者需解析并同步执行对应函数，再将结果以 `tool_message` 形式回传给下一轮 `/generation` 请求。这是最灵活、可完全自定义函数逻辑的方式。

- **Anthropic 兼容 Messages 接口**：使用标准 `tools` + `tool_choice`，响应中以 `content` 数组包含 `tool_use` 类型块（含 `id`、`name`、`input`）。需按 Anthropic 协议构造 `tool_result` 消息并发起下一次 `/messages` 调用。适合需要显式推理链（thinking step）和多工具编排的场景。

- **Qwen Omni Realtime API**：支持 `type=function` 工具定义（`type=mcp` 为另一协议），但**与 `enable_search` 互斥**。调用流程为 WebSocket 流式事件驱动：收到 `function_call` 事件 → 执行本地或远程函数 → 发送 `function_result` 事件。适用于低延迟语音/实时对话场景。

- **Managed Agents（托管智能体）**：函数调用被封装为 Skill 或 MCP 服务的自动触发行为。开发者不直接处理 `tool_calls`，而是预先注册 Skill（如 `pdf_parser`）或绑定 MCP 服务（如 `amap-maps`），智能体运行时根据 `description` 匹配意图并自动调度。此方式屏蔽底层协议细节，面向业务逻辑抽象。

> ⚠️ 注意：OpenAI 兼容 Chat Completions 接口（如 `/v1/chat/completions`）**不支持自定义函数调用**，其“工具能力”为平台预置且不可扩展；MCP 服务也**不能直接用于千问 API 调用**，仅限智能体或工作流内部集成。

## 关键参数和配置

| 参数 | 所属接口 | 类型 | 说明 |
|------|----------|------|------|
| `tools` | DashScope、Anthropic、Omni Realtime | array | 必填。函数定义列表，每个元素含 `type="function"`、`function.name`、`function.description`、`function.parameters`（JSON Schema） |
| `tool_choice` | DashScope、Anthropic | string / object | 可选。控制调用策略：`"auto"`（默认）、`"none"`（禁用）、`"required"`（必须调用），或指定 `{"type": "function", "function": {"name": "xxx"}}` |
| `tools`（Omni） | Omni Realtime | array | 同上，但字段路径为 `session.tools`，需通过 `session.update` 事件设置 |
| `enable_search` | DashScope、Omni Realtime | boolean | 平台内置搜索开关，**与自定义 `tools` 互斥**，启用后模型可自主触发联网搜索（非函数调用） |

- **无须配置但需开发者实现的环节**：  
  - 函数执行逻辑（如调用高德 API 获取天气）  
  - `tool_message` / `tool_result` 的构造与回传格式（各接口规范不同）  
  - 错误处理与重试（如函数超时、返回格式不符时的降级策略）

## 面向开发者，简洁实用

- ✅ **首选 DashScope 原生接口**：新项目推荐使用，参数最全、控制最细、文档最明确，`tools` 定义与 OpenAI 兼容但行为更稳定。  
- ✅ **实时场景用 Omni Realtime**：需语音/低延迟交互时，用 WebSocket 处理 `function_call`/`function_result` 事件流，避免 HTTP 往返延迟。  
- ✅ **业务集成用 Managed Agents**：已有业务系统（如 CRM、ERP），优先封装为 Skill 或 MCP 服务，在智能体中拖拽绑定，零代码调用。  
- ❌ **避免混用协议**：不要在 [OpenAI 兼容接口](openai-compatible-interface.md)里传 `tools`（会被忽略）；不要在单次 API 调用中同时开 `enable_search` 和 `tools`（会报错）。  
- 🔧 **调试建议**：开启 `stream=false` + `debug=true`（DashScope 支持）查看完整 `tool_calls` 输出；用 `curl -N` 或 SDK 流式解析验证事件顺序。  
- 📦 **函数设计原则**：`description` 要清晰描述用途和输入约束；`parameters` Schema 必须严格校验；返回结果尽量精简（避免 token 溢出）。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [agent store](../guides/agent-store.md)
- [managed agents api](../api/managed-agents-api.md)


