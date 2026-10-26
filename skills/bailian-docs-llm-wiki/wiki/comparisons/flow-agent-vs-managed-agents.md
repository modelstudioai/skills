# 流程型智能体与托管型智能体对比

为帮助开发者在百炼平台中高效选型，本文系统对比**流程型智能体（Flow Agent）** 与**托管型智能体（Managed Agent）** 两类核心智能体范式。二者定位不同：流程型面向“应用即服务”场景，强调开箱即用、低代码集成与标准化调用；托管型面向“可编程智能体”场景，强调运行时可控性、环境隔离与深度编排能力。本对比基于当前（2024年Q3）百炼平台正式发布的 API 能力，聚焦技术实质差异，不涉及未来规划或实验性功能。

## 关键维度对比

| 维度 | 流程型智能体（Flow Agent） | 托管型智能体（Managed Agent） |
|------|-----------------------------|--------------------------------|
| **核心定位** | 面向终端应用的**声明式工作流服务**：以预发布智能体/工作流为单位进行调用，关注“做什么” | 面向开发者的**可编程运行时基础设施**：以 Agent 实例为单位进行生命周期管理，关注“怎么做、何时做、在哪做” |
| **输入格式** | 支持两种模式：<br>• 单轮文本 `prompt`（字符串）<br>• 多轮结构化 `messages`（含 `system`/`user`/`assistant` 角色，支持文本+图片多模态）<br>• 可选传入 `session_id` 加载历史上下文（1小时有效期） | 基于 `Session` 的有状态交互：<br>• 请求体中通过 `input` 字段传递用户输入（字符串或 JSON 对象）<br>• 上下文由 `Environment` + `Memory Store` + `Session` 三重机制自动注入，支持 Jinja2 模板变量（如 `{{ memory.user_preferences }}`） |
| **输出格式** | • 同步响应：返回 `output` 字段（字符串或结构化 JSON）<br>• 流式响应（`stream=true`）：SSE 协议推送 `event: message` / `event: finish` 事件<br>• 支持 `incremental_output` 控制增量/全量返回逻辑 | • 同步响应：返回 `session_id` 和初始状态<br>• 异步事件流：通过 `/v1/sessions/{id}/events` 订阅 SSE，事件类型包括 `agent_step`（工具调用/思考步骤）、`agent_finish`（最终结果）、`error` 等<br>• 最终结果需从 `Event` 中解析 `output` 字段 |
| **支持模型** | **不直接暴露模型参数**。模型能力由预置的智能体或工作流应用封装，开发者通过 `app_id` 间接绑定模型（如某工作流固定使用 `qwen-plus`）。无运行时模型切换能力。 | **显式指定模型**：创建 Agent 时必须声明 `model` 字段（如 `"qwen-max"`），且须在项目已开通模型列表内。支持同一 `Environment` 下不同 Agent 使用不同模型。 |
| **API 端点与认证** | **双认证体系，严格分离**：<br>• 应用调用（如 `/apps/{app_id}/completion`）：`Bearer <API Key>`，Base URL 为 `https://dashscope.aliyuncs.com/...`<br>• 组件接口（Prompt/Memory）：`ACS3-HMAC-SHA256` 签名（AccessKey），Base URL 为 `https://bailian.{region}.aliyuncs.com/...` | **统一 Bearer [Token](../concepts/token.md) 认证**：<br>所有接口（Agent/Session/Skill/Memory Store）均使用 `Authorization: Bearer <access_token>`，Base URL 为 `https://bailian.{region}.aliyuncs.com/api/v1/...`（标准 OpenAPI 风格） |
| **[长期记忆](../concepts/long-term-memory.md)能力** | 提供 `Memory`（记忆体）与 `MemoryNode`（记忆片段）两级抽象：<br>• 需显式创建 `memoryId` 并在请求中传入<br>• 接口限流严格（≥1秒间隔）<br>• 文档标注为“[长期记忆](../concepts/long-term-memory.md)（旧）”，无明确演进路径 | 提供 `Memory Store`（结构化键值存储）：<br>• 自动与 `Session` 绑定，TTL 可配置<br>• 支持 `GET /v1/memory-stores/{id}/keys/{key}` 直接读写<br>• 无显式限流提示，设计更贴近生产级状态管理 |
| **技能（Tool）扩展** | 依赖工作流中预定义的节点（如 HTTP 调用、数据库查询），**不可动态注册新技能**。技能能力由平台内置或工作流配置固化。 | 支持 `Skill` 动态注册与绑定：<br>• 仅支持 Webhook 类型（HTTP 回调）<br>• 创建 Skill 后，可在 Agent 配置中声明启用<br>• 支持运行时事件驱动调用（`agent_step` 事件触发） |
| **计费方式** | 按**调用量计费**：<br>• 智能体/工作流调用按次计费（含输入 token + 输出 token）<br>• Prompt 模板、Memory 等组件操作**不单独计费**（计入平台基础资源） | 按**实例运行时长 + 调用量**双重计费：<br>• Agent 实例按小时计费（无论是否活跃）<br>• Session 处理按输入/输出 token 计费<br>• Memory Store 存储容量按月计费 |
| **典型场景** | • 客服对话机器人（嵌入 App/Web）<br>• 内部知识库问答（控制台发布后直接调用）<br>• 标准化数据处理工作流（如合同解析→摘要生成→存档） | • 需多租户隔离的 SaaS 应用（每个客户独立 Environment）<br>• 复杂决策系统（需分步调试 `agent_step` 事件）<br>• 集成企业内部系统（通过 Webhook 调用 ERP/CRM）<br>• AI Agent 开发平台（提供 SDK 让第三方构建 Agent） |

