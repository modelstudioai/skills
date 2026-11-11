# rag api

RAG API 是百炼平台提供的面向[检索增强生成](../concepts/rag.md)（RAG）场景的核心服务接口，支持知识库构建、文档切片、异步同步、语义检索与问答等端到端能力。开发者可通过该 API 快速集成私有知识检索功能，无需自行搭建向量数据库或编排检索流程。所有接口均需通过 Bearer Token 认证，详见 [RAG API](../../raw/application-api-reference/rag-api.md)。

## 支持的模型与功能

- **基础模型支持**：当前仅支持 `qwen-max` 和 `qwen-plus` 作为 RAG 问答阶段的 LLM 后端；其他模型（如 `qwen-turbo`）暂不支持生成式问答，仅可用于向量化（embedding）任务。
- **核心功能模块**：
  - 知识库生命周期管理（创建/删除/更新）
  - 文档上传与元数据标注（支持 PDF/DOCX/TXT/MD 等格式）
  - 自动切片（chunking）与可配置分块策略（按段落、固定长度、语义边界）
  - 异步知识同步任务（`sync_job`）状态轮询与结果获取
  - 检索增强问答（`/v1/knowledge/query`），支持 `top_k`、`score_threshold`、`enable_rerank` 等控制参数  
  > **注意**：[知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md) 中提及的 `qwen-14b-chat` 已于 v2.3 版本下线，实际调用将返回 400 错误；请以 [RAG API](../../raw/application-api-reference/rag-api.md) 的“支持模型”章节为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `knowledge_id` | string | 是 | 知识库唯一标识，由 `/v1/knowledge_bases` 创建后返回 |
| `query` | string | 是 | 用户自然语言问题，最大长度 2048 字符 |
| `top_k` | integer | 否 | 检索返回的最相关片段数，默认 3，范围 1–50 |
| `score_threshold` | float | 否 | 向量相似度阈值（0.0–1.0），低于此值的片段将被过滤，默认 0.3 |
| `enable_rerank` | boolean | 否 | 是否启用重排序（cross-encoder），默认 `false`；启用后延迟增加约 300–800ms |

> **注意**：`score_threshold` 的实际生效逻辑依赖于向量索引类型（HNSW vs IVF），详细行为请参考 [RAG API](../../raw/application-api-reference/rag-api.md) 中“检索原理”附录。

## 使用方式

1. **前置准备**：  
   - 创建知识库（`POST /v1/knowledge_bases`）→ 获取 `knowledge_id`  
   - 上传文档（`POST /v1/knowledge_bases/{kb_id}/documents`）→ 触发自动切片与嵌入  
   - 等待同步任务完成（轮询 `GET /v1/sync_jobs/{job_id}`，状态为 `succeeded`）

2. **发起问答请求**：  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/knowledge/query \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "knowledge_id": "kb-xxx",
           "query": "百炼平台如何配置RAG应用？",
           "top_k": 5,
           "enable_rerank": true
         }'
   ```

3. **响应结构**：包含 `answer`（LLM生成答案）、`references`（来源片段列表，含 `chunk_id`、`content`、`score`、`document_title`）和 `usage`（token消耗统计）。

## 限制和注意事项

- **配额限制**：单次问答请求最大 `top_k=50`；单知识库最多容纳 100 万切片；详见 [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md) 文档。
- **文档处理限制**：PDF 文件最大 100MB，且不支持加密或扫描版（需 OCR 预处理）；DOCX 中的复杂表格可能解析异常。
- **异步任务超时**：同步任务（如文档解析）默认超时 30 分钟，超时后状态置为 `failed`，需检查 [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md) 中的错误日志字段。
- **调试建议**：首次集成时，建议先调用 `/v1/knowledge/query?debug=true` 获取中间检索结果（`retrieved_chunks`），验证切片质量与相关性。

## 来源文档

- [RAG API](../../raw/application-api-reference/rag-api.md)


