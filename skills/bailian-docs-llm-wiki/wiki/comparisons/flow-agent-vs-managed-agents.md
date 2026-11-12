# 流程型智能体与托管智能体对比

本文旨在帮助开发者清晰理解百炼平台中两类核心智能体能力——**流程型智能体（Flow Agent）** 与**托管智能体（Managed Agent）** 的定位差异、技术边界与适用场景，为实际项目中的架构设计与 API 选型提供客观、可落地的技术参考。随着百炼平台能力演进，二者在抽象层级、控制粒度、运维责任和扩展方式上已形成明确分工：流程型智能体聚焦于**预编排应用的高效调用与轻量集成**，而托管智能体面向**全生命周期可控的生产级 Agent 构建与运营**。

以下从关键维度进行结构化对比，并附技术选型建议。

## 关键维度对比

| 维度 | 流程型智能体（Flow Agent） | 托管智能体（Managed Agent） |
|------|---------------------------|------------------------------|
| **核心定位** | 面向已发布、已配置完成的智能体/工作流应用的**标准化调用接口**，强调“即开即用”与低侵入集成 | 面向 Agent **全生命周期管理**的托管服务，支持从创建、配置、部署到扩缩容的自主控制，强调“按需构建”与深度定制 |
| **输入格式** | 支持 `prompt`（字符串）或 `messages`（消息数组，含 `system`/`user`/`assistant` 角色），兼容 OpenAI-style 格式；需显式传入 `app_id` | 必须通过 `POST /v1/sessions/{session_id}/messages` 提交消息体，格式为 `{ "content": "..." }` 或带 `role` 的结构化消息；首次交互前需先创建 `agent` 和 `session` |
| **输出格式** | 同步响应返回标准 JSON（含 `output.text` / `output.choices[0].message.content`）；支持 Server-Sent Events（SSE）[流式输出](../concepts/streaming-output.md)（`stream=true`）及增量流式（`incremental_output=true`） | 同步响应返回结构化消息对象（含 `id`, `role`, `content`, `timestamp`, `tool_calls` 等字段）；**原生支持工具调用结果解析与多轮状态透出**；暂不支持 SSE 流式，但可通过轮询 `GET /v1/messages/{message_id}` 获取异步执行结果 |
| **支持模型** | **不直接暴露模型选择**；模型能力由控制台发布的应用实例绑定（如 `qwen-max`、`qwen-plus` 等），API 调用时不可动态切换 | **严格限定模型列表**：仅支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 三款百炼托管模型；创建 Agent 时必须指定 `model_id`，不支持自定义模型或外部模型接入 |
| **API 端点与认证** | 分两类：<br>• 应用调用：`https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`，Bearer [Token](../concepts/token.md) 认证<br>• 组件管理（Prompt/记忆）：`https://bailian.{region}.aliyuncs.com/...`，AccessKey 签名认证<br>⚠️ **所有应用调用接口强制限定华北2（北京）地域** | 统一 RESTful 端点：`https://bailian.{region}.aliyuncs.com/v1/...`（支持多地域，如 `cn-shanghai`、`cn-beijing`）<br>统一 Bearer [Token](../concepts/token.md) 认证，API Key 需具备 `managed_agents:full_access` 权限 |
| **[长期记忆](../concepts/long-term-memory.md)能力** | 提供“[长期记忆](../concepts/long-term-memory.md)（旧）”接口（`CreateMemory`/`CreateMemoryNode`），为**显式、结构化、需手动注入**的记忆片段；文档明确提示该能力已被新架构替代，无迁移路径 | 内置 **Memory Store**（记忆存储），支持向量+结构化混合索引；自动关联 Session，支持语义检索、自动摘要与上下文注入；无需手动管理节点，由平台统一维护生命周期 |
| **会话管理** | 依赖 `session_id` 参数启用云端历史上下文，**有效期仅 1 小时（无请求即失效）**；无独立会话资源概念，纯状态标识符 | 提供一级资源 `Session`：可显式创建（`POST /v1/environments/{env_id}/sessions`）、查询、销毁；默认生命周期 24 小时（可配置），支持事件日志、状态快照与跨消息上下文继承 |
| **工具调用（Function Calling）** | 不直接暴露工具注册与调度能力；若底层应用已配置工具，其调用行为对调用方透明，输出中不结构化返回 `tool_calls` 字段 | 原生支持 **Skill（技能）机制**：可注册 HTTP Webhook、内置函数、文件处理等 Skill；Agent 自动识别用户意图并编排调用；响应中明确返回 `tool_calls` 及执行结果 `tool_outputs` |
| **计费方式** | 按**调用量计费**：以“[Token](../concepts/token.md) 数”或“调用次数”为单位（具体计费项依所选应用实例而定）；Prompt 模板、记忆等组件管理类 API 免费 | 按**Agent 实例运行时长 + 推理 Token + 文件存储 + Skill 调用**综合计费；部署后即产生基础资源占用费用（如环境、Memory Store）；支持细粒度用量监控与配额控制 |
| **典型场景** | • 客服对话机器人嵌入（H5/小程序快速对接）<br>• 工作流自动化触发（如审批流、数据报表生成）<br>• Prompt A/B 测试与模板灰度发布<br>• 轻量级 RAG 应用（配合临时文件上传） | • 企业级数字员工（需[长期记忆](../concepts/long-term-memory.md)、多系统集成、权限隔离）<br>• 复杂决策 Agent（如合规审查、投研分析，依赖多 Skill 协同）<br>• 高 SLA 要求的 SaaS 插件（需独立环境、可扩缩容、审计日志）<br>• 需要完整会话生命周期管理的对话产品（如教育陪练、心理疏导） |

