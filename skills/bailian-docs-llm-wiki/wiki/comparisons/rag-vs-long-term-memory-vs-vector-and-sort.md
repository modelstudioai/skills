# RAG、长期记忆与向量检索排序能力对比

为帮助开发者在百炼平台中高效选型，本文对三大核心检索增强能力——**RAG（知识库服务）**、**长期记忆（Long Term Memory）** 和 **向量与排序（Embedding & Rerank）** 进行系统性对比。三者虽均基于语义向量技术，但在设计目标、抽象层级、数据模型、运行机制及适用边界上存在本质差异。本对比聚焦实际工程落地维度，涵盖接口形态、能力边界、计费逻辑与典型模式，旨在为知识增强型应用（如智能客服、Agent 系统、个性化助手）提供清晰的技术决策依据。

| 维度 | RAG（Knowledge API） | 长期记忆（Long Term Memory） | 向量与排序（Vector & Sort） |
|------|------------------------|------------------------------|-------------------------------|
| **核心定位** | 面向**结构化/非结构化知识库**的端到端管理与问答服务，强调“知识即服务”（KaaS） | 面向**用户个体状态与经验沉淀**的记忆建模服务，强调“记忆即资产”（MaaS） | 面向**底层语义计算能力**的原子化工具集，强调“向量即原语”（VaaS） |
| **输入格式** | - 知识库：支持 PDF/DOCX/TXT/CSV/图像/音视频等多源文件上传<br>- 检索/问答：`query`（文本）、`images`（base64 或 URL）、`input.messages`（对话上下文） | - 写入：`messages`（含 `role`/`content`/`image_url`）、`user_id`、`project_ids`、可选 `profile_schema`<br>- 检索：`messages`（当前会话输入）+ `user_id` + 过滤参数 | - 向量：`input` 为字符串或字符串数组（文本），或 `{ "image": "...", "text": "..." }`（多模态）<br>- 排序：`{ "query": "...", "documents": [...] }` |
| **输出格式** | - 检索：返回带 `score`、`chunk_id`、`source` 的结构化结果列表<br>- 问答：流式或非流式 JSON 响应，含 `answer`、`references`、`agent_trace` 等字段 | - 写入：异步返回 `event_id`，轮询得 `memory_node_id`<br>- 检索：返回 `memory_nodes` 数组，含 `id`、`type`（`observation`/`skill`/`user_profile`）、`content`、`score`、`metadata` | - 向量：`data: [{ "embedding": [...], "index": 0 }]`<br>- 排序：`results: [{ "index": 1, "relevance_score": 0.92 }]`（按相关性降序） |
| **支持模型** | - 嵌入模型：`text-embedding-v4`、`qwen3.7-text-embedding` 等（知识库创建时指定）<br>- 重排模型：`qwen3-rerank` 等（可选启用）<br>- 问答模型：由绑定 Agent 的 LLM 决定（如 Qwen3） | - 抽取模型：由平台统一调度，不暴露模型名；`plan_version=pro` 时隐式启用更优抽取与 rerank 能力<br>- 无用户可选模型配置项 | - 文本嵌入：`text-embedding-v1` / `v2`<br>- 多模态嵌入：`multimodal-embedding-v1`<br>- 排序：`rerank-v1`（快）、`rerank-v2`（长文档支持） |
| **API 端点** | - Base URL：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com`<br>- 关键路径：<br> • `/api/v1/indices/rag/index/create_v2`（建库）<br> • `/api/v1/indices/knowledge/search`（检索）<br> • `/api/v2/apps/knowledge/chat`（问答） | - Base URL：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory`<br>- 关键路径：<br> • `/add_memory_async`（写入）<br> • `/search_memory`（检索）<br> • `/get_user_profile`（画像） | - 全局统一入口：<br> • `https://dashscope.aliyuncs.com/api/v1/services/embeddings`<br> • `https://dashscope.aliyuncs.com/api/v1/services/rerank`<br>- **不依赖 workspace_id**，与业务空间解耦 |
| **计费方式** | - 按**知识库调用量**计费：<br> • 文档解析（页数/时长）<br> • 检索请求（QPS/次数）<br> • 问答 [Token](../concepts/token.md)（输入+输出）<br>- 旗舰版含 Wiki、Agent 高级策略等增值功能 | - **商业化计费起始日：2026年8月20日**<br>- 分 `Lite` 与 `Pro` 版本：<br> • `Lite`：基础写入/检索，无 `min_score` 过滤<br> • `Pro`：支持 `min_score`、rerank、多项目联合抽取<br>- 计费粒度：`Add` / `Search` 请求次数 | - 按**调用次数 + 输入长度**计费：<br> • 向量：按 `input` 条目数 + token 数（文本）或图像尺寸（多模态）<br> • 排序：按 `documents` 数量 + query 长度<br>- 无版本区分，模型即服务（Model-as-a-Service） |
| **典型场景** | - 企业知识库问答（产品文档、内部 SOP）<br>- 多模态内容搜索（PPT 图表检索、培训视频关键帧定位）<br>- 基于 Wiki 的自动知识图谱构建与推理 | - 用户个性化助手（记住偏好、日程、设备习惯）<br>- Agent 技能持续学习（将成功[工具调用](../concepts/tool-calling.md)沉淀为 `skill` 记忆）<br>- 动态用户画像构建（结合对话与行为生成结构化 profile） | - 自研 RAG 系统的向量化组件（替代本地 Sentence-BERT）<br>- 搜索引擎相关性优化（对 BM25 初筛结果做 rerank）<br>- 多模态推荐系统（图文联合表征） |

