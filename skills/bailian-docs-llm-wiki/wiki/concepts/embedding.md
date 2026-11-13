# 向量化嵌入

向量化嵌入（Embedding）是将文本、图像、音视频等非结构化数据映射到统一高维语义向量空间的数学过程，其输出为固定长度的浮点数向量；该向量的几何距离（如余弦相似度）可有效表征原始内容的语义相关性。

## 在百炼平台的不同场景中，这个概念如何使用

- **RAG 知识库构建**：在创建知识库时，通过 `embeddingModelName`（文本）或 `multimodalEmbeddingModelName`（图文/音视频）指定嵌入模型，系统自动对导入文档切片进行向量化，并构建可检索的向量索引。支持 `basic_document_qa`、`lite_document_qa`、`visual_perception_qa`、`table` 等多类知识场景，每类绑定适配的嵌入能力。
- **独立向量服务调用**：通过 `vector and sort` API 直接调用嵌入模型，分为同步（低延迟、≤20 条）与异步（批量百万级、大文件）两类路径；支持纯文本（如 `text-embedding-v4`、`qwen3.7-text-embedding`）和多模态（如 `qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06`）输入，后者支持 `text`/`image`/`video` 混合输入并生成融合向量。
- **框架集成开发**：在 LlamaIndex 或 Spring AI Alibaba 中，使用 `DashScopeEmbedding` 组件（默认 `text-embedding-v2`，推荐升级至 `v3`）完成本地文档向量化；注意 `DashScopeCloudIndex` 为全托管方案，**不支持自定义嵌入模型或切分逻辑**，所有向量化由平台统一执行。
- **跨模态联合检索**：多模态嵌入模型（如 `qwen3-vl-embedding`）将不同模态数据映射至同一语义空间，使文本 query 可直接与图像/视频向量计算余弦相似度，支撑音视频搜索、图文问答等场景。

## 关键参数和配置

| 参数 | 适用场景 | 说明 |
|------|----------|------|
| `embeddingModelName` / `multimodalEmbeddingModelName` | RAG 知识库创建 | 必填字符串，如 `"text-embedding-v4"`（文本）、`"qwen3-vl-embedding"`（多模态）；决定知识库底层向量化能力。 |
| `dimensions` | 同步/异步向量 API | 可选，指定输出向量维度（如 `1024`, `2048`），不同模型支持值不同；`multimodal-embedding-v1` 固定为 1024，不可配置。 |
| `enable_fusion` | 多模态向量（旧版） | 布尔值，设为 `true` 时对同一 `content` 中的 text+image 生成融合向量；新版模型（如 `tongyi-embedding-vision-plus-2026-03-06`）通过结构化 `input.contents` 自动融合，无需此参数。 |
| `text_type` | 异步文本向量批处理 | 字符串，取值 `"query"` 或 `"document"`，用于优化检索任务效果（如 query 向量做归一化增强）；聚类等对称任务可忽略。 |
| `model_name` | LlamaIndex / Spring AI 集成 | `DashScopeEmbedding` 构造参数，默认 `"text-embedding-v2"`，生产环境建议显式设为 `"text-embedding-v3"` 以获得更高检索精度（CMTEB Retrieval 73.23 分）。 |

> ⚠️ 注意：  
> - 所有嵌入模型调用均需匹配地域专属 Endpoint（如北京：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com`）；  
> - 多模态嵌入输入必须使用 DashScope HTTP 接口（非 [OpenAI 兼容接口](openai-compatible-api.md)）；  
> - `gte-rerank` 系列排序模型已逐步淘汰，但其配套的 `text-embedding-v2` 仍可用；新项目请优先选用 `qwen3.7-text-embedding` 或 `text-embedding-v4`。

## 关联主题页

- [rag api](../api/rag-api.md)
- [vector and sort](../api/vector-and-sort.md)
- [more about models](../api/more-about-models.md)
- [frameworks](../api/frameworks.md)


