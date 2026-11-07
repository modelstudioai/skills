# 知识增强与记忆管理方案对比：RAG、[长期记忆](../concepts/long-term-memory.md)与向量检索排序

本对比旨在帮助开发者清晰理解百炼平台三大核心语义增强能力的技术定位、能力边界与适用范式。随着大模型应用从单次问答向持续交互、状态感知、知识沉淀演进，选择合适的知识增强或记忆管理方案，直接影响系统可靠性、开发效率与长期可维护性。本文聚焦 RAG（[检索增强生成](../concepts/rag.md)）、Long Term Memory（[长期记忆](../concepts/long-term-memory.md)）与 Vector & Sort（向量生成与重排序）三类能力，从接口设计、数据建模、运行时行为及商业化策略等维度展开客观分析，为技术选型提供结构化参考。

## 关键维度对比表

| 维度 | RAG API | [长期记忆](../concepts/long-term-memory.md)（LTM） | 向量与排序（Vector & Sort） |
|------|---------|----------------|-----------------------------|
| **核心定位** | 面向**静态知识库**的端到端检索增强问答服务，强调“知识即服务”（KaaS） | 面向**动态用户上下文**的结构化记忆生命周期管理，强调“记忆即状态”（MaaS） | 面向**底层语义计算**的原子能力组件，提供向量化与排序两类基础算子，强调“能力即原语”（PaaS） |
| **输入格式** | `query`（自然语言问题） + `knowledge_id`；支持 PDF/DOCX/TXT/MD 文档上传（自动切片） | `messages`（对话消息数组，支持 text/image 混合） + `user_id` + 可选 `project_ids`/`profile_schema`；不接受原始文件，仅处理结构化文本内容 | 多样化：<br>• 文本向量：字符串、字符串列表、文件对象（同步）；CSV/JSONL 文件（异步）<br>• 多模态向量：`contents` 数组含 `{"text":...}` / `{"image":...}` / `{"video":...}`<br>• 排序：`query` + `documents`（文本/图像/视频混合列表） |
| **输出格式** | JSON 结构体，含 `answer`（LLM生成答案）、`retrieved_chunks`（带来源文档的原始片段）、`usage`（token统计） | JSON 结构体：<br>• 写入响应：`event_id`（异步）或抽取结果（同步）<br>• 检索响应：`memory_nodes`（含 `content`, `score`, `type`, `source` 等字段）<br>• 画像响应：结构化 `profile` 对象 | • 向量：`data[].embedding`（float 或 base64 编码数组）+ `usage`<br>• 排序：`results[].index`, `results[].relevance_score`, `results[].document`（按相关性降序） |
| **支持模型** | 问答阶段仅限 `qwen-max` / `qwen-plus`；向量化阶段支持 `qwen-turbo` 等轻量模型（仅 embedding） | 不暴露底层模型选择；语义能力由平台统一调度（`pro`/`lite` 版本隐式绑定模型栈） | 全面开放：<br>• 向量：`qwen3.7-text-embedding`, `text-embedding-v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06` 等<br>• 排序：`qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank`（`gte-rerank` 已下线） |
| **API 端点** | `/api/v1/knowledge/query`（问答）<br>`/v1/knowledge_bases`（知识库管理）<br>`/v1/sync_jobs`（同步任务） | `/v1/memory/add`（同步写入）<br>`/v1/memory/add_async`（异步写入）<br>`/v1/memory/search`（语义检索）<br>`/v1/profiles/schema`（画像定义） | • 向量：<br> `/api/v1/services/embeddings/text-embedding/...`（同步）<br> `/api/v1/services/embeddings/multimodal-embedding/...`（多模态）<br> `/api/v1/services/embeddings/text-embedding-batch/...`（异步批处理）<br>• 排序：<br> `/api/v1/services/rerank/text-rerank/...`（文本）<br> `/api/v1/services/rerank/multimodal-rerank/...`（多模态） |
| **计费方式** | 按调用次数（QPS）与 token 消耗双重计费：<br>• 知识库创建/文档上传：免费<br>• `/knowledge/query` 调用：按 `top_k` 返回片段数 + LLM 生成 token 计费<br>• 启用 `enable_rerank` 增加额外 rerank token 费用 | 分版本计费（自 2026-08-20 起）：<br>• `Lite` 版：基础检索与抽取，无 `min_score` 过滤与 rerank<br>• `Pro` 版：支持高精度抽取、`min_score` 过滤、rerank、多项目联合检索；按 `Add`/`Search` 调用次数计费 | 按 token 精确计费：<br>• 向量：按输入 token 数 × 模型单价（如 `qwen3.7-text-embedding`: ¥0.0005/千 token）<br>• 排序：按 `(query_token × doc_count) + Σ(doc_token)` 总和计费<br>• 异步批处理：按总 token 数计费，无额外并发费用 |
| **典型场景** | • 客服知识库问答（产品文档、FAQ）<br>• 法律/医疗领域专业咨询<br>• 内部员工手册智能助手 | • Agent 对话历史沉淀与意图复用（如“提醒我喝水”→后续触发）<br>• 用户偏好建模（爱好、饮食禁忌、会议风格）<br>• 技能记忆管理（“会议纪要整理”工具调用上下文） | • 自建向量数据库的底库嵌入（需搭配 Milvus/Pinecone）<br>• RAG 流程中替换默认向量模型或启用重排序<br>• 跨模态搜索（图文混合检索）<br>• 聚类、去重、语义相似度计算等离线分析任务 |
| **数据持久性** | 知识库级持久化；文档上传后自动切片、向量化并存入专属向量索引；支持全量更新与增量同步 | 记忆节点级持久化；`observation`/`skill`/`profile` 均独立存储，支持细粒度 `DeleteMemory`；删除不可逆 | 无数据持久化；纯计算服务，输入即处理，输出即返回；需用户自行存储向量或排序结果 |

