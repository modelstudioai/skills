# rag api

RAG API 是百炼平台提供的面向[检索增强生成](../concepts/rag.md)（RAG）场景的核心服务接口，支持知识库构建、文档切片、异步同步、语义检索与问答等全链路能力。开发者可通过该 API 快速集成私有知识检索与生成能力，适用于客服问答、技术文档助手、内部知识中枢等场景。所有接口均需通过 [认证](raw/application-api-reference/rag-api/rag-api-authentication.md) 接入。

## 支持的模型与功能

- **基础能力**：文档上传与解析、自动切片（chunking）、向量化嵌入（默认使用 `text-embedding-v3`）、多路召回与重排序；
- **高级功能**：支持基于知识库的流式问答（`/v1/knowledge/query`）、同步任务管理（如触发全量/增量索引重建）、Agent 编排（通过 [Agent 管理](raw/application-api-reference/rag-api/rag-api-agents.md) 接口）；
- **模型兼容性**：问答阶段支持指定 LLM 模型（如 `qwen-max`、`qwen-plus`），但嵌入模型固定为平台托管版本，不可自定义——详见 [知识检索与问答](raw/application-api-reference/rag-api/knowledge.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `knowledge_id` | string | 是 | 知识库唯一标识，需先通过 [知识库](raw/application-api-reference/rag-api/rag-api-knowledge-base.md) 接口创建 |
| `query` | string | 是 | 用户自然语言问题，长度 ≤ 2048 字符 |
| `top_k` | integer | 否 | 检索返回的最相关切片数，默认 3，最大 10 |
| `stream` | boolean | 否 | 是否启用流式响应，默认 `false`；流式模式下需处理 SSE 格式 |
| `retrieval_strategy` | string | 否 | 可选 `hybrid`（关键词+向量）、`vector_only`，默认 `hybrid` |

> **注意**：原始文档中 [数据导入](raw/application-api-reference/rag-api/rag-api-data-import.md) 提到支持 `csv` 和 `jsonl` 批量导入，但实际 API 仅接受 `jsonl` 格式且字段名必须为 `content`（非 `text`），该不一致已在最新 SDK v2.3.0 中修正。

## 使用方式

1. **前置准备**：调用 `/v1/knowledge_bases` 创建知识库 → 上传文档（`/v1/documents`）→ 触发同步（`/v1/sync_jobs`）；
2. **发起问答**：向 `/v1/knowledge/query` 发送 POST 请求，携带 `knowledge_id` 与 `query`；
3. **调试建议**：首次集成时建议先用 [概览](raw/application-api-reference/rag-api/rag-api-overview.md) 中的 cURL 示例验证端到端流程；
4. **错误处理**：常见失败原因包括知识库未就绪（状态非 `active`）、`query` 含控制字符、或超出 [限流](raw/application-api-reference/rag-api/rag-api-rate-limits.md) 配额。

## 限制和注意事项

- 单次请求 `query` 长度上限 2048 字符，超长将被截断且不报错；
- 知识库最大文档数 10,000 份，单文档大小上限 50 MB（PDF/Word）或 10 MB（纯文本）；
- 切片（chunk）默认长度 512 token，不可配置——该行为与 [切片管理](raw/application-api-reference/rag-api/rag-api-chunks.md) 文档描述一致，但与旧版 SDK 注释存在出入；
- 所有[异步任务](../concepts/asynchronous-task.md)（如同步、导入）需轮询 `/v1/sync_jobs/{job_id}` 获取状态，最长等待 30 分钟，超时需重试；
- 流式响应中，`data:` 行末尾无换行符，客户端需按 `\n\n` 边界解析事件，避免粘包。

## 来源文档

- [RAG API](../../raw/application-api-reference/rag-api.md)


