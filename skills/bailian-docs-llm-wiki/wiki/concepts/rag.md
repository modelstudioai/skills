# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是百炼平台的核心能力范式，指在大语言模型生成响应前，先从私有或领域知识库中语义检索相关片段，并将检索结果作为上下文注入模型提示词，从而提升回答的准确性、专业性与事实一致性。该机制有效弥补了大模型固有的知识时效性差、幻觉率高、领域适应弱等局限。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼中不是单一 API，而是贯穿多个能力层的统一技术底座，按使用深度和控制粒度分为三类典型形态：

- **开箱即用的知识问答（Knowledge Chat）**：面向业务终端用户，通过 `POST /api/v2/apps/knowledge/chat` 接口调用。平台自动完成「查询理解 → 多库路由 → 向量+关键词混合检索 → Rerank 精排 → 模型上下文拼接 → 流式生成」全链路，开发者仅需传入 `agent_id` 和对话历史，无需感知底层 RAG 细节。适用于客服助手、内部知识库问答等零代码/低代码场景。

- **可编排的 RAG 工作流（Workflow RAG）**：面向需要确定性控制的开发者，在工作流画布中显式拖入「知识库节点」，配置 `topK`、`相似度阈值`、`标签过滤` 等参数，再将检索结果（如 `{知识库1/result}`）注入下游大模型节点的提示词。支持多知识库并行检索、条件分支、批处理等复杂逻辑，适用于合规审查、招投标应答等强流程场景。

- **框架级自定义 RAG（Framework RAG）**：面向专业开发者，通过 LlamaIndex 等 SDK 集成 `DashScopeCloudRetriever` 或 `DashScopeCloudIndex`，在代码中精细控制检索策略（如启用 `gte-rerank-hybrid` 重排、设置 `rerank_min_score` 过滤低分切片）。适用于需与本地向量库混合、或需定制解析/切分逻辑（注：云端知识库不支持自定义切分）的混合架构场景。

> ⚠️ 注意：所有 RAG 能力均依赖已发布的知识库服务（`agent_id`），模型选型（如 embedding 模型、rerank 模型）、索引结构、路由策略等均由控制台统一配置并发布，**API 层不可动态覆盖**。

## 关键参数和配置

RAG 行为主要由以下参数控制，其生效位置取决于使用方式：

| 参数名 | 生效位置 | 类型 | 常用值 | 说明 |
|--------|----------|------|--------|------|
| `agent_id` | 所有 RAG 接口必填 | `string` | `aid-xxx` | 绑定已发布的知识服务 ID；检索服务与问答服务 ID 不互通，须分别创建。 |
| `top_k` / `max_retrieval_count` | 工作流知识库节点、`DashScopeCloudRetriever` | `int` | `5`–`20` | 最终返回给模型的切片总数（非初步召回数），直接影响上下文长度与 token 消耗。 |
| `score_threshold` | 控制台知识库配置页、工作流节点、`retrieval_config` | `float` | `0.3`–`0.5` | 过滤低于该相似度分数的切片，值越高结果越精准但可能漏召。 |
| `dense_similarity_top_k` | `DashScopeCloudRetriever` SDK | `int` | `50`–`100` | 向量检索阶段初步召回数，决定 Rerank 模型输入规模（影响费用）。 |
| `enable_reranking` | `DashScopeCloudRetriever` SDK | `boolean` | `true` | 是否启用重排模型（默认开启），对初步召回结果进行语义精排。 |
| `tags` / `metadata_filter` | 控制台调试界面、工作流节点、SDK | `object` | `{"department": "legal"}` | 基于上传时设置的标签或元数据字段进行前置过滤，提升精度与效率。 |

- **全局约束**：单次 RAG 调用中，所有检索切片总 token 数计入模型上下文限制（如 `qwen-turbo` 上下文上限 8192），需合理设置 `top_k` 避免超限。
- **配置入口**：核心参数（相似度阈值、权重、标签过滤等）均在控制台「知识库详情页 → 检索配置」中设置并发布，API 仅通过 `agent_id` 绑定生效。

## 面向开发者，简洁实用

- ✅ **快速验证**：用控制台「知识库调试」功能，输入 query 实时查看原始切片、相似度分数及元数据，无需写代码。
- ✅ **生产集成**：优先使用 `knowledge/chat` 接口（SSE 流式）或工作流知识库节点，避免自行拼接 [prompt](../guides/prompt.md) 导致上下文溢出。
- ✅ **调试技巧**：若回答不准确，检查响应中的 `docs` 数组（问答接口）或工作流节点输出，确认检索是否命中关键文档；复制 `request_id` 提交工单时务必附上。
- ❌ **避免踩坑**：不要尝试在 API 请求体中传入 `model`、`embedding_model` 等模型参数——这些由 `agent_id` 对应的控制台配置决定，强行传入将被忽略。
- 📦 **SDK 推荐**：Python 开发者首选 `llama-index-indices-managed-dashscope` + `llama-index-postprocessor-dashscope-rerank`，一行代码接入云端 RAG 全能力。

## 关联主题页

- [knowledge](../api/knowledge.md)
- [start using](../guides/start-using.md)
- [knowledge base](../guides/knowledge-base.md)
- [llm application](../guides/llm-application.md)
- [frameworks](../api/frameworks.md)
- [use cases](../guides/use-cases.md)
- [application support](../guides/application-support.md)


