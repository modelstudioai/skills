# rag api

RAG API 是百炼平台提供的面向[检索增强生成](../concepts/rag.md)（RAG）场景的核心服务接口，支持知识库构建、文档切片、异步同步、语义检索与问答等端到端能力。开发者可通过该 API 快速集成私有知识检索能力到自有应用中。所有接口均需通过 [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md) 才能调用。

## 支持的模型/功能

- **知识库生命周期管理**：创建、查询、更新、删除知识库（见 [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)）  
- **文档与切片操作**：上传/删除文档、手动触发解析、查看/修改切片内容（见 [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md) 和 [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)）  
- **同步任务控制**：启动、查询、取消基于外部数据源（如 OSS、数据库）的增量同步（见 [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)）  
- **检索与问答**：支持单轮语义检索（`/v1/knowledge/retrieve`）和带上下文生成的问答（`/v1/knowledge/ask`），底层默认使用 `bge-reranker-v2-m3` 重排 + `text-embedding-v3` 向量模型（详见 [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)）

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `knowledge_id` | string | 是 | 知识库唯一标识，需先通过 [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md) 接口创建获取 |
| `query` | string | 是（检索/问答接口） | 用户自然语言问题或关键词，长度 ≤ 2048 字符 |
| `top_k` | integer | 否 | 检索返回的最相关切片数，默认 5，最大支持 100 |
| `enable_rerank` | boolean | 否 | 是否启用重排，默认 `true`；设为 `false` 可跳过重排以降低延迟 |
| `stream` | boolean | 否 | 仅 `/v1/knowledge/ask` 支持，设为 `true` 时返回 SSE 流式响应 |

> **注意**：原始文档中 [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md) 提到 `rerank_model` 可选参数，但当前 API 实际已移除此字段，重排模型由服务端统一管控，客户端不可覆盖。

## 使用方式

1. **认证**：在请求 Header 中携带 `Authorization: Bearer <api_key>`（参考 [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)）  
2. **准备知识库**：调用 `POST /v1/knowledge_bases` 创建知识库 → 获取 `knowledge_id`  
3. **导入数据**：可直接上传文件（`POST /v1/knowledge_bases/{id}/documents`），或配置数据源后提交同步任务（`POST /v1/knowledge_bases/{id}/sync_jobs`）  
4. **发起检索或问答**：  
   - 检索：`POST /v1/knowledge/retrieve`，返回匹配的切片列表及元数据  
   - 问答：`POST /v1/knowledge/ask`，返回带引用来源的生成答案  

所有接口均遵循 RESTful 设计，响应体为标准 JSON，错误格式统一（见 [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)）。

## 限制和注意事项

- 单次上传文档大小上限为 100 MB；单知识库总文档数上限为 10,000 份（见 [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)）  
- 切片长度默认为 512 token（按 `text-embedding-v3` 分词器），不可自定义；若需调整，请联系技术支持（[切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md) 中未提供长度配置入口）  
- 异步同步任务最长超时时间为 24 小时，失败后不会自动重试，需主动调用重试接口（见 [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)）  
- `stream=true` 问答请求不支持 `enable_rerank=false` 组合，否则将返回 400 错误

## 来源文档

- [RAG API](../../raw/application-api-reference/rag-api.md)