## 各方案适用场景建议

### ✅ 优先选用 RAG API 的场景
- **知识源稳定、更新频率低**：如企业规章制度、产品说明书、行业白皮书等静态文档集合。
- **需要开箱即用的问答体验**：业务方希望快速上线“问文档得答案”功能，不愿投入工程资源搭建向量库、编排检索链路。
- **对答案可解释性要求高**：需明确返回引用片段（`retrieved_chunks`）及来源文档，满足审计或合规需求。
- **团队缺乏向量数据库运维经验**：避免自行管理 HNSW/IVF 索引、分块策略调优、embedding 模型升级等复杂事项。

### ✅ 优先选用长期记忆（LTM）的场景
- **Agent 应用需维持长期状态**：如个人助理、销售陪练、教育辅导等需跨会话记住用户习惯、承诺、待办事项的场景。
- **需结构化提取与关联信息**：例如从对话中自动识别“用户生日”并写入画像，后续生日当天主动推送祝福。
- **记忆需多维度组织与隔离**：按 `project_id` 划分不同业务线记忆（如“电商订单” vs “客服投诉”），或按 `user_id` 实现严格租户隔离。
- **技能复用驱动工作流**：将高频操作（如“生成周报”“分析竞品价格”）注册为 `skill` 类型记忆，供 Agent 动态发现与调用。

### ✅ 优先选用向量与排序（Vector & Sort）的场景
- **已有向量数据库或自研检索系统**：需替换 embedding 模型（如从 `text-embedding-v2` 升级至 `qwen3.7-text-embedding`），或在现有 pipeline 中插入 `qwen3-rerank` 提升排序质量。
- **超大规模离线建库**：需对百万级文档批量生成向量，此时 `text-embedding-async-v2`（10 万行/请求）比 RAG 的同步上传更高效。
- **跨模态检索需求明确**：如“查找与这张设计图语义相似的产品宣传文案”，必须使用 `qwen3-vl-embedding` + `qwen3-vl-rerank`。
- **定制化语义计算逻辑**：需对向量做聚类、异常检测、余弦相似度矩阵计算等非标准 RAG 操作，直接调用原子 API 更灵活。

## 面向开发者的选型决策树

作为开发者，在技术选型时请按以下逻辑逐层判断：

1. **第一步：确认数据性质与生命周期**
   - 若数据是**静态文档集合（PDF/DOCX）且长期不变** → 选 **RAG API**  
   - 若数据是**动态对话流、用户行为事件、需实时写入与更新的状态** → 进入第二步  
   - 若需**完全自主控制向量生成/排序过程，或集成到自研系统** → 选 **Vector & Sort**

2. **第二步：确认状态管理粒度与结构化需求**
   - 若只需**简单语义检索历史消息**（如“查用户之前提过什么需求？”）→ **RAG API**（临时建知识库）或 **LTM**（推荐）  
   - 若需**提取结构化属性（年龄/城市/偏好）并持久化为画像** → 必须选 **LTM**（`profile_schema` + 异步抽取）  
   - 若需**将用户能力/工具调用经验抽象为可复用技能** → 必须选 **LTM**（`skill` 类型记忆）

3. **第三步：确认性能、成本与扩展性约束**
   - 若 QPS > 300 且需毫秒级响应 → **Vector & Sort**（同步向量）或 **LTM Lite**（避免 Pro 版 rerank 延迟）  
   - 若预算敏感且允许异步延迟 → **LTM Async**（写入） + **Vector & Sort Async**（批量建库）组合降低成本  
   - 若需跨地域部署（如北京+新加坡）→ **Vector & Sort**（各区域独立调用，无知识库跨域同步问题）

> **重要提醒**：RAG 与 LTM **不可互换替代**——RAG 的知识库无法存储用户个性化状态，LTM 无法直接索引原始 PDF 文档。当业务同时需要“静态知识问答”与“动态用户记忆”时，应采用**组合架构**：RAG 处理通用知识查询，LTM 管理用户上下文，二者通过 `user_id` + `project_id` 在业务层协同（例如：RAG 答案中插入 LTM 提取的用户偏好：“根据您的素食偏好，推荐以下三个选项…”）。

---  
*本文档依据百炼平台 2026 年 Q2 版本 API 规范编写，关键时间节点（如 LTM 商业化、`gte-rerank` 下线）已标注，开发者接入前请务必查阅对应模块最新版官方文档。*

## 被对比主题页

- [rag api](../api/rag-api.md)
- [long term memory new](../api/long-term-memory-new.md)
- [vector and sort](../api/vector-and-sort.md)


