# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，简称 RAG）是一种将外部知识检索与大语言模型生成能力深度融合的技术范式。它通过在模型推理前动态检索相关知识片段，并将其作为上下文注入 LLM 提示词，从而显著提升回答的准确性、可溯源性与领域适配性，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，RAG 不是独立功能模块，而是贯穿多个核心能力的**横切架构模式**，主要落地于以下三类场景：

- **知识库问答（最常用）**：通过 `/v1/knowledge_base/query` 接口，自动完成“向量检索 →（可选）重排序 → 拼接上下文 → 调用 Qwen 系列模型生成答案”全流程。适用于客服机器人、技术文档助手、内部知识查询等。
- **智能体（Agent）与工作流**：在 Agent 的「检索节点」或工作流中的「Data Source 节点」中，可配置数据连接（如 MySQL、OSS、Elasticsearch），实现结构化/非结构化数据的动态检索，并将结果注入后续 LLM 步骤，支撑复杂决策与多跳推理。
- **通用 LLM 应用（`/v1/chat/completions` 或 `llm-application` API）**：通过显式传入 `retrieval_config` 参数（含 `knowledge_base_id`、`top_k` 等），在标准对话接口中一键启用 RAG 增强，无需修改业务逻辑，适合快速集成到现有应用。

> ✅ 关键提示：所有 RAG 场景均**强制依赖百炼托管的 Qwen 系列模型**（`qwen-max`/`qwen-plus`/`qwen-turbo`）进行最终生成；不支持第三方或自定义 LLM 后端。向量嵌入与重排序也必须使用平台预置模型（`text-embedding-v1`、`rerank-v1`），不可替换。

## 关键参数和配置

RAG 行为由以下核心参数控制，需在请求中显式指定（无全局默认开启）：

| 参数名 | 类型 | 说明 | 典型值 | 注意事项 |
|--------|------|------|--------|----------|
| `retrieval_strategy` | string | 检索方式：`"vector"`（语义向量）、`"fulltext"`（关键词）、`"hybrid"`（两者融合） | `"hybrid"` | `hybrid` 检索必须配合 `rerank: true` 才生效；`top_k ≤ 50`（API 指南强制限制） |
| `top_k` | integer | 检索返回的最相关知识片段数 | `3`（推荐 2–5） | 过大会增加 token 开销与延迟；RAG 场景需预留足够 token 给 LLM 输出（如 `qwen-turbo` 总上限 8192） |
| `rerank` | boolean | 是否启用内置重排序（RRF 算法） | `true` | 仅对 `hybrid` 有效；启用后会调用 `rerank-v1` 模型二次打分 |
| `enable_citation` | boolean | 是否返回引用溯源信息（chunk ID、原始文档路径等） | `true` | 响应中新增 `citations` 字段，用于构建可验证、可审计的答案 |
| `retrieval_config` | object | 通用 RAG 配置对象（用于 `/v1/chat/completions` 等接口） | `{"knowledge_base_id": "kb-xxx", "top_k": 3}` | 必须包含有效的 `knowledge_base_id`；不支持混合多个知识库 |

> ⚠️ 注意：`retrieval_strategy` 和 `rerank` 是效果调优的关键开关，建议优先实测 `vector` vs `hybrid+rerank` 组合；`enable_citation` 对合规性要求高的场景（如金融、医疗）为必选项。

## 面向开发者，简洁实用

- **快速上手**：  
  1. 控制台创建知识库 → 上传 PDF/TXT/MD 文档 → 等待向量化完成（状态变“可用”）；  
  2. 调用 `/v1/knowledge_base/query`，传入 `knowledge_base_id` 和 `query`，加上 `{"retrieval_strategy": "hybrid", "rerank": true, "enable_citation": true}`；  
  3. 解析响应：`answer` 是最终答案，`citations` 是来源列表（含 `chunk_id` 和 `document_path`）。

- **调试技巧**：  
  - 若答案质量差，先检查 `citations` 是否为空或内容无关 → 优化知识库分块策略（避免过长/过短）或调整 `top_k`；  
  - 若响应慢，禁用 `rerank` 或改用 `vector` 检索；  
  - 使用数据连接时，在 RAG 节点中开启「试运行」，直接查看原始检索结果，确认数据格式符合预期。

- **避坑指南**：  
  - 知识库文档需为纯文本可提取格式（PDF/Word 中图片文字需 OCR 预处理）；  
  - `retrieval_config` 仅在 `/v1/chat/completions` 中生效，**不适用于** `/v1/knowledge_base/query`（后者用专属参数）；  
  - 所有 RAG 请求均计入知识库配额（按查询次数 + 向量维度计费），生产环境请监控用量。

- **进阶组合**：  
  将 RAG 与 Function Calling 结合：先检索知识库获取背景，再调用数据库插件查实时数据，最后由 LLM 综合生成——全部在单个 Agent 工作流中编排完成。

## 关联主题页

- [knowledge base](../guides/knowledge-base.md)
- [data connection overview](../guides/data-connection-overview.md)
- [vector and sort](../api/vector-and-sort.md)
- [use cases](../guides/use-cases.md)
- [application use cases](../guides/application-use-cases.md)
- [llm application](../guides/llm-application.md)


