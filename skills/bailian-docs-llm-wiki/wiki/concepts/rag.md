# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态检索相关文档片段，并将其作为上下文注入提示（[prompt](../guides/prompt.md)），显著提升回答的事实准确性、领域专业性与时效性，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台，RAG 不是单一功能，而是贯穿多个核心能力的横切技术底座，开发者可根据需求选择不同抽象层级的集成方式：

- **知识库（Knowledge Base）**：最常用、开箱即用的 RAG 实现。上传私有文档后，平台自动完成解析、分块、向量化与索引构建；调用时自动执行检索 → 重排 → 提示注入 → 生成全流程。适用于客服问答、内部知识助手、合规审查等需强可信度的场景。

- **知识检索（Knowledge Search）与知识问答（Knowledge Chat）**：提供更细粒度的控制权。  
  - `知识检索` 接口返回原始检索结果（含 `score`、`text`、`metadata`），适合需要自定义重排、融合多源结果或构建复杂工作流的开发者；  
  - `知识问答` 接口则封装为端到端智能体，自动调度检索工具并生成回答，支持多轮对话与多模态输入（如图文混合查询），适合快速上线对话类应用。

- **数据连接（Data Connection）**：为 RAG 提供数据源头。平台托管型连接器（如文件、表格）将数据导入后直接用于知识库构建；流处理型连接器（如 MySQL、语雀）则通过内置工具（如 `searchMySQL`）在智能体运行时实时查询，实现“检索增强”中的“实时数据增强”。

- **框架集成（LlamaIndex / Spring AI Alibaba）**：面向希望保留本地开发灵活性的团队。通过 `DashScopeCloudRetriever` 或 `DashScopeDocumentRetriever`，可将百炼云端知识库无缝接入主流开源框架，复用已有 RAG 工程实践，同时享受百炼的向量模型、重排模型与智能解析能力。

- **应用评测（Application Evaluation）**：RAG 效果可被系统化度量。评测体系支持对“检索环节”单独归因（如标记“检索失效”“切片不完整”），帮助定位 RAG 流程瓶颈，驱动针对性优化（如调整分块策略、优化 `score_threshold`）。

## 关键参数和配置

RAG 行为主要由以下参数控制，具体可用性取决于所选接口或组件：

| 参数名 | 所属模块 | 类型 | 默认值 | 说明 |
|--------|----------|------|--------|------|
| `top_k` | 知识库、LlamaIndex | integer | `3`（知识库） / `5`（`DashScopeCloudRetriever`） | 检索返回的最相关文档片段数，取值范围通常为 1–10。增大可提升召回率，但可能引入噪声。 |
| `score_threshold` | 知识库 | float | `0.3` | 向量相似度（余弦）阈值，低于此值的片段被过滤；设为 `0` 表示关闭过滤。适用于抑制低质量匹配。 |
| `enable_hybrid_search` | 知识库 | boolean | `true` | 是否启用关键词 + 向量混合检索，比纯向量检索更鲁棒，尤其对术语、缩写、数字敏感。 |
| `retrieval_mode` | 知识库 | string | `"auto"` | 可选 `"auto"`（混合）、`"vector_only"`、`"keyword_only"`；`"auto"` 在 v2.3.0+ 生效。 |
| `dense_similarity_top_k` | LlamaIndex (`DashScopeCloudRetriever`) | integer | `100` | 向量召回阶段返回的候选节点数，后续可由重排模型精筛。 |
| `rerank_top_n` | LlamaIndex (`DashScopeCloudRetriever`) | integer | `5` | 重排后最终返回给 LLM 的节点数，直接影响上下文长度与生成质量。 |
| `stream` | 知识问答、应用 API | boolean | `true`（强制） | 启用流式响应（SSE），必须显式设置为 `true`；RAG 生成过程天然支持增量输出。 |

> ⚠️ 注意：`knowledge chat` 接口不暴露检索参数（如 `top_k`、`score_threshold`），其检索策略完全由控制台发布的知识服务实例决定；如需精细控制，请使用 `knowledge search` 接口自行组装 RAG 流程。

## 面向开发者，简洁实用

- **快速验证**：优先使用控制台「知识库」模块，上传 3–5 份典型文档 → 创建并发布 → 在「测试问答」面板输入问题，5 分钟内验证 RAG 基础效果。
- **生产集成**：  
  - 简单场景：直接调用 `/v1/knowledge_bases/{kb_id}/query`（知识库 API）或 `/api/v2/apps/knowledge/chat`（知识问答 API）；  
  - 复杂场景：用 `knowledge search` 获取原始结果 → 自行重排/过滤/融合 → 构造 [prompt](../guides/prompt.md) → 调用 `/api/v1/services/aigc/text-generation/generation` 生成答案。  
- **调试技巧**：  
  - 若答案不准，先检查 `score_threshold` 是否过高（导致无结果）或过低（引入噪声）；  
  - 查看返回结果中的 `metadata` 字段（如 `_score_with_weight`），确认高分片段是否真正相关；  
  - 使用应用评测的「BadCase 归因」报告，快速区分问题是出在检索、切片还是生成环节。  
- **性能提示**：`top_k=3` 和 `rerank_top_n=5` 是平衡效果与延迟的常用起点；避免盲目增大 `top_k` 至 10 以上，除非明确需要宽泛召回并自行后处理。

## 关联主题页

- [knowledge base](../guides/knowledge-base.md)
- [knowledge](../api/knowledge.md)
- [data connection overview](../guides/data-connection-overview.md)
- [application evaluation](../guides/application-evaluation.md)
- [application support](../guides/application-support.md)
- [frameworks](../api/frameworks.md)


