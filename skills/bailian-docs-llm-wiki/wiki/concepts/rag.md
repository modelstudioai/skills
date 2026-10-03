# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）与外部知识源动态结合的技术范式：在生成回答前，系统先从结构化或非结构化知识库中检索相关片段，再将检索结果作为上下文注入提示（[prompt](../guides/prompt.md)），引导模型生成准确、可溯源、事实一致的响应。

在百炼平台中，RAG 不是独立模块，而是贯穿知识管理、检索服务与生成应用的一体化能力链路，核心目标是让大模型“言之有据”，同时保障企业私有知识的安全可控与高效复用。

## 在百炼平台的不同场景中，这个概念如何使用

- **知识库问答（核心场景）**：通过创建知识库（Knowledge Base）并绑定 RAG Agent，用户提问时系统自动执行「向量检索 → 重排精筛 → 上下文拼接 → 大模型生成」全流程。支持文档、表格、图片、音视频等多模态数据，适用于客服助手、内部知识查询等生产场景。
- **智能体应用（Agent）集成**：在调用已发布的智能体应用时，通过 `rag_options` 参数显式指定知识库（`pipeline_ids`）、文档（`file_ids`）、元数据过滤条件（`metadata_filter`）或标签（`tags`），实现按需启用 RAG 增强，无需修改应用逻辑。
- **低代码渠道集成（AppFlow）**：在网站悬浮窗、企业微信、钉钉等渠道中嵌入 AI 助手时，只需在应用配置页启用“知识库”并设为“必定调用”，即可零代码获得 RAG 能力，所有检索与生成由平台自动调度。
- **本地开发框架集成**：通过 LlamaIndex 或 Spring AI Alibaba SDK，开发者可组合 `DashScopeParse`（解析）、`DashScopeJsonNodeParser`（切分）、`DashScopeEmbedding`（向量化）、`DashScopeCloudRetriever`（检索）与 `DashScope`（生成）构建全自定义 RAG 流程，灵活控制各环节行为。
- **API 直接调用**：  
  - 底层检索：调用 `/api/v1/indices/rag/index/retrieve` 获取原始召回结果（无重排）；  
  - 联合语义检索：调用 `/api/v1/indices/knowledge/search`（需 `agent_id`），策略由 Agent 配置驱动；  
  - 流式问答：调用 `/api/v2/apps/knowledge/chat`，返回带引用高亮的 SSE 流式响应。

## 关键参数和配置

| 层级 | 参数名 | 说明 | 典型取值 | 生效位置 |
|------|--------|------|-----------|------------|
| **检索阶段** | `top_k`（初步召回数） | 向量检索返回的候选切片数量 | `10–100` | 知识库详情页 / Agent 配置 / API 请求体 |
| | `similarity_threshold`（相似度阈值） | 过滤低分切片，避免噪声干扰生成 | `0.3–0.8`（越高越严格） | 知识库详情页 / Agent 配置 / `rag_options` |
| | `rerank_model_name`（重排模型） | 对初检结果进行语义精排，提升相关性 | `qwen3-rerank`（文本）、`qwen3-vl-rerank`（多模态） | Agent 配置 / `rag_options` |
| **生成阶段** | `temperature` | 控制生成随机性，影响答案稳定性 | `0.0–0.5`（RAG 场景建议 ≤0.4） | 应用配置页 / `rag_options` / SDK 参数 |
| | `enable_thinking` | 启用模型内部推理链，提升复杂问题拆解能力 | `true` / `false` | 知识库问答服务配置 |
| **知识构建期** | `chunk_size`（切片长度） | 影响上下文完整性与检索精度平衡 | `300–1000` token（默认 `600`） | 创建知识库时设置 / `DashScopeJsonNodeParser` |
| | `embedding_model`（嵌入模型） | 决定语义匹配质量，创建后不可更改 | `text-embedding-v4`（推荐） | 创建知识库时选定 |

> ⚠️ 注意：`top_k` 与 `similarity_threshold` 存在协同效应——提高阈值可能降低有效召回数，建议优先调优 `top_k`，再微调阈值；`temperature` 在 RAG 场景中宜设较低值（如 `0.3`），以抑制幻觉、强化依据依赖。

## 面向开发者，简洁实用

- ✅ **快速验证**：用控制台 Playground 选择知识库 → 切换“知识问答”模式 → 输入问题，实时查看命中文档卡片与引用高亮，5 分钟完成效果验证。
- ✅ **生产集成**：优先使用 `/api/v1/indices/knowledge/search`（联合检索）和 `/api/v2/apps/knowledge/chat`（流式问答），二者均基于已发布的 `agent_id`，策略统一管控，避免参数分散。
- ✅ **调试技巧**：开启 `debug: true`（部分 API 支持）或在 Playground 中勾选“显示检索过程”，可查看每步召回内容、重排分数与 [prompt](../guides/prompt.md) 构造细节。
- ✅ **性能优化**：若延迟敏感，可关闭重排（`enable_reranking: false`）或降低 `top_k` 至 `10–20`；若准确性优先，启用 `qwen3-rerank` 并设 `rerank_top_n: 5`。
- ✅ **安全边界**：所有知识库运行在业务空间（Workspace）内，权限隔离；知识库 ID（`pipeline_id`）不暴露原始文件路径，确保私有数据不出域。

RAG 的本质是“让模型知道它该知道的”。在百炼，你只需聚焦知识组织与业务意图，其余——检索、排序、融合、生成——皆由平台可靠交付。

## 关联主题页

- [knowledge base](../guides/knowledge-base.md)
- [rag api](../api/rag-api.md)
- [application call](../api/application-call.md)
- [application use cases](../guides/application-use-cases.md)
- [frameworks](../api/frameworks.md)


