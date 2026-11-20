# RAG、[长期记忆](../concepts/long-term-memory.md)与向量检索排序能力对比

本对比旨在帮助开发者清晰区分百炼平台三大核心语义增强能力：**RAG API（知识库驱动的端到端问答）**、**[长期记忆](../concepts/long-term-memory.md)（LTM，用户级状态持久化）** 和 **向量与排序（底层嵌入与重排原子能力）**。三者定位不同——RAG 是面向业务场景的“解决方案层”，LTM 是面向用户生命周期的“状态管理层”，而向量与排序是支撑前两者的“基础能力层”。正确理解其边界、耦合关系与适用阶段，是构建高性能、可维护AI应用的关键前提。

## 关键维度对比

| 维度 | RAG API | [长期记忆](../concepts/long-term-memory.md)（LTM） | 向量与排序 |
|------|---------|------------------|-------------|
| **本质定位** | 知识库全生命周期管理 + 检索/问答服务编排能力（含Agent策略） | 用户级结构化上下文持久化与跨会话语义检索能力 | 原子级模型能力：文本/多模态向量化 + 查询-文档相关性重排序 |
| **输入格式** | JSON（含 `agent_id`, `query`, `messages`, `indexId`, `category` 等业务语义参数）；文件上传需三步协议（lease → OSS PUT → addFile） | JSON（含 `memory_id`/`user_id`, `fragment_type`, `content`, `metadata`, `retrieval_mode`）；支持 `profile` 白名单字段或自定义 schema | JSON（严格按模型要求：`text-embedding-*` 接受字符串；`rerank-*` 接受 `{query, documents}` 对象；`multimodal-*` 接受 `{image_url, text}`） |
| **输出格式** | • `/search`：返回 `hits[]`（含 `score`, `content`, `index_id`, `file_name`）<br>• `/chat`：SSE 流式响应（`plan` → `tool_calls` → `message` 三阶段）<br>• 管理接口：标准 REST JSON（如 `index_id`, `job_id`） | • 自动注入：系统角色占位符 `{memory}` 被替换为拼接后的上下文字符串<br>• 显式检索：`GET /v1/memory/retrieve` 返回 `fragments[]`（含 `id`, `content`, `metadata`, `score`）<br>• 写入/更新：返回 `fragment_id` 与 `created_at` | • 向量：`output.embeddings: [float32[]]`（单条或多条）<br>• 重排：`output.results: [{index, relevance_score, document}]`（按分数降序） |
| **支持模型** | • 知识库构建：`text-embedding-v3/v4`, `qwen3.7-text-embedding`, `qwen3-vl-embedding`<br>• 问答引擎：绑定 Agent 所配大模型（如 `qwen-max`）<br>• 重排：`qwen3-rerank`（由 Agent 配置隐式启用） | • 仅 `qwen-max-2025-03+` 及标注 `ltm-enabled` 的模型支持**自动读写**<br>• `qwen-plus/turbo` 仅支持**显式调用 `/v1/memory/retrieve`** 读取 | • 向量：`text-embedding-v1/v3/v4`, `qwen3.7-text-embedding`, `multimodal-embedding-v1`, `qwen3-vl-embedding`<br>• 重排：`rerank-v1`, `qwen3-rerank`（注意：`qwen3-rerank` 为 LTM/RAG 共享模型，但此处为纯能力调用） |
| **API 端点** | 统一业务空间域名：<br>`https://{workspace_id}.cn-beijing.maas.aliyuncs.com`<br>路径前缀：`/api/v1/indices/...`, `/api/v2/apps/knowledge/...`, `/api/v1/connector/dash/...` | 统一 DashScope 域名：<br>`https://dashscope.aliyuncs.com/api/v1`<br>路径：`/v1/memory/fragments`, `/v1/memory/retrieve`, `/v1/memory/profiles` | 统一 DashScope 域名：<br>`https://dashscope.aliyuncs.com/api/v1`<br>路径：`/services/embeddings`, `/services/rerank`, `/services/multimodal-embeddings` |
| **计费方式** | 按调用次数计费：<br>• 知识库管理类（创建/导入/删除）：按次<br>• 检索 `/search`：按次<br>• 问答 `/chat`：按 token（输入+输出）<br>• Agent 运行时资源另计（见控制台配额） | 按写入/读取分片次数计费：<br>• `POST /fragments`：按次<br>• `GET /retrieve`：按次<br>• `PUT/DELETE`：按次<br>• 存储不额外计费（按 TTL 自动清理） | 按调用次数计费：<br>• 向量：按 `input` 条目数（单次请求可批量）<br>• 重排：按 `(query + documents)` 总数计费（`rerank-v1` 单次最多 100 docs） |
| **状态管理** | • **无会话状态**：`/chat` 接口不维护历史，客户端必须传入完整 `messages` 数组<br>• Agent 配置为独立实体（草稿/发布双版本），变更需重新部署 | • **强用户隔离**：`memory_id` 或 `user_id` 为硬性隔离键，不可跨 ID 访问<br>• 支持 TTL 自动过期，`profile` 分片自动归一化 | • **完全无状态**：每次请求独立处理，无缓存、无上下文依赖、无 side effect |
| **典型场景** | • 客服知识库问答（PDF/Word/网页）<br>• 表格数据自然语言查询（SQL 生成）<br>• 图片/音视频内容语义搜索（如“找去年会议中展示架构图的PPT”）<br>• 多知识库联合检索（如“从产品文档+工单记录中找故障原因”） | • 个性化推荐（基于用户历史偏好/设备信息/地域）<br>• 对话连续性保障（“上次说要买MacBook，这次推荐M4芯片款”）<br>• 用户画像动态构建（实时聚合行为摘要）<br>• B2C 场景下跨 App/Session 的上下文继承 | • 自建向量数据库的 embedding 生成<br>• 对 Elasticsearch/Chroma 等检索结果做二次精排<br>• 多路召回（BM25 + 向量）后融合打分<br>• 文档片段相似度比对（如查重、版本差异分析） |

