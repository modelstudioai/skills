# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态检索相关文档片段，并将其作为上下文注入提示（[prompt](../guides/prompt.md)），显著提升回答的事实准确性、领域专业性与可追溯性，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，RAG 不是独立功能模块，而是贯穿于多个能力层的**横切增强机制**，开发者可通过以下方式按需启用：

- **免代码问答应用**：在控制台创建“知识库问答”模板应用时，上传文档即自动构建向量知识库；发布后所有对话请求默认启用 RAG，无需修改提示词。
- **API 调用（`/v1/chat/completions`）**：在请求体中传入 `retrieval: { "knowledge_id": "xxx" }` 参数，平台将自动执行检索 → 重排序 → 上下文拼接 → 模型生成全流程，返回带溯源信息的增强答案。
- **数据连接（Data Connection）集成**：将 MySQL、Elasticsearch 或 OSS 等外部数据源注册为连接后，可在知识库配置中直接绑定，实现私有数据库内容的实时/定时同步与 RAG 调用。
- **多模态与混合检索**：结合 `vector and sort` 服务，可自定义调用 `text-embedding-v1` 生成查询向量，并用 `rerank-v1` 对 BM25 初检结果进行精排，再送入 LLM——适用于对精度和可控性要求极高的场景。
- **低代码嵌入式应用（如企业微信、钉钉机器人）**：在模板配置页启用“知识库增强”，选择已构建的知识库 ID，即可在 IM 消息流中无缝获得 RAG 支持的回答。

> ✅ 提示：所有 RAG 路径最终都统一归结为向 LLM 注入高质量上下文（`input_documents` 字段），百炼平台自动处理切片、向量化、检索策略选择、敏感信息脱敏等底层细节。

## 关键参数和配置

| 参数 | 类型 | 说明 | 推荐值 |
|------|------|------|--------|
| `retrieval` | `boolean` 或 `object` | 启用 RAG 的开关。设为 `true` 使用默认知识库；设为 `{ "knowledge_id": "kb-xxx", "top_k": 5 }` 指定知识库与检索数量 | `{ "knowledge_id": "kb-xxx" }` |
| `top_k` | `integer` | 检索返回的最相关文档片段数 | `3`（平衡精度与 token 开销） |
| `retrieval_strategy` | `string` | 检索模式：`"vector"`（纯向量）、`"keyword"`（BM25）、`"hybrid"`（默认，双路融合） | `"hybrid"` |
| `enable_rerank` | `boolean` | 是否启用 RRF 重排序（提升 Top-K 结果质量） | `true`（生产环境建议开启） |
| `query_rewrite` | `boolean` | 是否启用查询改写（如代词消解、同义扩展） | `false`（实验性功能，生产环境慎用） |

⚠️ 注意：
- `retrieval` 参数仅在支持 RAG 的模型上生效（如 `qwen-max`、`qwen-plus`、`qwen-turbo`）；`qwen2.5-7b-instruct` 等开源模型需自行构造 `input_documents` 字段。
- 知识库 ID（`knowledge_id`）需通过 `/v1/knowledge_bases` API 创建后获取，不可手动生成。
- 若同时使用 `system` 角色和 RAG，`system` 内容会与检索片段共同构成上下文，注意总 token 不超模型限制（如 `qwen-max` 为 32768）。

## 面向开发者，简洁实用

- ✅ **快速验证**：控制台新建知识库 → 上传一份技术文档 → 创建“知识库问答”应用 → 直接提问测试，全程 2 分钟内完成。
- ✅ **API 最小化集成**：只需在标准 chat 请求中增加一行：
  ```json
  "retrieval": { "knowledge_id": "kb-1234567890" }
  ```
- ✅ **调试技巧**：在请求中添加 `"debug": true`（部分模型支持），响应中将返回 `retrieved_documents` 原始片段，用于验证检索质量。
- ⚠️ **避坑提醒**：
  - 知识库更新后必须手动点击「重建索引」或等待定时同步任务，否则新内容不参与检索；
  - `retrieval_strategy: "hybrid"` 在含大量专有名词的文档中效果更稳，纯 `vector` 易受语义漂移影响；
  - 流式响应（`stream: true`）下，RAG 检索阶段无[流式输出](streaming-output.md)，首字节延迟 ≈ 检索+重排耗时（通常 < 800ms）。

如需深度定制（如自定义分块逻辑、替换 embedding 模型、接入自有向量库），请参考 [向量与排序](api/vector-and-sort.md) 和 [数据连接概述](guides/data-connection-overview.md) 文档。

## 关联主题页

- [start using](../guides/start-using.md)
- [knowledge base](../guides/knowledge-base.md)
- [data connection overview](../guides/data-connection-overview.md)
- [vector and sort](../api/vector-and-sort.md)
- [application use cases](../guides/application-use-cases.md)


