# [长期记忆](../concepts/memory.md)、知识库与向量检索能力对比

本对比旨在帮助开发者清晰区分百炼平台三大核心语义增强能力的定位、边界与适用场景，避免因功能重叠导致的技术误用或架构冗余。[长期记忆](../concepts/memory.md)（Long Term Memory）聚焦**用户级结构化记忆建模与动态演化**；知识库（Knowledge Base）面向**业务文档资产的托管式 RAG 全流程管理**；而向量与排序（Vector & Sort）提供**原子级语义计算原语**，是前两者底层能力的支撑基础，亦可独立用于自定义检索系统构建。

以下从关键工程维度进行横向对比，所有信息均基于百炼平台 2024 年 Q3 正式发布版本（v3.7+）及配套文档规范。

| 维度 | [长期记忆](../concepts/memory.md)（Long Term Memory New） | 知识库（Knowledge Base） | 向量与排序（Vector & Sort） |
|------|----------------------------------|---------------------------|------------------------------|
| **核心定位** | 用户级、对话驱动的**结构化记忆生命周期管理**（事实+画像），强调语义理解后的**意图化存储与上下文感知检索** | 业务级、文档驱动的**托管式 RAG 服务**，强调多源数据接入、自动化切片、向量化与问答生成闭环 | **原子语义计算能力**：提供文本/多模态嵌入（Embedding）、结果重排（Rerank）等底层模型 API，不包含存储或业务逻辑 |
| **输入格式** | `messages`（role-content 对话数组，≤50 轮）或 `custom_content`（纯文本，≤512 字符）；支持 `profile_schema` 触发画像提取 | 多模态原始文件（PDF/DOCX/Excel/MP4/JPG 等）、OSS URL、飞书/钉钉/语雀等第三方链接；支持元数据标签与自定义字段 | 文本字符串、文本数组、Base64 图片、视频 URL、或多模态 `contents` 数组（含 text/image/video 字段）；无业务语义约束 |
| **输出格式** | 结构化 JSON：<br>• `memory_nodes`（含 id, content, type, score, project_id 等）<br>• `user_profile`（按 schema 提取的键值对）<br>• 异步任务状态（`event_id`, `status`, `result`） | 分层 JSON：<br>• 检索：`retrieved_chunks`（含 content, source, score, metadata）<br>• 问答：`answer` + `references`（带引用锚点）<br>• 控制台提供可视化 Playground 输出 | 原子响应：<br>• Embedding：`data[0].embedding`（float array 或 base64）<br>• Rerank：`results[]`（含 index, relevance_score）<br>• 无业务元数据封装 |
| **支持模型（内置/可选）** | • 事实抽取：`qwen3-pro`（默认）<br>• 画像提取：绑定 `profile_schema` 后由专用模型执行<br>• 检索重排：`plan_version=Pro` 启用 `qwen3-rerank` | • Embedding：创建时锁定 `text-embedding-v4`（不可改）<br>• Rerank：运行时可配置 `qwen3-rerank` / `qwen3-vl-rerank`<br>• 生成：问答服务绑定 `qwen3.6-plus` 等 LLM | • Embedding：`qwen3.7-text-embedding`, `text-embedding-v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06` 等<br>• Rerank：`qwen3-rerank`, `qwen3-vl-rerank`, `gte-rerank-v2`（即将下线） |
| **API 端点（典型）** | `POST /api/v1/memory_nodes/add`<br>`POST /api/v1/memory_nodes/search`<br>`GET /api/v1/profile_schemas/{id}/user_profile` | `POST /api/v1/indices/knowledge/search`（应用级联合检索）<br>`POST /api/v1/indices/rag/index/retrieve`（单库底层检索）<br>`POST /api/v1/indices/rag/qa`（问答服务） | `POST /api/v1/services/embeddings/text-embedding/text-embedding`<br>`POST /api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`<br>`POST /api/v1/services/rerank/text-rerank/text-rerank` |
| **计费方式** | • 按**调用次数**计费（add/search/update/delete）<br>• `add-async` 按事件数计费<br>• **无免费额度**（商业化计费自 2026-08-20 10:00 北京时间起） | • 按**RCU（Resource Capacity Unit）** 计费：1 RCU ≈ 支撑 50 QPS<br>• 标准版含 720 小时免费额度（仅抵扣规格费，不含模型/日志/存储）<br>• 切片、向量化、Rerank 均计入 RCU 消耗 | • 按**Token 数量**（Embedding）或**调用次数**（Rerank）计费<br>• 北京地域多数模型享 90 天免费额度（如 `qwen3.7-text-embedding`：100 万 Token）<br>• 新加坡地域无免费额度，单价略高 |
| **典型场景** | • 对话机器人中持续积累用户偏好、订单状态、健康记录等动态事实<br>• 构建实时更新的用户画像（年龄/职业/兴趣/投诉历史）<br>• 技能型 Agent 中管理 `skill_name`/`skill_tags` 标注的记忆节点 | • 客服知识库：将产品手册、FAQ、工单记录构建为可检索知识源<br>• 内部文档助手：接入 Confluence/语雀/SharePoint 的政策与流程文档<br>• 多模态内容检索：从 PPT 图表、培训视频字幕中召回关键信息 | • 自研 RAG 系统：在 LangChain/LlamaIndex 中替换 OpenAI embedding<br>• 跨模态搜索：构建图文混合商品库，支持“找类似这张图的红色连衣裙”<br>• 排序精调：对 Elasticsearch/Meilisearch 召回结果做二次重排 |

