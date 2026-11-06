# RAG、[长期记忆](../concepts/long-term-memory.md)与向量检索排序能力对比

为帮助开发者在百炼平台中高效构建智能应用，本文对三大核心语义增强能力——**RAG（知识库检索与问答）**、**[长期记忆](../concepts/long-term-memory.md)（结构化记忆管理）** 和 **向量与排序（底层嵌入与重排）** 进行系统性对比分析。三者定位不同：RAG 是面向业务场景的端到端知识服务；[长期记忆](../concepts/long-term-memory.md)聚焦用户/实体维度的动态状态建模；而向量与排序则提供原子级的语义计算能力，是前两者的底层支撑。本对比旨在厘清能力边界、明确技术选型依据，避免功能重叠误用或能力缺失导致的架构返工。

## 关键维度对比

| 维度 | RAG API | 长期记忆（New） | 向量与排序 |
|------|---------|----------------|-------------|
| **核心定位** | 端到端知识库服务：支持文档/表格/图像/音视频等多类型知识的管理、语义检索与生成式问答 | 结构化记忆服务：管理事实（observation）、技能（skill）、用户画像（profile）三类可演化的长期记忆节点 | 原子级语义计算能力：提供文本/多模态向量生成（embedding）与跨文档相关性精排（rerank） |
| **输入格式** | • 知识库管理：JSON（snake_case，如 `index_id`, `doc_ids`）<br>• 检索/问答：`agent_id` + `query` / `messages`（含对话历史）+ 可选 `images` | • 写入：`messages`（数组，含 text/image_url）或 `custom_content`（结构化 JSON）<br>• 检索：`messages` + `user_id` + `memory_types`<br>• 画像：需 `profile_schema` ID | • 文本向量：`string` 或 `string[]`（如 `["文本A", "文本B"]`）<br>• Rerank：`{ "query": "...", "documents": ["...", "..."] }`<br>• 多模态向量：`{ "text": "...", "image_url": "..." }` 或 base64 图像 |
| **输出格式** | • 检索：返回带 `score` 的知识片段列表（含原文、来源、高亮）<br>• 问答：SSE 流式响应（`data: {...}`），含答案、引用、思考链（若启用） | • 写入：同步返回 `memory_node_id`；异步返回 `event_id`（需轮询）<br>• 检索：返回 `memory_nodes` 数组，含 `id`, `content`, `score`, `type`, `metadata`<br>• 画像：返回结构化 JSON（按 schema 定义） | • 文本向量：`{ "data": [{ "embedding": [float, ...], "index": 0 }], "usage": {...} }`<br>• Rerank：`{ "results": [{ "index": 0, "relevance_score": 0.92 }], "usage": {...} }` |
| **支持模型/能力** | • 知识库类型：`document`/`table`/`image`/`multimedia`<br>• 依赖预发布 Agent 实例（含模型、混排、路由策略）<br>• 支持多库联合检索与结果混排 | • 记忆类型：`observation`（事实）、`skill`（技能）、`profile`（画像）<br>• 抽取模式：`intelligent`（AI 自动识别）、`profile_only`<br>• 计划版本：`pro`（支持 `min_score` 过滤）、`lite` | • 文本向量：`text-embedding-v1`（1024维）<br>• 多模态向量：`multimodal-embedding-v1`<br>• 重排序：`rerank-v1`（归一化 0.0–1.0 分） |
| **API 端点（Base URL）** | `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`<br>• 管理：`/api/v1/indices/rag/...`<br>• 检索：`/api/v1/indices/knowledge/search`<br>• 问答：`/api/v2/apps/knowledge/chat` | `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory`<br>• 写入：`/add`, `/add-async`<br>• 检索：`/memory_nodes/search`<br>• 画像：`/profile_schemas/{id}/user_profile` | `https://dashscope.aliyuncs.com/api/v1/`<br>• 向量：`/embeddings`<br>• 重排：`/rerank`<br>• 多模态向量：`/multimodal-embedding` |
| **认证方式** | `Authorization: Bearer <API-Key>`（DashScope API Key） | `Authorization: Bearer <DASHSCOPE_API_KEY>`（同上，但需确保 Key 有 Memory 权限） | `Authorization: Bearer <API-Key>`（DashScope API Key） |
| **计费方式** | 按知识库操作次数（创建/更新/删除）、文档处理量（页数/字节）、检索/问答调用量分项计费；无免费额度 | 2026年8月20日起商业化：<br>• `Add` 接口：按 `pro`/`lite` 计划区分计费<br>• `Search` 接口：`pro` 版本支持 `min_score` 过滤，按调用量计费<br>• 免费试用期已结束 | 按调用量计费：<br>• 文本向量：按 `input` 元素数计费<br>• Rerank：按 `query + documents` 总数计费<br>• 多模态向量：按请求次数计费<br>• 所有模型均有明确单价（控制台查看） |
| **典型场景** | • 客服知识库问答（基于产品文档）<br>• 行业报告智能摘要与溯源<br>• 多源数据（PDF+Excel+图片）联合查询 | • 用户个性化推荐（基于历史偏好与画像）<br>• Agent 自主学习与技能沉淀（如会议纪要模板复用）<br>• 动态用户画像构建与实时更新 | • 自建向量数据库的嵌入生成<br>• RAG 中召回后结果重排序（提升 Top-K 相关性）<br>• 跨文档相似性比对（如合同条款匹配） |

