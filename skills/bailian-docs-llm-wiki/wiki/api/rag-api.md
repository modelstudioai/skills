# rag api

RAG API 是阿里云百炼平台提供的知识增强型应用开发接口，支持知识库全生命周期管理、多源数据导入、语义检索与智能问答三大核心能力。所有接口均通过 DashScope 网关统一提供 HTTPS 服务，采用 API Key 鉴权，并严格遵循 RESTful 设计规范。开发者可通过编程方式构建端到端的 RAG 应用，无需依赖控制台操作。

## 支持的模型/功能

RAG API 提供两类核心运行时能力：**知识检索**（`/api/v1/indices/knowledge/search`）和**知识问答**（`/api/v2/apps/knowledge/chat`），二者均基于已发布的 Agent 实例调用，其底层策略（如多库权重、混排模型、知识路由等）在 Agent 配置中预设，运行时仅需传入 `agent_id` 和检索意图（`query` 或 `images`）。Agent 的创建、配置、发布与查询由独立的 [Agent 管理 API](../../raw/application-api-reference/rag-api/rag-api-agents.md) 支持，形成“管理-运行”分离的清晰架构。

知识库侧支持多种结构类型（`unstructured`/`structured`）与知识类型（`document`/`table`/`image`/`multimedia`），并可为不同场景（如 `lite_document_qa`、`visual_perception_qa`）指定专用嵌入模型（`embeddingModelName`）或多模态嵌入模型（`multimodalEmbeddingModelName`）。例如，`visual_perception_qa` 场景必须显式传入 `multimodalEmbeddingModelName`，否则返回 `invalid multi embedding model` 错误 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。

## 关键参数

- **认证参数**：所有请求必须携带 `Authorization: Bearer <API-Key>` 头，API Key 在 [控制台 API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 获取；业务空间 ID（`{workspace_id}`）用于构造 Base URL（`https://{workspace_id}.cn-beijing.maas.aliyuncs.com`）。
- **知识库标识**：各接口对知识库 ID 的参数名不一致，需特别注意：`delete_index` 接口使用 `index_id`，`update_index` 使用 `id`，而 `list_file_details` 使用 `indexId`；文档删除接口 `delete_file` 明确要求 `index_id`（非 `IndexId`），否则返回 `Index.InvalidParameter` [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)。
- **文件与切片参数**：[文件上传](../concepts/file-upload.md)流程中，`applyFileUploadLease` 要求 `sizeBytes` 必须以**字符串格式**传入（如 `"1048576"`），传数字将失败；`addFile` 接口的类目 ID 参数名为 `category`（非 `categoryId`），与 `listFile` 等接口不一致，易引发错误 [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)。
- **Agent 运行时参数**：知识问答接口 `knowledge/chat` 的 `stream` 字段**必须为 `true`**，当前版本不支持非流式响应；知识检索接口 `knowledge/search` 的 `kb_search_configs` 中 `search_filters` 会追加到离线配置末尾（AND 关系），而非替换 [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)。

> **注意**：`listCategory` 和 `listFile` 接口的分页参数名为 `maxResult`（单数），若误传 `maxResults`（复数）会被静默忽略，导致分页失效 [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)。

## 使用方式

1. **准备凭证**：获取 API Key 和业务空间 ID，构造 Base URL。
2. **管理数据源**：通过 `/api/v1/connector/dash/` 前缀接口管理类目（`addCategory`/`listCategory`）、文件（`applyFileUploadLease` → `addFile`）及连接器（`addConnector`）。
3. **构建知识库**：调用 `/api/v1/indices/rag/index/` 前缀接口创建（`create_v2`）、更新（`update`）、监控（`monitor`）知识库；或直接导入（`job/create`）。
4. **管理内容**：对知识库内文档（`files`/`delete_file`）和切片（`chunk/create`/`chunklist`/`chunk/update`）进行增删改查。
5. **发布能力**：使用 `/api/v1/indices/rag/app/` 前缀接口创建、配置、发布 Agent（`create` → `update` → `deploy`）。
6. **调用服务**：使用 `/api/v1/indices/knowledge/search` 或 `/api/v2/apps/knowledge/chat` 发起运行时请求，传入发布的 `agent_id`。

所有接口均返回标准 JSON 响应，成功时 `code` 为 `"Success"`，失败时 `error.code` 携带业务错误码（如 `INVALID_PARAMETER`、`KB_NOT_FOUND`），并附带 `request_id` 用于问题定位 [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)。

## 限制和注意事项

- **限流规则**：知识库管理接口中，`/rag/index/retrieve`（检索）QPS 上限为 2000，而 `/rag/index/monitor`（监控）仅为 1；运行时接口（`knowledge/search` 和 `knowledge/chat`）默认用户维度 25 QPS。超限返回 HTTP `429`，建议按 `Retry-After` 头或指数退避重试 [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)。
- **不可逆操作**：`delete_index`（删除知识库）、`delete_file`（删除文档）、`delete_chunk`（删除切片）均为永久性操作，无回收站机制，调用前务必确认。
- **参数兼容性**：`create_v2` 接口的 `docIds` 字段名与错误提示中的 `file_ids` 不一致；`submit_sync_job` 接口若未传 `sourceType`，将默认导入整个数据中心，存在安全风险 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。
- **协议约束**：所有接口强制 HTTPS，请求体与响应体必须为 UTF-8 编码 JSON；GET 接口参数通过 query string 传递（如 `list-indices`），POST 接口参数在 body 中（如 `create_v2`），具体方法以各接口文档为准 [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)。

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
- [新增类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)
- [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)
- [删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)
- [查询文件列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)
- [查询连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)
- [新增连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)


