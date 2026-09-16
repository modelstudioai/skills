# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，简称 RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态检索相关上下文片段，并将其注入提示词（[prompt](../guides/prompt.md)），使模型在生成回答时能基于最新、私有、领域特定的事实进行推理，从而显著提升回答的准确性、可解释性与可控性。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，RAG 不是单一功能，而是贯穿多个能力模块的横切技术模式，开发者可根据需求选择不同抽象层级的实现方式：

- **知识库（Knowledge Base）**：最完整的 RAG 开箱即用方案。支持文档/图片/音视频等多模态知识索引、混合检索（向量+关键词）、Rerank 排序、多库加权融合，并自动完成“检索→重排序→生成”全链路。适用于构建企业级问答助手、客服知识中枢、培训资料智能检索等场景。
  
- **数据连接（Data Connection）**：轻量级运行时 RAG 扩展机制。支持在 `chat` 请求中动态绑定结构化（SQL 查询）或非结构化（OSS 文件）数据源，将查询结果直接注入模型上下文。适用于需实时关联数据库、动态加载配置或临时注入业务数据的场景，但仅限 Qwen 系列模型且单次请求仅支持 1 个数据源。

- **知识 API（`/knowledge/search` & `/knowledge/chat`）**：面向自定义 RAG 流程的底层能力接口。`search` 接口返回带分数和元信息的原始切片，供开发者自行编排检索逻辑；`chat` 接口则封装了 Agentic 规划、工具调用与流式生成，适合快速构建对话式知识应用。二者均基于已发布的 `agent_id`，模型与策略由控制台统一配置，API 层不暴露模型选择。

- **向量与排序服务（Vector & Rerank）**：RAG 的原子能力底座。开发者可独立调用 `text-embedding-*` 系列模型构建私有向量库，再结合 `qwen3-rerank` 等模型实现高精度重排序。适用于需要完全掌控索引构建、分片策略、混合召回逻辑的高级场景（如多阶段检索、跨模态对齐、自定义打分函数）。

- **应用层 RAG 增强（Application Support）**：在智能体（Agent）或助手（Assistant）应用中，通过配置知识库作为插件式能力，实现“检索结果自动注入提示词→触发模型生成”的无缝集成。支持多知识库并行检索、结果融合与引用溯源，是低代码构建 RAG 应用的推荐路径。

> ✅ **关键提示**：所有 RAG 能力均严格受限于地域——中国站仅支持华北2（北京），国际站仅支持新加坡。跨地域调用将失败。

## 关键参数和配置

RAG 效果高度依赖以下核心参数，建议在控制台或 API 中按需调优：

| 类别 | 参数名 | 说明 | 典型取值/建议 |
|--------|--------|------|----------------|
| **检索控制** | 相似度阈值（`similarity_threshold`） | 过滤低分切片，避免噪声干扰生成。值过高易漏召，过低引入无关内容。 | 初始设 `0.4–0.6`，通过[命中测试](raw/application-user-guide/knowledge-base/rag-optimization.md)验证调整 |
| | 初步向量检索 TopK（`top_k`） | 向量库首轮召回数量，影响召回完整性与 Rerank 开销。 | 默认 `50`；若知识密度高可降至 `20–30`；需高召回时可增至 `80–100` |
| | 最大召回数量（`max_retrieved`） | 最终送入大模型的切片数，直接影响输入 Token 消耗与回答质量。 | 推荐 `3–10`；超过 `15` 易导致模型注意力稀释或超上下文 |
| **知识源控制** | 权重（`weight`） | 多知识库联合检索时，同类型库间的优先级系数（数值越大越靠前）。 | 仅在文档搜索类之间生效；例如：产品手册库 `weight=2`，FAQ 库 `weight=1` |
| | 标签过滤 / Meta 信息 | 通过 `tags` 或 `metadata`（如 `filename`, `date`）实现结构化过滤，提升精准召回。 | 示例：`{"tags": ["2024Q2", "internal"], "metadata": {"category": "policy"}}` |
| **向量与排序** | `instruct`（Rerank） | 自定义排序指令，明确任务目标（如 `"Rank by technical accuracy for engineering docs."`），显著影响打分逻辑。 | 必填推荐项，避免默认行为偏差 |
| | `text_type`（异步向量） | 区分 `query`（用户问题）与 `document`（知识库文本），启用专用编码器提升检索匹配度。 | 对 `text-embedding-async-v2` 等模型必须显式设置 |

## 面向开发者，简洁实用

- **起步最快**：用控制台创建「知识库」→ 上传 PDF/DOCX → 绑定到「智能体应用」或「工作流」节点 → 在提示词中用 `{result}` 引用检索内容。
- **调试必开**：API 调用时添加 `"debug": true`（数据连接）或启用 `stream=True` + 解析 `event: message`（知识问答），查看实际注入的上下文片段与中间步骤。
- **性能优化**：  
  - 减少无效 Token：用 `max_retrieved=5` + `similarity_threshold=0.5` 平衡精度与成本；  
  - 避免超限：检查模型 `max_context_length`，预留 ≥200 token 给系统提示与输出；  
  - 地域锁定：API Endpoint 必须匹配知识库地域（如北京：`bailian.cn-beijing.aliyuncs.com`）。
- **错误排查重点**：  
  - `Agent 未发布` → 控制台检查对应 `agent_id` 是否已在「知识检索服务」或「知识问答服务」页发布；  
  - `400 UnsupportedModel` → 数据连接仅支持 Qwen 系列，确认模型名（如 `qwen3`）；  
  - `429 Too Many Requests` → 默认 25 QPS，实现指数退避重试。
- **计费注意**：RAG 涉及**多项独立计费**：知识库规格费（小时）、向量化 Token、Rerank Token、路由 Token、生成 Token —— 请在控制台「费用中心」按服务类型分别查看。

## 关联主题页

- [knowledge base](../guides/knowledge-base.md)
- [data connection overview](../guides/data-connection-overview.md)
- [knowledge](../api/knowledge.md)
- [application support](../guides/application-support.md)
- [vector and sort](../api/vector-and-sort.md)