## 适用场景建议

### ✅ 选择流程型智能体（Flow Agent）当：
- 你已有在百炼控制台**发布完成的智能体或工作流应用**，目标是快速将其集成至现有业务系统；
- 对延迟敏感，需要**毫秒级同步响应**或**原生 SSE [流式输出](../concepts/streaming-output.md)**（如实时聊天界面）；
- 场景相对固定，无需频繁变更模型、记忆策略或工具集，且可接受 1 小时会话窗口；
- 团队以业务集成工程师为主，希望最小化运维负担，**不涉及 Agent 内部状态管理**；
- 需要灵活复用 Prompt 模板、做变量插值（`${user_name}`）等轻量 Prompt 工程。

### ✅ 选择托管智能体（Managed Agent）当：
- 你需要**从零构建一个具备长期记忆、多工具协同、安全凭证管理能力的 AI Agent**，而非调用现成应用；
- 要求**完整的资源隔离与环境管控**（如为不同客户分配独立 Environment 和 Memory Store）；
- 场景涉及复杂状态流转（如多步骤表单填写、跨会话任务恢复）、需精确控制 Session 生命周期与事件溯源；
- 必须支持**结构化工具调用（Skill）编排**，并期望平台自动处理 `tool_calls` → 执行 → `tool_outputs` → 思考链闭环；
- 运维团队具备一定云原生经验，愿意承担 Agent 配置、部署、扩缩容等职责，以换取更高可控性与扩展性。

## 技术选型参考（面向开发者）

| 选型考量点 | 推荐方案 | 理由说明 |
|------------|----------|----------|
| **快速上线 MVP，验证业务逻辑** | 流程型智能体 | 控制台发布即调用，无需理解 Agent 内部资源模型；5 分钟内完成端到端联调。 |
| **需要跨地域部署（如服务海外用户）** | 托管智能体 | Flow Agent 应用调用强制华北2，而 Managed Agent 支持 `cn-shanghai`、`ap-southeast-1` 等多地域 Endpoint。 |
| **必须使用自定义模型（非 Qwen 系列）** | ❌ 均不支持 | 两者均不开放自定义模型接入通道；如需私有模型，请评估百炼「模型服务」或「推理集群」方案。 |
| **要求会话历史永久保存 & 支持语义检索** | 托管智能体 | Flow Agent 的 `session_id` 仅缓存 1 小时；Managed Agent 的 Memory Store 支持持久化向量库与结构化元数据，可主动查询。 |
| **集成内部系统 API（如 ERP、CRM）作为工具** | 托管智能体 | 通过 Skill API 注册 Webhook，支持签名认证、重试策略、错误熔断；Flow Agent 无此能力。 |
| **预算敏感，追求最低起始成本** | 流程型智能体 | 无环境/内存存储等固定资源费用，按次/按 token 计费；托管 Agent 创建即产生基础资源成本。 |
| **需与现有 IAM/RAM 权限体系深度集成** | 流程型智能体 | Flow Agent 的 DashScope 接口使用通用 API Key，OpenAPI 组件接口复用阿里云 RAM 权限模型，权限粒度更成熟。 |

> **重要提醒**：两类智能体并非互斥，而是互补。典型架构中，可使用 **托管智能体构建核心业务 Agent**（如“合同审查专家”），再将其能力封装为一个**标准 Flow Agent 应用**，供前端或第三方系统通过简单 `/apps/{APP_ID}/completion` 接口调用——既保障了内核能力的可控性，又兼顾了外部集成的简洁性。

## 被对比主题页

- [flow agent api](../api/flow-agent-api.md)
- [managed agents api](../api/managed-agents-api.md)


