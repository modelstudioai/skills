# rag api

RAG API 是百炼平台提供的面向[检索增强生成](../concepts/rag.md)（RAG）场景的核心服务接口，支持知识库构建、文档切片、异步同步、语义检索与问答等端到端能力。开发者可通过该 API 快速集成私有知识检索能力到自有应用中。所有接口均需通过标准认证，并受统一限流策略约束 [RAG](../../raw/application-api-reference/rag-api.md)。

## 支持的模型/功能

- **知识库全生命周期管理**：创建、查询、更新、删除知识库（见 [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)）  
- **文档与切片操作**：上传/删除文档、触发解析、查看切片详情（见 [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md) 和 [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)）  
- **同步任务控制**：启动、查询、取消文档同步任务（见 [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)）  
- **检索与问答**：支持向量检索 + LLM 生成的联合调用，返回带引用来源的答案（见 [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)）  
- **Agent 集成**：可将 RAG 能力绑定至 Agent 工作流（见 [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)）

> **注意**：`/v1/knowledge/query` 接口当前仅支持同步模式，不支持流式响应；而部分旧版文档示例中提及的 `stream=true` 参数已被移除，以 [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md) 中最新定义为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `knowledge_id` | string | 是 | 目标知识库唯一标识，由 `/knowledge_bases` 创建后返回 |
| `query` | string | 是 | 用户自然语言问题，长度 ≤ 2048 字符 |
| `top_k` | integer | 否 | 检索返回的最相关切片数，默认 3，取值范围 1–10 |
| `enable_rerank` | boolean | 否 | 是否启用重排序，默认 `false`；启用后延迟略增但精度提升 |
| `model` | string | 否 | 指定生成模型（如 `qwen-max`, `qwen-plus`），未指定时使用知识库默认模型 |

## 使用方式

1. **认证**：在请求 Header 中携带 `Authorization: Bearer <api_key>`，密钥需通过 [认证方式](../../raw/application-api-reference/rag-api/rag-api-authentication.md) 获取  
2. **发起检索问答请求**（POST `/v1/knowledge/query`）：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/knowledge/query \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "knowledge_id": "kb-xxx",
           "query": "百炼平台如何配置RAG知识库？",
           "top_k": 5,
           "enable_rerank": true
         }'
   ```
3. **异步任务监控**：对大文档导入或批量同步，需轮询 `/sync_jobs/{job_id}` 获取状态（参考 [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)）

## 限制和注意事项

- 单次请求 `query` 长度上限为 2048 字符；单个知识库最多容纳 100 万切片（详见 [限流策略](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)）  
- 文档上传后需等待同步任务完成（状态为 `completed`）才可被检索，不可跳过 [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md) 流程直接查询  
- 错误响应统一遵循标准格式，含 `code` 与 `message` 字段；常见错误如 `KnowledgeBaseNotFound`、`DocumentParseFailed` 可查 [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)  
- 所有 API 均按调用量计费，免费额度详见控制台配额页；超出后请求将返回 `429 Too Many Requests`

## 来源文档

- [RAG](../../raw/application-api-reference/rag-api.md)


