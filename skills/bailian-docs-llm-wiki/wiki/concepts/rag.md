# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态检索相关上下文片段，并将其注入提示（prompt），使模型能在不更新参数的前提下，准确、可信地回答领域专属、时效性强或私有化的复杂问题。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，RAG 不是独立功能模块，而是贯穿知识库构建、检索服务、智能体编排与应用集成的核心架构模式：

- **知识库驱动的问答应用**：在「智能体应用」中启用知识库绑定后，平台自动在每次请求时执行 RAG 流程——先从已发布的知识库中语义检索 Top-K 相关片段（支持文档、表格、图片、音视频等多模态知识库），再将检索结果与用户问题拼接为增强 prompt，交由指定大模型（如 `Qwen3.5-Plus`）生成最终回答。该流程对开发者透明，无需手动构造检索逻辑。

- **RAG API 直接调用**：通过 `/api/v2/apps/knowledge/chat` 接口发起流式问答时，系统强制执行 RAG：自动关联应用配置的知识库，完成向量检索 + 重排（默认 `qwen3-rerank`）+ 上下文注入 + LLM 生成三阶段处理；而 `/api/v1/indices/knowledge/search` 则提供纯检索能力，供开发者自定义融合策略（如多库加权混排、人工后处理等）。

- **AppFlow 低代码集成**：在网站、企业微信、钉钉等渠道部署 AI 助手时，只要在应用配置中开启「必定调用」并绑定知识库，AppFlow 即自动注入 RAG 能力——所有来自渠道的消息均经 RAG 流程处理，无需修改前端或渠道侧代码。

- **Agent 智能体编排**：当 Agent 配置了知识库作为工具之一（如 `knowledge_retrieval` 工具），模型可在规划阶段自主决定是否触发检索，实现条件式 RAG；此时检索结果以结构化 tool message 形式传入后续生成步骤，支持更灵活的多步推理。

## 关键参数和配置

RAG 行为主要由以下参数与配置控制，开发者需按需显式设置或在控制台调整：

- **知识库绑定**：在应用或 Agent 的 `agent_config` 中通过 `knowledge_base_ids` 字段指定一个或多个 `indexId`；多库场景下，系统默认并行检索、统一重排合并（无串行开关）。

- **重排模型**：通过 `rerankModelName` 参数指定（如 `"qwen3-rerank"`），影响检索结果排序质量；该参数在 Agent 草稿配置或 RAG API 请求体中可覆盖默认值。

- **嵌入模型**：知识库创建时指定 `embeddingModelName`（如 `"text-embedding-v3"` 或 `"qwen3.7-text-embedding"`），决定向量化精度；视觉类知识库需额外配置 `multimodalEmbeddingModelName`（如 `"qwen3-vl-embedding"`）。

- **检索范围控制**：
  - `top_k`：控制每库返回的检索片段数（默认 3，最大 10）；
  - `score_threshold`：过滤低相关性片段（浮点数，范围 0–1，默认不启用）；
  - `filter`：支持按 `category_id`、`file_id`、时间范围等元数据过滤（仅部分接口支持）。

- **流式与增量输出**：RAG 问答必须启用 `stream=true`；如需前端高效渲染，建议同时设置 `incremental_output=true`，确保 SSE 响应中每个 `data:` 事件仅含本次新增 token。

- **会话状态**：RAG 服务本身**不维护会话历史**；若需上下文感知，客户端须在每次请求的 `messages` 中完整传入历史对话（含 system/user/assistant 角色），平台将基于全部历史 + 检索内容联合生成。

> ⚠️ 注意：所有参数名严格区分大小写与命名风格（如 `indexId` vs `index_id`），请以各接口文档为准；硬编码模型名（如 `qwen3-rerank`）存在版本迭代风险，推荐优先使用控制台发布的 Agent 配置。

## 关联主题页

- [rag api](../api/rag-api.md)
- [application use cases](../guides/application-use-cases.md)
- [use cases](../guides/use-cases.md)
- [application support](../guides/application-support.md)


