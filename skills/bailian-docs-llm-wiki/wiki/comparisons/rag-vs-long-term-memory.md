# RAG 与长期记忆对比

为帮助开发者在百炼平台中合理选型，本文对 **RAG（检索增强生成）能力** 与 **长期记忆（Long Term Memory, LTM）** 进行系统性对比。二者虽均面向“让模型记住信息”这一目标，但在设计哲学、数据形态、技术定位及适用边界上存在本质差异：  
- **RAG 是面向知识资产的“外部数据库”**：强调结构化/非结构化文档的批量摄入、向量化索引与高精度语义检索，服务于**通用问答、知识查询、文档理解等场景**；  
- **长期记忆是面向交互过程的“个性化记忆中枢”**：聚焦用户行为、意图片段、技能沉淀与画像建模，服务于**多轮对话上下文延续、用户个性化响应、Agent 自演化等场景**。  

本对比基于百炼平台当前（2024–2025）正式发布的 API 能力，覆盖接口设计、模型集成、运维成本与业务适配性等核心维度，旨在为架构设计与技术落地提供可操作的决策依据。

## 关键维度对比

| 维度 | RAG | 长期记忆（LTM） |
|------|-----|----------------|
| **核心定位** | 知识库驱动的**静态知识检索与生成增强**，解决“模型不知道某件事”的问题 | 用户/会话驱动的**动态记忆沉淀与个性化建模**，解决“模型记不住某个人/某次交互”的问题 |
| **输入格式** | 支持文件上传（PDF/DOCX/TXT/CSV/JSON/图片等）、OSS 批量导入；支持结构化类目、标签、元数据；文本需经切片（chunking）处理 | 支持纯文本消息（`messages`）、结构化字段（如 `user_id`, `profile_schema`）；支持异步抽取（`/add-async`），自动识别 observation/skill/profile；不依赖预切片 |
| **输出格式** | • 检索接口（`/knowledge/search`）：返回带 score 的文档片段列表（含 `content`, `source`, `chunk_id`）<br>• 问答接口（`/knowledge/chat`）：SSE 流式 JSON 响应，含 `answer`, `references`, `trace_id` | • 搜索接口（`/memory_nodes/search`）：返回带 `score` 和 `memory_type`（observation/skill）的记忆节点<br>• 画像接口（`/user_profile`）：返回结构化 JSON（如 `{"age": "28", "interests": ["AI", "travel"]}`）<br>• 列表/详情接口：标准分页 JSON 或单条记忆对象 |
| **支持模型** | • **嵌入模型**：`text-embedding-v4`, `qwen3-vl-embedding`（知识库创建时指定）<br>• **重排模型**：`qwen3-rerank`（知识库或 Agent 级配置）<br>• **生成模型**：`qwen3.7-plus` 等（Agent 级 `agent_model` 指定） | • **抽取模型**：由 `extract_scene`（`efficient`/`intelligent`）与 `plan_version`（`lite`/`pro`）隐式调度，不暴露模型名<br>• **搜索模型**：统一语义向量空间，无独立重排模型；`pro` 版本支持 `min_score` 过滤<br>• **无生成模型**：LTM 不直接生成回答，仅提供记忆数据供上层 Agent 使用 |
| **API 端点** | • 管理类：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/indices/rag/...`（如 `/index/create_v2`, `/app/deploy`）<br>• 服务类：`/api/v1/indices/knowledge/search`, `/api/v2/apps/knowledge/chat` | • 全部统一入口：`https://dashscope.aliyuncs.com/api/v1/memory/...`（如 `/add`, `/memory_nodes/search`, `/profile_schemas/{id}/user_profile`）<br>• 鉴权使用 `DASHSCOPE_API_KEY`（非 `BAILIAN_API_KEY`） |
| **认证方式** | `Authorization: Bearer <BAILIAN_API_KEY>` + `workspace_id` 路径参数 | `Authorization: Bearer <DASHSCOPE_API_KEY>` + 必填 `user_id` 查询参数/请求体 |
| **计费方式** | • 按调用量计费：<br> – 知识库构建（索引创建、切片、文件解析）按 token/页数计费<br> – 检索（`search`）按 query 次数计费<br> – 问答（`chat`）按生成 token 数 + 检索 token 数计费<br>• 无免费额度，按实际用量结算 | • 当前（2024–2026.8.19）为**免费公测期**；<br>• 2026 年 8 月 20 日起正式商业化：<br> – 按 `memory_node` 存储量（GB/月）+ `search` 调用次数计费<br> – `pro` 计划支持高级抽取与过滤，费用高于 `lite` |
| **典型场景** | • 客服知识库问答（产品手册、FAQ）<br>• 合同/财报智能解读<br>• 内部文档搜索引擎<br>• 多源资料聚合分析（如研报摘要） | • 多轮对话中记住用户偏好（“上次说喜欢咖啡因低的茶”）<br>• 自动归纳用户技能（“用户常通过 Excel 处理销售数据” → 抽取为 `skill`）<br>• 构建实时用户画像（年龄、职业、兴趣标签）用于个性化推荐<br>• Agent 自学习：将成功对话路径沉淀为可复用 `skill` |
| **数据生命周期管理** | • 支持软删除/硬删除（知识库、文档、切片）<br>• 删除操作**不可逆**，需谨慎执行<br>• 无自动过期机制，需人工清理 | • 记忆节点默认**永久有效**，无自动失效<br>• 支持显式删除单条记忆（`DELETE /memory_nodes/{id}`）<br>• 支持批量导出（`skill/export`）与归档 |
| **扩展性与集成** | • 需配合 Agent 封装才能对外提供问答服务<br>• 知识库与 Agent 解耦：同一知识库可被多个 Agent 复用<br>• 支持多知识库混合检索（Hybrid Search） | • 原生适配 Agent 场景：SDK 提供 `AddMemory`/`SearchMemory` 工具封装<br>• 记忆库（`memory_library_id`）与项目（`project_id`）支持多租户隔离<br>• 可与 RAG 协同：LTM 提供用户画像 → 注入 RAG 提示词提升相关性 |

