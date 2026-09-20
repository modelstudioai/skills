# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在生成前动态检索相关上下文片段，并将其注入提示词（[prompt](../guides/prompt.md)），显著提升模型回答的事实准确性、领域专业性和私有知识覆盖能力，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼平台不是单一功能，而是贯穿多个产品模块的**核心能力底座**，其落地形态取决于应用构建方式：

- **知识库（Knowledge Base）**：RAG 的标准化实现载体。用户上传文档后，平台自动完成解析→智能切片→向量化→索引构建；调用时执行“查询向量化→稠密检索→（可选）重排→拼接上下文→LLM 生成”，全程封装为统一 API（如 `/api/v2/apps/knowledge/chat`）。支持多模态 RAG（图片/音视频问答）和混合检索（稠密+稀疏）。

- **LLM 应用（Agent / Workflow）**：RAG 作为可插拔工具集成。  
  - *Agent 2.0*：知识库被抽象为 `tool`，由模型自主决策是否调用、何时调用、调用哪些知识库（支持多库路由），并融合检索结果与思考链（`enable_thinking`）生成最终回答。  
  - *工作流*：通过独立的“知识库节点”显式编排 RAG 步骤，可配置检索模式（极速/多轮智能）、引用策略、拒答开关等，与其他 AI 节点（如意图识别、参数提取）协同构成复杂业务流程。

- **API 直接调用（Application Call）**：面向生产集成，通过 `rag_options` 参数在调用智能体或工作流时**按需注入 RAG 能力**。例如，在 `POST /v1/apps/{app_id}/chat` 请求中传入 `{"rag_options": {"pipeline_ids": ["idx-xxx"], "metadata_filter": {...}}}`，即可在不修改应用配置的前提下，为单次请求动态绑定指定知识库及过滤条件。

- **框架集成（LlamaIndex / Spring AI）**：提供 `DashScopeCloudRetriever` 等原生适配器，开发者可基于熟悉框架编写 RAG 逻辑，底层自动对接百炼云端知识库服务（含解析、切分、向量检索、重排），无需自建基础设施。

## 关键参数和配置

RAG 效果高度依赖以下关键参数，均支持在控制台或 API 中配置（部分创建后不可修改）：

| 类别 | 参数名 | 说明 | 典型取值范围 | 备注 |
|--------|--------|------|----------------|------|
| **检索控制** | `top_k`（召回数） | 向量检索返回的初始候选片段数量 | 1–100（知识库级）<br>1–20（服务级） | 过小易漏召，过大增加重排与生成开销 |
| | `similarity_threshold`（相似度阈值） | 过滤低质量召回片段的余弦相似度下限 | 0.01–1.0 | 建议从 `0.35` 起调，结合业务精度要求调整 |
| | `rerank_model_name`（重排模型） | 对召回结果精排，提升 Top-K 相关性 | `qwen3-rerank`, `qwen3-vl-rerank`, `gte-rerank-hybrid` | 多模态场景必选 VL 版本；文本场景推荐 hybrid 版本 |
| **内容准备** | `chunk_size`（切片长度） | 文档切分的最大 token 数 | 10–6000（默认 600） | 长文本建议 512–1024，兼顾语义完整与上下文容纳 |
| | `chunk_strategy`（切片方式） | 决定分块逻辑 | `smart_split`（智能）, `by_length`, `by_page`, `by_title` | 智能切分优先保语义，标题切分适合结构化文档 |
| **生成增强** | `rag_options.file_ids`（文件级 RAG） | 在 API 调用中指定本次检索的文件 ID 列表 | 字符串数组 | 实现“仅在此文档内问答”，替代全局知识库 |
| | `rag_options.metadata_filter`（元数据过滤） | 按自定义标签（如 `department:finance`, `version:2024`）缩小检索范围 | JSON 对象 | 需在导入文档时预设 metadata 字段 |

> ⚠️ 注意：嵌入模型（如 `text-embedding-v4`）在知识库创建时锁定，不可更改；切片参数（`chunk_size`, `chunk_strategy`）导入后即固化，如需调整需重建知识库。

## 面向开发者，简洁实用

- **快速验证**：用控制台 [Playground](https://bailian.console.aliyun.com/#/knowledge-base/playground) 直接测试检索召回质量与问答效果，无需写代码。
- **最小集成路径**：  
  ```bash
  # 1. 创建知识库（指定 embedding 模型）
  POST /api/v1/indices/rag/index/create_v2
  {"name":"my_kb","embeddingModelName":"text-embedding-v4"}
  
  # 2. 导入文档（触发解析与切片）
  POST /api/v1/indices/rag/index/{index_id}/documents
  {"docIds":["file-xxx"]}
  
  # 3. 发起 RAG 问答（自动完成检索+生成）
  POST /api/v2/apps/knowledge/chat
  {"index_id":"idx-xxx","query":"阿里云百炼的 RAG 支持哪些模型？"}
  ```
- **调试技巧**：  
  - 若召回结果不相关，优先检查 `chunk_size` 是否过小导致语义断裂，或 `similarity_threshold` 是否过高；  
  - 若答案未引用知识库内容，确认问答服务中已开启 `引用` 开关，并检查 `file_ids` 或 `pipeline_ids` 是否传入正确；  
  - 多模态 RAG 必须使用 `qwen3-vl-*` 系列模型（嵌入、重排、生成），且图片需以 base64 或 OSS URL 形式传入。
- **性能提示**：启用 `qwen3-rerank` 可提升 Top-3 准确率约 15–20%，但延迟增加约 300ms；对延迟敏感场景，可关闭重排，改用 `dense_similarity_top_k=50` + `sparse_similarity_top_k=20` 的混合检索平衡效果与速度。

## 关联主题页

- [knowledge base](../guides/knowledge-base.md)
- [rag api](../api/rag-api.md)
- [llm application](../guides/llm-application.md)
- [application call](../api/application-call.md)
- [frameworks](../api/frameworks.md)


