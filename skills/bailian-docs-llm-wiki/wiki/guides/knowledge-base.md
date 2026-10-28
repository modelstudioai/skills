# knowledge base

百炼平台的 knowledge base 是面向企业级场景的 RAG（检索增强生成）服务，支持私有文档的自动解析、切片、向量化与索引构建，并提供低延迟检索与流式大模型问答能力。开发者可通过控制台或 API 快速接入，实现知识驱动的应用构建。该能力深度集成于百炼模型生态，是构建智能客服、内部知识助手等场景的核心基础设施。

## 支持的模型/功能

- **默认支持模型**：Qwen 系列（Qwen2、Qwen2.5、Qwen3）、Qwen-Audio（音频文档）、Qwen-VL（多模态文档），具体以 [RAG 简介](../../raw/application-user-guide/knowledge-base.md) 中“核心概念”章节说明为准。  
- **关键功能**：多路召回（BM25 + 向量混合）、Agentic 多轮检索、流式问答、异步文档处理、细粒度切片策略（按段落、标题、语义边界）。  
- **数据源支持**：本地文件（PDF/DOCX/TXT/MD/CSV/XLSX）、OSS、MySQL、PostgreSQL、飞书、钉钉等，详见 [数据集](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md) 文档。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `chunk_size` | 切片最大字符数（非 token 数） | `512`（默认），范围 `128–2048` | [创建知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md) |
| `chunk_overlap` | 相邻切片重叠字符数 | `64`（默认） | 同上 |
| `retrieval_top_k` | 检索返回的 Top-K 片段数 | `3`（问答默认），最大 `10` | [知识检索](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md) |
| `enable_rerank` | 是否启用重排序（需额外计费） | `true` / `false` | [RAG API 参考](../../raw/application-api-reference/rag-api/rag-api-overview.md) |

> **注意**：`chunk_size` 在 [RAG 简介](../../raw/application-user-guide/knowledge-base.md) 中被描述为“按语义自适应切分”，但实际配置仍以 `chunk_size` + `chunk_overlap` 为硬约束；语义切分仅在 `chunk_strategy=semantic` 时作为辅助优化，不替代参数控制。

## 使用方式

1. **控制台快速验证**：通过 [Playground](../../raw/application-user-guide/knowledge-base/playground.md) 上传单个文档，实时调试检索与问答效果；  
2. **API 集成**：调用 `/knowledge_bases/{kb_id}/retrieve` 进行纯检索，或 `/knowledge_bases/{kb_id}/chat` 发起流式问答（需传入 `model_id`）；  
3. **批量部署**：使用 CLI 或 MCP 协议批量创建知识库与导入文档，参考 [应用集成](../../raw/application-user-guide/knowledge-base/integration/channels.md)。

## 限制和注意事项

- 单知识库最大文档数：10,000 份；单文档最大体积：200 MB（PDF/DOCX）或 50 MB（其他格式）；  
- 向量索引更新非实时：文档上传后约 30–120 秒完成索引就绪，期间检索可能命中旧版本；  
- 流式问答响应中 `answer` 字段为模型生成结果，`retrieved_chunks` 字段为原始切片内容（含 `source_file_name` 和 `page_number`），二者需独立校验；  
- > **注意**：[知识问答](../../raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md) 明确要求 `model_id` 必须与知识库所选 embedding 模型兼容（如 `text-embedding-v3` 对应 `qwen3`），但 [RAG API 参考](../../raw/application-api-reference/rag-api/rag-api-overview.md) 未强调此约束，生产环境务必校验模型对齐。

## 来源文档

- [RAG 简介](../../raw/application-user-guide/knowledge-base.md)


