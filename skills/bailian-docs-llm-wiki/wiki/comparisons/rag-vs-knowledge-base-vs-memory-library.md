# RAG API、知识库与记忆库对比

本文档面向百炼平台开发者，旨在清晰区分 **RAG API**、**知识库（Knowledge Base）** 和 **记忆库（Memory Library）** 三大核心能力模块。三者虽均服务于“增强大模型能力”，但设计目标、数据生命周期、交互范式与适用场景存在本质差异。准确理解其边界与协同关系，是构建高性能、可维护、可扩展 AI 应用的关键前提。

> ⚠️ 注意：  
> - **RAG API 是底层能力封装**，面向需要精细控制 RAG 全链路（入库→切片→索引→检索→生成）的工程化场景；  
> - **知识库是面向应用的 RAG 服务抽象**，提供开箱即用、模型可选、多源接入的端到端问答能力；  
> - **记忆库是会话级长期状态管理服务**，不依赖预置文档，而是从实时对话中自动提取、结构化并复用用户专属信息。  
> 三者可组合使用（如：知识库提供领域知识 + 记忆库注入用户偏好），但不可互相替代。

---

## 关键维度对比表

| 维度 | RAG API | 知识库（Knowledge Base） | 记忆库（Memory Library） |
|------|---------|---------------------------|---------------------------|
| **核心定位** | RAG 全链路能力的标准化 API 接口，强调**可控性与集成深度** | 企业级 RAG 服务产品化封装，强调**易用性、开箱即用与多源支持** | 大模型跨会话长期记忆服务，强调**动态性、个性化与语义连贯性** |
| **输入格式** | `POST /v1/knowledge/query`：需显式传入 `knowledge_id` + `query`；文档上传需调用独立 `/documents` 接口；支持原始二进制文件流或 OSS URL | 支持多源输入：本地文件、OSS 路径、MySQL 表、CSV/Excel 表格等；上传后自动解析；问答请求仅需 `query` + `knowledge_id`（或 `model_id`） | `POST /add`：传入 `user_id` + `messages`（对话历史数组）；`POST /search`：传入 `user_id` + 当前 `messages`（用于语义匹配） |
| **输出格式** | 同步返回 JSON（含 `retrieved_chunks` 和 `answer`）；支持 `stream=true` 的 SSE 流式响应（仅 `/query`） | `/retrieve` 返回纯上下文切片列表；`/qa` 返回含 `answer` 和 `references` 的完整 JSON；均支持 `stream=true` 流式生成 | `/search` 返回带 `score` 的记忆节点列表（含 `fact` 或 `profile` 字段）；`/memory_nodes` 返回结构化记忆快照；无[流式输出](../concepts/streaming-output.md) |
| **支持模型** | 仅支持百炼托管的特定 RAG 优化模型（如 `qwen2-rag` 系列），模型绑定在知识库创建阶段，**不可运行时切换** | embedding 模型固定（`text-embedding-v1`），**问答模型完全可选**：`qwen-max`、`qwen-plus` 等任意已授权 LLM，通过 `model_id` 参数指定 | **不调用 LLM 生成答案**；所有记忆抽取与检索均为向量/规则驱动；LLM 仅作为上游调用方消费记忆结果 |
| **API 端点** | `POST /v1/knowledge/query`（主接口）<br>`POST /v1/knowledge-base`（建库）<br>`POST /v1/documents`（上传）<br>`POST /v1/sync-jobs`（同步） | `POST /v1/knowledge/retrieve`（检索）<br>`POST /v1/knowledge/qa`（问答）<br>`POST /v1/knowledge-base`（建库）<br>`POST /v1/data-sources`（数据源） | `POST /v1/memory/add`（写入）<br>`POST /v1/memory/search`（检索）<br>`GET /v1/memory/memory_nodes`（查询）<br>（基础路径：`https://dashscope.aliyuncs.com/api/v2/apps/memory/`） |
| **认证方式** | Bearer [Token](../concepts/token.md)（需通过 `/auth/token` 获取，**不支持 API Key**） | Bearer [Token](../concepts/token.md)（同 RAG API，统一鉴权体系） | `DASHSCOPE_API_KEY`（独立于 RAG [Token](../concepts/token.md)，需单独申请与管理） |
| **计费方式** | 按 **调用量（QPS）+ 向量索引存储量（GB/月）+ rerank 调用次数** 计费；免费额度有限，超限立即计费 | 按 **知识库实例数 + 文档解析页数 + 问答 token 数 + rerank 调用次数** 计费；含基础免费额度，控制台可查用量 | **2026 年 8 月 20 日起正式计费**；按 **记忆节点数（个/月）+ search 调用次数 + profile 提取次数** 计费；当前为免费体验期 |
| **典型场景** | - 需自定义切片策略（如按法律条款编号切分）<br>- 需异步监控同步任务状态与错误日志<br>- 需与 Agent 编排深度耦合（如多跳检索触发工具调用）<br>- 需严格遵循企业级审计与配额管控流程 | - 快速上线客服知识问答机器人<br>- 构建内部文档智能搜索门户<br>- 将 Excel 产品手册、PDF 技术白皮书接入 LLM 应用<br>- 通过 Playground 实时调试效果 | - 智能体记住用户偏好（“我讨厌咖啡因”）<br>- 跨天会议助手持续追踪待办事项（“周三下午3点与张总对齐方案”）<br>- 个性化推荐系统动态更新用户画像（职业、兴趣标签）<br>- 工作流中自动填充用户历史填写项 |
| **数据生命周期** | 文档上传后需显式触发 `sync-job`；索引更新非实时（1–3 分钟延迟）；删除知识库即清空全部数据 | 同知识库：需手动触发同步；索引延迟同上；支持单文档更新与增量同步 | **全自动生命周期管理**：事实记忆可设 TTL（7/30/180 天），过期自动清理；用户画像永久保留（除非显式删除）；写入即生效（事实记忆），画像提取异步完成（秒级） |

