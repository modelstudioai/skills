# rag api

RAG API 是百炼平台提供的知识库管理与检索服务接口，支持知识库全生命周期管理、文档导入、切片操作、跨库语义检索及基于知识的智能问答。所有接口通过 DashScope 网关统一提供，采用标准 RESTful 设计与 Bearer Token 鉴权。开发者需先在控制台获取 API Key 并配置业务空间 ID（`{workspace_id}`）作为 Endpoint 基础路径。

## 支持的模型/功能

RAG API 提供三类核心能力：**知识库管理**（创建、更新、监控、删除）、**数据导入与组织**（类目/文件/连接器管理）、**知识检索与问答**（运行时服务）。  
- **知识库类型**支持 `document`（文档搜索）、`table`（数据查询）、`image`（图片问答）、`multimedia`（音视频搜索），对应不同 `knowledgeType` 与 `knowledgeScene` 组合，例如 `visual_perception_qa` 场景需指定 `multimodalEmbeddingModelName`（如 `qwen3-vl-embedding`）[创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。  
- **检索与问答**依赖 RAG Agent 封装策略，Agent 支持 `chat`（问答）和 `search`（联合检索）两种场景，其 `agent_config` 定义模型（如 `qwen3.7-plus`）、重排（`rerank_top_n`）、知识路由等策略 [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)。  
- **向量模型**可显式指定 `embeddingModelName`（如 `text-embedding-v4`）或 `multimodalEmbeddingModelName`，未指定时使用系统默认值；重排序模型（如 `qwen3-rerank`）在知识库创建或 Agent 配置中设定。

> **注意**：文档 6 中 `knowledgeScene` 列表包含已下线的 `visual_document_qa`，而控制台 UI 已移除该选项，建议仅使用 `basic_document_qa`、`lite_document_qa` 或 `visual_perception_qa`。

## 关键参数

- **通用认证**：所有请求必须携带 `Authorization: Bearer <API-Key>` 头，API Key 在[控制台 API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)获取 [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)。  
- **Endpoint 构造**：Base URL 为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`，其中 `{workspace_id}`（如 `llm-xxxxxxxxxxxx`）需从[业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)页面获取。  
- **参数命名不一致**：知识库管理接口普遍使用 `snake_case`（如 `index_id`, `doc_ids`），但部分接口（如 `/list/index/file/details`）使用 `camelCase`（`indexId`, `pageNumber`）[查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)；删除文档接口明确警告传 `indexId` 会导致 `Index.InvalidParameter` 错误 [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)。  
- **Agent 运行时参数**：`knowledge/search` 和 `knowledge/chat` 接口必须传 `agent_id`（来自已发布的 Agent），且 `knowledge/chat` 要求 `stream=true` 并使用 `Accept: text/event-stream` 头 [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)。

## 使用方式

1. **初始化**：获取 API Key 与 `workspace_id`，构造 Base URL。  
2. **构建知识库**：  
   - 先通过数据导入接口（如 `addCategory` + `applyFileUploadLease` + `addFile`）准备文件 [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)；  
   - 再调用 `/api/v1/indices/rag/index/create_v2` 创建知识库并导入，或先创建后通过 `/api/v1/indices/rag/index/job/create` 追加导入 [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)。  
3. **封装服务能力**：  
   - 使用 Agent 管理 API（`/app/create` → `/app/update` → `/app/deploy`）创建并发布 `chat` 或 `search` Agent，获取 `agent_id` [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)；  
4. **运行时调用**：  
   - 检索：`POST /api/v1/indices/knowledge/search`，传 `agent_id` 与 `query`；  
   - 问答：`POST /api/v2/apps/knowledge/chat`，传 `agent_id` 与 `messages` 数组，必须启用流式响应。  

## 限制和注意事项

- **限流规则**：知识库管理接口有严格 QPS 限制，例如检索 `/rag/index/retrieve` 为 2000 QPS，而 `/rag/index/monitor` 仅 1 QPS；数据导入接口（如 `/describeFile`）上限为 10 QPS [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)。超限返回 HTTP `429`，应按 `Retry-After` 头或指数退避重试。  
- **不可逆操作**：删除知识库（`/index/delete`）、删除文档（`/index/delete_file`）、删除类目（`/deleteCategory`）均为软/硬删除且不可恢复，调用前须确认无业务依赖 [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)。  
- **文件上传约束**：`applyFileUploadLease` 的 `sizeBytes` 必须以**字符串格式**传入（如 `"1048576"`），传数字将失败；`addFile` 的 `category` 参数名易与 `categoryId` 混淆，需特别注意 [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)。  
- **错误处理**：所有错误响应含 `request_id`，联系支持时必须提供；业务错误码（如 `KB_NOT_FOUND`、`RETRIEVAL_TIMEOUT`）需结合 HTTP 状态码（4xx/5xx）判断，`RETRIEVAL_TIMEOUT`（504）建议降低 `top_k` 或切换更小重排模型 [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)。

## 来源文档

- [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
- [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)
- [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)
- [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)
- [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)
- [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md)
- [查询文档列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md)
- [查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)
- [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)
- [查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)
- [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)
- [更新切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)
- [删除切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-delete-chunk.md)
- [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)
- [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)
- [查询任务状态](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)
- [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)
- [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)
- [新增类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)
- [删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)
- [查询文件列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
- [查询连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [新增连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)


