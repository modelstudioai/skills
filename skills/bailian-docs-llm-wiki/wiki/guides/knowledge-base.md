# knowledge base

知识库（Knowledge Base）是百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于将私有文档数据注入大模型推理流程，提升问答准确性与领域适配性。它支持结构化/非结构化文档的上传、切片、向量化与语义检索，并可与多种大模型协同完成问答任务。该能力通过 API 和控制台双通道提供，适用于客服问答、技术文档助手、内部知识中枢等场景。

## 支持的模型/功能

- **模型支持**：知识库本身不绑定特定大模型，但需配合百炼平台支持的 LLM 使用（如 Qwen 系列、Qwen2 系列、Qwen3 等），具体兼容性请参考 [知识库（RAG）](../../raw/application-user-guide/knowledge-base.md) 中“知识问答”章节。
- **核心功能**：
  - 文档上传与自动解析（支持 PDF、Word、Excel、PPT、TXT、Markdown 等格式）
  - 自定义分块策略（按段落、标题、固定 token 长度等）
  - 向量索引构建与实时更新（支持增量同步）
  - 多路召回（关键词 + 向量混合检索）
  - 检索结果重排序（RRF 或自定义 score 融合）
  - 问答链路集成（检索 → 提示工程 → LLM 生成 → 引用溯源）

## 关键参数

| 参数 | 说明 | 默认值 | 可调范围 |
|------|------|--------|----------|
| `top_k` | 检索返回的最相关文档片段数 | `3` | `1–10` |
| `score_threshold` | 向量相似度阈值（余弦相似度），低于此值的片段被过滤 | `0.3` | `0.0–1.0` |
| `chunk_size` | 分块时最大 token 数（仅影响新建知识库） | `512` | `128–2048` |
| `chunk_overlap` | 相邻分块重叠 token 数 | `64` | `0–256` |
| `retrieval_mode` | 检索模式：`vector` / `keyword` / `hybrid` | `hybrid` | — |

> **注意**：`chunk_size` 和 `chunk_overlap` 仅在知识库创建时生效，后续不可修改；如需调整，须重建知识库。详见 [知识库（RAG）](../../raw/application-user-guide/knowledge-base.md) 的“知识库效果优化”部分。

## 使用方式

1. **控制台方式**：进入 Model Studio → 知识库 → 创建知识库 → 上传文件 → 配置分块与向量化参数 → 发布；
2. **API 方式**：
   - 调用 `/knowledge_bases` 创建知识库；
   - 调用 `/knowledge_bases/{kb_id}/files` 上传并解析文档；
   - 调用 `/knowledge_bases/{kb_id}/retrieve` 执行检索（支持 `query` + `filter`）；
   - 在 LLM 调用中通过 `retrieval` 字段指定知识库 ID，由平台自动注入上下文（见 [知识库API指南](../../raw/application-user-guide/knowledge-base.md)）；
3. **SDK 支持**：Python SDK `dashscope` v1.17.0+ 提供 `KnowledgeBase` 类封装全流程操作。

## 限制和注意事项

- 单个知识库最大文档数：10,000 份；单文档最大体积：100 MB（PDF/Word 等二进制格式）或 10 MB（纯文本）；
- 向量索引构建耗时与文档总 token 数正相关，超 1M tokens 建议分批上传；
- 检索结果默认不包含原始文件元信息（如页码、标题），需在上传时启用 `enable_metadata_extraction: true`（参见 [知识库（RAG）](../../raw/application-user-guide/knowledge-base.md) “知识检索”章节）；
- 免费试用期知识库不支持定时同步与日志导出，正式环境需开通对应权限；
- 知识库配额受项目级资源包约束，超出后请求将失败，详情见 [知识库配额与限制](../../raw/application-user-guide/knowledge-base.md)。

## 来源文档

- [知识库（RAG）](../../raw/application-user-guide/knowledge-base.md)