---

## 适用场景建议（面向开发者的技术选型指南）

### ✅ 选择 **RAG API** 当：
- 你正在构建一个**高度定制化的 RAG 中间件或平台级能力**，需要精确控制每个环节（例如：自研切片算法、混合检索策略编排、与私有向量库对接）；
- 你的业务要求**严格的审计追踪与资源隔离**（如金融、政务场景），需通过 API 显式管理知识库、文档、任务等全量资源 ID；
- 你需要将 RAG 能力嵌入到**复杂 Agent 工作流中**，且依赖 `agent_mode=true` 下的多跳检索与工具调用联动；
- 你已有成熟的文档处理流水线，仅需百炼提供向量化与检索能力，**不希望平台介入内容解析逻辑**。

> 🛑 不推荐：快速原型验证、中小团队轻量级知识问答、无需深度定制的业务场景（开发成本高、学习曲线陡峭）。

---

### ✅ 选择 **知识库（Knowledge Base）** 当：
- 你希望**以最低代码成本上线一个生产级 RAG 应用**（如客服机器人、内部知识助手）；
- 你需要支持**多种数据源混合接入**（如同时导入 Confluence 页面、MySQL 用户表、销售合同 PDF）；
- 你要求**问答模型灵活可换**（例如：测试阶段用 `qwen-plus`，上线后切至 `qwen-max`）；
- 你依赖**控制台 Playground 进行实时效果调优与 QA 验证**，而非纯命令行调试。

> 🛑 不推荐：需要毫秒级索引更新（如实时新闻问答）、需对每条 chunk 手动打标/审核、或数据安全策略要求完全离线部署（知识库为云托管服务）。

---

### ✅ 选择 **记忆库（Memory Library）** 当：
- 你的应用本质是**多轮、长周期、强个性化**的智能体（Agent），例如：个人健康教练、项目管理助手、学习规划师；
- 你需要**自动从自然对话中提取结构化事实与用户属性**，而非依赖人工整理知识文档；
- 你关注**跨会话状态一致性**（如用户昨天说“预算5万”，今天提问“推荐3款”时自动带入该约束）；
- 你正在构建**工作流自动化系统**，需让不同步骤共享同一用户的上下文记忆（如：销售线索跟进 → 合同生成 → 发票开具）。

> 🛑 不推荐：一次性问答场景（如单次技术文档查询）、静态知识服务（如百科问答）、或需要引用外部权威文档原文的合规性场景（记忆库不提供溯源 chunk）。

---

## 协同使用最佳实践

三者并非互斥，而是构成百炼平台 **“静态知识 + 动态记忆 + 智能推理”** 的黄金三角：

1. **知识库提供「世界知识」**：如公司制度、产品手册、行业法规 —— 内容稳定、来源明确、需精准引用；
2. **记忆库注入「用户知识」**：如用户身份、偏好、历史承诺、待办事项 —— 内容动态、私有性强、需语义关联；
3. **RAG API 或知识库接口作为「执行引擎」**：在生成回答前，先调用记忆库获取 `user_profile` 和 `recent_facts`，再拼接至 Prompt；或将其作为 `retrieved_chunks` 的补充上下文。

> 💡 示例架构：  
> `用户提问 → 记忆库 `/search` 获取个性化约束 → 知识库 `/qa` 检索领域知识 → LLM 综合两者生成答案 → 新对话片段写入记忆库 `/add` → 形成闭环`

如需进一步了解集成示例，请参考：[RAG 与记忆库联合实践](../../raw/application-user-guide/knowledge-base/integration-with-memory.md)、[Agent Harness 记忆增强配置指南](../../raw/application-user-guide/memory-library-overview/integration-with-agent-harness.md)。

## 被对比主题页

- [rag api](../api/rag-api.md)
- [knowledge base](../guides/knowledge-base.md)
- [memory library overview](../guides/memory-library-overview.md)


