# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）与外部知识源动态结合的技术范式：在模型生成响应前，先从结构化或非结构化知识库中检索相关片段，并将其作为上下文注入提示（prompt），从而提升回答的准确性、时效性与可溯源性。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台，RAG 不是独立功能模块，而是贯穿多个服务层级的**核心能力模式**，其具体实现方式因场景而异：

- **Agent 场景（Managed / Flow Agent）**：通过绑定 `RAG` 上下文模块，自动在每次调用前执行知识检索。检索结果以结构化文本形式注入 LLM 输入上下文，开发者无需手动拼接 prompt；支持多知识库联合检索（通过 `kb_search_configs` 配置权重与过滤条件），并可启用 `enable_citation` 自动标注引用来源。

- **RAG API 专用服务**：提供端到端知识库生命周期管理（创建、导入、切片、更新）与两类原子能力接口：
  - `/knowledge/search`：纯检索接口，返回带元数据（如 `doc_id`, `score`, `chunk_id`）的原始片段；
  - `/knowledge/chat`：检索+生成一体化接口，自动完成检索→重排→注入→生成→引用标注全流程，适用于问答型应用。

- **框架集成（LlamaIndex / Spring AI Alibaba）**：通过 `DashScopeCloudRetriever` 或 `SpringAIAlibabaRagTemplate` 等封装组件，将百炼云端知识库无缝接入本地开发流程，复用标准 RAG pipeline（如 `QueryEngine`），同时保留[向量嵌入](vector-embedding.md)、重排、流式生成等全链路控制权。

- **Application Use Cases（业务集成）**：在钉钉/企业微信等渠道应用中，通过 `retrieval_config` 参数（含 `top_k`, `score_threshold`）声明式启用 RAG，平台自动路由至已发布的知识库服务，实现“零代码接入知识增强”。

- **Legacy Agent（Agent 1.0）**：以插件化方式接入知识库，检索结果直接追加至历史对话末尾，计入输入 token；需开发者自行控制切片长度以防超限，不支持重排与引用标注。

> ✅ **统一原则**：所有场景均基于百炼统一的知识库底座（`pipelineId` 标识），同一知识库可被多个 Agent、API 或框架实例共享复用。

## 关键参数和配置

| 参数名 | 所属场景 | 类型 | 说明 | 推荐值 |
|--------|----------|------|------|--------|
| `kb_search_configs` | Agent（`/v1/agents/{id}/chat`）、RAG Search API | `array<object>` | 多知识库联合检索配置，每个元素含 `id`（知识库 ID）、`weight`（权重）、`search_filters`（元数据过滤） | `[{"id": "idx-abc", "weight": 1.0}]` |
| `top_k` | RAG Search API、Application Use Cases、LlamaIndex Retriever | `integer` | 检索返回的最相关片段数量 | `3`（平衡精度与成本） |
| `score_threshold` | Application Use Cases、RAG Search API（部分模式） | `float` | 片段相似度最低阈值（0–1），低于则过滤 | `0.3`（默认）或 `0.5`（高精度场景） |
| `rerank_model_name` | RAG API（知识库级）、Agent 配置、LlamaIndex Retriever | `string` | 重排模型 ID，用于对初检结果二次排序 | `qwen3-rerank`（推荐）、`gte-rerank-hybrid`（混合重排） |
| `embeddingModelName` | RAG API（创建知识库时） | `string` | [向量嵌入](vector-embedding.md)模型，决定知识库索引质量 | `text-embedding-v4`（最新版，检索效果最优） |
| `enable_citation` | Agent（`/v1/agents/{id}/chat`）、RAG Chat API | `boolean` | 是否在生成结果中标注引用来源（如 `[1]`, `[2]`）及对应文档元信息 | `true`（生产环境建议开启） |

> ⚠️ 注意：  
> - `stream=true` 是 RAG Chat API 的强制要求，不支持非流式调用；  
> - `score_threshold` 在 RAG Search API 中需配合 `return_score=true` 使用；  
> - `rerank_model_name` 若未显式配置，系统将回退至知识库创建时指定的默认重排模型。

## 面向开发者，简洁实用

- **快速起步**：控制台创建知识库 → 上传文档 → 发布 → 在 Agent 配置页绑定 RAG 模块 → 调用 `/v1/agents/{id}/chat` 即可获得增强回答。  
- **调试技巧**：调用 RAG Search API（`/api/v2/apps/knowledge/search`）单独验证检索质量，观察 `score` 和 `metadata` 字段是否符合预期；再启用 `enable_citation` 查看生成结果是否合理引用。  
- **性能优化**：  
  - 高频查询场景：优先使用 `text-embedding-v4` + `qwen3-rerank` 组合；  
  - 低延迟敏感场景：设 `top_k=3` 并关闭重排（`enable_reranking=false`）；  
  - 多源知识融合：用 `kb_search_configs` 为不同知识库分配权重（如内部文档 `weight=1.2`，公开手册 `weight=0.8`）。  
- **避坑提醒**：  
  - 检索文本计入模型输入 token，务必监控 `input_tokens` 避免超限（Qwen 系列上限 32768）；  
  - 非 UTF-8 编码文档（如 GBK）可能导致解析失败，请预处理为 UTF-8；  
  - `agent_id` 是服务实例 ID，不可跨 `chat`/`search` 接口混用。

## 关联主题页

- [get started with agents](../guides/get-started-with-agents.md)
- [rag api](../api/rag-api.md)
- [frameworks](../api/frameworks.md)
- [use cases](../guides/use-cases.md)
- [application use cases](../guides/application-use-cases.md)
- [agent legacy](../guides/agent-legacy.md)


