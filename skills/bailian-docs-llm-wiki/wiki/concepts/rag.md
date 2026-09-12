# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将外部知识检索与大语言模型生成能力深度融合的技术范式。它通过在模型推理前动态检索相关上下文片段，并将其注入提示（[prompt](../guides/prompt.md)），显著提升生成结果的事实准确性、领域专业性与可溯源性，同时降低幻觉风险。

## 在百炼平台的不同场景中如何使用

RAG 在百炼平台中不是独立服务，而是贯穿多个核心能力的**端到端工作流模式**，开发者可通过以下方式灵活启用：

- **知识库问答（最常用）**：上传私有文档（PDF/Word/TXT/MD 等）构建知识库，调用 `/v1/chat/completions` 时在请求体中指定 `retrieval` 字段（含 `knowledge_base_id`），平台自动完成「用户查询 → 多路检索（向量+关键词）→ 重排序 → 拼接上下文 → LLM 生成 → 引用标注」全链路。
- **数据连接增强**：将结构化数据源（MySQL、PostgreSQL、CSV 等）配置为数据连接后，在 RAG 应用中绑定该连接，模型可在生成过程中动态执行 SQL 查询或 API 调用，将实时结果作为上下文注入，适用于报表问答、客户数据实时解析等场景。
- **混合增强应用（RAG + Agent）**：在 Agent 工作流中，将知识库检索或数据连接查询作为工具（Tool）之一，由模型自主决策何时调用、如何组合多源信息，实现更复杂的推理闭环（如“查合同条款 + 查法务知识库 + 生成合规建议”）。
- **低代码集成场景**：在控制台创建 RAG 类型应用时，勾选「启用检索」并选择已发布知识库，即可零代码启用 RAG；Web SDK、企微/钉钉 Bot 等嵌入式场景同样支持一键开启。

> ✅ 提示：所有 RAG 流程均默认启用应用观测（Application Monitoring），可在「观测」面板查看各阶段耗时（检索 ms / 重排 ms / 生成 ms）、召回率、引用准确率等关键指标。

## 关键参数和配置

RAG 行为由多个层级的参数协同控制，主要分为三类：

### 1. 知识库级（创建时设定，不可变）
| 参数 | 说明 | 推荐值 |
|------|------|--------|
| `chunk_size` | 文档切片最大 token 数 | `256–512`（平衡语义完整性与召回精度） |
| `chunk_overlap` | 相邻分块重叠 token 数 | `32–64`（缓解边界信息丢失） |

> ⚠️ 注意：修改需重建知识库。

### 2. 检索调用级（每次请求可覆盖）
| 参数 | 说明 | 默认值 | 开发者建议 |
|------|------|--------|------------|
| `top_k` | 返回最相关片段数 | `3` | RAG 场景建议 `3–5`；Agent 中可设 `1` 配合多工具调用 |
| `score_threshold` | 向量相似度过滤阈值（0.0–1.0） | `0.3` | 严格场景（如法律/医疗）调高至 `0.5–0.6`，避免噪声注入 |
| `retrieval_mode` | 检索模式 | `hybrid` | 默认混合检索；纯语义场景用 `vector`，术语精确匹配用 `keyword` |

### 3. 生成请求级（API 请求体中指定）
```json
{
  "model": "qwen-plus",
  "messages": [{"role": "user", "content": "合同第5条如何解释？"}],
  "retrieval": {
    "knowledge_base_id": "kb-xxx",
    "top_k": 4,
    "score_threshold": 0.45
  }
}
```

- `retrieval` 字段为启用 RAG 的开关，必须包含 `knowledge_base_id`；
- 其内参数优先级高于知识库默认值，适合 A/B 测试或动态策略调整。

## 面向开发者：简洁实用指南

- **快速验证**：用控制台创建知识库 → 上传一份技术文档 → 在「调试」页输入问题，观察检索结果与生成答案是否带引用标记（如 `[1]`）；
- **调试技巧**：开启 `enable_monitoring: true` 后，在观测面板中点击任一 trace，展开 `retrieval` span 查看原始检索 query、返回的 chunk 内容及 score；
- **性能优化**：
  - 若检索慢：检查 `chunk_size` 是否过大（导致向量维度膨胀），或启用 `retrieval_mode: keyword` 快速兜底；
  - 若生成不准：先确认 `score_threshold` 是否过低引入噪声；再检查 `system_prompt` 是否明确要求“仅基于检索内容回答，不确定则拒绝”；
- **安全注意**：知识库与数据连接均不存储原始数据明文，但检索结果会拼入 [prompt](../guides/prompt.md) —— 敏感字段（如身份证号）请在上传前脱敏，或通过 `filter` 参数在检索时动态过滤（见知识库 API 文档）；
- **兼容性**：所有百炼托管 LLM（Qwen 系列、Qwen2/Qwen3）均原生支持 RAG 上下文注入；无需修改模型调用逻辑，仅需添加 `retrieval` 字段。

RAG 是百炼平台落地私有知识价值的核心路径。从上传文档到生产部署，全程无需训练、不依赖算力扩容，开发者只需聚焦业务语义与效果调优。

## 关联主题页

- [knowledge base](../guides/knowledge-base.md)
- [data connection overview](../guides/data-connection-overview.md)
- [vector and sort](../api/vector-and-sort.md)
- [application monitoring](../guides/application-monitoring.md)
- [application use cases](../guides/application-use-cases.md)


