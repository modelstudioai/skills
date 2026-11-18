# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，简称 RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态检索相关文档片段，并将其作为上下文注入 prompt，使模型能在不更新参数的前提下，准确、可信地回答领域特定、时效性强或事实敏感的问题。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼平台中并非单一功能模块，而是贯穿多个技术栈的**横切增强机制**，根据使用方式和控制粒度分为三类典型路径：

- **RAG API（服务化知识增强）**：面向需要自主构建知识应用的开发者。通过 `/api/v1/indices/rag/index/*` 系列接口管理知识库（支持 `document`/`table`/`image`/`multimedia` 多模态类型），自定义嵌入模型（如 `text-embedding-v4`）与重排模型（如 `qwen3-rerank`），再通过 `/api/v1/indices/rag/knowledge/search` 或 `/knowledge/chat` 接口完成端到端检索+生成。适用于需精细控制切片策略（`chunkMode: h1`/`length`/`regex`）、混排逻辑或对接自有数据管道的场景。

- **Agent Context（智能体上下文注入）**：面向调用 `/v1/chat/completions` 的开发者。只需在请求体中声明 `context_config.rag.enabled = true` 并指定 `knowledge_base_id`，平台即自动完成检索、片段筛选（默认 top-3）、上下文拼接与 token 截断（总上下文上限 8192 tokens）。该方式轻量、统一，且与 Memory、Connector 协同工作，是构建对话式 AI 助手的推荐路径。注意：仅 `qwen-max`、`qwen-plus`、`qwen-turbo`（v202408+）原生支持完整 RAG 上下文注入。

- **应用级 RAG（低代码集成）**：面向业务人员或前端集成开发者。在百炼控制台创建「智能体应用」后，在配置页开启「知识库」开关，选择已创建的知识库并设置调用策略（`必定调用` 或 `按需调用`），发布后即可通过 AppFlow 快速接入网站、微信公众号、企业微信、钉钉等渠道。此方式无需写代码，但检索参数（如召回数、相似度阈值）不可调，适合快速上线标准客服问答场景。

> ⚠️ 共同约束：所有路径均要求知识库已成功创建并完成数据导入（支持 `.pdf`/`.docx`/`.xlsx`/`.png` 等格式，单文件 ≤ 100 MB 或 1000 页）；检索内容计入模型输入 token，影响计费与上下文长度。

## 关键参数和配置

| 参数 | 所属路径 | 类型 | 说明 | 示例值 |
|------|----------|------|------|--------|
| `knowledge_base_id` | Agent Context / 应用级 | string | 知识库唯一标识，控制台创建后获得 | `kb-abc123xyz` |
| `embeddingModelName` | RAG API | string | 文本嵌入模型，决定向量表征质量 | `text-embedding-v4` |
| `rerankModelName` | RAG API | string | 重排模型，用于对初检结果精排序 | `qwen3-rerank` |
| `chunkMode` | RAG API | string | 文档切片策略，影响检索粒度与精度 | `h2`, `length`, `regex` |
| `context_config.rag.enabled` | Agent Context | boolean | 启用 RAG 上下文注入开关 | `true` |
| `context_config.rag.knowledge_base_id` | Agent Context | string | 同上，但必须显式传入 | `kb-abc123xyz` |
| `sinkType` | RAG API（部分场景） | string | 知识库输出类型，`BUILT_IN` 表示使用平台内置向量库 | `BUILT_IN` |

> 💡 提示：  
> - RAG API 中 `pipelineId`（即知识库 ID）在不同接口中字段名不一致（`createIndex` 返回 `data.pipelineId`，`updateIndex` 请求体用 `id`，`deleteIndex` 用 `index_id`），调用时请以接口文档为准；  
> - Agent Context 不支持流式响应（`stream: true`）中动态更新 `context_config`，配置必须在首次请求时固定；  
> - 所有路径均不支持运行时修改嵌入模型——模型绑定发生在知识库创建阶段，变更需重建知识库。

## 面向开发者，简洁实用

- ✅ **首选 Agent Context**：若你使用 `/v1/chat/completions` 调用 Qwen 系列模型，优先启用 `context_config.rag` —— 5 行 JSON 配置即可获得生产级 RAG 能力，无需管理向量库、切片或重排逻辑。  
- ✅ **选 RAG API 当你需要**：定制切片规则（如按标题层级 `h3` 分段）、混合多知识源（文档+表格+图片）、或集成自有 embedding/re-rank 模型。  
- ✅ **避坑提醒**：  
> - 知识库未发布 → Agent Context 和应用级 RAG 均无法生效；  
> - `knowledge_base_id` 错误或权限不足 → 返回 `InvalidParameter` 或 `Forbidden`；  
> - 检索无结果 → 模型仍会生成回答，但上下文为空，建议在业务层检查返回的 `retrieved_chunks` 字段（RAG API）或 `context` 字段（Agent Context 响应头中 `X-Bailian-Context-Info`）做兜底处理。  

RAG 是百炼平台实现“大模型 + 企业知识”落地的核心杠杆。从 API 到 Agent 再到应用，选择匹配你工程成熟度的路径，让知识真正驱动生成。

## 关联主题页

- [rag api](../api/rag-api.md)
- [agent context](../guides/agent-context.md)
- [application use cases](../guides/application-use-cases.md)
- [agent legacy](../guides/agent-legacy.md)
- [use cases](../guides/use-cases.md)


