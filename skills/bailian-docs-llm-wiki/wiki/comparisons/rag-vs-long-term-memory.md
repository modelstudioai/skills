# RAG 与[长期记忆](../concepts/long-term-memory.md)（LTM）架构对比

本对比旨在帮助百炼平台开发者清晰理解 **RAG（[检索增强生成](../concepts/rag.md)）API** 与 **[长期记忆](../concepts/long-term-memory.md)（Long Term Memory, LTM）服务** 在设计目标、能力边界、技术实现及工程落地层面的核心差异，避免因概念混淆导致的架构误用。二者虽均涉及“外部知识接入”与“语义检索”，但定位截然不同：  
- **RAG 是面向文档级知识库的静态/半静态知识服务**，核心解决「如何让大模型准确回答结构化业务文档中的问题」；  
- **LTM 是面向用户与会话的动态记忆管理系统**，核心解决「如何让 Agent 持续理解用户、沉淀经验、复用技能」。  
二者可协同使用（如 LTM 检索用户偏好 → 注入 RAG Agent 提示词），但不可相互替代。

## 关键维度对比

| 维度 | RAG API | [长期记忆](../concepts/long-term-memory.md)（LTM） |
|--------|---------|----------------|
| **核心定位** | 文档知识库的全生命周期管理与语义问答服务，聚焦**领域知识的结构化组织与精准问答** | 用户级结构化记忆的写入、抽取、检索与画像构建，聚焦**Agent 的持续学习与个性化上下文建模** |
| **输入格式** | 支持上传 PDF/Word/Excel/PPT/Markdown/TXT 等文件（通过 `docIds` 关联），或直接传入文本块（`chunks`）；支持多模态文档（需指定 `qwen3-vl-embedding` 等解析模型） | 以 `messages` 数组形式传入对话片段（含文本、`image_url`）、事件描述或原始日志；支持 `observation`（事实）、`skill`（可复用行为）、`profile_schema`（画像模板 ID）等语义类型标识 |
| **输出格式** | - 检索接口（`/knowledge/search`）：返回带相关性分数的文档切片列表（`chunks`）<br>- 问答接口（`/knowledge/chat`）：流式返回自然语言答案 + 引用来源（`citations`）<br>- 所有响应统一含 `request_id` 与 `code="Success"` 结构 | - 同步 `/add`：返回 `memory_node_id` 或错误码<br>- 异步 `/add-async`：返回 `event_id`，需轮询 `/events/{id}` 获取抽取结果（含 `observations`/`skills`/`profile` 字段）<br>- `/memory_nodes/search`：返回带 `score` 的记忆节点列表，含 `type`（`observation`/`skill`/`profile`）和结构化 `content`<br>- `/profile_schemas/{id}/user_profile`：返回符合 schema 的 JSON 用户画像对象 |
| **支持模型** | - 嵌入模型：`text-embedding-v4`（文本）、`qwen3-vl-embedding`（多模态）<br>- 重排序模型：`qwen3-rerank`（可配置阈值与 TopN）<br>- Agent 问答模型：`qwen3.7-plus`、`qwen3.6-plus` 等（由 `agent_config.agent_model` 指定）<br>- 解析模型：`DOCMIND`、`DASH_QWEN_VL_PARSER` | - 抽取模型：内置 `efficient`（低延迟）与 `intelligent`（高精度）双模式，自动适配 `extract_scene`<br>- 画像模型：依赖 `plan_version=pro` 或 `lite` 版本，影响 `min_score` 过滤、Rerank 能力及抽取深度<br>- **不暴露底层 LLM 调用接口**，所有模型能力封装在抽取/检索逻辑中 |
| **API 端点基址** | `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/indices/...`（知识库管理）<br>`/api/v1/indices/knowledge/search`（检索）<br>`/api/v2/apps/knowledge/chat`（问答） | `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory/...`<br>`/add`, `/add-async`, `/memory_nodes/search`, `/profile_schemas/...` |
| **计费方式** | 按知识库调用量计费：<br>- 文档解析、切片、索引构建（一次性）<br>- 检索（`/search`）与问答（`/chat`）调用次数<br>- 嵌入/重排/Agent 模型调用按 token 计费（计入对应模型账单） | 按记忆操作计费（2026年8月20日起正式商业化）：<br>- `Add` / `Add-Async` 调用次数（区分 `pro`/`lite` 版本）<br>- `SearchMemory` 调用次数（`pro` 版本支持 `min_score` 过滤与高级 Rerank）<br>- 用户画像模板创建与查询不额外计费 |
| **典型场景** | - 客服知识库问答（产品手册、FAQ）<br>- 内部文档智能搜索（合同、制度、研发文档）<br>- 多文档交叉分析（财报+新闻+公告联合解读）<br>- Agent 的「外部知识插件」（如 `RetrieveProductDocs` 工具） | - 对话式 Agent 的用户偏好记忆（如“用户常订川菜”、“讨厌电话推销”）<br>- 技能沉淀与复用（如“用户上次成功用扫码支付退款”→生成 `refund_by_scan` skill）<br>- 实时用户画像构建（职业、兴趣、消费等级）并用于个性化推荐<br>- 多轮会话状态跟踪（避免重复提问、跨 session 上下文延续） |

