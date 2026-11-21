# Flow Agent、托管 Agent 与 OpenAI 兼容 Agent 接口对比

本文档面向百炼平台开发者，旨在清晰对比三种主流智能体调用方案的技术特性、能力边界与适用场景，帮助团队基于业务需求、工程成熟度和迁移成本做出高效技术选型。随着智能体应用从单步推理向多步骤编排、状态持久化与系统集成演进，百炼平台提供了分层抽象的 Agent 能力：**Flow Agent** 侧重确定性流程控制，**托管 Agent** 提供全生命周期自主管理，而 **OpenAI 兼容 Agent** 则聚焦生态平滑迁移。三者并非替代关系，而是覆盖不同抽象层级与协作范式的互补方案。

## 关键维度对比

| 维度 | Flow Agent | 托管 Agent | OpenAI 兼容 Agent |
|------|------------|-------------|---------------------|
| **核心定位** | 流程即服务（Workflow-as-a-Service）：将预定义、强结构化的多步骤任务封装为可编程 API | 托管式智能体平台（Managed Agent Platform）：提供环境、会话、记忆、技能等完整运行时基础设施 | 兼容性优先的智能体网关（OpenAI-Compatible Gateway）：复用 OpenAI SDK/生态，零改造接入百炼 Agent 能力 |
| **输入格式** | JSON 对象，严格匹配流程 Schema 的 `input` 字段（如 `{"order_id": "O123", "reason": "delay"}`）；不支持 message 数组 | RESTful 多阶段调用：需先创建 Agent → 启动 Session → 发送 `chat` 请求；消息体为 `{"message": "..."}` 格式，含元数据字段（如 `session_id`, `enable_memory`） | 完全兼容 OpenAI `chat.completions` 格式：`messages` 数组（含 `system`/`user`/`assistant`）、`tools`、`tool_choice` 等字段；支持 `stream: true` |
| **输出格式** | 同步模式：返回结构化结果对象（含 `status`, `output`, `steps` 执行轨迹）；异步模式：返回 `task_id`，需轮询 `/tasks/{id}` 获取最终 JSON 结果 | 分阶段响应：`/chat` 接口支持 SSE [流式输出](../concepts/streaming-output.md)（`event: message`, `event: tool_call`）或 JSON 块；最终响应含 `content`, `tool_calls`, `session_state`, `memory_summary` 等字段 | 100% 兼容 OpenAI 响应格式：非流式返回 `choices[0].message`；流式返回标准 `data: {...}` chunk；`tool_calls` 字段结构与 OpenAI 一致 |
| **支持模型** | 仅 `flow-agent-v1`（百炼自研流程专用模型），不兼容通用 LLM | `qwen-max`, `qwen-plus`, `qwen-turbo`（Qwen 系列托管模型），不支持用户自定义模型 | 仅 `qwen-plus`, `qwen-max`（v202408+ 版本），`qwen-turbo` 已下线；不支持第三方模型 |
| **API 端点** | `POST /v1/flows/{flow_id}/run`（单次触发）<br>`GET /v1/tasks/{task_id}`（异步轮询） | `POST /v1/agents`（创建）<br>`POST /v1/agents/{agent_id}/sessions`（启动会话）<br>`POST /v1/agents/{agent_id}/sessions/{session_id}/chat`（交互） | `POST https://dashscope.aliyuncs.com/api/v1/agents/chat/completions`（单一入口，OpenAI 风格） |
| **状态与记忆** | 依赖 `enable_session` + `memory_id` 显式开启；记忆 TTL 固定 7 天，不可配置；[长期记忆](../concepts/long-term-memory.md)为“旧版”机制 | 内置 Session 生命周期管理（自动创建/续期）；Memory Store 可配置容量（`memory_capacity`）与清理策略（LRU）；支持多 Memory Store 绑定 | 通过 `session_id` 自动维护上下文；Session 默认 TTL 24 小时，支持手动 `extend`；记忆由平台透明管理，开发者无感知 |
| **工具调用（Function Calling）** | 不直接支持 OpenAI 风格 `tools`；工具能力内嵌于流程节点（如“调用 CRM API”节点），由流程设计器配置 | 支持 Skill（可复用技能包）作为工具载体；通过 `tool_choice` 控制调用，支持 `"auto"`/`"none"`/指定 Skill 名；Skill 可关联 Vault、Webhook 等 | 原生支持 OpenAI `tools` + `tool_choice` 语法；工具 schema 必须为 OpenAI 标准格式（`type: "function"`）；调用结果自动注入后续消息流 |
| **计费方式** | 按「Flow 执行次数」计费；每次 `run` 调用计为 1 次，无论内部步骤多少 | 按「Agent 实例小时数」+「Session 调用次数」+「Memory 存储量」组合计费；Environment、Vault、Webhook 等资源单独计费 | 按「Agent 调用量」独立计费（计入百炼「Agent」配额池），与普通 LLM 调用 quota 分离；不按 token 或小时计费 |
| **典型场景** | 客服工单自动分派与闭环（输入工单ID→查库→路由→生成回复→更新状态）<br>数据清洗流水线（ETL 步骤编排）<br>合规审批工作流（多角色人工介入节点） | 企业级 AI 助手（如 HR 助手：查政策+填表+发邮件+同步钉钉）<br>自动化运维 Agent（监控告警→诊断→执行修复脚本→生成报告）<br>知识增强型销售顾问（实时检索 Vault + 调用 CRM） | 快速迁移现有 OpenAI 应用（如 LangChain / LlamaIndex 项目）<br>前端 SDK 直连 Agent（React/Vue App 使用 `openai` npm 包调用）<br>需要复用大量 OpenAI 生态工具链（如 AutoGen, CrewAI）的场景 |

