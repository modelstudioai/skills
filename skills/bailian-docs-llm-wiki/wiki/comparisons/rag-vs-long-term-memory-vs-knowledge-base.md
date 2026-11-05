# RAG、[长期记忆](../concepts/long-term-memory.md)与知识库能力对比

在百炼平台构建智能应用时，开发者常需在**外部知识增强（RAG）**、**跨会话状态持久化（[长期记忆](../concepts/long-term-memory.md)）** 和**结构化知识组织与服务（知识库）** 三类能力间进行技术选型。尽管三者均涉及“记忆”与“检索”，但设计目标、数据模型、调用机制和适用边界存在本质差异。本页旨在为开发者提供清晰、可落地的对比分析，帮助其根据业务需求（如是否需要多轮上下文继承、是否依赖私有文档、是否需用户级个性化等）选择最匹配的能力组件，避免能力误用或重复建设。

---

## 关键维度对比

| 维度 | RAG API | [长期记忆](../concepts/long-term-memory.md)（LTM） | 知识库（Knowledge Base） |
|------|---------|------------------|---------------------------|
| **核心定位** | **知识增强服务框架**：提供知识库全生命周期管理 + 检索/问答运行时能力的统一 API 接口层 | **用户级状态持久化中间件**：跨会话保存并自动注入用户偏好、行为快照、画像属性等结构化/半结构化上下文 | **知识组织与服务单元**：承载文档、切片、向量索引及检索策略的实体容器，是 RAG 能力的底层数据载体与配置中心 |
| **输入格式** | - 管理类：JSON（含 `knowledgeType`/`knowledgeScene`/`indexId` 等字段）<br>- 检索/问答：`agent_id` + 用户 query（支持多轮 `tool_calls` 历史） | - 片段（Fragment）：`content`（string）+ `metadata`（object）<br>- 画像（Profile）：符合预定义 JSON Schema 的结构化对象<br>- 所有写入需指定 `memory_id` | - 文档：PDF/DOCX/MD/CSV/MP4 等原始文件（通过 OSS 或本地上传）<br>- 配置：创建时声明 `chunking_strategy`、`embedding_model`、`max_chunk_length` 等不可变参数 |
| **输出格式** | - 检索接口：JSON 数组（含 `chunks`、`score`、`source`）<br>- 问答接口：SSE 流式响应（含 `answer`、`retrieved_chunks`、`tool_calls`） | - 自动注入：无显式返回；记忆内容被拼接至 system [prompt](../guides/prompt.md) 后由 LLM 消费<br>- 主动查询：`GET /v1/applications/{app_id}/memories/fragments` 返回片段列表（含 `content`、`metadata`、`created_at`） | - 控制台 Playground：可视化展示检索切片 + 模型回答<br>- API：同 RAG API 输出（因 RAG API 的 `/search` 和 `/chat` 实际调用知识库服务） |
| **支持模型** | **不直接调用模型**，但依赖：<br>- 嵌入模型（如 `text-embedding-v4`）用于向量化<br>- 重排模型（如 `qwen3-rerank`）用于精排<br>- 生成模型（如 `qwen3.6-plus`）用于问答生成 | **仅限特定大模型主动消费**：<br>- `qwen-max`、`qwen-plus`、`qwen-turbo`（需显式启用 `enable_long_term_memory: true`）<br>- 其他模型调用时静默忽略记忆字段 | **作为模型能力的配置载体**：<br>- 嵌入模型：创建知识库时绑定（默认 `text-embedding-v4`）<br>- 重排模型：服务级配置（如 `qwen3-vl-rerank`）<br>- 生成模型：问答服务中独立选择（如 `qwen3.6-plus`） |
| **API 端点** | - 管理：`/api/v1/indices/rag/index/create_v2`、`/api/v1/connector/dash/addFile` 等<br>- 运行时：`/api/v1/indices/knowledge/search`（检索）、`/api/v2/apps/knowledge/chat`（流式问答） | - 写入：`POST /v1/applications/{app_id}/memories/fragments`、`PUT /v1/applications/{app_id}/memories/profiles/{memory_id}`<br>- 查询：`GET /v1/applications/{app_id}/memories/fragments?memory_id=xxx` | **无独立 API**；所有操作均通过 RAG API 或控制台完成。知识库 ID（`index_id`）是 RAG API 中的关键路径参数。 |
| **计费方式** | 按 **调用量计费**：<br>- 知识库管理（创建/更新/删除）：按次计费<br>- 数据导入（OSS/文件上传）：按文件数/大小计费<br>- 检索与问答：按请求次数 + 返回 token 数计费（含 embedding/rerank/generation） | 按 **存储量 + 调用量计费**：<br>- 记忆存储：按 GB/月计费（含片段内容与画像数据）<br>- 写入/读取：按 API 调用次数计费<br>- 自动注入：不额外计费（计入主模型推理费用） | **与 RAG API 计费完全一致**。知识库是 RAG 能力的资源实例，其使用成本已包含在 RAG API 的各项计费项中。 |
| **典型场景** | - 客服机器人基于产品手册实时问答<br>- 法律合同条款比对与解释<br>- 多源音视频资料语义搜索（如会议录像关键片段定位） | - 电商助手记住用户尺码偏好与历史退换货原因<br>- 教育应用持续追踪学生薄弱知识点与学习风格<br>- 企业内部助手识别不同部门员工的权限与常用流程 | - 构建企业私有维基（文档搜索）<br>- 将数据库表转为自然语言查询接口（NL2SQL）<br>- 图文混合的产品说明书问答（图片+文字联合理解） |

