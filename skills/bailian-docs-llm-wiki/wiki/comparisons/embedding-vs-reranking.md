# 文本向量与排序对比

百炼平台同时提供**通用文本向量（Text Embedding）**和**多模态向量（Multimodal Embedding）**两大类向量服务，它们在输入模态、模型选择、接口形式和典型应用场景上有显著差异。本文从开发者技术选型的角度，对两者进行系统化对比，帮助开发者根据业务需求选择合适的向量方案。

## 核心维度对比

| 维度 | 通用文本向量（Text Embedding） | 多模态向量（Multimodal Embedding） |
| --- | --- | --- |
| **支持模态** | 纯文本 | 文本、图像、视频（跨模态统一语义空间） |
| **代表模型** | text-embedding-v4（Qwen3-Embedding）、text-embedding-v3/v2/v1 | qwen3-vl-embedding、tongyi-embedding-vision-plus/flash（含 2026-03-06 版本）、multimodal-embedding-v1 |
| **向量维度** | 64 ~ 2048（v3/v4 可指定；v1/v2 固定 1536） | 768 ~ 2560（因模型而异，部分支持自定义） |
| **单次最大输入** | 10 ~ 25 行（同步）；100,000 行（异步批处理） | 最多 20 个内容元素（因模型而异） |
| **单行/单条最大 Token** | 2,048（v1/v2）或 8,192（v3/v4） | 512 ~ 32,000 Token（因模型而异） |
| **API 协议** | OpenAI 兼容（同步）+ DashScope（同步/异步） | DashScope HTTP |
| **同步 API 端点** | `POST /compatible-mode/v1/embeddings`（OpenAI 兼容）或 DashScope SDK | `POST /api/v1/services/embeddings/multimodal-embedding/multimodal-embedding` |
| **异步批处理** | 支持（text-embedding-async-v1/v2，单文件 ≤ 200MB） | 不支持 |
| **向量类型** | 仅独立向量 | 独立向量 + 融合向量（部分模型支持） |
| **语种覆盖** | v4：100+ 语种及编程语言；v1/v2：约 10 种主流语种 | qwen3-vl-embedding：33 种语言；旧版：中英双语 |
| **SDK 支持** | OpenAI SDK（兼容模式）+ DashScope SDK（Python/Java） | DashScope SDK（Python/Java） |
| **定价（每千 Token）** | 0.0005 元（v3/v4）；0.0007 元（v1/v2）；Batch API 半价 | 文本 0.0007 元；图片/视频 0.0005 ~ 0.0018 元（因模型而异） |
| **区域可用性** | 未特别限制 | 北京 + 新加坡（新加坡仅部分模型） |

## 输入与输出格式对比

| 特性 | 通用文本向量 | 多模态向量 |
| --- | --- | --- |
| **输入格式** | 字符串、字符串列表或文件对象 | `contents` 数组，每个元素可包含 `text`、`image`（URL/Base64）、`video`（URL）、`multi_images`（URL 数组） |
| **输出格式** | `data[].embedding`（float 数组），按 `index` 排列 | `output.embeddings[].embedding`（float 数组），独立向量按输入顺序返回；融合向量返回单个向量 |
| **维度可调** | v3/v4 支持 `dimensions` 参数指定输出维度 | 部分新模型支持 `dimension` 参数 |
| **额外参数** | `encoding_format`（当前仅 float） | `enable_fusion`（融合开关）、`fps`（视频帧率）、`instruct`（任务说明）、`res_level`（分辨率） |

## 适用场景建议

### 选择通用文本向量的场景

- **纯文本语义搜索**：文档检索、FAQ 匹配、知识库问答等以文搜文场景。
- **大批量离线向量化**：需要对百万级文本进行批处理时，可使用异步批处理接口（text-embedding-async-v1/v2），单次支持 10 万行，且 Batch API 享半价优惠。
- **OpenAI 兼容生态**：已有基于 OpenAI Embedding API 的应用，可通过切换 base_url 零成本迁移。
- **多语种覆盖**：需要覆盖 100+ 语种（含编程语言）的向量化需求，首选 text-embedding-v4。
- **成本敏感场景**：纯文本计费更低，且支持 Batch 半价模式。

### 选择多模态向量的场景

- **跨模态检索**：以文搜图、以图搜视频、以视频搜文本等跨模态匹配场景。
- **多模态融合表征**：需要将商品图片与描述文本融合为统一向量的电商搜索、内容理解场景。
- **视觉内容理解**：图像分类、视频内容聚类、视觉语义分析等场景。
- **图文混合检索**：同时需要文本和图像的统一语义空间进行联合检索。

## 技术选型建议

1. **如果输入全是文本**，优先选择通用文本向量系列。模型更成熟，支持更大批量，计费更低，且兼容 OpenAI 生态。推荐使用最新的 text-embedding-v4。
2. **如果涉及图像或视频**，必须选择多模态向量系列。建议优先评估 qwen3-vl-embedding（语种覆盖最广、支持融合向量、文本上限最大）。
3. **如果需要大批量离线处理纯文本**，通用文本向量的异步批处理接口是唯一选择（多模态向量暂不支持异步批处理）。
4. **如果需要融合向量**（将多种模态合成单一表征），需确认模型是否支持：qwen3-vl-embedding 通过 `enable_fusion` 参数开启，2026-03-06 版本通过同一 content 对象实现，旧版模型仅支持独立向量。
5. **维度选择**：两个系列都提供维度可调能力（部分模型），较低维度可减少存储和检索成本，但可能牺牲精度，建议根据实际效果测试后决定。

## 被对比主题页

- [general text embedding](../api/general-text-embedding.md)
- [vector and sort](../api/vector-and-sort.md)


