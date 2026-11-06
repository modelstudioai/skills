# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态检索相关上下文片段，并将其注入提示词（prompt），使模型能在私有、实时、结构化或非结构化知识基础上生成更准确、可溯源、低幻觉的回答。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，RAG 不是单一功能模块，而是贯穿知识管理、智能体运行、框架集成与应用交付的**核心增强机制**，具体体现为以下四类典型用法：

- **知识库驱动的问答服务**：通过 RAG API 创建 `document`/`table`/`image`/`multimedia` 类型知识库，上传 PDF、Excel、图片等文件，系统自动完成解析、切片、向量化与索引；调用 `/api/v1/indices/knowledge/search`（纯检索）或 `/api/v2/apps/knowledge/chat`（检索+生成）接口，即可获得基于私有知识的流式回答。

- **智能体（Agent）的上下文增强**：在 Agent 配置中启用 `"context_sources": ["rag"]`，并设置 `rag_top_k`（默认 3），RAG 将作为 [agent context](../guides/agent-context.md) 的一部分，在每次调用时自动检索匹配知识片段，与 memory、connector 等协同注入 prompt，支撑多轮、状态感知的对话。

- **主流框架原生集成**：  
  - LlamaIndex 中通过 `DashScopeCloudRetriever` 调用云端知识库，支持稠密/稀疏混合检索 + `gte-rerank-hybrid` 重排，默认返回 `rerank_top_n=5` 个高质量节点；  
  - Spring AI Alibaba 中通过 `DashScopeDocumentRetriever` 实现知识库检索，并支持 `searchFilters` 多条件组合（如按标签、时间、来源过滤）。

- **低代码应用快速落地**：在控制台创建智能体应用后，直接绑定已发布的知识库，配置 `knowledge_call_mode`（`必定调用` 或 `按需调用`）与 `retrieval_top_k`（建议 3–5），即可零代码启用 RAG 增强的客服、文档助手等场景，无缝对接微信公众号、企业微信、钉钉、网站等渠道。

## 关键参数和配置

| 参数 | 所属层级 | 说明 | 推荐值 | 注意事项 |
|------|----------|------|--------|-----------|
| `retrieval_top_k` / `rag_top_k` | 应用层 / Agent 层 | 检索返回的原始片段数（重排前） | `3`–`5` | 过高易引入噪声，过低可能漏检关键信息；Agent 中为 `rag_top_k`，应用配置中为 `retrieval_top_k`，语义一致 |
| `similarity_threshold` | 应用层 | 向量相似度最低阈值（0–1），低于此值的片段被过滤 | `0.3`–`0.7` | 设为 `0` 表示不限制；实际生效依赖知识库所用 embedding 模型的归一化特性 |
| `enable_reranking` / `rerank_model_name` / `rerank_top_n` | 框架层（LlamaIndex） | 是否启用重排、重排模型名、重排后最终返回数 | `True`, `gte-rerank-hybrid`, `5` | 重排显著提升相关性，`gte-rerank-v2` 性能优于 v1；`rerank_top_n` ≤ `dense_similarity_top_k` |
| `knowledgeScene` | RAG API 层 | 知识库场景标识，决定处理逻辑与模型选型 | `lite_document_qa`, `visual_perception_qa` 等 | 必须与 `knowledgeType` 组合使用；`lite_document_qa` 要求 `sinkType=BUILT_IN` |
| `agent_id` | RAG API 运行时 | 绑定已发布 Agent 的唯一 ID，承载知识库、模型、策略等全部配置 | 由 `/api/v1/indices/rag/app/publish` 返回 | 所有 RAG 运行时接口（`/knowledge/search`, `/knowledge/chat`）均需传入，**不在请求体中配置策略**，策略必须预置在 Agent 中 |

> ⚠️ 重要原则：**所有检索策略（多库权重、混排逻辑、路由规则、重排模型）均需在 Agent 或知识库创建/更新阶段通过 `agent_config` 或 API 请求体预先定义并发布，不可在运行时动态指定。**

## 面向开发者，简洁实用

- ✅ **起步最快路径**：控制台上传文件 → 创建标准知识库 → 创建智能体应用 → 绑定知识库 → 发布 → AppFlow 集成到网站/企微；全程无需写一行后端代码。  
- ✅ **API 自主可控路径**：用 RAG API 管理知识库生命周期 → 用 Agent API 配置 `agent_config`（含 `retriever_config`、`reranker_config`）→ 发布 Agent → 运行时仅需 `POST /knowledge/chat` + `agent_id` + `query`。  
- ✅ **框架高效开发路径**：Python 项目 `pip install llama-index-indices-managed-dashscope` → 初始化 `DashScopeCloudIndex` → `index.as_retriever()` 获取 `DashScopeCloudRetriever` → 直接 `.retrieve("问题")`。  
- ❌ **避免踩坑**：  
  - 不要尝试在 `/knowledge/chat` 请求体中传 `top_k` 或 `rerank_model` —— 它们只在 Agent 配置中生效；  
  - 使用 `DashScopeParse` 时务必显式传 `category_id`，否则智能解析不触发；  
  - 多模态 RAG（如图片问答）必须指定 `multimodalEmbeddingModelName`，且仅 `qwen-vl` 等多模态模型支持 ParseX OCR。  

RAG 是百炼平台实现“私有知识即服务”的技术底座。善用它，你交付的不是通用聊天机器人，而是懂你业务、知你文档、答你所问的专业智能体。

## 关联主题页

- [rag api](../api/rag-api.md)
- [frameworks](../api/frameworks.md)
- [application use cases](../guides/application-use-cases.md)
- [agent context](../guides/agent-context.md)
- [agent governance](../guides/agent-governance.md)


