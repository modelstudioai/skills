# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）与外部知识源动态结合的技术范式：在模型生成响应前，先从结构化或非结构化知识库中检索相关片段，并将其作为上下文注入提示（prompt），从而提升回答的准确性、时效性与领域专业性，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼平台中不是单一功能模块，而是贯穿知识管理、Agent 运行和应用集成的核心能力架构：

- **知识库服务（RAG API）**：通过 `rag/index` 系列接口构建私有知识库，支持文档上传、智能切片、向量化（Embedding）、混合检索（向量+全文）及重排序（Rerank）。调用 `/knowledge/search` 或 `/knowledge/chat` 时，系统自动完成“检索→精排→注入→生成”全流程，无需开发者手动拼接上下文。

- **Agent 上下文（Agent Context）**：RAG 是 `context` 的核心组件之一。通过配置 `knowledge_base_ids`，可为 Agent 动态挂载一个或多个知识库；检索结果以 `<doc>` 标签格式自动注入 prompt，与 Memory、Connector 等上下文模块协同工作，实现多源信息融合推理。

- **多渠道 AI 助手（Application Use Cases）**：所有网站、微信公众号、企业微信、钉钉等渠道集成方案均默认基于 RAG 架构。开发者只需在应用配置中启用知识库并设置调用策略（如“必定调用”），即可让终端用户获得基于私有文档的精准问答能力，无需修改前端或渠道逻辑。

- **框架集成（Frameworks）**：百炼原生支持 LlamaIndex 和 Spring AI Alibaba，提供 `DashScopeCloudRetriever`、`DashScopeEmbedding`、`DashScopeRerank` 等封装组件，使开发者能用几行代码构建本地+云端混合 RAG 流程，灵活替换嵌入/重排模型、自定义切分策略，兼顾开发效率与控制粒度。

## 关键参数和配置

RAG 行为由以下关键参数驱动，按作用层级分为知识库级、Agent 级和请求级：

| 参数名 | 所属层级 | 类型 | 说明 | 推荐值 |
|--------|----------|------|------|--------|
| `embeddingModelName` | 知识库创建 | string | 指定文本嵌入模型，影响检索召回质量 | `"text-embedding-v4"`（最新版） |
| `rerankModelName` | 知识库配置 | string | 指定重排序模型，用于对初检结果精细化打分排序 | `"qwen3-rerank"`（百炼推荐） |
| `rerankTopN` / `rerankMinScore` | 知识库配置 | int / float | 控制重排后返回数量与最低分数阈值，过滤低质片段 | `5`, `0.35` |
| `knowledge_base_ids` | Agent `context` | string[] | 指定启用的知识库 ID 列表，为空则禁用 RAG | `["kb-abc123"]` |
| `dense_similarity_top_k` / `sparse_similarity_top_k` | `DashScopeCloudRetriever` | int | 混合检索中向量/全文各自召回数 | `100`, `100` |
| `enable_reranking` | `DashScopeCloudRetriever` | bool | 是否启用重排，默认开启 | `true` |

> ⚠️ 注意：  
> - 单次请求中，RAG 检索内容 + Memory + Connector 返回总长度不得超过模型最大上下文的 80%，否则触发静默截断；  
> - 多模态 RAG 需配合 `qwen3-vl-embedding` 和 `DASH_QWEN_VL_PARSER` 使用，不兼容纯文本嵌入模型；  
> - `相似度阈值` 和 `召回片段数` 可在控制台知识库引用配置页或 API 请求体中动态调整，直接影响回答的相关性与简洁性。

## 面向开发者，简洁实用

- ✅ **快速起步**：用 RAG API 创建知识库 → 上传 PDF/DOCX → 发布 Agent 并配置 `knowledge_base_ids` → 调用 `/v1/agents/{id}/chat` 即可获得增强回答。  
- ✅ **精细调优**：若发现答案冗余，调小 `rerankTopN`；若相关性不足，提高 `rerankMinScore` 或切换为 `text-embedding-v4`；若需更细粒度切分，改用 `DashScopeJsonNodeParser(chunk_size=256)`。  
- ✅ **框架复用**：LlamaIndex 用户可直接使用 `DashScopeCloudRetriever` 替代本地 `VectorStoreIndex`，无缝对接百炼云端知识库，无需维护向量存储。  
- ✅ **避坑提示**：`pipelineId`/`indexId`/`index_id` 命名不统一，务必严格按接口文档传参；`agent_id` 必须先创建并发布，不可直接使用知识库 ID。  

RAG 不是黑盒服务，而是百炼平台中可观察、可配置、可组合的确定性能力——掌握上述参数与场景映射，即可稳定交付高质量私有知识问答体验。

## 关联主题页

- [rag api](../api/rag-api.md)
- [agent context](../guides/agent-context.md)
- [application use cases](../guides/application-use-cases.md)
- [frameworks](../api/frameworks.md)


