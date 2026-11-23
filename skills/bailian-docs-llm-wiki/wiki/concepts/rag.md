# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）与外部知识源动态结合的技术范式：在模型生成响应前，先从结构化或非结构化知识库中检索相关片段，并将其作为上下文注入提示词，从而提升回答的准确性、时效性与可溯源性。该技术有效缓解了 LLM 的幻觉、知识陈旧和领域泛化不足等问题，是百炼平台构建可信企业级 AI 应用的核心能力底座。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼平台并非单一功能模块，而是贯穿多个产品层级的**横切能力**，按使用方式可分为三类：

- **开箱即用型 RAG（Managed RAG）**  
  通过控制台「知识库」页面上传文档（PDF/DOCX/XLSX/PPTX/图片等），自动完成解析、切片、向量化（默认 `text-embedding-v4` 或 `qwen3-vl-embedding`）与索引构建；再在「智能体应用」或「Agent」配置中一键启用知识库并设为“必定调用”，即可实现零代码 RAG 增强。适用于客服问答、产品手册助手等标准化场景。

- **API 驱动型 RAG（RAG API）**  
  通过 `rag-api` 提供的 `/api/v1/indices/knowledge/search`（纯检索）和 `/api/v2/apps/knowledge/chat`（检索+生成）接口，以 `agent_id` 为枢纽，将知识检索与 LLM 生成解耦封装。开发者可自主控制检索过滤（如按 `doc_id`、`tags`）、混排策略（如 `qwen3-rerank`）、多模态查询（文本+图片），并集成到自有系统中。典型用于需定制路由逻辑、审计溯源或混合私有/公有知识源的生产系统。

- **开发可控型 RAG（Sandbox / Flow Agent）**  
  在 Sandbox 模式下，使用 `bailian-sdk` 调用 `KnowledgeRetriever` 工具，手动控制 `top_k`、`similarity_threshold`、重排序逻辑及上下文拼接方式；在 Flow Agent 中，可通过「知识库检索」节点接入自定义知识源，并与条件分支、HTTP 工具等组合编排。适用于需精细控制检索粒度、融合数据库查询或实现分阶段推理（如“先查政策→再判合规→最后生成话术”）的复杂业务流。

> ✅ 统一原则：所有 RAG 路径均共享同一套知识库存储与向量索引，一次上传，多处复用；检索结果默认以 `<doc id="xxx">...</doc>` 格式注入 Prompt，模型无需额外微调即可理解上下文来源。

## 关键参数和配置

RAG 行为由以下关键参数控制，按作用层级分类：

| 参数名 | 所属层级 | 说明 | 推荐值 | 注意事项 |
|---------|-----------|------|----------|------------|
| `retrieval_top_k` | 应用层（控制台/API） | 检索返回的最相关片段数量 | `3–5` | 过大会增加 token 开销与噪声；过小可能遗漏关键信息。在 `application-use-cases` 和 `agent-development` 中均显式暴露。 |
| `similarity_threshold` | 应用层（控制台/API） | 向量相似度阈值，低于此值的片段被过滤 | `0.3–0.6` | 适用于高精度场景（如法律条款引用），默认不启用；需配合支持阈值过滤的知识库类型（如 `unstructured`）。 |
| `kb_search_configs` | RAG API 层 | 检索配置对象，含 `filter`（字段过滤）、`rerank_model`（重排模型）、`vector_model`（嵌入模型）等 | `{ "filter": { "tags": ["faq"] } }` | 必须在 Agent 管理 API 中预配置，运行时不可变；`filter` 支持 `doc_id`、`category_id`、自定义 `tags` 等字段。 |
| `enable_rag` | Agent 层（Flow/Managed） | 是否启用 RAG 检索开关 | `true` | Flow Agent 中需在节点属性中开启；Managed Agent 中在知识库绑定后自动生效。 |
| `chunk_size` / `chunk_overlap` | 知识库构建层（控制台/API） | 文档切片大小（字符数）与相邻切片重叠长度 | `512–1024` / `64–128` | 影响召回精度与上下文完整性；大模型（如 `qwen3.7-max`）建议用较大 `chunk_size`；图文混合场景需同步调整视觉切片策略。 |

> ⚠️ 重要限制：RAG 检索内容直接计入模型输入上下文。若 `retrieval_top_k × avg_chunk_length + prompt_length` 超出模型上下文窗口（如 `qwen-plus` 为 32768 tokens），将触发截断且无告警。务必在上线前用真实数据压测总 token 消耗。

## 面向开发者，简洁实用

- **快速验证**：用 CLI 一行命令发起 RAG 问答 → `bl rag chat --query "产品保修期是多久？" --knowledge-base-id kb-xxx`  
- **调试技巧**：在控制台应用配置页开启「显示检索结果」，可直观查看哪些文档片段被召回及相似度分数。  
- **性能优化**：高频查询场景建议启用 `qwen3-rerank` 重排模型（比纯向量检索准确率高 15%+），并在知识库创建时指定 `multimodalEmbeddingModelName` 以对齐图文语义空间。  
- **安全兜底**：所有 RAG 路径均默认启用防泄漏策略（自动脱敏手机号/身份证号）和拒答机制（当检索结果置信度低或无匹配时返回标准兜底话术）。  
- **错误排查**：若返回“未找到相关信息”，优先检查 `similarity_threshold` 是否过高、`kb_search_configs.filter` 是否误过滤、或知识库状态是否为 `ACTIVE`（非 `PENDING`/`FAILED`）。  

RAG 不是黑盒插件，而是你掌控知识边界的杠杆——精调参数、善用过滤、监控 token，方能释放其全部价值。

## 关联主题页

- [rag api](../api/rag-api.md)
- [getting started](../guides/getting-started.md)
- [capabilities](../guides/capabilities.md)
- [application use cases](../guides/application-use-cases.md)
- [agent development](../guides/agent-development.md)
- [agent legacy](../guides/agent-legacy.md)
- [use cases](../guides/use-cases.md)


