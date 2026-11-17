# get started with agents

百炼 Agent 服务提供一套可组合、可扩展的智能体构建与运行能力，支持从快速体验到生产级 API 集成的全链路开发。开发者可通过托管模式（Managed Agent）、工作流编排（Flow Agent）或沙箱环境（Sandbox）启动 Agent，并按需接入知识、记忆、工具与安全治理能力。所有能力均基于统一上下文抽象和标准化接口设计。

## 支持的模型与功能

Agent 服务本身不绑定特定大模型，而是通过 `model_id` 参数动态指定底层 LLM（如 `qwen-max`、`qwen-plus` 等），实际可用模型以 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中“开始构建”章节所列控制台默认选项为准。核心功能模块包括：

- **运行时类型**：`managed`（托管会话与工具执行）、`flow`（可视化工作流编排）、`sandbox`（隔离式代码/浏览器/文件执行）  
- **上下文扩展**：RAG（知识库检索）、Memory（[长期记忆](../concepts/long-term-memory.md)管理）、Connector（企业系统对接）、ParseX（多格式文档结构化解析）  
- **能力接入**：MCP（Model Context Protocol 工具协议）、Skill（预置能力包，如天气、翻译、数据库查询等）  

> **注意**：文档中 MCP 链接指向外部 help.aliyun.com 页面，而 Skill 描述未说明是否支持自定义 Skill 注册；实际 API 层仅暴露 `mcp_server_urls` 参数用于 MCP 工具发现，自定义 Skill 需通过 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中提到的 Connector 或独立 Skill 服务部署实现。

## 关键参数

调用 Agent 时需在请求体中明确以下关键字段（以 Managed Agent 为例）：

- `model_id`: 指定底层大模型 ID，必须为平台当前支持的模型（参见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) “开始构建”部分控制台可用列表）  
- `agent_id`: Agent 实例唯一标识（创建后分配）  
- `input`: 用户输入文本，类型为 `string`  
- `parameters`: 可选，用于覆盖 Agent 创建时配置的超参（如 `temperature`、`max_tokens`）  
- `tools`: 显式声明启用的工具列表（如 `["rag", "memory", "mcp"]`），未声明则不加载对应能力  

## 使用方式

1. **快速体验**：访问控制台 Playground，选择模板 Agent 直接对话调试（链接见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)）  
2. **API 集成**：调用 `POST /v1/agents/{agent_id}/chat` 接口，传入 `model_id` 和 `input` 即可启动会话；完整请求示例与鉴权方式详见 [Managed Agents API 概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)  
3. **进阶开发**：  
   - 使用 Flow Agent 编排多步骤任务（参考 [Flow Agent 介绍](../../raw/application-user-guide/llm-application/llm-application-start-using/flow-agent-introduction.md)）  
   - 在 Sandbox 中安全执行 Python 代码或浏览器操作（参考 [Sandbox 快速开始](../../raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-quick-start.md)）

## 限制和注意事项

- 单次请求 `input` 长度上限为 32768 字符；超出将被截断且不报错  
- RAG 知识库仅支持已显式挂载至该 Agent 的知识源，未在创建时关联的知识库无法在运行时自动生效  
- Memory 模块默认启用但仅对同一 `session_id` 内的连续请求有效；跨会话记忆需自行实现持久化逻辑  
- MCP 工具调用依赖服务端可达性与协议兼容性，若 `mcp_server_urls` 中任一地址不可达，整个工具链将降级为不可用（无 fallback 机制）

## 来源文档

- [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)


