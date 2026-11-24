# RAG 与长时记忆（Long-Term Memory）架构对比

本对比旨在帮助百炼平台开发者清晰理解 **RAG（Knowledge API）** 与 **长时记忆（Long-Term Memory）** 两类核心知识管理能力的定位差异、技术边界与协作关系。二者虽均面向“外部知识接入”，但设计目标、数据建模范式、生命周期管理和适用阶段存在本质区别：  
- **RAG 是面向静态、结构化/非结构化知识库的检索增强问答系统**，强调**领域知识的规模化沉淀、语义召回与即时推理协同**；  
- **长时记忆是面向智能体（Agent）运行时的动态、人格化记忆中枢**，强调**跨会话的事实沉淀、技能固化与用户画像演进**。  

正确区分二者，可避免架构误用（如用 RAG 存储用户偏好）、资源错配（如为短期对话启用 Wiki 图谱），并支撑“知识库 + 记忆体 + 推理引擎”的分层智能体架构落地。

---

## 关键维度对比

| 维度 | RAG（Knowledge API） | 长时记忆（Long-Term Memory） |
|------|------------------------|------------------------------|
| **核心定位** | 静态知识库服务：将文档/表格/音视频等离线知识转化为可检索的向量索引，服务于问答、摘要等任务 | 动态记忆中枢：在智能体运行过程中持续积累、组织、演化用户事实、技能和画像，支撑上下文延续与个性化决策 |
| **输入格式** | 支持多源异构数据：<br>• 文档（PDF/DOCX/TXT/HTML 等）<br>• 表格（CSV/XLSX，需结构化 schema）<br>• 图片/音视频（需 `multimedia` 场景）<br>• 原始文本片段（`unstructured` 类型） | 结构化记忆事件：<br>• `messages`（含文本、`image_url` 等上下文消息）<br>• `user_id` + `project_id`（二级隔离标识）<br>• 可选 `profile_schema`（用户画像模板 ID）<br>• `custom_content`（自定义 JSON 结构化字段） |
| **输出格式** | • 检索结果：`chunks` 列表（含 `content`, `score`, `metadata`）<br>• 问答响应：SSE 流式 JSON（含 `answer`, `references`, `trace_id`）<br>• Wiki 图谱：JSON-LD 格式三元组（仅旗舰版） | • 写入响应：`event_id`（异步）或抽取后的 `memory_nodes`（同步）<br>• 检索结果：`memory_nodes` 列表（含 `id`, `type`, `content`, `score`, `created_at`, `metadata`）<br>• 用户画像：`UserProfile` 对象（按 `profile_schema` 结构化返回） |
| **支持模型/能力** | • 嵌入模型：`text-embedding-v3/v4`、`qwen3.7-text-embedding`、`qwen3-vl-embedding`（多模态）<br>• 重排模型：`qwen3-rerank`（可显式指定）<br>• 高级能力：Wiki 知识图谱、本体抽取（需 `pipelineCommercialType=enterprise`） | • 抽取模式：`efficient`（低延迟）与 `intelligent`（多步推理，**必须异步调用**）<br>• 计费版本：`lite`（基础检索）与 `pro`（支持 `min_score` 过滤、重排）<br>• 多模态：`image_url` 参与抽取（需项目配置启用） |
| **API 端点** | 统一业务空间 Endpoint：<br>`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/indices/...`<br>（如 `/rag/index/create_v2`, `/knowledge/search`, `/apps/knowledge/chat`） | 统一业务空间 Endpoint：<br>`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory/...`<br>（如 `/memory/add`, `/memory/add_async`, `/memory/search`, `/memory/profile/get`） |
| **计费方式** | • 按知识库实例计费（基础版/旗舰版）<br>• 按调用量计费：文档解析、嵌入生成、检索请求、问答调用<br>• Wiki/图谱功能需旗舰版授权 | • **商业化起始时间：2026 年 8 月 20 日 10:00（北京时间）**<br>• 分版本计费：`lite`（基础）与 `pro`（高级过滤/重排）<br>• 按调用次数计费：`AddMemory` / `SearchMemory` / `GetUserProfile` 等接口调用 |
| **典型场景** | • 客服知识库问答（产品文档、FAQ）<br>• 企业内部资料检索（制度、合同、财报）<br>• 多媒体内容搜索（培训视频关键帧定位）<br>• 基于 Wiki 的知识图谱构建与推理 | • 智能体长期用户建模（记录偏好、禁忌、历史承诺）<br>• SOP/工具链技能固化（如“订会议室流程”自动提炼为 skill 节点）<br>• 跨会话上下文恢复（“上次说要查的竞品报告，我已存为 observation”）<br>• 个性化推荐依据（结合 user_profile + observation 实时生成建议） |
| **数据生命周期** | • 显式管理：创建 → 导入 → 发布 → 检索 → 删除（**永久删除，无回收站**）<br>• 数据静态性高，更新需重新切片/嵌入 | • 自动演进：写入 → 抽取 → 检索 → （可选）软删除（`status=delete`，仍可查）<br>• 数据动态性强，支持增量更新与多轮修正（如用户画像随交互持续丰富） |
| **权限与隔离** | • 以 `workspace_id` + `index_id` 为粒度隔离<br>• 同一知识库内所有用户共享检索结果 | • 以 `user_id` + `project_id` 为双维度强隔离<br>• 不同 `user_id` 的记忆物理隔离，杜绝越权访问 |

