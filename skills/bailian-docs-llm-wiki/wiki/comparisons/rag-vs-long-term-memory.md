# RAG 与[长期记忆](../concepts/long-term-memory.md)能力对比

为帮助开发者在百炼平台中合理选型，本文对 **RAG（[检索增强生成](../concepts/rag.md)）API** 与 **[长期记忆](../concepts/long-term-memory.md)（Long Term Memory, LTM）服务** 进行系统性对比。二者虽均面向“外部知识接入”与“上下文增强”，但设计目标、数据模型、生命周期管理及适用范式存在本质差异：  
- **RAG** 是面向**静态知识库的端到端问答系统**，强调结构化文档/多模态资产的离线构建、向量化索引与联合检索，适用于**领域知识沉淀与专业问答场景**；  
- **[长期记忆](../concepts/long-term-memory.md)** 是面向**动态用户交互的结构化记忆中枢**，聚焦事实观察、技能封装与用户画像的实时写入、语义关联与跨会话复用，适用于**个性化 Agent、持续学习型应用与状态敏感型对话系统**。  

本对比基于当前（2025年Q2）百炼平台正式版 API 行为，所有结论已通过接口实测与文档交叉验证。

## 关键维度对比

| 维度 | RAG API | 长期记忆（LTM） |
|------|---------|----------------|
| **核心定位** | 静态知识库驱动的检索增强问答服务，以“知识即资产”为前提 | 动态交互驱动的记忆中枢，以“记忆即状态”为核心，支持跨会话、跨用户、跨项目持续演进 |
| **输入格式** | 支持结构化/非结构化混合输入：<br>• 文档（PDF/DOCX/TXT/CSV 等）<br>• 表格（Excel/CSV，自动识别 schema）<br>• 图片/音视频（需 `multimedia` 类型知识库）<br>• 查询文本或图像（`/search` 接口） | 以自然语言消息流为主：<br>• `messages`（含 `role`/`content`/`image_url`）<br>• `custom_content`（纯文本片段）<br>• 可选 `profile_schema` 触发画像抽取<br>• 不接受原始文件上传（无 OSS 租约等流程） |
| **输出格式** | • 检索结果：`documents` 列表（含 `content`、`score`、`metadata`）<br>• 问答结果：流式 `text` + `citations`（引用来源 ID）+ `status`（`completed`/`error`）<br>• 所有响应为 JSON，无原始二进制内容 | • 写入响应：同步返回 `memory_nodes`（含 `id`/`type`/`content`/`embedding_vector`）；异步返回 `event_id`<br>• 检索响应：`memory_nodes` 列表（含 `id`/`type`/`content`/`score`/`source`），支持 `observation` 与 `skill` 混合返回<br>• 用户画像：`GET /profile_schemas/{id}/user_profile` 返回结构化属性字典 |
| **支持模型/能力** | • 嵌入模型：`text-embedding-v4`、`qwen3-vl-embedding`<br>• 重排序模型：`qwen3-rerank`<br>• 多模态理解：`visual_perception_qa`、`basic_table_qa` 等专用 pipeline<br>• 依赖预构建的 Agent 封装能力 | • 统一嵌入与抽取模型（内部托管，不暴露模型名）<br>• 抽取模式：`efficient`（低延迟）与 `intelligent`（高精度，推荐异步）<br>• 技能记忆：支持 `skill_name`/`skill_description`/`skill_tags` 元数据<br>• 用户画像：基于模板的结构化属性抽取（如 `age`、`preference`、`behavior_pattern`） |
| **API 端点** | 统一业务空间 Endpoint：<br>`https://{workspace_id}.cn-beijing.maas.aliyuncs.com`<br>• 知识库管理：`/api/v1/indices/rag/...`<br>• Agent 管理：`/api/v1/indices/rag/app/...`<br>• 运行时：`/api/v1/indices/knowledge/search`、`/api/v2/apps/knowledge/chat` | 统一业务空间 Endpoint：<br>`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory/`<br>• 写入：`POST /add`、`POST /add-async`<br>• 检索：`POST /memory_nodes/search`<br>• 管理：`GET /memory_nodes`、`GET /memory_nodes/{id}`、`DELETE /memory_nodes/{id}`<br>• 画像：`POST /profile_schemas`、`GET /profile_schemas/{id}/user_profile` |
| **认证方式** | `Authorization: Bearer <BAILIAN_API_KEY>`<br>（使用百炼控制台生成的 `BAILIAN_API_KEY`） | `Authorization: Bearer <DASHSCOPE_API_KEY>`<br>（使用 DashScope 控制台生成的 `DASHSCOPE_API_KEY`） |
| **计费方式** | • 按知识库容量（GB/月）+ 检索调用量（次）+ 问答 [Token](../concepts/token.md) 数计费<br>• 知识库创建、文档导入、切片管理等管理类操作免费<br>• 详见 [RAG 计费说明](raw/application-user-guide/rag-billing/billing.md) | • 商业化起始时间：2026 年 8 月 20 日起<br>• 当前为公测期，免费使用<br>• 计费单元：<br>  - `Add`（写入）：按事件数（`event_id`）计费，区分 `pro`/`lite` 版本<br>  - `Search`（检索）：按查询次数计费，`pro` 版本支持 `min_score` 过滤，`lite` 版本不生效<br>• 详见 [LTM 计费说明](raw/application-user-guide/agent-billing/billing.md) |
| **数据生命周期** | • 知识库/文档/切片均为**永久存储**（除非显式删除）<br>• 删除操作为**硬删除**（不可恢复）<br>• 无自动过期或 TTL 机制 | • 记忆节点默认**永不过期**<br>• 删除为**软删除**（`status=delete`），仍可通过 `GetMemoryNode` 查看<br>• 用户画像为异步抽取，首次查询可能为空，需业务侧重试<br>• 无自动清理策略，需开发者主动管理 |
| **隔离粒度** | • 主隔离：`workspace_id`（业务空间）<br>• 次级隔离：`index_id`（知识库）、`fileId`（文档）、`agent_id`（问答管道）<br>• **无用户级隔离原语**（需应用层自行实现） | • 强制三级隔离：<br>  - `user_id`（必填，用户级强隔离）<br>  - `project_id` 或 `project_ids`（项目级规则隔离）<br>  - `memory_library_id`（可选记忆库分组）<br>• 数据可见性由三者交集决定，天然支持多租户 |
| **典型场景** | • 企业内部知识库问答（如产品手册、制度文档）<br>• 客服机器人对接 FAQ 与工单历史<br>• 表格数据自然语言查询（如销售报表分析）<br>• 图片/视频内容理解与问答（如医疗影像报告生成） | • 个性化 AI 助手（记住用户习惯、偏好、过往请求）<br>• 技能可复用的 Agent（如“会议纪要生成”、“周报撰写”作为 `skill` 节点）<br>• 用户画像驱动的推荐与决策（如教育场景中记录学生错题模式）<br>• 多轮对话中的状态持久化（避免重复确认、上下文断裂） |

