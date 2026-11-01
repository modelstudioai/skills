# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）与外部知识源动态结合的技术范式：在模型生成响应前，先从结构化或非结构化知识库中检索相关片段，并将其作为上下文注入提示（prompt），从而提升回答的准确性、时效性与事实依据。

在百炼平台中，RAG 不是独立模块，而是贯穿于 Agent、应用服务与框架集成的核心能力，其核心价值在于**让模型“有据可依”——既避免幻觉，又无需重新训练或微调模型即可接入私域知识**。

## 在百炼平台的不同场景中，这个概念如何使用

- **Agent 编排场景**：通过 `agent_config.yaml` 或 API 的 `context.rag` 字段启用 RAG，指定一个或多个已发布的知识库 ID（`knowledge_base_ids`）。系统自动执行「查询向量化 → 多库并行检索 → 重排精筛 → 上下文拼接」全流程，并将 Top 5 检索结果（按 relevance score 排序）注入模型输入。适用于客服问答、内部知识助手等需强事实性的任务。

- **应用级问答服务**：调用 `/api/v2/apps/knowledge/chat`（流式）或 `/api/v1/indices/knowledge/search`（纯检索）时，必须传入 `agent_id`（对应已绑定知识库的 RAG Agent 实例）。该 Agent 封装了完整的 RAG pipeline，包括嵌入模型、重排模型及切片策略，开发者无需管理底层向量操作。

- **框架集成场景**：
  - 使用 LlamaIndex 时，通过 `DashScopeCloudRetriever` 直接对接百炼云端知识库，或使用 `DashScopeEmbedding` + `VectorStoreIndex` 构建本地索引；
  - 使用 Spring AI Alibaba 时，通过 `DashScopeDocumentRetriever` 调用 RAG API 完成检索，再交由本地 LLM 生成答案；
  - 所有框架集成均复用百炼统一的向量与重排模型（如 `text-embedding-v4`、`qwen3-rerank`），确保效果一致性。

- **自定义插件/应用开发**：在 `application support` 层，RAG 作为基础支撑能力被隐式调用——例如启用“知识库问答”插件后，平台自动路由至对应 RAG Agent；开发者只需关注业务逻辑，无需实现检索逻辑。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 | 默认值 |
|------|------|------|------|--------|
| `rag.enabled` | `agent_config.yaml` / API `context` 对象 | boolean | 启用 RAG 检索 | `false` |
| `rag.knowledge_base_ids` | API `context.rag` 或 SDK `context` 字典 | string[] | 指定要检索的知识库 ID 列表 | — |
| `rerank_top_n` | 知识库创建/更新时配置 | integer | 重排后返回的最高分结果数 | `3`（RAG API）、`100`（`DashScopeCloudRetriever`） |
| `rerank_min_score` | 知识库创建/更新时配置 | float | 过滤低相关性结果的阈值（0.0–1.0） | `0.0` |
| `dense_similarity_top_k` | `DashScopeCloudRetriever` 初始化参数 | integer | 向量召回阶段返回的候选数 | `100` |
| `enable_reranking` | `DashScopeCloudRetriever` 初始化参数 | boolean | 是否启用重排模型精排 | `True` |

> ⚠️ 注意：  
> - 单次请求最多检索 **5 个 chunk**（Agent 场景）或 **100 个文档**（RAG API 检索接口）；  
> - `context_window_size` 总长度受模型限制（如 Qwen-Turbo 最大 4096 tokens），RAG 结果会截断拼接，建议监控 `usage.context_tokens` 并主动优化知识库切分粒度；  
> - 多模态 RAG（如图文问答）需显式配置 `multimodalEmbeddingModelName`，否则报错。

## 面向开发者，简洁实用

- ✅ **快速启用**：控制台 Agent 编排页 →「上下文设置」→ 勾选 RAG → 绑定知识库 → 发布即可生效；  
- ✅ **精准调试**：在知识库测试面板中输入问题，查看原始检索 chunk、relevance score 及重排前后对比，快速定位不准原因；  
- ✅ **灵活组合**：RAG 可与 Memory（历史对话）、Connector（实时数据库/API）同时启用，但需注意总 token 预算；  
- ✅ **自主可控**：支持自定义嵌入模型（`text-embedding-v3`）、重排模型（`gte-rerank-hybrid`）及切分策略（`DashScopeJsonNodeParser`），满足高阶需求；  
- ❌ **避坑提示**：不要混淆 `knowledge_base_id`（知识库 ID）与 `agent_id`（RAG Agent 实例 ID）；调用 `/knowledge/chat` 必须传 `agent_id`，而非知识库 ID。

## 关联主题页

- [agent context](../guides/agent-context.md)
- [rag api](../api/rag-api.md)
- [frameworks](../api/frameworks.md)
- [application support](../guides/application-support.md)
- [vector and sort](../api/vector-and-sort.md)