---

## 适用场景建议

### ✅ 选择 RAG（Knowledge API）当：
- 你拥有**批量、稳定、领域明确的静态知识资产**（如 1000+ 份 PDF 手册、50 张业务数据库表），需快速构建可检索的知识底座；
- 业务诉求是**“精准回答已知问题”**，例如：“《员工差旅报销制度》第 3.2 条如何规定？”；
- 需要**多模态混合检索能力**（图文音视频联合查询）或**知识图谱增强推理**（如通过 Wiki 关联“供应商资质”与“合同履约风险”）；
- 系统对**首次响应延迟敏感**（RAG 检索+LLM 生成端到端平均 < 2s），且无需记忆用户个性化状态。

### ✅ 选择长时记忆（Long-Term Memory）当：
- 你正在构建**具备人格化、连续性、成长性的智能体**（Agent），需在多次对话中记住用户习惯、承诺事项、操作反馈；
- 业务诉求是**“理解用户并主动服务”**，例如：“您上周提到想了解 A 产品，我已为您整理了对比报告”；
- 需要**结构化沉淀可复用的技能**（如“生成周报”流程自动抽象为 `skill` 节点，供其他 Agent 复用）；
- 用户画像需**动态演进**（如从“首次咨询”→“试用中”→“付费客户”，各阶段画像 schema 不同且需实时生效）。

### ⚠️ 协同使用建议（推荐架构）：
- **分层解耦**：RAG 作为“公司级知识大脑”（What we know），长时记忆作为“用户级记忆小脑”（What *you* need）；
- **典型工作流**：  
  `用户提问 → Agent 先查 Long-Term Memory（获取用户偏好/历史上下文）→ 再调 RAG（检索通用知识）→ 融合两者生成个性化回答`；  
- **数据流向**：RAG 中高频被引用的 chunk 可触发 `observation` 写入长时记忆（如用户反复询问某条款，自动标记为“重点关注”）；  
- **避坑提示**：勿将用户隐私数据（手机号、身份证号）直接存入 RAG 知识库（缺乏用户级隔离）；应统一走长时记忆 `user_profile` + `observation` 管道。

---

## 技术选型参考（面向开发者）

| 选型考量点 | 推荐方案 | 理由说明 |
|------------|----------|----------|
| **是否需要用户级数据隔离？** | 必须选长时记忆 | RAG 知识库全局共享，无 `user_id` 隔离机制；长时记忆强制 `user_id` 参数，保障多租户安全 |
| **知识来源是批量导入还是运行时生成？** | 批量文档 → RAG；对话中产生 → 长时记忆 | RAG 设计为离线预处理（切片/嵌入），不适合高频小数据写入；长时记忆专为运行时事件流优化（支持异步并发写入） |
| **是否需支持多轮对话状态追踪？** | 必须选长时记忆 | RAG 无会话上下文概念；长时记忆天然支持 `user_id` + 时间戳 + `memory_type` 多维检索，可精准还原对话脉络 |
| **是否需对检索结果做细粒度过滤（如置信度阈值）？** | RAG（默认支持 score） 或 长时记忆 `pro` 版本（`min_score`） | RAG 检索返回 `score` 字段，可直接用于前端高亮或后端过滤；长时记忆需 `plan_version=pro` 才支持 `min_score` |
| **是否需 SDK 开箱即用？** | 优先长时记忆（`agentscope-runtime`） | RAG 需手动拼接 endpoint、处理 snake/camelCase 参数不一致；长时记忆 SDK 已封装 `AddMemoryAsync`、`SearchMemory` 等方法，自动处理鉴权与序列化 |
| **是否需未来扩展知识图谱？** | RAG（旗舰版 Wiki） | 长时记忆聚焦节点关系（如 `skill` 调用 `observation`），不提供图谱可视化、SPARQL 查询等企业级图能力 |

> **最后建议**：新项目启动时，**优先评估长时记忆需求**——90% 的智能体应用瓶颈不在“知道什么”，而在“记住谁、记得什么、如何记住”。RAG 是强大补充，而非替代方案。二者不是二选一，而是智能体架构的左右手。

## 被对比主题页

- [rag api](../api/rag-api.md)
- [long term memory new](../api/long-term-memory-new.md)


