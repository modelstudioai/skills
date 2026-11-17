# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，简称 RAG）是一种将大语言模型（LLM）与外部知识源动态结合的技术范式：在模型生成响应前，先从私有或结构化知识库中实时检索相关片段，再将检索结果作为上下文注入提示（[prompt](../guides/prompt.md)），引导模型生成更准确、可溯源、低幻觉的回复。

在百炼平台中，RAG 不是独立模块，而是贯穿知识管理、向量服务、Agent 编排与应用集成的核心能力，统一由知识库（Knowledge Base）、RAG API 与 Agent Context 三层协同实现。

## 在百炼平台的不同场景中，这个概念如何使用

- **知识库问答（KB QA）**：最典型 RAG 场景。用户调用 `/v1/knowledge_bases/{kb_id}/qa` 接口，平台自动执行「查询理解 → 多路召回（BM25 + 向量 + 关键词）→ 重排序 → 注入 top_k 片段 → 调用指定 LLM（如 `qwen-plus`）生成答案」全流程，支持[流式输出](streaming-output.md)（`stream=true`）。
  
- **RAG API 驱动的 Agent 应用**：通过 `/api/v2/apps/knowledge/chat` 等接口，将知识库封装为可发布、可路由的 Agent。开发者可在 `agent_config` 中声明模型、安全策略及知识库 ID，实现多知识库动态路由、多模态（文档/表格/图片/音视频）混合检索与问答。

- **Agent 上下文增强（Agent Context）**：当启用 `context_sources: ["rag"]` 时，RAG 检索结果不再单独用于问答，而是作为 Agent 运行时上下文的一部分，与 Memory、Connector 数据、ParseX 解析内容共同注入 [prompt](../guides/prompt.md)，支撑多步推理、状态跟踪与跨数据源协同任务。

- **本地 RAG 集成**：通过 `local_rag` 示例工程，开发者可复用百炼的嵌入（`text-embedding-v4`）与重排（`qwen3-rerank`）模型 API，在自有服务中构建轻量级 RAG pipeline，并与百炼应用对接，适用于对数据主权或延迟敏感的场景。

- **多渠道 AI 助手**：网站悬浮窗、企业微信、钉钉机器人等渠道应用，均默认启用 RAG 增强——只要在应用配置中绑定了知识库，所有用户提问即自动触发检索+生成链路，无需修改渠道代码。

## 关键参数和配置

| 参数 | 所属层级 | 说明 | 推荐值 |
|------|----------|------|--------|
| `top_k` | 知识库 / RAG API | 检索返回的最相关切片数量 | `1–3`（平衡精度与噪声）；最大支持 `10` |
| `retrieval_strategy` | 知识库 | 检索策略类型 | `"hybrid"`（默认，BM25+向量+关键词），也可设 `"vector_only"` 或 `"bm25_only"` |
| `rerank_model` | 知识库 / RAG API | 重排序模型 ID | `"qwen3-rerank"`（推荐）、`"bge-reranker-v2-m3"`；需知识库创建时启用 rerank |
| `embeddingModelName` | RAG API | 文本嵌入模型 | `"text-embedding-v4"`（高精度）、`"qwen3.7-text-embedding"`（长文本友好） |
| `multimodalEmbeddingModelName` | RAG API | 多模态嵌入模型 | `"qwen3-vl-embedding"`（支持图文融合） |
| `similarity_threshold` | 应用层（AppFlow） | 过滤低相关性检索结果 | `0.6–0.75`（低于此值的片段不注入 [prompt](../guides/prompt.md)） |
| `context_sources` | Agent Context | 显式声明 RAG 是否参与上下文构建 | 必须包含 `"rag"` 才启用；建议与 `"memory"` 组合使用 |

> ⚠️ 注意：`enable_hybrid_search` 已标记为 legacy 参数，新项目请统一使用 `retrieval_strategy="hybrid"`；所有知识库参数需在创建时指定，运行时不可修改，变更需重建知识库。

## 面向开发者，简洁实用

- ✅ **快速起步**：控制台新建知识库 → 上传 PDF/Word → 发布 → 调用 `/v1/knowledge_bases/{id}/qa?query=xxx`，5 分钟完成端到端 RAG。
- ✅ **精准调试**：使用 [Playground](https://bailian.console.aliyun.com/?tab=app#/knowledge-base/playground) 查看原始检索片段、各片段相似度分数、重排后顺序及最终生成答案，定位效果瓶颈。
- ✅ **模型自由切换**：知识库本身不绑定 LLM；问答时可随时在 API 请求中指定 `model=qwen-max` 或 `model=qwen-turbo`，无需重建索引。
- ✅ **多模态开箱即用**：上传图片+文字说明，设置 `structureType=unstructured` & `knowledgeScene=image_qa`，即可支持“图中表格数据提取”“PPT 内容问答”等场景。
- ❌ **避免踩坑**：
  - 不要混用旧参数（如 `enable_hybrid_search`）与新参数（`retrieval_strategy`）；
  - RAG API 中知识库 ID 字段名不统一（`index_id`/`indexId`/`id`），务必对照具体接口文档；
  - `qwen-turbo` 和 `qwen-1.5` 系列**不支持** Agent Context，若需 RAG+Agent 能力，请选用 `qwen-plus` 或 `qwen-agent-*` 模型。

## 关联主题页

- [rag api](../api/rag-api.md)
- [knowledge base](../guides/knowledge-base.md)
- [vector and sort](../api/vector-and-sort.md)
- [application use cases](../guides/application-use-cases.md)
- [agent context](../guides/agent-context.md)


