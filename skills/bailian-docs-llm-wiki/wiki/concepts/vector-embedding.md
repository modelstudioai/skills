# 向量嵌入

向量嵌入（Embedding）是将原始文本、图像等非结构化数据映射为固定维度稠密实数向量的过程，使语义相近的内容在向量空间中距离更近，从而支撑语义搜索、相似匹配、RAG 检索等下游任务。该表示不依赖关键词匹配，而是基于模型学习到的深层语义表征。

## 在百炼平台的不同场景中，这个概念如何使用

- **RAG 知识库构建**：知识库创建或更新时，系统自动调用指定的嵌入模型（如 `text-embedding-v1` 或 `qwen3.7-text-embedding`）对文档切片进行向量化，并构建向量索引；检索阶段通过计算用户 query 向量与切片向量的余弦相似度完成语义召回。  
- **直接 API 调用**：通过 `/api/v1/services/embeddings` 接口，开发者可独立调用文本或多模态嵌入服务，输入字符串数组或图像+文本组合，获取标准化向量结果，用于自定义检索、聚类、去重等逻辑。  
- **混合检索策略**：在 Knowledge API 的 `retrieval_strategy=hybrid` 模式下，向量嵌入与关键词检索并行执行，结果融合后排序，兼顾语义准确性与术语召回率。  
- **多模态理解场景**：使用 `multimodal-embedding-v1` 模型，可将图像（base64 编码）与描述文本联合编码为统一 512 维向量，支持跨模态相似检索（如“找与这张图语义最接近的文档”）。  
- **Agent 工作流集成**：在 RAG Agent 的 `agent_config` 中，嵌入模型作为底层检索组件被策略性调用，其输出向量参与动态路由、上下文感知重排等高级编排逻辑。

## 关键参数和配置

- **`model`**（必填）：嵌入模型标识符，例如：  
  - 文本：`"text-embedding-v1"`（1024 维，默认）、`"text-embedding-v2"`（更高精度）、`"qwen3.7-text-embedding"`（RAG 场景推荐）；  
  - 多模态：`"multimodal-embedding-v1"`（512 维，仅支持 `float` 输出）。  
  > ✅ 注意：模型名必须与 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 文档严格一致，大小写敏感。

- **`input`**（必填）：  
  - 文本模型：接受单个字符串（如 `"你好"`）或字符串数组（如 `["A", "B"]`），最大总长度 2048 tokens；  
  - 多模态模型：接受对象 `{ "image": "base64...", "text": "可选描述" }`，图像尺寸 ≤ 1024×1024。

- **`encoding_format`**（可选，仅文本模型）：  
  - `"float"`（默认）：返回浮点数数组（如 `[0.12, -0.45, ...]`）；  
  - `"base64"`：返回 base64 编码的二进制向量（节省传输体积）；  
  > ⚠️ `multimodal-embedding-v1` **不支持** `"base64"`，强制返回 `float`。

- **维度与兼容性**：所有嵌入模型输出维度固定且不可配置（如 `text-embedding-v1`: 1024，`multimodal-embedding-v1`: 512），向量可直接用于余弦相似度计算或存入主流向量数据库（如 Milvus、PGVector）。

## 面向开发者，简洁实用

- ✅ **快速验证**：用 `curl` 直接调用 `/api/v1/services/embeddings`，确认模型响应格式与延迟；  
- ✅ **生产建议**：  
  - RAG 场景优先选用 `qwen3.7-text-embedding`（精度/速度平衡）；  
  - 多模态需求明确时，用 `multimodal-embedding-v1` 并预处理图像至 ≤1024×1024；  
  - 批量嵌入请合并请求（传入字符串数组），避免高频单条调用；  
- ❌ **避坑提示**：  
  - 不要为 `multimodal-embedding-v1` 设置 `encoding_format=base64`（将报错）；  
  - 向量索引更新非实时（30–120 秒延迟），业务需容忍短暂不一致；  
  - 所有嵌入模型均**不支持** `top_k`、`dimension` 等可调参数——维度与行为由模型本身固化。

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [rag api](../api/rag-api.md)
- [knowledge base](../guides/knowledge-base.md)
- [model experience](../guides/model-experience.md)
- [more about models](../api/more-about-models.md)


