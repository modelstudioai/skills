# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在生成前动态检索相关上下文片段，并将其作为提示（[prompt](../guides/prompt.md)）的一部分输入模型，从而显著提升回答的事实准确性、领域专业性和时效性，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台，RAG 不是独立功能，而是贯穿多个核心能力的**基础增强机制**，具体体现为以下三类典型应用路径：

- **知识库问答服务（云上 RAG）**：以「知识库」为统一载体，支持上传 PDF/DOCX/MD/XLSX 等格式文档，经自动解析、智能切片、[向量化](embedding.md)（默认 `text-embedding-v4`）后构建可检索索引；用户提问时，系统执行混合检索（向量 + 关键词）、可选重排（`qwen3-rerank`），再将 TopK 切片注入 LLM（如 `qwen3.6-plus`）生成带引用来源的回答。适用于客服知识库、产品文档助手等开箱即用场景。

- **智能体应用（Agent + RAG）**：在「应用管理」中创建的智能体（Agent）可绑定一个或多个知识库，并配置为「必定调用」。此时 RAG 成为 Agent 的隐式工具链环节——无需编写代码，即可让大模型在多轮对话中自动检索私域知识并融合生成回复，广泛用于企业微信/钉钉/网站嵌入的 AI 助手。

- **本地化 RAG 集成（开发者自控 RAG）**：通过 `DashScopeCloudIndex` 或 `DashScopeParse` SDK，开发者可在自有服务中构建端到端 RAG 流程：自主控制文档解析、切片策略、嵌入模型（如 `GTE-Chinese-Large`）、向量存储及检索逻辑，再调用百炼 API 进行生成。适合对数据主权、延迟、定制化有强要求的生产系统。

> ✅ 提示：所有 RAG 调用均返回结构化结果，包含 `answer`（生成内容）和 `references`（来源切片 ID、高亮文本、原始文档名），便于前端渲染引用标记与溯源审计。

## 关键参数和配置

RAG 效果高度依赖以下可调参数，按作用层分类如下：

| 层级 | 参数名 | 类型 | 说明 | 典型取值 | 可修改性 |
|------|--------|------|------|-----------|------------|
| **检索层** | `top_k` | integer | 检索返回给 LLM 的最相关切片数量 | `3`（默认）、`5`、`10` | ✅ 控制台/Playground/API 均可设 |
| | `similarity_threshold` | float | 过滤低于该相似度的切片（0.01–1.0） | `0.3`（推荐）、`0.5`（严格） | ✅ 同上 |
| | `enable_rerank` | boolean | 是否启用重排模型精排（提升相关性，增加延迟） | `false`（默认）、`true` | ✅ API 中显式传参 |
| **切片层** | `chunk_size` | integer | 单切片最大 token 数（影响召回粒度） | `600`（默认）、`1000` | ❌ 创建知识库时设定，不可更改 |
| | `chunk_strategy` | string | 切片方式：`auto`（智能）、`by_title`（Markdown 标题）、`by_page` 等 | `auto` | ❌ 同上 |
| **生成层** | `model` | string | 指定生成模型（覆盖知识库默认模型） | `qwen3.6-plus`, `qwen-max` | ✅ API 中指定；控制台可全局配置 |
| | `temperature` | float | 控制生成随机性（0.0–2.0） | `0.1`（生产推荐） | ✅ 仅本地 RAG 方案支持；云上服务默认由模型自身策略控制 |

> ⚠️ 注意：`top_k` 和 `similarity_threshold` 是调优 RAG 效果的两个最常用参数——增大 `top_k` 可提升信息覆盖度但可能引入噪声；提高 `similarity_threshold` 可过滤低质片段但可能导致召回不足。建议从 `(top_k=5, threshold=0.3)` 开始，在 Playground 中对比测试。

## 面向开发者，简洁实用

- **快速验证**：直接进入 [知识库 Playground](https://dashscope.console.aliyun.com/knowledge-base/playground)，选择知识库 → 输入问题 → 实时查看检索切片高亮与生成答案，5 分钟完成效果评估。
- **API 集成**：调用 `/v1/knowledge/query` 接口（同步）或 `/api/v2/apps/knowledge/chat`（流式），只需传 `knowledge_id` 和 `query`，其他参数均可省略使用默认值。
- **错误排查**：若返回空结果或无关回答，优先检查：
  - 文档是否已完成同步（状态为 `completed`）；
  - `similarity_threshold` 是否过高导致无切片通过；
  - 查询语句是否含模糊词（如“那个东西”），建议开启 `Query 改写`（控制台开启或 API 传 `rewrite_query=true`）。
- **性能提示**：启用 `enable_rerank=true` 可提升 Top3 结果准确率约 20%，但平均延迟增加 300–500ms；高并发场景建议权衡精度与吞吐。

RAG 是百炼平台连接私域知识与大模型能力的核心桥梁。掌握其参数含义与调试路径，即可高效构建可信、可控、可解释的企业级 AI 应用。

## 关联主题页

- [knowledge base](../guides/knowledge-base.md)
- [rag api](../api/rag-api.md)
- [use cases](../guides/use-cases.md)
- [application use cases](../guides/application-use-cases.md)
- [application support](../guides/application-support.md)


