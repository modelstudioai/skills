# knowledge base

知识库（Knowledge Base）是百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于将私有文档数据注入大模型推理流程，提升问答准确性与领域适配性。它支持结构化/非结构化文档的上传、切片、向量化与检索，并可与多种大模型协同完成问答、摘要等任务。知识库功能通过控制台和 API 两种方式接入，适用于企业级知识管理与智能客服等场景。

## 支持的模型与功能

- **支持模型**：所有百炼平台已接入的文本生成类大模型（如 Qwen 系列、Baichuan、GLM 等）均可作为知识库的“生成端”；嵌入模型默认使用 `text-embedding-v1`，暂不支持用户自定义替换（参见 [知识库（RAG）](../../raw/application-user-guide/knowledge-base.md)）。
- **核心功能**：
  - 文档上传与自动解析（支持 PDF、Word、Excel、TXT、Markdown 等格式）
  - 基于语义的向量检索（支持关键词+向量混合检索）
  - 检索结果重排序（RRF）、上下文截断与 [prompt](prompt.md) 自动拼接
  - 知识问答（QA）、知识检索（retrieval-only）、知识摘要等调用模式

## 关键参数

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `top_k` | int | 检索返回的最相关文档片段数 | `3` |
| `score_threshold` | float | 检索相似度阈值（0.0–1.0），低于此值的片段被过滤 | `0.3` |
| `enable_rerank` | bool | 是否启用重排序（需额外计费） | `false` |
| `retrieval_mode` | string | 取值 `"vector"` / `"keyword"` / `"hybrid"` | `"hybrid"` |

> **注意**：`score_threshold` 的实际生效逻辑依赖于所选嵌入模型的归一化方式；当前 `text-embedding-v1` 输出为余弦相似度，但部分旧版文档误标为点积结果（参见 [知识库（RAG）](../../raw/application-user-guide/knowledge-base.md) 中的 API 指南章节，该描述已过时，请以 [知识库API指南](../../raw/application-user-guide/knowledge-base.md) 实际响应字段为准）。

## 使用方式

1. **控制台方式**：在 Model Studio → 知识库模块中创建知识库，上传文件并触发构建；构建完成后，可在“测试”页直接输入问题验证效果。
2. **API 方式**：
   - 先调用 `/knowledge_bases/{kb_id}/files` 上传并解析文档；
   - 再调用 `/chat/completions` 或 `/knowledge_bases/{kb_id}/retrieve`，传入 `knowledge_base_id` 和上述关键参数；
   - 完整请求示例与错误码详见 [知识库API指南](../../raw/application-user-guide/knowledge-base.md)。

## 限制和注意事项

- 单个知识库最大文档数：50,000 份；单文档最大体积：100 MB（PDF/Word）或 50 MB（其他格式）；
- 向量索引构建耗时与文档总 token 数正相关，超 100 万 token 建议分批上传；
- 知识库不支持实时流式更新：新增/修改文档后需手动触发“同步索引”或等待定时同步（默认每 24 小时一次，详情见 [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base.md)）；
- 检索结果中若含敏感信息（如身份证号、手机号），知识库本身**不提供脱敏能力**，需在应用层自行处理。

## 来源文档

- [知识库（RAG）](../../raw/application-user-guide/knowledge-base.md)


