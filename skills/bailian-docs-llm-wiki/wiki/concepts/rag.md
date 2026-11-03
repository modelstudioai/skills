# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态检索相关上下文片段，并将其注入提示词（Prompt），使模型能在不更新参数的前提下，基于最新、私有、结构化或领域专属知识生成准确、可溯源的回答。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼平台不是单一功能，而是贯穿知识管理、智能体编排与应用集成的核心能力层，具体体现为以下三类协同使用方式：

- **知识库驱动的 RAG 服务**：以 `knowledge base` 为载体，对上传的文档、表格、图片、音视频等[多模态](multi-modal.md)数据进行解析、切片、向量化与索引构建；后续通过 `/api/v1/indices/knowledge/search`（检索）或 `/api/v2/apps/knowledge/chat`（问答）接口触发端到端 RAG 流程——即“用户查询 → Query 改写 → 多路召回（向量+关键词）→ 重排精筛 → 注入上下文 → LLM 生成回答”。该路径适用于需强可控性、高精度引用的客服、法务、产品支持等场景。

- **Agent 上下文注入式 RAG**：在调用 `/v1/chat/completions` 等通用 LLM 接口时，通过 `context.knowledge` 字段显式传入已检索好的文本片段（如从知识库 API 预先获取的 top-3 切片），由平台自动拼接进系统 Prompt。此方式绕过 RAG API 的完整链路，适合开发者已实现自有检索逻辑、或需在混合工具调用（如数据库+知识库）中精细控制上下文注入时机的场景。仅 `qwen-max`、`qwen-plus`、`qwen-turbo` 原生支持该字段。

- **低代码应用中的 RAG 集成**：在 `llm application`（智能体/工作流）或 `application use cases`（微信/钉钉/网站助手）中，通过可视化配置「挂载知识库」并启用「必定调用」策略，即可一键启用 RAG。平台自动完成检索触发、结果过滤、上下文组装与模型调用，开发者只需关注业务 Prompt 设计与渠道适配。这是面向业务快速上线的推荐路径。

> ✅ 提示：所有 RAG 能力均依赖知识库的正确创建与发布（状态为 `deployed`），且知识库类型（`document`/`table`/`image`/`multimedia`）决定了底层使用的嵌入与重排模型。

## 关键参数和配置

以下参数直接影响 RAG 效果，需在知识库创建、Agent 配置或运行时请求中明确设定：

| 参数名 | 所属层级 | 说明 | 典型值 | 注意事项 |
|----------|-----------|------|---------|------------|
| `embeddingModelName` | 知识库创建/更新 | 指定向量化模型，决定语义检索质量 | `text-embedding-v4`（文档）、`qwen3-vl-embedding`（图片） | 创建后不可修改；[多模态](multi-modal.md)知识库必须指定对应 VL 模型 |
| `rerankModelName` | 知识库创建/Agent 配置 | 对初步召回结果重排序，提升 TopK 相关性 | `qwen3-rerank`（文本）、`qwen3-vl-rerank`（[多模态](multi-modal.md)） | 可在 Agent 配置中全局覆盖知识库默认值 |
| `top_k` / `return_k` | 知识检索/问答服务配置 | `top_k`：向量/关键词召回数量（1–100）；`return_k`：最终返回给模型的切片数（1–20） | `top_k=50`, `return_k=5` | 过高易引入噪声，过低可能漏召关键信息 |
| `similarity_threshold` | 知识检索/问答服务配置 | 过滤低于该相似度的切片，单位为浮点数（0.01–1.0） | `0.35` | 值越高越严格，建议从 `0.25` 开始调优 |
| `enable_query_rewrite` | 知识库配置 | 启用后自动补全多轮对话中的省略指代（如将“它”还原为前文实体） | `true` | 对话类应用强烈推荐开启 |
| `context.knowledge` | `/v1/chat/completions` 请求体 | 手动注入的上下文数组，每项含 `content`、`source`、`score` | `[{"content": "订单已发货", "source": "CRM"}]` | 总 token ≤ 当前模型 context window 的 30%；仅限支持模型 |

## 面向开发者，简洁实用

- **快速验证**：用控制台 [Playground](raw/application-user-guide/knowledge-base/playground.md) 直接测试知识库检索效果，观察原始切片与模型回答是否匹配。
- **API 选型**：
  - 要完整 RAG 流程（含改写、混排、路由）→ 用 `/api/v2/apps/knowledge/chat`（SSE 流式）；
  - 只要原始召回结果 → 用 `/api/v1/indices/rag/index/retrieve`（单库）或 `/api/v1/indices/knowledge/search`（多库联合）；
  - 已有自研检索器或需混合其他上下文 → 用 `/v1/chat/completions` + `context.knowledge`。
- **调试技巧**：
  - 在知识问答响应中检查 `retrieved_chunks` 字段，确认召回内容是否相关；
  - 若回答空泛或幻觉，优先调低 `similarity_threshold` 或增大 `top_k`；
  - 若响应超时，检查知识库是否 `deployed`、`agent_id` 是否有效、`stream: true` 是否设置（问答接口强制要求）。
- **避坑提醒**：
  - 知识库 ID 在不同 API 中命名不一致（`pipelineId`/`id`/`index_id`），务必对照文档；
  - `lite_document_qa` 场景强制 `sinkType: BUILT_IN`，不可自定义输出；
  - `visual_document_qa` 已下线，新项目请用 `basic_document_qa` 或 `multimedia` 类型。

## 关联主题页

- [rag api](../api/rag-api.md)
- [knowledge base](../guides/knowledge-base.md)
- [application use cases](../guides/application-use-cases.md)
- [agent context](../guides/agent-context.md)
- [llm application](../guides/llm-application.md)


