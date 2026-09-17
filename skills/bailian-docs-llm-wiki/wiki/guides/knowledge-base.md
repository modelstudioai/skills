# [knowledge](../api/knowledge.md) base

知识库（Knowledge Base）是百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，支持将私有文档注入模型上下文，实现基于自有数据的精准问答与推理。它通过向量化存储、语义检索与大模型生成三阶段协同工作，适用于客服问答、技术文档助手、内部知识管理等场景。开发者可通过控制台或 API 快速接入，无需训练模型即可提升领域任务效果。

## 支持的模型与功能

- **模型支持**：当前知识库检索与问答功能默认对接 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列模型；`qwen2.5-72b` 等开源模型需通过 [知识库API指南](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-api-guide.md) 手动指定 `model_id` 参数启用。
- **核心功能**：
  - 文档上传与自动切片（支持 PDF、Word、Excel、TXT、Markdown 等格式）
  - 向量索引构建与实时更新（支持增量同步）
  - 多路召回（BM25 + 向量混合检索）、重排序（Rerank）
  - 基于检索结果的问答生成（含引用溯源、答案截断控制）
  - 定时数据同步（依赖 [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base/data-sync-guide.md) 配置）

> **注意**：原始文档中“[知识库效果优化](../../raw/application-user-guide/knowledge-base/rag-optimization.md)”提及可对切片长度手动设为 128 token，但该参数在 v3.2+ 控制台已移除，实际生效值由系统根据文档类型自动优化——请以 [知识库配额与限制](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-specifications.md) 中的最新规格说明为准。

## 关键参数

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `top_k` | integer | `3` | 检索返回的最相关文档片段数（范围 1–10） |
| `score_threshold` | float | `0.0` | 相似度阈值（0.0–1.0），低于此值的片段不参与生成 |
| `enable_rerank` | boolean | `true` | 是否启用重排序模型（仅对 `qwen-plus` 及以上模型生效） |
| `retrieval_mode` | string | `"hybrid"` | 可选 `"vector"` / `"keyword"` / `"hybrid"` |
| `prompt_template` | string | 内置模板 | 自定义生成提示词，需符合 [知识问答](../../raw/application-user-guide/knowledge-base/rag-knowledge-qa.md) 中定义的变量占位规范 |

## 使用方式

1. **控制台流程**：创建知识库 → 上传文件 → 等待状态变为 `active` → 在应用中绑定知识库 ID 并调用 `/v1/chat/completions` 接口（需传 `knowledge_base_id`）  
2. **API 调用**：使用 `/v1/knowledge_bases/{kb_id}/retrieve` 进行纯检索；或在 `/v1/chat/completions` 请求体中嵌入 `"knowledge_base": {"id": "kb-xxx", "top_k": 5}`  
3. **调试建议**：首次部署后务必通过 [知识库日志与监控](../../raw/application-user-guide/knowledge-base/rag-knowledge-base-log-monitoring.md) 查看检索命中率与延迟，避免因分片失败导致召回为空  

## 限制和注意事项

- 单个知识库最大文档数：10,000 份；单文档最大体积：100 MB（PDF/Word）或 50 MB（其他格式）  
- 向量索引构建耗时与文档总 token 数正相关，超 50 万 token 建议分库处理  
- 不支持跨知识库联合检索；若需多源融合，须合并为单一知识库或自行聚合检索结果  
- 删除知识库后，关联的向量索引与元数据**不可恢复**，且已绑定的应用将立即失效  
- 计费按实际调用量（检索次数 + 生成 token）结算，详情见 [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)

## 来源文档

- [知识库（RAG）](../../raw/application-user-guide/knowledge-base.md)


