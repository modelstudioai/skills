# rag api

RAG API 是阿里云百炼平台提供的知识库管理与检索服务接口，支持知识库全生命周期操作（创建、更新、删除、监控）、文档与切片的精细化管理、数据源导入，以及基于 Agent 的知识检索与问答能力调用。所有接口通过统一的业务空间 Endpoint 访问，采用 API Key 鉴权，返回结构化 JSON 响应。

## 支持的模型/功能

RAG API 提供三类核心能力：**知识库管理**（`/api/v1/indices/rag/`）、**数据导入**（`/api/v1/connector/dash/`）和**知识检索与问答**（`/api/v1/indices/knowledge/search` 与 `/api/v2/apps/knowledge/chat`）。  
- **知识库类型**支持 `document`（文档搜索）、`table`（数据查询）、`image`（图片问答）、`multimedia`（音视频搜索），对应不同 `structureType`（`unstructured` 或 `structured`）与 `knowledgeScene`（如 `basic_document_qa`、`image_qa`）组合 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。  
- **嵌入与重排模型**可自定义：`embeddingModelName`（如 `text-embedding-v4`）、`multimodalEmbeddingModelName`（如 `qwen3-vl-embedding`）、`rerankModelName`（如 `qwen3-rerank`），均在创建或更新知识库时指定 [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)。  
- **Agent 能力封装**：通过 Agent 管理 API（`/api/v1/indices/rag/app/`）创建、配置、发布 `chat` 或 `search` 场景的 Agent，其 `agent_config` 定义模型（`qwen3.7-plus`）、策略（`turbo`/`agentic`）、安全开关（防泄漏、拒答）及知识库路由规则 [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)。

## 关键参数

- **认证与地址**：所有请求需携带 `Authorization: Bearer <API-Key>` 头，并使用 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com` 作为 Base URL，其中 `{workspace_id}` 在控制台业务空间管理页获取 [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)。  
- **知识库标识**：各接口对知识库 ID 的参数名不一致——`index_id`（如 `/delete_file`）、`indexId`（如 `/list/index/file/details`）、`id`（如 `/update`），开发者需严格按接口文档传参，否则返回 `Index.InvalidParameter` [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)。  
- **文件与类目参数**：数据导入接口中，`category` 字段用于指定类目 ID（非 `categoryId`），且 `sizeBytes` 必须以字符串格式传入（如 `"1048576"`），数字格式将导致失败 [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)。  
- **运行时必填项**：知识问答（`/knowledge/chat`）要求 `stream=true` 且 `input.messages` 包含完整多轮历史；知识检索（`/knowledge/search`）必须传入已发布的 `agent_id`，否则报“Agent 未发布”错误 [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)。

> **注意**：文档 6 中 `knowledgeScene` 列出的 `visual_document_qa` 场景，在文档 5 的目录索引及控制台 UI 中已移除，属历史遗留字段，实际调用时请避免使用。

## 使用方式

1. **初始化**：在[控制台 API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)获取 API Key，确认业务空间 ID。  
2. **构建知识库**：  
   - 创建类目（`/addCategory`）→ 上传文件（`/applyFileUploadLease` → OSS PUT → `/addFile`）→ 创建知识库（`/create_v2`）或提交导入任务（`/job/create`）。  
3. **管理内容**：  
   - 文档操作：`/files`（查）、`/list/index/file/details`（详情）、`/delete_file`（删）；  
   - 切片操作：`/chunklist`（查）、`/chunk/create`（增）、`/chunk/update`（改）、`/chunk/delete`（删）。  
4. **启用检索/问答**：  
   - 先通过 Agent 管理 API 创建并发布 Agent（`/app/create` → `/app/deploy`），获取 `agent_id`；  
   - 再调用运行时接口：`POST /knowledge/search`（文本/多模态检索）或 `POST /knowledge/chat`（SSE 流式问答），传入 `agent_id` 和意图（`query`/`images` 或 `messages`）。

## 限制和注意事项

- **限流规则**：知识库管理接口按 QPS 限流（如 `/retrieve` 为 2000 QPS），知识检索与问答接口按每 10 秒请求数限流（默认 10 次） [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)。超限返回 HTTP `429`，需按 `Retry-After` 头或指数退避重试。  
- **不可逆操作**：删除知识库（`/delete`）、删除文档（`/delete_file`）、删除切片（`/chunk/delete`）均为永久删除，无回收站 [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)。  
- **参数兼容性**：`/listCategory` 接口的分页参数为 `maxResult`（单数），传 `maxResults` 会被静默忽略；`/listFile` 的 `fileIds` 最多支持 20 个 [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)。  
- **错误处理**：所有错误响应含 `request_id`，联系支持时必须提供；业务错误码（如 `KB_NOT_FOUND`、`RETRIEVAL_TIMEOUT`）需结合 HTTP 状态码（404/504）综合判断 [RAG API 错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)。

## 来源文档

- [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [RAG API 错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
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
- [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)
- [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)
- [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)
- [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)
- [查询任务状态](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)
- [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)
- [新增类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)
- [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)
- [删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)
- [查询文件列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)
- [新增数据集](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [查询数据集](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)


