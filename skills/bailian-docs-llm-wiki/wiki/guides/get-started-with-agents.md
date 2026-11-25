# get started with agents

百炼平台的 Agent 服务提供端到端的智能体开发与运行能力，支持从快速体验、低代码编排到高自由度 API 集成的多种路径。开发者可按需组合上下文（RAG、Memory、Connector）、工具（MCP、Skill）与执行环境（Managed Agent、Flow Agent、Sandbox），并借助 Evolution 和 Security 模块实现可观测性与安全治理。所有能力均通过统一控制台与标准化 API 暴露，详见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)。

## 支持的模型与核心功能

Agent 服务本身不绑定特定大模型，而是以“能力抽象层”方式解耦模型调用：Managed Agent 和 Flow Agent 默认支持 Qwen 系列（如 qwen-max、qwen-plus），同时允许用户在创建时指定任意已接入百炼的 LLM 模型；Sandbox 环境则独立于模型，专注安全执行代码/浏览器/文件操作。上下文模块中，RAG 依赖向量引擎（默认 DashVector），Memory 使用专用持久化存储，Connector 支持 HTTP、数据库、飞书/钉钉等标准协议接入。完整能力矩阵见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)。

## 关键参数

- `agent_id`：Agent 唯一标识，由控制台创建或 API 返回，用于后续调用（如 `/v1/agents/{agent_id}/chat`）  
- `session_id`：会话级状态隔离标识，建议业务侧生成 UUID，不复用以避免上下文污染  
- `enable_memory`：布尔值，启用后自动关联 Memory 模块（需提前配置 Memory 实例）  
- `tools`：显式声明 MCP 工具列表（格式为 `[{ "tool_id": "xxx", "version": "1.0" }]`），未声明则仅使用内置基础工具  
- `max_iterations`：Flow Agent 中工作流最大执行步数，默认 15，超限将终止并返回 `error: iteration_limit_exceeded`  

> **注意**：文档中 `tools` 参数在 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 的 MCP 描述部分未明确字段结构，但实际 API 要求必须为对象数组且含 `tool_id`；请以 [Managed Agents API 概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中的 OpenAPI Schema 为准。

## 使用方式

1. **快速体验**：访问控制台 Playground（[体验 Agent](https://bailian.console.aliyun.com/cn-beijing/playground?agent=template_01M4QREF0RGXZVYRF49DQMSBJ8)），选择模板 Agent 直接对话，无需编码  
2. **低代码构建**：使用 Flow Agent 可视化画布编排节点（LLM、RAG、Tool Call、条件分支），保存后自动生成可调用 `agent_id`  
3. **API 集成**：调用 `POST /v1/agents/{agent_id}/chat`，传入 `messages` 数组与上述关键参数；请求头需携带 `Authorization: Bearer <access_token>`。详细接口定义见 [Managed Agents API 概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)  

## 限制和注意事项

- 单次请求 `messages` 总 tokens 不得超过模型 context length（如 qwen-max 为 32768），超长将被截断且不报错  
- Sandbox 环境默认禁止外网访问（`network: false`），如需调用外部 API，须在创建时显式开启 `network: true` 并配置白名单域名  
- Memory 模块的长期记忆检索默认仅匹配当前 `session_id`，跨会话共享需主动调用 `/v1/memory/{memory_id}/search` 并合并结果  
- 所有 Agent 调用均受账号级 QPS 与并发数配额限制，超出将返回 `429 Too Many Requests`；具体配额请查阅控制台「配额管理」，或参考 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中的治理章节

## 来源文档

- [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)


