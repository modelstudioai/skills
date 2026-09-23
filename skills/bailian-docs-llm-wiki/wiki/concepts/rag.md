# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，简称 RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态检索相关上下文片段，并将其作为提示的一部分输入模型，从而显著提升回答的事实准确性、领域专业性和可控性，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，RAG 不是单一功能模块，而是贯穿多个产品层级的**核心增强能力**，其落地形式因使用场景而异：

- **RAG API（专用服务）**：提供开箱即用的端到端问答接口（`/v1/knowledge_bases/{kb_id}/query`），自动完成检索→重排→生成→引用标注全流程。适用于需快速集成私有知识问答能力的业务系统（如客服后台、内部文档助手），无需关心底层模型调度或切片逻辑。

- **知识库（Knowledge Base）**：作为 RAG 的“记忆中枢”，提供多模态数据接入、智能切片、向量化、混合检索（向量+全文）、重排及问答服务。开发者可独立调用检索接口（`/api/v1/indices/rag/index/retrieve`）获取原始切片，也可绑定生成模型构建自定义 RAG 流程。

- **LLM 应用（智能体 / 工作流）**：RAG 以“工具”或“节点”形式深度集成。Agent 2.0 将知识库统一为可自主调用的 MCP 工具；工作流中可通过“知识库检索节点”或“智能体群组节点”显式编排检索步骤，支持多跳、多库联合、条件触发等复杂逻辑。

- **应用集成（AppFlow / 第三方平台）**：通过 AppFlow 将 RAG 增强的智能体一键发布至网站、企业微信、钉钉等渠道；亦可通过 LangChain、LlamaIndex 等框架，利用 `DashScopeCloudRetriever` 等 SDK 在自有代码中调用百炼云端知识库，实现混合云架构。

- **本地化 RAG（进阶部署）**：支持完全本地运行的 RAG 方案（如 `local_rag.zip`），允许开发者使用自定义切分器、本地 embedding 模型（如 GTE-Chinese-Large）和百炼大模型（`qwen-max`/`qwen-plus`）组合，满足高数据主权与强定制性需求。

## 关键参数和配置

RAG 行为由多个层级的关键参数协同控制，开发者需根据场景选择关注点：

| 参数 | 所属层级 | 说明 | 典型取值/默认值 |
|------|----------|------|----------------|
| `knowledge_base_id` / `agent_id` | API & 控制台 | 指定目标知识库或问答服务实例，决定使用的嵌入模型、切片策略与重排模型 | 字符串 ID（必填） |
| `top_k` | RAG API / 知识库 / SDK | 检索返回的最相关文本切片数量 | `1–10`（API 默认 3）；`1–100`（知识库检索服务）；`1–20`（知识库问答服务） |
| `retrieval_strategy` | RAG API | 检索策略：`vector`（纯向量）、`fulltext`（纯关键词）、`hybrid`（默认，两者融合） | `hybrid`（推荐） |
| `similarity_threshold` | 知识库问答服务 | 过滤低质量切片的余弦相似度阈值，低于此值的切片不参与生成 | `0.01–1.0`（默认约 `0.3`） |
| `max_chunk_length` | 知识库创建时 | 切片最大 token 长度，影响召回粒度与上下文完整性 | `10–6000`（默认 `600`） |
| `enable_reranking` | SDK（如 `DashScopeCloudRetriever`） | 是否启用重排模型对初步召回结果进行精排 | `True`（默认） |
| `rerank_top_n` | SDK / 知识库服务 | 重排后保留的最终切片数（通常 ≤ `top_k`） | `5`（SDK 默认） |

> ⚠️ 注意：`model` 参数在 RAG API 中已被废弃，模型由知识库类型隐式绑定；在 LLM 应用或框架集成中，生成模型（如 `qwen-plus`）与嵌入/重排模型（如 `text-embedding-v4`、`qwen3-rerank`）需**分别独立配置**。

## 面向开发者，简洁实用

- **快速验证**：直接使用控制台 [Playground](https://bailian.console.aliyun.com/?tab=app#/playground) 选择知识库，切换“知识问答”模式，输入问题即可实时查看检索片段与生成答案。
- **生产集成**：
  - 简单问答：调用 RAG API `/v1/knowledge_bases/{kb_id}/query`，传入 `query` 和 `top_k` 即可。
  - 灵活编排：使用 `DashScopeCloudRetriever`（LlamaIndex）或 `Spring AI Alibaba` SDK，在代码中组合检索、重排、生成三步逻辑。
  - 多模态扩展：上传图片/音视频至知识库，配合 `qwen3-vl-rerank` 等多模态重排模型，实现跨模态语义检索。
- **调试要点**：
  - 查看响应中的 `retrieved_chunks` 字段，确认检索是否命中关键信息；
  - 若答案不准，优先检查 `similarity_threshold` 是否过严，或尝试增大 `top_k`；
  - 流式响应（`stream=true`）适用于长答案场景，注意处理 SSE 事件流格式。

## 关联主题页

- [rag api](../api/rag-api.md)
- [knowledge base](../guides/knowledge-base.md)
- [llm application](../guides/llm-application.md)
- [start using](../guides/start-using.md)
- [application use cases](../guides/application-use-cases.md)
- [frameworks](../api/frameworks.md)


