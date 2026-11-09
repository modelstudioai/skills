# RAG、[长期记忆](../concepts/long-term-memory.md)与知识库能力对比

为帮助开发者在百炼平台上准确选型，本文对 **RAG（[检索增强生成](../concepts/rag.md)）能力**、**[长期记忆](../concepts/long-term-memory.md)（Long Term Memory）服务** 和 **知识库（Knowledge Base）核心载体** 三类关键能力进行系统性对比。三者虽均面向“外部知识接入与利用”，但在设计目标、数据模型、生命周期、调用范式及适用场景上存在本质差异：  
- **RAG API** 是面向 *应用构建者* 的全链路知识工程接口层，强调可控性、可编排性与多模态检索能力；  
- **[长期记忆](../concepts/long-term-memory.md)** 是面向 *对话智能体（Agent）* 的用户级结构化记忆中枢，聚焦于跨会话的事实沉淀、技能复用与画像演化；  
- **知识库** 是 RAG 能力的 *逻辑封装单元与配置中心*，本身不提供直接 API，而是通过 RAG API 或服务端点被消费，是知识治理的“基础设施”。

以下从技术维度展开对比，供架构设计与集成开发参考。

## 关键能力维度对比

| 维度 | RAG API | 长期记忆（New） | 知识库（Knowledge Base） |
|------|---------|------------------|---------------------------|
| **定位与角色** | **服务集成层**：提供知识库管理、数据导入、联合检索与问答的标准化 REST API，支持端到端自动化编排 | **用户状态层**：以 `user_id` 为中心的记忆节点存储与语义检索服务，支持自动抽取、异步画像、多项目隔离 | **知识治理单元**：RAG 能力的逻辑容器，封装文档、切片、嵌入模型、元数据与索引策略，是能力的“配置实体”而非运行接口 |
| **输入格式** | 支持结构化（JSON 表单）、非结构化（PDF/DOCX/CSV/MP4/JPG 等文件 ID）、多模态（`query` + `images` 数组）；支持 `search_filters`（含嵌套 OR 条件） | 以对话消息流为主（`messages: [{role: "user", content: "..."}, ...]`），支持 `image_url`（仅限启用多模态项目）；支持显式传入 `observation`/`skill` 结构体 | 创建时输入原始文件或数据源（OSS/飞书/数据库等）；配置时定义切片策略、Metadata 字段、标签规则；**无运行时直接输入接口** |
| **输出格式** | 检索返回带 `score`、`content`、`doc_id`、`metadata` 的切片列表；问答返回流式 `answer` + `references`（含 `chunk_id`、`doc_name`）；支持 `rerank_top_n` 控制精排数量 | 返回带 `score` 的记忆节点列表（`observation`/`skill`），含 `id`、`content`、`created_at`、`project_ids`；画像接口返回结构化 JSON（按 `profile_schema` 定义字段） | **不直接输出**；其内容通过 RAG API 的 `/retrieve`、`/search` 或 `/chat` 接口间接输出；Playground 中可预览切片与检索效果 |
| **支持模型** | 显式指定：<br>• `embeddingModelName`（如 `text-embedding-v4`）<br>• `rerankModelName`（如 `qwen3-rerank`）<br>• `multimodalEmbeddingModelName`（如 `qwen3-vl-embedding`）<br>• 问答绑定 `model_id`（如 `qwen3.6-plus`） | 隐式调用：<br>• 记忆抽取依赖内部 `intelligent` 模式模型（未开放选择）<br>• 画像提取使用专用 schema 驱动模型<br>• 检索默认使用向量+关键词混合，`pro` 版本支持重排（模型不可选） | 嵌入模型在创建时绑定且**不可变更**（如 `text-embedding-v4`）；重排与生成模型在**服务层配置**（非知识库本身）；多模态能力由知识库类型（`image`/`multimedia`）触发对应模型栈 |
| **API 端点（核心）** | • 管理：`/api/v1/indices/rag/index/...`<br>• 导入：`/api/v1/connector/dash/...`<br>• 运行时：`/api/v1/indices/knowledge/search`（需 `agent_id`）、`/api/v2/apps/knowledge/chat` | • 写入：`POST /api/v2/apps/memory/add-async`<br>• 检索：`POST /api/v2/apps/memory/memory_nodes/search`<br>• 画像：`GET /api/v2/apps/memory/profile_schemas/{id}/user_profile` | **无独立 API**；所有操作均通过 RAG API 实现：<br>• 创建/查询：`/api/v1/indices/rag/index/...`<br>• 底层检索：`/api/v1/indices/rag/index/retrieve`（需 `index_id`）<br>• 服务调用：`/api/v1/indices/knowledge/search`（需 `agent_id`） |
| **计费方式** | 按调用次数计费：<br>• 知识库创建/更新/删除：免费<br>• 文档导入、切片、向量化：计入 `RAG Processing` 资源包<br>• 检索（`/search`）与问答（`/chat`）：按 token + 调用次数计费，区分基础版/专业版 | 商业化起始时间：**2026年8月20日10:00（北京时间）**<br>• `add` 与 `search` 调用均计费<br>• 分 `lite`（基础检索）与 `pro`（支持 `min_score`、重排）两档计费策略 | **不单独计费**；其成本已包含在 RAG API 的处理与调用费用中。知识库本身为逻辑资源，无存储费用（文档存储按实际用量计费） |
| **典型场景** | • 企业级产品文档智能客服<br>• 多源合同/财报联合分析系统<br>• 音视频培训资料语义搜索平台<br>• Agent 工作流中的动态知识注入节点 | • 对话机器人持续学习用户偏好（如“每次会议后自动发纪要给张经理”）<br>• 技能型 Agent 的行为模板沉淀（如“周报生成”流程）<br>• 用户画像驱动的个性化推荐（生日、职位、常用工具） | • 控制台快速搭建 FAQ 助手（低代码）<br>• 为多个应用复用同一份产品手册知识库<br>• 通过 Metadata 实现版本化文档管理（`v2.1`, `internal_only`）<br>• Playground 中调试切片质量与检索效果 |