## 适用场景建议

| 场景描述 | 推荐方案 | 理由说明 |
|----------|----------|----------|
| **需要让模型准确回答企业内部制度、产品文档、技术白皮书等问题** | ✅ RAG | RAG 专为大规模结构化/非结构化知识管理设计，支持精准切片、多级重排与权威引用溯源，确保答案可验证、可追溯。 |
| **希望 Agent 在多次对话中持续记住用户身份、历史请求、偏好设置（如语言、格式、禁忌）** | ✅ 长期记忆 | LTM 以 `user_id` 为第一维度组织数据，天然支持跨会话记忆关联；其 observation 抽取能自动捕获隐式意图，无需人工标注。 |
| **需从用户对话中自动提炼可复用的操作流程（如“导出周报→筛选部门→生成图表”），并沉淀为工具技能** | ✅ 长期记忆（`skill` 类型） | LTM 的 `skill` 记忆类型专为此设计，支持元信息（`skill_name`, `skill_tags`）导出与版本管理，便于后续编排调用。 |
| **构建一个支持多角色（销售/客服/HR）共享知识但权限隔离的知识中心** | ✅ RAG（配合业务空间 + 类目权限） | RAG 的 `workspace_id` + `category` + `tag` 体系支持细粒度知识分类与访问控制，比 LTM 的 `project_id` 更适合静态知识治理。 |
| **需同时满足“查公司年报”（RAG）和“记用户投资偏好”（LTM）** | ⚠️ **组合使用** | 百炼最佳实践：RAG 提供领域知识底座，LTM 提供用户上下文增强；可在 Agent 中先调用 `SearchMemory` 获取用户画像，再注入 RAG 提示词实现个性化问答。 |
| **轻量级应用，仅需存储少量键值对（如用户昵称、上次登录时间）** | ❌ 两者均不推荐 → 建议用自有数据库 | RAG/LTM 均面向语义化、向量化场景，对简单 KV 存储存在过度设计与成本浪费。 |

## 面向开发者的选型参考

作为开发者，在技术选型时请遵循以下原则：

### ✅ 优先选择 RAG 当：
- 你的数据源是**文档集合**（PDF/Word/网页/数据库导出），且需保持原文准确性；
- 业务强依赖**答案可解释性与来源可追溯性**（如金融、医疗、法务场景）；
- 需要支持**高频、大批量、离线构建**的知识库（如每日同步 1000+ 新文档）；
- 团队已具备向量数据库或检索系统运维经验，或愿意接受 RAG 的调优复杂度（切片策略、模型选型、重排阈值）。

### ✅ 优先选择长期记忆当：
- 你的数据源是**对话流、用户行为日志、交互事件**（如聊天记录、点击流、表单提交）；
- 核心诉求是**个性化、上下文连贯性、用户建模**，而非事实性问答；
- 需要**开箱即用的记忆抽取能力**（自动识别 observation/skill/profile），避免自研 NLU 模块；
- 项目处于快速迭代期，希望用最小接入成本获得“有记忆的 Agent”。

### ⚠️ 关键避坑提示：
- **不要用 RAG 存用户隐私数据**：RAG 知识库面向公开/半公开知识，其切片与索引机制不提供字段级脱敏或动态权限控制；用户画像、行为数据请严格使用 LTM。
- **不要用 LTM 替代知识库**：LTM 的搜索精度与召回率针对短文本片段优化，无法替代 RAG 对长文档的深度理解与结构化解析能力。
- **鉴权密钥不可混用**：RAG 使用 `BAILIAN_API_KEY` + `workspace_id`；LTM 使用 `DASHSCOPE_API_KEY` + `user_id`。密钥错误将导致 `401 Unauthorized`。
- **注意限流差异**：RAG 的知识服务（`/knowledge/chat`）QPS 限制为 25，而 LTM 的 `/memory_nodes/search` 为 300 QPM（≈5 QPS），高并发检索场景需提前压测。

> **最后建议**：对于中大型 Agent 应用，**RAG 与长期记忆不是二选一，而是分层协作关系**——RAG 构建“世界知识”，LTM 记录“用户故事”，二者通过 Agent 编排融合，方能实现真正智能、可信、个性化的 AI 体验。

## 被对比主题页

- [rag api](../api/rag-api.md)
- [long term memory new](../api/long-term-memory-new.md)