## 各方案的适用场景建议

### ✅ 选 RAG API 当：
- 你拥有**结构化或非结构化的企业知识资产**（如产品手册、API 文档、内部 Wiki、会议纪要），需快速构建可检索、可问答的知识服务；
- 你需要**开箱即用的多源混合检索能力**（文档+表格+图片+音视频），且不愿自行搭建向量库、切片逻辑与混排策略；
- 你依赖**Agent 编排能力**实现复杂工作流（如先查知识库→再调用工具→最后生成报告）；
- 你追求**低代码集成**：通过控制台配置 Agent 即可发布服务，API 调用简洁（只需 `agent_id` + `query`）。

### ✅ 选 长期记忆（LTM） 当：
- 你的应用需要**记住用户个体特征**（如语言偏好、购买历史、客服对话摘要），并在后续任意会话中自动复用；
- 你正在构建**高个性化体验的产品**（如智能导购、学习助手、健康顾问），且用户身份明确（有 `user_id`）；
- 你需要**轻量级、免运维的状态存储**，替代自建 Redis/PostgreSQL + 向量扩展的复杂方案；
- 你接受**平台托管的语义检索**（而非自己控制 embedding 模型与索引），且模型兼容性已满足（优先使用 `qwen-max-2025-03+`）。

### ✅ 选 向量与排序 当：
- 你已在使用**自研或第三方向量数据库**（如 Milvus、Qdrant、PGVector），仅需百炼提供高质量 embedding 或 rerank 模型；
- 你需要**完全掌控检索链路**：自主决定切片策略、索引结构、召回算法（BM25/向量/混合）、重排时机与粒度；
- 你有**特殊输入需求**（如直接传入图像二进制、长文档分段向量化、多 query 并行 rerank）；
- 你正在做**模型能力评测或 A/B 实验**（如对比 `text-embedding-v4` vs `qwen3.7-text-embedding` 在特定领域效果）。

## 技术选型参考（面向开发者）

| 选型目标 | 推荐方案 | 关键理由 | 注意事项 |
|----------|----------|----------|----------|
| **最快上线一个知识问答 Bot** | RAG API | 控制台 5 分钟创建知识库 + 发布 Agent，API 仅需 2 个请求（search/chat）即可交付；内置切片、向量化、重排、多源路由全栈能力 | 需适配参数命名不一致问题（`indexId` vs `index_id`）；Agent 配置变更需重新发布 |
| **构建用户专属智能体（如个人助理）** | LTM + RAG API 组合 | LTM 存储用户画像与历史摘要，RAG 提供领域知识；在 `/chat` 请求中将 LTM 注入的上下文作为 system message 传入，实现“个性+专业”双增强 | `qwen-plus` 等模型无法自动注入，需显式 retrieve + 拼接；profile 字段名必须白名单 |
| **已有向量库，仅需升级 embedding 质量** | 向量与排序 | 直接替换原有 embedding 模型调用，无需改造索引结构；支持批量请求，吞吐更高 | 注意 `text-embedding-v1` 输入截断至 512 token，长文档需预切片 |
| **对检索结果做精准可控的二次排序** | 向量与排序（rerank） | 绕过 RAG Agent 的黑盒重排，自主传入 top-K 候选，获得透明分数；支持 `rerank-v1` 等轻量模型降低延迟 | `rerank-v1` 不支持图像/JSON 输入，纯文本场景首选；单次最多 100 docs |
| **多模态内容理解（图文混合检索）** | RAG API（`image` 类型知识库） 或 向量与排序（`multimodal-embedding-v1`） | RAG 提供端到端闭环（上传图片→自动向量化→语义搜索）；向量 API 提供更灵活输入（如动态拼接图文描述） | 当前 `multimodal-embedding-v1` 仅支持 `image_url`，不支持 `image_bytes`；RAG 中视觉场景必须指定 `multimodalEmbeddingModelName` |

> **重要协同提示**：三者并非互斥，而是分层协作关系——  
> - **向量与排序** 是底层能力，被 RAG 和 LTM **内部调用**（如 RAG 创建知识库时调用 `text-embedding-v4`，LTM 检索时调用 `qwen3-rerank`）；  
> - **RAG** 与 **LTM** 可在同一请求中组合使用：将 LTM 检索出的用户上下文作为 `system` message 注入 RAG `/chat` 请求，实现“用户个性 + 企业知识”的双重增强；  
> - **避免重复建设**：若已用 RAG 构建了产品文档知识库，无需再用向量 API 为其生成 embedding；同理，LTM 的 profile 检索已内置语义能力，勿自行调用向量 API 实现相同逻辑。  

选择的本质，是权衡 **开发效率**（RAG）、**状态治理成本**（LTM）与 **技术栈控制力**（向量与排序）。建议从 MVP 场景出发，优先使用 RAG 快速验证价值，再根据个性化、性能或架构演进需求，渐进式引入 LTM 或向量与排序能力。

## 被对比主题页

- [rag api](../api/rag-api.md)
- [long term memory new](../api/long-term-memory-new.md)
- [vector and sort](../api/vector-and-sort.md)


