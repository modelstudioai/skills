# rag api

RAG API 是百炼平台提供的[检索增强生成](../concepts/rag.md)服务接口，支持将私有知识库与大模型能力结合，实现基于上下文的精准问答。开发者可通过该 API 管理知识库、导入文档、触发同步任务，并调用检索+生成一体化的问答接口。所有请求需通过 API Key 认证，且受统一限流策略约束 [RAG](../../raw/application-api-reference/rag-api.md)。

## 支持的模型与功能

- **核心功能**：知识库生命周期管理（创建/查询/删除）、文档上传与解析、自动切片（chunking）、异步同步任务调度、多路检索（关键词+向量）、以及端到端问答（`/knowledge/query`）。
- **模型支持**：问答环节默认使用平台托管的 `qwen-max` 或 `qwen-plus`，暂不支持用户自选基础模型；但可通过 `model` 参数在 `/knowledge/query` 中指定已开通的推理模型（详见 [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)）。
- **扩展能力**：支持与 Agent 模块联动，将 RAG 结果作为 Agent 的工具输出源 [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `knowledge_id` | string | 是 | 知识库唯一标识，需先通过 `/knowledge_bases` 创建获取 |
| `query` | string | 是 | 用户自然语言问题，长度 ≤ 2048 字符 |
| `top_k` | integer | 否 | 检索返回的最相关切片数，默认 3，取值范围 1–10 |
| `retrieval_mode` | string | 否 | 可选 `hybrid`（默认，关键词+向量融合）、`vector`、`keyword` |
| `model` | string | 否 | 指定生成模型，如 `qwen-plus`；若未传，则使用知识库绑定的默认模型 |

> **注意**：原始文档中 [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md) 提到 `model` 参数可全局配置于知识库级别，但实际 API 调用时仅 `/knowledge/query` 接口支持运行时覆盖——该行为以 [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md) 为准。

## 使用方式

1. **前置准备**：  
   - 创建知识库（`POST /v1/knowledge_bases`），获取 `knowledge_id`；  
   - 上传文档（`POST /v1/knowledge_bases/{kb_id}/documents`），支持 PDF/DOCX/TXT/MD 等格式；  
   - 触发同步（`POST /v1/knowledge_bases/{kb_id}/sync`），等待 `status=completed` 后方可检索。

2. **发起问答**：  
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/knowledge/query" \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "knowledge_id": "kb-xxx",
           "query": "百炼平台的RAG API如何限流？",
           "top_k": 5,
           "retrieval_mode": "hybrid"
         }'
   ```

3. **响应结构**：包含 `answer`（生成结果）、`retrieved_chunks`（来源切片列表）、`usage`（token 消耗）等字段，详见 [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md) 中的成功响应示例。

## 限制和注意事项

- 单次问答请求最大 `query` 长度为 2048 字符；单个知识库最多容纳 100 万切片；
- 文档解析异步完成，平均延迟 10–60 秒，超时时间由 [限流策略](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md) 中的 `sync_job_timeout` 控制；
- 不支持跨知识库联合检索；切片内容不可直接修改，需重新上传文档并同步；
- 所有 API 均强制 HTTPS，且 `API Key` 必须通过 `Authorization: Bearer <key>` 传递，明文拼接 URL 将被拒绝（参见 [认证方式](../../raw/application-api-reference/rag-api/rag-api-authentication.md)）。

## 来源文档

- [RAG](../../raw/application-api-reference/rag-api.md)


