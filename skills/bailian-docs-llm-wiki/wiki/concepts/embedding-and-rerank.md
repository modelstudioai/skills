# 向量化与重排序

向量化（Embedding）是将文本、图像、视频等非结构化数据映射到统一语义空间的稠密向量表示过程；重排序（Rerank）是在初步检索结果基础上，利用更精细的语义匹配模型对候选文档进行精细化打分与重排，提升相关性精度。二者共同构成 RAG、搜索、推荐等场景中“检索-精排”两阶段的核心能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **RAG 应用构建**：在知识库创建时，通过 `embeddingModelName`（如 `text-embedding-v4` 或 `qwen3-vl-embedding`）指定向量化模型，用于将文档切片编码为向量并存入向量库；检索时，系统自动对用户 query 向量化，并执行近邻搜索（ANN）；随后可启用 `rerankModelName`（如 `qwen3.7-text-rerank`）对 top-K 初筛结果进行重排，显著提升问答准确率。
- **多模态搜索**：使用 `qwen3-vl-embedding` 的 `enable_fusion=true` 模式，将图文/图文音混合输入编码为单一融合向量，实现跨模态统一检索；再通过 `qwen3-vl-rerank` 对混合类型（文本+图片+视频）的候选结果进行联合重排，支持“以文搜图”“以图搜视频”等复杂意图。
- **批量离线处理**：对海量文档（如 10 万行日志、PDF 解析文本），调用异步向量化接口 `text-embedding-async-v2`，指定 `text_type=document` 优化底库表征；后续可通过同步 rerank 接口对高频 query 的固定候选集做低延迟精排。
- **框架集成（LlamaIndex / Spring AI）**：在 `VectorStoreIndex` 或 `EmbeddingClient` 中直接传入百炼 embedding 模型 ID；重排序能力通过 `Reranker` 组件注入（如 LlamaIndex 的 `SentenceWindowNodeParser` + `QwenReranker`），无需手动拼接 API 调用。
- **OpenAI 兼容开发**：使用标准 `client.embeddings.create(model="text-embedding-v4", input=[...])` 调用向量化；重排序暂不支持 OpenAI 原生协议，需切换至 DashScope 原生 `/api/v1/services/rerank/text-rerank` 接口或通过 `model experience` 统一入口（`model_id=qwen3.7-text-rerank`）调用。

## 关键参数和配置

| 参数 | 适用能力 | 说明 | 推荐值 |
|------|----------|------|--------|
| `dimensions` | 文本/多模态向量 | 指定向量维度（64–2048），影响存储开销与检索精度；高维（如 2048）适合长尾语义区分，低维（如 256）适合高吞吐场景 | `1024`（平衡项） |
| `text_type` | 异步文本向量 | 区分 `document`（底库）与 `query`（检索）表征策略，影响 token 截断与归一化逻辑 | 底库用 `document`，查询用 `query` |
| `enable_fusion` | `qwen3-vl-embedding` | `true` 启用多模态融合向量（单向量），`false` 返回各模态独立向量 | 多源信息融合场景设为 `true` |
| `instruct` | Rerank | 控制重排意图，需传入自然语言指令（如 `"Retrieve passages answering the question..."`），直接影响模型注意力聚焦 | 必填，建议使用官方示例模板 |
| `top_n` | Rerank | 限制返回结果数，避免下游处理过载；若需全部重排结果，可省略此参数 | `10`–`50`（典型 RAG 场景） |
| `fps` | `qwen3-vl-rerank`（视频） | 视频抽帧密度（frames per second），影响计算开销与时序信息完整性 | `1`（默认），高精度需求可设 `2` |

> ⚠️ 注意：`gte-rerank` 系列模型将于 2026-05-30 下线，请立即迁移至 `qwen3.7-text-rerank` 或 `qwen3-rerank`；多模态向量不兼容 OpenAI Embedding 协议，须使用 DashScope 原生或多模态专用接口。

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [rag api](../api/rag-api.md)
- [model experience](../guides/model-experience.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [frameworks](../api/frameworks.md)


