# 向量嵌入

向量嵌入（Vector Embedding）是将原始非结构化数据（如文本、图像、音频等）映射到低维稠密实数向量空间的数学表示过程，其核心目标是使语义相似的内容在向量空间中距离更近。该表示可直接用于相似度计算、聚类、检索与下游任务建模，是百炼平台实现语义理解与多模态对齐的基础能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **语义搜索与 RAG**：知识库创建时指定 `embeddingModelName`（如 `text-embedding-v4`），系统自动对文档切片进行向量化并构建向量索引；检索时将用户查询转为向量，在索引中执行近邻搜索（ANN），作为召回主通路。
- **多模态检索**：使用 `qwen3-vl-embedding` 等模型，支持单模态（纯文本/纯图）或融合输入（如图文对），生成统一语义空间下的向量，支撑图片问答、音视频片段定位等跨模态场景。
- **独立向量化服务**：通过 `/api/v1/services/embeddings/...` 接口直接调用，适用于自建索引、特征工程、聚类分析等定制化需求；支持同步（实时小批量）与异步（海量离线）两种模式。
- **Agent 与应用集成**：在 Agent 配置中显式绑定嵌入模型，确保检索服务与知识库底层向量表征一致；CLI 工具（如 `bl knowledge search`）底层也依赖此能力完成向量召回。
- **资产中心快速验证**：在控制台「资产中心」中选择 Embedding 模型，调试输入文本或图像，实时查看向量维度、值分布及响应延迟，加速模型选型与效果评估。

## 关键参数和配置

| 参数 | 说明 | 是否必填 | 典型值示例 |
|------|------|----------|------------|
| `model` | 嵌入模型标识符，决定向量质量与模态支持能力 | 是 | `"text-embedding-v4"`, `"qwen3-vl-embedding"` |
| `input` | 待嵌入内容：支持字符串、字符串数组、文件 URL 或 `contents` 多模态对象数组 | 是 | `"今天天气很好"` / `["A", "B"]` / `{"contents": [{"type": "text", "text": "..." }, {"type": "image", "image_url": "..."}]}` |
| `dimensions` | 指定向量输出维度（部分模型支持可调）；影响存储开销与检索精度 | 否（推荐显式指定） | `1024`, `2560`（需查阅对应模型文档确认支持范围） |
| `encoding_format` | 控制向量返回格式：`"float"`（默认，JSON 数组）、`"base64"`（压缩传输） | 否 | `"base64"`（注意：老网关不支持） |
| `enable_fusion` | 仅 `qwen3-vl-embedding` 支持：设为 `true` 时对多模态输入生成单一融合向量 | 否 | `true` |

> ⚠️ 注意：  
> - 向量维度必须与后续使用的向量数据库（如 Milvus、Pinecone）或检索服务配置严格一致；  
> - 多模态嵌入中，`qwen2.5-vl-embedding` 强制融合，无 `enable_fusion` 参数；`qwen3-vl-embedding` 默认不融合，需显式开启；  
> - 所有 Embedding 请求单次最多处理 1024 token（按模型 tokenizer 计算），超长输入将被截断且不报错。

## 面向开发者，简洁实用

- ✅ **首选模型**：文本场景用 `text-embedding-v4`（高精度+兼容性好），多模态场景用 `qwen3-vl-embedding`（支持灵活融合）；  
- ✅ **调试建议**：先在资产中心调试单条输入，确认向量长度、响应时间与语义合理性；再批量测试相似句对的余弦相似度（应 >0.85）；  
- ✅ **生产集成**：  
  - 小流量/低延迟：用同步接口 `/api/v1/services/embeddings/text-embedding/text-embedding`；  
  - 大批量/离线处理：用异步批处理 `text-embedding-async-v2`，注意任务结果保留 24 小时；  
- ✅ **避坑提示**：知识库创建后嵌入模型不可变更，若需升级模型，请新建知识库并重新导入；RAG API 中 `multimodalEmbeddingModelName` 在视觉问答场景下必须显式传入，不可依赖默认值。

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [rag api](../api/rag-api.md)
- [knowledge base](../guides/knowledge-base.md)
- [asset center page](../guides/asset-center-page.md)
- [more models](../api/more-models.md)


