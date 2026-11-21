# get started with agents

百炼平台的 Agent 服务提供一套可组合、可扩展的智能体构建与运行框架，支持从零快速启动托管型、流程编排型或沙箱隔离型 Agent 应用。开发者可通过声明式配置或 API 集成方式接入知识、工具、记忆与安全能力，无需从底层模型训练开始。所有核心能力均围绕生产级部署设计，兼顾灵活性与可观测性。

## 支持的模型与功能

Agent 服务本身不绑定特定大模型，而是通过 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中定义的抽象层（如 `Managed Agent`、`Flow Agent` 和 `Sandbox`）解耦模型调用与执行逻辑。实际运行时，底层默认使用百炼平台托管的 Qwen 系列模型（如 `qwen-max`、`qwen-plus`），但支持通过 `model_id` 参数显式指定兼容的百炼模型。知识增强能力（RAG）、[长期记忆](../concepts/long-term-memory.md)（Memory）、企业系统连接（Connector）和文档解析（ParseX）均为即插即用模块，其行为由对应上下文组件独立控制，详见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)。

> **注意**：原始文档中 `MCP` 和 `Skill` 的链接指向外部帮助中心页面（非 `raw/` 路径），且未说明其是否已整合进当前 Agent 运行时。根据 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 的结构，二者属于“工具与能力包”分类，但实际 API 层暂未暴露统一的 `mcp_server_url` 或 `skill_id` 字段——建议优先使用 `tools` 数组传入标准 ToolSpec，避免依赖未同步更新的文档描述。

## 关键参数

创建或调用 Agent 时，以下参数在多数场景下必需或强推荐：

- `agent_id`：Agent 实例唯一标识（托管型 Agent 必填；Flow Agent 可选，若为空则按 flow 定义动态生成）
- `model_id`：指定底层 LLM（例如 `"qwen-max"`），必须为百炼平台已开通的模型 ID
- `tools`：JSON 数组，每个元素为符合 OpenAI Tool Specification 的工具定义（非 MCP 协议直连）
- `knowledge_config`：启用 RAG 时配置知识库 ID 与检索参数（参见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中 RAG 模块说明）
- `session_id`：用于会话状态追踪（Managed Agent 强依赖，Sandbox 中可选）

## 使用方式

1. **快速体验**：访问控制台 Playground，选择预置模板直接对话调试 —— 入口见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中的“体验 Agent”链接  
2. **API 集成**：调用 `POST /agents/{agent_id}/chat`（托管型）或 `POST /flows/{flow_id}/run`（流程型），请求体需包含 `messages` 和上述关键参数  
3. **本地开发**：使用 `@alibaba/bailian-sdk` v2.3+，初始化 `AgentClient` 后调用 `.chat()` 方法，自动处理流式响应与 tool call 回调  

## 限制和注意事项

- 托管型 Agent 单次会话最大上下文长度为 32k tokens（含 system prompt、历史消息、tool results），超长输入将被截断  
- Sandbox 模式下不支持任意外部网络请求（仅允许白名单域名及百炼内置 connector），且文件上传大小上限为 50MB  
- `Memory` 模块的[长期记忆](../concepts/long-term-memory.md)写入需显式调用 `/memory/write` 接口，不会在普通 chat 调用中自动触发持久化  
- 所有 Agent 类型均不支持跨区域调用（如 cn-beijing 创建的 agent_id 不可在 cn-hangzhou 区域 API 中使用）

## 来源文档

- [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)


