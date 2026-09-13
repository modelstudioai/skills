# 函数调用

函数调用（Function Calling）是百炼平台中大模型主动识别用户意图、生成结构化工具调用请求，并交由外部系统执行关键操作的核心能力。它使模型不再局限于文本生成，而是能安全、可控地对接数据库、API、计算服务等真实世界能力，构成智能体（Agent）、RAG增强、自动化工作流等高级应用的基础设施。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非单一接口，而是以统一语义、多路径支持的方式深度融入以下关键场景：

- **Managed Agents（托管智能体）**：作为 Agent 的默认工具调用机制。当配置 `tools` 列表（如 `http_request`, `sql_query`）后，模型在推理过程中自动决定是否及如何调用工具；调用结果通过上下文自动注入后续步骤，实现多步任务编排。注意：自定义 Python 函数不在此路径内，需通过独立 Function Calling API 调用。

- **Model Context Protocol（MCP）**：提供标准化、协议化的函数调用范式。开发者通过 OpenAPI Schema 注册工具，模型依据 `tools` 描述和 `tool_choice` 策略生成符合规范的 `tool_calls`；客户端解析后调用对应 MCP 服务，并将 `tool_responses` 回填至消息历史，形成闭环交互。这是构建可复用、可治理工具生态的推荐方式。

- **Plug-in（插件）**：面向开箱即用的轻量级扩展能力。通过声明 `plugins` 字段（如 `{"weather": {}}`），模型可调用平台预置或审核上架的插件。该路径屏蔽了底层协议细节，适合快速集成通用服务（如搜索、天气），但灵活性低于 MCP。

- **Application Use Cases（应用实践）**：在客服、助手、RAG等场景中，函数调用常与知识检索协同——例如，先调用 `search_knowledge_base` 工具获取文档片段，再将结果送入 LLM 生成最终回答。此时函数调用是“增强推理”的关键中间环节。

- **Toolkits and Frameworks（工具包兼容）**：[OpenAI 兼容接口](openai-compatibility.md)（`/v1/chat/completions`）完全支持函数调用语义（`tools`, `tool_choice`, `tool_calls` 字段），开发者可用标准 `openai` SDK 或 LangChain 的 `BailianChatModel` 直接启用，无缝迁移已有代码。

> ⚠️ 统一说明：所有路径均要求模型为 `qwen-max` / `qwen-plus` / `qwen-turbo`（部分新模型如 `qwen2.5-*` 尚未支持）。不支持的模型会忽略 `tools` 字段或返回错误。

## 关键参数和配置

函数调用行为由以下核心参数控制（适用于 `/v1/chat/completions` 及相关接口）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `tools` | array | 否（启用调用必填） | 工具列表，每个元素为 `{ "type": "function", "function": { "name": "...", "description": "...", "parameters": {...} } }`；`parameters` 为 OpenAPI 3.0 兼容 JSON Schema，强烈建议提供以提升参数生成准确性。 |
| `tool_choice` | string / object | 否 | 控制调用策略：<br>• `"auto"`（默认）：模型自主决定是否调用及调用哪个工具；<br>• `"required"`：强制模型必须调用一个工具；<br>• `{"type": "function", "name": "xxx"}`：指定必须调用某工具。 |
| `plugins` | object | 否（插件专用） | 插件启用字典，如 `{"web-search": {}, "calculator": {}}`；若同时传入 `plugins` 和 `tools`，`plugins` 优先级更高。 |
| `max_plugin_calls` | integer | 否（插件专用） | 单次请求最多触发插件调用次数，默认 `3`，上限 `5`。 |

其他重要配置：
- **上下文约束**：单次请求总 token（含 history + input + tools 定义）不得超过模型 context window 的 80%，否则拒绝请求。
- **安全策略**：HTTP 类工具默认禁止访问内网地址（`10.0.0.0/8`, `192.168.0.0/16` 等），不可绕过。
- **调试支持**：添加 `"debug": true` 可在响应中返回完整调用链路（如 `mcp_trace` 或 reasoning trace），便于定位工具选择或参数生成问题。

## 面向开发者，简洁实用

- ✅ **快速开始**：只需在 `messages` 后添加 `tools` 数组和 `tool_choice`，即可启用函数调用。无需修改模型或部署额外服务。
- ✅ **一次注册，多处复用**：通过 MCP 注册的工具，可同时被 Managed Agents、API 直调、可视化编排调用。
- ✅ **错误有迹可循**：常见失败原因包括：工具名不匹配、`parameters` Schema 缺失导致参数生成错误、插件未授权、响应格式不符合 JSON（顶层需含 `content` 或 `result` 字段）。
- ✅ **生产就绪建议**：
  - 工具 `description` 应清晰描述用途与副作用（如“查询用户订单，返回最近3笔”）；
  - 为关键工具设置 `parameters` Schema，避免模型生成非法参数；
  - 在 Agent 或 MCP 场景中，务必处理 `tool_calls` 返回后的异步执行与结果回填逻辑；
  - 流式响应（`stream=true`）**不支持函数调用**（会被自动禁用），需按完整响应处理。

函数调用不是“黑盒魔法”，而是你掌控 AI 行为的明确接口——定义好工具，模型就会按规则调用；校验好响应，业务逻辑就能稳稳承接。

## 关联主题页

- [managed agents](../guides/managed-agents.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [model context protocol](../guides/model-context-protocol.md)
- [application use cases](../guides/application-use-cases.md)
- [plug in](../guides/plug-in.md)


