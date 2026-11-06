# 向量嵌入

向量嵌入（Embedding）是将原始非结构化数据（如文本、图像等）映射为固定长度、稠密、实数型向量的数学表示，其核心目标是使语义相近的数据在向量空间中距离更近。该表示是百炼平台实现语义检索、相似匹配、RAG 检索召回及多模态理解的基础能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **语义检索与 RAG 召回**：在 RAG API 中，知识库（`document`/`image`/`multimedia` 类型）创建时需指定向量模型（如 `text-embedding-v1` 或 `multimodal-embedding-v1`），系统自动对文档切片或图像+文本描述生成嵌入向量并构建向量索引；运行时检索（`/knowledge/search`）即基于 query 嵌入与索引向量的余弦相似度完成 Top-K 召回。

- **框架集成开发**：LlamaIndex 通过 `DashScopeEmbedding` 组件调用 `text-embedding-v3` 等模型，直接参与本地索引构建或云端检索流程；Spring AI Alibaba 则通过 `DashScopeDocumentRetriever` 隐式依赖平台向量能力，无需手动调用嵌入接口。

- **原生 API 调用**：通过 `/api/v1/embeddings` 接口可独立调用文本嵌入模型（如 `text-embedding-v1`/`v2`/`v3`），批量生成句子或段落的向量；多模态嵌入（`multimodal-embedding-v1`）需传入 base64 图像 + 文本描述组合，输出联合语义向量。

- **混合检索与重排协同**：向量嵌入本身不负责排序，但为 rerank 模型（如 `rerank-v1` 或 `gte-rerank-v2`）提供高质量候选集——rerank 模型接收 query 和由嵌入召回的 documents，进行细粒度相关性打分（0.0–1.0），实现“粗排→精排”两级检索架构。

## 关键参数和配置

| 参数 | 适用模型 | 说明 | 默认值 |
|------|----------|------|--------|
| `model` | 所有嵌入模型 | 必填，模型标识符，如 `"text-embedding-v3"`、`"multimodal-embedding-v1"` | — |
| `input` | `text-embedding-*` | 必填，支持单个字符串或字符串数组（`string[]`），**不接受 object** | — |
| `input` | `multimodal-embedding-v1` | 必填，格式为 `{ "text": "...", "image": "base64-encoded-string" }` | — |
| `encoding_format` | `text-embedding-*` | 可选，`"float"`（默认，返回 float32 数组）或 `"base64"`（Base64 编码的二进制向量） | `"float"` |
| `batch_size` | — | **非 API 参数，但重要实践约束**：单次请求最多 128 个文本输入（超限返回 429）；建议生产环境按 32–64 批量调用以平衡延迟与吞吐 | — |

> ⚠️ 注意：  
> - `text-embedding-v3` 是当前推荐模型（CMTEB 检索任务得分 73.23），显著优于 v1/v2；  
> - 多模态嵌入不支持批量图像（`input` 中仅允许一个图像对象）；  
> - 所有嵌入模型输出向量维度固定（如 `text-embedding-v1`: 1024 维；`v3`: 1024 维；`multimodal-embedding-v1`: 1024 维），无需解析响应 schema 中的 `dimension` 字段。

## 面向开发者，简洁实用

- ✅ **快速验证**：用 curl 调用 `text-embedding-v3` 生成两个句子的向量，计算余弦相似度即可验证语义一致性：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/embeddings \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "model": "text-embedding-v3",
          "input": ["苹果是一种水果", "香蕉属于热带水果"]
        }'
  ```

- ✅ **生产建议**：  
  - RAG 场景优先使用 RAG API 创建知识库（自动嵌入+索引），而非自行调用 `/embeddings` + 自建向量库；  
  - 若需自定义切片逻辑或混合检索，用 LlamaIndex 的 `DashScopeEmbedding` + `DashScopeCloudRetriever` 组合，启用 `enable_reranking=True`；  
  - 多模态需求务必使用 `multimodal-embedding-v1`，且确保图像 base64 编码无换行、无前缀（如 `data:image/png;base64,`）。

- ❌ **避坑提示**：  
  - 不要向 `text-embedding-*` 传入 object 类型 `input`（如 `{ "text": "xxx" }`），会返回 400；  
  - 不要在 rerank 请求中复用 embedding 接口的 `input` 格式——rerank 的 `input` 是 `{ "query": "...", "documents": [...] }`；  
  - 向量维度不可变，下游应用（如 FAISS/Pinecone）请按 1024 维预设索引。

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [rag api](../api/rag-api.md)
- [frameworks](../api/frameworks.md)
- [more models](../api/more-models.md)


