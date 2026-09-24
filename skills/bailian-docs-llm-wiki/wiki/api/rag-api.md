# rag api

RAG API 是百炼平台提供的面向[检索增强生成](../concepts/rag.md)（Retrieval-Augmented Generation）场景的核心服务接口，支持知识库构建、文档切片、异步同步、语义检索与问答等端到端能力。开发者可通过该 API 快速集成私有知识检索与 LLM 增强推理能力。所有接口均需通过标准认证，并遵循统一的限流与错误处理规范。

## 支持的模型/功能

- **知识库全生命周期管理**：包括创建、查询、更新、删除知识库，以及关联文档、切片、同步任务等子资源；详见 [RAG](../../raw/application-api-reference/rag-api.md) 文档中“知识库”和“文档管理”章节。
- **多模态数据导入与处理**：支持 PDF、Word、Excel、TXT、Markdown 等格式文档上传与自动解析，支持自定义分块策略（如按段落、标题、固定 token 数）；具体参数与行为请参考 [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md) 和 [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)。
- **实时检索与问答**：提供 `/v1/knowledge/query` 接口，支持向量+关键词混合检索、相关性重排序、答案生成（可选调用指定大模型），并返回引用片段及置信度；该能力在 [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md) 中有完整定义。

## 关键参数

- `knowledge_id`（必填）：目标知识库唯一标识，需提前通过 `/v1/knowledge_bases` 创建获取。
- `query`（必填）：用户自然语言问题，长度上限 2048 字符。
- `top_k`（可选，默认 3）：返回最相关切片数量，取值范围 1–50。
- `model`（可选）：指定用于生成答案的大模型 ID（如 `qwen-max`、`qwen-plus`），若不传则仅返回检索结果，不触发 LLM 生成。
- `enable_rerank`（可选，默认 `true`）：是否启用 Rerank 模型对初筛结果重排序；注意：[限流策略](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md) 中明确说明，启用 rerank 将消耗双倍 token 配额。

## 使用方式

1. **认证**：使用 `Authorization: Bearer <api_key>` 请求头，API Key 通过百炼控制台「API 密钥管理」获取；认证流程详见 [认证方式](../../raw/application-api-reference/rag-api/rag-api-authentication.md)。
2. **发起检索+问答请求**：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/knowledge/query" \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "knowledge_id": "kb-xxx",
           "query": "百炼平台如何配置 RAG？",
           "top_k": 5,
           "model": "qwen-plus"
         }'
   ```
3. **异步任务监控**：文档解析、切片、同步等耗时操作均返回 `job_id`，需轮询 `/v1/sync_jobs/{job_id}` 查询状态；同步任务细节见 [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)。

## 限制和注意事项

- 单次请求最大 `top_k` 为 50；单个知识库最多容纳 100 万切片（chunk），超出后写入失败。
- 所有文件上传接口（如 `/v1/documents`）要求 `Content-Type: multipart/form-data`，且单文件大小上限为 100 MB；该限制在 [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md) 中明确定义。
- > **注意**：原始文档中 [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md) 提到“支持实时流式问答响应”，但当前 `/v1/knowledge/query` 接口**仅支持同步阻塞返回**，暂不支持 `stream=true` 参数——该描述已过时，请以 [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md) 的最新接口定义为准。
- 错误响应统一遵循 RFC 7807 格式，常见错误码（如 `429 Too Many Requests`、`404 KnowledgeBaseNotFound`）含义详见 [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)。

## 来源文档

- [RAG](../../raw/application-api-reference/rag-api.md)


