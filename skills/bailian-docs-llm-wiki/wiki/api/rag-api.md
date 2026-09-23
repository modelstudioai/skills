# rag api

RAG API 是百炼平台提供的知识增强型问答服务接口，支持将私有知识库与大模型能力结合，实现精准、可控的[检索增强生成](../concepts/rag.md)。开发者可通过该 API 构建智能客服、文档助手、内部知识查询等场景。所有请求需通过 API Key 认证，并遵循统一的限流与错误处理规范。

## 支持的模型与功能

当前 RAG API 默认绑定平台托管的 `qwen-max-rag` 和 `qwen-plus-rag` 两类专用 RAG 模型，不支持用户自定义基础模型。核心功能覆盖知识库全生命周期管理（创建、更新、删除）、文档上传与解析、语义切片、异步同步任务调度，以及实时检索问答（含流式响应）。Agent 相关能力（如多跳推理、工具调用）需通过 [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md) 单独配置，不属于基础 RAG 请求范畴。

## 关键参数

- `knowledge_base_id`（必填）：目标知识库唯一标识，需提前通过 [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md) 接口创建并获取。
- `query`（必填）：用户自然语言问题，长度 ≤ 2048 字符。
- `top_k`（可选，默认 3）：返回最相关切片数量，取值范围 1–10。
- `stream`（可选，默认 `false`）：设为 `true` 时启用 SSE 流式响应，适用于长回答场景。
- `retrieval_strategy`（可选，默认 `hybrid`）：支持 `vector`、`fulltext`、`hybrid` 三种检索策略，详见 [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)。

> **注意**：原始文档中 [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md) 提到 `model` 参数可显式指定模型，但实际调用时该字段已被废弃；当前模型由 `knowledge_base_id` 所关联的知识库类型隐式决定，强行传入 `model` 将被忽略。

## 使用方式

1. 通过 [认证方式](../../raw/application-api-reference/rag-api/rag-api-authentication.md) 获取有效 API Key；
2. 调用 `/v1/knowledge_bases/{kb_id}/query` 发起 POST 请求；
3. 请求体为 JSON 格式，示例：
   ```json
   {
     "query": "百炼平台如何配置 RAG 知识库？",
     "top_k": 5,
     "stream": false
   }
   ```
4. 成功响应包含 `answer`（生成答案）、`retrieved_chunks`（引用切片列表）及 `trace_id`（用于问题排查）。

## 限制和注意事项

- 单次请求最大响应长度为 8192 tokens；超长答案将被截断，不触发分页；
- 知识库内单个文档大小上限为 50 MB（PDF/DOCX）或 10 MB（TXT）；
- 同步任务（如文档解析）状态需轮询 [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md) 接口获取，不支持 webhook 回调；
- 所有 RAG 请求受 [限流策略](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md) 约束，超出配额返回 `429 Too Many Requests`；
- 文档解析失败时，错误详情仅在 [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md) 的 `status` 字段中体现，需主动拉取而非实时推送。

## 来源文档

- [RAG](../../raw/application-api-reference/rag-api.md)


