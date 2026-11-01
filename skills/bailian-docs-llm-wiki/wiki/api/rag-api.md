# rag api

RAG API 是阿里云百炼平台提供的知识库管理与检索服务接口，支持知识库全生命周期操作（创建、更新、监控、删除）、文档与切片的精细化管理、多源数据导入，以及基于知识库的语义检索与智能问答。所有接口通过统一的 DashScope 网关提供服务，采用标准 RESTful 设计与 API Key 鉴权机制。

## 支持的模型/功能

RAG API 本身不直接暴露大语言模型调用，但深度集成多种向量与重排模型，并通过 Agent 封装能力：
- **嵌入模型**：支持 `text-embedding-v4` 等文本嵌入模型，可在创建知识库时通过 `embeddingModelName` 指定；图片/多模态场景需使用 `qwen3-vl-embedding` 等专用模型，通过 `multimodalEmbeddingModelName` 参数配置 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。
- **重排模型**：默认使用 `qwen3-rerank`，可在知识库创建或更新时配置 `rerankModelName`，其行为受 `rerankMinScore`、`rerankTopN` 等参数控制 [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)。
- **核心功能分组**：
  - **知识库管理**：CRUD、监控（存储/QPS）、切片管理；
  - **数据导入**：类目/连接器管理、OSS 批量导入、文件注册与标签管理；
  - **知识检索与问答**：`/api/v1/indices/knowledge/search`（联合多库语义检索）与 `/api/v2/apps/knowledge/chat`（SSE 流式问答），二者均依赖预先创建并发布的 RAG Agent 实例 [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)。

> **注意**：文档中提及的 `lite_document_qa` 场景要求 `sinkType` 必须为 `BUILT_IN`，而 `visual_perception_qa` 和 `image_qa` 场景则强制要求传入有效的 `multimodalEmbeddingModelName`，否则将返回 `invalid multi embedding model` 错误。这些约束在创建知识库时必须严格满足。

## 关键参数

- **认证与路由**：所有请求必须携带 `Authorization: Bearer <API-Key>` 头，并使用形如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com` 的 Base URL，其中 `{workspace_id}` 为业务空间 ID [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)。
- **知识库标识**：不同接口使用不一致的参数名表示知识库 ID —— `id`（`/update`）、`index_id`（`/delete_file`）、`pipelineId`（`/chunk/create`）、`indexId`（`/chunklist`），开发者需严格按各接口文档要求传参，错误命名将导致 `Index.InvalidParameter` 错误 [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)、[删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)。
- **文件与切片标识**：`docIds`（创建知识库时传入）、`doc_id`（响应中返回）、`doc_ids`（删除文档时使用 snake_case）存在命名差异；切片 ID 在响应中位于 `node.metadata._id` 字段，用于 `update`/`delete` 操作 [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)、[更新切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)。
- **Agent 调用必需参数**：知识检索与问答运行时接口（`/knowledge/search`、`/knowledge/chat`）必须传入 `agent_id`，该 ID 来源于 Agent 管理 API 创建并发布的实例，而非知识库 ID [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)。

## 使用方式

1. **准备凭证**：在百炼控制台 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 获取 API Key，并确保 RAM 子账号已获得 `AliyunBailianDataFullAccess` 权限 [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)。
2. **构建知识库**：调用 `/api/v1/indices/rag/index/create_v2` 一步创建知识库并导入文件；或先创建知识库，再通过 `/api/v1/indices/rag/index/job/create` 提交追加导入任务 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。
3. **管理数据源**：使用 `/api/v1/connector/dash/` 前缀接口管理类目（`addCategory`/`listCategory`）、连接器（`addConnector`）及文件（`applyFileUploadLease` → `addFile` → `listFile`）[数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)。
4. **执行检索/问答**：
   - **检索**：调用 `/api/v1/indices/knowledge/search`，传入 `agent_id` 和 `query`（或 `images`），可选 `kb_search_configs` 进行知识库级过滤。
   - **问答**：调用 `/api/v2/apps/knowledge/chat`，`stream` 必须为 `true`，`input.messages` 需包含完整对话历史，`parameters.agent_options.agent_id` 指向已发布 Agent [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)。
5. **监控与运维**：使用 `/api/v1/indices/rag/index/monitor` 查询知识库存储与 QPS 监控数据，时间戳需为秒级 Unix 时间戳 [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)。

## 限制和注意事项

- **限流策略**：知识库管理接口有严格 QPS 限制，例如检索 `/rag/index/retrieve` 为 2000 QPS，而 `/rag/index/monitor` 仅为 1 QPS；知识检索与问答运行时接口默认用户维度 25 QPS [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)。超限返回 `429 Too Many Requests`，应遵循 `Retry-After` 头或指数退避重试。
- **不可逆操作**：删除知识库（`/delete`）、删除文档（`/delete_file`）、删除切片（`/chunk/delete`）、删除类目（`/deleteCategory`）均为软删除或永久删除，操作后数据无法恢复，调用前务必确认 [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)、[删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)。
- **参数兼容性**：`/list/index/file/details` 接口使用 camelCase（`pageNumber`/`pageSize`），而 `/list` 类查询接口普遍使用 snake_case（`page_number`/`page_size`）；`addFile` 接口的类目参数名为 `category`，非 `categoryId`，与 `listFile` 等接口不一致 [查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)、[注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)。
- **Agent 生命周期**：Agent 必须先通过管理 API（`/app/create` → `/app/update` → `/app/deploy`）创建并发布，才能被运行时接口调用；已发布版本的 `agent_config` 不可直接修改，需先更新 `beta` 草稿再重新发布 [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)。

## 来源文档

- [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
- [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)
- [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)
- [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)
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
- [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)
- [新增类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)
- [删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)
- [查询文件列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)
- [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
- [新增连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [查询连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)


