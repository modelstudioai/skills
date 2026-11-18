# RAG 与[长期记忆](../concepts/long-term-memory.md)能力对比

在构建智能体（Agent）和企业级知识应用过程中，开发者常需在**外部知识增强**与**内部经验沉淀**两类能力间进行技术选型。RAG（Retrieval-Augmented Generation）API 侧重于将结构化/非结构化**静态知识库**作为可信外部源，支撑精准检索与生成；而[长期记忆](../concepts/long-term-memory.md)（Long Term Memory, LTM）服务则聚焦于对**动态交互过程中的用户事实、技能与画像**进行结构化建模与生命周期管理，实现个性化上下文延续。本页旨在从工程落地视角，系统对比二者在接口设计、能力边界、集成成本与适用阶段上的核心差异，为开发者提供可操作的技术选型参考。

## 关键维度对比

| 维度 | RAG API | [长期记忆](../concepts/long-term-memory.md)（LTM） |
|------|---------|----------------|
| **核心定位** | 外部知识增强：将预置文档、表格、音视频等作为权威知识源，服务于问答、搜索、摘要等任务 | 内部经验沉淀：将对话中产生的事实、技能、用户属性等作为可复用记忆节点，服务于 Agent 的上下文感知与个性化推理 |
| **输入格式** | • 知识库创建：`structureType`（flat/hierarchical）、`knowledgeType`（document/table/image/multimedia）<br>• 数据导入：支持本地文件、OSS URL、文本内容（Base64 或 raw）<br>• 检索/问答：`query`（字符串或 ContentPart 数组，含 text/image_url）+ `agent_id` + 可选 `kb_search_configs` | • 写入：`messages`（OpenAI 格式数组，支持 text/image_url）、`user_id`、`project_id`（或 `profile_schema`）<br>• 检索：`messages`（触发语义召回）+ `user_id` + `memory_types` + `plan_version`（`lite`/`pro`） |
| **输出格式** | • 检索（`/knowledge/search`）：返回 `chunks` 列表（含 `content`, `score`, `metadata`），不包含生成结果<br>• 问答（`/knowledge/chat`）：流式返回 `choices[].delta.content`，含模型基于检索结果的合成回答 | • 写入（同步/异步）：返回 `memory_nodes`（含 `id`, `type`, `content`, `score`, `created_at`）或 `event_id`<br>• 检索（`/memory_nodes/search`）：返回排序后的 `memory_nodes` 列表（含 `score`, `type`, `custom_content`, `source`），**不生成自然语言回答** |
| **支持模型/能力** | • 嵌入模型：可指定 `embeddingModelName`（如 `text-embedding-v4`）<br>• 重排模型：可指定 `rerankModelName`（如 `qwen3-rerank`）<br>• Agent 封装：支持 `qwen3.7-plus` 等大模型 + `turbo`/`agentic` 策略 + 混排配置 | • 抽取模型：底层由平台统一调度，开发者不可见具体模型名；`plan_version=pro` 启用 Rerank 能力<br>• 记忆类型：原生支持 `observation`（事实）、`skill`（流程）、`user_profile`（结构化画像）三类语义节点<br>• 多模态：仅在启用多模态项目的 `messages` 中解析图片，其他场景忽略 |
| **API 端点（Base URL）** | `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`<br>路径示例：<br>• 创建知识库：`/api/v1/indices/rag/index/create_v2`<br>• 知识问答：`/api/v2/apps/knowledge/chat` | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory`<br>路径示例：<br>• 写入记忆：`/add` 或 `/add-async`<br>• 检索记忆：`/memory_nodes/search`<br>• 查询画像：`/profile_schemas/{id}/user_profile` |
| **认证方式** | `Authorization: Bearer <API-Key>`<br>API Key 在百炼控制台「API Key 管理」获取，需 RAM 子账号具备 `AliyunBailianDataFullAccess` 权限 | `Authorization: Bearer $DASHSCOPE_API_KEY`<br>使用同一套 DashScope API Key，但需 RAM 子账号具备 `AliyunBailianFullAccess`（或最小权限策略） |
| **计费方式** | • 按调用量计费（知识库管理、数据导入、检索、问答均独立计费）<br>• 知识库存储按容量（GB/月）计费<br>• 嵌入/重排模型调用按 Token 计费（详见[计费说明](https://help.aliyun.com/product/420492.html)） | • **商业化起始时间：2026 年 8 月 20 日 10:00（北京时间）**<br>• `Add` 与 `Search` 接口区分 `Pro`/`Lite` 版本，影响抽取质量与 Rerank 能力<br>• 当前公测期免费，正式计费后按调用次数 + `plan_version` 分级计费 |
| **典型场景** | • 客服知识库问答（产品文档、FAQ）<br>• 企业内部政策/制度检索<br>• 表格数据自然语言查询（销售报表分析）<br>• 图片/视频内容理解（如“找出所有含红色Logo的PPT截图”） | • Agent 记住用户偏好（“用户不吃香菜”，存为 `user_profile`）<br>• 自动归纳用户需求模式（“用户每次出差前都会问航班+酒店”，存为 `skill`）<br>• 追踪临时状态（“用户说‘明天要开会’”，存为 `observation` 并设置时效提醒）<br>• 多轮对话中跨会话复用上下文（避免重复提问） |

## 各方案的适用场景建议

### ✅ 选择 RAG API 当：
- 你拥有**大量静态、权威、需版本管控的知识资产**（如 PDF 手册、数据库表、培训视频），且要求检索结果可追溯、可审计；
- 应用目标是**提升问答准确性与信息覆盖广度**，而非建模用户行为；
- 需要支持**多模态混合检索**（图文并茂的文档、带字幕的视频）；
- 已有知识库管理流程（如定期更新 SOP 文档），需通过 API 实现自动化同步；
- 对响应延迟敏感（如实时客服），且能接受 `knowledge/chat` 必须传完整历史消息的约束。

### ✅ 选择长期记忆（LTM）当：
- 你的应用是**以 Agent 为核心**，需在多次对话中持续理解用户意图、积累个性化认知；
- 需要**自动从对话中提炼结构化记忆**（如识别出“会议纪要整理”是一个可复用技能），而非人工维护知识库；
- 关注**用户画像的动态演进与合规管理**（如 GDPR 下的用户数据生命周期控制）；
- 希望降低 Agent 开发复杂度——LTM 提供开箱即用的 `observation`/`skill`/`profile` 三层抽象，无需自行设计向量库 Schema；
- 接受异步写入（`add-async`）作为默认实践，并能处理 `event_id` 轮询逻辑。

### ⚠️ 不建议混用或替代的情形：
- **不要用 LTM 替代 RAG 做知识库问答**：LTM 不提供 `query → answer` 的端到端生成能力，其 `search` 返回的是记忆片段，仍需上层模型做推理整合；
- **不要用 RAG 替代 LTM 做用户画像管理**：RAG 的 `document` 知识库无法天然支持 `user_id` 隔离、`profile_schema` 校验、软删除回溯等用户级数据治理能力；
- **二者可协同，但需分层设计**：推荐架构为 —— LTM 负责管理 `user_id` 维度的个性化记忆，RAG 负责管理 `workspace_id` 维度的通用知识库；Agent 在生成前先调用 LTM 获取用户上下文，再调用 RAG 获取领域知识，最后融合决策。

## 面向开发者的技术选型参考

| 选型考量点 | RAG API | 长期记忆（LTM） | 建议动作 |
|------------|---------|------------------|----------|
| **首次集成复杂度** | ⚠️ 较高：需依次完成知识库创建 → 文件上传 → 切片管理 → Agent 发布 → 运行时调用，参数命名不一致（如 `index_id`/`pipelineId`/`id`） | ✅ 较低：只需 `user_id` + `messages` 即可触发抽取，SDK 封装完善（`agentscope-runtime`） | 新项目优先评估 LTM 快速验证可行性；已有知识资产团队可直接启动 RAG 落地 |
| **数据主权与治理** | ✅ 强：知识库完全由客户控制，支持 OSS 直传、私有化部署选项、细粒度 RBAC | ⚠️ 中：记忆数据归属百炼平台，虽支持软删除与 `user_id` 隔离，但暂无自定义 TTL 或加密密钥 BYOK 支持 | 涉及金融/政务等强监管场景，RAG 更易满足等保要求；LTM 适用于互联网 SaaS 类应用 |
| **多模态支持成熟度** | ✅ 生产就绪：`image`/`multimedia` 类型知识库已支持视觉感知问答（`visual_perception_qa`） | ⚠️ 有限：仅在启用多模态项目的 `messages` 中解析图片，且不保证所有场景生效 | 视觉理解是刚需时，RAG 是当前唯一稳定选项 |
| **长期演进潜力** | 🔁 依赖知识库运营：效果提升取决于文档质量、切片策略、嵌入模型升级 | 🚀 平台驱动增强：`plan_version=pro` 将持续接入更优抽取模型与 Rerank 策略，开发者零改造即可受益 | 若团队缺乏 NLP 运维能力，LTM 的“托管式智能”更具可持续性 |
| **调试与可观测性** | ✅ 丰富：各环节（切片、检索、重排）均有独立日志与指标，支持 `debug: true` 参数查看中间结果 | ⚠️ 有限：异步事件需轮询，同步接口超时风险存在，暂无细粒度中间结果透出 | 对调试效率要求极高时，RAG 提供更透明的链路追踪能力 |

> **总结一句话选型口诀**：  
> **“管知识，选 RAG；记用户，用 LTM；要准确，靠 RAG；要聪明，靠 LTM。”**  
> 二者非竞争关系，而是百炼平台面向不同抽象层级（知识层 vs 认知层）提供的互补能力。建议在 Agent 架构设计初期即明确分层职责，避免能力错配导致后期重构成本激增。

## 被对比主题页

- [rag api](../api/rag-api.md)
- [long term memory new](../api/long-term-memory-new.md)


