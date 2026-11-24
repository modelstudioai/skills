# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，简称 RAG）是一种将大语言模型（LLM）与外部知识源动态结合的技术范式：在模型生成响应前，先从结构化或非结构化知识库中检索相关片段，并将其作为上下文注入提示（prompt），从而提升回答的准确性、时效性与可溯源性。该技术有效缓解了模型幻觉、知识陈旧和领域适配不足等问题，是百炼平台构建可信企业级 AI 应用的核心基础设施。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，RAG 不是一个孤立功能，而是深度融入多个能力层级的横切能力：

- **智能体（Agent）上下文注入**：通过 `agent context` 机制，开发者可在调用 `bl text chat` 或 `bl knowledge chat` 时，显式绑定 Knowledge 库（`context_type: "knowledge"`），实现运行时动态检索。该方式支持多源组合（如 Knowledge + Memory），并受 `max_context_tokens` 控制，确保上下文精炼有效。

- **知识库即服务（Knowledge API）**：RAG 的完整生命周期由 Knowledge API 承载，覆盖知识库创建、文档导入（支持 PDF/Word/Excel/音视频等）、自动切片、[向量嵌入](vector-embedding.md)（默认 `text-embedding-v3`）、语义检索与重排（默认 `qwen3-rerank`）。开发者可通过 REST API 或 CLI（如 `bl knowledge chat`）直接调用，无需自行搭建向量数据库与检索流水线。

- **应用级低代码集成**：在百炼控制台创建的 AI 助手（App）中，RAG 以“知识库”模块形式启用，支持配置调用策略（`必定调用` / `按需调用`）、相似度阈值（0–1）、结果数量（`top_k`）等参数，并与 Prompt 工程、工具调用无缝协同，快速交付网站、企微、钉钉等多端助手。

- **混合部署模式**：支持“本地检索 + 云端生成”架构——开发者在本地执行文档解析与向量检索（如使用 LlamaIndex 或自研检索器），仅将召回片段与用户问题拼接后，通过百炼 `text chat` API 调用 `qwen3-plus` 等模型完成最终生成，满足数据不出域、预处理灵活等合规需求。

- **框架集成支持**：通过 `frameworks` 能力，LlamaIndex 和 Spring AI 可原生接入百炼的 RAG 服务——例如将 `BailianEmbedding` 替换为嵌入组件，`BailianLLM` 作为生成器，自动复用百炼知识库索引与检索逻辑，避免重复建设。

## 关键参数和配置

| 参数 | 说明 | 典型值/约束 | 生效位置 |
|------|------|-------------|----------|
| `--agent-id` / `context.id` | 知识库唯一标识符（`kb_xxx`） | 必填；CLI 中用于 `bl knowledge chat`，API 中为 `id` 或 `indexId` | CLI、REST API、Agent Context |
| `top_k` | 检索返回的最相关片段数 | 默认 3；建议 2–5；过高易引入噪声，过低可能漏关键信息 | Knowledge API `/search`、App 配置页、CLI `--top-k` |
| `similarity_threshold` | 召回片段的最小语义相似度 | 范围 0.0–1.0；生产环境推荐 0.4–0.7；低于阈值则不注入上下文 | App 配置页、Knowledge API `search_filters` |
| `max_context_tokens` | 注入检索结果的最大 token 数 | 默认为模型上下文窗口的 30%，上限 8192；必须 ≤ 模型剩余 prompt 容量 | Agent Context API、CLI `--max-context-tokens` |
| `embedding_model_name` | 知识库使用的嵌入模型 | `text-embedding-v3`（默认）、`qwen3.7-text-embedding`、`qwen3-vl-embedding`（多模态） | Knowledge API `create_v2` 请求体 |
| `rerank_model_name` | 检索后重排序模型 | `qwen3-rerank`（默认）；若遇 `RETRIEVAL_TIMEOUT` 错误，可降级为更轻量模型 | Knowledge API `create_v2` / `update` |

> ⚠️ 注意：`bl text chat` 命令本身不内置 RAG，需配合 `--agent-id`（调用 Knowledge Agent）或显式构造含检索结果的 prompt；而 `bl knowledge chat` 是专为 RAG 封装的快捷命令，自动完成检索+生成两步。

## 面向开发者，简洁实用

- **快速验证**：  
  ```bash
  bl knowledge chat --message "产品保修期多久？" --agent-id kb_abc123 --top-k 3
  ```

- **调试检索质量**：  
  先单独调用检索接口（`POST /api/v1/indices/kb_abc123/search`），检查返回的 `chunks` 内容与 `score`，再决定是否调整 `similarity_threshold` 或更换嵌入模型。

- **避免上下文溢出**：  
  若提示 `context_length_exceeded`，请显式设置 `--max-context-tokens 4096`（或更低），而非依赖默认值。

- **生产环境建议**：  
  - 使用 `qwen3-plus` 或 `qwen3.5-flash` 作为生成模型，平衡效果与延迟；  
  - 知识库启用 `pipelineCommercialType=enterprise` 以获得 Wiki 图谱与合成摘要能力；  
  - 监控 `knowledge.search` QPM（限流 300 QPM），高并发场景添加客户端缓存或异步预检。

- **不推荐做法**：  
  ❌ 将原始文档全文塞入 prompt；  
  ❌ 在非 Qwen 模型上强行启用 Knowledge context（可能被静默忽略）；  
  ❌ 混用不同 embedding 模型与知识库（导致向量空间不匹配）。

## 关联主题页

- [capabilities](../guides/capabilities.md)
- [rag api](../api/rag-api.md)
- [application use cases](../guides/application-use-cases.md)
- [agent context](../guides/agent-context.md)
- [frameworks](../api/frameworks.md)


