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

3. **响应结构**：包含 `answer`（LLM生成答案）、`retrieved_chunks`（原始片段列表及来源文档）、`usage`（token消耗统计）。完整字段定义见 [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)。

## 限制和注意事项

- **速率限制**：默认 10 QPS / key，突发峰值不超过 30 QPS；超出将返回 `429 Too Many Requests`，具体策略参见 [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)。
- **文档大小**：单文件上限 100 MB；PDF 超过 500 页建议预处理分卷。
- **切片长度**：默认 chunk size 为 512 token，最小不可低于 64；过短切片将显著降低检索精度，详见 [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)。
- **敏感内容过滤**：所有上传文档在切片前会经内容安全检测，含违规文本的文档将被拒绝并返回错误码 `INVALID_DOCUMENT_CONTENT`。

## 来源文档

- [RAG API](../../raw/application-api-reference/rag-api.md)