## 适用场景建议

### ✅ 推荐使用 RAG API 当：
- 你的数据是**批量导入、相对稳定、以文档为单位**（如 PDF 手册、Word 规范、网页快照）；
- 核心需求是**高精度、可溯源的答案生成**，且需明确标注答案出处（`citations`）；
- 需要支持**复杂文档结构解析**（表格、图表、多级标题）与**多模态内容理解**（图文混合文档）；
- 业务要求**知识库权限隔离、版本管理、人工审核流程**（通过控制台或 API 管理 `indexId` 生命周期）；
- 你已具备或计划构建一个**面向领域的垂直问答 Agent**，需要可靠的知识底座支撑。

### ✅ 推荐使用长期记忆（LTM）当：
- 你的数据是**实时产生、高度动态、以用户/会话为粒度**（如聊天记录、操作日志、表单提交）；
- 核心需求是**让 Agent “记住用户”、“学会做事”、“越用越懂”**，而非回答某个固定文档的问题；
- 需要**结构化提取用户意图（observation）、可复用行为模式（skill）、画像属性（profile）**，并支持后续条件检索（如“查所有标记为 `high_value_user` 的 observation”）；
- 你正在构建**个性化推荐、智能客服、数字员工等强交互型 Agent**，需跨会话维持上下文一致性；
- 你接受异步处理（尤其 `intelligent` 模式），并愿意通过 `event_id` 轮询管理任务状态。

### ⚠️ 不推荐混用或替代的情况：
- ❌ 用 LTM 存储整份《产品白皮书》PDF 并期望它像 RAG 一样做全文精准问答 —— LTM 不提供文档级切片、向量索引与重排能力，召回精度与可解释性远低于 RAG；  
- ❌ 用 RAG 管理 10 万用户的实时对话偏好 —— RAG 缺乏 `user_id` 隔离、画像 schema、技能抽象等机制，无法支撑个性化记忆建模；  
- ❌ 在未启用 `profile_schema` 的情况下，期望 LTM 自动识别用户年龄/职业 —— 必须先定义 schema 并在 `AddMemory` 中显式传入，否则仅作通用文本记忆。

## 技术选型参考（面向开发者）

| 选型考量点 | RAG API | 长期记忆（LTM） | 建议动作 |
|------------|---------|------------------|----------|
| **数据形态** | 文档集合（静态/低频更新） | 用户事件流（高频、实时） | 选 RAG 若数据源是文件系统/OSS；选 LTM 若数据源是消息队列/API 日志 |
| **查询模式** | “这个问题在哪些文档里被提到？”（关键词+语义） | “这个用户过去说过什么？做过什么？喜欢什么？”（用户ID+类型+语义） | RAG 无 `user_id` 概念；LTM 所有接口强制 `user_id`，缺失则报错 |
| **开发复杂度** | 中高：需管理知识库生命周期（创建/同步/删除）、切片策略、Agent 配置、多模型参数协调 | 中：SDK 封装良好（`agentscope-runtime`），但需理解 `extract_mode`/`plan_version`/`profile_schema` 语义 | 新团队建议从 LTM 同步 `/add` 入手；RAG 建议用控制台先行验证知识库效果 |
| **可观测性** | 提供 `/index/monitor`（秒级时间戳）、任务状态查询、详细 `request_id` 日志 | 提供 `/events/{id}` 状态轮询、`GetUserProfile` 延迟说明、`UNRECORDED` 等明确错误码 | 二者均需集成阿里云 SLS 日志；RAG 更依赖 `Retry-After` 处理限流，LTM 更需处理 `PENDING/RUNNING` 状态机 |
| **扩展性** | 支持自定义嵌入/重排模型、多知识库路由、Agent 插件化编排 | 支持多 `project_id` 隔离、`memory_library_id` 分库、`profile_schema` 模板热更新 | 高并发场景：RAG 注意 `/rag/index/monitor` 仅 1 QPS；LTM 注意 `/add` ≤ 120 QPM，超量必用 `/add-async` |

> **协同实践提示**：最佳架构常为 **RAG + LTM 双引擎**。例如：用户提问“我的订单为什么还没发货？”时，Agent 可并行执行：<br>① RAG 检索《物流规则手册》获取通用政策；<br>② LTM 检索该 `user_id` 的 `observation`（如“上周投诉过物流慢”）与 `skill`（如“曾用 `track_shipment` 工具查单号”）；<br>③ 将二者结果融合注入最终 LLM 提示词，生成既专业又个性化的回复。

## 被对比主题页

- [rag api](../api/rag-api.md)
- [long term memory new](../api/long-term-memory-new.md)


