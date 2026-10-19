# RAG（检索增强生成）

RAG（Retrieval-Augmented Generation，检索增强生成）是一种将外部知识检索与大语言模型生成能力深度融合的技术范式：在模型响应前，先从结构化或非结构化知识源中实时检索相关片段，并将其作为上下文注入提示（prompt），从而提升回答的准确性、时效性与可溯源性。在百炼平台中，RAG 不是独立模型，而是贯穿知识库构建、向量检索、重排序、过滤及应用集成的一整套工程化能力链。

## 在百炼平台的不同场景中，这个概念如何使用

- **[智能体（Agent）](agent.md)应用调用**：通过 `application call` API 的 `rag_options` 参数启用 RAG 检索，仅限新版智能体（Agent 2.0）支持。平台自动完成知识库匹配、语义检索、结果注入与生成协同，开发者无需手动拼接 prompt 或管理检索逻辑。
  
- **知识库构建与检索**：基于 LlamaIndex 集成流程，使用 `DashScopeParse` 解析文档（PDF/DOCX/TXT 等），通过 `DashScopeCloudIndex` 创建向量化知识库；后续调用 `retriever.retrieve()` 或 `application call` 即可触发端到端 RAG 流程。

- **精细化检索控制**：
  - 使用 `SearchFilters` 对检索结果进行字段级过滤（如按 `department: "AI Platform"` 或 `publish_date > "2024-01-01"`），支持 AND/OR 嵌套逻辑；
  - 结合 `text-rerank` 模型（如 `qwen3-rerank`）对初检结果重排序，显著提升 Top-3 相关性；
  - 多模态 RAG 场景下，可调用 `qwen3-vl-embedding` + `qwen3-vl-rerank` 实现图文混合检索。

- **向量与排序服务协同**：RAG 的底层依赖 `vector and sort` 提供的能力——文本嵌入（`qwen3.7-text-embedding`）、多模态嵌入（`qwen3-vl-embedding`）和重排序（`qwen3-rerank`）。所有服务均支持同步/异步调用，并可通过 DashScope SDK 统一接入。

## 关键参数和配置

| 参数 | 所属模块 | 类型 | 说明 | 示例值 |
|------|----------|------|------|--------|
| `rag_options` | `application call`（DashScope API） | object | 启用并配置 RAG 行为，仅新版智能体支持 | `{"enable": true, "top_k": 5}` |
| `search_filters` | `more` / RAG API | array of object | 结构化过滤条件，支持字段匹配、范围查询、模糊匹配（`like`）等 | `[{"_operator": "OR", "_conditions": [{"status": "published"}, {"tag": {"like": "%faq%"}}]}]` |
| `top_k` | `rag_options` / `rerank` | integer | 检索返回的最相关片段数（默认 3，最大 20） | `5` |
| `instruct` | `qwen3-rerank` / `qwen3-vl-rerank` | string | 显式指定重排序任务意图，影响语义对齐效果 | `"Retrieve the most authoritative answer to the user's question."` |
| `enable_fusion` | `qwen3-vl-embedding` | boolean | 多模态嵌入时是否启用融合向量（单向量表征图文联合语义） | `true` |

> ⚠️ 注意：`rag_options` 仅在 `application call` 中生效；若需自定义 RAG 流程（如分步检索+人工后处理），应直接调用 `vector and sort` 和 `more` 相关接口，而非依赖 `rag_options`。

## 面向开发者，简洁实用

- ✅ **快速上手**：在控制台创建知识库 → 发布新版智能体 → 调用 `application call` 并设置 `rag_options: {"enable": true}`，即启用开箱即用 RAG。
- ✅ **精准控制**：对高敏感业务（如客服知识库），务必配合 `SearchFilters` 限定来源范围，并用 `qwen3-rerank` 替代默认排序。
- ✅ **性能优化**：单次检索建议 `top_k ≤ 10`；大批量文档入库优先使用异步嵌入（`text-embedding-async-v2`）；输入文本超长时，提前切片（chunk）并确保每段 ≤ 8,192 Token（`text-embedding-v4` 限制）。
- ❌ **避坑提示**：
  - `rag_options` 不支持旧版智能体或工作流；
  - `SearchFilters` 在 OpenAPI SDK 与 RAG API 中语法不兼容，不可混用；
  - `text-embedding-v4` 不自动截断超长输入，超限直接报 400 错误；
  - 所有 RAG 相关服务（向量、排序、知识库）均受地域约束，北京地域功能最全，跨地域调用需显式指定 `WorkspaceId`。

## 关联主题页

- [application call](../api/application-call.md)
- [use cases](../guides/use-cases.md)
- [vector and sort](../api/vector-and-sort.md)
- [more](../api/more.md)


