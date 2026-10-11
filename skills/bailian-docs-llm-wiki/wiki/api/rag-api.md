# rag api

RAG API 是百炼平台提供的面向[检索增强生成](../concepts/rag.md)（RAG）场景的核心服务接口，支持知识库构建、文档切片、异步同步、语义检索与问答等全流程能力。开发者可通过该 API 实现私有知识的接入、管理与推理集成。所有接口均需通过标准认证，并受统一限流策略约束 [RAG](../../raw/application-api-reference/rag-api.md)。

## 支持的模型/功能

- **知识库生命周期管理**：创建、查询、更新、删除知识库，支持多租户隔离  
- **文档与切片管理**：上传文档（PDF/Word/TXT/Markdown 等）、触发解析、查看切片内容及元数据 [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)  
- **同步任务控制**：启动/取消/查询文档解析与向量化任务，支持增量同步 [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)  
- **检索与问答**：调用 `/knowledge/query` 接口执行混合检索（关键词 + 向量），返回带来源引用的结构化答案；支持流式响应  
- **Agent 集成**：可将知识库绑定至 RAG Agent，用于构建对话式应用 [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `knowledge_base_id` | string | 是 | 目标知识库唯一标识，需提前创建 |
| `query` | string | 是 | 用户自然语言问题，长度 ≤ 2048 字符 |
| `top_k` | integer | 否 | 检索返回的最相关切片数，默认 3，范围 1–50 |
| `enable_hybrid_search` | boolean | 否 | 是否启用关键词+向量混合检索，默认 `true` |
| `stream` | boolean | 否 | 是否启用流式响应，默认 `false`；设为 `true` 时响应格式为 SSE |

> **注意**：`top_k` 在 [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md) 中明确限定最大值为 50，但部分旧版 SDK 示例中误写为 100，以该文档为准。

## 使用方式

1. **认证**：在请求 Header 中携带 `Authorization: Bearer <access_token>`，Token 通过 [认证方式](../../raw/application-api-reference/rag-api/rag-api-authentication.md) 获取  
2. **发起检索**：向 `POST /v1/knowledge/query` 发送 JSON 请求体（含 `knowledge_base_id` 和 `query`）  
3. **处理响应**：成功时返回 `200 OK`，含 `answer` 字段与 `references` 数组（含切片 ID、原文片段、文档来源）  
4. **错误处理**：参考 [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md) 文档解析 `code` 与 `message`

## 限制和注意事项

- 单次请求 `query` 长度上限为 2048 字符；超长将被截断并返回 `400 Bad Request`  
- 知识库内单文档大小上限为 100 MB（PDF/Word）或 50 MB（其他格式）  
- 免费试用额度下，每知识库每分钟最多 60 次 `/query` 调用；超出触发 [限流策略](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)  
- 切片（chunk）默认按语义分段（非固定长度），不可手动指定切片粒度；如需细粒度控制，需使用 `/rag-api-chunks.md` 接口后置调整  
- 同步任务状态轮询间隔建议 ≥ 2 秒，高频轮询不加速处理且计入限流 quota

## 来源文档

- [RAG](../../raw/application-api-reference/rag-api.md)


