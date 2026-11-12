# rag api

RAG API 是百炼平台提供的知识库管理与检索服务接口，支持开发者以编程方式完成知识库的创建、文档导入、切片管理、联合检索及智能问答。所有接口通过统一的业务空间 Endpoint 提供 HTTPS 服务，并采用 API Key 鉴权。

## 支持的模型/功能

RAG API 支持多模态与文本混合检索能力，底层依赖向量嵌入模型（如 `text-embedding-v4`、`qwen3-vl-embedding`）和重排序模型（如 `qwen3-rerank`）。知识库类型覆盖 `document`（文档搜索）、`table`（数据查询）、`image`（图片问答）、`multimedia`（音视频搜索），对应不同结构类型（`unstructured`/`structured`）与使用场景（如 `lite_document_qa`、`visual_perception_qa`、`basic_table_qa`）。检索与问答能力封装在 RAG Agent 中，需先通过 [Agent 管理](raw/application-api-reference/rag-api/rag-api-agents.md) 创建并发布，再调用运行时接口。

知识库管理功能包括：创建（[创建知识库并导入](raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)）、查询列表（[查询知识库列表](raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)）、更新（[更新知识库](raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)）、删除（[删除知识库](raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)）及监控（[获取知识库监控数据](raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)）。文档与切片支持全生命周期操作，包括导入、查询、更新与删除；数据源管理涵盖类目、文件、OSS 批量导入及数据集配置。

> **注意**：文档 46 明确指出“新增切片”接口不支持 `multimedia` 类型知识库，但文档 4 中 `knowledgeType` 字段说明中将 `multimedia` 列为合法取值且与 `unstructured` 搭配。该矛盾表明 `multimedia` 类型知识库的切片级直接操作未被当前 API 支持，应优先使用标准导入流程。

## 关键参数

- **认证参数**：所有请求必须携带 `Authorization: Bearer <API-Key>` 头，API Key 在 [控制台 API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 获取。
- **业务空间标识**：Endpoint 格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`，其中 `{workspace_id}` 为业务空间 ID，可在 [业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 查看。
- **知识库标识**：多数接口使用 `indexId` 或 `pipelineId`（二者等价，均为创建知识库返回的 `data.id`）；但部分接口使用 `index_id`（snake_case），例如 [删除知识库](raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md) 和 [删除文档](raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)，需严格区分命名风格。
- **Agent 标识**：知识检索（`/api/v1/indices/knowledge/search`）与知识问答（`/api/v2/apps/knowledge/chat`）均需传入已发布的 `agent_id`，该 ID 由 [Agent 管理](raw/application-api-reference/rag-api/rag-api-agents.md) 接口创建并发布后获得。
- **分页与过滤**：通用分页参数为 `page_number`（从 1 开始）与 `page_size`（默认 10，上限 100）；模糊过滤常用 `pipeline_name`（知识库名）或 `fileName`（文件名）；精确匹配使用 `index_id`、`fileId`、`agent_id` 等 ID 字段。

## 使用方式

1. **准备凭证**：获取 API Key 并设置环境变量（如 `BAILIAN_API_KEY`），避免硬编码。
2. **管理知识库**：调用 `/api/v1/indices/rag/index/create_v2` 创建知识库；通过 `/api/v1/indices/rag/index/list` 查询列表；使用 `/api/v1/indices/rag/index/update` 修改配置。
3. **导入数据**：
   - 文件上传三步法：先调用 `/api/v1/connector/dash/applyFileUploadLease` 获取 OSS 租约，再 PUT 上传至预签名 URL，最后用 `/api/v1/connector/dash/addFile` 注册；
   - 或直接批量导入：调用 `/api/v1/connector/dash/addFilesFromAuthorizedOss` 从授权 OSS Bucket 导入。
4. **构建 Agent**：使用 `/api/v1/indices/rag/app/create` 创建 Agent，通过 `/api/v1/indices/rag/app/update` 编辑草稿配置，最后用 `/api/v1/indices/rag/app/deploy` 发布。
5. **运行时调用**：
   - 检索：`POST /api/v1/indices/knowledge/search`，传 `agent_id` 与 `query`/`images`；
   - 问答：`POST /api/v2/apps/knowledge/chat`，传 `agent_id` 与 `messages` 历史，`stream` 必须为 `true`。

## 限制和注意事项

- **限流策略**：知识库管理接口按 QPS 限流（如 `/rag/index/list` 上限 10 QPS），检索与问答接口按每 10 秒请求数限流（默认 10 次/10 秒）。超限返回 HTTP `429`，需按 `Retry-After` 头或指数退避重试（1s/2s/4s）。
- **不可逆操作**：删除知识库（[删除知识库](raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)）、删除文档（[删除文档](raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)）、删除类目（[删除类目](raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)）均为软删除或永久移除，无恢复机制。
- **参数兼容性**：文档管理接口存在命名不一致问题——[查询文档列表](raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md) 使用 `index_id`（snake_case），而 [查询文件详情列表](raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md) 使用 `indexId`（camelCase），调用时需严格匹配接口文档要求。
- **安全建议**：API Key 具有账号级权限，禁止提交至代码仓库；建议按应用拆分 Key 并定期轮转；生产环境使用 RAM 子账号并授予最小必要权限（如 `AliyunBailianDataFullAccess`）。

## 来源文档

- [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
- [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)
- [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)
- [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)
- [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)
- [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md)
- [查询文档列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md)
- [查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)
- [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)
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
- [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
- [新增数据集](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [查询数据集](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
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
- [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)


