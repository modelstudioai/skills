# RAG、[长期记忆](../concepts/memory.md)与向量检索排序能力对比

本对比旨在帮助开发者清晰区分百炼平台三大核心语义增强能力的定位、边界与协同关系：**RAG API**（面向知识库驱动的端到端问答服务）、**[长期记忆](../concepts/memory.md)（Long Term Memory）**（面向用户/项目级结构化记忆的生命周期管理）、**向量与排序（Vector & Sort）**（面向底层语义表征与重排的原子能力）。三者并非互斥替代，而是分层协作：向量与排序是 RAG 和[长期记忆](../concepts/memory.md)的**技术底座**；RAG 是面向业务知识场景的**封装服务**；长期记忆则是面向 Agent 智能体持续演化的**状态中枢**。准确理解差异，是构建可扩展、可维护、可计费的 AI 应用的关键前提。

## 关键维度对比

| 维度 | RAG API | 长期记忆（New） | 向量与排序（Vector & Sort） |
|------|---------|------------------|----------------------------|
| **核心定位** | 知识库全生命周期管理 + 语义检索/问答一体化服务（SaaS 化能力封装） | 用户/项目级结构化记忆（observation/skill/profile）的写入、检索、更新与画像构建（状态管理服务） | 文本/多模态向量化（embedding）与语义相关性重排（rerank）的原子模型能力（PaaS 基础设施） |
| **输入格式** | • 检索/问答：`query`（文本/图片）、`messages`（对话历史）、`agent_id`<br>• 知识库管理：`docIds`/`categoryIds`、OSS 文件元数据、`sourceType` 分支参数<br>• 多模态：支持 `image_url`、`video_url` 等字段 | • 写入：`messages`（含 text/image/video）、`custom_content`、`profile_schema`、`project_ids`<br>• 检索：`query`（文本）、`memory_types`、`min_score`（Pro 版）、`user_id`<br>• 画像：`schema_id` + `user_id` | • 向量：`input`（string/array/file 或 `{"contents": [...]}`）<br>• 排序：`{"query": "...", "documents": [...]}`（支持混合模态文档）<br>• 支持 OpenAI 兼容格式（如 `/v1/embeddings`） |
| **输出格式** | • 检索：`{ "results": [{ "doc_id", "content", "score", "metadata" }] }`<br>• 问答：流式 `text/event-stream`（含 `plan`/`tool_call`/`answer` 三阶段事件）<br>• 管理：标准 REST JSON（含 `index_id`, `chunk_id`, `request_id`） | • 写入：`event_id`（异步）或 `memory_node_id`（同步）<br>• 检索：`{ "nodes": [{ "id", "type", "content", "score", "project_id" }] }`<br>• 画像：结构化 JSON（按模板定义的字段）<br>• 所有响应含统一 `request_id` | • 向量：`{ "data": [{ "embedding": [...], "index": 0 }], "usage": {...} }`（支持 `base64` 编码）<br>• 排序：`{ "results": [{ "index", "relevance_score", "document" }] }`（`return_documents=true` 时返回原文） |
| **支持模型/能力** | • **不直接暴露模型**，通过 Agent 封装：<br> – 向量模型：`text-embedding-v4`, `qwen3-vl-embedding` 等（配置在 Agent）<br> – 重排模型：`qwen3-rerank`（配置在 `kb_search_configs`）<br> – LLM：`qwen3.7-plus`（用于问答生成）<br>• 四类知识库：`unstructured`/`structured`/`image`/`multimedia` | • **不绑定特定模型**，记忆抽取由后台策略执行：<br> – 抽取逻辑透明（`intelligent` 模式），开发者不可选模型<br> – 技能导出、画像生成为黑盒服务<br>• 支持 `project_ids` 路由，但无显式模型参数 | • **显式模型选择**：<br> – 向量：`qwen3.7-text-embedding`, `text-embedding-v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06`<br> – 排序：`qwen3-rerank`, `qwen3.7-text-rerank`, `qwen3-vl-rerank`<br>• 支持 `instruct` 自定义任务指令、`enable_fusion` 控制融合模式 |
| **API 端点（典型）** | • 知识库管理：`/api/v1/indices/knowledge/create_v2`<br>• 检索：`/api/v1/indices/knowledge/search`（需 `agent_id`）<br>• 问答：`/api/v2/apps/knowledge/chat`（强制 `stream: true`） | • 写入：`POST /api/v2/apps/memory/add-async`<br>• 检索：`POST /api/v2/apps/memory/memory_nodes/search`<br>• 画像：`GET /api/v2/apps/memory/profile_schemas/{schema_id}/user_profile` | • 向量（同步）：`/api/v1/services/embeddings/text-embedding/text-embedding`<br>• 向量（异步）：`/api/v1/services/embeddings/text-embedding/text-embedding` + `X-DashScope-Async: enable`<br>• 排序：`/api/v1/services/rerank/text-rerank/text-rerank` |
| **鉴权方式** | `Authorization: Bearer <API-Key>`（百炼平台 API Key）<br>Base URL 含 `{workspace_id}` | `Authorization: Bearer $DASHSCOPE_API_KEY`（DashScope API Key）<br>Endpoint 含 `{WorkspaceId}`（业务空间 ID） | `Authorization: Bearer $DASHSCOPE_API_KEY`（DashScope API Key）<br>支持 OpenAI 兼容 Header（`Authorization: Bearer sk-xxx`） |
| **计费方式** | • **按调用次数计费**：<br> – 知识库管理接口（创建/删除/同步）：按次<br> – 检索/问答接口：按“每 10 秒请求数”计费（非 QPS）<br>• 无免费额度说明（依赖所配 Agent 的模型计费） | • **商业化起始时间明确**：2026 年 8 月 20 日 10:00（北京时间）起正式计费<br>• 分版本计费：<br> – `Lite`：基础检索（无 `min_score`/Rerank）<br> – `Pro`：支持过滤、重排、高并发<br>• 当前处于免费试用期 | • **按 Token/请求计费**：<br> – 文本向量：按输入 Token 计费（`qwen3.7-text-embedding` 等享北京地域 100 万 Token 免费额度）<br> – 多模态向量：按输入内容复杂度计费<br> – 排序：按 `query + documents` 总 Token 计费<br>• 明确标注各模型 Token 上限（如 `text-embedding-v4`: 8,192 Token/行） |
| **典型场景** | • 企业知识库问答（产品文档、内部 SOP）<br>• 客服机器人（多轮对话+知识引用）<br>• 多源异构数据联合检索（文档+数据库+图片）<br>• 需要开箱即用、带安全策略（拒答/防泄漏）的生产服务 | • Agent 智能体长期状态维护（记住用户偏好、会议安排、技能步骤）<br>• 用户画像动态构建（消费习惯、兴趣标签、角色权限）<br>• 项目级经验沉淀（`project_ids` 隔离，跨会话复用技能）<br>• 需要结构化存储、支持软删除与异步抽取的场景 | • 构建自定义 RAG 流水线（自主选择 embedding + rerank 模型）<br>• 批量预处理知识库文档（异步向量化）<br>• 跨模态搜索系统（图文混合检索、视频关键帧匹配）<br>• 对延迟/成本/模型精度有精细化控制需求的场景 |

