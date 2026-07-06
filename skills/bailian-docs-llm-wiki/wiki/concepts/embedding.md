# 向量嵌入

向量嵌入（Embedding）是将文本、图像、视频等非结构化数据转换为固定维度的数值向量，使语义相近的内容在向量空间中距离也相近。百炼平台提供多类嵌入模型，支撑语义检索、RAG 召回、跨模态搜索、聚类推荐等下游任务。

## 在百炼平台的使用场景

- **RAG 知识库召回**：知识库创建时选择向量模型，对导入文档切片做嵌入入库；查询时对 Query 做同款嵌入，再与切片向量做相似度匹配，作为 RAG 流程的第一段召回。文档搜索、数据查询、音视频搜索类知识库支持 `text-embedding-v4` 或 `text-embedding-v3`（均为 512 维，维度不可更改）；图片问答类固定使用 `multimodal-embedding-v1`（1024 维）；视觉理解场景自动切换为 `qwen3-vl-embedding`。
- **本地 RAG 应用**：本地知识库方案默认调用百炼 embedding API 生成向量，也可替换为本地部署的 GTE 文本向量模型（如 `iic/nlp_gte_sentence-embedding_chinese-large`）。受 embedding API 限流影响，单文件不建议超过 100 MB。
- **跨模态检索**：多模态向量模型（如 `qwen3-vl-embedding`、`multimodal-embedding-v1`）将文本、图像、视频映射到同一语义空间，支持以文搜图、以图搜视频等。支持「独立向量」（逐项生成）与「融合向量」（多输入合并为 1 个向量）两种模式。
- **框架集成**：LlamaIndex 路线将知识库部署在百炼云端，使用官方向量模型与智能切分，不支持自定义嵌入模型；如需灵活选择嵌入模型，应改用本地知识库方案。

## 模型与关键参数

通用文本向量模型当前推荐 `text-embedding-v4`（Qwen3-Embedding 系列，支持 100+ 语种）。

| 模型 | 向量维度 | 最大行数 | 单行最大 Token | 语种 |
|------|---------|---------|---------------|------|
| text-embedding-v4 | 2048/1536/1024(默认)/768/512/256/128/64 | 10 | 8,192 | 100+ 语种 |
| text-embedding-v3 | 1024(默认)/768/512/256/128/64 | 10 | 8,192 | 50+ 语种 |
| text-embedding-v2 | 1,536 | 25 | 2,048 | 10 语种 |
| text-embedding-v1 | 1,536 | 25 | 2,048 | 6 语种 |

请求参数：

- `model`（必选）：模型名称。
- `input`（必选）：字符串、字符串列表或文件。
- `dimensions`（可选）：指定向量维度，仅 v3/v4 支持。
- `encoding_format`（可选）：当前仅支持 `float`。

调用方式支持 OpenAI 兼容接口（base_url：`https://dashscope.aliyuncs.com/compatible-mode/v1`）和 DashScope SDK。

## 批处理接口

大规模文本向量化可使用异步批处理接口（`text-embedding-async-v1/v2`），单次最多 10 万行文本。需在 HTTP 请求头加 `X-DashScope-Async: enable` 启用异步模式，提交后通过 `task_id` 轮询结果。同时处理中任务不超过 50 个，并发运行上限 3 个，超出部分排队等待。

## 与 Rerank 的关系

向量嵌入负责「召回」，Rerank 模型负责「精排」。在知识库检索流程中，先由向量 + 关键词混合检索召回 TopK 切片，再由 `qwen3-rerank`、`qwen3-vl-rerank` 等排序模型对候选切片二次排序，最终按相似度阈值与最大召回数量返回。两者配合提升 RAG 命中准确率。

## 注意事项

- 知识库向量模型与维度在创建时选定，**维度不可更改**；Meta 抽取、多轮对话改写等索引配置在创建后也无法追加，需重建知识库。
- 嵌入与 Rerank 是两类不同模型，不要混用接口：qwen3-rerank 走 `/compatible-api/v1/reranks`，qwen3-vl-rerank / gte-rerank-v2 走 `/api/v1/services/rerank/text-rerank/text-rerank`。
- `gte-rerank` 系列将于 2026 年 5 月 30 日下线，建议迁移到 `qwen3-rerank`。

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [knowledge base](../guides/knowledge-base.md)
- [knowledge](../api/knowledge.md)
- [frameworks](../api/frameworks.md)
- [application use cases](../guides/application-use-cases.md)


