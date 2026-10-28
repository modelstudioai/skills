# 检索增强生成（RAG）

检索增强生成（RAG）是一种将大语言模型（LLM）与外部知识源动态结合的技术范式：在模型生成响应前，先根据用户查询从结构化或非结构化知识库中检索相关片段，并将其作为上下文注入提示（[prompt](../guides/prompt.md)），从而提升回答的准确性、时效性与可溯源性。RAG 不依赖模型参数微调，而是通过“检索 + 注入 + 生成”三阶段流水线实现知识实时更新与领域适配。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼平台不是单一功能，而是贯穿数据、模型与应用层的**能力组合模式**，具体体现为以下三类典型使用方式：

- **知识库驱动问答（核心场景）**  
  通过控制台或 RAG API 创建知识库（`knowledge base`），上传 PDF/DOCX/表格/OSS/数据库等多源数据；平台自动完成解析、语义切片、向量化（embedding）与索引构建。调用 `/knowledge_bases/{kb_id}/chat` 或 `/api/v2/apps/knowledge/chat` 接口时，系统自动执行检索（召回 Top-K 切片）→ 重排序（可选）→ 注入 [prompt](../guides/prompt.md) → 调用指定 LLM（如 `qwen3`）生成答案，全程流式返回。

- **Agent 编排增强（高阶场景）**  
  在 Agent 配置中启用 RAG 插件，支持多知识库并行检索、按权重混排、路由策略（如按问题意图分发至文档库/表格库/图像库）。运行时仅需传入 `agent_id` 和 `query`，底层自动协调检索模型（如 `text-embedding-v4`）、重排序模型（如 `qwen3.7-text-rerank`）与生成模型（如 `qwen-max`），开发者无需手动拼接 pipeline。

- **通用应用集成（轻量场景）**  
  在 `application use cases`（如企业微信、网站助手）中，通过 `enable_search=true` 参数一键启用本地知识库检索能力。此时 RAG 作为透明插件嵌入标准 `/v1/chat/completions` 流程：服务端自动触发检索，将结果以 `context` 形式注入 system [prompt](../guides/prompt.md)，再交由 `qwen-plus` 等模型生成回答，对前端 SDK 完全无感。

> ✅ 关键区别：知识库 API 提供细粒度控制（如自定义 `chunk_size`、显式调用 `/search`），适合需要调试检索质量的场景；Agent 和应用用例 API 提供开箱即用的端到端体验，适合快速交付业务价值。

## 关键参数和配置

| 参数 | 所属层级 | 说明 | 推荐值/约束 |
|--------|-----------|------|--------------|
| `retrieval_top_k` | 知识库级 | 检索返回的切片数量（影响召回广度与 prompt 长度） | `3`（问答默认），最大 `10`；超大知识库建议 `5–7` |
| `chunk_size` / `chunk_overlap` | 知识库级 | 切片最大字符数与相邻切片重叠字符数（非 token） | `chunk_size`: `128–2048`（默认 `512`）；`chunk_overlap`: `64`（默认） |
| `enable_rerank` | 知识库级 | 是否启用重排序模型（提升相关性精度，额外计费） | `true`（高精度场景），`false`（低延迟场景） |
| `embeddingModelName` | 知识库创建时 | 指定向量模型（决定语义空间质量） | `text-embedding-v4`（推荐）、`qwen3.7-text-embedding`；多模态场景必须用 `qwen3-vl-embedding` |
| `multimodalEmbeddingModelName` | 多模态知识库 | 仅当知识类型含 `image`/`video` 时必填 | `qwen3-vl-embedding`（支持 `enable_fusion`） |
| `stream` | 运行时接口 | 必须设为 `true`（百炼 RAG 所有问答接口仅支持流式） | `true`（强制） |
| `model_id` | 运行时接口 | 生成模型 ID，**必须与 embedding 模型兼容** | `qwen3` 需搭配 `text-embedding-v4`；`qwen-vl` 需搭配 `qwen3-vl-embedding` |

⚠️ 注意事项：
- 知识库索引更新非实时：文档上传后约 30–120 秒生效，期间检索可能命中旧数据；
- `chunk_size` 是硬约束：即使启用 `semantic` 切分策略，仍以该参数为上限；
- 多模态 RAG 中，`visual_perception_qa` 场景必须显式传 `multimodalEmbeddingModelName`，否则报错；
- 所有 RAG 接口均要求 `Authorization: Bearer <API-Key>` 认证，且 Base URL 需包含业务空间 ID（`{workspace_id}`）。

## 面向开发者，简洁实用

- **快速验证**：用控制台 Playground 上传单个 PDF，5 分钟内完成检索效果调试；
- **生产集成**：优先使用 RAG API 的 “管理-运行”分离架构——用 `/api/v1/indices/rag/index/` 管理知识库，用 `/api/v1/indices/knowledge/search` 或 `/api/v2/apps/knowledge/chat` 调用服务；
- **模型对齐**：务必校验 `embeddingModelName` 与 `model_id` 兼容性（参考 [RAG 简介](../../raw/application-user-guide/knowledge-base.md)）；
- **错误定位**：所有失败响应均含 `request_id`，配合 `error.code`（如 `INVALID_PARAMETER`、`KB_NOT_FOUND`）可精准排查；
- **性能优化**：高并发场景下，复用已发布的 `agent_id`，避免重复初始化；对长文档，优先启用 `enable_rerank` 并调小 `retrieval_top_k` 以平衡精度与延迟。

## 关联主题页

- [rag api](../api/rag-api.md)
- [knowledge base](../guides/knowledge-base.md)
- [vector and sort](../api/vector-and-sort.md)
- [application use cases](../guides/application-use-cases.md)
- [application support](../guides/application-support.md)


