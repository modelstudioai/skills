# rag api

RAG API 是阿里云百炼平台提供的知识库管理与检索服务接口，支持知识库全生命周期操作（创建、更新、监控、删除）、文档与切片的精细化管理、多源数据导入，以及基于 Agent 的知识检索与问答能力。所有接口通过 DashScope 网关统一提供，采用标准 RESTful 设计与 Bearer Token 鉴权。

## 支持的模型/功能

RAG API 不直接暴露大模型调用，而是通过预置模型能力支撑上层功能：
- **嵌入模型**：`embeddingModelName`（如 `text-embedding-v4`）用于非结构化知识库向量化；`multimodalEmbeddingModelName`（如 `qwen3-vl-embedding`）用于图片问答、视觉理解等多模态场景，详见[创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。
- **重排序模型**：`rerankModelName`（如 `qwen3-rerank`）在检索后对结果进行精排，其配置（`rerankTopN`、`rerankMinScore`）可于知识库级别设置或在 Agent 中按知识库粒度覆盖。
- **Agent 能力封装**：知识检索（`/api/v1/indices/knowledge/search`）与知识问答（`/api/v2/apps/knowledge/chat`）均依赖 RAG Agent 实例，其 `agent_config` 中定义了模型（`agent_model`，如 `qwen3.7-plus`）、策略（`agent_policy`：`turbo` 或 `agentic`）、路由、混排及安全策略等，详见[Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)。

> **注意**：文档 6 明确指出 `knowledgeScene` 为 `lite_document_qa`（极速问答）时 `sinkType` 必须为 `BUILT_IN`；而文档 35 和 37 均强调运行时 API（`knowledge/search` / `knowledge/chat`）必须使用已发布的 Agent ID（`agent_id`），否则返回“Agent 未发布”错误——这表明模型与策略的实际生效依赖于 Agent 的发布状态，而非知识库创建时的静态配置。

## 关键参数

- **认证与路由**：所有请求需携带 `Authorization: Bearer <API-Key>` 头，并使用业务空间 ID 构造 Base URL：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com`。API Key 获取方式见[认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)。
- **知识库标识**：多数接口使用 `indexId`（camelCase）作为路径或请求体参数（如 `/rag/index/update`、`/rag/list/index/file/details`），但部分接口（如 `/rag/index/delete_file`、`/rag/index/delete`）明确要求 `index_id`（snake_case），命名不一致需特别注意。
- **文件与切片标识**：文档操作中 `doc_ids`（snake_case）为数组，而切片操作中 `chunkIds`（camelCase）亦为数组；`dataId`（新增切片）、`docId`（查询切片列表）等字段名也存在大小写与语义差异。
- **Agent 相关**：运行时 API 必须传 `agent_id`；`kb_search_configs` 允许为每个知识库指定 `search_filters` 进行文档/标签过滤，其语法详见[知识库 SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 使用方式

1. **准备凭证**：在控制台获取 API Key 与业务空间 ID（`workspace_id`）。
2. **管理知识库**：使用 `/api/v1/indices/rag/index/` 前缀接口，例如：
   - 创建：`POST /api/v1/indices/rag/index/create_v2`（一步创建+导入）
   - 查询列表：`GET /api/v1/indices/rag/index/list`
   - 更新：`POST /api/v1/indices/rag/index/update`（注意参数名为 `id`）
   - 删除：`POST /api/v1/indices/rag/index/delete`（不可逆）
3. **管理文档与切片**：
   - 文档：`/api/v1/indices/rag/index/files`（GET 列表）、`/api/v1/indices/rag/index/delete_file`（POST 删除）
   - 切片：`/api/v1/indices/rag/index/chunklist`（POST 查询）、`/api/v1/indices/rag/index/chunk/update`（POST 更新，注意 `content` 长度 10–6000 字符）
4. **数据导入**：使用 `/api/v1/connector/dash/` 前缀，完成类目管理（`listCategory`/`addCategory`）、文件上传（三步：`applyFileUploadLease` → OSS PUT → `addFile`）及批量导入（`addFilesFromAuthorizedOss`）。
5. **运行知识服务**：
   - 先通过 Agent 管理 API（`/api/v1/indices/rag/app/`）创建、配置并[发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)；
   - 再调用运行时 API：`POST /api/v1/indices/knowledge/search`（联合检索）或 `POST /api/v2/apps/knowledge/chat`（SSE 流式问答），传入 `agent_id` 及意图（`query`/`images`）。

## 限制和注意事项

- **限流规则**：知识库管理接口按 QPS 限流（如 `/rag/index/retrieve` 为 2000 QPS），知识检索与问答接口按每 10 秒请求数限流（默认 10 次）。超限返回 HTTP `429`，需按 `Retry-After` 头或指数退避重试，详见[限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)。
- **参数命名不一致**：`indexId` vs `index_id`、`docIds` vs `doc_id`、`pageNumber`（`/list/index/file/details`）vs `page_number`（`/index/files`）等，务必严格按各接口文档要求传参，错误命名将导致 `InvalidParameter`。
- **不可逆操作**：删除知识库（`/rag/index/delete`）、删除文档（`/rag/index/delete_file`）、删除类目（`/dash/deleteCategory`）均为软/硬删除且不可恢复，调用前需二次确认。
- **Agent 生命周期约束**：`agent_config` 仅允许修改 `beta` 草稿版本；已发布版本只能修改 `agent_version_desc`。要更新线上配置，必须先 `update` 草稿再 `deploy` 发布新版本，详见[更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)。
- **错误处理**：所有错误响应均为统一 JSON 结构，含 `error.code`（如 `INVALID_PARAMETER`）、`error.message` 和 `request_id`。排查问题时务必提供 `request_id`，详见[RAG API 错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)。

## 来源文档

- [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [RAG API 错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
- [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)
- [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)
- [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md)
- [查询文档列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md)
- [查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)
- [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)
- [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)
- [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)
- [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)
- [更新切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)
- [删除切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-delete-chunk.md)
- [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)
- [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)
- [查询任务状态](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)
- [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)
- [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)
- [新增类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)
- [删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)
- [查询文件列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
- [新增数据集](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)
- [查询数据集](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)


