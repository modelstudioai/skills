# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，简称 RAG）是百炼平台的核心能力范式，指在大模型生成响应前，先从结构化或非结构化知识源中实时检索相关片段，并将检索结果作为上下文注入提示词，从而提升回答的事实准确性、时效性与领域专业性。它不是独立模型，而是一套可配置、可编排的端到端流水线，涵盖知识接入、语义索引、混合检索、重排序与条件化生成。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼中以**服务化、模块化、多模态化**方式深度集成，具体体现为以下四类典型用法：

- **知识库问答服务（/api/v2/apps/knowledge/chat）**：最常用场景。用户提问后，系统自动触发知识库检索 → 重排 → 将 Top-K 切片拼入 Prompt → 调用绑定的生成模型（如 `qwen3.6-plus`）生成带引用的自然语言回答。支持文档、表格、图片、音视频四类知识库类型，对应不同 `knowledgeType` 和 `knowledgeScene`。

- **Agent 运行时上下文注入（`agent context`）**：当 Agent 配置 `context_type: ["rag"]` 时，RAG 不再独立调用，而是作为上下文组装环节嵌入 Agent 执行流。平台自动根据 `rag_config.kb_ids` 检索并注入内容，与 Memory、Connector 等上下文并列，统一由 `system_prompt` 封装传递给模型。

- **低代码应用集成（Application Use Cases）**：在网站、企业微信、钉钉等渠道部署 AI 助手时，“配置知识库”即启用 RAG。无需写代码，控制台一键关联知识库至应用，所有渠道请求均自动走 RAG 流水线；本地 RAG 方案还支持完全离线运行，使用自定义切分器和本地嵌入模型（如 `GTE-Chinese-Large`）。

- **底层检索 API（/api/v1/indices/rag/index/retrieve）**：面向需要精细控制的开发者。直接传 `index_id` 和 `query`，跳过重排与生成，返回原始向量召回结果（含 `score`、`content`、`metadata`），适用于构建自定义排序逻辑、A/B 测试或调试切片质量。

## 关键参数和配置

RAG 行为由多个层级的参数协同控制，开发者需按需显式配置（未配置则使用平台默认值）：

| 类别 | 参数名 | 说明 | 常见取值 | 是否可变 |
|------|--------|------|----------|----------|
| **知识库创建期** | `embeddingModelName` | 向量化模型，决定语义检索质量 | `"text-embedding-v4"`（文本）、`"qwen3-vl-embedding"`（多模态） | ❌ 创建后不可修改 |
|  | `chunkingStrategy` / `maxChunkLength` | 切片策略与最大长度（token） | `"smart"` / `600`（默认） | ❌ 创建后不可修改 |
|  | `metadataFields` | 自定义元数据抽取字段（用于过滤） | `["product_id", "version"]` | ❌ 创建后不可补配 |
| **检索服务期** | `top_k`（召回数） | 向量检索初步召回数量 | `10`（范围 1–100） | ✅ 可在服务配置中调整 |
|  | `similarityThreshold` | 相似度阈值（低于此值的结果被剔除） | `0.35`（范围 0.01–1.0） | ✅ 可调 |
|  | `rerankModelName` | 重排模型（精排阶段使用） | `"qwen3-rerank"`（文本）、`"qwen3-vl-rerank"`（多模态） | ✅ 可切换 |
|  | `hybrid_rerank` | 是否启用混合重排（向量+关键词） | `true` / `false` | ✅ 可开关 |
| **运行时调用期** | `search_filters` | 按 `tags`、`doc_id` 或自定义 metadata 过滤 | `[{"tags": ["v2"]}]` | ✅ 每次请求可传 |
|  | `kb_search_configs`（Agent） | 多知识库权重、路由策略 | `[{ "kb_id": "kb-xxx", "weight": 0.8 }]` | ✅ Agent 配置中定义 |

> ⚠️ 注意：`knowledgeScene=visual_perception_qa` 时必须显式传 `multimodalEmbeddingModelName`，否则可能降级为默认模型，影响效果一致性。

## 面向开发者，简洁实用

- **快速验证**：用控制台 Playground → 选择知识库 → 切换“知识问答”模式，5 秒内看到 RAG 效果。
- **API 调试**：优先使用 `/api/v1/indices/knowledge/search`（需 `agent_id`），它已内置重排与混排，比底层 `/retrieve` 更贴近真实业务。
- **避免踩坑**：
  - 知识库创建后，嵌入模型、切片策略、metadata 字段均**不可修改**——出错请重建，勿尝试 PATCH。
  - `index_id`、`pipelineId`、`agent_id` 是三个不同 ID，分别用于知识库管理、切片操作、服务调用，混用必报 `InvalidParameter`。
  - 微信公众号等有 5 秒超时限制的渠道，请设 `temperature=0.1` + `max_tokens=256` + 选用 `qwen-turbo`，并关闭非必要 RAG 上下文。
- **进阶控制**：如需完全掌控 RAG 流程（例如自定义重排逻辑或融合外部搜索），建议使用本地 RAG 方案，通过 Python SDK 接入百炼嵌入模型 API，自行组装检索与生成链路。

## 关联主题页

- [rag api](../api/rag-api.md)
- [knowledge base](../guides/knowledge-base.md)
- [application use cases](../guides/application-use-cases.md)
- [agent context](../guides/agent-context.md)
- [use cases](../guides/use-cases.md)


