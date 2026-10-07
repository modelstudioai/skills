# rag api

RAG API 是百炼平台提供的[检索增强生成](../concepts/rag.md)服务接口，支持将私有知识库与大模型能力结合，实现基于上下文的精准问答。开发者可通过该 API 管理知识库、导入文档、触发同步任务，并调用检索+生成一体化的问答接口。所有操作均需通过标准 HTTP 请求完成，依赖平台统一认证与限流机制。

## 支持的模型/功能

- 支持的知识库类型包括结构化数据（如数据库表）和非结构化文档（PDF、Word、TXT 等），具体格式限制详见 [RAG](../../raw/application-api-reference/rag-api.md) 中的 [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md) 和 [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md) 章节。  
- 核心功能涵盖：知识库生命周期管理、文档切片（chunking）策略配置、异步同步任务控制、以及端到端的“检索+生成”问答（`/knowledge/query`）。  
- 当前仅支持百炼平台内置的 RAG 专用推理引擎，不开放自定义 LLM 后端替换；该约束在 [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md) 文档中有明确说明。

## 关键参数

- `knowledge_base_id`（必需）：目标知识库唯一标识，需提前通过 `/knowledge_bases` 创建并获取。  
- `query`（必需）：用户自然语言问题，长度上限 2048 字符。  
- `top_k`（可选，默认 3）：返回最相关切片数量，取值范围 1–10。  
- `enable_rerank`（可选，默认 false）：启用重排序模型提升相关性，会略微增加延迟。  
- `stream`（可选，默认 false）：设为 `true` 时以 SSE 流式返回生成结果，适用于长响应场景。

## 使用方式

1. **认证**：使用 Bearer [Token](../concepts/token.md) 方式，在 `Authorization` 请求头中传入 `Bearer <access_token>`；[Token](../concepts/token.md) 获取方式见 [认证方式](../../raw/application-api-reference/rag-api/rag-api-authentication.md)。  
2. **发起问答请求**：向 `POST /v1/knowledge/query` 发送 JSON 请求体，示例：
   ```json
   {
     "knowledge_base_id": "kb-xxx",
     "query": "如何申请API访问权限？",
     "top_k": 5,
     "enable_rerank": true
   }
   ```
3. **处理响应**：成功时返回 `200 OK`，含 `answer` 字段（生成答案）、`retrieved_chunks`（匹配切片列表）及 `usage`（token 消耗统计）。

## 限制和注意事项

- 单次问答请求最大响应长度为 4096 tokens；超出部分将被截断，不触发错误。  
- 知识库内单个文档大小上限为 100 MB，超限文件在 [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md) 阶段会被拒绝。  
- > **注意**：[限流策略](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md) 文档中描述的“每秒 5 QPS”为旧版配额，实际生效值以控制台「API 配额管理」页面为准，新创建应用默认为 20 QPS。  
- 切片（chunk）内容不可直接修改，如需更新，须删除原文档后重新上传；该行为在 [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md) 中有明确说明。  
- 同步任务（sync job）状态轮询建议间隔 ≥3 秒，高频轮询可能触发限流且无业务收益。

## 来源文档

- [RAG](../../raw/application-api-reference/rag-api.md)


