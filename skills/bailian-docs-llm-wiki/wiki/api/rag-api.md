# rag api

RAG API 是百炼平台提供的面向开发者的一套 RESTful 接口，用于程序化管理知识库、导入文档、执行语义检索及调用知识问答服务。所有接口通过 DashScope 网关统一接入，需使用业务空间 ID 拼接 Base URL 并携带 API Key 鉴权。核心能力覆盖从数据准备（类目/文件管理）、知识构建（知识库/切片 CRUD）到运行时服务（检索/问答）的完整 RAG 流程。

## 支持的模型/功能

RAG API 本身不直接暴露大模型调用，而是通过配置驱动的方式集成多种模型能力：

- **嵌入模型（Embedding）**：在创建知识库时通过 `embeddingModelName`（如 `text-embedding-v4`）指定，用于文档向量化；多模态场景需配合 `multimodalEmbeddingModelName`（如 `qwen3-vl-embedding`）[创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。
- **重排序模型（Rerank）**：知识库级配置 `rerankModelName`（如 `qwen3-rerank`），影响检索结果精排质量，可在[查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)响应中查看。
- **问答/检索模型（LLM）**：由 Agent 封装，通过 `agent_config.agent_model`（如 `qwen3.7-plus`）指定，仅在[Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)相关接口中配置，运行时由 `/api/v2/apps/knowledge/chat` 或 `/api/v1/indices/knowledge/search` 调用。
- **解析模型（Parser）**：文件上传时通过 `parser` 字段（如 `DOCMIND_LLM_VERSION`）选择，决定文档结构化解析能力，详见[注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)。

> **注意**：文档中提及的 `visual_document_qa` 场景虽在 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md) 中列出，但明确说明“控制台已不再提供该入口”，建议优先使用 `basic_document_qa` 或 `lite_document_qa`。

## 关键参数

RAG API 参数命名存在不一致，开发者需特别注意：

- **知识库 ID 字段名**：在知识库管理接口中为 `id`（如 [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)），而在文档/切片管理接口中为 `index_id`（如 [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)）或 `indexId`（如 [查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)）。参数名错误将导致 `Index.InvalidParameter` 错误。
- **文件 ID 字段名**：创建知识库时为 `docIds`（数组），而提交导入任务时同样为 `docIds`，但错误信息中可能显示为 `file_ids`，需以实际接口文档为准 [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)。
- **类目 ID 字段名**：在数据导入接口中，`applyFileUploadLease` 和 `addFile` 使用 `category`，而 `listFile` 和 `addFilesFromAuthorizedOss` 使用 `categoryId`，混用会导致参数被忽略 [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)。
- **时间戳格式**：监控接口 `/api/v1/indices/rag/index/monitor` 要求 `startTimestamp` 和 `endTimestamp` 为**秒级** Unix 时间戳（字符串或整数均可），与其他接口常用的毫秒级时间戳不同 [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)。

## 使用方式

### 1. 基础配置
- **Base URL**：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com`，其中 `{workspace_id}` 在控制台[业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)获取。
- **认证**：所有请求必须携带 `Authorization: Bearer <API-Key>` 头，API Key 在控制台 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 获取 [认证方式](../../raw/application-api-reference/rag-api/rag-api-authentication.md)。

### 2. 典型工作流
1. **准备数据**：通过数据导入接口（如 `listCategory`, `applyFileUploadLease`, `addFile`）将文件归类并注册到数据中心。
2. **构建知识库**：调用 `create_v2` 创建知识库并同步导入文件，或先 `create_index` 再 `submit_sync_job` 追加导入。
3. **管理内容**：使用知识库/文档/切片管理接口（如 `update`, `delete_file`, `chunk/create`）维护索引内容。
4. **发布服务**：创建 Agent（`app/create`），配置检索/问答策略，再 `app/deploy` 发布，获取 `agent_id`。
5. **运行时调用**：使用发布的 `agent_id` 调用 `/api/v1/indices/knowledge/search`（检索）或 `/api/v2/apps/knowledge/chat`（问答）。

### 3. 请求示例（检索）
```bash
curl -X POST "https://llm-xxxxxxxxxxxx.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search" \
  -H "Authorization: Bearer $BAILIAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "aid-xxxxxxxxxxxxxxxx",
    "query": "推荐一件适合秋冬的运动夹克"
  }'
```

## 限制和注意事项

- **限流策略**：各接口 QPS 差异显著。检索接口 `/rag/index/retrieve` 最高 2000 QPS，而监控接口 `/rag/index/monitor` 仅 1 QPS；知识库管理类接口普遍为 10 QPS [限流策略](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)。超出限流返回 `429`，应遵循 `Retry-After` 头或指数退避重试。
- **不可逆操作**：删除知识库（`/rag/index/delete`）、删除文档（`/rag/index/delete_file`）、删除切片（`/rag/index/chunk/delete`）均为永久性操作，无回收站机制，调用前务必确认 [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)。
- **Agent 生命周期**：Agent 必须先 `create` → `update`（可选）→ `deploy` 才能被运行时 API 调用。未发布的 Agent 会返回“Agent 未发布”错误。已发布版本的配置无法直接修改，需先 `update` beta 草稿再 `deploy` 新版本 [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)。
- **错误处理**：所有响应均含 `request_id`，排查问题时必须提供此 ID。错误码需结合 HTTP 状态码与响应体 `code` 字段判断，例如 `403 Forbidden` 对应 `FORBIDDEN`，`429` 对应 `RATE_LIMITED` [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)。

## 来源文档

- [API 概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [认证方式](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [限流策略](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
- [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)
- [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)
- [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)
- [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)
- [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md)
- [查询文档列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md)
- [查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)
- [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)
- [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)
- [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)
- [查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)
- [更新切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)
- [删除切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-delete-chunk.md)
- [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)
- [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)
- [查询任务状态](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)
- [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)
- [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)
- [删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)
- [新增类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)
- [查询文件列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [新增连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [查询连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)


