# RAG 与[长期记忆](../concepts/long-term-memory.md)能力对比

本页旨在为百炼平台开发者提供 **RAG（[检索增强生成](../concepts/rag.md)）** 与 **[长期记忆](../concepts/long-term-memory.md)（Long Term Memory, LTM）新版本** 两大核心上下文管理能力的系统性对比，帮助技术团队根据业务目标、数据形态、交互模式及工程约束，做出清晰、可落地的技术选型决策。二者虽均面向“让大模型具备外部知识/状态感知能力”，但设计哲学、适用边界与集成方式存在本质差异：RAG 聚焦于**静态知识的结构化索引与精准检索**，服务于问答、搜索等任务；而[长期记忆](../concepts/long-term-memory.md)则聚焦于**动态交互中用户意图、事实与技能的持续沉淀与语义关联**，服务于个性化 Agent 的状态持久化与自主演化。

---

## 关键维度对比

| 维度 | RAG API | 长期记忆（新版本） |
|------|---------|-------------------|
| **核心定位** | 知识库驱动的**外部知识检索与问答服务**，强调对预置文档/数据的高精度、低延迟语义召回 | 用户与系统交互过程中的**结构化记忆沉淀与语义关联服务**，强调对动态上下文的事实抽取、技能固化与画像构建 |
| **输入格式** | 支持多种原始内容：纯文本（`.txt`, `.pdf`, `.docx` 等）、结构化表格（`.xlsx`, `.csv`）、图像（`.jpg`, `.png`）、音视频（`.mp4`, `.mp3`）；需通过 `sourceType` 显式指定来源类型 | 主要为**对话消息流（`messages` 数组）**，支持文本 + 可选 `image_url`；也可传入自定义结构化内容（如 `custom_content` JSON 对象），但需匹配预设 schema 或显式标注类型（`observation`/`skill`/`user_profile`） |
| **输出格式** | - 检索接口（`/search`）：返回带相关性分数、原文片段、元信息的 `chunk` 列表<br>- 问答接口（`/chat`）：返回流式或非流式 LLM 生成结果，附带引用来源（`citations`） | - 搜索（`SearchMemory`）：返回带 `score`、`type`（`observation`/`skill`/`user_profile`）、`content` 和 `metadata` 的记忆节点列表<br>- 查询（`GetUserProfile` / `GetSkillExport`）：返回结构化 JSON（如完整画像字段、技能描述与标签）<br>- [异步任务](../concepts/asynchronous-task.md)（`GetEvent`）：返回抽取结果、错误详情及结构化节点 ID |
| **支持模型/能力** | - 嵌入模型：`text-embedding-v4`、`qwen3-vl-embedding` 等（按 `knowledgeScene` 自动匹配）<br>- 重排模型：`qwen3-rerank`（需显式配置）<br>- 场景模型：`basic_document_qa`、`image_qa`、`table_qa` 等严格绑定知识库类型 | - 抽取模型：内置统一多模态理解模型，支持 `efficient`（毫秒级）与 `intelligent`（高精度，推荐异步）两种提取模式<br>- 计划版本：`lite`（基础搜索）与 `pro`（支持 `min_score` 过滤、Rerank、高级画像）<br>- 不暴露底层嵌入/重排模型名，由平台自动调度 |
| **API 端点（典型）** | - 创建知识库：`POST /api/v1/indices/rag/index/create_v2`<br>- 跨库检索：`POST /api/v1/indices/knowledge/search`<br>- 知识问答：`POST /api/v2/apps/knowledge/chat`<br>- Base URL：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com` | - 写入记忆：`POST /api/v2/apps/memory/fragments/add`（同步）或 `/add_async`（异步）<br>- 语义搜索：`POST /api/v2/apps/memory/fragments/search`<br>- 查询画像：`GET /api/v2/apps/memory/profiles/{user_id}`<br>- Base URL：`https://llm-{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory`（末尾无 `/`） |
| **计费方式** | 按**知识库调用量**计费：<br>- 文档导入（按 token 或文件数）<br>- 检索请求（按次）<br>- 问答请求（按 token + 模型调用）<br>- 存储费用（按知识库容量月结） | 按**记忆操作量 + 计划版本**计费：<br>- 写入（`AddMemory`/`AddMemoryAsync`）按次<br>- 搜索（`SearchMemory`）按次（`pro` 版本含 Rerank 调用）<br>- 画像抽取（`CreateProfileSchema` + `AddMemory`）按次<br>- `pro` 计划支持高级能力，`lite` 为轻量免费版（功能受限） |
| **典型场景** | - 企业内部知识库问答（制度、手册、FAQ）<br>- 客服工单智能检索与摘要<br>- 多源产品文档联合查询（PDF+表格+图片）<br>- 合同/财报等专业文档深度分析 | - 用户个性化 Agent：记住用户偏好、习惯、历史承诺（如“提醒我每天11点点外卖”）<br>- 技能自动化：将高频操作固化为可复用、可导出的 `skill`（如“生成周报”）<br>- 动态用户画像：从对话中持续更新角色、职责、关注点等字段<br>- 多轮对话状态管理：避免重复提问，实现跨会话上下文连贯 |

