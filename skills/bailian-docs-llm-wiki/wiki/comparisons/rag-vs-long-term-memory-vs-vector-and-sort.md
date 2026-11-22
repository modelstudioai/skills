# RAG、[长期记忆](../concepts/long-term-memory.md)与向量检索排序能力对比

## 背景与目的  
在构建智能体（Agent）、知识增强型应用或个性化服务时，开发者常需在**语义[检索增强生成](../concepts/rag.md)（RAG）**、**结构化[长期记忆](../concepts/long-term-memory.md)管理**和**底层向量/重排序能力**三类能力间进行技术选型。三者虽均涉及语义理解与相似性计算，但设计目标、抽象层级、数据模型与生命周期管理存在本质差异。本文旨在为百炼平台开发者提供清晰、可落地的横向对比，帮助其根据业务需求（如是否需要状态持久化、是否依赖用户上下文、是否需自定义检索链路等）做出精准技术决策，避免能力误用或架构冗余。

---

## 关键维度对比表

| 维度 | RAG API | [长期记忆](../concepts/long-term-memory.md)（New） | 向量与排序（Vector & Sort） |
|------|---------|------------------|----------------------------|
| **核心定位** | 面向**知识库问答场景**的端到端解决方案：封装文档处理→切片→嵌入→召回→重排→LLM生成全流程 | 面向**智能体状态管理**的结构化记忆中枢：支持事实、技能、用户画像三类记忆的写入、关联、演化与跨会话检索 | 面向**基础语义计算**的原子能力层：提供文本/[多模态](../concepts/multi-modal.md)向量化（embedding）与相关性重排序（rerank）两类独立、可组合的底层模型服务 |
| **输入格式** | `query`（字符串，≤2048字符） + `knowledge_id`；文档上传支持 PDF/Word/纯文本/JSONL（字段名必须为 `content`） | `messages`（对话历史数组）或 `custom_content`（原始字符串） + `user_id` + `project_id`/`profile_schema`；支持结构化画像模板定义 | 向量：字符串、字符串列表、文件 URL 或[多模态](../concepts/multi-modal.md) `contents` 数组；排序：`query` + `documents`（字符串或对象数组） |
| **输出格式** | 非流式：JSON 结构含 `answer`、`retrieved_chunks`（含内容、来源、score）；流式：SSE 格式，按 `\n\n` 解析事件 | 写入：`event_id`（异步）或 `memory_node_id`（同步）；检索：`memory_nodes` 数组（含 `type`、`content`、`score`、`metadata`）；画像：结构化 JSON 对象（按 schema 定义） | 向量：`data: [{embedding: [...], index: 0}, ...]`；排序：`results: [{index: 0, relevance_score: 0.92}, ...]`（含原始文档索引与分数） |
| **支持模型** | 嵌入模型固定为 `text-embedding-v3`（不可替换）；问答 LLM 可选 `qwen-max`、`qwen-plus` 等 | 记忆抽取与排序能力由服务内部模型自动调度，**不暴露模型选择接口**；`pro` 计划启用高级重排，`lite` 仅基础向量召回 | **完全开放模型选择**：<br>• 向量：`qwen3.7-text-embedding`、`text-embedding-v4`、`qwen3-vl-embedding` 等<br>• 排序：`qwen3.7-text-rerank`（主力）、`qwen3-vl-rerank`（跨模态）等 |
| **API 端点** | `/v1/knowledge/query`（问答）<br>`/v1/knowledge_bases`（知识库管理）<br>`/v1/documents`（文档上传） | `/add` / `/add-async`（写入）<br>`/memory_nodes/search`（检索）<br>`/profile_schemas`（画像管理） | 向量：<br>• 同步：`/api/v1/services/embeddings/text-embedding`<br>• 批处理：`/api/v1/services/embeddings/text-embedding/text-embedding`（带 `X-DashScope-Async` header）<br>排序：`/api/v1/services/rerank/text-rerank` |
| **计费方式** | 按**知识库调用量**计费：每次 `/v1/knowledge/query` 请求计为 1 次 RAG 调用（含嵌入+检索+生成），与文档体积无关 | 按**调用次数**计费：<br>• `Add` / `AddAsync`：每次写入计 1 次<br>• `Search`：每次 `/memory_nodes/search` 计 1 次<br>• `GetUserProfile`：每次查询计 1 次<br>区分 `lite` 与 `pro` 版本（影响抽取质量与重排能力） | 按**[Token](../concepts/token.md) 用量**计费：<br>• 向量：输入文本 [Token](../concepts/token.md) 数 × 模型单价（例：`qwen3.7-text-embedding` 北京地域 0.0005 元/千 [Token](../concepts/token.md)）<br>• 排序：`query` + `documents` 总 Token 数 × 模型单价 |
| **典型场景** | 客服知识库问答、技术文档助手、企业内部政策查询、FAQ 自动应答 | 智能体长期状态维护（如“用户偏好咖啡因”）、跨会话技能复用（如“会议纪要整理流程”）、动态用户画像构建（如“兴趣标签：AI、摄影”） | 构建自定义 RAG 流程、跨模态搜索（图文混合检索）、语义聚类、推荐系统召回层、第三方系统集成（需自主控制向量/排序环节） |
| **数据生命周期** | 文档与切片绑定于知识库，**无自动过期机制**；删除知识库即清除全部关联数据 | 记忆节点**长期有效**，无自动失效；支持软删除（`status="delete"`），但节点仍可被查询 | **无数据存储**：纯计算服务，输入即处理，不保留任何原始内容或向量结果 |

