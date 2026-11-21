# rag api

RAG API 是百炼平台提供的知识库管理与检索服务接口，支持知识库全生命周期管理、文档导入、切片操作、跨库语义检索及基于知识库的智能问答。所有接口均通过 HTTPS 提供，采用统一的鉴权机制和 JSON 数据格式，面向开发者提供细粒度控制能力。

## 支持的模型/功能

RAG API 支持多类型知识库与多模态能力：
- **知识库类型**：`document`（文档搜索）、`table`（数据查询）、`image`（图片问答）、`multimedia`（音视频搜索），由 `knowledgeType` 和 `structureType` 共同决定 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)；
- **嵌入模型**：支持 `text-embedding-v3`、`text-embedding-v4`、`qwen3.7-text-embedding` 等文本嵌入模型；多模态场景需指定 `qwen3-vl-embedding` 等专用模型 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)；
- **重排序模型**：默认使用 `qwen3-rerank`，可在创建或更新知识库时通过 `rerankModelName` 自定义 [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)；
- **检索与问答服务**：通过 Agent 封装策略，支持 `search`（联合语义检索）和 `chat`（流式问答）两类运行时能力，其配置（如混排、路由、防泄漏）均在 Agent 管理 API 中定义 [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)。

> **注意**：文档 5 中 `knowledgeScene` 列出的 `visual_document_qa` 场景已在控制台下线，仅保留 `lite_document_qa`、`visual_perception_qa`、`image_qa` 等有效值；若使用已废弃场景将导致 `invalid multi embedding model` 错误。

## 关键参数

RAG API 参数命名存在不一致，需特别注意：
- **知识库 ID 字段名**：在 `/index/update` 接口为 `id`，在 `/index/delete` 为 `index_id`，在 `/index_job/status` 查询参数中亦为 `index_id`，三者不可混用 [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)、[删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)；
- **文件/类目 ID 字段名**：数据导入接口（如 `/addFile`、`/listCategory`）统一使用 `categoryId` 和 `fileId`，但 `/applyFileUploadLease` 和 `/addFile` 的类目参数名为 `category`（非 `categoryId`），易引发 `Required parameter missing or invalid` 错误 [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)、[注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)；
- **分页参数风格**：知识库管理接口（如 `/index/list`）使用 `page_number`/`page_size`（snake_case），而文档详情接口 `/list/index/file/details` 使用 `pageNumber`/`pageSize`（camelCase） [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)、[查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)。

## 使用方式

1. **认证**：所有请求必须携带 `Authorization: Bearer <API-Key>` Header，API Key 在[控制台 API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)获取，业务空间 ID 用于构造 Base URL：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com` [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)；
2. **接口分组**：
   - 知识库管理：路径前缀 `/api/v1/indices/rag/`（如 `/index/create_v2`、`/index/retrieve`）；
   - 数据导入：路径前缀 `/api/v1/connector/dash/`（如 `/addCategory`、`/addFile`）；
   - 知识检索与问答：路径前缀 `/api/v1/indices/knowledge/search`（POST）和 `/api/v2/apps/knowledge/chat`（SSE 流式） [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)；
3. **典型流程**：
   - 创建类目 → 上传文件 → 注册文件 → 创建知识库 → 提交导入任务 → 发布 Agent → 调用 `knowledge/search` 或 `knowledge/chat`；
   - 所有运行时 API（检索/问答）均依赖已发布的 Agent 实例，其 `agent_id` 由 Agent 管理 API（`/app/create` + `/app/deploy`）产出 [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)。

## 限制和注意事项

- **限流规则**：知识库管理接口按 QPS 限流（如 `/rag/index/retrieve` 为 2000 QPS），知识检索与问答接口按每 10 秒请求数限流（默认 10 次）；超限返回 HTTP `429` 及错误码 `RATE_LIMITED` 或 `THROTTLING.pipelineQPSLimit` [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)、[知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)；
- **不可逆操作**：删除知识库、文档、切片、类目、文件均为软/硬删除且不可恢复，调用前须确认无业务依赖 [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)、[删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)；
- **时间戳格式**：监控接口 `/index/monitor` 要求 `startTimestamp`/`endTimestamp` 为**秒级** Unix 时间戳（字符串或整数均可），与其他接口常用的毫秒级时间戳不同 [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)；
- **Agent 配置约束**：`agent_config` 仅允许修改 `beta` 草稿版本；已发布版本（如 `1`、`2`）只能更新 `agent_version_desc`，如需变更策略，必须先 `update` 草稿再 `deploy` 新版本 [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)。

## 来源文档

- [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [RAG API 错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
- [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)
- [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)
- [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)
- [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)
- [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md)
- [查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)
- [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)
- [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)
- [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)
- [查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)
- [更新切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)
- [删除切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-delete-chunk.md)
- [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)
- [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)
- [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)
- [新增类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)
- [查询文档列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md)
- [查询文件列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)
- [删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
- [新增数据集](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [查询数据集](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [查询任务状态](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)


