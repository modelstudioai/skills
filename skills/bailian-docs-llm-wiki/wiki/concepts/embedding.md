# 向量嵌入

向量嵌入（Vector Embedding）是将原始非结构化数据（如文本、图像、视频等）映射到高维连续语义空间中的稠密向量表示，使语义相近的内容在向量空间中距离更近。它是百炼平台实现语义检索、RAG、跨模态搜索等AI能力的底层基础表征技术。

## 在百炼平台的不同场景中，这个概念如何使用

- **RAG 知识库构建**：知识库在文档切片后，调用指定嵌入模型（如 `text-embedding-v4` 或 `qwen3-vl-embedding`）为每个切片生成向量，并存入向量索引。后续检索时，用户查询被同样向量化，通过向量相似度（如余弦相似度）召回最相关的切片。
- **多模态搜索**：支持文本、图像、视频及其组合的统一表征。例如：
  - *独立向量*：对单张图片和一段描述分别生成向量，用于“以图搜图”或“以文搜图”的逐项比对；
  - *融合向量*：将图文混合输入（如商品标题+主图+细节图）编码为单一向量，用于整体语义匹配。
- **通用语义服务 API**：通过 `/embeddings`（文本）或 `/multimodal-embedding`（多模态）接口，开发者可直接调用向量嵌入能力，用于自建检索系统、聚类分析、去重、特征工程等下游任务。
- **Agent 与检索服务协同**：RAG Agent 在执行检索时，底层自动调用配置的嵌入模型完成查询向量化；检索服务（如 `/knowledge/search`）则依赖该向量与知识库索引进行匹配。

> ⚠️ 注意：嵌入模型在知识库创建时选定且不可更改；不同模型的向量空间不兼容，更换模型需重建整个知识库索引。

## 关键参数和配置

| 参数 | 适用模型/场景 | 说明 | 建议 |
|------|----------------|------|------|
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06` 等 | 指定向量维度（如 1024、2048）。维度越高通常表征能力越强，但索引体积与检索延迟也增加。未指定时取模型默认值。 | 生产环境建议显式指定，便于版本控制与空间预估；RAG 知识库默认使用模型原生维度，无需手动设置。 |
| `enable_fusion` | `qwen3-vl-embedding`（仅该模型） | `true`：将 `contents` 中所有模态输入融合为 1 个向量；`false`（默认）：为每个输入生成独立向量。 | 多模态联合理解场景（如图文商品）设为 `true`；需逐项比对（如图库检索）保持 `false`。 |
| `text_type` | 批处理接口（`text-embedding-async-v2/v1`） | 取值 `"query"` 或 `"document"`，用于非对称检索任务（如问答场景），帮助模型优化 query/document 向量分布对齐。 | RAG 场景中，查询文本传 `"query"`，知识库切片传 `"document"`，可提升召回质量。 |
| `encoding_format` | 同步文本向量接口 | `"float"`（默认，返回浮点数组）或 `"base64"`（压缩传输，节省带宽）。注意：新网关下短请求生效，长请求仍强制 `float`。 | 高频小请求可用 `base64` 降低网络开销；调试或本地开发推荐 `float` 便于查看。 |

## 面向开发者，简洁实用

- ✅ **选型建议**：
  - 中英文通用文本 → 优先 `text-embedding-v4`（平衡效果与成本）；
  - 多模态图文 → `qwen3-vl-embedding`（支持融合/独立，精度高）；
  - 超大规模离线批处理（>10万条）→ 使用异步批处理接口 + `text-embedding-async-v2`；
  - 图像为主、弱文本 → `tongyi-embedding-vision-plus-2026-03-06`（视觉增强型）。

- ✅ **集成提示**：
  - 向量本身不包含业务语义，务必与原始内容（如 `chunk_id`, `file_name`, `meta` 字段）建立可靠映射并持久化；
  - RAG 场景中，确保查询与知识库使用**同一嵌入模型与参数**，否则向量空间错位导致召回失效；
  - 多模态融合向量不可直接与文本向量做相似度计算——必须使用同类型模型生成的向量进行比对。

- ✅ **避坑指南**：
  - 不要混用 `gte-rerank` 系列（已下线）与新版嵌入模型搭配；
  - `dimensions` 参数对旧版模型（如 `text-embedding-v1/v2`）无效，调用前请查阅对应模型文档；
  - 控制台创建的知识库默认启用 `text-embedding-v4`，API 创建时需显式指定 `embeddingModelName` 字段。

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [rag api](../api/rag-api.md)
- [knowledge base](../guides/knowledge-base.md)
- [more models](../api/more-models.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)


