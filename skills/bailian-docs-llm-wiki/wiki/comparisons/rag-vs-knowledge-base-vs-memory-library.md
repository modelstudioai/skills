# RAG、知识库与记忆库方案对比

本文档面向百炼平台开发者，旨在清晰区分 **RAG API**、**知识库（Knowledge Base）** 和 **记忆库（Memory Library）** 三类核心能力的定位、技术边界与适用场景，辅助技术选型决策。三者虽均涉及“信息检索+上下文增强”，但设计目标、数据生命周期、调用范式与集成深度存在本质差异：  
- **RAG API** 是面向开发者的 *轻量级、任务导向型* 检索增强接口，强调快速接入与端到端问答闭环；  
- **知识库** 是 *企业级、数据驱动型* 的语义索引基础设施，提供全生命周期管理与多源治理能力；  
- **记忆库** 是 *会话感知型* 的[长期记忆](../concepts/memory.md)服务，聚焦跨轮次、跨会话的用户级个性化状态建模与自动注入。  
正确理解三者差异，可避免功能误用（如用记忆库存储产品手册）、架构冗余（如重复构建知识索引）或体验断层（如客服对话中无法记住用户偏好）。

## 关键维度对比

| 维度 | RAG API | 知识库（Knowledge Base） | 记忆库（Memory Library） |
|------|---------|--------------------------|---------------------------|
| **核心定位** | [检索增强生成](../concepts/rag.md)（Retrieval-Augmented Generation）的 *标准化 API 封装*，聚焦单次问答任务 | 企业私有知识的 *语义化存储与索引平台*，支持多源治理、精细切片与混合检索 | 大模型应用的 *跨会话[长期记忆](../concepts/memory.md)中枢*，自动提取并关联用户事实与画像 |
| **输入格式** | 自然语言 `query`（≤2048 字符），需显式传入 `knowledge_base_id` | 多源异构数据：<br>• 非结构化：PDF/Word/TXT/CSV（纯文本）<br>• 结构化：MySQL 表、OSS JSONL、飞书文档等<br>• 多模态：图片/音视频（需启用 VL 模型） | 对话消息流（`AddMemory`）或结构化用户属性（`CreateProfileSchema` + `AddMemory`），以 `user_id` 为隔离键 |
| **输出格式** | `{ "answer": "LLM生成结果", "retrieved_chunks": [...] }`（一体化）<br>或仅 `retrieved_chunks`（纯检索） | • 检索：`{ "chunks": [...], "scores": [...] }`<br>• 问答：`{ "answer": "...", "citations": [...] }`<br>• Playground 支持可视化切片高亮 | • `SearchMemory`: `{ "memories": [{ "content": "...", "type": "fact/profile", "score": 0.x }] }`<br>• `GetUserProfile`: `{ "profile": { "age": 28, "preference": "dark mode" } }` |
| **支持模型** | • Embedding：默认 `text-embedding-v3`，可自定义<br>• LLM：默认 `qwen-max`，可指定其他 Qwen/DeepSeek 模型 | • Embedding：创建时锁定 `text-embedding-v4`（不可变）<br>• Rerank：`qwen3-rerank` / `qwen3-vl-rerank`（按知识库独立启用）<br>• LLM：问答服务支持 `qwen3.6-plus` 等，可动态切换 | • Embedding：内部专用模型（不开放配置）<br>• Rerank：`Pro` 版本启用重排，`Lite` 版本跳过<br>• 无 LLM 生成环节（仅检索注入） |
| **API 端点** | `POST /v1/knowledge_bases/{kb_id}/retrieve_and_answer`<br>`POST /v1/knowledge_bases/{kb_id}/retrieve` | • 底层检索：`POST /api/v1/indices/rag/index/retrieve`<br>• 应用级检索：`POST /api/v1/indices/knowledge/search`<br>• 流式问答：`POST /api/v2/apps/knowledge/chat` | `POST /api/v1/memory/add`<br>`POST /api/v1/memory/search`<br>`POST /api/v1/memory/profile/create`<br>`GET /api/v1/memory/profile/{user_id}` |
| **计费方式** | • 按 **RAG 调用次数** 计费（含检索+生成）<br>• 模型调用费用单独计算（LLM + Embedding）<br>• 免费额度不覆盖模型费用 | • 按 **知识库规格** 计费（标准版/专业版，按月订阅）<br>• **免费额度仅抵扣规格费，不含模型调用费**<br>• 存储、SLS 日志等附加服务单独计费 | • **2026年8月20日起正式计费**<br>• `AddMemory`：按规格分档计费（6类）<br>• `SearchMemory`：按规格分档计费（2类）<br>• 存储：10,000 条以内长期免费 |
| **典型场景** | • 快速验证知识问答效果<br>• 构建轻量客服插件（单次问题响应）<br>• 临时性文档分析任务（如合同条款提取） | • 企业知识中心（产品文档/制度规范/FAQ）<br>• 多系统知识融合（数据库+文档+会议纪要）<br>• Agent 技能底座（绑定 Skill 提供领域知识） | • 智能客服：记住用户历史投诉、设备型号、偏好语言<br>• 个人助理：跟踪日程安排、健康目标、购物清单<br>• Agent 多轮对话：保持上下文连贯性（如“上一条说的报告，帮我导出 PDF”） |
| **数据生命周期** | 依赖知识库，数据持久化由知识库管理；RAG API 本身无状态 | • 文档/切片永久存储（除非手动删除）<br>• 知识库创建后，切片策略不可变更（需重建）<br>• 删除即永久清除 | • 事实记忆/用户画像可设过期时间（7/30/180天）<br>• 默认永不过期<br>• 删除记忆库 = 永久清除所有内容 |
| **地域限制** | 无明确地域限制（遵循百炼通用地域策略） | **严格地域限定**：<br>• 中国站：仅支持 **华北2（北京）**<br>• 国际站：仅支持 **新加坡** | 无明确地域限制（遵循百炼通用地域策略） |
| **开发者控制粒度** | • 高：可动态指定 `top_k`、`enable_rerank`、`filter`<br>• 中：需预创建知识库并传 `kb_id` | • 极高：可精细配置切片长度、相似度阈值、标签规则、混排策略、多库路由 | • 中：通过 `plan_version` 控制质量/成本权衡，`min_score`/`top_k` 可调<br>• 低：Embedding/Rerank 模型不可自定义 |

