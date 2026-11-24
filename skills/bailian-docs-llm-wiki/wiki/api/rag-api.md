# rag api

RAG API（现称 Knowledge API）是阿里云百炼平台提供的知识库全生命周期管理与运行时服务接口，覆盖知识库创建、文档导入、切片管理、语义检索及智能问答等核心能力。所有接口通过统一的业务空间 Endpoint 提供服务，采用 API Key 鉴权，并严格遵循 HTTPS + JSON 协议约定。开发者需先在控制台获取 API Key 并确认业务空间 ID，方可调用 [API 总览](../../raw/application-api-reference/rag-api/rag-api-overview.md) 中定义的各组接口。

## 支持的模型/功能

- **知识库类型**：支持 `document`（文档搜索）、`table`（数据查询）、`image`（图片问答）、`multimedia`（音视频搜索）四类知识场景，对应不同结构类型（`unstructured` 或 `structured`）与嵌入/重排模型组合。
- **嵌入模型**：默认使用 `text-embedding-v3`，可显式指定 `text-embedding-v4`、`qwen3.7-text-embedding` 等；多模态场景（如 `image_qa`）必须配置 `multimodalEmbeddingModelName`（如 `qwen3-vl-embedding`），详见 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。
- **重排序模型**：默认为 `qwen3-rerank`，可在知识库创建或更新时通过 `rerankModelName` 指定；检索超时错误 `RETRIEVAL_TIMEOUT` 明确建议“降低 top_k 或启用更小的重排模型”，见 [错误码文档](../../raw/application-api-reference/rag-api/rag-api-errors.md)。
- **高级功能**：旗舰版知识库（`pipelineCommercialType=enterprise`）支持 Wiki 与本体知识图谱，需在 `create_v2` 请求中配置 `wikiEnabled=true` 及 `wikiConfig.extraction.synthesisModelId`（如 `qwen3.8-max`），详见 [Wiki API](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-wiki.md)。

> **注意**：文档 7 与文档 10 对 `knowledgeScene` 的取值约束存在不一致：文档 7 允许 `visual_document_qa`（但注明“控制台已不再提供该入口”），而文档 10 明确要求 Wiki 场景必须为 `basic_document_qa`。实际开发应以 Wiki 功能的强制约束为准，即开启 Wiki 时 `knowledgeScene` 必须为 `basic_document_qa`。

## 关键参数

- **通用认证**：所有请求必须携带 `Authorization: Bearer <API-Key>` 头，API Key 在 [认证文档](../../raw/application-api-reference/rag-api/rag-api-authentication.md) 中说明获取方式。
- **业务空间标识**：Endpoint 中的 `{workspace_id}`（如 `llm-xxxxxxxxxxxx`）是必需路径前缀，非 query 参数。
- **知识库 ID**：各接口对 ID 字段命名不统一：`delete` 接口使用 `index_id`（snake_case），而 `update`、`monitor`、`list-chunks` 等多数接口使用 `id` 或 `indexId`（camelCase）。例如，[删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md) 要求 `index_id`，而 [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md) 要求 `id`。
- **文件/文档标识**：数据导入相关接口（如 `applyFileUploadLease`、`addFile`）使用 `category`（非 `categoryId`）作为类目参数名；而 `listFile`、`oss-import` 等接口则使用 `categoryId`，需严格区分。
- **检索过滤**：`search_filters` 语法支持 `_operator` 和嵌套 `_conditions` 表达 OR 条件，具体规则见 [知识库 SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 使用方式

1. **初始化配置**：设置 `BASE_URL=https://{workspace_id}.cn-beijing.maas.aliyuncs.com` 和环境变量 `BAILIAN_API_KEY`。
2. **知识库管理**：
   - 创建：调用 `POST /api/v1/indices/rag/index/create_v2`，传入 `name`、`structureType`、`sourceType`、`docIds` 等必填字段。
   - 查询列表：`GET /api/v1/indices/rag/index/list`（query string 传参）。
   - 更新/删除：分别使用 `POST /api/v1/indices/rag/index/update` 和 `POST /api/v1/indices/rag/index/delete`。
3. **数据导入**：
   - 三步流程：`applyFileUploadLease` → OSS PUT 上传 → `addFile` 注册。
   - 批量导入：`addFilesFromAuthorizedOss` 需提前授权 SLR 角色，见 [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)。
4. **运行时服务**：
   - **知识检索**：`POST /api/v1/indices/knowledge/search`，需已发布检索服务并传 `agent_id` 与 `query`。
   - **知识问答**：`POST /api/v2/apps/knowledge/chat`，**必须**设 `stream=true`，且仅支持 SSE 流式响应。

## 限制和注意事项

- **限流策略**：知识库管理接口按 QPS 限流（如 `/rag/index/retrieve` 为 2000 QPS），而知识检索与问答接口按“每 10 秒请求数”限流（默认 10 次/10 秒）。超限返回 HTTP 429，需按 `Retry-After` 头或指数退避重试，详见 [限流文档](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)。
- **不可逆操作**：删除知识库（`/rag/index/delete`）、删除类目（`/dash/deleteCategory`）、删除切片（`/rag/index/chunk/delete`）均为永久性操作，无回收站机制。
- **参数兼容性**：部分接口存在命名冲突或静默忽略行为。例如，`listCategory` 的 `maxResult` 参数若误传为 `maxResults` 将被静默忽略；`delete_file` 接口若传 `IndexId` 会返回误导性错误信息 `Required parameter(IndexId) missing or invalid`，但正确参数名是 `index_id`（见 [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)）。
- **错误处理**：所有响应含 `request_id`，联系支持时必须提供；业务错误码（如 `KB_NOT_FOUND`、`RATE_LIMITED`）与 HTTP 状态码需联合判断，重试策略详见 [错误码文档](../../raw/application-api-reference/rag-api/rag-api-errors.md)。

## 来源文档

- [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [Knowledge（原RAG） API 错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
- [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)
- [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)
- [Wiki API](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-wiki.md)
- [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)
- [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md)
- [查询文档列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md)
- [查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)
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
- [新增类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)
- [删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)
- [查询文件列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)
- [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)
- [查询数据集](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)
- [新增数据集](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)


