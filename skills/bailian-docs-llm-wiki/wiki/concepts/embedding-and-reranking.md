# 向量嵌入与重排序

向量嵌入（Embedding）是将文本、图像等非结构化数据映射为稠密数值向量的过程，用于表征语义；重排序（Reranking）则是在初检结果基础上，基于 query 与候选文档的细粒度语义匹配，重新打分并精排，提升检索相关性。二者共同构成百炼平台 RAG 检索链路中“表征→召回→精排”的核心能力层。

## 在百炼平台的不同场景中，这个概念如何使用

- **RAG 知识库服务**：创建知识库时通过 `embeddingModelName`（如 `text-embedding-v4` 或 `qwen3-vl-embedding`）指定嵌入模型，自动完成文档切片向量化；检索时默认启用 `qwen3-rerank` 对 top-K 初检结果进行重排，可通过 Agent 的 `agent_config` 中 `hybrid_rerank` 开关控制是否启用。
- **独立向量/排序 API**：直接调用 `/v1/embeddings`（支持文本单模态、多模态联合嵌入）和 `/v1/rerank`（接收 `query + documents` 对象），适用于自定义检索流程、混合检索（dense + sparse）、跨源结果融合等高级场景。
- **框架集成（LlamaIndex / Spring AI Alibaba）**：
  - `DashScopeEmbedding` 组件封装嵌入调用，支持 `text-embedding-v3` 等模型；
  - `DashScopeRerank` 提供 `gte-rerank` 等模型及 `top_n`、`rerank_min_score` 等客户端可控参数；
  - `DashScopeCloudRetriever` 在云端知识库检索中默认启用重排，并通过 `enable_reranking` 和 `rerank_top_n` 控制行为。
- **多模态场景**：当知识库配置为 `knowledgeScene: image_qa` 时，嵌入阶段自动选用 `qwen3-vl-embedding`，支持图文联合编码；重排序仍由文本语义模型（如 `qwen3-rerank`）执行，要求输入为纯文本片段（即图像已解析为 caption 或 OCR 文本）。

## 关键参数和配置

| 场景 | 参数名 | 说明 | 可选值示例 | 备注 |
|------|--------|------|-------------|------|
| **RAG API（知识库创建）** | `embeddingModelName` | 指定嵌入模型 | `"text-embedding-v4"`, `"qwen3-vl-embedding"` | 创建知识库时传入，不可后续修改 |
| **RAG API（检索运行时）** | `rerankModelName` | 自定义重排模型 | `"qwen3-rerank"`（当前唯一可用） | 当前未开放独立配置接口，仅在响应中返回默认值 |
| **独立 Vector & Sort API** | `model` | 必填模型标识 | `"text-embedding-v4"`, `"rerank-v1"` | 需与端点 `/v1/embeddings` 或 `/v1/rerank` 匹配 |
| | `input` | 输入格式严格区分 | 字符串/字符串数组（embedding）；`{ "query": "...", "documents": [...] }`（rerank） | `multimodal-embedding-v1` 要求 `{"image_url": "...", "text": "..."}` |
| | `encoding_format` | 向量编码格式 | `"float"`（默认）, `"base64"` | 仅 embedding 接口支持 |
| **LlamaIndex 集成** | `model_name`（`DashScopeEmbedding`） | 嵌入模型名 | `"text-embedding-v3"` | 推荐用于高精度检索 |
| | `model`, `top_n`, `rerank_min_score`（`DashScopeRerank`） | 重排模型、返回数量、分数阈值 | `"gte-rerank"`, `5`, `0.3` | `rerank_min_score` 用于过滤低置信结果 |
| | `enable_reranking`, `rerank_top_n`（`DashScopeCloudRetriever`） | 是否启用重排、重排后返回数 | `True`, `5` | 默认开启，`rerank_top_n ≤ dense_similarity_top_k` |

> ⚠️ 注意事项：
> - 所有嵌入模型输出维度固定（如 `text-embedding-v4` 为 1024 维），不可配置；
> - rerank 接口单次最多处理 50 个 `documents`，超出需分批调用；
> - 多模态嵌入要求 `image_url` 公开可访问且响应头含 `Content-Type: image/*`，否则返回 400；
> - 云端知识库（`DashScopeCloudIndex`）强制使用百炼托管的嵌入与重排流程，不支持自定义模型或切分逻辑；
> - 临时文件 URL（用于多模态输入）仅限调试，生产环境请使用持久化 OSS 存储。

面向开发者：优先使用 RAG API 构建端到端知识库服务；若需灵活控制嵌入/重排粒度（如混合多源结果、A/B 测试不同模型），请直接调用 `/v1/embeddings` 和 `/v1/rerank`；框架用户推荐搭配 `DashScopeEmbedding` + `DashScopeRerank` 组合，兼顾易用性与可调性。

## 关联主题页

- [rag api](../api/rag-api.md)
- [vector and sort](../api/vector-and-sort.md)
- [frameworks](../api/frameworks.md)
- [more about models](../api/more-about-models.md)


