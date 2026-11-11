# get started with agents

Agent 是百炼平台提供的智能体运行与编排能力，支持开发者快速构建具备知识、工具调用、记忆和安全治理能力的可执行智能体。本文档面向开发者，梳理核心能力边界、关键配置项及接入路径，帮助你基于业务场景选择合适的技术路径。所有功能均需通过百炼控制台或 API 调用，不支持本地独立部署。

## 支持的模型与功能类型

百炼 Agent 服务不绑定特定大模型，而是以**运行时抽象层**方式支持多种 Agent 架构模式，包括：

- **Managed Agent**：托管会话生命周期、工具执行与环境隔离，适合通用对话型智能体；详见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)  
- **Flow Agent**：基于可视化工作流编排多步骤任务，支持条件分支与并行调用；其设计范式在 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中有明确分类说明  
- **Sandbox**：提供代码解释器、浏览器自动化与文件沙箱执行环境，用于高风险操作隔离  

上下文能力方面，RAG、Memory、Connector 和 ParseX 均作为可插拔模块集成，无需修改 Agent 核心逻辑即可启用。其中 RAG 与 Memory 的初始化配置直接影响首次响应质量，建议在创建 Agent 前完成知识库或记忆库预加载。

## 关键参数

调用 Agent 时需显式指定以下参数（以 Managed Agent API 为例）：

- `agent_id`：必填，Agent 实例唯一标识（控制台创建后生成）  
- `input`：必填，用户输入文本或结构化消息（如 `{"text": "查订单状态", "order_id": "ORD123"}`）  
- `session_id`：推荐填写，用于跨请求维持会话上下文；若为空则每次请求视为新会话  
- `enable_memory`：布尔值，默认 `false`；设为 `true` 时自动启用已绑定的 Memory 模块  
- `tools`：数组，仅 Flow Agent 和 Sandbox 支持显式覆盖工具列表；Managed Agent 工具由后台配置决定，此字段将被忽略  

> **注意**：原始文档中 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 将 MCP 与 Skill 并列列为“工具与能力包”，但实际 API 层面，MCP 工具需通过 `tools` 参数注册，而 Skill 是预置能力包（如“天气查询”“日程管理”），不可动态增删——二者接入方式不同，开发者应按能力来源选择对应机制。

## 使用方式

### 控制台快速体验  
访问 [体验 Agent](https://bailian.console.aliyun.com/cn-beijing/playground?agent=template_01M4QREF0RGXZVYRF49DQMSBJ8) 页面，选择模板后直接对话，无需编码。该路径适用于原型验证与非生产场景。

### API 接入（推荐生产使用）  
调用 `POST /v1/agents/{agent_id}/chat` 接口（参考 [Managed Agent API 概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)）。需提前完成：
- 在控制台创建 Agent 并获取 `agent_id`  
- 配置所需上下文（如绑定知识库、开启 Memory）  
- 若需工具调用，确保已通过 MCP 或 Connector 完成工具注册  

Flow Agent 和 Sandbox 有独立 API 路径，不可混用 Managed Agent 接口。

## 限制和注意事项

- 单次请求最大输入长度为 32,768 token（含系统提示词与上下文），超长内容将被截断，不触发自动分块处理  
- Sandbox 环境默认超时 30 秒，复杂计算或网络请求需主动优化逻辑或申请配额提升  
- Memory 模块当前仅支持 key-value 形式[长期记忆](../concepts/long-term-memory.md)，不支持向量检索；如需语义检索，请使用 RAG 模块替代  
- 所有 Agent 实例均运行于阿里云百炼专属 VPC 内，无法直连公网未备案域名；外部系统对接必须通过 Connector 配置白名单或使用内网 SLB  

> **注意**：[Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 提到“Sandbox 支持浏览器操作”，但截至 v2024.07 版本，浏览器自动化能力仍处于灰度阶段，仅对白名单账号开放，正式商用前请确认控制台中该能力开关是否可用。

## 来源文档

- [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)


