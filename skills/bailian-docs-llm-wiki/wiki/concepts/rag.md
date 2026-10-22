# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态检索相关文档片段，并将其作为上下文注入 prompt，显著提升回答的事实准确性、领域专业性和时效性，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台，RAG 不是独立模块，而是贯穿多个能力层的**核心增强机制**，具体体现为以下三种协同模式：

- **Agent 场景（推荐首选）**：在 `qwen-agent-2.5` 及以上 Agent 模型中，通过 `context_config.knowledge_base_ids` 直接绑定一个或多个已发布的知识库 ID。平台自动完成“查询→向量检索→重排→片段注入→生成”全链路，开发者无需编写检索逻辑，仅需配置即可启用。此方式深度集成 Memory 与 Connector，天然支持多轮问答中的上下文感知与知识联动。

- **RAG API 运行时调用**：通过 `/api/v1/indices/knowledge/search`（纯检索）或 `/api/v2/apps/knowledge/chat`（检索+生成一体化）接口，传入 `agent_id` 显式触发 RAG 流程。适用于需要细粒度控制检索行为（如自定义 `search_filters`）、或需将检索结果用于非生成类下游任务（如内容摘要、合规校验）的场景。

- **框架集成（LlamaIndex / Spring AI Alibaba）**：使用 `DashScopeCloudRetriever` 或 `DashScopeDocumentRetriever` 组件，以代码方式接入百炼云端知识库。适合已有 LlamaIndex 工程、需复用本地索引逻辑，或需在检索后插入自定义后处理（如规则过滤、敏感词脱敏）的开发者。

> ✅ 共同前提：所有方式均要求知识库已完成创建、文档导入、切分与向量索引构建，并处于「已发布」状态。

## 关键参数和配置

| 参数位置 | 参数名 | 类型 | 说明 | 默认值 / 注意事项 |
|----------|--------|------|------|-------------------|
| `context_config`（Agent） | `knowledge_base_ids` | string[] | 关联的知识库 ID 列表 | 必填；最多支持 5 个知识库并行检索 |
| `retrieval_config`（应用用例） | `top_k` | integer | 检索返回的原始片段数 | `3`；不可通过该字段调整，如需更多结果请改用 RAG API |
| `retrieval_config`（应用用例） | `rerank` | boolean | 是否启用重排序 | `false`；设为 `true` 后使用默认 `qwen3-rerank` 模型 |
| RAG API `/search` | `top_k` | integer | 检索阶段返回的文档片段数 | `3`（服务端硬编码，不可覆盖） |
| `DashScopeCloudRetriever` | `dense_similarity_top_k`, `rerank_top_n` | integer | 向量召回数、重排后返回数 | `100`, `5`；可显式配置，优于默认限制 |

> ⚠️ 重要限制：  
> - 所有 RAG 路径均**不支持嵌套检索**（例如在 Connector 返回内容中再次触发 RAG）；  
> - 知识库路由（`kb_router_model`）与混合重排（`hybrid_rerank`）需在 Agent 配置中统一声明，无法在单次请求中临时覆盖；  
> - 检索结果默认截断为 top-3 片段，若需更高灵活性（如动态 top-k 或自定义重排），请直接调用 RAG API 或使用 `DashScopeCloudRetriever`。

## 面向开发者，简洁实用

- **快速上手**：优先使用 Agent 模式 + `context_config`，3 行 JSON 即可启用 RAG，适合 90% 的问答/客服/知识助手场景。  
- **调试技巧**：开启 `stream=True` 并关注 `tool_calls` 字段，可观察模型是否准确识别并调用 `retrieval` 工具；若未触发，检查 `knowledge_base_ids` 是否有效、知识库是否已发布。  
- **性能优化**：对长文档问答，建议在知识库创建时选用 `text-embedding-v3`（高精度）+ `qwen3-rerank`（强语义），并在 `DashScopeCloudRetriever` 中设置 `rerank_top_n=3` 平衡效果与延迟。  
- **避坑指南**：  
  - 文件上传必须使用小写后缀（如 `report.pdf`，非 `REPORT.PDF`）；  
  - `context_config` JSON 序列化后总大小 ≤ 16KB，避免一次性绑定过多知识库；  
  - 企业微信/钉钉等平台集成时，RAG 结果需经 `tools` 回调透传，务必在 `tools` 中声明 `retrieval` 并确保权限开通。

## 关联主题页

- [agent context](../guides/agent-context.md)
- [rag api](../api/rag-api.md)
- [frameworks](../api/frameworks.md)
- [vector and sort](../api/vector-and-sort.md)
- [application use cases](../guides/application-use-cases.md)
- [application support](../guides/application-support.md)


