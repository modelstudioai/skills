# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是百炼平台的核心能力范式：它通过在大模型推理前动态检索相关知识片段，并将其作为上下文注入提示（prompt），从而显著提升模型回答的准确性、时效性与领域专业性，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼中不是单一接口，而是贯穿数据准备、运行时调用与应用编排的端到端能力链：

- **知识库驱动问答**：在智能体（Agent）或 RAG API 中，用户上传 PDF/DOCX/TXT 等文档 → 经 ParseX 语义切分与向量化 → 构建知识库 → 调用时自动触发检索 → 将 top-K 相关片段注入 LLM 上下文，实现“基于你提供的资料回答”；
- **多模态 RAG**：支持 `document`（文本）、`table`（结构化数据）、`image`（图文问答）、`multimedia`（音视频语义检索）四类知识库，对应不同嵌入模型（如 `qwen3-vl-embedding`）和检索策略；
- **跨渠道统一增强**：网站、企业微信、钉钉等所有渠道集成的 AI 助手，均复用同一套知识库与 RAG 配置，确保问答一致性；
- **Agent 上下文集成**：通过 `context.rag` 字段在 Agent 创建或调用时声明知识库 ID 与 `top_k`，RAG 结果与 Memory、Connector 输出自动合并为统一上下文输入模型；
- **低代码应用构建**：在控制台配置智能体时开启「知识库」开关并设为「必定调用」，即完成 RAG 启用，无需编写检索逻辑。

## 关键参数和配置

| 参数 | 说明 | 可选值/示例 | 所属层级 |
|------|------|-------------|----------|
| `knowledge_base_id` | 知识库唯一标识符 | `"kb-abc123"` | Agent `context.rag` / RAG API 请求体 |
| `top_k` | 检索返回的最相关片段数 | `3`（默认）、`1`–`10` | Agent `context.rag` / RAG API `/search` |
| `rerankModelName` | 重排序模型名称（影响最终排序质量） | `"qwen3-rerank"`（默认）、自定义模型名 | RAG API 创建知识库时指定 |
| `knowledgeType` + `structureType` | 决定知识库类型与处理方式 | `{"knowledgeType": "document", "structureType": "unstructured"}` | RAG API 创建知识库参数 |
| `embeddingModelName` | 文本嵌入模型（影响检索召回质量） | `"text-embedding-v4"`、`"qwen3.7-text-embedding"` | RAG API 创建知识库参数 |
| `enable_context` | 启用上下文注入的全局开关（需模型支持） | `true`（必开） | Agent 创建请求体顶层标志 |

> ⚠️ 注意：  
> - 单次请求注入的总上下文（含 RAG 片段 + Memory + Prompt）token 上限为 **8192**，超长内容将被静默截断；  
> - RAG 检索结果按相关性降序排列，但**不保证时间顺序**，如需保序（如按文档页码），须在业务层对 `context.rag.results` 手动后处理；  
> - “必定调用”模式下，即使用户问题看似无关，系统仍强制执行检索并注入结果——适用于强合规、强依据场景。

## 面向开发者，简洁实用

- ✅ **快速起步**：控制台上传文件 → 创建标准知识库 → 在智能体中开启知识库并设为「必定调用」→ 发布 → 测试。全程无代码。
- ✅ **精细控制**：使用 RAG API 自主管理知识库生命周期（创建/更新/删除）、导入任务、跨库联合检索；通过 `/api/v2/apps/knowledge/chat` 实现流式 RAG 问答。
- ✅ **模型协同**：RAG 与 Qwen3.5-Plus、Qwen-Max、Qwen-Turbo 等模型天然兼容；推荐搭配 `qwen3-rerank` 重排 + `text-embedding-v4` 嵌入，平衡效果与延迟。
- ✅ **调试定位**：所有 RAG 调用返回 `RequestId`，配合控制台「问题反馈」按钮或工单提交，可精准追溯检索片段来源、嵌入质量与重排得分。
- ❌ **避坑提醒**：  
> - 不要混用 `id` / `index_id` 字段名（见 RAG API 文档）；  
> - 扫描版 PDF 必须预处理为文本型 PDF，ParseX 不支持 OCR；  
> - 微信公众号未认证时 5 秒超时限制会导致 RAG 调用失败，务必完成认证。

## 关联主题页

- [rag api](../api/rag-api.md)
- [application use cases](../guides/application-use-cases.md)
- [agent context](../guides/agent-context.md)
- [use cases](../guides/use-cases.md)
- [application support](../guides/application-support.md)