---

## 各方案适用场景建议

| 场景特征 | 推荐方案 | 理由说明 |
|----------|----------|----------|
| **需要基于大量私有文档（PDF/Excel/视频）提供精准、可溯源的问答服务** | ✅ **知识库（配合 RAG API）** | 知识库专为多模态、大规模、结构化/非结构化文档设计，支持切片策略、嵌入模型绑定、重排精调，且可通过 RAG API 统一调度检索与生成，满足企业级知识服务对可控性、可审计性的要求。 |
| **需跨多次对话保持用户个性化状态（如偏好、历史行为、身份属性），且该状态需被模型自动感知与利用** | ✅ **长期记忆（LTM）** | LTM 提供开箱即用的 `memory_id` 隔离、TTL 自动过期、结构化画像 Schema 校验，并与 `qwen-max/plus/turbo` 深度集成，实现“零代码注入”。若自行用数据库模拟，将丧失语义召回、自动注入、配额管控等平台级能力。 |
| **需灵活管理多个知识源（如法务库、HR政策库、产品文档库），并支持联合检索、权限隔离与效果监控** | ✅ **RAG API（作为编排层） + 多知识库** | RAG API 的 `/knowledge/search` 接口原生支持 `agent_id` 绑定多个知识库，可配置统一检索策略与权限；其管理 API 支持批量创建、标签过滤、监控告警，是构建复杂知识中台的事实标准接口。 |
| **轻量级、单点文档快速验证（如测试某份 PDF 是否能被正确解析）** | ✅ **知识库（控制台 Playground）** | 无需写一行代码，上传文档 → 创建知识库 → 在 Playground 输入问题，5 分钟内完成端到端验证，适合 PoC 和效果调优。 |
| **需将用户记忆与知识库检索结果共同作为上下文输入给模型（如：“结合我上次反馈的退货原因（LTM）和最新版售后政策（知识库），给出处理建议”）** | ⚠️ **组合使用：LTM + RAG API** | 二者能力正交互补：LTM 注入用户侧上下文，RAG API 提供领域知识上下文。需在请求 `messages` 中同时启用 `"long_term_memory": {"enable": true}` 并传入有效 `agent_id`，平台将自动融合两类信息。 |

---

## 技术选型参考（面向开发者）

- **不要混淆“知识库”与“RAG API”**：  
  知识库是**数据实体与配置集合**（类似数据库表），RAG API 是**操作该实体的标准化接口集**（类似 JDBC）。开发中应优先通过 RAG API 管理知识库，而非直接操作知识库元数据。

- **长期记忆 ≠ 简单的 KV 缓存**：  
  若仅需存储 `user_id → language` 这类简单键值，可用 Redis；但若需语义召回（如“找出所有抱怨物流慢的用户片段”）、自动注入、Schema 校验、TTL 精细控制，则必须使用 LTM。其 `embedding_model` 参数决定了语义检索质量，务必与主模型 embedding 对齐。

- **警惕“知识库万能论”**：  
  知识库擅长**静态、权威、可归档**的知识（如制度、手册、产品参数）。对于**动态、个性化、高时效性**的用户状态（如“张三刚提交的退款申请ID”），应存入 LTM 或业务数据库，而非强行塞入知识库——这会导致索引膨胀、检索噪声增大、权限管理混乱。

- **生产环境必做三件事**：  
  1. **参数校验前置**：RAG API 中 `index_id`/`docIds`/`dataId` 等参数命名不一致，务必严格对照各接口文档；LTM 的 `ttl_seconds` 必须为整数，`sizeBytes` 必须为字符串。  
  2. **错误处理标准化**：所有能力均返回 `429` 限流，必须实现指数退避重试；知识库删除、LTM 写入失败均为不可逆错误，需增加业务层确认逻辑。  
  3. **监控与告警接入**：通过 RAG API 的 `/get-index-monitor` 获取知识库切片数、召回率；通过 LTM 的配额 API 监控存储水位，避免突发流量导致服务降级。

- **演进路线建议**：  
  `PoC 验证（控制台 Playground）` → `MVP 上线（RAG API + 单知识库）` → `规模化扩展（LTM + 多知识库 + Agent 编排）` → `智能融合（LTM + RAG + 工具调用 + 自反思）`。避免在早期阶段过度设计多知识库或复杂记忆 Schema。

## 被对比主题页

- [rag api](../api/rag-api.md)
- [long term memory new](../api/long-term-memory-new.md)
- [knowledge base](../guides/knowledge-base.md)


