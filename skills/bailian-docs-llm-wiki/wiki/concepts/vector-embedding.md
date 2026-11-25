# 向量嵌入

向量嵌入（Vector Embedding）是将原始文本、图像、音频等非结构化数据映射到高维稠密实数向量空间的数学表示过程，使语义相近的内容在向量空间中距离更近（如余弦相似度更高），从而支撑语义搜索、RAG、跨模态检索等核心AI能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **RAG 知识库构建**：创建知识库时通过 `embeddingModelName`（如 `qwen3.7-text-embedding` 或 `text-embedding-v4`）指定嵌入模型，平台自动对上传文档切片进行向量化，并构建可检索的向量索引；多模态知识库还需配置 `multimodalEmbeddingModelName`（如 `qwen3-vl-plus`）。
- **独立向量服务调用**：通过 `/vector-and-sort` 接口直接调用嵌入模型，支持同步（低延迟实时）和异步批处理（10万行/任务）两种模式，适用于自定义索引构建、特征工程或离线预计算。
- **框架集成**：LlamaIndex 中使用 `DashScopeEmbedding` 组件，需显式传入 `model_name`（如 `"text-embedding-v3"`）；Spring AI Alibaba 通过 `spring-ai-alibaba-starter-dashscope` 自动绑定嵌入能力，无需手动向量化。
- **混合检索与多模态联合**：所有支持的文本/多模态嵌入模型（如 `qwen3-vl-embedding`）均产出统一语义空间的向量，允许文本查询与图像/视频文档直接计算相似度，实现跨模态语义检索。

## 关键参数和配置

| 参数 | 适用模型 | 说明 | 推荐值 |
|------|----------|------|--------|
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4` | 指定向量维度（影响精度与存储开销），默认 `1024`；`v1/v2` 及多模态模型不支持此参数 | `1024`（平衡）、`2048`（高精度场景） |
| `encoding_format` | 所有同步嵌入接口 | 返回格式：`float`（默认，便于调试）或 `base64`（节省带宽，适合大规模传输） | 生产环境建议 `base64`，开发调试用 `float` |
| `enable_fusion` | `qwen3-vl-embedding` | 设为 `true` 时，对图文混合输入生成单个融合向量；设为 `false` 则分别输出文本向量和图像向量 | 多模态检索推荐 `true` |
| `input` | 全部 | 支持字符串、字符串数组、文件 URL（如 `oss://bucket/key`）或结构化多模态对象（如 `{"text": "...", "image": "url"}`） | 单文本用字符串，批量用数组，多模态用对象 |

> ⚠️ 注意：  
> - `text-embedding-v4` 单行上限 8,192 Token，`qwen3.7-text-embedding` 支持 128K Token；超长文本需分块。  
> - 多模态嵌入模型（如 `qwen3-vl-embedding`）要求图片 ≤10MB、视频需先抽帧为图片序列。  
> - 向量维度必须与后续检索/相似度计算环节保持一致（例如 FAISS 索引需预先指定相同 `dimension`）。

## 面向开发者，简洁实用

- ✅ **快速上手**：一行代码即可获取向量  
  ```python
  from dashscope import TextEmbedding
  resp = TextEmbedding.call(model='qwen3.7-text-embedding', input=['杭州天气如何？'])
  vector = resp.output.embeddings[0].embedding  # list[float]
  ```

- ✅ **生产建议**：  
  - 实时服务优先选 `qwen3.7-text-embedding-flash`（低延迟）或 `text-embedding-v4`（高精度）；  
  - 离线批量建库用异步接口 `/api/v1/services/embeddings/text-embedding/text-embedding`（支持 10 万行/任务）；  
  - 多模态场景统一使用 `qwen3-vl-embedding`，启用 `enable_fusion=true` 简化下游逻辑；  
  - 向量需持久化存储时，务必记录所用 `model` 和 `dimensions`，避免混用导致相似度计算失效。

- ❌ **避坑提示**：  
  - 不要将 `text-embedding-v1` 的向量与 `v3` 模型的向量混存于同一索引；  
  - `base64` 编码向量需解码为 float 数组后才能用于余弦计算（SDK 已自动处理）；  
  - 临时文件 URL（`oss://...`）有效期仅 48 小时，勿用于长期索引构建。

## 关联主题页

- [rag api](../api/rag-api.md)
- [vector and sort](../api/vector-and-sort.md)
- [frameworks](../api/frameworks.md)
- [more about models](../api/more-about-models.md)
- [use cases](../guides/use-cases.md)


