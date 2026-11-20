# get started with agents

Agent 是百炼平台提供的智能体运行与编排能力，支持开发者快速构建具备知识接入、工具调用、上下文管理与安全治理能力的自主执行应用。本文档面向开发者，梳理核心模型类型、关键参数、使用路径及约束条件，帮助你完成首次 Agent 部署与调用。所有功能均需通过百炼控制台或 API 接入，不依赖独立 SDK。

## 支持的模型与功能类型

百炼当前提供三类核心 Agent 运行形态，分别适用于不同复杂度与可控性需求：

- **Managed Agent**：全托管式智能体，由平台统一管理会话生命周期、工具执行沙箱与环境隔离。适合快速验证业务逻辑，无需自行维护执行上下文。详见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)。
- **Flow Agent**：基于可视化工作流编排的 LLM 应用，支持多节点条件分支、并行调用与状态传递，适用于需要精细控制执行路径的场景。其设计范式与 Managed Agent 不同，不可混用配置。详见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)。
- **Sandbox**：轻量级隔离执行环境，专用于代码解释、浏览器自动化与文件解析等高风险操作，不承载完整 Agent 生命周期，需配合其他 Agent 类型使用。详见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)。

> **注意**：文档中提及的 MCP（Model Context Protocol）链接指向外部 help.aliyun.com 页面，而百炼平台实际对接的 MCP 服务已内置于 `managed-agents-api` 中，API 调用时通过 `tools` 字段声明即可，无需额外注册 MCP 服务器。请以 [raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中的 `tools` 参数定义为准。

## 关键参数

调用 Agent（尤其是 Managed Agent）时，以下参数直接影响行为与能力：

- `model_id`：必需，指定底层大模型 ID（如 `qwen-max`, `qwen-plus`），必须为平台已开通的模型；
- `tools`：数组，声明启用的工具列表，格式为 `{"type": "knowledge", "id": "kb-xxx"}` 或 `{"type": "connector", "id": "conn-xxx"}`；
- `memory_id`：可选，关联 Memory 实例 ID，用于跨会话[长期记忆](../concepts/long-term-memory.md)检索；
- `session_id`：推荐传入，用于会话状态追踪与调试，未提供时平台自动生成；
- `enable_sandbox`：布尔值，仅 Managed Agent 支持，设为 `true` 时自动启用 Sandbox 执行环境。

## 使用方式

1. **控制台快速体验**：访问 [体验 Agent](https://bailian.console.aliyun.com/cn-beijing/playground?agent=template_01M4QREF0RGXZVYRF49DQMSBJ8)，选择模板后直接对话生成 Agent，适用于原型验证；
2. **API 集成**：调用 `/v1/agents/{agent_id}/chat` 接口（见 [raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)），需提前在控制台创建 Agent 并获取 `agent_id`；
3. **上下文扩展**：通过 RAG、Memory 或 Connector 模块增强 Agent 能力，各模块均需独立创建资源并绑定至 Agent 实例。

## 限制和注意事项

- 单次请求最大 token 数受所选 `model_id` 限制，且 `tools` 声明数量上限为 10 个；
- Sandbox 环境默认超时 30 秒，不支持持久化存储或后台进程；
- Flow Agent 不支持直接通过 `/chat` API 调用，必须使用 `/v1/flows/{flow_id}/run` 接口；
- 所有 Agent 默认开启内容安全检测（含输入/输出），若需关闭需在 Security 模块中显式配置策略，详见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中的 Security 小节。

## 来源文档

- [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)