## 各方案适用场景建议

| 方案 | 推荐使用场景 | 不推荐场景 | 关键提醒 |
|------|--------------|--------------|----------|
| **RAG API** | ✅ 需快速上线、无需自建基础设施的知识问答应用（如内部知识助手、客服机器人）<br>✅ 多模态内容（图文/音视频）混合检索与理解<br>✅ 要求开箱即用的监控、权限隔离与审计能力 | ❌ 需完全自定义向量索引结构或底层存储引擎<br>❌ 对检索延迟极度敏感（如毫秒级响应）且无法接受百炼网关转发开销<br>❌ 知识更新频率极高（分钟级），且无法接受异步导入延迟 | • 必须通过 Agent 发布才能调用检索/问答接口<br>• 知识库删除为软删除，不可逆，请谨慎操作<br>• 控制台与 API 的参数命名风格不一致（snake_case vs camelCase），务必以接口文档为准 |
| **长期记忆（New）** | ✅ 构建具备“记忆”能力的智能体（Agent），实现用户偏好持续积累与技能自主演化<br>✅ 需要将非结构化对话自动提炼为结构化事实（如“用户喜欢咖啡因饮品”）或技能（如“自动整理会议待办”）<br>✅ 构建动态、可查询的用户360°画像 | ❌ 替代传统数据库存储业务核心事务数据（如订单、账户）<br>❌ 纯关键词匹配或规则式检索（应使用关系型数据库）<br>❌ 需要强一致性事务（如金融级 ACID） | • `intelligent` 抽取模式必须搭配异步接口（`/add-async`），同步接口易超时<br>• 用户画像首次提取需轮询，业务层需实现重试逻辑<br>• 当前无自动过期机制，长期记忆需自行设计生命周期管理策略 |
| **向量与排序** | ✅ 作为 RAG 或长期记忆的底层能力补充：自建向量库、定制化重排策略、多模态特征融合<br>✅ 需要细粒度控制嵌入/重排过程（如指定 tokenizer、截断策略、输出格式）<br>✅ 进行离线批量处理（如全量文档向量化） | ❌ 直接用于构建端到端问答应用（缺少知识库管理、Agent 编排等能力）<br>❌ 替代 RAG 的语义检索（缺少文档切片、元数据管理、多源混排等关键环节）<br>❌ 替代长期记忆的结构化存储（无 `user_id` 隔离、无记忆类型语义） | • Rerank 模型对长文本会静默截断（≤2048 tokens），务必预处理或分块<br>• 多模态向量暂不支持单次请求处理多个图像，需循环调用<br>• 所有模型均不支持流式响应，均为同步阻塞调用 |

## 面向开发者的选型参考

开发者在技术选型时，应遵循 **“能力分层、按需组合”** 原则：

1. **明确核心诉求层级**  
   - 若目标是 **快速交付一个知识问答产品** → 优先选用 **RAG API**，它封装了从知识摄入、索引构建到检索问答的全链路，大幅降低工程复杂度。  
   - 若目标是 **让 Agent 具备持续学习与个性化能力** → 必须引入 **长期记忆**，它是构建“有记忆的智能体”的基础设施，与 RAG 形成互补（RAG 提供静态知识，长期记忆提供动态上下文）。  
   - 若目标是 **深度定制语义计算逻辑**（如替换默认向量模型、实现自定义重排算法、构建私有向量库）→ 应直接调用 **向量与排序** API，并将其集成到自研检索框架中。

2. **警惕能力重叠与缺失风险**  
   - RAG 的“知识检索”与长期记忆的“记忆搜索”均支持语义相似度匹配，但**语义空间不同**：前者在知识库文档切片空间，后者在用户/实体记忆节点空间。二者不可互相替代，但可协同（例如：RAG 检索出产品文档，长期记忆补充该用户的历史购买偏好）。  
   - 向量与排序 API **不提供任何存储与管理能力**。调用 `text-embedding-v1` 生成的向量需自行存入向量数据库（如 Milvus、PGVector），否则调用即丢弃。它不是“免运维知识库”。

3. **生产环境关键实践建议**  
   - **鉴权与安全**：三个服务均使用 DashScope API Key，但权限范围不同。建议为不同服务创建独立 Key，并在控制台最小化授权（如 RAG Key 不授予 Memory 权限）。  
   - **错误处理**：三者均返回标准 `429` 限流错误，但限流策略不同（RAG 按 10 秒窗口，长期记忆按 QPM，向量按单次请求元素数）。务必实现差异化重试策略（指数退避 + jitter）。  
   - **可观测性**：RAG 提供知识库级监控指标；长期记忆提供事件追踪（`event_id`）；向量与排序仅提供基础 `request_id`。关键链路建议统一打标（如 `trace_id`）并接入日志系统。  
   - **演进路线图**：长期记忆将于 2026 年全面商业化，当前处于功能稳定期；RAG API 已广泛应用于客户生产环境；向量与排序模型持续迭代（新模型发布可通过 `model` 参数无缝切换）。

> **一句话总结选型口诀**：  
> **“RAG 开箱即用做问答，长期记忆赋予 Agent 记忆力，向量与排序是你的语义发动机——需要自建底盘，也允许你更换引擎。”**

## 被对比主题页

- [rag api](../api/rag-api.md)
- [long term memory new](../api/long-term-memory-new.md)
- [vector and sort](../api/vector-and-sort.md)


