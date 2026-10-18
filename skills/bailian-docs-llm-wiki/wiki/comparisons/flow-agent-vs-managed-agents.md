# Flow Agent 与托管 Agent 对比

本文旨在帮助开发者清晰理解百炼平台中两类核心智能体调用能力的定位差异、技术边界与适用场景，避免因选型不当导致集成复杂度上升、功能受限或运维成本增加。Flow Agent API 面向**已发布应用的轻量级调用与底层组件管理**，而托管 Agent（Managed Agents）API 则面向**从零构建、可自主演进的全托管智能体系统**。二者在架构理念、能力抽象层级和运维责任划分上存在本质区别，不属于简单替代关系，而是互补共存的技术路径。

---

## 关键维度对比

| 维度 | Flow Agent API | 托管 Agent API |
|------|----------------|----------------|
| **核心定位** | 调用已发布的智能体/工作流应用 + 管理 Prompt、旧版长期记忆等基础组件 | 创建、配置、运行具备多步推理、工具调用、结构化记忆的**全生命周期托管智能体** |
| **输入格式** | • 应用调用：支持 `prompt`（单轮字符串）或 `messages`（多角色消息数组，含 `system`/`user`/`assistant`）<br>• 组件调用：JSON 结构化参数（如 `name`, `content`, `workspaceId`） | 统一 JSON 格式：<br>• 创建 Agent：声明式配置（`model_id`, `skills`, `memory_store_type` 等）<br>• 启动会话：`input` 字符串或结构化对象<br>• 追加消息：`POST /sessions/{id}/messages`，支持流式追加 |
| **输出格式** | • 应用调用：同步返回 `output.text`；流式响应（`stream=true`）为 SSE 格式，增量输出文本片段<br>• 组件调用：标准 REST JSON（如 `promptTemplateId`, `memoryId`） | • 同步调用：返回 `session_id`, `output`, `status`, `steps`（执行轨迹）<br>• 流式会话：SSE 响应，含 `event: step`, `event: output`, `event: done` 等语义事件，支持完整执行过程可观测 |
| **支持模型** | • 新版智能体（Agent 2.0）：支持百炼全系模型（`qwen-max`/`qwen-plus`/`qwen-turbo` 等），通过 `app_id` 绑定<br>• 旧版智能体/工作流：同上，但能力较固定<br>• **不提供模型选择接口**，模型由应用发布时固化 | 仅支持平台预置模型：`qwen-max`、`qwen-plus`、`qwen-turbo`；创建 Agent 时必须显式指定 `model_id`；**不支持自定义模型或第三方模型接入** |
| **API 端点与认证** | • **双端点体系**：<br> – 应用调用：`https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`（DashScope API），使用 `Authorization: Bearer <API-Key>`<br> – 组件管理：`https://bailian.{region}.aliyuncs.com/...`（OpenAPI），使用阿里云 AccessKey 签名（ACS3-HMAC-SHA256）<br>• 地域限制：**全部 DashScope 接口仅限华北2（北京）** | • 单一端点体系：`https://bailian.aliyuncs.com/v1/...`（统一域名，无地域硬约束）<br>• 认证：使用短期 [Token](../concepts/token.md)（`X-DashScope-Token`），需先调用 `/v1/auth/token` 获取，有效期 1 小时<br>• **无需 AccessKey，不涉及阿里云签名复杂性** |
| **长期记忆能力** | • 仅支持“长期记忆（旧）”：基于 Key-Value 的简单存储，无向量检索能力<br>• 限流严格（≥1 秒间隔），且已被标记为历史方案<br>• 不支持与智能体自动绑定，需手动管理记忆体与片段 | • 内置结构化 Memory Store：<br> – `vector` 模式（默认）：支持语义检索、自动嵌入、相似度排序<br> – `kv` 模式（实验性）：键值对存储，**不支持语义检索，生产环境禁用**<br>• 记忆与 Session/Agent 自动关联，生命周期受控 |
| **工具调用（Function Calling）** | • 旧版/工作流应用：可通过 Prompt 工程模拟，但无原生协议支持<br>• 新版智能体（Agent 2.0）：支持内置工具（如搜索、计算），但**不可扩展自定义工具** | • 原生支持 Skill 编排：<br> – 内置 Skill：WebSearch、CodeInterpreter 等<br> – 自定义 Skill：注册符合 OpenAPI 3.0 规范的函数，沙箱执行（Python 3.11，≤30s） |
| **计费方式** | • 按调用次数与模型 [Token](../concepts/token.md) 量计费（应用调用部分）<br>• Prompt 模板、旧版记忆等组件操作**免费**（不计入账单）<br>• 计费主体为“应用调用”，组件管理不产生费用 | • 按 Agent 实例运行时长（秒） + 消息处理 [Token](../concepts/token.md) 量 + 文件存储（GB/月）综合计费<br>• Skill 执行、Webhook 投递、Memory 向量索引均计入资源消耗<br>• **明确区分开发态（创建/配置）与运行态（会话/执行）成本** |
| **典型场景** | • 快速集成一个已上线的客服问答机器人<br>• 在自有系统中嵌入一个报告生成工作流<br>• 批量管理 Prompt 模板用于 A/B 测试<br>• 临时上传文件供工作流解析（通过 DashScope 文件上传接口） | • 构建具备自主规划能力的销售助手（自动查库存→比价→生成报价单）<br>• 开发支持多文档深度分析与跨文件引用的研究助理<br>• 需要安全注入数据库凭证并自动执行 SQL 查询的内部运营 Agent<br>• 要求完整执行链路可观测、可审计、可重放的企业级智能体 |