## 各方案适用场景建议

### ✅ 推荐选择「长期记忆」当：
- 你需要**以用户为中心**（`user_id` 为第一维度）管理随对话演进的个性化记忆；
- 记忆内容天然具有**强结构化语义**（如“用户上周投诉物流延迟”、“用户对 vegan 食谱感兴趣”），且需支持增删改查与跨项目混合检索；
- 你希望**零代码提取用户画像**（如自动识别“35岁产品经理，喜欢徒步”），并复用于推荐或风控；
- 场景对**低延迟写入**有要求（同步 `add` 接口 QPM 达 120），且能接受 ≤512 字符的轻量输入限制。

### ✅ 推荐选择「知识库」当：
- 你的数据源是**静态或半静态业务文档**（PDF/Excel/网页），且需批量上传、定时同步与可视化管理；
- 你追求**开箱即用的 RAG 效果**，不愿自行处理切片策略、向量化、Rerank 链路编排；
- 需要**多知识库路由、标签过滤、Query 改写、Playground 快速调试**等企业级运维能力；
- 场景涉及**多模态混合检索**（如同时搜索合同文本与签署扫描件），且接受知识库创建后模型不可变更的约束。

### ✅ 推荐选择「向量与排序」当：
- 你需要**完全自主控制语义计算链路**（例如：用 `qwen3-vl-embedding` 对视频帧+ASR文本联合编码，再用 `qwen3-vl-rerank` 排序）；
- 你已在使用 LangChain、LlamaIndex 或自研检索框架，仅需**替换底层 embedding/rerank 模型**；
- 你有特殊合规要求（如必须部署在北京地域），且需精确控制 token 消耗与批处理规模；
- 你需要**超大文本嵌入**（`qwen3.7-text-embedding` 支持 128K token/行）或**细粒度参数调优**（如 `dimensions=2560`, `instruct="Find legal clauses..."`）。

## 技术选型参考（面向开发者）

| 选型目标 | 推荐方案 | 关键理由 | 注意事项 |
|----------|----------|----------|----------|
| **快速上线客服问答机器人** | 知识库 | 控制台 5 分钟完成文档上传 → Playground 实时验证 → API 直接对接前端，无需开发 embedding pipeline | 避免在知识库中存敏感用户对话；需单独用长期记忆管理用户会话状态 |
| **构建个性化推荐引擎** | 长期记忆 + 向量与排序 | 用长期记忆沉淀用户行为事实（`user_id=xxx, content="收藏了AI绘画教程"`），再用 `qwen3.7-text-embedding` 向量化内容做相似推荐 | 不可直接用知识库替代——知识库无 `user_id` 隔离，无法实现千人千面 |
| **自研金融风控系统** | 向量与排序（为主） + 长期记忆（辅助） | 用 `qwen3-vl-embedding` 对财报PDF+截图+电话录音联合编码，`qwen3-rerank` 精排风险线索；长期记忆仅存用户授信变更事件（审计留痕） | 知识库不适用——其切片策略无法满足财报数字精度要求，且不可修改向量化模型 |
| **多租户 SaaS 应用记忆隔离** | 长期记忆（`project_id` 隔离） | 通过 `project_id="tenant_a"` 实现租户级记忆分组，支持跨租户混合检索（`project_ids=["tenant_a","tenant_b"]`）用于运营分析 | 知识库虽支持多库，但无 `user_id` 维度，无法解决同一用户在不同租户下的记忆归属问题 |
| **低成本 PoC 验证语义搜索效果** | 向量与排序（北京地域） | 利用 `text-embedding-v4` + `qwen3-rerank` 免费额度，10 行代码完成端到端 demo，规避知识库/长期记忆的配置复杂度 | 长期记忆和知识库均无免费额度，初期验证成本更高 |

> **重要提醒**：三者非互斥关系，而是**分层协作**关系——  
> - 向量与排序 是知识库与长期记忆的**底层能力提供者**（知识库内部调用 `text-embedding-v4`，长期记忆 `plan_version=Pro` 依赖 `qwen3-rerank`）；  
> - 长期记忆 与 知识库 可**协同使用**：例如，用知识库管理公司制度文档，用长期记忆管理员工个人审批历史，二者通过 `project_id` 隔离并在 Agent 中按需调用。  
> 开发者应基于数据主权（谁拥有数据？）、更新频率（静态文档 vs 动态对话）、隔离粒度（业务库 vs 用户级）三个核心维度决策，而非仅看“是否支持向量检索”。

## 被对比主题页

- [long term memory new](../api/long-term-memory-new.md)
- [knowledge base](../guides/knowledge-base.md)
- [vector and sort](../api/vector-and-sort.md)


