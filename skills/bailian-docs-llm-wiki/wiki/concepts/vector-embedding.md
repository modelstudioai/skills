# 向量嵌入

向量嵌入（Vector Embedding）是将原始文本、图像、音视频等非结构化数据映射到高维实数向量空间的数学表示过程，其核心目标是让语义相似的内容在向量空间中距离更近（如余弦相似度更高），从而支撑语义搜索、RAG、聚类、跨模态检索等AI任务。

## 在百炼平台的不同场景中如何使用

- **RAG 知识库构建**：知识库创建时，文档内容（PDF/Word/图片等）经解析与切片后，由指定嵌入模型（如 `text-embedding-v4` 或 `qwen3-vl-embedding`）统一向量化，生成可检索的语义索引。该向量索引是后续“检索-重排-生成”链路的基础。
- **实时语义搜索**：用户查询（Query）需与底库向量在同一语义空间中对齐——通常调用同步向量模型（如 `qwen3.7-text-embedding`）实时生成 Query 向量，再通过向量数据库（如 Milvus、Pinecone 或百炼内置索引）进行近似最近邻（ANN）检索。
- **[多模态](multi-modal.md)联合检索**：在 `multimedia` 或 `image` 类型知识库中，使用[多模态](multi-modal.md)嵌入模型（如 `qwen3-vl-embedding`）为文本、图像、视频生成统一表征；支持图文混合输入（如“红色跑车照片”配文字描述）并召回语义匹配的[多模态](multi-modal.md)结果。
- **批量预处理**：对海量文档（如千万级商品描述、企业文档库）进行离线向量化时，优先选用异步批处理接口（如 `text-embedding-async-v2`），提升吞吐效率并降低延迟敏感型服务压力。
- **框架集成开发**：LlamaIndex 和 Spring AI Alibaba 等框架通过 `EmbeddingClient` 封装百炼向量 API，开发者只需配置模型名（如 `"text-embedding-v3"`）和认证信息，即可在标准 pipeline 中直接调用，无需手动处理 HTTP 请求与重试逻辑。

## 关键参数和配置

| 参数 | 适用模型 | 说明 | 推荐值/注意事项 |
|------|----------|------|----------------|
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v4/v3`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06` | 指定向量维度，影响存储开销、检索速度与表达能力。高维（如 2560）适合精度优先场景；低维（如 512）适合资源受限或快速原型验证。 | `qwen3.7-text-embedding` 支持 256/512/768/1024/1536/2048/2560；默认为全维（2560）。不支持该参数的模型（如 `text-embedding-v2`）将固定输出预设维度。 |
| `text_type` | 异步文本向量模型（`text-embedding-async-v2/v1`） | 明确输入用途：`document`（底库文本，优化[长期记忆](long-term-memory.md)表征）或 `query`（用户实时查询，优化检索判别力）。二者向量不可混用计算相似度。 | 必须显式指定；若用于 RAG 底库构建，设为 `"document"`；Query 向量化必须设为 `"query"`。 |
| `enable_fusion` | `qwen3-vl-embedding` | 控制多模态输入的向量生成方式：`true` → 单一融合向量（适用于图文联合理解）；`false`（默认）→ 各模态独立向量（适用于分别索引或对比学习）。 | 多模态检索场景建议启用融合；若需对图像和文本单独做相似度分析，则保持默认。 |
| `input_type`（隐式） | 所有向量模型 | 虽无显式参数，但模型严格区分输入类型：文本模型仅接受 `str` 或 `list[str]`；多模态模型需按规范传入 `{"text": "...", "image_url": "..."}` 等结构化对象。 | 错误类型输入将返回 `400 Bad Request`；请严格参照各模型的 [API 参考文档](../../raw/model-api-reference/vector-and-sort/) 格式。 |

> ⚠️ 注意：`gte-rerank` 系列模型已下线，但其配套的旧版向量模型（如 `gte-embedding`）**未被支持**；百炼当前所有向量能力均由 Qwen 系列及 Tongyi 自研模型提供，不兼容第三方 embedding 模型。

## 面向开发者：简洁实用提示

- ✅ **选型建议**：
  - 实时 Query 向量化 → `qwen3.7-text-embedding`（低延迟、高维可配）
  - 海量文档预处理 → `text-embedding-async-v2`（吞吐优先，支持百万级/小时）
  - 图文混合知识库 → `qwen3-vl-embedding`（支持 `enable_fusion=true`）
- ✅ **调用方式**：
  - HTTP 直接调用：使用 `POST /api/v1/services/embeddings/text`（同步）或 `/api/v1/services/embeddings/text/batch`（异步），带 `Authorization: Bearer <API-Key>`。
  - OpenAI 兼容模式：复用 `openai.Embedding.create()`，`base_url` 设为 `https://{WorkspaceId}.<region>.maas.aliyuncs.com/compatible-mode/v1`。
  - SDK 推荐：Python 使用 `dashscope` SDK 的 `Embedding` 类，Java 使用 `DashScopeClient.embedding()`，自动处理鉴权、重试与错误解析。
- ✅ **避坑指南**：
  - 同一知识库中，`document` 和 `query` 向量**必须使用同一模型版本与相同 `dimensions`**，否则相似度计算失效。
  - 多模态嵌入时，`image_url` 必须为公网可访问地址或 Base64 编码字符串；OSS 内网地址需确保百炼服务可直连。
  - 向量维度变更后，原有索引需**全部重建**——百炼不支持向量降维/升维转换。
  - 控制台创建的知识库默认使用 `text-embedding-v4`，且**创建后不可修改嵌入模型**；如需更换，请新建知识库。

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [rag api](../api/rag-api.md)
- [frameworks](../api/frameworks.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [knowledge base](../guides/knowledge-base.md)