## 各方案适用场景建议

### ✅ 优先选用 RAG API 当：
- 你希望**快速上线一个知识问答应用**，无需自行搭建向量库、设计检索流程、集成 LLM；
- 你的知识源是**结构化文档（PDF/Word/Excel）或多媒体文件**，且需要开箱即用的解析、切片、多模态检索能力；
- 你需要**企业级保障**：内置安全策略（敏感信息过滤、拒答控制）、统一监控（QPS/存储）、细粒度权限（业务空间隔离）；
- 你接受**Agent 封装带来的抽象**，不追求对 embedding/rerank 模型的逐层调试与替换。

> 📌 *典型误用*：试图用 RAG API 替代长期记忆来存储用户个性化状态（如“用户喜欢蓝色主题”），因其知识库设计面向静态知识，缺乏 `user_id`/`project_id` 一级隔离与动态画像能力。

### ✅ 优先选用长期记忆（New）当：
- 你在构建**具备记忆能力的智能体（Agent）**，需要跨会话记住用户事实（`observation`）、固化操作流程（`skill`）、构建动态画像（`user_profile`）；
- 你需要**多租户/多项目隔离**，且记忆数据需与具体 `user_id` 和 `project_ids` 强绑定；
- 你接受**抽取逻辑黑盒化**，更关注“存什么、查什么”，而非“如何向量化、如何重排”；
- 你计划在 2026 年 8 月后持续运营，且愿意采用 `Pro` 版本获取 `min_score` 过滤与 Rerank 支持。

> 📌 *典型误用*：用长期记忆替代向量与排序服务做通用语义搜索（如“在 10 万篇新闻中找相似报道”），因其未提供大规模向量索引（如 FAISS/Milvus）托管，仅支持基于向量相似度的轻量级检索。

### ✅ 优先选用向量与排序（Vector & Sort）当：
- 你正在**自研 RAG 框架或高级搜索系统**，需要自由组合不同 embedding 模型（如用 `text-embedding-v4` 做文档向量，`qwen3-vl-embedding` 做图片向量）与 rerank 模型（如用 `qwen3-rerank` 重排图文混合结果）；
- 你需要**超大批量离线处理**（如每日同步 50 万份合同 PDF 的向量化），依赖异步批处理能力；
- 你对**延迟、Token 成本、模型精度有极致要求**，需逐个测试 `qwen3.7-text-embedding` vs `text-embedding-v4` 的效果与性价比；
- 你已有向量数据库（如 Milvus/Pinecone），仅需百炼提供高质量向量生成与重排服务。

> 📌 *典型误用*：直接调用向量与排序 API 构建用户问答界面——它不提供 LLM 生成、不管理知识库、不处理对话状态，必须自行补全完整链路。

## 技术选型参考（面向开发者）

| 你的需求 | 推荐方案 | 关键理由 | 注意事项 |
|----------|----------|----------|----------|
| **从零启动一个客服知识库，2 周内上线** | ✅ RAG API | 提供端到端闭环：上传文档 → 创建知识库 → 配置 Agent → 调用问答接口。免去向量库选型、LLM 集成、安全策略开发。 | 务必提前规划 `agent_id` 生命周期；注意 `delete-index` 为不可逆操作。 |
| **为对话机器人添加“记住用户生日”“掌握报销流程”能力** | ✅ 长期记忆（New） | 原生支持 `user_id` 隔离、`skill` 类型、异步抽取，与 Agent 运行时天然契合。`AddMemoryAsync` 可并行处理多项目记忆。 | `AddMemory` 同步接口在复杂抽取时可能超时，务必优先用 `AddMemoryAsync`；画像首次查询需等待异步完成。 |
| **构建跨模态电商搜索（用户拍图搜同款+文字描述优化）** | ✅ 向量与排序 + 自研索引 | `

## 被对比主题页

- [rag api](../api/rag-api.md)
- [long term memory new](../api/long-term-memory-new.md)
- [vector and sort](../api/vector-and-sort.md)


