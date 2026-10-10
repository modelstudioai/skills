# 向量嵌入与重排序

向量嵌入（Embedding）是将文本、图像、视频等非结构化数据映射到统一高维语义空间的稠密向量表示；重排序（Rerank）则是在初步检索结果基础上，利用更精细的语义匹配模型对候选条目进行相关性重打分与重新排序。二者协同构成百炼平台语义检索的核心双阶段范式：先通过嵌入实现高效召回，再通过重排序提升精度。

## 在百炼平台的不同场景中，这个概念如何使用

- **RAG 应用（知识库问答）**：知识入库时，文档被自动切片并调用默认或指定的嵌入模型（如 `text-embedding-v3`）生成向量索引；检索时，用户查询被向量化后在索引中进行近邻搜索（ANN），若启用 `enable_rerank=true`，则进一步调用重排序模型（如 `qwen3.7-text-rerank`）对 Top-K 候选切片做精细化重排，显著提升最终答案质量。
- **自定义 RAG 流程（API/SDK 集成）**：开发者可独立调用 `/embeddings` 接口完成向量化（支持同步/异步/多模态），再结合自有向量数据库（如 Milvus、Qdrant）构建检索链路；同时通过 `/rerank` 接口对召回结果进行重排序，灵活控制召回与精排解耦。
- **多模态检索**：使用 `qwen3-vl-embedding` 等模型，可为图文混合内容生成统一语义向量（启用 `enable_fusion=true`）或独立模态向量，支撑跨模态相似性检索；配合 `qwen3-vl-rerank`，支持图文/视频混合查询下的细粒度相关性判断。
- **框架集成（LlamaIndex / Spring AI）**：通过 `DashScopeEmbedding` 和 `DashScopeRerank` 组件，一键接入百炼嵌入与重排序能力；例如 `DashScopeCloudRetriever` 默认启用 `enable_reranking=True`，自动融合向量召回与重排序两阶段逻辑。
- **低延迟在线服务 vs 高吞吐离线任务**：同步接口（如 `qwen3.7-text-embedding`）适用于实时问答、交互式搜索等低延迟场景（≤20 条输入）；异步批处理（如 `text-embedding-async-v2`）则面向千万级文档的离线建库任务，支持单次 10 万行，且区分 `document`/`query` 类型以优化非对称检索效果。

## 关键参数和配置

| 参数 | 适用模型/场景 | 说明 | 推荐值/注意事项 |
|------|----------------|------|------------------|
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding` 等 | 指定向量维度（如 `1024`, `2048`），影响存储与计算开销；固定维度模型（如 `text-embedding-v2`）不支持此参数。 | 优先使用模型默认维度；调整前需确认下游向量库兼容性。 |
| `encoding_format` | 同步文本向量接口 | 返回格式：`float`（默认，直接可用）或 `base64`（节省带宽，需客户端解码）。 | 生产环境建议 `float`；长文本请求下新网关仍回落至 `float`，无需强依赖 `base64`。 |
| `enable_fusion` | `qwen3-vl-embedding` | 布尔值，启用后将 `contents` 中多模态输入融合为单个向量；`qwen2.5-vl-embedding` 等仅支持融合，无此参数。 | 多模态联合检索必开；单模态任务可关闭以保留模态特异性。 |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义任务指令（英文），引导模型理解检索目标（如 `"Given a technical support query..."`）。 | 强烈建议显式设置，尤其在问答检索、法律/医疗等专业场景；避免中文指令。 |
| `text_type` | 异步文本向量（`text-embedding-async-v2`） | 标识输入类型：`document`（知识库文本）或 `query`（用户问题），用于优化非对称嵌入空间。 | 必须准确区分；混用会导致检索精度下降。 |
| `enable_rerank` | RAG API（`/v1/knowledge/query`）、知识库 SDK | 布尔值，全局开关重排序流程。启用后自动调用默认重排序模型（如 `qwen3-rerank`）。 | 开发调试阶段建议设为 `true`；高并发低延迟场景可设为 `false` 并自行调度 rerank。 |

> ⚠️ 注意：`gte-rerank` 模型将于 2026 年 5 月 30 日下线，请尽快迁移到 `qwen3-rerank`（轻量高效）或 `qwen3.7-text-rerank`（高精度、长上下文）。  
> 💡 提示：重排序虽提升精度，但引入额外延迟（通常 +200~500ms），建议在 `top_k=5~10` 范围内启用，避免对大量候选做重排。

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [rag api](../api/rag-api.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [more models](../api/more-models.md)


