# 应用构建框架对比：Managed Agents、Application Components 与 Model Context Protocol

为帮助开发者在百炼平台上高效选型，本文系统对比三种核心应用构建范式：**Managed Agents（托管智能体）**、**Application Components（应用组件）** 和 **Model Context Protocol（[模型上下文协议](../concepts/mcp.md)，MCP）**。三者定位不同——Managed Agents 面向**全生命周期可管理的生产级智能体应用**；Application Components 提供**轻量、标准化、即插即用的能力调用接口**；MCP 则聚焦于**大模型与外部工具之间的安全、协议化、可扩展连接机制**。理解其差异对架构设计、成本控制与运维复杂度至关重要。

---

## 关键维度对比表

| 维度 | Managed Agents | Application Components | Model Context Protocol (MCP) |
|------|----------------|--------------------------|------------------------------|
| **核心定位** | 托管式智能体运行时：提供带状态、带记忆、多会话、可编排的完整 Agent 生命周期管理 | 标准化能力调用接口：面向对话生成、RAG、工具执行等原子能力的 RESTful 封装 | 工具接入协议层：定义大模型与外部服务（地图、数据库、API 等）之间安全、声明式、流式交互的标准通信机制 |
| **输入格式** | `POST /v1/agents/{id}/chat`，支持结构化 `messages` + `files`（需预上传）、`session_id`、`memory_store_id`；支持 system/user/assistant 角色 | OpenAI 兼容格式：`input.messages` 数组（仅支持 `system`/`user`/`assistant`），`model` 字段必填；支持 `enable_search` 等能力开关 | **不直接接收用户请求**；由上层（Agent 或 Workflow）根据提示词决策后，以 `tool_calls` 形式发起调用；输入由 MCP Server 的 `inputSchema` 定义，模型按 Schema 生成参数 |
| **输出格式** | 同步 JSON 或 SSE 流式响应（含 `delta`、`event`、`memory_update` 等事件）；支持返回结构化 memory 变更与 tool execution trace | 同步 JSON 或 SSE 流式响应（`text-generation` 类型）；输出为纯文本或结构化 `choices[].message`；无原生 memory/event 语义 | **不直接生成最终用户响应**；输出为工具执行结果（JSON），作为上下文注入模型后续推理；支持 Streamable HTTP（`/mcp`）或 SSE（`/sse`）两种协议 |
| **支持模型** | 仅限百炼托管 Qwen 系列：`qwen-max`、`qwen-plus`、`qwen-turbo`；**不支持自定义模型或外部模型接入** | 支持同上 Qwen 系列模型；`model` 参数显式指定；**不支持自定义模型别名或 BYOM（Bring Your Own Model）** | **不绑定任何模型**；作为协议层运行于智能体/工作流之上；可被任意兼容 MCP 的模型（包括未来接入的非 Qwen 模型）调用 |
| **API 端点** | `/v1/agents`（创建）、`/v1/agents/{id}/chat`（调用）、`/v1/sessions/{id}/events`（追踪）、`/v1/memory-stores/{id}/entries`（读写） | 统一服务端点（如 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`），按能力类型路由（`text-generation`/`retrieval`/`tool-execution`） | 无统一 API 端点；MCP Server 自行暴露 `/mcp`（Streamable HTTP）或 `/sse`；百炼平台内通过智能体/工作流配置自动代理调用 |
| **计费方式** | 按 **Agent 实例 + Session 调用 + Memory Store 容量 + 文件存储时长** 多维计费；Memory Store 默认 1MB/7天，扩容另计；文件上传后 24 小时有效 | 按 **调用次数 + 输入/输出 Token** 计费；QPS 受应用级配额限制（默认 5 QPS），超限返回 `429`；无内存/会话持久化费用 | 按 **MCP 服务部署模式 + 调用时长 + 调用次数** 计费：<br>• 基础模式：0.000156 元/秒（仅调用时计费）<br>• 极速模式：0.000156 元/秒（调用）+ 0.000036 元/秒（常驻部署）<br>• 云服务调用额外产生模型 Token 成本 |
| **典型场景** | 客服机器人（需[长期记忆](../concepts/memory.md)用户偏好）、自动化投研助手（多文档分析+代码执行+历史回溯）、合规审计 Agent（Vault 加密凭证+事件留痕） | 快速集成聊天界面、知识库问答卡片、批量文本生成任务、低延迟工具调用（如单次搜索） | 天气查询联动地图展示、数据库查询后自动生成图表、多步骤工作流中跨系统数据协同（如“查订单 → 调物流 → 发短信”） |
| **状态管理能力** | ✅ 原生支持：Session 级上下文隔离、Memory Store 持久化（TTL 可设）、事件驱动 Webhook | ❌ 无内置状态：每次请求为无状态调用；需业务侧自行维护 session history 或 memory | ❌ 无状态协议：仅传递工具输入/输出；状态管理由上层 Agent 或 Workflow 承担 |
| **工具调用方式** | 内置 Skill（WebSearch/CodeInterpreter）+ Vault 凭据安全调用；支持自定义函数（需通过 Application Components 或 MCP 接入） | 支持预置工具链（如网页搜索）及控制台注册的 Plugin；调用逻辑由平台封装，开发者不可见底层协议 | ✅ 协议标准：通过 `tool.name` + `inputSchema` 声明式调用；支持官方服务、第三方服务、自定义服务（FC/网关/OpenAPI）；强调安全沙箱与权限隔离 |
| **扩展性与定制深度** | 中：可通过 Environment 隔离、Vault 管理密钥、Skill 编排扩展，但模型与工具链封闭 | 低：能力边界由平台预置接口定义；Plugin 注册需控制台配置，不支持动态加载 | 高：支持任意符合 MCP 协议的服务接入（Python/Node.js/HTTP）；可封装私有 API、阿里云产品、本地服务（需公网可达） |

---

## 适用场景建议

### ✅ 选择 **Managed Agents** 当：
- 需要构建**具备[长期记忆](../concepts/memory.md)、多轮会话、状态追踪与安全审计能力**的生产级智能体；
- 业务逻辑复杂，涉及**多工具协同、环境隔离、敏感凭证管理（如数据库密码）及事件溯源**；
- 团队希望**减少基础设施运维**，专注业务编排（如用可视化编辑器配置 Skill 流程）；
- 对 **SLA、可观测性（Events/Memory 日志）、合规性（Vault/KMS 集成）有明确要求**。

> ⚠️ 注意：不适合简单单次调用、对模型选择自由度要求高、或需 BYOM 的场景。

---

### ✅ 选择 **Application Components** 当：
- 需要**快速、低成本接入标准化 AI 能力**（如对话、RAG、搜索），且无需维护会话状态；
- 架构已存在成熟会话管理（如前端维护 conversation ID），只需后端提供“能力黑盒”；
- 追求**最低接入门槛与最简依赖**，适合作为微服务中的 AI 能力模块；
- 调用量稳定、QPS 可控，且能接受平台统一的模型与参数约束。

> ⚠️ 注意：不适合需要跨请求共享上下文、自定义工具链或深度调试模型行为的场景。

---

### ✅ 选择 **Model Context Protocol (MCP)** 当：
- 需要**安全、标准化地接入多个异构外部系统**（如地图、ERP、内部数据库），并希望模型能自主决策调用时机与参数；
- 构建**复杂工作流或智能体**，其中工具调用是核心环节（如“解析意图 → 查询库存 → 生成报价单 → 发送邮件”）；
- 团队具备一定工程能力，愿意**封装自有服务为 MCP Server**（FC 函数/网关代理），实现能力复用；
- 重视**协议开放性与未来兼容性**（如计划接入非 Qwen 模型，或与 Cherry Studio/Cursor 等 IDE 工具集成）。

> ⚠️ 注意：MCP 是**协议层，不可单独使用**；必须与 Managed Agents 或 Workflow 结合；不适用于纯文本生成类需求。

---

## 技术选型参考（面向开发者）

| 你的需求 | 推荐方案 | 理由 |
|----------|-----------|------|
| “我要做一个客服机器人，记住用户上次投诉的订单号，并自动关联历史工单” | ✅ **Managed Agents** | 原生 Session + Memory Store + Vault 凭据调用工单系统，开箱即用 |
| “我在现有 Web 应用里加一个‘智能问答’按钮，后端调用知识库回答用户问题” | ✅ **Application Components** | 直接调用 `/text-generation` + `enable_search=true`，5 行代码集成，无状态友好 |
| “我需要让大模型调用公司内部的 CRM API 查询客户信息，并把结果渲染到前端表格” | ✅ **MCP + Managed Agents** | 将 CRM API 封装为 MCP Server（FC 函数），在 Agent 中启用该 MCP 服务；模型自动决定何时调用、传什么参数 |
| “我有自研的小模型，想在百炼上测试它和工具的配合效果” | ❌ 三者均不支持 → 建议使用 **DashScope [OpenAI 兼容接口](../concepts/openai-compatible-api.md)** | Managed Agents 与 Application Components 均限定 Qwen 系列；MCP 协议虽开放，但当前仅支持在百炼托管 Agent/Workflow 中调用，不支持 BYOM 直接透传 |
| “我需要每秒处理 1000 次独立的文本摘要请求，低延迟、高并发” | ✅ **Application Components**（配额调至 100+ QPS） | 无状态、轻量、直连模型，比启动 Agent Session 更高效；避免 Session 初始化开销 |

> 💡 **组合使用提示**：  
> - 最佳实践常为 **Managed Agents（主干） + MCP（工具层） + Application Components（备用能力）** 三层架构；  
> - 例如：Agent 负责会话管理与流程控制 → MCP 接入地图/天气等动态服务 → Application Components 作为兜底 RAG 或文本生成模块；  
> - 所有方案均支持流式响应（SSE），但 **MCP 的流式需通过 `/mcp` 协议实现，而非直接返回给终端用户**。

---  
*本文档基于百炼平台 2024 年 Q3 版本功能编写。API 行为、计费策略与限制条款请以控制台实时说明及最新版官方文档为准。*

## 被对比主题页

- [managed agents api](../api/managed-agents-api.md)
- [application component api reference](../api/application-component-api-reference.md)
- [model context protocol](../guides/model-context-protocol.md)


