# 检索增强生成（RAG）

检索增强生成（RAG）是百炼平台的核心能力之一，指在大模型生成响应前，先从私有知识库中检索与用户问题最相关的文本片段，并将这些片段作为上下文注入模型提示词，从而显著提升回答的准确性、时效性与领域专业性。该机制有效缓解了大模型幻觉、知识过时和私域数据不可见等问题。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼中不是单一接口，而是贯穿知识管理、应用构建与渠道集成的端到端架构：

- **知识库服务**：通过控制台或 RAG API 创建知识库，系统自动完成文档解析（PDF/Word/Excel/TXT/Markdown）、语义切片、双路向量化（稠密向量 + 关键词倒排）与索引构建；支持 `hybrid`（默认）、`vector_only`、`keyword_only` 三种检索策略。
- **智能体（Agent）应用**：RAG 作为 Agent 的可插拔能力，默认启用；配置“必定调用”策略可确保所有用户问题强制触发知识检索，避免模型凭参数化记忆作答。
- **多渠道 AI 助手**：网站、微信公众号、企业微信、钉钉等场景均基于统一 RAG 架构——知识库一次构建，多端复用；AppFlow 连接流自动将用户消息路由至 RAG 检索+LLM 生成流水线。
- **Agent 上下文注入**：RAG 检索结果可作为 `context.type="rag"` 的结构化上下文，通过 `system` 消息注入 `/v1/chat/completions` 请求，供 `qwen-max`/`qwen-plus` 等原生支持模型直接消费。
- **低代码集成**：无需编写向量检索逻辑，开发者只需上传文档、创建知识库、绑定 Agent，即可获得开箱即用的语义问答能力；高级场景可通过 SDK 或 RAG API 自定义切片规则、重排序策略与混合召回。

## 关键参数和配置

| 参数 | 所属层级 | 说明 | 典型值 | 注意事项 |
|------|----------|------|--------|----------|
| `top_k` | 检索层 | 单次检索返回的最相关切片数 | `3`–`5`（推荐），上限 `50` | 数值过大易引入噪声，过小可能遗漏关键信息 |
| `retrieval_strategy` | 检索层 | 召回方式 | `"hybrid"`（默认）、`"vector_only"`、`"keyword_only"` | `hybrid` 同时调用向量与关键词引擎，平衡精度与召回率 |
| `similarity_threshold` | 检索层 | 片段相似度过滤阈值 | `0.6`–`0.8`（提升精准度） | 默认为 `0`（不过滤），设为 `0.7` 可丢弃低置信片段 |
| `embeddingModelName` | 知识库创建 | 文本向量化模型 | `"text-embedding-v4"`、`"qwen3-vl-embedding"`（多模态） | 影响切片表征质量，需与业务语义匹配 |
| `rerankModelName` | 知识库/Agent 级 | 检索后精排模型 | `"qwen3-rerank"` | 对 top_k 候选做二次打分排序，提升最终输入质量 |
| `agent_model` | Agent 配置 | 生成阶段大模型 | `"qwen3.5-plus"`、`"qwen-max"` | 决定回答质量与风格，需与 `context` 兼容 |
| `stream` | 问答接口 | 是否流式返回 | `true`（仅 `/knowledge/chat` 等问答接口支持） | 启用后返回 SSE 流，适合前端实时渲染 |

> ⚠️ 注意：`index_id`（snake_case）用于删除知识库等管理接口，而 `indexId`（camelCase）用于查询切片等运行时接口，传错将返回 `Index.InvalidParameter` 错误。

## 面向开发者，简洁实用

- **快速起步**：控制台 → 「知识库」→「新建」→ 上传文档 → 自动生成索引 → 在「应用」中绑定该知识库并发布 Agent → 调用 `/v1/knowledge_bases/{kb_id}/chat?stream=true` 即可获得流式问答。
- **API 集成**：使用 RAG API 时，务必区分两类接口：
  - **管理类**（如 `/api/v1/indices/rag/index/create_v2`）：需 `workspace_id` + `API-Key`，操作知识库生命周期；
  - **运行类**（如 `/api/v2/apps/knowledge/chat`）：需 `agent_id` + `API-Key`，仅用于已发布 Agent 的推理调用。
- **调试技巧**：
  - 先用 [Playground](https://bailian.console.aliyun.com/?tab=app#/playground) 观察原始检索结果（切片内容、相似度分），再调整 `top_k` 和 `similarity_threshold`；
  - 若回答不准确，检查文档是否加密/PDF 是否为扫描件（需 OCR 预处理），或切片是否过长（建议按段落或 ≤512 token 切分）；
  - 使用 `RequestId` 提交工单时，附上请求时间、`workspace_id`、`agent_id` 和原始 query，便于平台定位日志。
- **生产建议**：
  - 客服类场景：固定 `temperature=0.1` + `top_k=3` + `retrieval_strategy=hybrid`，保障稳定输出；
  - 多知识库并行：无需手动合并，平台自动加权融合各库 top_k 结果；
  - 避免敏感信息：`context.content` 中的 RAG 片段若含密钥等字段，须在注入前由业务侧脱敏。

## 关联主题页

- [rag api](../api/rag-api.md)
- [knowledge base](../guides/knowledge-base.md)
- [application use cases](../guides/application-use-cases.md)
- [application support](../guides/application-support.md)
- [use cases](../guides/use-cases.md)
- [agent context](../guides/agent-context.md)


