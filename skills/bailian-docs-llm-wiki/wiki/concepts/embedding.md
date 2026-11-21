# 向量嵌入

向量嵌入（Embedding）是将原始非结构化数据（如文本、图像、视频等）映射到低维稠密实数向量空间的数学表示过程，其核心目标是让语义相近的内容在向量空间中距离更近，从而支撑检索、聚类、去重、RAG 等下游任务。

## 在百炼平台的不同场景中，这个概念如何使用

- **RAG 知识库构建**：在创建知识库时，需指定嵌入模型（如 `text-embedding-v4` 或 `qwen3-vl-embedding`），平台自动对导入文档进行切片与向量化，构建可检索的向量索引；多模态知识库（如 `image` 或 `multimedia` 类型）必须使用多模态嵌入模型。
- **实时语义检索**：调用 `/api/v1/indices/knowledge/search` 时，查询文本会通过同一嵌入模型实时转为向量，与知识库向量做相似度计算（默认余弦相似度），实现毫秒级语义召回。
- **向量服务 API 直接调用**：开发者可通过同步接口（如 `/compatible-mode/v1/embeddings`）或异步批处理接口（如 `/api/v1/services/embeddings/text-embedding/text-embedding`）独立调用嵌入能力，用于自建向量库、A/B 测试或离线特征工程。
- **框架集成场景**：在 LlamaIndex 或 Spring AI Alibaba 中，通过 `DashScopeEmbedding` 组件封装调用，自动复用百炼统一的模型选型、参数配置与鉴权机制，无需管理底层向量生成逻辑。
- **多模态融合建模**：对含文本+图像+视频的混合输入，可选用支持融合向量的模型（如 `tongyi-embedding-vision-plus-2026-03-06`），将多源信息编码为单个语义一致的向量，适用于跨模态搜索与推荐。

## 关键参数和配置

| 参数 | 类型 | 说明 | 常见取值 | 是否必需 |
|------|------|------|-----------|------------|
| `model` | string | 嵌入模型名称 | `text-embedding-v4`, `qwen3.7-text-embedding`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06` | ✅ |
| `dimensions` / `dimension` | integer | 输出向量维度 | 文本模型：64–2048；多模态模型：128–2560（具体以模型文档为准） | ❌（有默认值） |
| `input` | string / array | 待嵌入内容 | 同步接口：单条字符串或字符串数组；多模态接口：结构化对象（含 `text`, `image_url`, `video_url` 字段） | ✅ |
| `encoding_format` | string | 向量数值编码格式 | `float`（默认）、`base64`（节省带宽，需客户端解码） | ❌（仅同步文本接口支持） |
| `enable_fusion` | boolean | 仅 `qwen3-vl-embedding` 支持：启用多模态融合向量模式 | `true` / `false` | ❌（默认 `false`，即独立向量） |
| `text_type` | string | 批处理接口专用：区分文档向量 vs 查询向量 | `document`（默认）、`query`（用于非对称检索优化） | ❌ |

> ⚠️ 注意：  
> - 多模态模型中，`qwen2.5-vl-embedding` **仅支持融合向量**，不接受 `enable_fusion` 参数；`tongyi-embedding-vision-plus-*` 通过 input 结构隐式启用融合，无需显式参数。  
> - `dimensions` 不同模型支持范围不同，超出范围将返回 400 错误；建议优先使用默认维度（如 `text-embedding-v4` 默认 2048），平衡效果与性能。  
> - 异步批处理接口要求输入文件为公网可访问 URL，且单次最多 10 万行（`text-embedding-async-v2`）。

## 面向开发者，简洁实用

- ✅ **快速上手**：用 OpenAI 兼容方式调用最简示例（Python）：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key="YOUR_API_KEY",
      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
  )
  response = client.embeddings.create(
      model="text-embedding-v4",
      input=["今天天气真好", "阳光明媚适合出游"],
      dimensions=1024
  )
  vectors = [item.embedding for item in response.data]  # list of list[float]
  ```

- ✅ **生产建议**：
  - 实时检索场景优先用**同步接口**（低延迟）；批量预计算（如日更知识库）用**异步批处理**（高吞吐）；
  - RAG 场景中，确保查询与知识库使用**完全相同的嵌入模型 + 相同 `dimensions`**，否则相似度不可比；
  - 多模态任务请严格按模型文档构造 `input`：`qwen3-vl-embedding` 需显式传 `enable_fusion=true`；`tongyi-embedding-vision-plus-*` 直接传 `{ "text": "...", "image_url": "..." }` 即可融合。

- ❌ **避坑提示**：
  - 不要混用不同模型生成的向量做相似度计算（如用 `v3` 向量查 `v4` 索引）；
  - `encoding_format=base64` 仅新网关支持，老网关强制返回 `float`，勿依赖 base64 解码逻辑做兼容；
  - 批处理接口的 `text_type=query` 仅对 `text-embedding-async-*` 生效，同步接口不识别该参数。

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [rag api](../api/rag-api.md)
- [frameworks](../api/frameworks.md)
- [use cases](../guides/use-cases.md)
- [more models](../api/more-models.md)