## 适用场景建议

### 选择流程型智能体（Flow Agent）当：
- ✅ 你已有明确业务需求，且可通过百炼控制台快速配置并发布一个智能体或工作流；
- ✅ 你的前端应用（App/H5/小程序）需要简单、稳定、低延迟的 API 集成，无需管理 Agent 生命周期；
- ✅ 你依赖平台提供的 Prompt 工程能力（模板变量插值）和轻量级[长期记忆](../concepts/long-term-memory.md)，但不需要跨会话强一致性；
- ✅ 你追求上线速度，接受“黑盒模型绑定”和有限的运行时干预能力。

### 选择托管型智能体（Managed Agent）当：
- ✅ 你需要对 Agent 行为进行细粒度可观测性（如审计每一步工具调用、拦截中间结果）；
- ✅ 你的架构要求环境隔离（如测试/预发/生产 Environment）、多版本灰度、蓝绿部署；
- ✅ 你需将 Agent 深度集成至现有系统（如通过 Webhook 调用内部 API，或从 Vault 安全读取数据库凭证）；
- ✅ 你正在构建 AI 原生应用平台，需提供 SDK 让业务方自主创建、调试、部署 Agent 实例；
- ✅ 你对状态持久化有明确 SLA 要求（如 Session 级记忆 TTL 精确控制、24 小时存活保障）。

## 技术选型参考（致开发者）

| 选型考量点 | 推荐方案 | 理由说明 |
|------------|----------|----------|
| **快速验证 MVP** | 流程型智能体 | 控制台拖拽配置 → 发布 → 5 分钟完成 API 调用，零 SDK 依赖；适合业务方主导的 PoC。 |
| **高并发、低延迟 C 端服务** | 流程型智能体 | DashScope 网关专为高吞吐优化，流式响应成熟，错误码体系清晰；托管型因事件订阅链路更长，端到端延迟略高。 |
| **企业级多租户 SaaS** | 托管型智能体 | `Environment` 是天然租户隔离单元，支持独立配额、模型策略、Skill 白名单；流程型仅靠 `workspaceId` 隔离，权限粒度粗。 |
| **需要调试 Agent 内部执行逻辑** | 托管型智能体 | `agent_step` 事件提供完整执行轨迹（思考链、工具参数、返回结果），便于问题定位；流程型仅返回最终输出。 |
| **与内部系统深度集成** | 托管型智能体 | Skill Webhook 支持自定义鉴权头、重试策略、超时控制；流程型工作流节点无法灵活适配私有协议。 |
| **长期记忆需跨会话强一致** | 托管型智能体 | `Memory Store` 设计为 Session 无关的持久化存储，支持显式 CRUD；流程型 `MemoryNode` 依赖 `session_id` 关联，且文档未明确跨会话复用机制。 |
| **团队具备较强工程能力** | 托管型智能体 | 需理解 Environment/Session/Deployment 概念，编写事件处理器，管理 Access [Token](../concepts/token.md) 生命周期；流程型只需维护 API Key。 |

> **重要提醒**：两类智能体**不互斥**，可混合使用。典型模式是——用托管型智能体开发、调试并验证复杂 Agent 逻辑；待稳定后，将其封装为标准化工作流，再通过流程型智能体 API 对外提供轻量服务。百炼平台鼓励此渐进式演进路径。

## 被对比主题页

- [flow agent api](../api/flow-agent-api.md)
- [managed agents api](../api/managed-agents-api.md)


