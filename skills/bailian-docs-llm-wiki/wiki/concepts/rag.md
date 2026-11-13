# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，简称 RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态检索相关知识片段，并将其作为上下文注入提示（prompt），显著提升回答的事实准确性、领域专业性和可追溯性，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼平台中不是单一功能模块，而是贯穿知识管理、智能体构建与多端集成的核心架构范式，具体体现为以下三类典型用法：

- **知识库驱动的问答应用**：通过 RAG API 创建结构化知识库（支持 `document`/`table`/`image`/`multimedia` 四类场景），上传 PDF/DOCX/XLSX 等文件后自动完成解析、切片、向量化与索引。调用时，系统并行检索多个知识库，按配置策略（如相似度阈值、权重、重排序）融合 topN 片段，注入 LLM 生成上下文。
  
- **智能体（Agent）的上下文增强**：在 Agent 配置中启用 `knowledge_base_ids`，即可将 RAG 检索结果作为 `agent context` 的一部分。该机制与 Memory、Connector 协同工作，使 Agent 在对话中既能调用私有知识，又能保持会话连贯性与外部系统交互能力。

- **多渠道 AI 助手统一底座**：网站悬浮窗、微信公众号、企业微信、钉钉等所有渠道集成方案均基于 RAG 架构。开发者只需一次构建知识库与 Prompt，即可通过 AppFlow 绑定至不同渠道，实现“一套知识、多端复用”，大幅降低运维成本。

> ✅ 提示：RAG 不是黑盒服务——你始终可控：从文档切片粒度、嵌入/重排序模型选型，到检索是否强制触发（`必定调用`/`按需调用`/`不调用`）、召回数量与相似度阈值，均可显式配置。

## 关键参数和配置

以下为开发者最常调整、直接影响 RAG 效果的核心参数（按作用域分层）：

| 作用域 | 参数名 | 类型 | 说明 | 示例值 |
|--------|--------|------|------|--------|
| **知识库级** | `embeddingModelName` | string | 文本嵌入模型，决定向量质量 | `"text-embedding-v4"` |
| | `multimodalEmbeddingModelName` | string | 图文混合嵌入模型（仅 `image`/`multimedia` 场景） | `"qwen3-vl-embedding"` |
| | `rerankModelName` | string | 重排序模型，优化初检结果顺序 | `"qwen3-rerank"` |
| | `rerankTopN` | integer | 重排序后保留的 topN 片段数 | `5` |
| | `rerankMinScore` | float | 重排序最低得分阈值（过滤低质片段） | `0.3` |
| **Agent / 应用级** | `knowledge_base_ids` | string[] | 关联的知识库 ID 列表（最多 5 个） | `["kb-abc123", "kb-def456"]` |
| | `retrieval_strategy` | string | 检索触发策略 | `"always"`（必定调用）、`"on_demand"`（按需）、`"never"`（不调用） |
| | `retrieval_top_k` | integer | 单知识库召回片段数 | `3` |
| | `retrieval_similarity_threshold` | float | 相似度阈值（0.0–1.0），低于此值的片段被丢弃 | `0.5` |
| | `retrieval_weight` | float | 多知识库融合时的相对权重（用于加权打分） | `1.0` |

⚠️ 注意：  
- 所有参数均区分大小写，且 `snake_case` 与 `camelCase` 命名严格对应接口（如 RAG API 中知识库 ID 字段为 `id`，而文档删除接口为 `index_id`）；  
- 时间戳必须为**秒级 Unix 时间戳**（字符串或整数），非毫秒；  
- 文件大小参数（如 `sizeBytes`）必须传**字符串**（如 `"1048576"`），传数字将导致失败。

## 面向开发者，简洁实用

- **快速起步**：优先使用控制台「标准版知识库」+ `Qwen3.5-Plus` 模型 + `必定调用` 策略，5 分钟内完成首个 RAG 应用；  
- **效果调优三步法**：① 检查切片质量（是否过长/过短？是否跨语义断句？）→ ② 调整 `rerankTopN` 与 `rerankMinScore` 平衡召回率与精度 → ③ 在 Prompt 中明确指令（如“请严格依据以下引用内容作答，并标注来源”）；  
- **避坑清单**：  
  - ❌ 不要上传 >100 MB 或 >1000 页的单文档（Embedding API 易超时）；  
  - ❌ 不要混用 `千问-Plus`（旧别名）与 `Qwen3.5-Plus`（当前标准 ID）；  
  - ❌ 不要在前端直接调用 RAG API（需通过后端代理鉴权，避免泄露 API Key）；  
  - ✅ 推荐开启 `enable_citation`（Agent 配置）以自动返回引用来源，提升可信度。  

RAG 是百炼平台“让大模型真正懂业务”的关键杠杆——你提供知识，平台负责高效检索与可信生成。

## 关联主题页

- [rag api](../api/rag-api.md)
- [application use cases](../guides/application-use-cases.md)
- [application support](../guides/application-support.md)
- [use cases](../guides/use-cases.md)
- [agent context](../guides/agent-context.md)


