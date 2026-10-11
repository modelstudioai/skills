# 向量化与重排序

向量化（Embedding）是将文本、图像、视频等非结构化数据映射到高维语义向量空间的过程，使语义相似的内容在向量空间中距离更近；重排序（Rerank）则是在初步检索结果基础上，利用更精细的交叉注意力模型对候选文档进行相关性精排，显著提升 Top-K 结果的准确率。二者共同构成语义检索的核心双阶段范式：先粗筛（向量化 + 向量检索），再精排（重排序）。

## 在百炼平台的不同场景中，这个概念如何使用

- **RAG 应用链路**：知识库构建时默认调用指定嵌入模型（如 `text-embedding-v4`）对切片进行向量化；知识检索（`/v1/knowledge/query`）默认启用混合检索（关键词 + 向量），并可选开启重排序（如 `qwen3-rerank`）对召回的 Top-K 切片进行二次打分与重排，最终返回高置信度结果。
- **原生向量/排序服务**：通过 `/compatible-mode/v1/embeddings`（同步向量）、`/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`（多模态向量）或 `/compatible-api/v1/reranks`（`qwen3-rerank`）等接口，开发者可直接调用向量化与重排序能力，用于自建检索系统、聚类分析、跨模态搜索等场景。
- **框架集成（LlamaIndex / Spring AI）**：`DashScopeEmbedding` 和 `DashScopeRerank` 组件封装了底层 API 调用逻辑，支持在 `VectorStoreIndex` 或 `Retriever` 中无缝插入向量化与重排序步骤；`DashScopeCloudRetriever` 更内置混合检索 + 重排组合策略（如 `gte-rerank-hybrid`）。
- **多模态检索**：`qwen3-vl-embedding` 支持文本、图像、视频统一编码为向量；`qwen3-vl-rerank` 可对图文混合查询与文档进行端到端重排，适用于图片问答、视频片段检索等场景。
- **Agent 与工作流编排**：RAG Agent 在执行检索步骤时，自动调用知识库配置的嵌入与重排模型；开发者也可在自定义工作流中显式插入向量化节点（如对用户 query 实时编码）或重排序节点（如对多个来源召回结果统一精排）。

## 关键参数和配置

| 参数 | 适用模型/场景 | 说明 | 注意事项 |
|------|----------------|------|-----------|
| `model` | 所有向量/重排接口 | 必填，严格匹配模型标识符（如 `qwen3.7-text-embedding`、`qwen3-rerank`） | `qwen3-rerank` 使用独立接口 `/compatible-api/v1/reranks`，其余 rerank 模型走 `/api/v1/services/rerank/text-rerank/text-rerank` |
| `dimensions` | `qwen3.7-text-embedding`、`text-embedding-v3/v4`、`qwen3-vl-embedding` | 可选，指定输出向量维度（如 `256`、`1024`） | 旧模型（如 `multimodal-embedding-v1`）不支持，强制返回固定维度 |
| `enable_fusion` | 仅 `qwen3-vl-embedding` | 设为 `true` 时融合全部输入为单向量；其他多模态模型通过 `{"contents": [...]}` 结构隐式融合 | `tongyi-embedding-vision-plus-2026-03-06` 等模型**不支持该参数** |
| `instruct` | `qwen3.7-text-rerank`、`qwen3-rerank`、`qwen3-vl-rerank` | 可选，提供任务指令（如 `"Retrieve passages that answer the query."`）以引导排序逻辑 | 对纯相似度任务（如语义去重）可设为 `"Retrieve semantically similar text."` |
| `top_k`（检索侧） | RAG API、知识库检索、`DashScopeCloudRetriever` | 控制初始召回数量（如 `top_k=100`）或最终返回数量（如 `top_k=5`） | 知识库最大召回数为 20，RAG API `top_k` 上限为 50 |
| `similarity_threshold` | 知识库配置、检索请求 | 过滤重排后低分结果（范围 0.01–1.0） | 值过高可能导致漏召，建议从 `0.3` 起调优 |
| `enable_reranking` | `DashScopeCloudRetriever`、RAG 服务配置 | 布尔值，启用后自动调用配置的 rerank 模型 | 默认开启，关闭后仅返回向量/关键词初检结果 |

> ⚠️ **重要兼容性提示**：  
> - `gte-rerank` 已于 2026 年 05 月 30 日下线，请迁移至 `qwen3-rerank` 或 `qwen3.7-text-rerank`；  
> - 多模态向量必须使用原生 HTTP 接口，**不支持 OpenAI 兼容模式**；  
> - `qwen3-rerank` 的 `query` + `documents` 输入需扁平化（非嵌套 `input` 对象），与其他 rerank 模型参数结构不同。

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [rag api](../api/rag-api.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [more models](../api/more-models.md)