## 各方案的适用场景建议

| 场景特征 | 推荐方案 | 理由说明 |
|----------|----------|----------|
| **知识源稳定、更新频率低（月更/季更）、内容体量大（GB 级文档/表格/图片）** | ✅ RAG API | RAG 的知识库批量导入、OSS 集成、多模态切片与重排序能力，专为大规模静态资产优化；长期记忆不支持文件上传与结构化解析。 |
| **需严格权限管控、按部门/项目划分知识边界，且无用户身份体系** | ✅ RAG API | RAG 通过 `index_id` + `agent_id` 实现资源级隔离，配合 RAM 子账号最小权限策略，适合组织内知识分域管理；LTM 强制要求 `user_id`，无纯资源隔离模式。 |
| **应用需记忆用户个性化信息（如“张三喜欢咖啡因”、“李四常在周五下午提交代码”）、并跨会话复用** | ✅ 长期记忆 | LTM 原生支持 `user_id` 隔离、`observation` 事实记忆与异步画像抽取，是唯一能天然承载“用户状态”的服务；RAG 无法绑定用户身份，所有检索对所有用户开放。 |
| **需将可复用能力封装为标准化模块（如“合同条款比对”、“简历打分”），供多个 Agent 调用** | ✅ 长期记忆 | `skill` 类型记忆支持元数据标注（`skill_tags`）、语义检索与版本化管理，比 RAG 中“将技能文档存为知识库”更轻量、更结构化、更易发现。 |
| **需同时满足：① 对接企业知识库 + ② 记住用户个性化行为 + ③ 实现技能复用** | ⚠️ **组合使用** | 推荐架构：RAG 作为“公司大脑”（处理制度、产品、案例等公共知识），LTM 作为“个人小脑”（记录用户习惯、技能调用历史、画像）；两者通过 `agent_id`（RAG）与 `user_id`（LTM）在应用层桥接。 |
| **快速原型验证、无需复杂知识工程、仅需轻量级上下文记忆（如聊天机器人记住上一句）** | ✅ 长期记忆（Lite 版） | LTM 异步写入接口简单（仅需 `user_id` + `messages`），无知识库创建、Agent 发布等前置步骤，开发成本显著低于 RAG。 |

## 面向开发者的选型参考

作为技术决策者，请依据以下 checklist 快速判断：

🔹 **选 RAG 当且仅当：**  
- 你的核心数据是**已存在的文档、表格、图片等静态资产**；  
- 你希望用户用自然语言**查询这些资产的内容**（而非记录用户说了什么）；  
- 你没有用户身份体系，或所有用户共享同一套知识视图；  
- 你需要**精确控制检索结果来源**（如必须引用某份 PDF 的第 3 页）；  
- 你愿意投入精力完成知识库创建 → 文档导入 → 切片配置 → Agent 发布的完整流程。

🔹 **选长期记忆当且仅当：**  
- 你的核心数据是**用户在对话中产生的新信息**（如“帮我订明天上午 10 点的会议室”）；  
- 你需要**区分不同用户、不同项目、不同记忆类型**（事实 vs 技能）；  
- 你希望记忆具备**语义关联能力**（如搜索“会议”能召回“订会议室”和“生成纪要”两个 skill）；  
- 你追求**极简接入**：无需建库、无需切片、无需发布 Agent，只需 `POST /add-async` 即可开始积累；  
- 你计划构建**长期演化的个性化 Agent**，而非一次性问答工具。

> 💡 **重要提醒**：二者非互斥关系。百炼最佳实践推荐“RAG + LTM”协同架构——RAG 提供权威、稳定的领域知识底座，LTM 提供鲜活、个性化的用户上下文。在 `knowledge/chat` 问答中，可先用 LTM 检索用户相关 `observation`，再将其作为 context 注入 RAG 请求，实现“既懂行业，又懂你”的智能体验。

---  
*最后更新：2025年6月*  
*文档版本：bailian-platform-wiki/v2.3*

## 被对比主题页

- [rag api](../api/rag-api.md)
- [long term memory new](../api/long-term-memory-new.md)


