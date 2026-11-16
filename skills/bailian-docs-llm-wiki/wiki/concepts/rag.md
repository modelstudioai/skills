# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将外部知识检索与大语言模型（LLM）生成能力深度融合的技术范式。它通过在模型推理前动态检索相关知识片段，并将其作为上下文注入 prompt，显著提升回答的准确性、时效性与可溯源性，同时避免模型幻觉和知识固化问题。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，RAG 不是独立功能模块，而是贯穿于多个核心能力层的**基础增强机制**，其落地方式因使用场景而异：

- **RAG API 场景**：以知识库为单位提供端到端 RAG 服务。开发者通过 `POST /api/v1/indices/knowledge/search`（纯检索）或 `POST /api/v2/apps/knowledge/chat`（检索+生成）调用已发布的 Agent，平台自动完成：文档切片向量化（`embeddingModelName`）、语义检索、重排序（`rerankModelName`）、结果拼接与 LLM 生成。所有 RAG 行为由 Agent 实例封装并发布后生效，**知识库本身不直接执行生成**。

- **Agent 开发场景（Managed / Flow / Sandbox）**：RAG 作为上下文注入能力（`agent context`）集成。开发者在请求中声明 `context.knowledge_base.ids`，平台自动触发对应知识库的检索流程，并将 Top-K 结果（经重排后）注入 LLM 输入上下文。该方式支持多知识库混合检索、与 Memory/Connector 并行加载，适用于需灵活编排的复杂 Agent。

- **应用级 RAG（如企业微信助手、网站 AI 助手）**：通过 `/v1/chat/completions` 接口配合 `retrieval_config` 参数启用。此路径适合轻量集成，无需创建独立 Agent，但仅支持单知识库、有限重排策略（如 `top_k=3`），且不参与 `agent context` 的统一调度与 token 管理。

> ✅ 关键共识：无论哪种路径，RAG 的核心价值在于**运行时动态注入**——知识库内容不参与模型训练或微调，所有检索与融合均发生在每次请求中，确保知识实时更新、权限隔离与按需加载。

## 关键参数和配置

| 参数 | 所属层级 | 类型 | 说明 | 典型值 |
|------|----------|------|------|--------|
| `knowledge_base.ids` | `context` 对象 | `string[]` | 指定要检索的知识库 ID 列表（需已发布） | `["kb-xxx1", "kb-xxx2"]` |
| `retrieval_config.top_k` | 应用级调用 | `int` | 检索返回的原始片段数（未重排） | `5` |
| `retrieval_config.rerank_model` | 应用级调用 | `string` | 指定重排序模型（若启用重排） | `"qwen3-rerank"` |
| `rerankTopN` / `rerankMinScore` | 知识库/Agent 级别 | `int` / `float` | 在知识库创建或 Agent 配置中设置，控制重排后保留数量与最低分阈值 | `3`, `0.35` |
| `embeddingModelName` | 知识库创建时 | `string` | 向量化模型，决定检索质量基线 | `"text-embedding-v4"` |
| `multimodalEmbeddingModelName` | 多模态知识库 | `string` | 支持图文混合检索的嵌入模型 | `"qwen3-vl-embedding"` |

⚠️ 注意事项：
- 所有 RAG 调用必须基于**已发布的 Agent ID**（`agent_id`）或**已授权的知识库 ID**，未发布/未授权将返回错误；
- 检索结果占用输入 token，需主动监控 `context_truncated: true` 响应字段，建议将 `retrieval_config.top_k` 控制在 3–5 以内；
- 重排序（Rerank）为可选增强步骤，若未配置 `rerankModelName` 或 `rerankTopN`，则跳过精排，直接使用向量检索 Top-K 结果。

## 面向开发者，简洁实用

- **快速起步**：优先使用 RAG API 的 `/api/v2/apps/knowledge/chat` 接口，只需创建知识库 → 创建并发布 Agent → 调用带 `agent_id` 的问答接口，5 分钟内可验证效果。
- **调试技巧**：在请求头添加 `X-Debug-Context: true`，响应中 `debug.context_summary` 会明确列出各知识库是否命中、检索耗时、token 占用及截断状态。
- **性能优化**：
  - 文档预处理时启用 ParseX 自动切片（避免人工分段不合理）；
  - 高频问答场景，选用 `qwen3-rerank` + `rerankTopN=3` 平衡精度与延迟；
  - 多知识库联合检索时，注意 `context.knowledge_base.ids` 顺序影响混排权重（靠前优先）。
- **避坑指南**：
  - ❌ 不要尝试在 `system` 角色 message 中硬编码知识片段——这属于 Prompt 注入，非 RAG，无法更新、不可审计、易超 token；
  - ❌ 不要复用未发布的 Agent ID —— “Agent 未发布” 是最常见报错，发布操作不可跳过；
  - ✅ 所有知识库操作（增删改查）均通过 RAG API 完成，**不通过 `/v1/chat/completions` 接口管理知识库**。

RAG 是百炼平台实现“准确、可控、可解释”AI 服务的核心支柱。善用它，让模型真正成为你知识资产的智能接口。

## 关联主题页

- [rag api](../api/rag-api.md)
- [agent development](../guides/agent-development.md)
- [agent context](../guides/agent-context.md)
- [application use cases](../guides/application-use-cases.md)
- [agent legacy](../guides/agent-legacy.md)