---

## 各方案适用场景建议

### ✅ 优先选用 **RAG API** 当：
- 业务目标是快速上线一个**基于静态知识库的问答系统**（如产品手册、规章制度、培训材料）；
- 不希望自行管理文档解析、切片策略、向量模型选型、重排逻辑等复杂环节；
- 需要开箱即用的流式响应、多路召回（关键词+向量）、Agent 编排集成能力；
- 知识更新频率较低（月级/季度级），且文档格式相对统一（PDF/Word/Markdown）。

> ⚠️ 注意：若需高频更新小片段（如每日运营公告）、或需将用户实时反馈注入知识库，RAG 的“全量/增量同步”机制可能带来延迟，此时应评估长期记忆方案。

### ✅ 优先选用 **长期记忆（New）** 当：
- 构建的是**具备记忆能力的智能体（Agent）**，需跨多轮对话甚至跨天/跨周维持用户状态；
- 需要区分并管理不同语义类型的记忆：如将“用户说‘我过敏花生’”存为 `observation`，将“自动过滤含花生食谱”抽象为 `skill`，将“年龄28、职业设计师”结构化为 `user_profile`；
- 业务强依赖**用户画像驱动的个性化**（如推荐、话术适配），且画像字段需动态扩展与联合抽取；
- 需要记忆与项目（`project_id`）强绑定，实现多业务线隔离（如电商、金融、教育三个独立记忆空间）。

> ⚠️ 注意：长期记忆**不替代知识库**——它不用于托管公开文档，而是管理 Agent 与用户交互中产生的私有、动态、结构化事实。

### ✅ 优先选用 **向量与排序（Vector & Sort）** 当：
- 需要**完全掌控检索链路**：例如自定义切片逻辑（按标题/段落/代码块）、混合多种向量模型（dense + sparse）、接入外部向量数据库（如 Milvus、Qdrant）；
- 场景涉及**[多模态](../concepts/multi-modal.md)内容**（图文混排、视频关键帧+字幕）、或需对非文本内容（如图像特征）生成向量；
- 已有成熟 NLP 工程栈，仅需百炼提供高性能、高精度的 embedding/rerank 模型作为“黑盒算力”；
- 进行离线批量处理（如百万级商品描述向量化）、或对延迟极度敏感（需同步低延迟向量 API）。

> ⚠️ 注意：该能力**无上层业务抽象**，开发者需自行实现索引构建、缓存、去重、结果融合等工程逻辑。

---

## 技术选型参考（面向开发者）

| 你的问题 | 推荐方案 | 理由简述 |
|----------|----------|----------|
| “我想让客服机器人回答公司内部制度问题，1周内上线。” | **RAG API** | 最小化开发成本，知识库创建→上传→问答三步完成，无需模型调优。 |
| “我的 Agent 需记住用户每次说的偏好，并在后续对话中主动应用（如避开过敏源、推荐同类书籍）。” | **长期记忆（New）** | `observation` 类型天然适配用户声明式信息，`user_profile` 支持结构化标签，`project_id` 实现业务隔离。 |
| “我要构建一个图文混合搜索的产品库，用户传一张图+一句话，返回最匹配的商品。” | **向量与排序（Vector & Sort）** + 自研索引 | 必须使用 `qwen3-vl-embedding` 生成图文融合向量，并用 `qwen3-vl-rerank` 对图文混合结果精排。RAG 和长期记忆均不支持此多模态输入范式。 |
| “我已有 Elasticsearch，但想用百炼的 rerank 模型提升搜索相关性。” | **向量与排序（Vector & Sort）** | 直接调用 `/api/v1/services/rerank/text-rerank`，将 ES 召回的 Top-K 结果传入重排，无缝集成。 |
| “用户反馈某条知识回答不准，我想快速修正并生效，不希望重建整个知识库。” | **RAG API**（增量同步）或 **长期记忆**（若属用户专属事实） | RAG 支持单文档增量更新；若该反馈是用户个人事实（如“我的地址变了”），则更适合写入长期记忆的 `observation` 并在问答中动态注入。 |
| “我需要统计所有用户对‘退款政策’的提问频次和情感倾向。” | **RAG API**（日志分析） + **向量与排序**（语义聚类） | RAG 提供标准 query 日志；再用 `text-embedding-v4` 向量化所有提问，聚类分析主题分布。 |

> 💡 **组合使用提示**：三者并非互斥。典型高阶架构为：**长期记忆** 管理用户状态 → 注入 **RAG API** 的 prompt 中作为上下文 → 若需更高精度，用 **向量与排序** 替换 RAG 内置重排模块（通过 `retrieval_strategy=vector_only` 获取原始切片，再调用 `qwen3.7-text-rerank` 重打分）。

---  
*最后更新时间：2025年4月*  
*本文档依据百炼平台 v2.5.0 文档体系编写，具体行为以实际 API 响应与控制台配置为准。*

## 被对比主题页

- [rag api](../api/rag-api.md)
- [long term memory new](../api/long-term-memory-new.md)
- [vector and sort](../api/vector-and-sort.md)


