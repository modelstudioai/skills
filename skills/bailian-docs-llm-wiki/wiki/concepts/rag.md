# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，简称 RAG）是一种将大语言模型（LLM）与外部知识源动态结合的技术范式：在模型生成响应前，先从私有或领域知识库中检索相关上下文片段，并将其作为提示的一部分输入模型，从而显著提升回答的准确性、时效性与事实一致性。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼平台不是单一功能，而是贯穿多个产品层级的**核心能力底座**，开发者可根据应用复杂度选择适配方式：

- **知识库（Knowledge Base）**：最直接的 RAG 实现。上传文档 → 自动解析/切片/向量化 → 构建专属索引 → 通过 `/v1/knowledge/qa` 接口一键完成“检索+生成”端到端问答。适用于客服知识库、内部文档助手等场景。
- **RAG API（`/v1/knowledge/query`）**：面向高可控性集成需求，提供细粒度控制链路：可先调用 `/v1/knowledge/retrieve` 获取原始切片（用于调试、审计或自定义后处理），再拼接至 Prompt 调用任意大模型；也支持 `stream=true` 流式返回生成结果。
- **LLM Application 工作流（Workflow）**：将 RAG 封装为可视化节点（如“知识库检索节点”或“文档解析+检索节点”），与其他 AI 节点（大模型、条件判断、工具调用）编排组合，实现多步骤推理（如“先查政策原文 → 再对比用户合同 → 最后生成风险提示”）。
- **智能体（Agent）**：Agent 1.0 中 RAG 作为预设工具执行单次检索；Agent 2.0 中 RAG 被统一抽象为标准工具（Tool），可由 Agent 自主规划调用时机与次数，支持多跳检索、混合工具协同（如“检索技术文档 + 调用代码解释器”）。
- **框架集成（LlamaIndex / Spring AI Alibaba）**：通过官方 SDK（如 `DashScopeCloudRetriever` 或 `DashScopeDocumentRetriever`）在本地代码中调用百炼云端知识库，无需管理向量数据库，快速构建 RAG 应用原型或嵌入现有系统。

> ✅ 关键共识：所有场景均复用同一套知识库基础设施（索引、切片、embedding 模型），确保行为一致；差异仅在于调用入口、控制粒度与编排自由度。

## 关键参数和配置

以下参数在多数 RAG 场景中通用，直接影响效果与性能：

| 参数 | 类型 | 默认值 | 说明 | 建议 |
|------|------|--------|------|------|
| `knowledge_id` | string | — | 必填。目标知识库唯一 ID，创建后获取 | 请勿硬编码，建议从环境变量或配置中心读取 |
| `query` | string | — | 必填。用户原始问题文本（≤2048 字符） | 提前清洗（去空格、截断超长输入），避免注入风险 |
| `top_k` | int | `3` | 检索返回的最相关切片数量（范围 1–50） | 初期设为 `3`～`5`；若答案不完整可增至 `10`，但注意增加延迟与噪声 |
| `enable_rerank` | bool | `false` | 是否启用语义重排序（rerank） | **强烈推荐设为 `true`**：`gte-rerank` 显著提升 Top-3 相关性，延迟增加约 200–500ms，性价比极高 |
| `model_id` | string | — | 问答阶段指定的大模型 ID（如 `qwen-max`） | 明确指定，避免依赖知识库默认模型（可能变更）；`qwen-plus` 平衡效果与成本 |
| `stream` | bool | `false` | 是否启用 SSE 流式响应（仅 `/v1/knowledge/qa` 和 `/v1/knowledge/query` 支持） | 对终端用户体验敏感时设为 `true`，前端需处理 `data:` 事件 |

⚠️ 注意：
- `model_id` 仅在**问答接口**（`/v1/knowledge/qa`）生效，纯检索接口（`/v1/knowledge/retrieve`）不接受该参数；
- 向量索引更新非实时：文档上传/更新后，通常需 **1–3 分钟** 完成索引构建，期间检索可能命中旧数据；
- 单条切片最大长度为 **2048 tokens**（硬限制，不可配置），超长内容会被截断，建议在知识库创建时合理设置切片策略（如按标题/段落切分）。

## 面向开发者，简洁实用

- **快速验证**：直接使用控制台 [Playground](../../raw/application-user-guide/knowledge-base/playground.md)，上传 PDF/Word，输入问题，5 分钟内验证 RAG 效果。
- **生产集成**：优先使用 `/v1/knowledge/qa`（端到端）而非分步调用，减少网络往返与状态管理；启用 `enable_rerank=true` 是提升准确率最简单有效的操作。
- **调试技巧**：若答案不准，先调用 `/v1/knowledge/retrieve` 查看原始检索结果——检查 `top_k` 是否过小、`query` 是否歧义、知识库是否覆盖该问题；再确认 `model_id` 是否支持长上下文（如 `qwen-max` 支持 32K）。
- **安全合规**：所有知识库数据默认加密存储于租户专属空间，不跨租户共享；RAG 检索过程受平台[默认安全防护](../../raw/application-user-guide/security-guide/section-assets/overview.md)自动保护，无需额外配置。
- **成本优化**：`enable_rerank=true` 和高 `top_k` 均会增加计算开销；免费试用额度仅覆盖基础检索，高并发问答或 rerank 调用计入额外计费项，请监控用量。

## 关联主题页

- [rag api](../api/rag-api.md)
- [knowledge base](../guides/knowledge-base.md)
- [llm application](../guides/llm-application.md)
- [security guide](../guides/security-guide.md)
- [frameworks](../api/frameworks.md)


