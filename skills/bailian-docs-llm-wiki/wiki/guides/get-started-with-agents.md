# get started with agents

Agent 是百炼平台提供的可编程智能体运行与编排服务，支持开发者快速构建具备知识、工具调用和上下文感知能力的 AI 应用。你可通过托管模式（Managed Agent）、工作流编排（Flow Agent）或沙箱环境（Sandbox）启动 Agent，并按需集成 RAG、Memory、Connector 等上下文能力及 MCP/Skill 工具包。所有能力均通过统一 API 或控制台交互接入，适用于生产级集成与实验性开发。

## 支持的模型与功能

- **运行模式**：支持 `Managed Agent`（全托管会话与工具执行）、`Flow Agent`（可视化工作流编排）和 `Sandbox`（隔离式代码/浏览器/文件执行）。详见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)。
- **上下文能力**：包括 RAG（知识库检索）、Memory（[长期记忆](../concepts/long-term-memory.md)管理）、Connector（企业系统对接）和 ParseX（文档结构化解析），均提供开箱即用的 Quick Start 文档。
- **工具与能力扩展**：通过 MCP 协议接入官方或自定义工具服务；通过 Skill 能力包快速添加预置功能（如天气查询、数据库操作等）。注意：[Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中 Skill 的链接指向外部帮助中心，其内容与当前平台 UI 存在版本差异，建议以控制台实际可用 Skill 列表为准。

## 关键参数

- `agent_id`：必需，Agent 实例唯一标识（由平台分配或用户指定）。
- `input`：必需，用户输入文本或结构化 payload（如 JSON 对象）。
- `session_id`：推荐传入，用于会话状态追踪（尤其在 Managed Agent 模式下）。
- `enable_memory` / `enable_rag`：布尔型开关，控制是否启用对应上下文能力（默认 `false`）。
- `tool_choice`：指定工具调用策略（`auto`、`none` 或显式工具名），仅对支持 MCP 的 Agent 生效。详细参数说明见 [Managed Agent API 概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 使用方式

1. **控制台快速体验**：访问 [体验 Agent](https://bailian.console.aliyun.com/cn-beijing/playground?agent=template_01M4QREF0RGXZVYRF49DQMSBJ8) 页面，选择模板并对话生成首个 Agent。
2. **API 集成**：调用 `POST /v1/agents/{agent_id}/run` 接口（参考 [Managed Agent API 概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)），传入必要参数即可触发执行。
3. **本地开发调试**：使用 SDK 初始化 Agent 客户端，设置 `base_url` 和 `api_key` 后调用 `.run()` 方法。各语言 SDK 示例同步更新于对应 Quick Start 文档中，例如 [Sandbox 快速开始](../../raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-quick-start.md)。

## 限制和注意事项

- 单次请求最大 `input` 长度为 32768 字符；输出受模型 token 限制（如 Qwen-Max 默认 8192 output tokens）。
- Sandbox 模式下不支持持久化文件写入，临时文件在会话结束后自动清理。
- > **注意**：原始文档中 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 将 Flow Agent 归类为“LLM Application”，但最新控制台已将其统一纳入 Agent 一级分类，API 路径与权限模型均与 Managed Agent 对齐，请以 `/v1/agents/...` 前缀为准，勿沿用旧版 `/v1/llm-apps/...` 路径。
- MCP 工具调用需确保工具服务已注册且健康检查通过；未配置 `tool_choice` 时，Agent 可能拒绝调用任何工具（取决于底层 LLM 的 tool-calling 行为）。

## 来源文档

- [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)


