# rag api

RAG API 是百炼平台提供的知识库全生命周期管理与语义检索/问答服务接口集合，覆盖知识库创建、文档导入、切片管理、监控、Agent 配置及运行时检索与问答等能力。所有接口通过统一的业务空间 Endpoint 提供 HTTPS 服务，采用 API Key 鉴权，请求与响应均为 UTF-8 编码的 JSON 格式。开发者需先在控制台获取 API Key 并确认业务空间 ID，方可调用 [API 总览](../../raw/application-api-reference/rag-api/rag-api-overview.md) 中定义的各组接口。

## 支持的模型/功能

RAG API 支持以下核心功能模块：

- **知识库管理**：支持创建（`/api/v1/indices/rag/index/create_v2`）、查询列表（`/api/v1/indices/rag/index/list`）、更新（`/api/v1/indices/rag/index/update`）、删除（`/api/v1/indices/rag/index/delete`）及监控（`/api/v1/indices/rag/index/monitor`）。知识库类型（`knowledgeType`）包括 `document`（文档搜索）、`table`（数据查询）、`image`（图片问答）、`multimedia`（音视频搜索），需与 `structureType`（`unstructured`/`structured`）匹配；使用场景（`knowledgeScene`）如 `basic_document_qa`、`lite_document_qa`（要求 `sinkType="BUILT_IN"`）等需显式指定 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。
- **数据导入**：提供类目管理（`/api/v1/connector/dash/listCategory` 等）、文件上传三步流程（申请租约 → OSS PUT → 注册文件）、OSS 批量导入（`/api/v1/connector/dash/addFilesFromAuthorizedOss`）及标签管理。注意：`applyFileUploadLease` 要求 `sizeBytes` 必须以字符串格式传入，且 `addFile` 接口参数名为 `category`（非 `categoryId`）[申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)。
- **切片管理**：支持新增（`/api/v1/indices/rag/index/chunk/create`）、查询（`/api/v1/indices/rag/index/chunklist`）、更新（`/api/v1/indices/rag/index/chunk/update`）和删除（`/api/v1/indices/rag/index/chunk/delete`）切片。文档搜索类知识库切片内容字段固定为 `content`/`title`/`image_urls`；表格类知识库则按 Excel 列标题动态映射字段 [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)。
- **Agent 管理**：提供 RAG Agent 全生命周期操作（创建、更新、发布、删除、查询），用于封装检索策略或问答逻辑。Agent 分 `chat`（问答）与 `search`（检索）场景，配置通过 `agent_config` 定义，仅 `beta` 草稿版本允许修改配置；已发布版本仅能修改描述，如需更新配置须先 `update` 草稿再 `deploy` 发布新版本 [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)。
- **运行时服务**：包含知识检索（`POST /api/v1/indices/knowledge/search`）与知识问答（`POST /api/v2/apps/knowledge/chat`）两个流式接口。二者均依赖预先创建并发布的 Agent 实例（`agent_id`），不直接暴露底层检索参数，策略由 `agent_config` 统一管控。

> **注意**：文档 35 和文档 36 均指出知识检索接口路径为 `/api/v1/indices/knowledge/search`，但文档 35 将其归类为“DashScope 应用网关”体系，而文档 36 明确其 Base URL 与 OpenAPI 一致（`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`）。实际调用应以文档 36 的说明为准，即该接口属于 RAG API 统一网关，无需额外网关跳转。

## 关键参数

- **通用参数**：
  - `Authorization`: `Bearer <API-Key>`，必填，从[控制台 API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)获取。
  - `Base URL`: `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`，其中 `{workspace_id}` 为业务空间 ID，在[业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)中查看。
- **知识库相关**：
  - `index_id` / `id`: 知识库 ID，创建后返回于 `data.id` 字段；注意删除接口（文档 8）使用 `index_id`，而更新接口（文档 7）使用 `id`，命名不一致。
  - `docIds`: 文件 ID 列表，用于创建知识库或提交导入任务；参数名统一为 `docIds`（非 `file_ids` 或 `fileIds`），但错误提示中可能显示 `file_ids`（见文档 6 警告）。
