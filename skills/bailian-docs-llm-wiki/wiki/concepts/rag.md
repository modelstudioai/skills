# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，简称 RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态检索相关文档片段，并将其作为上下文注入提示（[prompt](../guides/prompt.md)），使模型能在不更新参数的前提下，准确、可溯源地回答基于私有或时效性知识的问题。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼平台不是单一功能，而是贯穿多个产品模块的底层增强能力，开发者可根据需求层级选择适配方式：

- **知识库问答（开箱即用）**：在控制台创建「知识库」并上传文档后，绑定至智能体应用、工作流中的「知识库节点」或高代码应用，调用 `/v1/chat/completions` 时传入 `knowledge_base_id` 即可自动启用 RAG 流程（检索 → 重排 → 生成）。适用于客服助手、内部文档查询等标准场景。

- **知识问答（RAG 智能体）**：通过 `/api/v2/apps/knowledge/chat` 接口调用已发布的「知识问答」服务实例。该接口封装完整 RAG Agent 能力，支持多跳检索、工具调用（如 `section_browse`）、流式规划与生成，返回含引用标记的答案，适合需复杂推理与证据溯源的业务。

- **知识检索（原子级能力）**：调用 `/api/v1/indices/knowledge/search` 获取原始语义匹配的 chunk 列表（含 `content`、`score`、`source` 等字段），开发者可自行拼接 [prompt](../guides/prompt.md)、融合多源结果或集成到自定义 RAG pipeline 中，适用于低延迟要求、需细粒度控制或与第三方 Embedding/LLM 混合部署的场景。

- **工作流编排**：在 Workflow 中，「知识库节点」作为独立 AI 节点，支持配置 `top_k`、`retrieval_mode`（vector/keyword/hybrid）、`enable_rerank` 等参数，并可与条件判断、循环、多模态解析等节点串联，构建带状态、多步骤的 RAG 增强流程（如“先检索合同条款 → 再比对用户提问 → 最后生成合规建议”）。

- **智能体（Agent）工具链**：在 Agent 2.0 中，知识库被抽象为标准工具（`semantic_search`），与其他 MCP 工具统一参与「规划-执行-反思」链路。模型自主决定是否调用、如何组合检索结果，实现更灵活的上下文感知与任务分解。

## 关键参数和配置

以下参数在不同 RAG 使用路径中高频出现，开发者应按需显式设置以优化效果：

| 参数名 | 类型 | 默认值 | 说明 | 所属场景 |
|--------|------|--------|------|----------|
| `top_k` | integer | `3` | 检索返回的最相关文本片段数（范围 1–10）；增大可提升召回率，但可能引入噪声 | 知识库、知识检索、工作流知识库节点、本地 RAG 方案 |
| `score_threshold` / `similarity_threshold` | float | `0.0` | 相似度阈值（0.0–1.0），低于此值的片段不参与后续生成；设为 `0.3`~`0.5` 可过滤低质匹配 | 知识库、应用用例、本地 RAG 方案 |
| `retrieval_mode` | string | `"hybrid"` | 检索模式：`"vector"`（纯向量）、`"keyword"`（BM25）、`"hybrid"`（两者融合）；混合模式通常鲁棒性最佳 | 知识库、工作流知识库节点 |
| `enable_rerank` | boolean | `true` | 是否启用重排序模型（仅对 `qwen-plus` 及以上模型生效）；开启后对 top_k 结果二次打分排序，显著提升答案准确性 | 知识库、工作流知识库节点 |
| `prompt_template` | string | 内置模板 | 自定义生成提示词，需包含 `{context}` 和 `{question}` 占位符；可用于控制答案格式、强调引用或添加领域约束 | 知识库、本地 RAG 方案 |

> ⚠️ 注意：`agent_id` 是知识服务的唯一标识，但**严格区分类型**——知识问答接口必须使用「知识问答」服务 ID，知识检索接口必须使用「知识检索」服务 ID，混用将返回 `AgentApp.NotFound` 错误。

## 面向开发者，简洁实用

- **快速验证**：控制台新建知识库 → 上传 1–2 份 PDF/DOCX → 创建智能体应用并绑定该知识库 → 发布后直接调用 endpoint 测试，全程无需写代码。
- **调试必查**：若答案不准或无引用，优先检查三处：① 知识库状态是否为 `active`；② 检索 `top_k` 是否过小（尝试设为 `5`）；③ `score_threshold` 是否过高（临时设为 `0.0` 排查）；④ 通过 [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md) 查看实际召回的 chunk 内容。
- **生产优化**：
  - 对长文档（>50 页），启用「增量同步」避免全量重建索引；
  - 高并发场景下，将 `top_k` 控制在 `3`–`5`，避免生成阶段 token 超限；
  - 需要强溯源时，在 `prompt_template` 中明确要求“答案必须标注来源段落编号”；
  - 多知识库需求，须手动合并文档或聚合各库检索结果，平台暂不支持跨库联合检索。
- **API 调用要点**：
  - 知识问答接口**强制流式**（`stream=true` + `Accept: text/event-stream`）；
  - 知识检索接口返回 JSON，务必校验响应体 `success` 字段（非仅 HTTP 状态码）；
  - 所有 RAG 请求均需确保知识服务已「发布」，否则返回 `AgentApp.NotFound`。

## 关联主题页

- [start using](../guides/start-using.md)
- [llm application](../guides/llm-application.md)
- [knowledge](../api/knowledge.md)
- [knowledge base](../guides/knowledge-base.md)
- [application support](../guides/application-support.md)
- [use cases](../guides/use-cases.md)
- [application use cases](../guides/application-use-cases.md)


