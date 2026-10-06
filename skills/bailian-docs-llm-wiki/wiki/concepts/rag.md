# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）与外部知识源动态结合的技术范式：模型在生成回答前，先从结构化或非结构化知识库中检索相关片段，再将检索结果作为上下文输入模型，从而生成**准确、可溯源、时效性强且不幻觉**的响应。

在百炼平台，RAG 不是单一功能模块，而是贯穿知识管理、模型服务与应用编排的横切能力，其核心实现依托于“知识库 + 检索服务 + 生成模型”的协同链路，并深度集成至 API、智能体（Agent）、框架（如 LlamaIndex）及控制台全栈体验。

## 在百炼平台的不同场景中，这个概念如何使用

- **知识库问答（基础 RAG）**  
  通过创建文档/图片/音视频/数据类知识库，配置向量化与检索策略后，调用 `/api/v2/apps/knowledge/chat` 接口即可触发完整 RAG 流程：Query → 向量召回 → 重排 → 注入上下文 → `qwen3.6-plus` 等模型生成带引用标注的回答。适用于客服知识库、内部文档助手等场景。

- **智能体（Agent）中的 RAG 扩展**  
  在新版 Agent 应用中，通过 `rag_options` 参数显式注入知识库（`pipeline_ids`）、文件（`file_ids`）、标签（`tags`）或元数据过滤条件（`metadata_filter`），使 Agent 在推理过程中自动触发多源检索，实现“边思考、边查证”的增强决策。支持与[长期记忆](memory.md)、工具调用并行执行。

- **框架级集成（LlamaIndex / Spring AI）**  
  使用 `DashScopeCloudRetriever` 或 `DashScopeDocumentRetriever`，开发者可零运维接入百炼云端知识库；配合 `DashScopeEmbedding` 和 `DashScopeRerank`，在本地代码中复用百炼最优向量与重排模型，快速构建符合工程规范的 RAG 应用，无需自建向量数据库。

- **多模态 RAG 场景**  
  对图文混排文档，自动启用 `Qwen-VL` 解析 + `qwen3-vl-rerank` 混排；对音视频内容，先经语音转写+时间戳切片，再以文本形式参与向量检索；对表格数据，绕过嵌入，直接通过 NL2SQL 模型生成 SQL 查询——同一 RAG 架构下，底层适配不同模态的数据语义理解路径。

- **Playground 与 CLI 调试**  
  控制台 Playground 提供可视化 RAG 链路追踪：可查看原始召回切片、重排分数、模型输入上下文及引用高亮；CLI 命令 `bl knowledge search` 和 `bl knowledge chat` 支持一键验证检索质量与生成效果，是开发迭代阶段最轻量的验证入口。

## 关键参数和配置

以下参数直接影响 RAG 效果，建议按场景组合调优：

| 参数 | 作用 | 推荐值（示例） | 配置位置 |
|------|------|----------------|----------|
| `max_chunk_length` | 切片最大 token 数，平衡上下文完整性与召回粒度 | FAQ：256；长报告：1024–2048 | 创建知识库时的索引设置 |
| `top_k`（向量召回） | 初步向量检索返回的切片数 | 20–50（过高增加重排开销，过低易漏召） | 知识库独立配置 或 `rag_options.top_k` |
| `similarity_threshold` | 过滤低相关性切片的余弦相似度阈值 | 0.35–0.65（严格场景选高值） | 知识库独立配置 或 `rag_options.similarity_threshold` |
| `rerank_top_n` | 重排后最终送入 LLM 的切片数 | 3–7（兼顾信息量与上下文长度限制） | 全局检索服务配置 或 `DashScopeCloudRetriever.rerank_top_n` |
| `rerank_model_name` | 重排模型，决定精排质量 | `"qwen3-rerank"`（文本）、`"qwen3-vl-rerank"`（图文） | 创建知识库或更新 Agent 时指定 |
| `embedding_model_name` | 向量模型，影响召回基础质量 | `"text-embedding-v4"`（文档）、`"qwen3-vl-embedding"`（多模态） | 创建知识库时必填 |

> ⚠️ 注意：`top_k` 与 `rerank_top_n` 是两级过滤——前者控制召回广度，后者控制输入精度；二者不可混淆。流式问答中，`rerank_top_n` 还影响首 token 延迟（越小越快）。

## 面向开发者，简洁实用

- **快速验证**：用控制台 Playground 上传一份 PDF，选 `basic_document_qa` 场景，5 分钟内完成端到端 RAG 测试。
- **API 优先**：生产集成首选 `/api/v2/apps/knowledge/chat`（带引用的流式问答）或 `/api/v1/indices/knowledge/search`（纯检索），避免使用已弃用的 `retrieve` 接口。
- **模型选型明确**：  
  - 向量：默认 `text-embedding-v4`（优于 v3），多模态用 `qwen3-vl-embedding`；  
  - 重排：纯文本用 `qwen3-rerank`，图文混排必须用 `qwen3-vl-rerank`；  
  - 生成：问答推荐 `qwen3.6-plus` 或 `qwen3.7-plus`，对延迟敏感可降级为 `qwen3-turbo`。
- **调试技巧**：开启 Playground 的“显示检索详情”开关，或在 API 请求中添加 `debug=true`（部分接口支持），直接查看召回切片、分数、重排顺序与模型 prompt 输入。
- **避坑提示**：  
  - 知识库仅支持华北2（北京）和新加坡地域，跨地域调用会失败；  
  - `agent_id` 必须为已“发布”状态的服务 ID，未发布则返回 404；  
  - 多知识库联合检索时，务必配置全局混排模型（`qwen3-rerank`），否则结果无统一排序。

RAG 的本质是“让模型知道它该知道的”，而非“让它记住一切”。在百炼，你只需聚焦业务知识组织与问题定义，其余——切分、向量化、检索、重排、生成、引用——均由平台闭环保障。

## 关联主题页

- [knowledge base](../guides/knowledge-base.md)
- [rag api](../api/rag-api.md)
- [application call](../api/application-call.md)
- [use cases](../guides/use-cases.md)
- [frameworks](../api/frameworks.md)


