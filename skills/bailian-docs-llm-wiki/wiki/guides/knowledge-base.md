# knowledge base

百炼平台的 knowledge base 是面向企业级场景的 RAG（[检索增强生成](../concepts/rag.md)）服务，支持私有文档的自动解析、切片、向量化与索引构建，并提供多路召回检索与流式大模型问答能力。开发者可通过控制台或 API 快速接入结构化/非结构化数据源，将自有知识无缝注入大模型应用。该能力深度集成于百炼平台，与主流大模型（如 Qwen 系列）协同工作，无需自行维护向量数据库或召回 pipeline。

## 支持的模型与功能

- **模型支持**：knowledge base 本身不绑定特定大模型，但检索结果默认送入百炼托管的 `qwen-max`、`qwen-plus` 或 `qwen-turbo` 进行 RAG 问答生成；也可通过 [RAG API 参考](../../raw/application-api-reference/rag-api/rag-api-overview.md) 自定义 LLM 后端。
- **核心功能**：
  - 多源数据接入：支持本地文件上传、OSS、MySQL、Excel/CSV 表格等（详见 [数据集](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md)）；
  - 智能解析与切片：自动识别 PDF/Word/Markdown 等格式的标题层级、表格、代码块，支持按语义段落或固定 token 长度切片；
  - 多路召回：BM25 + 向量相似度 + 关键词增强三路并行检索，支持重排序（rerank）；
  - Agentic 检索：支持多轮上下文感知的迭代检索（见 [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)）；
  - 流式问答：返回结构化检索片段 + 模型生成答案，支持 `stream=true` 参数实现逐 token 输出。

## 关键参数

| 参数 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `top_k` | integer | 检索返回的最相关切片数量 | `3`（默认），最大支持 `10` |
| `retrieval_strategy` | string | 检索策略类型 | `"hybrid"`（默认）、`"vector_only"`、`"bm25_only"` |
| `rerank_model` | string | 重排序模型 ID | `"bge-reranker-v2-m3"`（需知识库启用 rerank） |
| `stream` | boolean | 是否启用流式问答响应 | `true`（仅用于 `/v1/knowledge_base/qa` 接口） |
| `enable_hybrid_search` | boolean | 是否启用混合检索（BM25+向量） | `true`（默认），若设为 `false` 则退化为纯向量检索 |

> **注意**：`enable_hybrid_search` 在 [RAG API 参考](../../raw/application-api-reference/rag-api/rag-api-overview.md) 中已标记为 legacy 参数，新知识库推荐使用 `retrieval_strategy="hybrid"` 替代，旧参数仍兼容但未来版本将移除。

## 使用方式

1. **创建知识库**：在控制台选择「知识库」→「新建」，配置名称、描述、解析策略（如是否保留表格结构）、切片长度（512–2048 token）及嵌入模型（默认 `bge-m3`）；也可调用 [`POST /v1/knowledge_bases`](../../raw/application-api-reference/rag-api/rag-api-overview.md) 创建。
2. **导入数据**：通过控制台上传文件，或调用 `/v1/knowledge_bases/{kb_id}/documents` 接口批量导入；支持增量更新（同名文件会覆盖）。
3. **发起检索或问答**：
   - 检索：`GET /v1/knowledge_bases/{kb_id}/retrieve?query=xxx&top_k=3`
   - 问答：`POST /v1/knowledge_bases/{kb_id}/qa`，请求体含 `query` 和可选 `stream` 字段（见 [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)）。
4. **调试验证**：使用 [Playground](../../raw/application-user-guide/knowledge-base/playground.md) 实时查看检索命中片段、向量相似度分数及问答生成过程。

## 限制和注意事项

- 单个知识库最大文档数：10,000 份；单文档最大体积：100 MB（PDF/Word）或 50 MB（其他格式）；
- 切片后总 token 数超 10M 时，系统自动触发分片索引优化，可能导致首次检索延迟增加（约 1–3 分钟）；
- 嵌入模型 `bge-m3` 支持中英双语，但对小语种（如日、韩、阿拉伯语）效果有限，建议优先使用 [RAG 简介](../../raw/application-user-guide/knowledge-base.md) 中推荐的多语言适配方案；
- 所有上传文档内容将被加密存储于用户专属租户空间，但元数据（如文件名、大小、解析状态）在控制台可见；
- 不支持动态更新嵌入模型或切片策略：修改需重建知识库（删除后重新创建并导入）。

## 来源文档

- [RAG 简介](../../raw/application-user-guide/knowledge-base.md)


