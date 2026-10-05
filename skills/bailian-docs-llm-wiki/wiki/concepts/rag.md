# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）与外部知识源动态结合的技术范式：在生成响应前，系统先从结构化或非结构化知识库中检索相关片段，再将检索结果作为上下文注入提示（[prompt](../guides/prompt.md)），驱动模型生成准确、可溯源、时效性强的自然语言回答。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，RAG 不是独立模块，而是贯穿知识管理、服务调用与应用集成的核心能力，具体体现为以下三类使用方式：

- **知识库问答服务**：面向业务人员，通过控制台 Playground 或发布后的问答 API（`/v1/services/aigc/retrieval-augmented-generation/generation`），输入用户问题，自动完成「查询改写 → 多路检索（向量+关键词）→ 重排 → LLM 生成」全链路，返回带引用标注的答案。适用于客服问答、内部文档助手等场景。

- **知识库检索服务**：面向开发者，调用 `/v1/indices/{index_id}/search` 等 RAG API，仅执行检索环节，返回原始切片（chunk）列表及元数据（如来源文件、页码、相似度分）。适用于需自定义后处理逻辑（如规则过滤、多源融合、NL2SQL 转换）的高级场景。

- **框架与应用集成**：通过 `frameworks`（如 LlamaIndex、Spring AI Alibaba）或 `application use cases`（如钉钉机器人、网站嵌入），以声明式方式启用 RAG。只需设置 `retrieval_enabled: true` 并传入 `knowledge_id`，底层自动绑定知识库、选择默认嵌入/重排/生成模型，无需手动拼接 [prompt](../guides/prompt.md) 或管理检索流程。

> ✅ 提示：所有 RAG 调用均运行在业务空间内，知识库资源隔离、权限可控；不支持跨空间共享知识库。

## 关键参数和配置

RAG 行为由多个层级参数协同控制，开发者需按需调整：

| 类别 | 参数名 | 说明 | 可变性 | 典型值 |
|--------|---------|------|---------|----------|
| **知识库创建时** | `embedding_model_name` | 嵌入模型，决定语义向量质量 | ❌ 创建后不可更改 | `text-embedding-v4`（文本）、`qwen3-vl-embedding`（多模态） |
| | `chunking_strategy` / `max_chunk_length` | 切片策略与最大长度，影响召回粒度与精度 | ❌ 创建后不可更改 | `smart`（智能切分），`600`（token） |
| **检索调用时** | `top_k`（初检） / `rerank_top_n` | 向量/关键词初检数量、重排后保留数 | ✅ 动态可调 | `10` / `3` |
| | `similarity_threshold` | 过滤低相关切片的最小相似度 | ✅ 动态可调 | `0.35`（推荐起始值） |
| | `max_retrieved_results` | 最终返回切片总数 | ✅ 动态可调 | `5` |
| **问答调用时** | `retrieval_mode` | 检索模式 | ✅ 动态可调 | `fast`（单轮）、`agentic`（多轮 Query 改写） |
| | `enable_citation` / `refuse_if_no_evidence` | 是否标注引用、是否拒答无依据问题 | ✅ 动态可调 | `true` / `true` |
| **通用调用** | `model`（LLM） | 生成模型，影响回答质量与成本 | ✅ 动态可调 | `qwen3.6-plus`（RAG 推荐） |

> ⚠️ 注意：  
> - `embedding_model_name` 和切片参数一旦创建知识库即固化，如需变更，须新建知识库并重新导入数据。  
> - 多知识库联合检索时，可通过 `kb_search_configs` 为每个知识库单独配置 `top_k`、`rerank_top_n` 等参数。  
> - 使用 `agentic` 模式时，系统会自动进行 Query 扩展、路由与迭代检索，但会增加延迟与 token 消耗。

## 面向开发者，简洁实用

- **快速验证**：用控制台 Playground 选中知识库 → 切换“知识问答”模式 → 输入问题，实时查看检索切片与生成答案，5 分钟完成效果评估。  
- **API 集成**：优先使用 RAG 专用 endpoint `https://dashscope.aliyuncs.com/api/v1/services/aigc/retrieval-augmented-generation/generation`，传参简洁（`model`, `knowledge_id`, `input.text`, `retrieval_enabled: true`），无需手动构造检索逻辑。  
- **避免常见错误**：  
  - 不要混淆 `index_id`（snake_case）与 `indexId`（camelCase）——删除知识库用 `index_id`，查切片列表用 `indexId`；  
  - 文件上传时务必使用 `docIds`（复数），而非 `file_ids`；  
  - 启用 RAG 时，`knowledge_id` 必须指向已成功完成切片与索引构建的知识库（状态为 `active`）。  
- **性能优化建议**：  
  - 对 FAQ 类知识，设 `max_chunk_length=256`；对长报告，设 `2048`；  
  - 高精度场景必开 `rerank_model_name=qwen3-rerank`；  
  - 流式响应（`stream=true`）与 RAG 兼容，但首 token 延迟略高于纯生成请求。

## 关联主题页

- [knowledge base](../guides/knowledge-base.md)
- [rag api](../api/rag-api.md)
- [application use cases](../guides/application-use-cases.md)
- [frameworks](../api/frameworks.md)


