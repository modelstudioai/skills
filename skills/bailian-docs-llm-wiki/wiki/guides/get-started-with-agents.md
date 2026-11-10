# get started with agents

百炼 Agent 服务提供一套可组合、可扩展的智能体构建与运行能力，支持从快速体验到生产级 API 集成的全链路开发。开发者可通过托管模式（Managed Agent）、工作流编排（Flow Agent）或沙箱环境（Sandbox）启动 Agent，并按需接入知识、记忆、工具与安全治理能力。所有能力均基于统一上下文抽象和标准化接口设计。

## 支持的模型与功能

Agent 服务本身不绑定特定大模型，而是通过 `model_id` 参数动态指定底层 LLM（如 `qwen-max`、`qwen-plus` 等），实际可用模型以 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中“开始构建”章节所列控制台默认选项为准。核心功能模块包括：

- **运行时类型**：`managed`（托管会话与工具执行）、`flow`（可视化工作流编排）、`sandbox`（隔离式代码/浏览器/文件执行）  
- **上下文扩展**：RAG（知识库检索）、Memory（[长期记忆](../concepts/long-term-memory.md)管理）、Connector（企业系统对接）、ParseX（多格式文档结构化解析）  
- **能力接入**：MCP（Model Context Protocol 工具协议）、Skill（预置能力包，如天气、翻译、数据库查询等）  

> **注意**：[Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中将 MCP 链接指向外部 help.aliyun.com 文档，但当前平台已统一要求使用 `mcp-server` 标准化注册方式；请以 [Managed Agent 快速开始](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using/managed-agents-quick-start.md) 中的 MCP 配置示例为准，避免直接复用旧版 HTTP [工具调用](../concepts/tool-calling.md)方式。

## 关键参数

创建或调用 Agent 时需关注以下必需/常用参数（以 Managed Agent API 为例）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 底层推理模型 ID，须为平台已开通的模型（见控制台「模型管理」） |
| `agent_type` | string | 是 | 取值为 `managed` / `flow` / `sandbox` |
| `tools` | array | 否 | 工具列表，每个元素含 `tool_id` 和可选 `config`；MCP 工具需提前在平台注册 |
| `knowledge_config` | object | 否 | 指定 RAG 知识库 ID 与检索参数（`top_k`, `score_threshold`） |
| `memory_config` | object | 否 | 启用[长期记忆](../concepts/long-term-memory.md)时配置 `memory_id` 与 `enable_history` |

完整参数定义请参考 [Managed Agents API 概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 使用方式

1. **快速体验**：访问 [体验 Agent](https://bailian.console.aliyun.com/cn-beijing/playground?agent=template_01M4QREF0RGXZVYRF49DQMSBJ8) 控制台 Playground，选择模板后直接对话调试；  
2. **低代码构建**：使用 Flow Agent 可视化画布编排节点（LLM、工具、条件分支等），详见 [Flow Agent 入门](../../raw/application-user-guide/llm-application/llm-application-start-using/flow-agent-introduction.md)；  
3. **API 集成**：调用 `/v1/agents/{agent_id}/chat` 接口发起会话，请求体需包含 `messages` 和上述关键参数，认证方式为 Bearer [Token](../concepts/token.md)（AccessKey）。

## 限制和注意事项

- 单次会话最大上下文长度受所选 `model_id` 限制（例如 `qwen-turbo` 为 8K tokens），超出部分将被截断；  
- Sandbox 模式下 Python 执行超时默认为 30 秒，不可修改；浏览器操作仅支持 Chromium 内核，且不支持跨域 Cookie 持久化；  
- RAG 检索结果默认最多返回 5 片段，如需更多需显式设置 `top_k > 5` 并确保知识库已启用高精度向量索引；  
- 所有 Agent 实例共享账户级调用配额，高频调用需申请提升 QPS 限额——具体策略参见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中“治理与进化”章节。

## 来源文档

- [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)


