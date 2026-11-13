# RAG、[长期记忆](../concepts/long-term-memory.md)与向量排序检索方案对比

本对比旨在帮助开发者清晰理解百炼平台三大核心检索增强能力的技术定位、能力边界与适用阶段，避免功能重叠误用或能力错配。随着AI应用从“单次问答”走向“持续交互+个性化服务”，RAG（知识库驱动）、[长期记忆](../concepts/long-term-memory.md)（用户状态建模）与底层向量/排序（原子能力层）已形成分层协同架构：**向量与排序是基础设施，RAG 是面向业务的知识服务封装，[长期记忆](../concepts/long-term-memory.md)则是面向用户的上下文状态管理**。本文聚焦技术选型维度，不涉及控制台操作指南或计费明细计算逻辑。

## 关键维度对比

| 维度 | RAG API | 长期记忆（New） | 向量与排序（Vector & Sort） |
|------|---------|----------------|-----------------------------|
| **核心定位** | 面向**结构化知识库**的端到端检索与问答服务（含索引构建、切片、混合检索、Agent 封装） | 面向**用户级状态**的结构化记忆写入、抽取与检索（支持事实、技能、画像三类记忆） | 面向**语义计算**的原子能力层（向量化 embedding + 相关性重排序 rerank），供上层自定义调用 |
| **输入格式** | 支持多源异构数据：<br>• 文档（PDF/Word/Excel/PPT/Markdown 等）<br>• 表格（CSV/Excel，自动结构化解析）<br>• 图片/音视频（需指定 `knowledgeScene`）<br>• 纯文本 query（检索/问答接口） | 以对话消息流（`messages`）为核心输入：<br>• `messages[].role` + `messages[].content`（支持 `text`/`image_url`）<br>• 可选 `profile_schema` 触发画像抽取<br>• 必填 `user_id` 实现用户隔离 | 高度标准化：<br>• **向量**：纯文本字符串、图像 URL/bytes、视频 URL/bytes、或多模态混合数组（`input.contents`）<br>• **排序**：`query` 字符串 + `documents` 字符串数组（或图文混合文档列表） |
| **输出格式** | 分场景返回：<br>• `/knowledge/search` → JSON 数组：`{chunk_id, content, score, source}`<br>• `/knowledge/chat` → 流式或非流式 LLM 响应 + 引用标注（`citation`）<br>• Agent 运行时自动融合模型推理与知识召回 | 结构化节点输出：<br>• `/add` → `memory_nodes[]`（含 `id`, `type`, `content`, `score`）<br>• `/search` → `memory_nodes[]`（可按 `type`/`score`/`project_ids` 过滤）<br>• `/user_profile` → 严格遵循 `profile_schema` 定义的 JSON 对象（如 `{"age": 32, "interests": ["AI", "travel"]}`） | 原子结果：<br>• **向量**：`embedding` 数组（float/base64） + `usage`（token 数）<br>• **排序**：`results[]` 数组，每项含 `index`, `relevance_score`, `document`（原始输入） |
| **支持模型** | • 嵌入模型：`text-embedding-v4`, `qwen3-vl-embedding` 等（知识库级配置）<br>• 重排序模型：`qwen3-rerank`（知识库级启用）<br>• Agent 模型：任意百炼托管 LLM（`qwen3`, `qwen3.7` 等） | • 抽取模型：内置 `efficient`（轻量）与 `intelligent`（高精度）两种策略（无显式模型名）<br>• 画像抽取：依赖 `profile_schema` 定义，由平台统一调度模型 | • 文本向量：`qwen3.7-text-embedding`, `text-embedding-v4`, `text-embedding-async-v2`<br>• 多模态向量：`qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06`<br>• 排序模型：`qwen3-rerank`, `qwen3-vl-rerank`, `gte-rerank-v2`（`gte-rerank` 已下线） |
| **API 端点** | 统一业务空间域名：<br>`https://{workspace_id}.cn-beijing.maas.aliyuncs.com`<br>路径前缀：`/api/v1/indices/...`（知识库）、`/api/v2/apps/knowledge/...`（问答） | 统一业务空间域名：<br>`https://{workspace_id}.cn-beijing.maas.aliyuncs.com`<br>路径前缀：`/api/v2/apps/memory/...`（如 `/add`, `/search`, `/user_profile`） | 双网关支持：<br>• DashScope 原生：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/services/embeddings/...`<br>• OpenAI 兼容：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings`（仅部分模型） |
| **计费方式** | 按**知识库实例生命周期**计费：<br>• 创建/更新/删除知识库：免费<br>• 文档导入、切片、检索、问答调用：按 token/请求次数计费<br>• Agent 调用：计入对应 LLM 模型费用 + RAG 附加费 | 按**调用行为**计费（2026年8月20日起正式商业化）：<br>• `Add` / `Search` 调用：区分 `Lite`（基础）与 `Pro`（含 rerank/min_score）版本<br>• `GetUserProfile`：免费（但依赖 `Add` 的付费抽取）<br>• 画像模板创建/管理：免费 | 按**调用粒度**计费：<br>• 向量：按输入 token 数或请求数（异步批处理按行数）<br>• 排序：按 `(query_tokens × doc_count) + sum(doc_tokens)` 总 token 数<br>• 免费额度按地域独立分配（如北京区有 `qwen3.7-text-embedding` 免费额度） |
| **典型场景** | • 企业知识库问答（制度/产品/客服文档）<br>• 表格数据自然语言查询（销售报表分析）<br>• 图片/视频内容理解（截图问答、视频摘要）<br>• 构建可引用、可审计的 AI 助手（开启 `enable_citation`） | • 用户个性化推荐（基于历史偏好/技能记忆）<br>• 多轮对话状态保持（“上次说要订机票”）<br>• 自动构建用户画像（年龄、兴趣、职业等结构化标签）<br>• Agent 技能复用（将“会议纪要生成流程”存为 `skill` 类型） | • 自研 RAG 系统的底层向量引擎（替代开源 embedding 模型）<br>• 跨模态搜索（图文混合检索）<br>• 检索后重排（对 Elasticsearch/向量库召回结果二次打分）<br>• 聚类/去重/相似度分析等离线任务 |

