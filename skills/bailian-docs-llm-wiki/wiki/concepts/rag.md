# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，简称 RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态检索相关上下文片段，并将其注入提示（prompt），使模型能在私域知识约束下生成更准确、可溯源、时效性强的回答，有效缓解幻觉、过时和领域泛化不足等问题。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼平台中不是单一功能模块，而是贯穿多个产品层级的**核心增强机制**，支持三种典型集成方式：

- **RAG API 独立服务**：通过 `/api/v1/indices/knowledge/search` 接口执行跨知识库联合检索（支持文本+图片多模态输入），或通过 `/api/v2/apps/knowledge/chat` 发起端到端流式问答（SSE 响应，含规划→工具调用→生成三阶段）。适用于需完全自主控制检索逻辑、结果融合与后处理的开发者。
  
- **Agent 上下文（Agent Context）集成**：在 `/v1/chat/completions` 请求中启用 `context.rag.enabled = true`，并指定 `knowledge_base_id`，平台将自动完成检索、片段筛选（默认 Top 5）、清洗（ParseX）与上下文拼接，全程同步注入、零额外模型调用。适用于快速构建智能体应用，与 Memory、Connector 模块无缝协同。

- **低代码应用（Application）配置**：在百炼控制台创建智能体应用后，在「知识库」设置中绑定已发布的知识库，并选择调用策略（如“必定调用”）。该配置会自动透传至底层 Agent Context 或 RAG API，实现网站、企业微信、钉钉等多渠道统一增强，无需修改业务代码。

> ✅ 所有场景均基于同一套知识库基础设施：文档上传 → 切片 → 向量化（`text-embedding-v4` 等）→ 存储 → 语义检索 → 重排序（`qwen3-rerank` 等）→ 注入生成。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 | 推荐值 |
|------|------|------|------|--------|
| `knowledge_base_id` | RAG API `/search`、Agent Context `context.rag.knowledge_base_id`、应用配置界面 | string | 目标知识库唯一 ID（状态必须为 `FINISH`） | `kb-xxxxxx` |
| `top_k` | RAG API `/search` 的 `kb_search_configs` 字段、Agent Context 隐式控制 | integer | 检索返回的最相关片段数 | `3`–`5`（默认 `5`，单次最多 `5`） |
| `rerank_model` | 创建知识库时指定（`rag/index/create_v2`）、或 RAG API 动态覆盖 | string | 重排序模型，影响最终片段排序质量 | `qwen3-rerank`（主力）、`qwen3.7-text-rerank`（高精度） |
| `embedding_model` | 创建知识库时指定（`rag/index/create_v2`） | string | 文档切片向量化模型，决定检索召回基础 | `text-embedding-v4`（通用平衡）、`qwen3-vl-embedding`（多模态） |
| `context.max_tokens` | Agent Context `context.max_tokens` | number | 注入上下文（含检索片段 + prompt）总 token 上限 | `4096`（需 ≤ 所选模型最大上下文，如 Qwen-Turbo 为 8K） |
| `stream` & `incremental_output` | RAG API `/chat`、Agent Context 调用 | boolean | 启用流式响应（必设 `stream=true`）；`incremental_output=true` 可避免重复输出 | `true`（推荐启用） |

⚠️ 注意：
- 知识库 ID 参数名不一致：RAG API 中常见为 `index_id` 或 `indexId`，Agent Context 中为 `knowledge_base_id`，务必按接口文档严格使用；
- 检索片段经 ParseX 清洗后单片最长 1024 字符，超长内容会被截断；
- 多知识库并行检索时，各库 `top_k` 独立计算，再全局重排合并。

## 面向开发者，简洁实用

- **快速起步**：优先使用 Agent Context 方式——只需在 `/v1/chat/completions` 请求中添加 `context.rag` 对象，5 行 JSON 即可启用 RAG，无需管理检索接口、token 截断或上下文拼接。
- **精细控制**：若需自定义检索逻辑（如多路召回、业务规则过滤、混合排序），直接调用 RAG API 的 `/search` 接口，再将结果手动注入 prompt 调用 LLM。
- **性能优化**：
  - 选用 `qwen3-rerank` 替代已下线的 `gte-rerank-v2`；
  - 大批量文档向量化请用异步接口 `text-embedding-async-v2`；
  - 多模态场景统一使用 `qwen3-vl-embedding` + `qwen3-vl-rerank` 栈。
- **调试技巧**：测试时点击模型回复下方「问题反馈」按钮，或复制 `RequestId` 提交工单；也可在 RAG API `/search` 响应中直接查看原始检索片段及 `score`，快速定位召回/排序问题。

RAG 是百炼平台实现“私域知识即服务”的技术底座。正确配置，即可让任意大模型即时掌握你的业务知识，无需微调、无需训练、开箱即用。

## 关联主题页

- [rag api](../api/rag-api.md)
- [agent context](../guides/agent-context.md)
- [application use cases](../guides/application-use-cases.md)
- [application support](../guides/application-support.md)
- [vector and sort](../api/vector-and-sort.md)


