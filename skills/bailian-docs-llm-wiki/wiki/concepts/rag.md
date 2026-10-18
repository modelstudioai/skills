# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将外部知识检索与大语言模型生成能力深度融合的技术范式：系统在生成响应前，先从结构化知识库中实时检索相关片段，并将这些高相关性上下文作为提示的一部分注入模型，从而显著提升回答的事实准确性、领域专业性和时效性。

## 在百炼平台的不同场景中如何使用

RAG 在百炼平台中并非独立功能模块，而是作为 **[agent context](../guides/agent-context.md) 的核心子能力** 和 **[application support](../guides/application-support.md) 的关键增强手段** 被统一集成，主要应用于以下两类典型场景：

- **智能体（Agent）场景**：当 Agent 配置了 `rag.enabled = true` 且指定了 `knowledge_base_id` 时，平台会在每次推理前自动执行多路语义检索（支持向量+关键词混合召回），将 top-k 最相关文档片段（chunk）注入模型上下文。该过程与 Memory、Connector 等其他 context 模块协同工作，共同构成 Agent 的“认知基础”。适用于客服问答、内部知识助手、合规咨询等需强事实依据的任务。

- **通用应用（Application）场景**：通过 Application SDK 或控制台快速接入 RAG 增强能力，无需编写检索逻辑。平台自动完成知识库切片、向量化、索引构建与查询重排序（Cross-Encoder 重打分）。开发者只需上传 PDF/DOCX 等格式文档并启用 RAG 开关，即可在问答接口中获得知识增强的响应。适用于教育内容答疑、产品文档助手、培训材料解读等轻量级知识服务。

> ⚠️ 注意：RAG 不支持在纯 `model experience` 的基础模型调用（如直接调用 `qwen-plus` 的 `/call` 接口）中单独启用；必须通过 Agent 或 Application 封装层触发，以确保检索结果的安全注入与 token 管控。

## 关键参数和配置

RAG 行为由以下参数控制，均需在 `context_config.rag` 对象中显式声明：

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `enabled` | bool | `false` | 是否启用 RAG 检索；设为 `true` 时必须指定 `knowledge_base_id` |
| `knowledge_base_id` | string | — | 已创建的知识库唯一 ID（可在控制台「知识库管理」中获取） |
| `top_k` | integer | `3` | 检索返回的最大 chunk 数量；建议保持 `1–5`，超过 `10` 可能触发截断警告并影响性能 |
| `retrieval_strategy` | string | `"hybrid"` | 检索策略，可选 `"vector"`（纯向量）、`"keyword"`（BM25）、`"hybrid"`（默认，向量+关键词加权融合） |

此外，RAG 的实际效果还受全局上下文约束：
- 总上下文长度由 `context_window_size`（默认 32768）限制，RAG chunks 与 Memory 共享该预算；
- 当总 token 超限时，系统**优先保留 RAG 内容**，按 LRU 策略裁剪最旧 Memory 条目。

## 面向开发者的实用提示

- ✅ **必做**：知识库需提前完成文档上传、解析与向量化（控制台自动完成），未就绪的知识库会导致 RAG 返回空结果；
- ✅ **推荐**：对专业性强、术语密集的文档，上传前进行人工清洗（如删除页眉页脚、合并表格文本），可显著提升检索相关性；
- ❌ **避免**：在单次请求中配置多个 `knowledge_base_id` —— 当前仅支持单知识库检索，多源需求请预先合并知识库；
- 🔍 **调试技巧**：在控制台「Agent 测试窗口」或「Application 测试页」中开启「显示检索详情」开关，可查看实际召回的 chunk 文本及相似度得分，用于优化知识库质量或调整 `top_k`；
- 📦 **文件支持**：仅 `.pdf`（小写后缀）、`.doc`、`.docx` 可被 ParseX 正确解析；`.txt` 文件需转为上述格式再上传，否则无法提取结构化文本。

RAG 是百炼平台实现“准确、可控、可解释”生成的关键基础设施，其价值不在于替代模型，而在于让模型始终基于可信、最新、领域的事实作答。

## 关联主题页

- [agent context](../guides/agent-context.md)
- [application support](../guides/application-support.md)
- [model experience](../guides/model-experience.md)


