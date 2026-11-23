# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，简称 RAG）是一种将大语言模型（LLM）与外部知识源动态结合的技术范式：在生成响应前，系统先从结构化或非结构化知识库中实时检索相关片段，再将这些高相关性上下文注入模型提示（prompt），从而显著提升回答的事实准确性、领域专业性和时效性。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼平台中不是单一接口，而是贯穿多个能力层的**核心增强机制**，按使用方式可分为三类：

- **全托管知识库服务（推荐新手/业务快速上线）**  
  通过控制台「知识库」页面上传文档（PDF/DOCX/TXT/CSV/PNG等），平台自动完成智能切分、向量化（默认 `text-embedding-v3`）、索引构建与混合检索（稠密+稀疏）。绑定至应用或 Agent 后，无需代码即可启用 RAG——平台在每次调用时自动检索 top_k 片段并拼入 system prompt。

- **API 驱动的 RAG 工作流（适合定制化集成）**  
  使用 RAG API（`/api/v1/indices/knowledge/search` 和 `/api/v2/apps/knowledge/chat`）实现端到端控制：  
  - `/knowledge/search`：纯检索接口，支持跨知识库联合语义搜索、多模态输入（文本+图片）、指定重排模型（如 `qwen3-rerank`）；  
  - `/knowledge/chat`：SSE 流式问答接口，在后台自动完成“检索→规划→工具调用→生成”三阶段，返回带引用标记的自然语言答案。

- **框架级深度集成（面向高级开发者）**  
  通过 LlamaIndex 或 Spring AI Alibaba 等框架调用百炼原生组件：  
  - `DashScopeCloudIndex`：一键构建云端知识库，免运维向量数据库；  
  - `DashScopeCloudRetriever`：支持配置 `dense_similarity_top_k` / `sparse_similarity_top_k`、启用 `gte-rerank-hybrid` 重排；  
  - `DashScopeParse`：对 PDF/DOCX 进行版面感知解析，提升切分质量，为 RAG 提供更精准的原始语义单元。

> ✅ 所有场景均默认启用并行多知识库检索，并在结果合并后统一排序，无需手动协调。

## 关键参数和配置

RAG 行为由以下关键参数控制（按作用域分层）：

| 作用域 | 参数名 | 类型 | 说明 | 常用值 | 默认值 |
|---------|--------|------|------|--------|--------|
| **全局检索策略** | `top_k` | integer | 检索返回的最高相关性片段数 | `3`, `5`, `10` | `3`（Agent context）；`5`（CloudRetriever） |
| | `rerank_top_n` | integer | 重排后最终送入 LLM 的片段数 | `3`, `5` | `5`（CloudRetriever） |
| | `rerank_model_name` | string | 重排模型名称 | `"qwen3-rerank"`, `"gte-rerank-hybrid"` | `"qwen3-rerank"`（RAG API）；`"gte-rerank-hybrid"`（CloudRetriever） |
| | `rerank_min_score` | float | 重排得分阈值，低于此值的片段被过滤 | `0.3`, `0.5` | `0.0`（不启用过滤） |
| **知识库类型** | `knowledgeType` | string | 知识库语义类型 | `"document"`, `"table"`, `"image"`, `"multimedia"` | `"document"` |
| | `structureType` | string | 数据结构类型 | `"unstructured"`, `"structured"` | `"unstructured"` |
| **嵌入与解析** | `embeddingModelName` | string | 文本嵌入模型 | `"text-embedding-v4"`, `"qwen3.7-text-embedding"` | `"text-embedding-v3"`（RAG API）；`"text-embedding-v2"`（Embedding SDK） |
| | `multimodalEmbeddingModelName` | string | 多模态嵌入模型（图片/音视频） | `"qwen3-vl-embedding"` | — |
| | `max_pages`（ParseX） | integer | 解析文档最大页数 | `10`, `20` | `10`（Agent context） |

⚠️ 注意：  
- `top_k` 最大支持 `10`，超过将被截断；  
- 时间戳参数需严格区分：RAG API 中 `get_index_monitor` 要求**秒级** Unix 时间戳，其余多数接口为**毫秒级**；  
- 参数命名存在大小写/下划线差异（如 `indexId` vs `index_id`），务必以各接口文档示例为准。

## 面向开发者，简洁实用

- **快速验证**：在控制台创建知识库 → 上传一份产品手册 → 绑定到一个 `qwen-plus` 应用 → 直接在测试窗提问，无需写一行代码。  
- **调试技巧**：开启 `stream=true` + `incremental_output=true`，观察[流式输出](streaming.md)中是否包含 `[引用:xxx]` 标记，确认 RAG 已生效；若无引用，检查知识库状态（是否发布）、文件格式（`.pdf` 必须小写）及文档页数（≤1000页）。  
- **性能优化**：高频问答场景下，优先启用 `enable_reranking=true` 并设 `rerank_top_n=3`，平衡效果与延迟；对长文档，建议配合 `DashScopeParse` 解析后再建索引，比原始切分准确率提升 30%+。  
- **避坑提醒**：  
  - 不要手动拼接检索结果到 prompt——Agent context 和 RAG API 均自动完成注入；  
  - 自定义插件调用时，RAG 检索结果**不会**自动传入插件参数，需显式在 `tools` schema 中声明依赖字段；  
  - 单次请求总上下文（RAG 片段 + Memory + ParseX 输出）不得超过模型上下文窗口的 80%，否则静默截断。

## 关联主题页

- [rag api](../api/rag-api.md)
- [application use cases](../guides/application-use-cases.md)
- [agent context](../guides/agent-context.md)
- [use cases](../guides/use-cases.md)
- [frameworks](../api/frameworks.md)
- [application support](../guides/application-support.md)


