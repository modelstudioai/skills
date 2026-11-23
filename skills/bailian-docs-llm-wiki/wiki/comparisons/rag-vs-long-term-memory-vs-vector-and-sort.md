# RAG、[长期记忆](../concepts/long-term-memory.md)与向量检索排序能力对比

本对比旨在帮助开发者清晰理解百炼平台三大核心语义基础设施——**RAG API**、**[长期记忆](../concepts/long-term-memory.md)（Long Term Memory）** 和 **向量与排序（Vector & Sort）** 在定位、能力边界、技术实现与工程适配性上的本质差异。三者虽均依赖向量表示与语义匹配，但设计目标迥异：RAG 面向**知识库驱动的问答系统构建**，[长期记忆](../concepts/long-term-memory.md)聚焦**Agent 上下文的结构化持久化与个性化建模**，而向量与排序则提供**原子级、可组合的底层嵌入与重排能力**。本文不替代各模块独立文档，而是从技术选型视角提炼关键决策因子，助力架构设计与接口集成。

## 关键维度对比

| 维度 | RAG API | 长期记忆（New） | 向量与排序（Vector & Sort） |
|------|---------|------------------|----------------------------|
| **核心定位** | 知识库全生命周期管理 + 语义检索/问答服务（端到端应用层） | Agent 的结构化记忆存储与上下文增强（中间件层） | 原子化向量化（Embedding）与重排序（Rerank）能力（基础能力层） |
| **输入格式** | 支持多模态混合输入：<br>• 文本（`query`）、<br>• 图片 URL / base64（`image_urls`）、<br>• 结构化数据（`table` 类型知识库）；需绑定预发布 `agent_id` | 以对话消息流（`messages`）为主，支持文本+图片 URL；支持显式传入 `user_id`、`project_id`、`profile_schema` 等上下文标识符 | 严格按能力类型区分：<br>• Embedding：`string[]` 或单图 `{"url": "..."} / {"image": "base64..."}`<br>• Rerank：`{"query": "...", "documents": [...]}` |
| **输出格式** | • 检索：返回带 `score`、`content`、`source` 的文档片段列表<br>• 问答：SSE 流式响应（含规划、工具调用、生成三阶段）<br>• 所有响应含统一错误结构（`error.code`, `request_id`） | • 写入：同步返回 `memory_nodes` 或异步 `event_id`<br>• 检索：返回 `memory_nodes` 列表（含 `type`, `content`, `score`, `metadata`）<br>• 画像：返回结构化 JSON（字段由 `profile_schema` 定义） | • Embedding：`data[i].embedding`（float 数组）+ `object`, `model`<br>• Rerank：`results[i].index`, `results[i].relevance_score`, `results[i].document` |
| **支持模型** | • 嵌入：`text-embedding-v3/v4`, `qwen3.7-text-embedding`, `qwen3-vl-embedding`<br>• 重排：默认 `qwen3-rerank`，支持自定义 `rerankModelName` | • 抽取模型隐式绑定 `project_id` 或 `plan_version`（`pro`/`lite`）<br>• `pro` 版本启用 `qwen3-rerank` 等高阶重排能力<br>• 不暴露底层嵌入模型选择权 | • Embedding：`text-embedding-v1/v2`, `multimodal-embedding-v1`<br>• Rerank：`rerank-v1/v2`<br>• **模型 ID 必须显式指定且与路径强绑定**（如 `/v1/embeddings` 只接受 embedding 模型） |
| **API 端点** | • 管理类：`/api/v1/indices/...`, `/api/v1/documents/...`<br>• 运行时：`/api/v1/indices/knowledge/search`, `/api/v2/apps/knowledge/chat`（需 `agent_id`） | • 写入：`POST /memory_nodes/add`, `POST /memory_nodes/add-async`<br>• 检索：`POST /memory_nodes/search`, `GET /profile_schemas/{id}/user_profile`<br>• 全路径基于 `MEMORY_SERVICE_ENDPOINT`（业务空间专属域名） | • 统一入口：`https://dashscope.aliyuncs.com/api/v1/embeddings`<br>• `https://dashscope.aliyuncs.com/api/v1/rerank`<br>• **不依赖业务空间 ID，全局可用** |
| **计费方式** | 按调用次数计费：<br>• 知识库管理（创建/更新/删除）<br>• 检索（`/search`）与问答（`/chat`）<br>• 监控接口（`/get_index_monitor`）单独计费 | 按调用次数计费（2026年8月20日起生效）：<br>• `add` / `add-async`（写入）<br>• `search`（检索）<br>• `profile_schema` 相关操作<br>• `pro` 版本费用高于 `lite` | 按调用次数计费：<br>• 每次 `/v1/embeddings` 请求计 1 次<br>• 每次 `/v1/rerank` 请求计 1 次<br>• **无版本/能力分级，单价统一** |
| **典型场景** | • 企业知识库问答（产品文档、客服话术）<br>• 多模态内容搜索（图文混搜、音视频摘要）<br>• 基于结构化数据（表格）的自然语言查询 | • Agent 对话历史的记忆沉淀与回溯（如“用户上次说要买咖啡”）<br>• 用户画像动态构建（偏好、身份、设备等）<br>• SOP/技能流程的结构化存储与复用（如“报销审批步骤”） | • 自研 RAG 系统的向量底座（替换默认嵌入）<br>• 搜索引擎结果页（SERP）重排序<br>• 推荐系统召回后精排<br>• 对接第三方向量数据库（如 Milvus、PGVector）的前置处理 |

