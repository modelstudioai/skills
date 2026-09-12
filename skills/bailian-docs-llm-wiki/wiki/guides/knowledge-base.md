# knowledge base

知识库（Knowledge Base）是百炼平台提供的 RAG（[检索增强生成](../concepts/rag.md)）核心能力，用于将私有文档数据注入大模型推理流程，提升问答准确性与领域适配性。它支持结构化/非结构化文档的上传、切片、向量化与语义检索，并可与多种大模型协同完成问答任务。该能力通过 API 和控制台双通道提供，适用于客服问答、技术文档助手、内部知识沉淀等场景。

## 支持的模型/功能

- **模型兼容性**：知识库检索结果可作为上下文输入至百炼平台所有支持 `input_documents` 参数的大模型（如 Qwen-Max、Qwen-Plus、Qwen-Turbo），具体支持列表见 [知识库（RAG）](../../raw/application-user-guide/knowledge-base.md)。
- **核心功能**：
  - 文档上传与自动解析（PDF/Word/Excel/TXT/Markdown 等格式）
  - 基于语义的向量检索（支持 BM25 混合检索）
  - 检索结果重排序（RRF）、片段截断与上下文拼接
  - 支持问答（QA）模式与纯检索（Retrieval）模式两种调用路径
  - 定时数据同步（需配置 OSS 或 NAS 数据源），详见 [知识库定时数据同步指南](../../raw/application-user-guide/knowledge-base.md)

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `knowledge_id` | string | 是 | 知识库唯一标识，创建后由平台分配 |
| `top_k` | integer | 否 | 返回最相关文档片段数，默认 3，最大支持 10 |
| `retrieval_strategy` | string | 否 | 取值 `"vector"` / `"keyword"` / `"hybrid"`，默认 `"hybrid"` |
| `enable_rerank` | boolean | 否 | 是否启用重排序，默认 `true`；关闭可降低延迟但可能影响精度 |
| `query_rewrite` | boolean | 否 | 是否启用查询改写（如补全指代、扩展同义词），默认 `false` |

> **注意**：`query_rewrite` 在 [知识库API指南](../../raw/application-user-guide/knowledge-base.md) 中被标记为实验性功能，生产环境建议设为 `false`；而部分旧版 SDK 示例中默认开启，存在行为不一致风险。

## 使用方式

1. **控制台创建**：进入 Model Studio → 知识库 → 新建知识库 → 上传文件或绑定数据源 → 构建索引（约 1–5 分钟/GB）  
2. **API 调用**（以问答为例）：
   ```http
   POST /v1/knowledge_bases/{knowledge_id}/query
   {
     "query": "如何配置SSL证书？",
     "top_k": 5,
     "retrieval_strategy": "hybrid"
   }
   ```
   响应包含 `retrieved_documents`（带 score 的文本片段）和可选的 `answer`（若启用 QA 模式）。完整请求规范参见 [知识库API指南](../../raw/application-user-guide/knowledge-base.md)。

## 限制和注意事项

- 单个知识库最大文档数：10 万份；单文档最大体积：100 MB（PDF/Word）或 50 MB（其他格式）  
- 向量索引构建后不支持实时更新，新增/修改文档需手动触发“重建索引”或依赖定时同步任务  
- 检索结果中的 `content` 字段已做敏感信息脱敏（如身份证号、手机号），若需原始内容请在创建知识库时关闭脱敏开关（见 [知识库效果优化](../../raw/application-user-guide/knowledge-base.md)）  
- 免费试用额度仅覆盖前 100 万 tokens 的向量化与检索，超出后按 [知识库计费说明](../../raw/application-user-guide/knowledge-base.md) 扣费  
- 日志与监控数据保留 30 天，需长期审计请自行对接 SLS，参考 [知识库日志与监控](../../raw/application-user-guide/knowledge-base.md)

## 来源文档

- [知识库（RAG）](../../raw/application-user-guide/knowledge-base.md)


