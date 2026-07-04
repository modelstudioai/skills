# 向量与嵌入

向量与嵌入（Embedding）是指将文本、图像、视频等非结构化内容映射为固定维度的数值向量，使语义相近的内容在向量空间中距离也更近，从而支持语义检索、聚类、推荐与 RAG 召回等下游任务。在百炼平台中，向量化是知识库检索与跨模态搜索的基础环节，与 Rerank 排序模型共同构成检索链路。

## 在百炼平台的使用场景

- **知识库检索召回**：文档搜索、数据查询、音视频搜索类知识库在创建时会对接向量模型，将入库切片向量化并写入索引；查询时对用户问题做同样的向量化，再执行向量 + 关键词混合检索。文档搜索、数据查询、音视频搜索类知识库支持 `text-embedding-v4` 或 `text-embedding-v3`（均为 512 维，维度不可更改）；视觉理解场景自动切换为 `qwen3-vl-embedding`；图片问答类仅支持 `multimodal-embedding-v1`（1024 维）。
- **RAG 应用构建**：无论是云端知识库还是本地 RAG 方案，嵌入模型都决定了召回上限。云端方案使用百炼官方嵌入模型，不支持自定义切分与嵌入；本地 RAG 可改用自部署的 GTE 文本向量模型（如 `iic/nlp_gte_sentence-embedding_chinese-large`），以灵活控制切分与嵌入。
- **跨模态检索**：多模态向量模型将文本、图像、视频映射到同一语义空间，支持以文搜图、以图搜视频等。`qwen3-vl-embedding` 默认维度 2560，支持「独立向量」（每个输入各生成一向量，用于逐项对比）与「融合向量」（所有输入融合为 1 个向量，用于综合理解）两种类型。
- **框架集成**：通过 LlamaIndex 构建 RAG 应用时，云端知识库默认使用百炼官方向量模型，配合 `similarity_top_k`、`similarity_cutoff`、`top_n` 等参数控制召回与重排。

## 文本向量模型

通用文本向量模型将文本转换为数值向量，当前推荐 `text-embedding-v4`（属 Qwen3-Embedding 系列），支持 100+ 主流语种。

| 模型 | 向量维度 | 最大行数 | 单行最大 Token | 语种 |
|------|---------|---------|---------------|------|
| text-embedding-v4 | 2048/1536/1024(默认)/768/512/256/128/64 | 10 | 8,192 | 100+ 语种 |
| text-embedding-v3 | 1024(默认)/768/512/256/128/64 | 10 | 8,192 | 50+ 语种 |
| text-embedding-v2 | 1,536 | 25 | 2,048 | 10 语种 |
| text-embedding-v1 | 1,536 | 25 | 2,048 | 6 语种 |

**关键参数：**

- `model`（必选）：模型名称
- `input`（必选）：字符串、字符串列表或文件
- `dimensions`（可选）：指定向量维度，仅 v3/v4 支持
- `encoding_format`（可选）：当前仅支持 `float`

**调用方式**：支持 OpenAI 兼容接口（`base_url: https://dashscope.aliyuncs.com/compatible-mode/v1`）和 DashScope SDK。对于大规模文本向量化，可使用异步批处理接口（`text-embedding-async-v1/v2`），单次最多 10 万行，通过 `X-DashScope-Async: enable` 请求头启用异步模式，提交后用 `task_id` 轮询结果；同时处理中任务不超过 50 个，并发上限 3。

## 多模态向量模型

多模态向量模型将文本、图像、视频统一映射到同一语义空间，支持跨模态检索。向量类型分「独立向量」（每个输入分别生成向量，适用于逐项对比）与「融合向量」（将所有输入融合为 1 个向量，适用于综合理解多模态内容）。`qwen3-vl-embedding` 默认维度 2560，支持独立与融合两种模式；`multimodal-embedding-v1` 默认 1024 维，用于图片问答类知识库。

## 知识库中的嵌入配置要点

- 文档搜索、数据查询、音视频搜索类知识库统一使用 512 维 `text-embedding-v4` / `text-embedding-v3`，维度不可更改。
- 视觉理解场景自动切换为 `qwen3-vl-embedding`，无需手动指定。
- 嵌入模型与切片策略共同决定召回质量：推荐使用智能切分（基于语义自适应选择切片点，单切片 Token 上限 6,000），切片过大或过小都会影响向量匹配效果。
- 本地 RAG 场景若需自定义嵌入模型，可改用自部署 GTE 文本向量模型，但需注意 embedding API 限流，不建议传入超过 100 MB 的文件。

## 与 Rerank 的协作

向量检索负责语义召回（初步 TopK 默认 50，可设 1–100），Rerank 模型负责二次精准排序。知识库中可选 `qwen3-rerank` / `qwen3-rerank(hybrid)` / `qwen3-vl-rerank`（多模态库只能选 vl-rerank），排序后再按相似度阈值（0.01–1.0）与最大召回数量（1–20）裁剪。向量召回质量直接影响 Rerank 上限，调优时通常先确认嵌入模型与切片合理，再调整 Rerank 阈值与 K 值。

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [knowledge base](../guides/knowledge-base.md)
- [knowledge](../api/knowledge.md)
- [frameworks](../api/frameworks.md)
- [application use cases](../guides/application-use-cases.md)


