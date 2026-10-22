# 向量嵌入

向量嵌入（Embedding）是将文本、图像、音频等非结构化数据映射到低维稠密实数向量空间的数学表示方法，使语义相近的内容在向量空间中距离更近。该表示是百炼平台实现语义检索、RAG、聚类与跨模态理解等高级AI能力的基础底座。

## 在百炼平台的不同场景中，这个概念如何使用

- **RAG 知识库构建**：在创建知识库时，通过 `embeddingModelName`（如 `text-embedding-v4`）或 `multimodalEmbeddingModelName`（如 `qwen3-vl-embedding`）指定嵌入模型，系统自动对上传文档切片进行向量化，并存入向量索引，支撑后续语义检索。
- **独立向量服务调用**：通过 `/vector` 类 API（如 `text-embedding-synchronous-api` 或 `multimodal-embedding-api-reference`）直接调用嵌入模型，适用于自定义 RAG 流程、本地索引构建、数据预处理等场景；支持同步（小批量实时）与异步（万级批量）两种模式。
- **框架集成开发**：在 LlamaIndex 等框架中，通过 `DashScopeEmbedding` 组件配置 `model_name="text-embedding-v3"` 等参数，无缝接入百炼嵌入能力，无需自行管理模型部署与推理逻辑。
- **多模态联合理解**：使用 `qwen3-vl-embedding` 等多模态嵌入模型时，可将文本、图像、视频片段统一编码至同一语义空间，实现“以图搜文”“以文搜图”等跨模态检索任务；通过 `enable_fusion` 参数控制是否融合多模态输入为单一向量。

> ⚠️ 注意：`text-embedding-v1/v2` 已属旧版低容量模型（单行 [Token](token.md) 上限仅 2048），新项目请优先选用 `text-embedding-v4`（8192 [Token](token.md)）、`qwen3.7-text-embedding` 或 `text-embedding-v3`（CMTEB 检索得分 73.23，当前最优）。

## 关键参数和配置

| 参数 | 适用接口/组件 | 说明 | 示例值 |
|------|----------------|------|--------|
| `model` / `model_name` | 所有嵌入调用 | 必填，严格匹配模型名列表，区分文本与多模态型号 | `"text-embedding-v4"`, `"qwen3-vl-embedding"` |
| `input` / `contents` | 请求体 | 文本嵌入：`string` 或 `array<string>`；多模态嵌入：`[{ "text": "..." }, { "image": "url" }]` 或融合格式 | `["你好", "世界"]`；`[{"text":"猫"},{"image":"https://..."}]` |
| `dimensions` | 文本/多模态嵌入（部分模型） | 可选，指定输出向量维度（影响存储与计算开销） | `1024`, `2560`（`qwen3-vl-embedding` 默认） |
| `enable_fusion` | `qwen3-vl-embedding` | 可选布尔值，启用后将 `contents` 中所有模态输入融合为单个向量 | `true` |
| `encoding_format` | 同步文本嵌入 API | 可选，控制返回格式（`"float"` 或 `"base64"`），长请求自动降级为 float | `"float"` |

- **性能建议**：
  - 实时低延迟场景（如在线问答）：使用同步接口，单次 ≤20 条文本（`qwen3.7-text-embedding`）或 ≤10 条（`text-embedding-v4`）；
  - 大批量预处理（如万级文档入库）：务必选用 `text-embedding-async-v2` 异步接口，单次最多支持 100,000 行；
  - 中文场景：`DashScopeJsonNodeParser` 默认 `language="cn"`，配合 `text-embedding-v3` 或 `v4` 可获得最佳语义保真度。

面向开发者，请始终以模型文档中标注的 [Token](token.md) 限制、维度支持与地域可用性为准（如 `qwen3-vl-embedding` 当前仅在北京 Region 可用），并在生产环境启用 `rerank_min_score` 和 `rerankTopN` 配合重排序模型进一步提升检索精度。

## 关联主题页

- [rag api](../api/rag-api.md)
- [vector and sort](../api/vector-and-sort.md)
- [frameworks](../api/frameworks.md)
- [model data overview](../guides/model-data-overview.md)