## 各方案的适用场景建议

### ✅ 优先选用 **RAG（Knowledge API）** 当：
- 你拥有**静态、批量、领域明确的知识资产**（如 1000 份 PDF 手册、500 张产品截图），需快速构建可检索、可问答的知识服务；
- 业务要求**开箱即用的完整链路**：从文档上传、切片、嵌入、检索到生成答案，无需自行编排 Embedding/Rerank/LLM 调用；
- 需要**多模态混合检索**（例如“找出上周会议 PPT 中关于预算的图表”）或**结构化数据问答**（如 Excel 表格中的销售趋势查询）；
- 团队缺乏 NLP 工程能力，但需快速上线知识增强型应用。

### ✅ 优先选用 **长期记忆（Long Term Memory）** 当：
- 你的应用核心是**与用户长期交互的智能体（Agent）**，需动态积累并复用用户专属事实（“用户小王怕辣”）、技能（“小王订餐习惯：先查优惠再下单”）和画像（“Z 世代，科技爱好者，常驻北京”）；
- 需要**跨会话、跨项目共享记忆**，且记忆具有强生命周期管理需求（如自动过期、按项目隔离）；
- 你已具备基础 Agent 框架（如 AgentScope），仅需一个**高可靠、低延迟、语义感知的记忆后端**，而非从零实现向量存储与检索；
- 场景涉及**敏感信息沉淀**（如医疗咨询记录），需平台级权限隔离（`user_id` + `project_ids` 双重沙箱）。

### ✅ 优先选用 **向量与排序（Vector & Sort）** 当：
- 你正在**自研 RAG 或搜索系统**，需要灵活控制 Embedding/Rerank 模型选型、参数与调用链路；
- 需要**极致性能与可控性**：例如在边缘设备预计算向量、在服务端做轻量级 rerank、或对特定 domain 微调后部署私有模型（此时可将百炼 API 作为 baseline 对比）；
- 应用场景**不依赖平台知识库管理能力**，仅需原子化语义计算（如：对商品评论做情感聚类、对短视频标题做相似去重）；
- 你已有成熟的向量数据库（如 Milvus、PGVector），仅需百炼提供**高质量、免运维的向量生成与重排能力**作为增强模块。

## 面向开发者的选型参考

| 你的问题 | 推荐方案 | 关键理由 |
|----------|-----------|-----------|
| “我有一批产品手册 PDF，想让客服机器人能准确回答‘如何重置设备？’” | **RAG** | 知识库一键导入 + `document` 场景 + Agent 问答，5 分钟可上线，无需处理切片/向量化细节。 |
| “我的 AI 助手需要记住用户每次说‘别提醒我开会’，并在下次自动过滤日程通知” | **长期记忆** | `observation` 类型天然匹配临时偏好；`user_id` 隔离确保隐私；异步写入避免阻塞主流程。 |
| “我在用 LangChain 构建 RAG，现有 OpenAI embeddings 效果不佳，想换百炼的 `text-embedding-v4`” | **向量与排序** | 直接替换 Embeddings 类，调用 `/services/embeddings` 即可，零侵入现有架构。 |
| “我要对 10 万条用户评论做聚类，需先统一向量化” | **向量与排序** | 批量调用 `input` 数组（单次最多 2048 tokens × N 条），比逐条 RAG 检索高效 100 倍。 |
| “用户问‘我上次说的旅行计划是什么？’，需关联历史多轮对话” | **长期记忆** + **RAG** | 单独用长期记忆存 `observation`；若需结合知识库（如“上次说的日本行程，查下东京地铁票价”），则用 RAG 检索外部知识 + 记忆补全上下文。 |
| “我们做金融投顾 App，需对客户风险测评报告做语义搜索，且必须满足等保三级” | **RAG**（私有化部署版） | 百炼企业版支持 VPC 内网访问与审计日志，知识库数据不出域；`table` 场景可精准查询结构化测评字段。 |

> **重要提醒**：  
> - **不要混用同质能力**：RAG 与长期记忆均含向量检索，但 RAG 的检索服务于“知识”，长期记忆服务于“人”；二者数据模型、更新频率、一致性要求完全不同，不可互相替代。  
> - **向量与排序是基础设施，非解决方案**：它不提供存储、不管理生命周期、不处理多模态文件解析——这些必须由上层系统（RAG 或长期记忆）完成。  
> - **计费敏感场景请实测**：`rerank-v2` 的 batch size 限制（1）、`SearchMemory` 的 `min_score` 生效条件（仅 `pro` 版本）等细节，直接影响成本，务必在压测阶段验证。  

通过本对比，开发者可清晰识别：**RAG 是“知识管家”，长期记忆是“个人秘书”，向量与排序是“语义引擎”**。合理分层使用三者，方能构建既强大又可持续演进的智能应用。

## 被对比主题页

- [rag api](../api/rag-api.md)
- [long term memory new](../api/long-term-memory-new.md)
- [vector and sort](../api/vector-and-sort.md)


