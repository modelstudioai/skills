# get started with agents

百炼平台的 Agent 服务提供端到端的智能体开发与运行能力，支持从零构建具备知识、工具调用、记忆和安全治理能力的生产级 Agent。开发者可按需组合托管环境（Managed Agent）、工作流编排（Flow Agent）或沙箱执行（Sandbox），并灵活接入 RAG、Memory、Connector 等上下文模块。所有能力均通过统一 API 或控制台快速启用，详见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)。

## 支持的模型与功能

- **核心运行时**：`Managed Agent`（全托管会话与工具执行）、`Flow Agent`（LLM 驱动的工作流编排）、`Sandbox`（隔离式代码/浏览器/文件执行）  
- **上下文扩展**：`RAG`（知识库检索）、`Memory`（[长期记忆](../concepts/long-term-memory.md)存储与检索）、`Connector`（企业系统对接）、`ParseX`（多格式文档结构化解析）  
- **能力接入层**：`MCP`（Model Context Protocol，支持官方及第三方工具注册）、`Skill`（预封装能力包，如天气查询、数据库操作等）  
- **治理模块**：`Evolution`（基于真实对话的评测与迭代优化）、`Security`（内容过滤、运行时沙箱防护、供应链风险扫描）  

完整能力矩阵与适用场景请参考 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)。

## 关键参数

调用 Agent 时需明确以下关键参数（以 Managed Agent API 为例）：

- `agent_id`：Agent 唯一标识（控制台创建后分配，或通过 `/agents` 列表获取）  
- `input`：用户输入文本，类型为 `string`；若需结构化输入（如 JSON 表单），须在 Skill 或 Flow Agent 中明确定义 schema  
- `session_id`（可选）：用于维持多轮会话状态；未提供时平台自动创建新会话  
- `parameters`（可选）：透传至底层模型或工具的配置，例如 `{"temperature": 0.3, "max_tokens": 1024}`  
- `enable_memory`（布尔，默认 `false`）：仅当 Agent 已绑定 Memory 模块时生效；启用后自动读写[长期记忆](../concepts/long-term-memory.md)  

> **注意**：`parameters` 中的 `top_p` 和 `frequency_penalty` 在 Sandbox 模式下被忽略，该限制已在 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 的 Sandbox 小节中明确说明，但部分旧版 SDK 文档未同步更新。

## 使用方式

1. **控制台快速体验**：访问 [体验 Agent](https://bailian.console.aliyun.com/cn-beijing/playground?agent=template_01M4QREF0RGXZVYRF49DQMSBJ8) 页面，选择模板并直接对话调试  
2. **API 集成**：调用 `POST /v1/agents/{agent_id}/chat`（Managed Agent）或 `POST /v1/flows/{flow_id}/run`（Flow Agent），认证使用阿里云 STS Token 或 AccessKey  
3. **本地开发联调**：通过 `bailian-cli` 工具加载本地 Skill 或 MCP Server，运行 `bailian agent run --local` 启动沙箱调试环境  

详细接口定义与示例见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中的“通过 API 接入”章节及配套 API 文档。

## 限制和注意事项

- 单次请求最大 `input` 长度为 32768 字符；超出将返回 `400 Bad Request`  
- Sandbox 模式下禁止执行 `fork()`、`execve()` 等系统调用，且网络请求仅允许白名单域名（默认含 `api.bailian.aliyuncs.com`）  
- Memory 模块默认保留最近 100 条交互记录，历史数据不支持手动清理（需通过 Evolution 模块导出后批量删除）  
- Flow Agent 的循环节点（Loop Node）最大嵌套深度为 5，超限将终止执行并返回错误码 `FLOW_LOOP_DEPTH_EXCEEDED`  

以上约束均已在 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 的各子模块 Quick Start 文档中验证一致。

## 来源文档

- [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)


