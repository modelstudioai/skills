# RAG、[长期记忆](../concepts/long-term-memory.md)与向量检索排序能力对比

本对比旨在帮助百炼平台开发者清晰区分 **RAG（知识库问答）**、**[长期记忆](../concepts/long-term-memory.md)（Long Term Memory）** 和 **向量与排序（Vector & Sort）** 三大核心能力的技术定位、能力边界与集成路径。三者虽均依赖语义向量化与检索技术，但在设计目标、数据生命周期、抽象层级和适用阶段上存在本质差异：  
- **RAG** 是面向 *结构化业务知识* 的端到端问答解决方案，强调“知识可管理、检索可配置、回答可编排”；  
- **[长期记忆](../concepts/long-term-memory.md)** 是面向 *动态对话上下文与用户状态* 的结构化记忆中枢，强调“事件可沉淀、类型可定义、画像可演进”；  
- **向量与排序** 是底层 *原子级AI能力服务*，提供标准化的嵌入、多模态编码与重排序接口，不绑定业务逻辑，供上层系统按需调用。  

本文为技术选型提供客观维度对照与场景化建议，适用于智能体（Agent）架构设计、知识增强系统开发及检索优化策略制定。

## 关键维度对比

| 维度 | RAG API | 长期记忆（New） | 向量与排序（Vector & Sort） |
|------|---------|------------------|----------------------------|
| **核心定位** | 知识库全生命周期管理 + 可配置语义问答服务 | 结构化对话记忆与用户状态持久化服务 | 原子级向量生成（Embedding）、多模态编码（Multimodal Embedding）与结果重排序（Rerank）能力 |
| **输入格式** | • 知识库管理：JSON（`docIds`, `index_id`, `agent_config`）<br>• 运行时检索/问答：`query`（文本/图像）、`messages`（多轮对话）、`agent_id` | • 写入：`messages`（对话历史）、`project_ids`（技能/事实分类）、`profile_schema`（画像模板）<br>• 检索：`messages`（查询意图）、`memory_types`（`observation`/`skill`/`user_profile`）、`top_k` | • Embedding：纯文本数组、或 `contents` 多模态混合数组（含 `text`/`image`/`video` 字段）<br>• Rerank：`query` + `documents` 数组（支持文本或结构化多模态对象） |
| **输出格式** | • 检索：`{ "results": [{ "chunk_id", "content", "score" }] }`<br>• 问答：流式 `SSE` 或 JSON 格式响应，含 `answer`、`references`（引用切片） | • 写入：异步 `event_id` 或同步 `memory_node_id`<br>• 检索：`{ "nodes": [{ "id", "type", "content", "score", "metadata" }] }`<br>• 查询画像：结构化 `user_profile` 对象（按 schema 定义） | • Embedding：`{ "data": [{ "embedding": [...], "index": 0 }] }`（同步）或[异步任务](../concepts/asynchronous-task.md) ID<br>• Rerank：`{ "results": [{ "index": 0, "relevance_score": 0.92 }] }` |
| **支持模型（可配置性）** | • 嵌入模型：`text-embedding-v4`, `qwen3-vl-embedding`（创建知识库时指定）<br>• 重排序模型：`qwen3-rerank`（知识库级或 Agent 级配置）<br>• 问答模型：`qwen3.7-plus`（Agent 配置） | • 抽取模型：由 `plan_version`（`pro`/`lite`）隐式控制，`pro` 版使用更高质量抽取与 Rerank 模型<br>• 不暴露显式模型名，模型能力与记忆类型强绑定 | • 文本嵌入：`qwen3.7-text-embedding`, `text-embedding-v4`, `text-embedding-v3`<br>• 多模态嵌入：`qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06`<br>• 排序模型：`qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank`（支持 `instruct`） |
| **API 端点归属** | DashScope 应用网关（`/api/v1/indices/knowledge/search`, `/api/v2/apps/knowledge/chat`）<br>• 管理类：`/api/v1/indices/rag/...`<br>• 运行时：`/api/v1/indices/knowledge/...` & `/api/v2/apps/knowledge/...` | 独立记忆服务网关（`/api/v2/apps/memory/...`）<br>• 写入：`POST /add`, `/add-async`<br>• 检索：`POST /memory_nodes/search`<br>• 管理：`GET /memory_nodes`, `DELETE /memory_nodes/{id}` | 模型服务网关（兼容 OpenAI / DashScope 原生）<br>• 同步 Embedding：`/v1/embeddings`（OpenAI 兼容）或 `/api/v1/services/embedding`<br>• 异步 Embedding：`/api/v1/services/embedding-async`<br>• Rerank：`/v1/rerank`（OpenAI 兼容）或 `/api/v1/services/rerank` |
| **鉴权方式** | `Authorization: Bearer <API-Key>` + `workspace_id`（拼入 Base URL） | `Authorization: Bearer <DASHSCOPE_API_KEY>` + `workspace_id`（拼入 Base URL） | `Authorization: Bearer <API-Key>` + `workspace_id`（拼入 Base URL）<br>• 注意：部分 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)要求 `base_url` 显式包含 workspace 域名 |
| **计费方式** | • 按知识库调用量（检索/问答 QPS）+ 存储容量（GB/月）计费<br>• Agent 调用消耗 LLM [Token](../concepts/token.md)（`agent_model` 所用模型）<br>• 免费额度有限，生产环境需开通计费 | • 公测期免费（截至 2026-08-20）<br>• 正式计费后分 `Lite` 与 `Pro` 计划：<br>  - `Lite`：基础抽取与检索，无 `min_score` 过滤<br>  - `Pro`：高精度抽取、Rerank 支持、`min_score` 过滤、画像增强 | • 按 [Token](../concepts/token.md) 数计费（Embedding 输入长度、Rerank 总输入 [Token](../concepts/token.md)）<br>• 异步批量任务按文件处理量计费<br>• 地域差异大：北京地域部分模型享免费额度（如 `qwen3.7-text-embedding` 100万 Token），新加坡无 |
| **典型场景** | • 企业内部知识库问答（产品文档、客服FAQ、制度手册）<br>• 行业垂类 Agent（法律条文解读、医疗指南查询）<br>• 需版本管理、权限控制、人工审核的知识服务 | • 智能客服中持续积累用户偏好与历史诉求（`observation`）<br>• 工具调用后自动沉淀可复用流程（`skill`）<br>• 基于对话动态构建用户画像（`user_profile`），驱动个性化推荐 | • 自建 RAG 系统的向量化模块（替代开源模型）<br>• 多模态搜索（图文混合检索、视频关键帧匹配）<br>• 对召回结果做二次精排（如：在 Elasticsearch 返回 Top 100 后用 `qwen3-rerank` 重排 Top 5）<br>• 聚类、去重、相似性分析等 NLP 基础任务 |

