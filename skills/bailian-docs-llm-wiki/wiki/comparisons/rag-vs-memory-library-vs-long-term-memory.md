# RAG、记忆库与[长期记忆](../concepts/long-term-memory.md)方案对比

为帮助开发者在百炼平台中合理选型，本文对三种核心知识增强与状态管理能力——**RAG API（[检索增强生成](../concepts/rag.md)）**、**记忆库（Memory Library）** 和 **[长期记忆](../concepts/long-term-memory.md)（Long Term Memory）** 进行系统性对比。三者虽均面向“外部知识接入”与“上下文扩展”，但设计目标、数据形态、生命周期和集成范式存在本质差异：RAG 侧重**静态知识的结构化索引与实时语义检索**，适用于文档问答、知识库助手等场景；记忆库与[长期记忆](../concepts/long-term-memory.md)则聚焦**动态会话中产生的用户级事实与画像的自动提取、持久化与跨轮次召回**，解决大模型“健忘”问题。本文从技术实现、接口规范、计费策略及适用边界出发，提供可落地的选型决策参考。

## 关键维度对比

| 维度 | RAG API | 记忆库（Memory Library） | 长期记忆（Long Term Memory） |
|------|---------|--------------------------|------------------------------|
| **核心定位** | 静态知识库的构建、检索与问答服务（面向文档/表格/音视频等结构化/非结构化内容） | 跨会话的**自动化长期记忆服务**，预置规则驱动的事实提取与用户画像构建（面向对话流） | 结构化长期记忆的**全生命周期管理 API**，支持显式控制的事实记忆（Observation/Skill）与用户画像（Profile）操作 |
| **输入格式** | 支持多种原始格式：<br>• 文档：PDF/DOCX/TXT/MD 等<br>• 表格：CSV/XLSX<br>• 图片/音视频：URL 或 base64<br>• 结构化数据：JSON Schema 定义的表 | 仅接受**对话消息数组（`messages`）**：<br>`[{ "role": "user", "content": "..." }, { "role": "assistant", "content": "..." }]`<br>（可选传 `profile_schema` 触发画像提取） | 同记忆库，输入为 `messages` 数组；<br>额外支持：<br>• `extract_mode: "profile_only"`（仅抽画像）<br>• `project_id` / `project_ids`（二级业务隔离）<br>• `memory_library_id`（指定记忆库） |
| **输出格式** | • 检索：返回匹配的**切片（chunk）列表**，含 `content`, `score`, `metadata`<br>• 问答：流式响应（`stream=true`），返回带引用的自然语言答案及溯源信息 | • 检索：返回**记忆节点（`memory_node`）列表**，含 `id`, `type`（fact/profile）, `content`, `score`, `created_at`<br>• 管理接口：标准 RESTful JSON（如 `GET /memory_nodes/{id}` 返回完整节点对象） | 同记忆库，但字段更丰富：<br>• `memory_node` 明确区分 `type: "observation"` / `"skill"` / `"profile"`<br>• 支持 `GET /profile_schemas/{id}/user_profile?user_id=xxx` 获取结构化画像<br>• 异步写入返回 `event_id`，需轮询 `/events/{id}` 获取结果 |
| **支持模型/能力** | • 向量模型：`embeddingModelName`（如 `text-embedding-v4`）、`multimodalEmbeddingModelName`（如 `qwen3-vl-embedding`）<br>• 问答模型：由 Agent 中 `model_id` 指定（如 `qwen3`）<br>• 混排策略：Agent 配置中定义 | • 提取模型：封装在预置/自定义**记忆规则**中，不可直接指定模型<br>• 策略版本：`Pro`（高精度+`min_score`过滤）或 `Lite`（轻量级）<br>• 默认使用百炼统一语义理解模型 | • 提取模型：同记忆库，基于规则封装<br>• `extract_scene: "efficient"`（推荐）或 `"intelligent"`（可能超时）<br>• `plan_version: "pro"` / `"lite"` 控制搜索精度与能力 |
| **API 端点（Base URL）** | `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`<br>（`workspace_id` 为业务空间 ID） | `https://dashscope.aliyuncs.com/api/v2/apps/memory/`<br>（全局统一地址，无需 workspace_id） | `https://dashscope.aliyuncs.com/api/v2/apps/memory/`<br>（与记忆库**共用同一 Base URL 和鉴权体系**） |
| **认证方式** | Bearer Token（`Authorization: Bearer <API-Key>`）<br>API Key 来源于百炼控制台【API 密钥管理】 | Bearer Token（`Authorization: Bearer $DASHSCOPE_API_KEY`）<br>使用 DashScope 全局 API Key | Bearer Token（`Authorization: Bearer $DASHSCOPE_API_KEY`）<br>同记忆库，使用 DashScope 全局 API Key |
| **计费方式** | • 按**知识库调用量**计费：<br>  - 知识库创建/更新/删除（按次）<br>  - 文档导入/切片（按页/按文件）<br>  - 检索（`/search`）与问答（`/chat`）调用（按次）<br>• 免费额度有限，超出后按量付费（详见 [RAG 计费说明](../../raw/application-api-reference/rag-api/rag-api-billing.md)） | • **2026年8月20日起正式计费**<br>• 按调用次数计费：<br>  - `Add`（写入）调用<br>  - `Search`（检索）调用<br>• Pro/Lite 版本单价不同，首3个月享免费额度 | • **2026年8月20日起正式计费**（与记忆库同步）<br>• 计费项与记忆库一致：<br>  - `add` / `add-async`（写入）<br>  - `search`（检索）<br>• `pro`/`lite` 版本区分定价，免费额度共享 |
| **典型场景** | • 企业知识库问答（产品文档、内部 SOP）<br>• 多源数据联合查询（数据库+PDF报告）<br>• 图片/音视频内容理解（如“从会议录像中找张三发言片段”）<br>• 基于私有资料的智能客服 | • 个人助理类应用（记住用户偏好：“我不吃香菜”、“每周三健身”）<br>• 任务型 Agent（自动提取待办：“明天下午3点开会”并设提醒）<br>• 用户画像构建（从多轮对话中沉淀“职业：设计师，爱好：摄影”） | • 需要精细控制记忆生命周期的场景：<br>  - 技能复用（将“订会议室流程”存为 `skill` 类型，供其他会话调用）<br>  - 多项目隔离（`project_ids` 实现客户A/B数据物理隔离）<br>  - 异步高可靠写入（避免 `intelligent` 模式超时风险）<br>• 需导出结构化记忆用于分析或迁移 |

