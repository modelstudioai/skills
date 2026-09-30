# knowledge base

百炼平台的知识库（Knowledge Base）是面向企业级 RAG 应用的核心基础设施，支持私有文档的自动解析、切片、向量化与索引，并提供多路召回检索与大模型驱动的流式问答能力。它可通过控制台或 API 快速接入结构化/非结构化数据源，实现知识服务与业务系统的深度集成。该能力在 [RAG 简介](../../raw/application-user-guide/knowledge-base.md) 中被定义为“企业级知识库与检索服务”。

## 支持的模型/功能

- **内置模型支持**：知识库默认使用百炼平台托管的向量模型（如 `text-embedding-v1`）完成向量化；问答阶段可自由指定任意已开通的 LLM（如 `qwen-max`、`qwen-plus`），需确保模型具备 `rag` 能力标识。
- **核心功能**：
  - 多源数据接入（文件上传、MySQL、OSS、表格等），详见 [数据集](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md)；
  - 自动解析（PDF/Word/Excel/PPT/TXT/Markdown 等格式）与语义切片（支持按段落、标题、固定 token 长度等策略）；
  - 多路召回（BM25 + 向量混合检索）、Agentic 多轮重写与重检；
  - 流式问答（SSE 响应）、引用溯源（返回匹配切片 ID 与原文片段）；
  - 全生命周期管理（知识库创建、文档增删、切片状态查询、索引重建）。

> **注意**：部分旧版文档提及“仅支持 qwen-turbo 用于问答”，该描述已过时；当前所有具备 `rag` 能力的模型均可用于知识问答，以 [RAG API 参考](../../raw/application-api-reference/rag-api/rag-api-overview.md) 中 `qa` 接口的 `model_id` 参数允许值为准。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `knowledge_base_id` | 知识库唯一标识符，创建后生成 | `kb-xxx` | [创建知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md) |
| `retrieval_config.top_k` | 单次检索返回的最相关切片数 | `3` | [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md) |
| `retrieval_config.strategy` | 检索策略，支持 `hybrid`（默认）、`vector_only`、`bm25_only` | `"hybrid"` | [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md) |
| `qa_config.stream` | 是否启用流式响应 | `true` | [知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md) |
| `qa_config.model_id` | 指定问答所用大模型 ID | `"qwen-max"` | [RAG API 参考](../../raw/application-api-reference/rag-api/rag-api-overview.md) |

## 使用方式

1. **控制台快速验证**：通过 [Playground](../../raw/application-user-guide/knowledge-base/playground.md) 直接上传文档、执行检索与问答，无需编码；
2. **API 集成**：
   - 创建知识库 → 上传文档 → 等待 `status=active`（索引就绪）；
   - 调用 `/v1/knowledge_bases/{kb_id}/retrieve` 进行检索；
   - 调用 `/v1/knowledge_bases/{kb_id}/qa` 发起问答（支持 `stream=true`）；
3. **高级集成**：通过 MCP 协议对接 Agent 框架，或使用 CLI 批量管理知识库（参见 [应用集成](../../raw/application-user-guide/knowledge-base/integration/channels.md)）。

## 限制和注意事项

- 单个知识库最大文档数：50,000；单文档最大体积：100 MB（PDF/Word 类）或 50 MB（其他格式）；
- 切片后单条文本长度上限：8192 tokens（超出将被截断，不报错）；
- 索引重建期间（如修改切片策略后）知识库不可用于检索/问答；
- 所有上传内容仅存储于用户专属租户空间，不用于模型训练——该隐私承诺在 [RAG 简介](../../raw/application-user-guide/knowledge-base.md) 中明确声明；
- 不支持跨知识库联合检索；如需多源融合，须预先合并为单一知识库或在应用层聚合结果。

## 来源文档

- [RAG 简介](../../raw/application-user-guide/knowledge-base.md)