## 各方案适用场景建议

| 场景描述 | 推荐方案 | 理由说明 |
|----------|----------|----------|
| **需要将大量 PDF/Word/Excel 文档转化为可检索的知识资产，并对外提供 API 接口供业务系统调用** | ✅ RAG API + 知识库 | RAG API 提供完整的生命周期管理（创建→导入→检索→问答），知识库作为配置实体承载文档与策略，二者协同构成生产级 RAG 应用底座。控制台可快速验证，API 可深度集成。 |
| **构建对话式 AI Agent，需在多轮交互中自动记住用户习惯、任务指令、个性化设置，并支持跨会话调用** | ✅ 长期记忆（New） | 长期记忆专为 Agent 设计：`user_id` 隔离、`observation`/`skill` 类型语义清晰、异步画像支持动态建模。相比手动维护数据库，其语义检索与自动抽取大幅降低开发复杂度。 |
| **已有结构化数据库（如 MySQL），希望用自然语言提问获取结果（如“查上月销售额超50万的客户”）** | ✅ RAG API（`knowledgeType=table`） + 知识库 | 知识库支持 `table` 类型，底层调用 NL2SQL 模型；RAG API 提供 `POST /search` 接口统一接入，无需自行对接数据库与大模型。 |
| **需对同一份知识（如公司制度）按不同部门、权限、版本打标签并分别授权访问** | ✅ 知识库（配合 Tags + Metadata） + RAG API 过滤 | 知识库原生支持 `tags`（字符串数组）与自定义 `metadata_filter`（结构化 JSON）。RAG API 的 `search_filters` 支持按 `tags` 或 `metadata` 字段精确/范围过滤，满足多维权限控制。 |
| **临时调试某份文档的切片效果、向量质量或检索相关性，不涉及上线部署** | ✅ 知识库（控制台 Playground） | 直接在知识库详情页使用 Playground，切换“知识检索”模式输入问题，实时查看召回切片、相似度分数与元数据，零代码快速验证。 |
| **需将用户上传的图片（如设计稿）与文字描述联合检索，回答“这个按钮在哪个页面？”** | ✅ RAG API（`knowledgeType=image` + `knowledgeScene=visual_perception_qa`） + 知识库 | 知识库类型设为 `image`，场景设为 `visual_perception_qa`，RAG API 自动调度多模态嵌入与重排模型，支持图文混合理解。长期记忆当前不支持图片内容解析。 |

## 面向开发者的选型参考

- **优先使用 RAG API，而非直接操作知识库**：知识库是配置概念，所有生产级调用（检索、问答）必须经由 RAG API 的 `/search` 或 `/chat` 接口，并传入 `agent_id`。直接调用 `/retrieve` 仅用于调试，缺少重排与混排能力。
  
- **长期记忆 ≠ 知识库的替代品**：二者数据模型根本不同——知识库面向“静态组织知识”，长期记忆面向“动态用户状态”。一个客服系统可能同时使用：用知识库托管产品文档，用长期记忆记住用户历史投诉与偏好。

- **避免混淆“知识库创建”与“服务发布”**：知识库创建后，必须通过 Agent 管理 API（`/api/v1/indices/rag/app/`）创建并**发布**检索/问答服务，才能获得可用的 `agent_id`。未发布的知识库无法被调用。

- **注意参数命名一致性陷阱**：RAG API 中 `index_id`（snake_case）、`id`（camelCase）、`pipelineId` 混用，务必严格对照各接口文档；长期记忆统一使用 `user_id`、`project_id`，命名更规范。

- **计费敏感场景需明确边界**：  
  - RAG 的文档导入、切片、向量化属于“预处理”，计入资源包；  
  - 长期记忆的 `add-async` 与 `search` 在商业化后独立计费；  
  - 知识库本身无额外费用，但其关联的 API 调用（如 `/search`）按 RAG 标准计费。

- **多模态项目需显式指定模型**：当使用图片/音视频能力时，RAG API 必须传 `multimodalEmbeddingModelName`；长期记忆仅在启用多模态的项目中解析 `image_url`，否则静默忽略。

如需进一步了解某项能力的接入示例、错误排查或性能优化，请查阅对应模块的详细 API 参考文档。

## 被对比主题页

- [rag api](../api/rag-api.md)
- [long term memory new](../api/long-term-memory-new.md)
- [knowledge base](../guides/knowledge-base.md)


