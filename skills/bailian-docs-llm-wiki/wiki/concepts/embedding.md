# 向量化

向量化（Vectorization）是将非结构化或半结构化数据（如文本、图像、音视频等）映射为高维稠密实数向量（embedding）的过程，其核心目标是使语义相近的内容在向量空间中距离更近。该向量表示可被用于语义检索、聚类、相似度计算、RAG 召回等下游任务，是百炼平台实现“理解内容”而非“匹配关键词”的基础能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **知识库（Knowledge Base）**：文档上传后，系统默认调用 `text-embedding-v4` 对每个切片进行向量化，构建向量索引；多模态知识库支持 `qwen3-vl-rerank` 等模型生成跨模态统一向量，支撑图文混合检索。向量化发生在文档解析与切片之后、索引构建之前，创建后不可更换嵌入模型。

- **独立向量服务（Vector & Sort API）**：提供细粒度控制能力，支持三类向量化：
  - *通用文本向量*：适用于搜索、分类等场景，模型如 `qwen3.7-text-embedding`、`text-embedding-v3`；
  - *批处理向量*：面向离线建库，单次支持 10 万行文本，需指定 `text_type=query` 或 `document` 以优化非对称检索效果；
  - *多模态向量*：支持文本+图像/视频组合输入，通过 `enable_fusion=true` 控制是否生成融合向量（1 个），或返回各模态独立向量（N 个）。

- **框架集成（LlamaIndex / Spring AI）**：通过 `DashScopeEmbedding` 组件直接调用百炼向量模型，`model_name` 参数指定嵌入模型（如 `"text-embedding-v3"`），自动适配 [OpenAI 兼容接口](openai-compatible-api.md)，无需手动构造 HTTP 请求。

- **RAG API**：向量化作为隐式底层能力，不暴露给开发者；但 `top_k`、`similarity_threshold` 等检索参数直接影响向量召回质量，`enable_rerank=true` 可在向量初检结果上叠加重排模型进一步提升精度。

- **模型数据（Model Data）**：当前不涉及向量化——该模块聚焦训练/评测数据集的结构化管理（CSV/JSONL），不参与 embedding 计算或向量索引构建。

> ⚠️ 注意：向量化是**单向、无状态、不可逆**的操作；向量本身不携带原始内容，也不支持反向解码。所有向量计算均按实际 [Token](token.md) 消耗计费，且受地域限制（仅华北2、新加坡可用）。

## 关键参数和配置

| 参数 | 所属场景 | 是否必填 | 说明 | 示例值 |
|------|----------|-----------|------|--------|
| `model` | 知识库创建、Vector API、框架集成 | 是 | 指定嵌入模型 ID；知识库创建后不可修改 | `"text-embedding-v4"`, `"qwen3-vl-embedding"` |
| `dimensions` | Vector API（同步） | 否 | 指定向量维度（部分模型固定维度，不支持此参数） | `1024`, `2048` |
| `encoding_format` | Vector API（同步） | 否 | 输出格式：`float`（默认）或 `base64`（节省带宽） | `"base64"` |
| `text_type` | Vector API（批处理） | 是（批处理场景） | 区分查询文本（`query`）与底库文本（`document`），影响归一化与相似度计算逻辑 | `"query"`, `"document"` |
| `enable_fusion` | `qwen3-vl-embedding` 多模态向量 | 否 | `true` 返回 1 个融合向量；`false` 或省略返回 N 个独立向量 | `true` |
| `instruct` | Rerank 模型（非向量化，但常与向量检索联动） | 否 | 自定义排序指令，影响相关性判断（仅限 `qwen3-rerank` 系列） | `"Find the most technically accurate answer."` |

> ✅ 最佳实践：  
> - 小规模实时调用 → 用同步接口 + `text-embedding-v4`；  
> - 百万级文档建库 → 用异步批处理 + `text-embedding-async-v2` + `text_type=document`；  
> - 多模态混合检索 → 用 `qwen3-vl-embedding` + `enable_fusion=true`；  
> - 知识库场景 → 无需手动调用向量 API，专注切片策略与检索参数调优即可。

## 面向开发者，简洁实用

- 向量化不是“功能开关”，而是**数据进入语义检索链路的必经转换步骤**；你不需要自己实现，但需要选对模型、配对参数、理解其行为边界。
- 所有向量接口均兼容 OpenAI 格式（`/v1/embeddings`），可无缝替换现有 LlamaIndex/Spring AI 配置。
- 向量结果为 `list[float]`，可直接存入 Milvus/Pinecone/FAISS 等向量数据库，也可直接传给百炼重排或 RAG 服务。
- 调试建议：先用 Playground 或 `bailian-cli` 快速验证向量一致性（相同文本多次请求应得近似向量），再集成到业务流。
- 计费提示：向量化按输入 [Token](token.md) 计费，图片/视频按分辨率折算为等效 [Token](token.md)；避免重复向量化同一文档——知识库会自动缓存切片向量。

## 关联主题页

- [knowledge base](../guides/knowledge-base.md)
- [vector and sort](../api/vector-and-sort.md)
- [frameworks](../api/frameworks.md)
- [rag api](../api/rag-api.md)
- [model data overview](../guides/model-data-overview.md)