## 各方案适用场景建议

| 方案 | 推荐采用场景 | 不推荐采用场景 | 关键提醒 |
|------|--------------|----------------|----------|
| **RAG API** | ✅ 需快速上线一个具备知识管理后台、支持文档上传/切片/审核、并对外提供问答 API 的业务系统。<br>✅ 业务知识高度结构化、更新频率低（周/月级）、需与现有 LLM 应用解耦集成。<br>✅ 要求开箱即用的混合检索（关键词+向量）、重排序、引用溯源能力。 | ❌ 需要实时捕获每轮对话中的细微意图变化并即时反馈。<br>❌ 知识来源高度动态（如每分钟新增数百条工单记录），且需毫秒级写入与检索。<br>❌ 仅需底层向量能力，不愿承担知识库元数据管理复杂度。 | • 必须通过 **Agent 发布**才能调用运行时接口，不可直接对知识库 ID 请求检索。<br>• 参数命名不一致（`index_id` vs `indexId`）易引发集成错误，建议封装 SDK 层统一处理。<br>• 检索结果默认不带原始文档元信息（如标题、URL），需在切片导入时通过 `custom_metadata` 显式注入。 |
| **长期记忆（New）** | ✅ 构建具备“记忆”的对话式 Agent，需跨会话记住用户习惯、承诺事项、技能偏好。<br>✅ 需将工具调用结果（如“已预约会议室A”）自动转化为可检索的结构化技能节点（`skill`）。<br>✅ 有明确用户画像需求，且愿投入 Schema 设计与异步抽取流程。 | ❌ 仅需简单缓存最近几轮对话（可用短期 Session Memory 替代）。<br>❌ 知识来源为静态 PDF/Word，无动态事件流或用户交互上下文。<br>❌ 要求强一致性写入（如金融交易日志），而该服务为最终一致性设计。 | • **必须传 `user_id`**，否则无法隔离不同用户记忆，是安全红线。<br>• `project_ids` 与 `custom_content` 互斥，技能抽取务必用 `project_ids`，勿混用。<br>• 用户画像为异步过程，首次查询可能为空，业务侧需实现重试逻辑（建议 1s/3s/10s 指数退避）。 |
| **向量与排序（Vector & Sort）** | ✅ 自研 RAG 系统，需高性能、高定制化的向量生成与重排能力（如自定义 chunking 策略、私有排序指令）。<br>✅ 多模态应用（如“用这张图找相似商品详情页”），需统一语义空间的跨模态向量。<br>✅ 对延迟极度敏感（<100ms），且请求规模可控（≤20 条/次），需同步低延迟响应。 | ❌ 需要开箱即用的知识库管理界面、文档解析、切片质量监控等运营能力。<br>❌ 无工程能力维护向量数据库（如 Milvus/Pinecone）或检索链路（召回→重排→LLM）。<br>❌ 仅需简单关键词搜索，无需语义理解。 | • 多模态模型向量空间 **不可混用**：`qwen3-vl-embedding` 与 `tongyi-embedding-vision-plus` 输出向量不能直接计算相似度。<br>• `gte-rerank` 系列将于 **2026-05-30 下线**，新项目请直接选用 `qwen3-rerank`。<br>• 异步向量任务有严格并发限制（运行中 ≤3，排队+运行中 ≤50），海量数据需做好任务调度。 |

## 面向开发者的技术选型参考

作为百炼平台的开发者，在设计智能体或知识增强系统时，请按以下逻辑进行技术选型：

1. **先明确数据性质与生命周期**  
   - 若数据是**静态、权威、需人工维护**的业务知识（如合同模板、操作手册）→ 优先评估 **RAG API**；  
   - 若数据是**动态、事件驱动、源自对话或工具调用**的上下文信息（如“用户说喜欢咖啡”、“已帮用户订机票”）→ 优先评估 **长期记忆**；  
   - 若你已在自建向量数据库、或需将向量能力嵌入现有检索链路（如 ES + Rerank）→ 直接调用 **向量与排序**。

2. **再判断集成深度与控制粒度需求**  
   - 要求**零运维、快速上线、带 UI 管理后台** → RAG API 是最优解；  
   - 要求**完全掌控检索全流程**（自定义分词、混合召回、多级重排、结果融合）→ 向量与排序 + 自研向量库是唯一选择；  
   - 要求**在 Agent 中自然沉淀对话状态，并支持 Schema 化画像** → 长期记忆提供最契合的抽象。

3. **最后验证能力边界与演进风险**  
   - RAG 的重排序能力绑定

## 被对比主题页

- [rag api](../api/rag-api.md)
- [long term memory new](../api/long-term-memory-new.md)
- [vector and sort](../api/vector-and-sort.md)


