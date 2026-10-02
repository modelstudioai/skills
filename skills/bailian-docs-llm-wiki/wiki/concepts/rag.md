# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态检索相关知识片段，并将其作为上下文注入提示词，显著提升模型回答的事实准确性、领域专业性和私有数据覆盖能力，同时规避模型幻觉与知识过时问题。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼平台不是单一功能，而是贯穿多个核心能力层的**横切增强机制**，开发者可根据应用复杂度和控制粒度需求，在以下场景中按需启用：

- **知识库服务（独立 RAG API）**：最轻量级接入方式。调用 `/v1/knowledge` 接口，传入 `knowledge_base_id` 和 `query`，平台自动完成检索（向量+关键词混合召回）、重排（可选 rerank 模型）、片段拼接与 LLM 生成全流程，适用于问答、摘要等标准化场景。
  
- **LLM Application 工作流（Workflow）**：在可视化编排中，将「知识库」节点作为 AI 节点之一嵌入流程。可与其他节点（如条件判断、多模态生成、API 工具）组合，实现“先检索 → 再决策 → 后生成”的确定性逻辑，例如：用户提问后，先查知识库获取政策条款，再调用 LLM 解析条款适用性，最后生成合规建议。

- **智能体（Agent）**：RAG 以「工具」形式深度集成。在 Agent 2.0 中，知识库与 MCP [插件](plugin.md)统一为可被规划器（Planner）自主调用的工具；在 Agent 1.0 中，则作为预设的固定检索步骤。支持多轮对话中自动维护检索上下文，结合 `Query 改写` 提升模糊查询鲁棒性。

- **高代码应用（Rich Code）**：开发者完全掌控 RAG 链路。可通过 `fastmcp.Client` 调用知识库检索 API，或直接集成 `DashScopeCloudRetriever`（LlamaIndex）/ `DashScopeDocumentRetriever`（Spring AI）等 SDK，自定义切分策略、重排逻辑与上下文组装规则，满足金融、法律等强合规场景需求。

- **框架集成（LlamaIndex / Spring AI）**：面向熟悉开源生态的开发者。使用 `DashScopeCloudIndex` 构建云端托管知识库，或用 `DashScopeEmbedding` + `DashScopeRerank` 搭建本地可控 RAG 流水线，无缝对接现有工程架构。

> ✅ 关键区别：**知识库服务/API 是开箱即用的端到端 RAG；工作流与 Agent 提供编排灵活性；高代码与框架集成则赋予最大定制自由度。**

## 关键参数和配置

RAG 效果高度依赖参数协同，主要分为三类，均支持控制台、API 或 SDK 配置：

| 类别 | 参数名 | 常用值/范围 | 作用说明 |
|--------|---------|--------------|-----------|
| **检索控制** | `top_k`（检索） | 3–10（默认 3） | 控制向量/关键词初检召回数量；值过小易漏关键信息，过大增加噪声与延迟 |
| | `max_retrieved` | 1–20 | 最终送入 LLM 的最大片段数，硬性截断上限 |
| | `similarity_threshold` | 0.01–1.0（默认 0.3） | 过滤低相似度切片，提升答案精准度（值越高越严格） |
| | `enable_query_rewrite` | `true`/`false` | 开启后自动优化用户原始 query（如补全缩写、纠正错字），提升多轮对话检索一致性 |
| **重排增强** | `rerank_model` | `qwen3-rerank`, `gte-rerank-hybrid` | 对初检结果进行语义精排，显著提升 Top-K 相关性；`hybrid` 版本融合稀疏与稠密信号 |
| | `rerank_top_n` | 1–10（默认 5） | 重排后保留的最终片段数 |
| **生成控制** | `temperature` | 0.0–1.0（默认 0.5） | 控制生成随机性；RAG 场景建议设为 0.1–0.3 以保障事实稳定性 |
| | `enable_thinking` | `true`/`false` | 开启后模型显式输出推理链（如“根据知识库第2段…”），便于调试与可信度验证 |

> ⚠️ 注意：`top_k` 与 `max_retrieved` 是两个独立参数——前者影响检索阶段性能，后者决定生成阶段上下文长度。建议 `max_retrieved ≤ top_k`，避免无效截断。

## 面向开发者，简洁实用

- **快速验证**：用控制台 [Knowledge Base Playground](https://dashscope.console.aliyun.com/knowledge-base/playground) 输入问题，实时查看检索切片与生成结果，5 分钟完成效果调优。
- **生产集成**：
  - 简单问答：直接调用 RAG API `/v1/knowledge`，传 `knowledge_base_id` + `query`；
  - 复杂流程：在 Workflow 中拖入「知识库」节点，连接至下游 LLM 节点，配置 `top_k` 和 `similarity_threshold`；
  - 完全可控：Python 中使用 `DashScopeCloudRetriever`（LlamaIndex）或 `DashScopeDocumentRetriever`（Spring AI），代码示例见 [框架文档](../../raw/application-api-reference/frameworks/llamaindex/dashscopecloudindex-and-dashscopecloudretriever.md)。
- **避坑指南**：
  - 切片参数（如 `chunk_size`）在知识库创建后**不可修改**，首次配置务必结合业务文档结构测试；
  - 使用 `agent_id` 调用 RAG API 时，`model` 字段已废弃，模型由 Agent 绑定决定；
  - 多轮对话需显式传递历史 `tool_calls`（见 `/api/v2/apps/knowledge/chat` SSE 流响应格式），否则无法维持上下文连贯性。

## 关联主题页

- [llm application](../guides/llm-application.md)
- [rag api](../api/rag-api.md)
- [knowledge base](../guides/knowledge-base.md)
- [use cases](../guides/use-cases.md)
- [frameworks](../api/frameworks.md)


