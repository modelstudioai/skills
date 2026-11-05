# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态检索相关上下文片段，并将其注入提示词（[prompt](../guides/prompt.md)），使模型能在不修改参数的前提下，实时、可控、可验证地利用私有或领域知识生成准确、可信的回答。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，RAG 不是单一接口或模型，而是贯穿知识管理、检索服务与生成应用的**端到端能力链路**，具体体现为以下三类核心使用方式：

- **知识库驱动的问答服务**：  
  以 `knowledge_base` 为载体，通过向量化（`text-embedding-v4` 等）、混合检索（向量 + 关键词）、重排（`qwen3-rerank`）和流式生成（`qwen3.6-plus` 等）四步闭环，实现“提问 → 检索 → 排序 → 生成”全流程托管。开发者只需创建并发布知识库，配置 Agent 即可调用 `/api/v2/apps/knowledge/chat` 获取带溯源的自然语言回答。

- **Agent 上下文动态注入**：  
  在智能体（Agent）应用中，RAG 作为 `agent context` 的一种关键来源（`type: knowledge_base`），与其他上下文（如 Memory、Connector）协同注入 [prompt](../guides/prompt.md)。系统自动完成检索、去重、截断（按 `context_max_tokens`）与格式归一化，无需手动拼接提示词。

- **低代码/无代码业务集成**：  
  在企业微信、钉钉、网站等场景中，RAG 以“知识库启用开关 + 相似度阈值 + 召回数量”等可视化参数嵌入应用配置。开发者在控制台勾选知识库、设置 `top_k=5` 和 `similarity_threshold=0.4`，即可让 AI 助手自动调用私有文档回答客户问题，全程无需写代码。

> ✅ 提示：所有 RAG 调用均依赖已**发布（Published）** 的知识库；草稿状态知识库不可用于运行时服务。

## 关键参数和配置

以下参数直接影响 RAG 效果，需在知识库创建、Agent 配置或 API 调用时显式指定：

| 参数名 | 作用域 | 取值范围 | 说明 | 是否可变 |
|--------|--------|----------|------|----------|
| `top_k` | 检索服务 / 应用配置 | 1–100 | 初步召回的切片数量（向量+关键词联合检索后） | ✅ 运行时可调（API 中传 `top_k`）或控制台配置 |
| `similarity_threshold` | 检索服务 / 应用配置 | 0.01–1.0 | 过滤低于该相似度的切片，避免噪声干扰生成 | ✅ 同上 |
| `max_retrieved_nodes` | 检索服务 | 1–20 | 最终送入 LLM 的切片总数（经重排后截取） | ✅ 同上 |
| `query_rewrite` | 检索服务 | `true` / `false` | 开启后自动优化模糊/多轮用户输入（如补全指代、改写歧义句） | ✅ 同上 |
| `enable_rerank` | 知识库服务配置 | `true` / `false` | 是否启用重排模型（如 `qwen3-rerank`），显著提升长尾查询精度 | ✅ 控制台或 API 配置 |
| `context_sources` | Agent YAML 配置 | JSON 数组 | 声明 RAG 知识库 ID（`{ "type": "knowledge_base", "id": "kb-xxx" }`）及其他上下文源 | ✅ Agent 版本更新即生效 |

> ⚠️ 注意：知识库创建后不可更改的参数（如 `chunking_strategy`、`embedding_model`、`max_chunk_length`）将直接影响 RAG 的底层效果上限，建议在首次创建时审慎选择。

## 面向开发者，简洁实用

- **快速验证**：用控制台 [Playground](raw/application-user-guide/knowledge-base/playground.md) 直接测试知识库检索结果与模型回答，观察切片匹配度与生成质量。
- **调试技巧**：调用 `/api/v1/indices/knowledge/search`（需 `agent_id`）可获取纯检索结果（含 `score`、`content`、`doc_id`），用于验证召回是否合理，再决定是否调整 `top_k` 或 `similarity_threshold`。
- **错误排查**：若返回空结果或低质量回答，优先检查：
  - 知识库是否已**发布**（非草稿）；
  - 文档是否成功切片（查看“切片列表”，确认 `status=success`）；
  - `similarity_threshold` 是否设得过高（建议从 `0.3` 起调）；
  - 查询语句是否过于简短（尝试开启 `query_rewrite` 或在 Prompt 中加引导句）。
- **性能优化**：对高并发问答场景，建议：
  - 使用 `qwen3-rerank` 替代默认重排（精度更高、延迟可控）；
  - 将 `max_retrieved_nodes` 设为 `5–8`，避免过多上下文稀释模型注意力；
  - 对图文/音视频等多模态知识库，明确启用 `qwen3-vl-rerank` 并传入对应模态字段。

RAG 是百炼平台实现“可控、可信、可解释”AI 的基础设施。善用它，你交付的不是黑盒模型，而是扎根于业务知识的智能助手。

## 关联主题页

- [rag api](../api/rag-api.md)
- [knowledge base](../guides/knowledge-base.md)
- [application use cases](../guides/application-use-cases.md)
- [agent context](../guides/agent-context.md)
- [vector and sort](../api/vector-and-sort.md)