- **Agent 相关**：
  - `agent_id`: 运行时接口（`knowledge/search` / `knowledge/chat`）必需，由 Agent 管理 API 创建并发布后生成。
  - `agent_scene`: 创建/更新 Agent 时必填，取值 `chat` 或 `search`，决定 Agent 类型及 `agent_config` 结构。
- **分页与过滤**：
  - `page_number` / `page_size`: 多数 GET 查询接口（如文档列表、知识库列表）使用 query string 传递。
  - `pageNum` / `pageSize`: 部分 POST 接口（如切片列表）使用 camelCase 命名（文档 16）。
  - `pipelineName` / `agent_name`: 支持模糊匹配（文档 5）或精确匹配（文档 44）。

## 使用方式

1. **环境准备**：在百炼控制台获取 API Key，并确认业务空间 ID（`workspace_id`）。
2. **知识库构建**：
   - （可选）通过数据导入接口（如 `addCategory`, `applyFileUploadLease`, `addFile`）准备文件。
   - 调用 `create_v2` 创建知识库并导入，或先 `create_v2` 再通过 `submit-sync-job` 追加导入。
3. **Agent 配置**：
   - 调用 `app/create` 创建 Agent，设置 `agent_scene` 和初始 `agent_config`。
   - 通过 `app/update` 修改草稿配置，再调用 `app/deploy` 发布为正式版本，获取 `agent_id`。
4. **运行时调用**：
   - **知识检索**：`POST /api/v1/indices/knowledge/search`，传入 `agent_id` 和 `query`（或 `images`），`kb_search_configs` 可为各知识库指定过滤条件。
   - **知识问答**：`POST /api/v2/apps/knowledge/chat`，传入 `agent_id` 和 `messages` 历史，`stream` 必须为 `true`，响应为 SSE 流。
5. **调试与排障**：
   - 所有响应均含 `request_id`，联系支持时务必提供。
   - 错误响应结构统一，`error.code` 指示具体问题（如 `INVALID_PARAMETER`, `KB_NOT_FOUND`），详见 [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)。

## 限制和注意事项

- **限流规则**：
  - 知识库管理接口（如 `retrieve`, `list`）按 QPS 限流（最高 2000 QPS），数据导入与 Agent 管理接口按每 10 秒请求数限流（默认 10 次）。超限返回 HTTP `429`，建议实现指数退避重试 [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)。
- **参数命名不一致**：
  - 文档管理接口（如 `delete_file`）使用 snake_case（`index_id`, `doc_ids`），而切片管理（如 `chunklist`）和 Agent 管理（如 `app/list`）使用 camelCase（`indexId`, `agent_id`）。务必依据具体接口文档传参，否则返回 `InvalidParameter`（见文档 12、16、44）。
- **不可逆操作警告**：
  - 删除知识库（文档 8）、删除文档（文档 12）、删除切片（文档 18）、删除类目（文档 24）均为永久性操作，无回收站，调用前必须二次确认。
- **文件与租约约束**：
  - `applyFileUploadLease` 要求 `sizeBytes` 为字符串（如 `"1048576"`），传数字将失败（文档 29）。
  - `addFile` 接口参数名为 `category`（非 `categoryId`），与 `listFile` 等接口不一致（文档 30）。
- **Agent 版本管理**：
  - `agent_config` 仅可在 `beta` 草稿版本修改；已发布版本（如 `1`, `2`）只能通过 `update` 修改 `agent_version_desc`，无法更新配置。要更新配置，必须先 `update` 草稿，再 `deploy` 发布新版本（见文档 41、43）。

## 来源文档

- [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
- [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)
- [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)
- [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)
- [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md)
- [查询文档列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md)
- [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)
- [查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)
- [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)
- [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)
- [查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)
- [更新切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)
- [删除切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-delete-chunk.md)
- [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)
- [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)
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
- [查询数据集](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)
- [查询任务状态](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)