---

## 适用场景建议

### ✅ 选择 Flow Agent API 当：
- 你已有在百炼控制台**发布完成的智能体或工作流应用**，只需在业务系统中调用其能力；
- 你需要**低成本、低侵入地复用现有 Prompt 模板或旧版记忆逻辑**（如迁移历史对话数据）；
- 项目对地域无特殊要求，且能接受**全部调用必须走华北2（北京）节点**；
- 团队熟悉 DashScope SDK 或 OpenAPI 签名机制，能分别处理两类认证；
- 对工具扩展性、记忆语义检索、执行过程追踪无强需求。

### ✅ 选择托管 Agent API 当：
- 你需要**从零设计一个具备多步推理、工具调用、长期上下文理解能力的智能体**，而非调用现成应用；
- 业务要求**记忆支持向量检索**（如“找出上周所有关于合同违约的客户沟通记录”）；
- 你希望将敏感凭证（API Key、DB 连接串）通过 Vault 安全注入，并由 Agent 自动调用；
- 需要**Webhook 事件驱动架构**（如 Agent 完成任务后自动触发钉钉通知或 CRM 更新）；
- 要求统一认证、免签名校验、跨地域可用，且愿意为更高阶能力支付相应运行成本。

> ⚠️ 注意：二者**不可混用同一智能体实例**。Flow Agent 调用的是“已发布应用”，托管 Agent 运行的是“动态创建的托管实例”。若需将托管 Agent 封装为可复用应用，须通过控制台将其**发布为新版智能体（Agent 2.0）**，此后方可被 Flow Agent API 调用。

---

## 技术选型参考（面向开发者）

| 评估项 | Flow Agent API | 托管 Agent API | 建议动作 |
|--------|----------------|----------------|----------|
| **上手速度** | ⚡️ 极快（尤其已有应用）；但需处理双认证、双 endpoint | 🐢 中等（需理解 Agent/Skill/Session 概念模型，首次需调试 Webhook/Token） | 新项目无历史资产 → 优先试托管 Agent QuickStart |
| **可控性** | 🔧 高（直接控制 Prompt、messages、session_id） | 🛠️ 中（声明式配置，执行细节封装；可通过 `steps` 字段观测但不可干预中间步骤） | 需精细控制每轮 Prompt → Flow Agent；需专注业务逻辑而非执行细节 → 托管 Agent |
| **扩展性** | ❌ 弱（无法新增工具、无法升级记忆架构、无法修改模型） | ✅ 强（支持自定义 Skill、可切换 memory store、未来模型升级自动生效） | 长期演进需求强烈 → 托管 Agent 是唯一可持续路径 |
| **运维负担** | ⚠️ 分散（需维护 API Key + AccessKey，监控两个服务健康度） | ✅ 集中（单一 Token、统一错误码、平台负责扩缩容与高可用） | 运维人力有限 → 托管 Agent 显著降低 SRE 成本 |
| **合规与安全** | ⚠️ 依赖开发者实现（如凭证硬编码风险） | ✅ 内置（Vault 加密存储、最小权限 Skill 调用、网络隔离沙箱） | 金融、政务等强合规场景 → 托管 Agent 为首选 |

**一句话总结**：  
> **Flow Agent 是“即插即用的智能体插座”，托管 Agent 是“可编程的智能体操作系统”。**  
> 用插座点亮一盏灯（快速上线），选 Flow Agent；  
> 要建造一座智能楼宇（持续迭代、多系统联动），请部署托管 Agent。

## 被对比主题页

- [flow agent api](../api/flow-agent-api.md)
- [managed agents api](../api/managed-agents-api.md)