## 适用场景建议

- **选择 Flow Agent 当：**  
  你的业务逻辑是**高度确定、步骤固定、强依赖外部系统集成**的流程（如订单履约、贷款审批）。你已通过百炼控制台完成可视化流程编排，并希望以轻量 HTTP 接口被 ERP、CRM 等后端系统调用。此时，你追求的是**可审计、可追踪、低代码交付**，而非自由对话能力。

- **选择托管 Agent 当：**  
  你需要构建一个**长期在线、具备自主记忆、能灵活切换工具与环境、需精细管控资源权限**的生产级 Agent（如 7×24 客服坐席、研发助手）。你愿意投入初期学习成本，以换取对 Environment 隔离、Memory Store 容量、Skill 版本、Webhook 重试策略等**全栈可控性**。这是百炼平台最完整、最“原生”的 Agent 能力。

- **选择 OpenAI 兼容 Agent 当：**  
  你的团队已在使用 OpenAI 生态（如 LangChain Agents、LlamaIndex Query Engine），或正快速验证 MVP，**要求最小化代码修改即可接入百炼 Agent 能力**。你接受在功能上做一定取舍（如不支持 `response_format`、无自定义 Memory TTL），以换取**开发效率与生态延续性**。这是最快落地、风险最低的迁移路径。

## 技术选型参考指南（致开发者）

| 你的关键诉求 | 推荐方案 | 理由说明 |
|--------------|----------|----------|
| **已有成熟 OpenAI 代码，想 1 小时内跑通百炼 Agent** | ✅ OpenAI 兼容 Agent | 替换 endpoint 和 API Key 即可，无需改逻辑；`tools` 参数开箱即用；LangChain `OpenAIAssistantAgent` 可直接复用 |
| **需要严格遵循 SOP，每一步操作都可回溯、可审批、可人工干预** | ✅ Flow Agent | 流程节点天然支持人工审核节点、条件分支、失败重试策略；输出含完整 `steps` 执行日志，满足审计要求 |
| **要构建一个带知识库、能调用多个内部 API、需区分不同部门数据权限的 AI 助手** | ✅ 托管 Agent | Environment 实现数据/工具沙箱隔离；Vault 支持部门级知识库挂载；Credential 管理密钥；Skill 封装标准化 API 调用，避免硬编码 |
| **预算敏感，且主要负载是短时、无状态的问答（如 FAQ 查询）** | ⚠️ 三者均非最优 | 此类场景应优先选用 `chat.completions`（普通 LLM 接口），成本更低、延迟更小；Agent 方案均引入额外状态管理开销 |
| **需要自定义模型（如微调后的 Qwen）或接入第三方模型（如 Claude）** | ❌ 三者均不支持 | 百炼当前所有 Agent 方案均限定于平台托管模型；如需自定义模型，请使用基础 `chat.completions` 接口自行编排 |
| **必须支持 JSON Schema 输出格式（`response_format: {"type": "json_object"}`）** | ❌ OpenAI 兼容 Agent 不支持<br>✅ Flow Agent 可通过流程节点后处理实现<br>✅ 托管 Agent 可在 Skill 返回前做 JSON 格式化 | [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)明确声明忽略该字段；另两者可通过流程/技能逻辑保障输出结构 |

> **重要提醒**：三者可混合使用。例如：用 Flow Agent 编排主业务流程，在某个节点中调用托管 Agent 处理复杂对话，再将结果传给 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)供前端展示——百炼平台的设计哲学是“组合优于耦合”。请始终以**业务问题本质**而非技术名词驱动选型。

## 被对比主题页

- [flow agent api](../api/flow-agent-api.md)
- [managed agents api](../api/managed-agents-api.md)
- [openai compatible agents api](../api/openai-compatible-agents-api.md)


