# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是百炼平台的核心能力范式，指在大模型生成响应前，先从私有知识库中实时检索相关片段，并将检索结果作为上下文注入提示词（[prompt](../guides/prompt.md)），从而提升回答的准确性、可溯源性与领域专业性。它本质是“检索 + 生成”的协同机制，解耦了知识存储与模型推理，使 LLM 能够安全、可控地调用企业自有数据。

## 在百炼平台的不同场景中，这个概念如何使用

- **知识库问答（`/v1/rag/qa`）**：最典型的 RAG 应用。用户提问后，系统自动执行多路召回（向量+关键词混合检索），返回 top_k 相关文本切片，再拼接进 [prompt](../guides/prompt.md)，交由 `qwen-plus` 等模型生成带引用标记的流式回答。
- **Agent 智能体增强**：通过 `agent context` 的 `knowledge` 类型上下文源，将知识库动态注入 Agent 运行时环境；配合 `context_config.knowledge.max_chunks` 控制注入片段数，实现多轮对话中持续的知识感知与引用。
- **多渠道 AI 助手集成**：在企业微信、钉钉、公众号或网站嵌入的智能体应用中，“关联知识库”即启用 RAG；配置“必定调用”策略后，所有用户消息均强制触发检索，确保客服、产品支持等场景的回答始终基于最新文档。
- **API 级细粒度控制**：RAG API（Knowledge API）提供分离式接口：`/v1/rag/retrieve` 仅执行纯检索（返回切片 ID 与原文），供开发者自定义 [prompt](../guides/prompt.md) 工程；`/v1/rag/qa` 则封装完整 RAG 流程，开箱即用。
- **Wiki 知识图谱构建（旗舰版）**：在 `basic_document_qa` 场景下开启 `wikiEnabled` 后，RAG 不仅用于问答，还驱动 Wiki 内容自动抽取与结构化合成，实现从文档到知识图谱的增强演进。

## 关键参数和配置

| 参数 | 所属层级 | 说明 | 推荐值 | 注意事项 |
|------|-----------|------|---------|----------|
| `top_k` | 问答/检索接口 | 单次检索返回的最相关切片数量 | `3`（平衡精度与延迟） | 值过大易引入噪声，且增加 token 成本；最大支持 `10` |
| `retrieval_strategy` | 知识库/问答接口 | 检索策略类型 | `hybrid`（默认） | 可选 `vector_only`（纯向量）、`keyword_only`（纯关键词）；`hybrid` 效果更鲁棒 |
| `enable_rerank` | 问答接口 | 是否启用交叉编码器重排序 | `true`（高精度场景） | 开启后延迟略增，但显著提升 top3 结果相关性 |
| `knowledge_id` / `agent_id` | 全局调用 | 知识库或已发布 Agent 实例 ID | `kb-xxxxxx` / `agent-xxxxxx` | 必须提前创建并发布，否则调用失败 |
| `context_config.knowledge.max_chunks` | Agent 上下文配置 | Agent 中注入的最大知识切片数 | `3`（与 `top_k` 对齐） | 超出部分被截断，不参与计费与生成 |
| `embeddingModelName` / `rerankModelName` | 知识库创建时 | 指定向量化与重排模型 | `text-embedding-v4`, `qwen3-rerank` | 影响检索质量，需与知识类型匹配（如 `multimedia` 场景需多模态 embedding） |

> ⚠️ 提示：所有 RAG 调用均按实际使用的 token 计费（含检索返回的文本 + prompt 注入内容 + 模型输出），建议通过 `top_k` 和 `max_chunks` 主动约束规模。

## 面向开发者，简洁实用

- ✅ **快速验证**：用控制台 Playground 上传 PDF/Word，直接测试检索与问答效果，无需写代码。
- ✅ **API 集成**：优先使用 `/v1/rag/qa?stream=true` 获取流式回答；若需自定义 prompt 或融合其他上下文，改用 `/v1/rag/retrieve` + 自行调用 `/v1/chat/completions`。
- ✅ **Agent 场景**：在 `agent_config.context` 中声明 `"knowledge"` 源，并绑定 `knowledge_id`；无需修改模型逻辑，RAG 自动注入。
- ✅ **调优建议**：
  - 检索不准？检查文档解析质量（PDF 表格是否保留）、`retrieval_strategy` 是否为 `hybrid`、是否启用了 `enable_rerank`；
  - 回答泛化？降低 `top_k` 或启用 `rerank` 提升精准度；
  - 延迟高？关闭 `enable_rerank`，或选用 `qwen3.5-flash` 等低延迟模型处理生成阶段。
- ❌ **避免踩坑**：
  - 不要混用 `index_id`（snake_case）和 `pipelineId`（camelCase）——接口文档明确标注格式；
  - 文件上传必须携带 `MD5` 校验值，否则拒绝；
  - 知识库更新后索引非实时（30–120 秒延迟），调试时注意时间窗口。

## 关联主题页

- [rag api](../api/rag-api.md)
- [knowledge base](../guides/knowledge-base.md)
- [application use cases](../guides/application-use-cases.md)
- [agent context](../guides/agent-context.md)
- [application support](../guides/application-support.md)


