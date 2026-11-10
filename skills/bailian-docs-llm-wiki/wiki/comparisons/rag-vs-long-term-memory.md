# RAG 与[长期记忆](../concepts/long-term-memory.md)（LTM）能力对比

本对比旨在帮助百炼平台开发者清晰区分 **RAG（[检索增强生成](../concepts/rag.md)）** 与 **[长期记忆](../concepts/long-term-memory.md)（Long Term Memory, LTM）** 两大核心知识管理能力的技术定位、适用边界与工程实践差异。二者虽均面向“让大模型具备外部知识能力”这一目标，但在设计哲学、数据建模、生命周期、调用范式及商业化路径上存在本质区别。本文基于百炼平台当前（2024年Q3）正式发布的 API 规范撰写，聚焦可落地的技术选型决策依据。

## 关键维度对比

| 维度 | RAG API | [长期记忆](../concepts/long-term-memory.md)（LTM） |
|------|---------|----------------|
| **核心定位** | **面向静态/半静态知识库的语义检索与问答服务**：以文档、表格、图片、音视频等结构化/非结构化内容为输入，构建可复用、可共享、可监控的知识资产，服务于多用户、多场景的通用问答或精准检索。 | **面向动态交互过程的记忆沉淀与个性化复用服务**：以对话消息流（`messages`）、用户行为、[工具调用](../concepts/tool-calling.md)结果等为输入，自动抽取事实（`observation`）、技能（`skill`）、画像（`user_profile`），形成用户/项目粒度的私有化、演进式记忆图谱。 |
| **输入格式** | - 文档类：PDF/Word/Excel/PPT/Markdown/TXT 等文件（通过 OSS 上传或批量导入）<br>- 表格类：Excel/CSV 文件，列标题即字段名<br>- 多媒体类：图片 URL、音视频 URL（需开启多模态支持）<br>- 切片内容：JSON 格式，固定字段如 `content`/`title`/`image_urls`（文档类）或动态列映射（表格类） | - 消息流：标准 OpenAI-style `messages` 数组（含 `role`/`content`/`tool_calls`），支持 `image_url`（需多模态配置）<br>- 自定义内容：`custom_content` 字符串（用于简单 observation）<br>- 技能元信息：`skill_name`/`skill_description`/`skill_tags`（异步写入必需）<br>- 用户画像模板 ID：`profile_schema`（条件必填） |
| **输出格式** | - **检索接口**（`/knowledge/search`）：返回带相关性分数的文档片段列表（`chunks`），含 `content`、`source`、`score` 等字段<br>- **问答接口**（`/knowledge/chat`）：SSE 流式响应，最终输出自然语言答案，并可携带引用来源（`citations`）<br>- 所有管理接口（创建/更新/列表）返回标准 JSON 结构，含 `data`、`request_id`、分页信息等 | - **搜索接口**（`/memory_nodes/search`）：返回匹配的记忆节点数组，每个节点含 `id`、`type`（`observation`/`skill`/`user_profile`）、`content`、`score`、`created_at` 及类型特有字段（如 `skill_tags`）<br>- **画像接口**（`/profile_schemas/{id}/user_profile`）：返回结构化 JSON，字段由 `profile_schema` 定义<br>- **异步写入**：立即返回 `event_id`，需轮询 `GET /events/{event_id}` 获取抽取结果（含 `memory_node_id` 或错误详情） |
| **支持模型/能力** | - **模型无关**：RAG 本身不绑定特定大模型；检索与重排序（Rerank）使用平台内置向量模型与 Rerank 模型；最终问答由 Agent 中配置的 LLM（如 Qwen-Max/Qwen-Plus）执行<br>- 支持知识库类型：`document` / `table` / `image` / `multimedia`<br>- 支持结构类型：`unstructured` / `structured` | - **模型感知但非强耦合**：抽取阶段依赖平台智能体（AgentScope Runtime）内置的轻量级抽取模型；`intelligent` 模式下可能调用更强大的推理模型（透明封装）<br>- 记忆类型严格限定：`observation`（事实）、`skill`（流程化能力）、`user_profile`（结构化画像）<br>- 抽取模式：`efficient`（同步，低延迟） / `intelligent`（异步，高精度） |
| **API 端点（Base URL）** | `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`<br>所有接口统一网关，路径如：<br>`/api/v1/indices/rag/index/create_v2`<br>`/api/v1/indices/knowledge/search` | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory`<br>独立内存服务网关，路径如：<br>`/add-async`<br>`/memory_nodes/search`<br>`/profile_schemas/{id}/user_profile` |
| **鉴权方式** | `Authorization: Bearer <API-Key>`<br>API Key 在百炼控制台「API Key 管理」中获取，与业务空间解耦 | `Authorization: Bearer <DASHSCOPE_API_KEY>`<br>DASHSCOPE_API_KEY 为独立密钥，需在控制台「API Key 管理」中启用「长期记忆」权限 |
| **计费方式** | - **按调用量计费**：知识库创建、文档导入、切片操作、Agent 调用（检索/问答）均产生费用<br>- **分项计价**：知识库存储（GB/月）、文档解析（页/次）、向量索引（千条/次）、Rerank（次）、LLM 问答（[Token](../concepts/token.md)）等独立计费项<br>- 无免费额度，按实际用量结算 | - **商业化起始时间**：2026年8月20日10:00（北京时间）起正式计费<br>- **版本区分计费**：`Pro` 版本（支持 Rerank、`min_score` 过滤、`intelligent` 抽取）与 `Lite` 版本（基础检索）价格不同<br>- **当前为免费公测期**，但受账号级限流约束（3000 QPM 总量） |
| **典型场景** | - 企业知识库问答（HR政策、产品手册、技术文档）<br>- 数据库自然语言查询（Excel/CSV 表格问答）<br>- 图文混合检索（产品图库+说明书联合搜索）<br>- 客服机器人知识增强（对接 FAQ 库）<br>- 多租户 SaaS 应用的共享知识中心 | - 对话式应用中的用户偏好记忆（“上次说喜欢咖啡因含量低的茶”）<br>- 自动归纳用户工作习惯并生成可复用技能（“用户常要求将会议录音转纪要并标重点” → 抽取为 `skill`）<br>- 构建跨会话的用户画像（消费倾向、技术栈、沟通风格）<br>- Agent 自我进化：将成功解决的问题模式沉淀为 `skill`，供后续调用<br>- 私人助理类应用的个性化上下文管理 |

## 各方案的适用场景建议

### ✅ 选择 RAG API 当：
- 你拥有**明确、稳定、批量的外部知识源**（如数百份 PDF 文档、一个 Excel 产品数据库、一批产品图片），需要快速构建一个**可被多人、多应用共享调用的知识服务**；
- 你的核心需求是**精准召回原文片段**或**基于原文生成权威答案**，且对答案的溯源性、可审计性要求高；
- 你需要对知识库进行**精细化运营**：如按部门/项目划分知识库、设置访问权限、监控检索效果、A/B 测试不同切片策略；
- 你正在构建**标准化、可复用的 AI 应用组件**（如一个通用的“合同审查助手”），其知识底座相对固定。

### ✅ 选择长期记忆（LTM）当：
- 你的应用核心是**持续、动态的用户交互**（如个人助理、销售陪练、教育辅导），需要在对话过程中**自动捕捉、沉淀、复用个性化信息**；
- 你希望模型具备**“记住用户说过什么、做过什么、擅长什么”的能力**，而非仅回答预设问题；
- 你需要将**零散的对话经验升华为结构化、可检索、可导出的技能资产**（例如把多次成功的“周报生成”对话提炼成一个 `skill`）；
- 你计划构建**高度个性化的用户体验**，依赖跨会话的用户画像驱动推荐、摘要、提醒等行为；
- 你接受**异步处理流程**（尤其对 `skill` 和 `user_profile` 的抽取），并愿意为长期记忆的智能化能力（`intelligent` 模式）做工程适配。

### ⚠️ 不建议混用或替代的场景：
- **不要用 LTM 替代 RAG 做大规模文档问答**：LTM 不提供文档级全文检索、表格行列级查询、多媒体内容深度理解等 RAG 原生能力；其 `search` 接口面向记忆节点，非原始文档。
- **不要用 RAG 替代 LTM 做用户个性化记忆**：RAG 知识库是全局/租户级共享资源，缺乏 `user_id`/`project_id` 粒度的天然隔离与演化能力；无法自动从对话流中抽取 `skill` 或动态更新 `user_profile`。
- **二者可协同，但非叠加**：典型协同模式是——RAG 提供领域知识底座（如公司制度），LTM 提供用户个性化上下文（如该用户所属部门、历史咨询记录），两者通过 Agent 编排共同参与最终响应生成。

## 面向开发者的选型参考

| 决策维度 | RAG API | 长期记忆（LTM） | 选型提示 |
|----------|---------|----------------|----------|
| **数据准备成本** | 较高：需文档上传、格式校验、切片策略配置、知识库发布 | 极低：直接传 `messages` 数组即可启动写入（`efficient` 模式同步） | 若已有现成文档资产，选 RAG；若数据天然来自对话流，选 LTM。 |
| **开发复杂度** | 中高：需管理知识库生命周期、Agent 版本发布、处理流式问答响应、处理 `request_id` 排障 | 中：需理解 `user_id`/`project_id` 隔离模型、掌握异步轮询机制、适配 `profile_schema` | RAG 更适合有知识工程团队的场景；LTM 更适合快速迭代的对话应用开发。 |
| **实时性要求** | 检索/问答接口为实时响应（毫秒~秒级） | `efficient` 模式同步写入快；`intelligent` 模式需异步（秒级~分钟级） | 对写入实时性敏感（如即时反馈用户偏好），优先 `efficient` + LTM；对抽取精度要求高，接受异步，则选 `intelligent` + LTM。 |
| **运维与可观测性** | 提供完整的知识库监控面板（命中率、慢查询、切片统计） | 提供事件追踪（`event_id`）、记忆节点列表与搜索日志 | RAG 运维更成熟；LTM 运维能力随公测进展持续增强。 |
| **未来扩展性** | 易于接入新知识源类型（平台持续扩展 `knowledgeType`） | 易于扩展记忆类型与抽取能力（平台规划支持 `context`、`goal` 等新类型） | 两者均为百炼重点投入方向，长期看生态丰富度相当，但当前 RAG 功能更完备。 |
| **安全与合规** | 知识库可设置私有访问策略；文档内容存储于阿里云 OSS，符合等保要求 | `user_id` 级别强隔离；记忆内容默认永不过期，支持软删除与审计日志 | 敏感数据场景均需关注密钥管理与传输加密（HTTPS），二者均满足。 |

> **总结一句话选型口诀**：  
> **“有料用 RAG，有聊用 LTM；要查全用 RAG，要记深用 LTM；建中心用 RAG，养个人用 LTM。”**  
> 实际项目中，建议优先明确核心业务诉求——是解决“**我知道什么**”（RAG），还是解决“**我记得什么**”（LTM）。两者并非竞争关系，而是百炼平台为不同抽象层级的知识管理问题提供的专业化答案。

## 被对比主题页

- [rag api](../api/rag-api.md)
- [long term memory new](../api/long-term-memory-new.md)


