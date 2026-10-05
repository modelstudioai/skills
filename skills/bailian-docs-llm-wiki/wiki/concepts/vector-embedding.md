# 向量嵌入与重排序

向量嵌入（Embedding）是将文本、图像等非结构化数据映射为稠密数值向量的过程，用于表征语义；重排序（Rerank）则是在初步检索结果基础上，利用细粒度相关性模型对候选文档进行精排打分，提升最终召回质量。二者共同构成百炼平台 RAG 流程中“检索-精排”双阶段的核心能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **知识库服务**：知识库创建时需指定嵌入模型（如 `text-embedding-v4`），用于将文档切片向量化并构建索引；检索时可启用重排序模型（如 `qwen3-rerank` 或 `qwen3-vl-rerank`），对初筛的 TopK 切片进行二次打分与重排，显著提升相关性排序准确率。
- **RAG API 调用**：通过 `/api/v1/indices/rag/index/create_v2` 创建知识库时，可配置 `embeddingModelName` 和 `rerankModelName`；在运行时检索接口中，通过 `kb_search_configs.rerank_top_n` 控制重排数量，并用 `rerank_min_score` 过滤低置信结果。
- **独立向量与排序服务**：直接调用 `/v1/embeddings`（生成文本/多模态向量）和 `/v1/rerank`（对 query-document 对打分），适用于自定义检索链路、混合搜索（BM25 + 向量）、或非知识库场景下的语义匹配任务。
- **框架集成（LlamaIndex / Spring AI）**：在 LlamaIndex 中通过 `DashScopeEmbedding(model="text-embedding-v3")` 替换默认嵌入器；Spring AI Alibaba 通过 `spring.ai.alibaba.embedding.model=text-embedding-v4` 配置，自动完成向量化；重排序需在 QueryEngine 层手动集成 `/v1/rerank` 调用或启用知识库内置混排能力。

## 关键参数和配置

| 参数 | 所属能力 | 说明 | 示例值 |
|------|----------|------|--------|
| `model` | 全部 | 必填，显式指定模型 ID，无默认路由 | `"text-embedding-v2"`, `"rerank-v2"`, `"qwen3-rerank"` |
| `input` | Embedding | 文本向量：字符串或字符串数组；多模态：`{ "image_url": "...", "text": "..." }` | `["杭州天气", "北京降雨"]` 或 `{ "image_url": "https://...", "text": "产品包装图" }` |
| `query` / `documents` | Rerank | 必填对象字段，`documents` 为字符串数组，最大长度 100 | `{ "query": "量子计算原理", "documents": ["量子比特...", "Python 是..."] }` |
| `top_k` | Rerank（API） | 返回前 K 个重排结果（`rerank-v1` ≤50，`rerank-v2` ≤100） | `20` |
| `encoding_format` | Embedding | 输出向量编码格式，默认 `"float"`，可选 `"base64"` | `"base64"` |
| `rerankModelName` | 知识库创建（RAG API） | 创建知识库时指定重排模型，影响后续所有检索请求 | `"qwen3-vl-rerank"` |
| `rerank_top_n` | 检索请求（RAG API） | 单次请求中参与重排的文档数上限 | `50` |

> ⚠️ 注意：  
> - 所有向量模型单次 `input` 数组长度上限为 2048；  
> - 多模态嵌入仅支持公网可访问的 `https://` 图像 URL，不支持本地文件上传；  
> - `text-embedding-v1` 已进入维护期，新项目请优先选用 `text-embedding-v2` 或 `text-embedding-v4`；  
> - 知识库创建后，嵌入模型不可更改，重排模型可在更新知识库配置时调整。

## 面向开发者，简洁实用

- ✅ **快速验证**：用 Playground 的“知识检索”模式开启“启用重排序”，直观对比开启前后的排序变化；  
- ✅ **最小集成**：只需两个 HTTP 请求——先 `/v1/embeddings` 获取 query 向量做初步召回，再 `/v1/rerank` 对 top-50 结果精排；  
- ✅ **生产推荐**：知识库场景下，直接配置 `qwen3-rerank` 并设 `rerank_top_n=30`，配合 `相似度阈值=0.35`，平衡精度与性能；  
- ✅ **避坑提示**：调用 `/v1/rerank` 时务必传 `model`，且 `documents` 必须是字符串数组（非对象数组）；知识库 API 中注意 `index_id`（snake_case）与 `indexId`（camelCase）字段名差异。

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [knowledge base](../guides/knowledge-base.md)
- [rag api](../api/rag-api.md)
- [frameworks](../api/frameworks.md)


