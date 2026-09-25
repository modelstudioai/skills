# rag api

RAG API 是百炼平台提供的知识库管理与检索服务接口，支持知识库全生命周期管理、文档导入、切片操作、跨库语义检索及基于知识的智能问答。所有接口通过统一的业务空间 Endpoint 提供 HTTPS 服务，采用 API Key 鉴权，返回标准 JSON 响应。

## 支持的模型/功能

RAG API 提供两类核心能力：**知识库管理与数据导入**（OpenAPI 风格）和**知识检索与问答**（应用网关风格）。

- **知识库类型**：支持 `document`（文档搜索）、`table`（数据查询）、`image`（图片问答）、`multimedia`（音视频搜索），需与 `structureType`（`unstructured`/`structured`）匹配。例如 `document` 类型必须搭配 `unstructured`，而 `table` 必须搭配 `structured` [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。
- **嵌入与重排模型**：可指定 `embeddingModelName`（如 `text-embedding-v4`）和 `rerankModelName`（如 `qwen3-rerank`），部分场景（如 `image_qa`）要求 `multimodalEmbeddingModelName`（如 `qwen3-vl-embedding`）[创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。
- **Agent 能力封装**：通过 Agent 管理 API（`/api/v1/indices/rag/app/`）创建、配置并发布 `chat` 或 `search` 场景的运行实体，其 `agent_config` 定义模型、策略、路由与混排逻辑 [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)。
- **运行时服务**：知识检索（`POST /api/v1/indices/knowledge/search`）和知识问答（`POST /api/v2/apps/knowledge/chat`）均依赖已发布的 Agent 实例，调用时仅需传入 `agent_id` 和意图（`query`/`images`/`messages`）[知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)。

> **注意**：文档中 `knowledgeScene` 的取值（如 `visual_document_qa`）在控制台已下线，但 API 仍支持；实际使用应优先选用 `basic_document_qa`、`lite_document_qa` 或 `visual_perception_qa`。

## 关键参数

- **认证与地址**：所有请求需携带 `Authorization: Bearer <API-Key>` 头，并使用形如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com` 的 Base URL，其中 `{workspace_id}` 在控制台业务空间管理页获取 [API 概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)。
- **知识库标识**：多数接口使用 `indexId`（camelCase），但删除知识库接口使用 `index_id`（snake_case）；创建知识库返回 `pipelineId`，该 ID 在切片操作（如 `/chunk/create`）中作为 `pipelineId` 使用 [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)、[新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)。
- **文件与类目参数**：数据导入接口参数命名不一致——`applyFileUploadLease` 和 `addFile` 使用 `category` 字段名，而 `listFile` 和 `addFilesFromAuthorizedOss` 使用 `categoryId` [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)、[注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)。
- **时间戳格式**：监控接口（如 `/index/monitor`）要求 `startTimestamp`/`endTimestamp` 为**秒级** Unix 时间戳（字符串或整数均可），而知识库元数据中的 `created_at`/`updated_at` 为毫秒级 [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)。

## 使用方式

1. **初始化**：在控制台获取 API Key 并确认业务空间 ID，设置环境变量（如 `BAILIAN_API_KEY`）避免硬编码 [认证方式](../../raw/application-api-reference/rag-api/rag-api-authentication.md)。
2. **构建知识库**：
   - （可选）通过数据导入 API 创建类目、上传文件并注册 [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)；
   - 调用 `/api/v1/indices/rag/index/create_v2` 一步创建知识库并导入文件，或先创建后调用 `/api/v1/indices/rag/index/job/create` 追加导入 [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)。
3. **管理内容**：使用 `/chunk/create`、`/chunk/update`、`/chunk/delete` 精细控制切片；通过 `/index/files` 和 `/list/index/file/details` 查询文档状态 [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)。
4. **发布服务**：
   - 创建 Agent（`/app/create`），配置 `agent_scene` 为 `chat` 或 `search`；
   - 更新草稿配置（`/app/update`），然后发布（`/app/deploy`）生成 `agent_id` [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)。
5. **运行时调用**：
   - 检索：`POST /api/v1/indices/knowledge/search`，传 `agent_id` 和 `query`；
   - 问答：`POST /api/v2/apps/knowledge/chat`，传 `agent_id` 和 `messages`，且 `stream` 必须为 `true` [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)。

## 限制和注意事项

- **限流**：知识库管理接口有严格 QPS 限制，例如检索 `/rag/index/retrieve` 为 2000 QPS，而 `/rag/index/monitor` 仅为 1 QPS；知识检索与问答默认用户维度 25 QPS [限流策略](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)。
- **不可逆操作**：删除知识库、文档、切片、类目或文件均为永久性操作，无回收站机制，调用前须二次确认 [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)、[删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)。
- **参数兼容性**：`create_v2` 接口的 `docIds` 参数名易与错误信息中的 `file_ids` 混淆；`delete_file` 接口明确要求 `index_id`（snake_case），传 `indexId` 会报错 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)、[删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)。
- **错误处理**：失败响应含 `request_id`，务必提供此 ID 以便技术支持定位；429 错误需按 `Retry-After` 头或指数退避重试，5xx 错误建议最多重试 3 次 [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)。

## 来源文档

- [API 概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [认证方式](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [限流策略](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
- [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)
- [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)
- [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)
- [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md)
- [查询文档列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md)
- [查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)
- [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)
- [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)
- [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)
- [查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)
- [更新切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)
- [删除切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-delete-chunk.md)
- [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)
- [查询任务状态](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)
- [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)
- [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)
- [新增类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)
- [删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)
- [查询文件列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)
- [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)
- [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
- [新增连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
- [查询连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)