## 各方案的适用场景建议

- **优先选用 RAG API 当**：  
  ✅ 你拥有明确的、静态或半静态的**业务知识资产**（如 PDF 手册、数据库表、产品图片），需要快速构建一个可被自然语言查询的“智能知识库”；  
  ✅ 你需要开箱即用的**检索+问答一体化能力**，并要求结果具备来源引用、安全过滤（防泄漏）、混排路由等生产级特性；  
  ❌ 不适合高频变更的用户临时状态（如“用户刚说想买手机”，该信息生命周期短且需跨会话关联）。

- **优先选用长期记忆（New）当**：  
  ✅ 你需要在**多轮对话、跨会话、多 Agent 场景中持久化用户专属状态**，且这些状态具有明确语义类型（事实/技能/画像）；  
  ✅ 你需要**自动化抽取结构化用户标签**（如从对话中识别“用户是程序员，喜欢开源项目”），并用于后续个性化决策；  
  ❌ 不适合存储通用领域知识（如“Python 中如何读取 CSV 文件”），此类应放入 RAG 知识库。

- **优先选用向量与排序（Vector & Sort）当**：  
  ✅ 你需要**完全掌控检索流水线**（例如：用 Milvus 存向量、用 ES 做关键词召回、再用 `qwen3-rerank` 做融合排序）；  
  ✅ 你需要**超大批量离线处理**（如百万文档向量化、全量商品图库特征提取）；  
  ✅ 你需要**跨模态统一语义空间**（如用同一向量模型同时处理商品图文描述与用户搜索词）；  
  ❌ 不适合直接构建终端用户可见的问答服务——它不提供索引管理、切片、Agent 封装等应用层能力。

## 面向开发者的选型参考

| 你的需求 | 推荐方案 | 关键理由 | 注意事项 |
|----------|----------|----------|----------|
| “我要把公司 500 份 PDF 制度文档做成一个员工可问‘请假流程是什么’的机器人” | ✅ RAG API | 开箱即用的知识库创建、文档解析、切片、检索、问答全链路；支持 `enable_citation` 显示来源页码 | 需规划知识库类型（`basic_document_qa`），避免使用已下线的 `visual_document_qa` |
| “我的客服机器人需要记住用户上次投诉的产品型号，并在下次对话中主动跟进” | ✅ 长期记忆（New） | `observation` 类型天然适配短时效事实记忆；`user_id` 隔离确保隐私；软删除机制便于调试 | 记忆写入需搭配 `messages` 上下文，单条文本无法触发有效抽取 |
| “我已有 Elasticsearch 集群，想用百炼的 `qwen3-rerank` 提升搜索相关性” | ✅ 向量与排序 | 提供标准 HTTP 接口，输入 `query` + `documents` 即可返回重排结果；支持 OpenAI 兼容调用降低迁移成本 | 注意 `qwen3-vl-rerank` 的总 token 消耗上限（120,000），大文档集需分批 |
| “我想构建一个支持图文混合搜索的电商后台系统（搜‘红色连衣裙’返回图文商品）” | ⚠️ 组合使用：<br>• 向量与排序（`qwen3-vl-embedding`）→ 生成图文融合向量<br>• RAG API（`multimedia` 知识库）→ 管理商品库并提供检索接口 | 多模态向量提供统一语义空间；RAG 封装了索引、权限、监控等运维能力 | RAG 的 `multimedia` 场景需正确配置 `sinkType` 和 `multimodalEmbeddingModelName` |
| “我需要实时分析 10 万条用户评论，聚类出 TOP10 情感主题” | ✅ 向量与排序（异步批处理） | `text-embedding-async-v2` 支持单次 100,000 行，远超同步接口限制；返回向量可直接送入聚类算法 | [异步任务](../concepts/asynchronous-task.md)结果 URL 24 小时过期，需及时下载 |

> **重要协同提示**：三者并非互斥，而是分层协作。典型高级架构为：  
> **向量与排序** → 提供底层 embedding/rerank 能力，被 RAG 和长期记忆内部调用；  
> **RAG API** → 构建面向业务的知识服务，其知识库底层依赖向量模型；  
> **长期记忆** → 构建面向用户的上下文服务，其记忆抽取过程可能调用向量与排序能力。  
> 开发者可根据阶段选择：MVP 阶段用 RAG 快速上线；规模化后，用向量与排序优化性能；体验深化阶段，用长期记忆实现个性化。

## 被对比主题页

- [rag api](../api/rag-api.md)
- [long term memory new](../api/long-term-memory-new.md)
- [vector and sort](../api/vector-and-sort.md)


