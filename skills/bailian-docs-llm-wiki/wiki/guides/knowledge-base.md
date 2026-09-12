# knowledge base

知识库（Knowledge Base）是百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，支持将私有文档注入模型上下文，实现基于自有数据的精准问答与推理。它通过向量化存储、语义检索与大模型生成三阶段协同工作，适用于客服问答、技术文档助手、内部知识沉淀等场景。所有功能均通过 API 或控制台统一接入，开发者可灵活集成至业务系统。

## 支持的模型/功能

- **基础能力**：支持知识检索（[知识检索](https://help.aliyun.com/zh/model-studio/rag-knowledge-retrieval)）、知识问答（[知识问答](https://help.aliyun.com/zh/model-studio/rag-knowledge-qa)）、定时数据同步（[知识库定时数据同步指南](https://help.aliyun.com/zh/model-studio/data-sync-guide)）  
- **模型兼容性**：当前仅支持调用百炼托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 等 Qwen 系列模型进行生成；不支持第三方模型或自定义 LLM 后端。向量模型固定为 `text-embedding-v1`，不可替换。  
- **高级功能**：支持多路召回、重排序（RRF）、引用溯源（source citation），但需在请求参数中显式启用（见下文“关键参数”）。  

## 关键参数

| 参数名 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| `top_k` | integer | 检索返回的最相关文档片段数 | `3` |
| `retrieval_strategy` | string | 可选 `"vector"`、`"fulltext"` 或 `"hybrid"` | `"vector"` |
| `enable_citation` | boolean | 是否返回引用来源（chunk ID、原始文档路径等） | `false` |
| `rerank` | boolean | 是否启用内置重排序（仅对 `hybrid` 检索有效） | `false` |

> **注意**：`retrieval_strategy=hybrid` 在 [知识库API指南](https://help.aliyun.com/zh/model-studio/rag-knowledge-base-api-guide) 中明确要求 `top_k ≤ 50`，但 [知识库配额与限制](https://help.aliyun.com/zh/model-studio/rag-knowledge-base-specifications) 文档仍标注为 `≤ 100`，以 API 指南为准。

## 使用方式

1. **准备知识源**：上传 PDF/Word/TXT/Markdown 等格式文件，或通过 API 接入 OSS、NAS、数据库等外部数据源（详见 [知识库API指南](https://help.aliyun.com/zh/model-studio/rag-knowledge-base-api-guide)）  
2. **创建知识库实例**：在控制台选择分块策略（按段落/固定 token 数）、嵌入模型（仅 `text-embedding-v1`）、是否启用自动同步  
3. **发起 RAG 请求**：调用 `/v1/knowledge_base/query` 接口，传入 `knowledge_base_id`、`query` 及上述关键参数  
4. **解析响应**：结果包含 `answer` 字段（生成答案）和可选的 `citations` 字段（引用元数据），结构详见 [知识库API指南](https://help.aliyun.com/zh/model-studio/rag-knowledge-base-api-guide)

## 限制和注意事项

- 单个知识库最大文档数：10,000 份；单文档最大体积：100 MB（PDF/Word）或 50 MB（纯文本）  
- 分块后单 chunk 最大长度：512 tokens；最小长度：32 tokens（低于此值将被丢弃）  
- 知识库构建耗时取决于文档总量与复杂度，首次构建可能需数分钟至数小时；增量更新延迟通常 < 2 分钟（参见 [知识库定时数据同步指南](https://help.aliyun.com/zh/model-studio/data-sync-guide)）  
- 日志与监控需单独开通 SLS 投递，且仅保留最近 30 天数据（[知识库日志与监控](https://help.aliyun.com/zh/model-studio/rag-knowledge-base-log-monitoring)）  
- 计费按向量维度、查询次数、存储容量三维度叠加，具体规格见 [知识库配额与限制](https://help.aliyun.com/zh/model-studio/rag-knowledge-base-specifications) 和 [知识库计费说明](https://help.aliyun.com/zh/model-studio/billing-for-knowledge-base)  

> **注意**：原始文档中多次出现的“知识库效果优化”链接（[知识库效果优化](https://help.aliyun.com/zh/model-studio/rag-optimization)）未提供具体参数调优阈值或 A/B 测试方法，实际调优应优先参考 [知识库API指南](https://help.aliyun.com/zh/model-studio/rag-knowledge-base-api-guide) 中的 `retrieval_strategy` 与 `rerank` 组合实测结果。

## 来源文档

- [知识库（RAG）](../../raw/application-user-guide/knowledge-base.md)