## 各方案的适用场景建议

- **优先选用 RAG API 当且仅当**：  
  ✅ 你需要快速上线一个**开箱即用的知识问答系统**，且能接受百炼托管的知识库构建、切片、索引、检索、问答全流程；  
  ✅ 业务涉及**多模态（图文/音视频）或结构化（表格）知识**，需平台原生支持；  
  ❌ 不适合需要完全自定义向量索引结构、或必须对接私有向量数据库的深度定制场景。

- **优先选用长期记忆（New）当且仅当**：  
  ✅ 你正在构建 **Agent 应用**，需在多次对话中**跨会话保持用户状态、行为习惯与技能记忆**；  
  ✅ 你需要**结构化、可 Schema 化的用户画像**，并支持动态增删属性与异步抽取；  
  ✅ 记忆需按 `project_id` 实现**多租户/多业务线隔离**；  
  ❌ 不适合用于构建通用文档搜索引擎，因其不提供文档上传、切片、全文检索等 RAG 核心能力。

- **优先选用向量与排序（Vector & Sort）当且仅当**：  
  ✅ 你是**系统架构师或算法工程师**，需将向量化/Rerank 能力作为**可插拔组件**集成进自研系统（如 LangChain、LlamaIndex、内部搜索中台）；  
  ✅ 你需要**最高灵活性**：自由选择模型、控制输入输出格式、批量处理、与自有向量库协同；  
  ✅ 你已具备向量索引、相似度计算、结果融合等工程能力，仅缺高质量嵌入与重排模型；  
  ❌ 不适合直接用于构建终端问答产品——它不提供知识库管理、对话状态维护、Agent 编排等上层能力。

## 面向开发者的技术选型参考

| 你的需求 | 推荐方案 | 关键理由 | 注意事项 |
|----------|----------|----------|----------|
| “我要三天内上线一个客服知识库问答页面” | ✅ RAG API | 提供 `create_index_v2` 一键导入 + `agent_id` 直接调用 `/knowledge/chat`，最小化开发量 | 注意 `agent_id` 需提前发布；监控接口限流极严（QPS=1） |
| “我的 Agent 需记住用户每次对话中的关键事实，并在后续对话中主动引用” | ✅ 长期记忆（New） | 原生支持 `observation` 类型 + `user_id` 隔离 + 异步抽取，专为 Agent 上下文设计 | 默认使用 `efficient` 模式；高精度需 `intelligent` + `add-async`，首次画像查询需重试 |
| “我已有 Milvus 集群，但嵌入质量差，想换百炼的 `qwen3.7-text-embedding`” | ✅ 向量与排序 | 直接调用 `/v1/embeddings` 获取向量，无缝注入自有库；无知识库绑定开销 | 注意 `text-embedding-v2` 输出 2048 维，勿硬编码 1024 |
| “我在 RAG 流程中发现 BM25 初检结果相关性不足，想加一层百炼重排” | ✅ 向量与排序（Rerank） | `/v1/rerank` 接口简洁明确，支持 `top_k` 控制，可插入任意检索 pipeline 后 | `query` 超 512 token 会被静默截断，务必前端预处理 |
| “我需要同时做知识库问答 + 用户画像分析 + 自定义推荐排序” | ⚠️ **组合使用** | RAG API 处理知识问答，长期记忆管理用户画像，向量与排序支撑推荐精排 | 注意三者鉴权方式一致（API Key），但域名不同（RAG/记忆为 workspace 域名，向量为 dashscope 全局域名） |
| “我要求所有数据不出私有云，且必须审计每条知识变更” | ❌ 三者均不适用 | RAG API 与长期记忆均为百炼 SaaS 服务；向量与排序虽为 API，但模型运行在阿里云环境 | 需评估百炼私有化部署方案或切换至开源模型自建 |

> **最后提醒**：  
> - **命名一致性是高频踩坑点**：RAG API 中 `indexId`/`index_id`/`id` 混用，长期记忆中 `project_id`/`project_ids` 互斥，向量 API 中 `model` 字段必须与路径严格匹配——请始终以最新 OpenAPI Spec 为准，勿依赖参数名直觉。  
> - **时间戳单位陷阱**：RAG 的 `get_index_monitor` 要求秒级时间戳，其余多数接口为毫秒级；长期记忆与向量 API 统一使用毫秒级。  
> - **错误重试策略**：三者均返回标准 `429`，但退避策略略有差异——RAG 建议读取 `Retry-After` Header，长期记忆与向量推荐指数退避（1s/2s/4s）。  
> - **未来演进提示**：长期记忆将于 2026 年 8 月起正式商业化；RAG API 的 `qwen3-rerank` 已成事实标准；向量与排序将持续扩展多模态模型族。建议在架构设计中预留模型升级与能力迁移路径。

## 被对比主题页

- [rag api](../api/rag-api.md)
- [long term memory new](../api/long-term-memory-new.md)
- [vector and sort](../api/vector-and-sort.md)


