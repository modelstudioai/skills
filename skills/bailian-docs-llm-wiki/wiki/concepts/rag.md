# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态检索相关上下文，并将其注入提示（[prompt](../guides/prompt.md)），显著提升回答的事实准确性、领域专业性与时效性，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，RAG 不是单一功能模块，而是贯穿多个能力层的**横切架构模式**，开发者可根据需求灵活组合使用：

- **知识库（Knowledge Base）**：最典型的 RAG 实现。上传私有文档（PDF/Word/TXT/Markdown 等），平台自动完成解析、分块、向量化与索引构建；调用时按需检索 Top-K 片段，自动拼接至 [prompt](../guides/prompt.md) 中供大模型生成答案。适用于智能客服、内部知识问答、合规文档解读等场景。

- **数据连接（Data Connection）**：支持在 RAG 流程中接入结构化数据源（如 MySQL、Elasticsearch、OSS 文件等）。可在 Agent 工作流或自定义函数节点中，以 SQL 或文件路径方式动态查询实时/准实时数据，结果直接作为检索上下文注入生成环节，实现“数据库即知识源”。

- **应用级 RAG 集成**：在「应用」创建向导中选择 RAG 模板，系统自动绑定知识库 ID 并启用 `enable_retrieval: true`；也可在 `/v1/chat/completions` 请求中显式传入 `knowledge_base_id` 和检索参数，实现低代码快速上线。

- **混合检索增强链路**：结合向量接口（`/v1/embeddings`）与重排序接口（`/v1/rerank`），可构建自定义 RAG 流水线——例如先用 `text-embedding-v1` 向量化用户问题，从向量库召回候选片段，再用 `gte-rerank` 对结果重打分并截断，最后送入 LLM 生成。该方式适用于对检索精度要求极高、需精细控制中间环节的场景。

> ✅ 提示：所有 RAG 调用均默认启用多阶段可观测性——应用监控（Application Monitoring）会自动拆分并统计「检索耗时」「重排耗时」「生成耗时」，便于性能调优与问题定位。

## 关键参数和配置

以下参数在不同 RAG 使用路径中高频出现，开发者应重点关注其语义与取值建议：

| 参数 | 所属模块 | 类型 | 说明 | 推荐值 | 注意事项 |
|------|----------|------|------|--------|----------|
| `top_k` | 知识库 / 自定义 RAG | int | 检索返回的最相关文档片段数量 | `3–5` | 过高易引入噪声，过低可能遗漏关键信息；单次排序请求上限为 100（见 `/v1/rerank`） |
| `score_threshold` | 知识库 | float | 相似度阈值（0.0–1.0），低于此值的片段被过滤 | `0.3–0.6` | 当前 `text-embedding-v1` 输出为余弦相似度；实际生效依赖归一化逻辑，勿按点积理解 |
| `retrieval_mode` | 知识库 | string | 检索模式：`"vector"`（纯向量）、`"keyword"`（BM25）、`"hybrid"`（混合） | `"hybrid"`（默认） | 混合模式兼顾语义与关键词匹配，对模糊查询更鲁棒 |
| `enable_rerank` | 知识库 | bool | 是否启用重排序（RRF 或专用 rerank 模型） | `false`（默认），高精度场景设为 `true` | 启用后额外计费，且需确保 `top_k ≤ 100`（受 rerank 接口限制） |
| `knowledge_base_id` | 应用 / API | string | 绑定的知识库唯一标识 | 必填 | 单个应用最多绑定 1 个知识库；多源需求请预先合并或设计多路召回策略 |
| `connection_id` + `query` | 数据连接 | string | 外部数据源连接 ID 与动态查询语句（支持 `{{input.xxx}}` 占位符） | 必填（RAG 场景下） | 查询仅限 `SELECT`，禁止写操作；OSS 路径需含完整协议（如 `oss://bucket/path.json`） |

## 面向开发者，简洁实用

- **快速验证**：控制台 → Model Studio → 知识库 → 创建并上传文档 → “测试”页直接输入问题，5 分钟内验证 RAG 效果。
- **API 调用核心模式**：
  ```http
  POST /v1/chat/completions
  {
    "model": "qwen-plus",
    "messages": [{"role": "user", "content": "如何申请发票？"}],
    "knowledge_base_id": "kb-xxx",
    "top_k": 3,
    "retrieval_mode": "hybrid"
  }
  ```
- **自定义 RAG 流水线（推荐进阶用法）**：
  1. 调用 `/v1/embeddings` 获取 query 向量；
  2. 用该向量查询向量库（或调用 `/knowledge_bases/{kb_id}/retrieve`）；
  3. 将召回结果传入 `/v1/rerank` 重排序；
  4. 拼接 top-N 片段到 [prompt](../guides/prompt.md)，调用 `/v1/chat/completions` 生成。
- **避坑提醒**：
  - 知识库不自动脱敏：若检索结果含身份证、手机号等敏感字段，**必须在应用层处理**；
  - 索引非实时：新增/修改文档后需手动触发「同步索引」，或等待每 24 小时一次的定时同步；
  - 流式响应兼容性：启用 RAG 时仍可设 `"stream": true`，但重排序（`enable_rerank=true`）不支持流式，需权衡延迟与精度。

> 💡 最佳实践：从 `top_k=3` + `retrieval_mode="hybrid"` 开始迭代；观察监控中的「检索命中率」与「生成准确率」指标，再逐步调整 `score_threshold` 或启用重排。

## 关联主题页

- [knowledge base](../guides/knowledge-base.md)
- [data connection overview](../guides/data-connection-overview.md)
- [vector and sort](../api/vector-and-sort.md)
- [application use cases](../guides/application-use-cases.md)
- [application monitoring](../guides/application-monitoring.md)
- [use cases](../guides/use-cases.md)


