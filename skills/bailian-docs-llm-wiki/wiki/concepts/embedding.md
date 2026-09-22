# 向量嵌入

向量嵌入（Vector Embedding）是将原始数据（如文本、图像、视频等）映射到高维实数向量空间的数学表示过程，其核心目标是让语义相似的输入在向量空间中距离更近。该表示具备可计算性、可检索性和跨模态对齐能力，是百炼平台实现语义搜索、RAG、聚类与多模态理解的基础技术底座。

## 在百炼平台的不同场景中，这个概念如何使用

- **通用文本检索与分析**：通过 `text-embedding-v3`、`text-embedding-v4`、`qwen3.7-text-embedding` 等模型，将文档、查询、标签等文本转换为稠密向量，用于知识库索引构建、语义相似度计算、聚类分析等。同步接口适用于低延迟交互（如实时问答），异步接口 `text-embedding-async-v2` 支持单次10万行批量向量化，适用于知识库初始化或定期更新。

- **RAG 应用构建**：在 RAG API 和知识库服务中，向量嵌入是默认启用的底层能力。知识库创建时即绑定嵌入模型（如默认 `text-embedding-v4`），所有上传文档经智能切片后自动向量化并存入向量索引；检索阶段通过向量相似度（如余弦相似度）完成初步召回，再经重排序（Rerank）优化结果。

- **多模态统一表征**：使用 `qwen3-vl-embedding` 或 `tongyi-embedding-vision-plus-2026-03-06` 等模型，支持文本、图像、视频、多图混合输入。可通过 `enable_fusion=true`（旧模型）或同 content 对象内混写（如 `{"text": "...", "image": "..."}`）生成融合向量，实现跨模态语义对齐，支撑图文检索、视频内容理解等场景。

- **框架集成开发**：LlamaIndex 与 Spring AI Alibaba 提供 `DashScopeEmbedding` 和 `DashScopeCloudIndex` 等封装组件，开发者可一键接入百炼嵌入能力——本地构建索引时自由指定嵌入模型，云端知识库则自动托管向量化流程（不可自定义模型，但可选配）。

- **向量与排序联合工作流**：向量嵌入负责“粗召回”（dense retrieval），输出 top-k 相似切片；后续交由 `qwen3-rerank` 等排序模型进行 cross-encoder 精排，形成“向量+排序”两级检索范式，显著提升相关性精度。

## 关键参数和配置

| 参数 | 适用模型/场景 | 说明 | 注意事项 |
|------|----------------|------|-----------|
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v4`, `qwen3-vl-embedding` 等 | 指定输出向量维度（如 `2560`, `1024`, `256`） | 必须严格匹配模型支持列表；不支持的模型（如 `tongyi-embedding-vision-plus`）固定维度，传入将报错 |
| `encoding_format` | 同步文本向量（`text-embedding-*`） | 返回格式：`float`（默认）或 `base64`（节省带宽） | 新网关对长请求仍强制回落为 `float`；生产环境建议统一用 `float` 避免兼容性问题 |
| `text_type` | 异步文本向量（`text-embedding-async-v2`） | 取值 `document`（知识库底库文本）或 `query`（用户搜索词） | 影响模型内部表征优化，非对称检索任务（如文档库 vs 查询）**必须显式设置**以提升效果 |
| `enable_fusion` | `qwen3-vl-embedding`（仅旧版） | `true` 时将 `contents` 数组中所有模态输入融合为单向量 | 新版模型（如 `tongyi-embedding-vision-plus-2026-03-06`）已弃用此参数，改用同 content 对象内混合输入方式 |
| `input.contents` | 多模态向量 API | JSON 数组，每个元素为 `{ "type": "text"/"image"/"video", "data": "..." }` 或融合对象 `{ "text": "...", "image": "..." }` | 图像/视频需传 OSS URL 或 base64 编码；融合向量要求所有模态字段位于同一字典层级 |

## 面向开发者，简洁实用

- ✅ **首选模型**：中文场景推荐 `text-embedding-v4`（平衡精度与速度）；多模态融合推荐 `qwen3-vl-embedding`（支持 `enable_fusion`）或 `tongyi-embedding-vision-plus-2026-03-06`（新版融合更鲁棒）。
- ✅ **调用方式**：
  - 同步文本：`POST /compatible-mode/v1/embeddings`（OpenAI 兼容）或 `/api/v1/services/embeddings/text-embedding`（原生）；
  - 异步文本：HTTP 请求头加 `X-DashScope-Async: enable`，传 OSS 文件 URL；
  - 多模态：统一调用 `/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`。
- ⚠️ **避坑提示**：
  - `gte-rerank` 系列模型将于 2026-05-30 下线，请勿新接入；迁移至 `qwen3-rerank`；
  - 知识库创建后嵌入模型不可更改，如需换模型请新建知识库；
  - 异步向量化任务失败时，检查文件 URL 有效期（48 小时）及 `model_name` 是否与上传时一致；
  - 向量维度不匹配、`text_type` 未设置、融合输入格式错误是三大高频 400 错误原因。
- 📦 **SDK 快速起步**（Python）：
  ```python
  from dashscope import TextEmbedding, MultiModalEmbedding
  
  # 同步文本嵌入
  resp = TextEmbedding.call(model='text-embedding-v4', input=['你好', 'Hello'])
  
  # 多模态融合嵌入（新版）
  resp = MultiModalEmbedding.call(
      model='tongyi-embedding-vision-plus-2026-03-06',
      input={'contents': [{'text': '一只猫', 'image': 'https://xxx.jpg'}]}
  )
  ```

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [rag api](../api/rag-api.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [more about models](../api/more-about-models.md)


