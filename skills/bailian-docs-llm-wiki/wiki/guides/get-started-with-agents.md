# get started with agents

百炼 Agent 服务提供一套可组合、可扩展的智能体构建与运行框架，支持从零快速启动托管型、流程编排型或沙箱隔离型 Agent。开发者可通过 API 或控制台接入，按需装配知识、工具、记忆与安全能力。本文档基于 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 整理核心实践路径。

## 支持的模型与功能

Agent 服务本身不绑定特定大模型，而是通过 `model_id` 参数动态指定后端 LLM（如 `qwen-max`、`qwen-plus` 等），并支持多模型协同调度。功能模块分为三类：
- **运行时类型**：`Managed Agent`（全托管会话与工具执行）、`Flow Agent`（可视化工作流编排）、`Sandbox`（代码/浏览器/文件的隔离执行环境）；
- **上下文增强**：`RAG`（知识库检索）、`Memory`（[长期记忆](../concepts/long-term-memory.md)存储与召回）、`Connector`（企业系统对接）、`ParseX`（PDF/Word 等文档结构化解析）；
- **能力扩展**：`MCP`（Model Context Protocol 工具协议，支持官方及自定义工具注册与调用）、`Skill`（预封装能力包，如“会议纪要生成”“SQL 查询助手”）。

> **注意**：[Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中将 `MCP` 链接指向外部 help.aliyun.com 文档，但实际平台内已统一为 `mcp_server` 配置项，建议以 [Managed Agent API 概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中的参数定义为准。

## 关键参数

调用 Agent 的核心参数（以 Managed Agent 为例）包括：
- `model_id`: 必填，指定推理模型 ID（如 `"qwen-max"`）；
- `agent_id`: 必填，Agent 实例唯一标识（控制台创建或 API 注册后获得）；
- `input`: 用户输入消息（字符串或结构化对象）；
- `session_id`: 可选，用于维持多轮对话状态；
- `tools`: 可选，显式声明启用的工具列表（如 `["web_search", "calculator"]`），若未指定则使用 Agent 默认配置；
- `enable_memory`: 布尔值，控制是否激活[长期记忆](../concepts/long-term-memory.md)（需已配置 Memory 实例）。

完整参数说明见 [Managed Agent API 概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 使用方式

1. **控制台快速体验**：访问 [体验 Agent](https://bailian.console.aliyun.com/cn-beijing/playground?agent=template_01M4QREF0RGXZVYRF49DQMSBJ8) 页面，选择模板一键部署并对话测试；
2. **API 集成**：调用 `/v1/agents/{agent_id}/chat` 接口（需携带 `Authorization` 和 `Content-Type: application/json`），请求体参考上述关键参数；
3. **本地开发调试**：使用 `bailian-sdk`（Python/JS）封装的 `AgentClient`，自动处理鉴权、重试与 session 管理，详见 [Managed Agent 快速开始](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using/managed-agents-quick-start.md)。

## 限制和注意事项

- 单次请求 `input` 长度上限为 32,768 tokens（含系统提示词与历史上下文），超长内容需前置截断或分块；
- `Sandbox` 模式下，代码执行默认超时 30 秒，不可修改；浏览器操作仅支持 Chromium 内核，且不支持跨域 Cookie 持久化；
- `Memory` 模块需单独开通配额并绑定 Agent 实例，未绑定时即使设置 `enable_memory=true` 也无效；
- 所有工具调用（含 `MCP` 和 `Skill`）均受账户级工具调用频次限制，超出后返回 `429 Too Many Requests`，具体阈值请查阅 [Agent 治理指南](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)。

## 来源文档

- [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)