## 各方案的适用场景建议

### ✅ 选择 **RAG API** 当：
- 你已有现成知识库，只需快速封装一个问答接口供前端调用；
- 场景为单次、无状态的查询（如“查一下报销流程”），无需维护会话上下文；
- 开发周期紧张，希望绕过知识库管理复杂度，直接复用已有 `knowledge_base_id`；
- 需要灵活切换不同知识库 ID（如按部门路由），且接受每次请求显式传参。

### ✅ 选择 **知识库（Knowledge Base）** 当：
- 你需要统一纳管企业级多源知识（文档、数据库、三方协作平台）；
- 要求精细化控制索引质量（如按标题切分、自定义元数据、标签过滤）；
- 计划构建 Agent 技能或集成到工作流中，并需要多知识库联合检索与混排；
- 对数据合规性、地域部署、审计日志（SLS）有明确要求；
- 预算允许承担知识库规格费 + 模型调用费的组合成本。

### ✅ 选择 **记忆库（Memory Library）** 当：
- 你的应用核心是 **多轮、个性化、长周期交互**（如客服、助理、教育陪练）；
- 需要自动从对话中提取动态事件（“下周三开会”）和稳定属性（“用户是iOS用户”）；
- 希望降低开发负担：通过 `autoCapture`/`autoRecall` 实现记忆全自动闭环；
- 不想自行设计记忆存储结构、相似度计算、过期清理等底层逻辑；
- 用户数据隔离是刚需（`user_id` 级别强隔离，天然支持 SaaS 多租户）。

## 技术选型参考指南（面向开发者）

| 选型问题 | 推荐方案 | 关键依据 |
|----------|----------|----------|
| **“我只有一份 PDF 手册，想做个简单问答页面”** | ✅ RAG API | 最小路径：上传文档 → 创建知识库 → 调用 `/retrieve_and_answer`，5分钟上线 |
| **“我们要把 2000 份产品文档、5 张 MySQL 表、10 个飞书知识库统一搜索”** | ✅ 知识库 | 唯一支持多源异构接入、字段映射（未来上线）、跨库混排的方案 |
| **“客服机器人需要记住用户上次投诉的订单号，并在下次对话自动关联”** | ✅ 记忆库 | RAG/API 无用户状态概念；知识库不支持 `user_id` 隔离；记忆库原生支持事实记忆自动提取与召回 |
| **“Agent 需要同时调用知识库（查政策）和记忆库（记用户偏好）”** | ✅ **组合使用** | 百炼推荐架构：Agent Orchestrator → 并行调用 `knowledge/search` + `memory/search` → 聚合上下文 → LLM 生成 |
| **“担心模型费用失控，如何控制成本？”** | ⚠️ 分层管控：<br>• RAG API：用 `top_k=3` + `enable_rerank=false` 降延迟<br>• 知识库：选用 Lite 规格 + 关闭 SLS 日志<br>• 记忆库：`Lite` plan + `min_score=0.6` 减少低质召回 | 三者均提供明确的成本调节参数，但记忆库的 `plan_version` 是唯一内置质量/成本开关 |
| **“需要支持中文、英文、图片混合检索”** | ✅ 知识库（启用 VL 模型） | RAG API 当前仅支持文本 embedding；记忆库暂不支持多模态记忆 |

> **重要提醒**：  
> - **不要用记忆库替代知识库**：记忆库不支持文档解析、切片、结构化字段抽取，无法承载产品手册、法规条文等静态知识；  
> - **不要用 RAG API 替代记忆库**：RAG API 无 `user_id` 概念，无法实现用户级记忆隔离与自动注入；  
> - **知识库是 RAG API 的底层依赖**：所有 RAG API 调用必须指向一个已存在的知识库，二者是“能力封装”与“基础设施”的关系；  
> - **地域合规是硬门槛**：若业务部署在中国站，请务必确认知识库操作仅在 **华北2（北京）** 进行，否则将返回 `404` 或权限错误。

## 被对比主题页

- [rag api](../api/rag-api.md)
- [knowledge base](../guides/knowledge-base.md)
- [memory library overview](../guides/memory-library-overview.md)


