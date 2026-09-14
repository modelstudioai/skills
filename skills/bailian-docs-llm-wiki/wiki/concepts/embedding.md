# 向量嵌入

向量嵌入（Embedding）是将原始文本、图像等非结构化数据映射到低维稠密实数向量空间的数学表示方法，其核心目标是让语义相近的内容在向量空间中距离更近（如余弦相似度更高），从而支撑语义检索、聚类、去重等下游任务。

## 在百炼平台的不同场景中，这个概念如何使用

- **RAG 知识库**：知识库构建时，系统自动调用默认嵌入模型（`text-embedding-v1`）对上传文档的切片进行向量化，并存入向量索引；检索阶段，用户查询被同样嵌入，再与索引中向量做相似度计算，返回 top-k 最相关片段。  
- **向量检索 API**：通过 `/v1/embeddings` 接口直接调用嵌入模型，支持批量文本（最多 2048 tokens/条）、多模态输入（需使用 `multimodal-embedding-v1`），输出可用于自建向量数据库或定制检索逻辑。  
- **资产中心管理**：嵌入模型作为一类独立资产（`asset_type="model"` 且用途为 embedding），可在资产中心查看、调试和复用；当前不支持用户上传或微调自定义嵌入模型。  
- **混合检索与重排序协同**：向量嵌入结果常作为第一阶段召回输出，交由 rerank 模型（如 `bge-rerank-v2`）进行精细化相关性重打分，形成“向量召回 + 排序精排”的标准 RAG 流程。  
- **数据连接扩展场景**：当结合结构化数据源（如 Elasticsearch）使用时，部分向量数据库插件可利用百炼嵌入能力对非结构化字段（如商品描述、日志文本）实时向量化，实现跨模态联合检索。

## 关键参数和配置

- `model`（必需）：指定嵌入模型 ID，如 `"text-embedding-v1"`（通用文本）、`"multimodal-embedding-v1"`（支持图文输入）。  
- `input`（必需）：字符串或字符串数组，单次最多支持 2048 tokens/条；超长文本将被截断，建议预处理分段。  
- `encoding_format`（可选）：取值 `"float"`（默认，返回浮点数列表）或 `"base64"`（压缩传输，但存在精度损失风险，生产环境慎用）。  
- 输出字段：`data[i].embedding` 为 float32 向量（维度固定，如 `text-embedding-v1` 为 1024 维），`usage.total_tokens` 返回总 token 数，用于计费与限流统计。  
- 注意：所有嵌入模型均**不可微调**，仅提供推理服务；向量维度、归一化方式（当前 `text-embedding-v1` 输出已归一化，余弦相似度 ≈ 点积）由模型本身决定，无需额外配置。

## 面向开发者，简洁实用

- ✅ **快速上手**：一行代码即可生成嵌入：
  ```python
  resp = client.embeddings.create(model="text-embedding-v1", input=["阿里巴巴百炼平台"])
  vector = resp.data[0].embedding  # list[float], len=1024
  ```
- ✅ **性能提示**：批量调用（传入字符串数组）比单条多次调用更高效；避免在循环内频繁新建 client 实例。  
- ✅ **生产注意**：知识库中 `score_threshold` 默认 0.3，对应余弦相似度；若业务要求高精度（如法律条款匹配），建议设为 ≥0.6 并配合 `enable_rerank=true` 提升结果质量。  
- ⚠️ **避坑指南**：  
  - 不要将 `base64` 编码向量用于精确相似度计算（解码后存在浮点误差）；  
  - 知识库暂不支持替换嵌入模型，如需更换，请重建知识库；  
  - 向量接口无流式响应，响应时间取决于输入长度与模型负载，建议设置合理 timeout（如 15s）。

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [knowledge base](../guides/knowledge-base.md)
- [data connection overview](../guides/data-connection-overview.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)
- [asset center page](../guides/asset-center-page.md)


