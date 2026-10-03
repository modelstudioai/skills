# 向量嵌入

向量嵌入（Vector Embedding）是将原始文本、图像、视频等非结构化数据映射到高维稠密实数向量空间的表示方法，使语义相近的内容在向量空间中距离更近，从而支撑检索、聚类、去重、RAG 等下游任务。该表示不依赖关键词匹配，而是基于模型对语义的理解生成，是百炼平台实现语义搜索与多模态理解的核心基础能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **知识库（RAG）构建**：知识库创建时需指定嵌入模型（如 `text-embedding-v4`），系统自动对文档切片进行向量化，并构建可检索的向量索引；向量质量直接影响召回准确率与问答依据可靠性。
- **通用语义检索服务**：通过 `/api/v1/services/embeddings/text-embedding`（同步）或 `/api/v1/services/embeddings/text-embedding/batch`（异步）接口，开发者可独立调用文本向量能力，用于自建检索系统、相似文本推荐、去重等场景。
- **多模态统一表征**：使用 `qwen3-vl-embedding` 或 `tongyi-embedding-vision-plus-2026-03-06` 等模型，支持文本+图像+视频混合输入，生成**融合向量**（单向量表征跨模态语义）或**独立向量**（各模态各一向量），服务于图文搜索、音视频内容理解等场景。
- **框架集成开发**：LlamaIndex 通过 `DashScopeEmbedding` 组件封装调用，Spring AI Alibaba 亦提供对应 Embedding 支持；开发者可将向量生成无缝嵌入本地 RAG 流程（解析 → 切分 → 嵌入 → 索引），绕过云端知识库限制，实现完全自定义。
- **Agent 与工作流底座**：RAG Agent 的检索阶段依赖向量嵌入完成初步召回；其配置中的 `embedding_model` 字段（如 `text-embedding-v4`）即决定整个知识服务的语义表征能力边界。

## 关键参数和配置

| 参数 | 适用模型/场景 | 说明 | 注意事项 |
|------|----------------|------|-----------|
| `dimensions` / `dimension` | 同步文本向量（OpenAI 兼容） / 多模态向量（DashScope 原生） | 指定向量维度，如 `64`、`256`、`1024`；`text-embedding-v4` 支持 64–2560 可调，更高维通常提升精度但增加存储与计算开销 | OpenAI 接口用 `dimensions`，DashScope 多模态接口用 `dimension`；旧模型（如 `v2`）不支持该参数，固定维度 |
| `text_type` | 批处理文本向量（`text-embedding-async-v1/v2`） | 取值 `document`（默认，用于知识库底库）或 `query`（用于用户检索查询）；影响向量方向性，对检索效果有显著影响 | 必须严格区分用途：底库切片用 `document`，用户问题用 `query`，混用将导致语义错位 |
| `enable_fusion` | `qwen3-vl-embedding` 模型 | `true`：将 `contents` 中所有模态输入融合为 1 个向量；`false` 或未设置：返回各模态独立向量 | 仅该模型支持；其他多模态模型（如 `tongyi-embedding-vision-plus-2026-03-06`）通过输入格式隐式控制融合，不依赖此参数 |
| `model_name` | 框架集成（LlamaIndex/Spring AI） | 指定嵌入模型标识，如 `"text-embedding-v4"`、`"qwen3-vl-embedding"` | 框架内需与百炼平台实际可用模型名一致；建议优先选用带版本后缀的最新模型（如 `-2026-03-06`）以获得最佳效果 |

> ⚠️ 重要提示：  
> - 向量模型在知识库创建时选定且**不可修改**，如需更换，需重建知识库；  
> - 多模态嵌入中，`qwen2.5-vl-embedding` 仅支持融合向量且不支持多图，而 `tongyi-embedding-vision-plus`（无后缀）仅支持独立向量——请以 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md) 中的能力对照表为准；  
> - `gte-rerank` 系列模型将于 2026 年 5 月 30 日下线，但其配套的 `text-embedding-v2` 等嵌入模型仍长期可用。

## 面向开发者，简洁实用

- ✅ **选型建议**：  
  - 中文为主、兼顾性能：用 `text-embedding-v4`（64–2560 维可调，推荐 256 或 512）；  
  - 超长文本（≤128K Token）：用 `qwen3.7-text-embedding`；  
  - 图文混合搜索：首选 `qwen3-vl-embedding`（支持 `enable_fusion=true`）或 `tongyi-embedding-vision-plus-2026-03-06`（支持多图+视频+文本混合输入）。

- ✅ **调用速查**：  
  - 小批量（≤20 条）→ 同步接口：`POST /compatible-mode/v1/embeddings`（OpenAI 兼容）或 `/api/v1/services/embeddings/text-embedding/text-embedding`（DashScope 原生）；  
  - 大批量（万级+）→ 异步批处理：`POST /api/v1/services/embeddings/text-embedding/batch` + `X-DashScope-Async: enable`，输入为 OSS URL；  
  - 多模态 → `POST /api/v1/services/embeddings/multimodal-embedding`，按文档要求组织 `contents` 数组。

- ✅ **避坑提醒**：  
  - 不要对同一份文本同时用 `document` 和 `query` 类型生成向量；  
  - 多模态输入时，确保 `contents` 中每个元素的 `type`（`text`/`image`/`video`）与 `value`（字符串或 OSS URL）严格匹配；  
  - 使用框架时，确认 `DashScopeEmbedding` 的 `model_name` 与百炼控制台「模型中心」中已开通的模型完全一致（含大小写与版本号）。

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [knowledge base](../guides/knowledge-base.md)
- [rag api](../api/rag-api.md)
- [frameworks](../api/frameworks.md)
- [more about models](../api/more-about-models.md)


