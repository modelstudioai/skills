# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将外部知识检索与大语言模型（LLM）生成能力深度融合的技术范式。它通过在生成前动态检索相关知识片段，并将其作为上下文注入 LLM 提示中，显著提升模型回答的事实准确性、领域专业性与可追溯性，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼平台不是单一功能，而是贯穿多个能力层的**横切增强机制**，开发者可根据应用形态选择最适合的集成方式：

- **RAG API（纯 RAG 场景）**：面向需完全可控、端到端私有知识问答的场景。开发者调用 `/v1/knowledge/query` 接口，平台自动完成知识库检索（向量+可选重排）→ 拼接上下文 → 调用指定 LLM（如 `qwen-plus`）生成答案 → 返回答案及带来源的参考片段。适用于构建知识库问答机器人、文档智能助手等独立服务。

- **Agent 上下文（RAG + Agent 场景）**：在智能体（Agent）运行时，通过 `context.knowledge_base_ids` 字段声明关联的知识库 ID 列表。RAG 检索作为 Agent 的“实时感知能力”被自动触发——当 Agent 判定需要外部知识时（如用户提问超出记忆范围），平台自动执行检索并注入上下文。支持多知识库协同、与 Memory/Connector 动态组合，适用于复杂业务流程自动化。

- **应用渠道集成（RAG + 渠道场景）**：在网站、微信公众号、企业微信、钉钉等渠道的 AI 助手中，通过百炼控制台“应用配置 → 知识库”一键绑定。RAG 成为应用的默认增强能力，支持“必定调用”“按需调用”策略，且知识更新后只需重新发布应用即可生效。适用于快速落地企业级客服、产品助手等轻量级场景。

- **框架集成（RAG + 开发者自定义场景）**：通过 LlamaIndex 或 Spring AI Alibaba SDK，开发者可复用百炼的云端能力（如 `DashScopeCloudRetriever`、`DashScopeRerank`）或本地能力（如 `DashScopeEmbedding` + `DashScopeJsonNodeParser`），灵活构建混合架构。例如：用百炼向量模型处理中文语义，用自定义切分策略优化技术文档结构，再接入百炼重排模型提升精度。

- **向量与排序服务（RAG 底座能力）**：RAG 的底层依赖由 `/vector` 和 `/rerank` 两类原子服务支撑。开发者可直接调用 `text-embedding-v4` 生成向量、`qwen3.7-text-rerank` 对召回结果重排，或组合使用构建自有检索系统。适用于对延迟、成本、数据主权有强定制需求的场景（如本地部署、合规敏感行业）。

## 关键参数和配置

RAG 行为高度可调，核心参数按使用层级归类如下：

| 参数名 | 所属层级 | 类型 | 说明 | 典型取值 |
|--------|----------|------|------|-----------|
| `top_k` | RAG API / Agent / Frameworks | integer | 检索返回的最相关知识片段数 | `3`（默认）、`5`、`10`（Agent 限 10） |
| `score_threshold` | RAG API | float | 向量相似度阈值（0.0–1.0），低于此值的片段被过滤 | `0.3`（默认），高精度场景可设 `0.5` |
| `enable_rerank` | RAG API / Frameworks | boolean | 是否启用 Cross-Encoder 重排序（显著提升相关性，增加 300–800ms 延迟） | `false`（默认）、`true` |
| `knowledge_base_ids` | Agent Context | string[] | 指定参与检索的知识库 ID 列表（最多 5 个） | `["kb-abc", "kb-def"]` |
| `dense_similarity_top_k` | Frameworks (`DashScopeCloudRetriever`) | integer | 向量检索召回数（重排前） | `100`（默认） |
| `rerank_top_n` | Frameworks (`DashScopeCloudRetriever`) | integer | 重排后最终返回给 LLM 的片段数 | `5`（默认） |
| `chunk_size` / `overlap_size` | Frameworks (`DashScopeJsonNodeParser`) | integer | 文档切分块大小（字数）与重叠长度 | `500` / `100`（中文推荐） |

> ⚠️ 注意：`score_threshold` 的实际效果受向量索引类型（HNSW/IVF）影响；`top_k` 在 Agent 中硬限制为 10，以适配模型 context window（约 4096 token）；所有参数均支持运行时传入，优先级：API 请求体 > Agent 调用时 `context` > Agent 全局配置。

## 面向开发者，简洁实用

- **快速验证**：首次集成务必加 `?debug=true` 参数（如 `/v1/knowledge/query?debug=true`），查看 `retrieved_chunks` 输出，确认切片质量、相关性与元数据是否符合预期。
- **性能权衡**：启用 `enable_rerank` 可提升准确率 15–30%，但延迟增加明显；高并发场景建议先关闭重排，用 `top_k=5` + `score_threshold=0.4` 平衡效果与吞吐。
- **知识更新**：RAG 效果依赖知识新鲜度。文档上传后需等待 `sync_job` 状态为 `succeeded`；应用侧需**重新发布**才能加载新知识（渠道集成场景易遗漏）。
- **格式兼容**：PDF 需非扫描版（否则解析失败）；DOCX 表格可能错乱；推荐优先使用 `.txt` 或 `.md` 格式保障解析稳定性。
- **调试链路**：RAG 故障常源于三环节之一：① 文档未成功同步（查 `/v1/sync_jobs`）；② 检索无结果（调 `debug=true` 看 `retrieved_chunks` 是否为空）；③ LLM 未正确使用上下文（检查 `answer` 是否引用 `references` 中内容）。

## 关联主题页

- [rag api](../api/rag-api.md)
- [agent context](../guides/agent-context.md)
- [application use cases](../guides/application-use-cases.md)
- [frameworks](../api/frameworks.md)
- [vector and sort](../api/vector-and-sort.md)


