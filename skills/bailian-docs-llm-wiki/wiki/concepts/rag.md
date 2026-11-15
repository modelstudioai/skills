# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，简称 RAG）是一种将大语言模型（LLM）与外部知识源动态结合的技术范式：在模型生成响应前，先从结构化或非结构化知识库中检索相关片段，并将检索结果作为上下文注入提示（prompt），从而提升回答的准确性、时效性与可追溯性。该技术有效缓解了大模型幻觉、知识固化和私有数据不可见等问题。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼平台中不是单一功能，而是贯穿多个服务层级的**核心能力底座**，开发者可根据需求选择不同抽象粒度的集成方式：

- **全托管 RAG 应用（推荐新手/业务快速上线）**  
  通过「应用管理」创建智能体应用，上传文档（PDF/DOCX/TXT/CSV 等）并启用知识库，平台自动完成解析、切片、向量化、索引构建与重排。调用时只需配置 `knowledge_call_mode: "always"` 或 `"on_demand"`，无需关心底层流程。适用于网站助手、企微/钉钉客服等标准化渠道集成。

- **API 驱动的 RAG（面向中高级开发者）**  
  使用 RAG API 进行细粒度控制：  
  - 创建多类型知识库（`document`/`table`/`image`/`multimedia`），支持结构化与非结构化混合检索；  
  - 显式指定嵌入模型（`embeddingModelName`）、重排序模型（`rerankModelName`）及最小相似分（`rerankMinScore`）；  
  - 通过 `/api/v1/indices/knowledge/search` 实现跨库语义检索，或通过 `/api/v2/apps/knowledge/chat` 发起带引用溯源的流式问答。

- **Agent 上下文注入（面向复杂对话系统）**  
  在调用 `/v1/chat/completions` 时，通过 `context.rag.knowledge_base_ids` 字段声明需激活的知识库 ID 列表（最多 3 个）。该机制与 Memory、Connector 协同工作，实现“一次请求、多源上下文融合”，但仅在 `stream=false` 模式下生效。

- **框架级深度集成（面向定制化开发）**  
  借助 LlamaIndex 或 Spring AI Alibaba 等框架，复用百炼的 `DashScopeCloudRetriever`（支持向量+文本混合检索、内置重排）、`DashScopeParse`（智能版面解析）和 `DashScopeRerank` 组件。支持本地预处理（如用 `DashScopeJsonNodeParser` 自定义切分）后上传，兼顾灵活性与云端能力。

## 关键参数和配置

以下参数在不同接入路径中高频出现，直接影响 RAG 效果与性能：

| 参数名 | 所属场景 | 说明 | 典型值 | 注意事项 |
|--------|----------|------|--------|-----------|
| `retrieval_top_k` | 应用配置 / Agent Context | 检索召回的 Top-K 片段数 | `1–10`，默认 `3` | 过大会增加 prompt 长度与 token 成本；过小可能遗漏关键信息 |
| `similarity_threshold` | 应用配置 | 相似度过滤阈值（0.0–1.0） | 默认 `0.3` | 值越高越严格，建议结合业务测试调整；低于阈值的片段不参与生成 |
| `knowledge_call_mode` | 应用配置 | 知识库调用策略 | `"always"` / `"on_demand"` / `"never"` | `"on_demand"` 依赖模型判断是否需要查知识，需模型具备强指令理解能力 |
| `embeddingModelName` | RAG API（知识库创建） | 文本嵌入模型名称 | `"text-embedding-v4"` | 影响向量质量，新知识库推荐使用 v4；多模态场景需额外配置 `multimodalEmbeddingModelName` |
| `rerankModelName` | RAG API / DashScopeCloudRetriever | 重排序模型名称 | `"qwen3-rerank"` / `"gte-rerank-hybrid"` | 启用重排可显著提升 Top-3 准确率；需显式设置 `enable_reranking=true` |
| `dense_similarity_top_k` | DashScopeCloudRetriever | 向量检索召回数 | 默认 `100` | 混合检索中与 `sparse_similarity_top_k` 共同决定初检规模 |

> ⚠️ 注意：所有 RAG 调用均依赖已**发布**的资源（知识库、Agent、应用），未发布状态将返回明确错误（如 `Agent.NotPublished`）。调试时请优先检查资源状态与权限绑定。

## 面向开发者，简洁实用

- **起步最快**：用「应用管理」+「数据连接」上传文件 → 启用知识库 → 发布应用 → 接入渠道，5 分钟可上线可用助手。  
- **效果调优三步法**：① 提高 `retrieval_top_k` 观察召回内容完整性；② 调低 `similarity_threshold` 放宽匹配范围；③ 启用 `qwen3-rerank` 重排验证精度提升。  
- **避免踩坑**：  
  - RAG API 中知识库 ID 字段名不统一（`index_id`/`id`/`pipelineId`），务必对照接口文档；  
  - 流式问答（`/knowledge/chat`）必须传 `stream: true`，且 `Accept: text/event-stream`；  
  - `context.rag` 仅在非流式请求中生效，流式场景请改用 RAG API 或应用层 Agent。  
- **进阶建议**：对专业文档（如合同、财报），优先使用 `DashScopeParse` 解析 + `DashScopeJsonNodeParser` 自定义切分（按章节/条款），再构建知识库，比默认切分更可控。

## 关联主题页

- [rag api](../api/rag-api.md)
- [application use cases](../guides/application-use-cases.md)
- [agent context](../guides/agent-context.md)
- [frameworks](../api/frameworks.md)


