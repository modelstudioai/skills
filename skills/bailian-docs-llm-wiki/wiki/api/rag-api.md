# rag api

RAG API 是百炼平台提供的面向开发者的一套知识库管理与检索服务接口，覆盖知识库生命周期管理、文档/切片操作、数据导入、Agent 配置及运行时检索与问答能力。所有接口均通过 DashScope 网关统一接入，采用标准 RESTful 设计与 Bearer Token 鉴权。

## 支持的模型/功能

RAG API 支持多模态与文本混合检索、结构化/非结构化知识库、多场景知识问答（基础问答、视觉理解、极速问答等），并提供完整的 Agent 全生命周期管理能力。核心功能分组如下：

- **知识库管理**：创建、查询、更新、删除知识库（`/api/v1/indices/rag/index/*`），支持 `unstructured`（文档/图片/音视频）与 `structured`（表格）两类结构类型；`knowledgeType` 与 `knowledgeScene` 组合决定具体能力，例如 `document` + `lite_document_qa` 启用极速问答，`image` + `image_qa` 启用图片问答 [API 概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)。
- **数据导入**：类目与文件管理（`/api/v1/connector/dash/*`），支持本地上传（三步流程：申请租约 → OSS PUT → 注册文件）、OSS 批量导入、连接器配置等 [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)。
- **切片管理**：细粒度控制知识单元，支持新增、查询、更新、删除切片（`/api/v1/indices/rag/index/chunk*`），适用于需人工干预或动态注入内容的场景 [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)。
- **Agent 管理**：创建、更新、发布、删除 RAG Agent（`/api/v1/indices/rag/app/*`），`agent_config` 封装全部检索策略（如混排模型、知识路由、过滤规则），是知识检索与问答服务的运行主体 [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)。
- **运行时服务**：`/api/v1/indices/knowledge/search`（联合语义检索）与 `/api/v2/apps/knowledge/chat`（SSE 流式问答），均需已发布的 `agent_id`，策略完全由 Agent 配置驱动，调用方仅传意图与过滤条件。

> **注意**：文档 5 中 `knowledgeScene` 列出的 `visual_document_qa` 场景在控制台已下线，虽 API 仍接受该值，但实际行为未定义，建议使用 `basic_document_qa` 或 `visual_perception_qa`。

## 关键参数

- **认证参数**：所有请求必须携带 `Authorization: Bearer <API-Key>` 头，API Key 在控制台 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 获取；业务空间通过 Endpoint 中的 `{workspace_id}` 标识，格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com` [认证方式](../../raw/application-api-reference/rag-api/rag-api-authentication.md)。
- **知识库标识**：知识库 ID 字段名不统一：`createIndex` 返回 `pipelineId`，`updateIndex` 请求体用 `id`，`deleteIndex` 用 `index_id`，`listDocuments` 查询参数用 `index_id`，`listChunks` 请求体用 `indexId` —— 开发者需严格按各接口文档要求传参，不可混用 [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)、[删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)。
- **切片与文件 ID**：切片 ID 通常取自 `listChunks` 响应中 `node.metadata._id`；文件 ID 来自 `addFile` 返回的 `fileId` 或 `listFile` 的 `fileId` 字段；二者不可互换。
- **时间戳格式**：监控接口（如 `/index/monitor`）要求秒级 Unix 时间戳（字符串或整数），而其他接口（如文档元数据中的 `gmt_modified`）返回毫秒级时间戳，务必区分 [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)。

## 使用方式

1. **准备凭证**：获取 API Key 与业务空间 ID，构造 Base URL `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`。
2. **构建知识库**：
   - （可选）通过 `/api/v1/connector/dash/addCategory` 创建类目；
   - 上传文件：调用 `/api/v1/connector/dash/applyFileUploadLease` 获取租约 → PUT 到 OSS → 调用 `/api/v1/connector/dash/addFile` 注册；
   - 创建知识库：调用 `/api/v1/indices/rag/index/create_v2`，传入 `docIds` 及 `structureType`/`knowledgeType`/`knowledgeScene` 等配置。
3. **配置与发布 Agent**：
   - 调用 `/api/v1/indices/rag/app/create` 创建 Agent；
   - 通过 `/api/v1/indices/rag/app/update` 编辑 `beta` 草稿的 `agent_config`；
   - 调用 `/api/v1/indices/rag/app/deploy` 发布，获取 `agent_id`。
4. **运行时调用**：
   - 检索：`POST /api/v1/indices/knowledge/search`，传 `agent_id` 和 `query`/`images`；
   - 问答：`POST /api/v2/apps/knowledge/chat`，`stream=true`，传 `agent_id` 与 `messages` 历史。

所有接口遵循统一响应格式：成功时 `code: "Success"`，失败时 `error.code` 包含业务错误码（如 `KB_NOT_FOUND`），排查问题必提供 `request_id`。

## 限制和注意事项

- **限流策略**：接口 QPS 差异显著，检索（`/rag/index/retrieve`）上限 2000 QPS，而监控（`/rag/index/monitor`）仅 1 QPS；知识问答与检索运行时接口默认用户维度 25 QPS [限流策略](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)。超限返回 `429`，需按 `Retry-After` 头或指数退避重试。
- **参数命名不一致**：`listFile` 请求体用 `maxResult`（单数），传 `maxResults` 会被静默忽略；`listCategory` 同样如此；`listFileDetails` 请求体用 camelCase（`pageNumber`），而多数知识库接口用 snake_case（`page_number`）—— 必须严格匹配文档 [查询文件列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)、[查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)。
- **不可逆操作警告**：删除知识库（`/rag/index/delete`）、删除类目（`/dash/deleteCategory`）、删除文件（`/dash/deleteFile`）均为永久删除，无回收站机制，调用前必须确认依赖关系 [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)。
- **Agent 版本约束**：`agent_config` 仅允许修改 `beta` 草稿版本；已发布版本（如 `1`, `2`）只能通过 `update` 接口修改 `agent_version_desc`，若需更新配置，必须先 `update` 草稿再 `deploy` 新版本 [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)。
- **文件大小与内容限制**：切片 `content` 长度必须在 10–6000 字符之间；上传文件 `sizeBytes` 必须以字符串格式传入（如 `"1048576"`），传数字将失败；`kb_search_configs` 总字节数不能超过 80,000 [更新切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)、[申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)、[知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)。

## 来源文档

- [API 概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [认证方式](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [限流策略](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
- [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)
- [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)
- [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md)
- [查询文档列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md)
- [查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)
- [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)
- [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)
- [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)
- [查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)
- [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)
- [删除切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-delete-chunk.md)
- [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)
- [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)
- [查询任务状态](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)
- [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)
- [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)
- [新增类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)
- [删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)
- [查询文件列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
- [更新切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
- [新增连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [查询连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)