---

## 适用场景建议

### ✅ 选择 RAG API 当：
- 你拥有**大量静态、结构清晰的业务知识资产**（如产品文档、政策法规、技术白皮书），需要快速构建可检索的知识服务；
- 任务目标明确为**“基于已有资料回答问题”或“在多份材料中定位关键信息”**，对答案的准确性、可溯源性要求极高；
- 数据形态多样（文本+表格+图像），且需**统一索引、联合检索**；
- 已有成熟的内容治理流程（如文档审核、版本管理），希望将知识库作为独立可维护模块接入应用；
- 对响应延迟敏感（如客服实时问答），且能接受预建索引带来的首次检索延迟。

### ✅ 选择长期记忆（新版本）当：
- 你的应用是**强交互型 Agent**（如个人助理、销售顾问、学习教练），需在持续对话中**主动学习、归纳、沉淀用户专属信息**；
- 核心需求是**个性化与状态延续**：例如“记住用户上次说的过敏史”、“自动识别并复用用户常提的‘会议纪要’技能”、“构建跨会话的完整用户画像”；
- 数据天然以**对话消息流（message history）形式产生**，无需人工预处理为文档；
- 需要**结构化、可编程的操作能力**：如按类型筛选记忆、批量更新画像字段、导出技能定义供其他系统调用；
- 接受部分高精度抽取（如复杂画像）采用异步方式，以换取更优效果与稳定性。

> ⚠️ 注意：二者**非互斥，而是互补**。典型高级架构中，RAG 提供“世界知识”，长期记忆提供“用户知识”，两者可通过 `user_id` + `memory_library_id` 在运行时协同调用（例如：先查长期记忆获取用户偏好，再用该偏好优化 RAG 检索 query）。

---

## 技术选型参考（面向开发者）

| 选型考量点 | 推荐方案 | 理由说明 |
|------------|----------|----------|
| **是否需要管理海量静态文档？** | RAG API | 长期记忆不支持文档批量上传、切片管理、多格式解析等 RAG 原生能力；其 `custom_content` 仅适合小规模结构化注入。 |
| **是否需保证每次回答均有明确出处？** | RAG API | RAG 问答接口原生返回 `citations`，支持审计与可信回溯；长期记忆返回的是抽取后的结构化节点，原始对话上下文需额外存储。 |
| **是否需支持图像/音视频内容的语义检索？** | RAG API | RAG 明确支持 `image_qa`、`visual_perception_qa` 等 multimodal 场景；长期记忆仅支持 `image_url` 作为消息附件，抽取能力限于文本描述。 |
| **是否需在多轮对话中自动记住用户未明说的隐含信息？** | 长期记忆 | RAG 无自动抽取机制；长期记忆的 `observation` 类型专为此设计，可从对话中识别事实（如时间、地点、承诺）。 |
| **是否需将用户高频操作固化为可复用、可共享的“技能”？** | 长期记忆 | `skill` 类型记忆支持 `skill_name`/`skill_tags`/`skill_description` 元信息，且提供 `GetSkillExport` 导出标准 JSON，便于跨 Agent 复用。 |
| **是否需构建动态更新的、字段化的用户画像？** | 长期记忆 | 必须通过 `ProfileSchema` 定义结构，再由平台自动抽取填充；RAG 无此抽象层，需自行设计 schema 并在应用层实现映射。 |
| **是否追求最低开发成本与最快上线？** | RAG API（简单问答）<br>长期记忆（个性化 Agent） | RAG 的文档导入+问答链路成熟，控制台可快速验证；长期记忆的 `AddMemory` + `SearchMemory` 接口极简，无需构建索引，适合快速迭代 Agent 状态逻辑。 |
| **是否需严格隔离不同租户/项目的数据？** | 二者均支持 | RAG 通过 `workspace_id` + `index_id` 隔离；长期记忆通过 `user_id` + `memory_library_id` + `project_id` 三级隔离，粒度更细。 |

> 💡 **最佳实践提示**：<br>
> - **混合架构优先**：在 Agent 应用中，将长期记忆作为“用户侧上下文中枢”，RAG 作为“组织侧知识中枢”，通过统一 `user_id` 关联两者；<br>
> - **警惕参数陷阱**：RAG 接口命名风格混用（`snake_case`/`camelCase`）、时间戳单位（秒级字符串）、数字类型校验（必须字符串）等易错点，务必严格对照文档；<br>
> - **善用异步能力**：长期记忆的 `intelligent` 抽取与 RAG 的大批量文档导入均推荐使用异步接口，避免超时与阻塞；<br>
> - **监控先行**：RAG 关注 `index_monitor` 中的检索成功率与延迟；长期记忆关注 `SearchMemory` 的 `min_score` 分布与 `GetEvent` 的失败率，及时调整抽取策略。

## 被对比主题页

- [rag api](../api/rag-api.md)
- [long term memory new](../api/long-term-memory-new.md)


