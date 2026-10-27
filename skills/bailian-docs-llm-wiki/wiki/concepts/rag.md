# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，简称 RAG）是一种将大语言模型（LLM）与外部知识源动态结合的技术范式：在模型生成回答前，先从结构化或非结构化知识库中检索相关片段，并将其作为上下文注入提示（[prompt](../guides/prompt.md)），从而提升回答的准确性、时效性与可追溯性。它有效缓解了大模型幻觉、知识固化和私有数据不可见等问题，是百炼平台构建可信企业级 AI 应用的核心能力。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼平台中并非单一功能模块，而是贯穿数据接入、服务编排与应用集成的横切能力，具体体现为以下三类典型使用方式：

- **知识库原生问答服务**：通过控制台创建「文档搜索」「数据查询」「图片问答」或「音视频搜索」类型的知识库，上传文件后自动完成解析、切片、向量化与索引构建；调用 `/api/v1/indices/knowledge/chat` 接口时，系统自动执行「向量检索 → 重排 → 注入上下文 → 大模型生成」全链路，开发者只需传入 `agent_id` 和用户问题。
  
- **Agent 上下文动态注入**：在调用 `/v1/chat/completions` 标准大模型 API 时，通过 `context.rag` 字段显式指定知识库 ID（`knowledge_base_id`），即可将该知识库中召回的高相关性切片（经默认重排模型精排后）拼接到 system [prompt](../guides/prompt.md) 前置区，实现轻量、灵活的 RAG 增强，无需额外部署检索服务。

- **多渠道 AI 助手集成**：在网站、微信公众号、钉钉等渠道配置百炼智能体应用时，启用「知识库调用」并设置策略（如「必定调用」或「按需调用」），平台会在每次对话请求中自动触发关联知识库的检索流程，并将结果注入到 Agent 的推理上下文中，实现开箱即用的私有知识增强。

> ✅ 提示：所有 RAG 调用均基于业务空间（`workspace_id`）隔离，且依赖统一的 DashScope 鉴权体系（`Authorization: Bearer <API-Key>`）。

## 关键参数和配置

以下参数直接影响 RAG 效果，开发者应在创建知识库、配置 Agent 或发起请求时重点关注：

| 参数名 | 所属层级 | 说明 | 推荐值 | 可调位置 |
|--------|----------|------|--------|-----------|
| `retriever_top_k` / `initial_retrieval_top_k` | 知识库级 | 向量检索阶段初步召回数量 | `50–100`（平衡召回率与重排开销） | 创建知识库时配置（控制台或 `/create_v2` API） |
| `rerankModelName` | 知识库级 | 重排模型名称 | `qwen3-rerank`（文本）、`qwen3-vl-rerank`（多模态） | 知识库配置项，支持自定义 |
| `rerankMinScore` | 知识库级 | 重排后保留结果的最低分数阈值 | `0.3–0.6`（避免低质噪声） | 知识库配置项 |
| `max_retrieved_chunks` | 请求级 | 最终返回给大模型的切片数上限 | `3–5`（默认 `5`；过高易引入干扰） | `/knowledge/chat` 或 `context.rag` 中通过 `top_k` 控制 |
| `similarity_threshold` | 请求/知识库级 | 相似度过滤阈值（0.01–1.0） | `0.4–0.7`（根据语义粒度调整） | 控制台知识检索设置、API 请求体 `kb_search_configs` 或 `context.rag.similarity_threshold` |
| `embedding_model_name` | 知识库级 | 切片向量化所用嵌入模型 | `text-embedding-v4`（默认）、`qwen3-vl-embedding`（图文） | 创建知识库时锁定，不可变更 |

> ⚠️ 注意：`context.rag` 方式不支持自定义重排模型，仅复用知识库配置的 `rerankModelName`；若需多模型混排，应使用 `/knowledge/chat` 或 `/knowledge/search` 等 RAG 专用 API。

## 面向开发者，简洁实用

- **快速验证**：用 CLI 一行命令调试 RAG 效果：  
  `bl knowledge chat --query "公司差旅报销标准是多少？" --agent-id aid-xxxx --debug`  
  加 `--debug` 可查看实际检索到的切片及注入 [prompt](../guides/prompt.md) 的完整上下文。

- **错误排查重点**：  
  - `404 Not Found`：检查 `agent_id` 是否已发布、`knowledge_base_id` 是否存在且状态为 `active`；  
  - `400 Bad Request`：确认 `context.rag.knowledge_base_id` 非空、`similarity_threshold` 在合法范围、未超 context 子模块总数限制（≤3）；  
  - 无召回结果：优先调高 `initial_retrieval_top_k` 并降低 `similarity_threshold`，再检查文档是否成功解析（通过 `/index/files` 查询状态）。

- **性能优化建议**：  
  - 对高频问答场景，将 `RCU`（检索并发单位）设为 ≥50，保障 QPS；  
  - 使用 `qwen3.5-flash` 或 `qwen-turbo` 作为生成模型，配合 `enable_thinking=false` 减少冗余推理；  
  - 多知识库路由时，通过 `kb_search_configs` 显式指定 `index_id` 和权重，避免全库扫描。

- **安全与合规**：所有 RAG 检索结果默认开启「引用标注」（`enable_citation=true`），响应中自动标记来源切片 ID 与页码；敏感字段（如数据库密码、API Key）不会出现在任何检索结果或日志中——前提是 Connector 配置已遵循最小权限原则。

## 关联主题页

- [rag api](../api/rag-api.md)
- [knowledge base](../guides/knowledge-base.md)
- [application use cases](../guides/application-use-cases.md)
- [use cases](../guides/use-cases.md)
- [agent context](../guides/agent-context.md)


