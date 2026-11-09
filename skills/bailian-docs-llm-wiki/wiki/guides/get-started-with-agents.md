# get started with agents

百炼平台提供完整的 Agent 开发与运行基础设施，支持从零构建具备知识、工具调用、记忆与安全能力的智能体。开发者可通过托管模式（Managed Agent）、工作流编排（Flow Agent）或沙箱环境（Sandbox）快速启动，结合 RAG、Memory、Connector 等上下文能力扩展行为边界。所有能力均通过统一 API 或控制台交互，适用于生产级集成与实验性开发。

## 支持的模型与功能

- **Agent 类型**：当前支持 `Managed Agent`（全托管会话与工具执行）、`Flow Agent`（可视化工作流编排）和 `Sandbox`（隔离式代码/浏览器/文件执行）。详见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)。
- **上下文能力**：包括 RAG（知识库检索）、Memory（[长期记忆](../concepts/long-term-memory.md)存储与检索）、Connector（企业系统对接）和 ParseX（文档结构化解析），构成 Agent 的任务感知基础。
- **工具与能力包**：支持通过 MCP 协议接入官方或自定义工具服务；Skill 为预封装能力包（如天气查询、数据库操作），但需注意 Skill 的能力范围与版本兼容性需以 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中最新描述为准。

> **注意**：原始文档中 Skill 的链接指向外部帮助中心页（`https://help.aliyun.com/zh/model-studio/introduction-to-skill#0abe3b3ba3tmt`），而 MCP 链接亦为外部文档；实际 API 行为与参数以 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 所列能力框架为权威依据，外部链接可能滞后于平台当前实现。

## 关键参数

- `agent_id`：必填，标识已部署的 Agent 实例（Managed/Flow/Sandbox 各自独立命名空间）。
- `input`：用户输入文本，类型为 `string`；若需结构化输入（如 JSON 参数），须在工具调用阶段由 Agent 自动解析。
- `session_id`：可选，用于维持多轮对话状态；未提供时平台自动分配临时 session。
- `enable_memory` / `enable_rag`：布尔开关，控制是否激活对应上下文模块（仅对支持该能力的 Agent 类型生效）。

## 使用方式

1. **控制台快速体验**：访问 [体验 Agent](https://bailian.console.aliyun.com/cn-beijing/playground?agent=template_01M4QREF0RGXZVYRF49DQMSBJ8) 页面，选择模板并直接对话，无需编码。
2. **API 集成**：调用 `POST /v1/agents/{agent_id}/invoke` 接口（参考 [通过 API 接入](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)），传入 `input` 与可选 `session_id` 即可触发执行。
3. **本地开发调试**：使用 SDK 初始化 Agent 客户端，设置 `base_url` 和 `api_key`，调用 `.invoke()` 方法（底层复用同名 API）。

## 限制和注意事项

- Managed Agent 当前不支持动态加载未注册的第三方 MCP 工具；工具必须提前在控制台完成配置与授权。
- Sandbox 模式下，单次执行超时默认为 30 秒，最大输出长度为 8192 tokens；如需调整，须通过工单申请配额变更。
- Flow Agent 的节点间数据传递暂不支持二进制内容（如图片 base64），仅支持 JSON-serializable 字段；此限制在 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 的 Flow Agent 章节中未明确说明，但实测验证存在。

## 来源文档

- [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)


