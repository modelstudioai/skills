# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，简称 RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态检索相关知识片段，并将其作为上下文注入提示（[prompt](../guides/prompt.md)），显著提升回答的事实准确性、领域专业性与可溯源性，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼平台不是单一功能，而是贯穿多个产品层级的**核心增强机制**，开发者可根据需求选择不同抽象层级的实现方式：

- **零代码应用层**：在「知识库问答应用」或「智能体应用（Agent 2.0）」中，只需绑定已创建的知识库，开启 `enable_search` 开关，平台自动完成检索→重排→融合→生成全流程，无需编写任何 RAG 逻辑。
- **低代码工作流层**：在 Workflow 中拖入「知识库节点」，可显式配置 `topK`（召回片段数）、知识库描述（影响触发准确性）、检索策略（如 `hybrid` 混合检索），并与其他节点（如条件判断、[函数调用](function-calling.md)）组合编排复杂 RAG 流程。
- **API 集成层**：通过 RAG API 直接调用 `/api/v1/indices/knowledge/search`（纯检索）或 `/api/v2/apps/knowledge/chat`（检索+生成），传入 `agent_id` 控制具体知识库与策略，适用于需要细粒度控制或与自有系统深度集成的场景。
- **框架开发层**：使用 LlamaIndex 或 Spring AI Alibaba 等官方适配器，通过 `DashScopeCloudRetriever` 或 `DashScopeEmbedding` 等组件，在本地代码中构建端到端 RAG 流水线，支持自定义切分、向量化与重排（注意：云端托管知识库 `DashScopeCloudIndex` 不支持自定义切分与 embedding 模型）。

> ✅ 统一前提：所有 RAG 能力均依赖**已发布且状态为 `active` 的知识库**，且所用大模型必须具备 `rag` 能力标识（如 `qwen-max`、`qwen-plus`、`Qwen3.5-Plus`）。

## 关键参数和配置

以下参数直接影响 RAG 效果，需根据业务场景合理设置：

| 参数名 | 所属层级 | 说明 | 推荐值 | 注意事项 |
|---------|-----------|------|----------|------------|
| `retrieval_config.top_k` / `topK` | 知识库/API/Workflow | 单次检索返回的最相关切片数量 | `3–10` | 过小易遗漏关键信息；过大增加噪声与 token 开销；多知识库并行时按库分别计数 |
| `retrieval_config.strategy` | 知识库/API | 检索策略 | `"hybrid"`（默认） | 支持 `"hybrid"`（BM25 + 向量混合）、`"vector_only"`、`"bm25_only"`；混合策略通常效果更鲁棒 |
| `qa_config.model_id` | 知识库/API/应用配置 | 执行最终生成的大模型 ID | `"qwen-plus"`（平衡型） | 必须是平台开通且带 `rag` 标识的模型；`qwen-turbo` 适合低延迟场景，`qwen-max` 适合高精度长文本 |
| `enable_reranking` + `rerank_top_n` | Frameworks/API | 是否启用重排序模型（如 `gte-rerank`）对初检结果二次打分 | `true`, `5` | 重排可显著提升 top1 准确率，但增加约 200–500ms 延迟；`rerank_min_score` 可过滤低置信结果 |
| `stream` / `incremental_output` | API/SDK | 是否启用流式响应 | `true`, `true` | `incremental_output=True` 时客户端仅接收新增 token，避免重复渲染，推荐用于 Web/APP 实时交互 |

> ⚠️ 重要约束：  
> - 知识库切片单条长度上限为 **8192 tokens**（超长将被截断，不报错）；  
> - 所有上传文档仅存储于用户专属租户空间，**不用于模型训练**，符合企业数据合规要求；  
> - 不支持跨知识库联合检索；如需多源融合，须在应用层聚合或预先合并知识库。

## 面向开发者，简洁实用

- **快速验证**：用控制台 Playground 上传一份 PDF，执行一次检索+问答，5 分钟内确认 RAG 效果是否符合预期。  
- **调试技巧**：若问答结果不准，优先检查 `RequestId` 并提交工单；同时复制检索返回的 `chunk_ids` 和原文片段，比对是否召回了正确依据。  
- **性能优化**：  
  - 对响应延迟敏感的场景（如微信公众号），选用 `qwen-turbo` + `topK=3` + `enable_reranking=false`；  
  - 对准确性要求高的场景（如合同审查），选用 `qwen-max` + `topK=5` + `enable_reranking=true` + `rerank_top_n=3`；  
- **避坑提醒**：  
  - API 参数命名不一致（如 `index_id` vs `indexId`），务必严格按各接口文档传参；  
  - 文件上传时 `sizeBytes` 必须为字符串（如 `"1048576"`），传数字会失败；  
  - `AgentKey`（业务空间标识）必须与 `App ID`、`API Key` 同属一个 workspace，否则鉴权失败。  

RAG 是百炼平台连接私有知识与大模型智能的“神经突触”。善用它，即可让通用大模型瞬间成为你业务领域的专家。

## 关联主题页

- [rag api](../api/rag-api.md)
- [start using](../guides/start-using.md)
- [llm application](../guides/llm-application.md)
- [knowledge base](../guides/knowledge-base.md)
- [application use cases](../guides/application-use-cases.md)
- [application support](../guides/application-support.md)
- [frameworks](../api/frameworks.md)


