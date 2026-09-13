# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，简称 RAG）是一种将外部知识检索与大语言模型生成能力深度融合的技术范式。它通过在模型推理前动态检索相关知识片段，并将其作为上下文注入提示（[prompt](../guides/prompt.md)），使模型在不微调的前提下显著提升事实准确性、领域专业性和回答可追溯性。

## 在百炼平台的不同场景中如何使用

RAG 在百炼平台并非单一功能模块，而是贯穿多个核心能力的横切架构，开发者可根据需求选择不同粒度的集成方式：

- **知识库问答（开箱即用）**：在「知识库」模块中上传文档（PDF/Word/Markdown 等），平台自动完成解析、分块、向量化与索引构建；调用 `/v1/knowledge_base/query` 即可获得端到端检索+生成结果，适用于客服助手、内部文档查询等标准化场景。

- **LLM 应用内嵌 RAG（低代码/高代码统一支持）**：在 `llm application` 中配置知识库后，所有应用类型（智能体、工作流、高代码、文件问答）均可通过 `enable_search: true` + `retrieval_config` 自动启用 RAG。平台在生成前透明执行混合检索（关键词+向量+重排序），并将 top-k 片段拼入系统提示词，无需修改业务逻辑。

- **数据连接驱动的动态 RAG**：通过「数据连接」接入 MySQL/PostgreSQL 等结构化数据源，在工作流节点中执行参数化 SQL 查询，将实时数据库结果（如订单状态、库存信息）直接注入 LLM 上下文，实现“查完即答”的动态知识增强。

- **自定义 RAG 流程（细粒度控制）**：开发者可独立调用向量 API（`/v1/services/embeddings`）生成 query 向量，再调用 rerank API（`/v1/services/rerank`）对候选文档重排序，最后将精排结果手动拼入 LLM 请求的 `messages` 或 `system` 字段，适用于需定制召回策略或融合多源知识的高级场景。

## 关键参数和配置

| 参数 | 所属能力 | 类型 | 说明 | 推荐值 |
|------|----------|------|------|--------|
| `top_k` | 知识库 / LLM 应用 | integer | 检索返回的文档片段数量 | `3`（平衡精度与噪声），最大 `10` |
| `score_threshold` | 知识库 | float (0.0–1.0) | 向量相似度过滤阈值，低于此值的片段被丢弃 | `0.35`（初始值，建议结合 A/B 测试调优） |
| `enable_hybrid_search` | 知识库 | boolean | 是否同时启用关键词匹配与向量检索 | `true`（默认，显著提升长尾 query 召回率） |
| `retrieval_mode` | 知识库 | string | 检索模式：`single`（单次）或 `multi`（多跳） | `single`（默认）；复杂推理问题可选 `multi`（延迟+40%） |
| `enable_search` | LLM 应用（`parameters` 内） | boolean | 全局开关，启用知识库检索 | `true`（需配合 `retrieval_config`） |
| `retrieval_config` | LLM 应用（`parameters` 内） | object | 指定知识库 ID、`top_k`、`score_threshold` 等 | `{ "knowledge_base_id": "kb-xxx", "top_k": 3 }` |
| `model`（rerank） | 向量与排序 | string | 专用重排序模型 ID | `rerank-v1`（必须显式指定，不可混用 embedding 模型） |

> ⚠️ 注意：`max_tokens` 等生成参数不影响检索过程；RAG 效果高度依赖检索质量，建议优先优化 `score_threshold` 和 `top_k`，而非盲目增大生成长度。

## 面向开发者，简洁实用

- **快速验证**：先用控制台「知识库 > 测试问答」确认文档分块与检索相关性，再接入应用——避免因 PDF 扫描图、表格识别异常等静默失败。
- **[Token](token.md) 管控**：RAG 检索结果计入模型上下文。若 `qwen2.5-7b-instruct`（32K context）用于处理长文档，请确保 `top_k × 平均片段长度 + prompt` 不超限，否则前端截断会导致关键信息丢失。
- **时效性保障**：知识库更新后需等待 2–5 分钟索引生效；高时效场景请配置 [定时数据同步](https://help.aliyun.com/zh/model-studio/data-sync-guide) 或 Webhook 回调。
- **安全底线**：数据连接密码必须通过平台 UI/API 显式传入（平台加密存储），禁止硬编码或环境变量注入；SQL 查询运行于沙箱，不支持跨库 JOIN 或系统命令。
- **调试链路**：所有 RAG 调用均支持完整 trace 追踪。通过控制台「调用日志」按 `app_id` + `request_id` 查看检索原始片段、重排序分数、最终注入 [prompt](../guides/prompt.md) 的完整上下文，精准定位效果瓶颈。

## 关联主题页

- [llm application](../guides/llm-application.md)
- [knowledge base](../guides/knowledge-base.md)
- [data connection overview](../guides/data-connection-overview.md)
- [vector and sort](../api/vector-and-sort.md)
- [application use cases](../guides/application-use-cases.md)


