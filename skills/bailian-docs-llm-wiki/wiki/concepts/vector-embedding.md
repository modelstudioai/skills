# 向量嵌入

向量嵌入（Embedding）是将原始非结构化数据（如文本、图像等）映射到低维稠密实数向量空间的数学表示方法，其核心目标是使语义相近的输入在向量空间中距离更近。该表示可直接用于相似度检索、聚类、分类及作为 RAG 系统中语义召回的基础特征。

## 在百炼平台的不同场景中，这个概念如何使用

- **RAG 知识库构建与检索**：知识库创建时，文档内容（文本或图文混合）经指定向量模型（如 `text-embedding-v3`、`qwen3.7-text-embedding` 或 `qwen3-vl-embedding`）编码为固定维度向量，并存入向量数据库；后续检索阶段，用户 query 被同样编码，系统通过向量相似度（如余弦相似度）从知识库中召回最相关的片段。
- **独立向量服务调用（`vector and sort` API）**：开发者可直接调用 `/api/v1/services/embeddings` 接口，对任意文本或图文对生成嵌入向量，适用于自建索引、A/B 测试、特征工程等灵活场景；多模态嵌入支持 `image_url + text` 联合编码，输出统一语义空间向量。
- **框架集成（LlamaIndex / Spring AI）**：通过 `DashScopeEmbedding`（Python）或 `DashScopeDocumentRetriever`（Java）等封装组件，自动完成文本切分、向量化与检索链路；本地构建索引时可自由指定模型（如 `text-embedding-v4`），而云端知识库（`DashScopeCloudIndex`）则强制使用平台托管的嵌入模型与切分策略。
- **混合检索与重排协同**：向量嵌入本身不参与重排序，但它是 rerank 模型（如 `rerank-v1`、`gte-rerank-hybrid`）的前置依赖——初检结果由向量相似度召回，再交由 rerank 模型进行细粒度相关性打分与重排序。

## 关键参数和配置

- **模型选择（`model`）**：必填字符串，需严格匹配平台支持列表，常见值包括：
  - 文本嵌入：`text-embedding-v1`（1024 维，≤512 token）、`text-embedding-v3`、`text-embedding-v4`、`qwen3.7-text-embedding`
  - 多模态嵌入：`multimodal-embedding-v1`、`qwen3-vl-embedding`
- **输入格式（`input`）**：
  - 文本模型：接受单个字符串（`"hello world"`）或字符串数组（`["doc1", "doc2"]`）
  - 多模态模型：接受 JSON 对象 `{"image_url": "https://...", "text": "描述文字"}`
- **输出编码（`encoding_format`）**：可选 `"float"`（默认，返回 float32 数组）或 `"base64"`（Base64 编码的二进制向量）；注意 rerank 模型不支持 `"base64"`。
- **维度与约束**：
  - 所有文本嵌入模型输出固定维度（如 `text-embedding-v1` 为 1024 维），无需配置；
  - 输入长度超限将被自动截断（如 `text-embedding-v1` 截断至 512 token），建议预处理控制输入长度；
  - 多模态模型对 `image_url` 的 HTTP 响应超时为 5 秒，不支持直接传入 `image_bytes`（该功能暂未上线）。

## 面向开发者，简洁实用

- ✅ **快速上手**：只需 `POST /api/v1/services/embeddings`，带 `model` 和 `input`，即可获得标准向量输出；响应中 `output.embeddings` 是核心结果数组。
- ✅ **生产建议**：
  - 中文短文本优先选用 `text-embedding-v3` 或更高版本（兼容性好、MTEB 指标优）；
  - 图文联合检索场景必须使用 `multimodal-embedding-v1` 或 `qwen3-vl-embedding`，且确保 `image_url` 可公开访问；
  - 批量嵌入时，使用数组形式 `input` 一次请求处理多条，比串行调用效率更高；
  - 向量需归一化后再计算余弦相似度（百炼所有文本/多模态嵌入模型输出已归一化，可直接点积）；
- ⚠️ **避坑提示**：
  - 不要硬编码模型名（如 `rerank-v1`）到 RAG 应用逻辑中，应从 Agent 配置或控制台获取实际生效模型；
  - `DASHSCOPE_WORKSPACE_ID` 必须与 API Key 所属业务空间一致，否则向量服务返回 `401 Unauthorized`；
  - 云端知识库不支持替换嵌入模型——若需自定义 embedding，应使用 LlamaIndex 的 `VectorStoreIndex` + `DashScopeEmbedding` 本地构建。

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [rag api](../api/rag-api.md)
- [frameworks](../api/frameworks.md)
- [more models](../api/more-models.md)


