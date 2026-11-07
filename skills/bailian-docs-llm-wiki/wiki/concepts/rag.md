# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态检索相关文档片段，并将其作为上下文注入提示（prompt），显著提升回答的事实准确性、领域专业性和私有知识覆盖能力，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，RAG 不是单一功能模块，而是贯穿多个核心能力层的横切技术底座，具体体现为以下三类典型应用方式：

- **RAG API 独立服务**：面向需要端到端知识管理能力的开发者，提供完整的知识库生命周期控制（创建/上传/同步）、可配置切片（按段落、语义边界或固定 token 长度）、向量检索（HNSW/IVF 索引）与生成式问答一体化接口。适用于构建私有知识助手、客服知识中枢等标准化 RAG 应用。

- **Agent 上下文（Agent Context）中的 RAG 子源**：作为 `context_sources` 的可选组件之一，RAG 与 Memory、Connector 等协同构成 Agent 运行时动态上下文。此时 RAG 检索结果与其他上下文数据按来源分别注入 prompt，不参与混合排序，但支持多轮对话中持续调用，适用于状态感知型智能体（如销售顾问、IT 支持机器人）。

- **应用级集成（Application Use Cases）中的默认增强机制**：在企业微信、钉钉、公众号、网站等渠道的 AI 助手方案中，RAG 是开箱即用的核心能力。用户上传的 PDF/DOCX/TXT/XLSX 等文件经“文档智能解析”自动切片并嵌入，所有问答请求默认触发知识检索，无需额外编码即可实现私域知识赋能。

> ⚠️ 注意：RAG 能力依赖模型兼容性——仅 `qwen-max`、`qwen-plus`、`qwen3.5-plus` 等 Qwen 系列模型原生支持完整 RAG 问答；其他模型（如 `qwen-turbo`、三方模型）仅可用于 embedding 生成，不可直接用于 `/v1/knowledge/query` 或 Agent RAG 问答阶段。

## 关键参数和配置

RAG 行为由一组轻量、正交的参数控制，不同接入方式对应不同参数名，但语义一致：

| 场景 | 参数名 | 类型 | 默认值 | 说明 | 典型取值建议 |
|------|--------|------|--------|------|--------------|
| RAG API（`/v1/knowledge/query`） | `top_k` | integer | `3` | 检索返回的最相关文本片段数量 | `3–5`（平衡精度与噪声）；最大 `50` |
| | `score_threshold` | float | `0.3` | 向量相似度过滤阈值（0.0–1.0），低于此值的片段被丢弃 | `0.3–0.6`（生产环境推荐）；设 `0.0` 表示不过滤 |
| | `enable_rerank` | boolean | `false` | 是否启用 cross-encoder 重排序（提升相关性，增加 300–800ms 延迟） | `true`（对精度敏感场景）；`false`（低延迟优先） |
| Agent Context | `rag_top_k` | integer | `3` | 同 `top_k`，作用于 Agent 中 RAG 子源 | 与 `top_k` 保持一致即可 |
| 应用集成控制台 | “召回片段数” | integer | `3` | 控制台可视化配置项，映射至 `top_k` | 同上 |
| | “相似度阈值” | float | `0`（即无过滤） | 控制台可视化配置项，映射至 `score_threshold` | `0.3–0.6` |

> ✅ 提示：  
> - 所有参数均在请求级生效，无需全局配置；  
> - `score_threshold` 实际效果受向量索引类型影响（HNSW 更稳定，IVF 对阈值更敏感），调试时建议结合 `retrieved_chunks` 返回的 `score` 字段观察分布；  
> - 切片长度（chunk size）虽非运行时参数，但直接影响 RAG 效果——默认 `512 tokens`，最小 `64`；过短易割裂语义，过长则降低检索粒度，推荐根据文档结构选择“按段落”或“语义切分”。

## 面向开发者，简洁实用

- **快速起步**：只需三步——① 创建知识库获取 `knowledge_id`；② 上传文档并等待 `sync_job` 完成；③ 调用 `/v1/knowledge/query` 即可获得带溯源的答案。  
- **调试技巧**：响应中 `retrieved_chunks` 字段明确列出每个片段的 `content`、`source_document_name` 和 `score`，是验证检索质量的第一手依据。  
- **性能权衡**：启用 `enable_rerank` 可提升 top-3 结果相关性约 15–25%，但延迟增加明显；若业务允许少量噪声，优先调优 `top_k` 与 `score_threshold`。  
- **避坑指南**：  
  - 不要混用模型：`qwen-turbo` 不能用于 RAG 问答，仅支持 embedding；  
  - 文档上传后需等待 1–6 分钟同步完成，期间查询将返回空结果；  
  - API Key 与应用必须处于同一业务空间，否则鉴权失败（错误码 `401` 或 `403`）。  

RAG 是百炼平台连接私有知识与大模型智能的“神经突触”。善用其参数组合，你无需训练模型，即可让 LLM 精准说出你文档里写下的每一句话。

## 关联主题页

- [rag api](../api/rag-api.md)
- [agent context](../guides/agent-context.md)
- [application use cases](../guides/application-use-cases.md)
- [use cases](../guides/use-cases.md)