## 各方案的适用场景建议

- **选择 RAG API 当且仅当**：  
  ✅ 你拥有**大量静态、结构化或半结构化的业务资料**（如 PDF 手册、Excel 数据、产品图片），需要将其转化为可被大模型精准引用的知识源；  
  ✅ 你的应用核心是**“查资料、答问题、做推理”**，而非维护用户状态；  
  ❌ 不适合用于记录用户临时意图、行为偏好或跨会话状态——RAG 的知识库是“只读索引”，不支持自动从对话中学习新事实。

- **选择 记忆库（Memory Library） 当且仅当**：  
  ✅ 你希望**零代码/低代码快速启用长期记忆能力**，通过控制台配置规则即可自动提取事实与画像；  
  ✅ 你的应用是**标准化对话机器人**（如客服、HR 助手），对记忆的定制化控制需求较低，接受百炼预置的 Pro/Lite 策略；  
  ✅ 你依赖 **Agent Harness 或 OpenClaw 插件模式**进行集成，追求开箱即用的钩子（`before_agent_start`）；  
  ❌ 不适合需要细粒度控制记忆类型（如明确区分 `skill` 与 `observation`）、多项目隔离或异步任务状态跟踪的复杂业务。

- **选择 长期记忆（Long Term Memory） 当且仅当**：  
  ✅ 你需要**完全自主掌控记忆的写入、分类、检索与管理逻辑**，例如将用户流程固化为可复用 `skill`、为不同客户分配独立 `project_id`；  
  ✅ 你已具备一定工程能力，愿意处理**异步任务轮询、事件状态机、Schema 版本管理**等细节；  
  ✅ 你要求**最高灵活性与可审计性**：所有 API 均为显式调用，无隐藏规则；支持记忆节点导出、分页列表、精确 ID 查询；  
  ❌ 不适合追求极简接入、无开发资源支撑的 MVP 场景——其 API 丰富度带来更高学习与维护成本。

## 面向开发者的技术选型参考

| 你的需求 | 推荐方案 | 理由 |
|----------|----------|------|
| **已有大量 PDF/Word/Excel，想快速搭建一个“公司知识问答机器人”** | ✅ RAG API | RAG 原生支持多格式文档解析、切片、向量化与混合检索，控制台可一键发布 Agent，5 分钟上线问答服务。 |
| **正在开发个人健康助手 App，需记住用户饮食禁忌、运动习惯、用药提醒，并在后续对话中自动关联** | ✅ 记忆库 | 开通即用，配置“健康事实规则”（有效期 30 天）+ “用户画像模板”，通过 `Add`/`Search` 两接口完成闭环，无需关心底层模型与异步逻辑。 |
| **为 SaaS 平台构建多租户智能客服，每个客户有独立知识库（RAG）+ 独立用户记忆（LTM），且需将客户 SOP 流程存为可复用技能** | ✅ RAG API + 长期记忆 | RAG 管理客户静态知识，长期记忆管理客户级动态事实与技能；二者通过 `user_id` + `project_id` 实现数据隔离，API 设计正交，易于组合。 |
| **团队有成熟 NLP 工程能力，需将记忆抽取逻辑与自有模型/规则深度集成，并导出记忆用于 BI 分析** | ✅ 长期记忆 | 提供最完整的 CRUD 接口、异步事件机制、结构化 Schema 管理及记忆导出能力，满足高定制化与数据治理需求。 |
| **预算敏感，需最大化免费额度，且功能需求简单（仅基础事实记忆）** | ⚠️ 记忆库（Lite 版本） | 在免费期内，记忆库 Lite 版本调用单价更低，且控制台配置成本远低于长期记忆的代码集成成本。 |

> **重要提示**：  
> - **记忆库与长期记忆并非互斥替代关系，而是演进关系**：长期记忆是记忆库能力的 API 化、精细化与开放化升级，二者共享底层引擎与计费体系，未来记忆库控制台功能将逐步收敛至长期记忆 API 之上。  
> - **RAG 与记忆类方案可协同使用**：典型架构为“RAG 提供领域知识底座 + 记忆/长期记忆注入用户上下文”，二者通过 [Prompt 工程](../concepts/prompt-engineering.md)或 Agent 编排融合，共同提升回答准确性与个性化水平。  
> - **所有方案均需关注限流与错误处理**：RAG 运行时接口限流为用户维度 25 QPS；记忆类接口为账号维度总计 3000 QPM（`add` ≤120，`search` ≤300）。务必实现 `429` 错误的指数退避重试，并在日志中记录 `request_id` 便于排查。

## 被对比主题页

- [rag api](../api/rag-api.md)
- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)


