# rag api

RAG API 是百炼平台提供的知识库全生命周期管理与检索问答服务接口，支持知识库创建、文档导入、切片管理、监控查询，以及基于知识库的语义检索和流式问答。所有接口均通过 HTTPS 提供，使用统一的业务空间 Endpoint 和 API Key 鉴权。

## 支持的模型/功能

RAG API 不直接暴露大语言模型调用，而是围绕**知识增强能力**提供三类核心功能：

- **知识库管理**：支持 `unstructured`（文档搜索、图片问答、音视频搜索）和 `structured`（数据查询）两类结构类型；对应 `knowledgeType`（如 `document`、`table`、`image`、`multimedia`）及 `knowledgeScene`（如 `basic_document_qa`、`lite_document_qa`、`image_qa`），详见[创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。
- **数据导入**：支持本地上传（三步流程：申请租约 → OSS PUT 上传 → 注册文件）、OSS 批量导入、类目/连接器管理等，路径前缀为 `/api/v1/connector/dash/`，详见[数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)。
- **知识检索与问答**：通过 Agent 封装检索策略，提供两个运行时接口：`POST /api/v1/indices/knowledge/search`（联合多库语义检索）和 `POST /api/v2/apps/knowledge/chat`（SSE 流式问答），二者均需已发布的 `agent_id`，详见[知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)。

> **注意**：`knowledgeScene` 中 `visual_document_qa`（图文并茂回复）虽在 API 文档中提及，但控制台已移除该入口，不建议新业务使用。

## 关键参数

- **认证参数**：所有请求必须携带 `Authorization: Bearer <API-Key>` Header，API Key 在[控制台 API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)获取，详见[认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)。
- **业务空间标识**：Base URL 为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`，`{workspace_id}`（如 `llm-xxxxxxxxxxxx`）需从[业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)页面获取。
- **知识库 ID 参数名不一致**：创建/更新/监控等接口使用 `id` 或 `indexId`，而删除知识库接口明确要求 `index_id`（snake_case），详见[删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)；文档/切片操作中也存在 `index_id`（如删除文档）与 `indexId`（如查询切片列表）混用现象，需严格按各接口文档指定。
- **文件/切片 ID 参数名**：`docIds`（非 `file_ids` 或 `fileIds`）用于创建知识库和提交导入任务；`dataId` 用于新增/更新切片；`doc_id` 用于查询切片列表过滤。

## 使用方式

1. **准备凭证**：获取 API Key 和 `workspace_id`，配置环境变量（如 `BAILIAN_API_KEY`）避免硬编码。
2. **构建知识库**：
   - 先通过数据导入接口（如 `applyFileUploadLease` + `addFile`）将文件注册到数据中心；
   - 再调用 `/api/v1/indices/rag/index/create_v2` 一步创建知识库并导入，或先 `create` 后 `submit_sync_job` 追加。
3. **管理内容**：使用知识库管理接口增删改查知识库、文档、切片；使用数据导入接口管理类目、文件元数据（标签、详情等）。
4. **发布 Agent**：通过 Agent 管理 API（`/api/v1/indices/rag/app/create` → `update` → `deploy`）创建并发布检索/问答服务，获取 `agent_id`。
5. **运行时调用**：使用 `agent_id` 调用 `/api/v1/indices/knowledge/search` 或 `/api/v2/apps/knowledge/chat`，注意问答接口 `stream` 必须为 `true`。

## 限制和注意事项

- **限流规则**：知识库管理接口按 QPS 限流（如 `create_v2` 为 10 QPS），知识检索/问答接口按“每 10 秒最多 10 次”限流；超限返回 `429`，应遵循指数退避重试策略，详见[限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)和[错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)。
- **不可逆操作**：删除知识库、文档、切片、类目、文件均为永久删除且无法恢复，调用前务必确认。
- **参数格式陷阱**：
  - 时间戳：监控接口 `startTimestamp`/`endTimestamp` 为**秒级** Unix 时间戳（非毫秒），支持字符串或整数格式；
  - 文件大小：`applyFileUploadLease` 的 `sizeBytes` 必须传**字符串**（如 `"1048576"`），传数字会失败；
  - 分页参数：`listCategory`/`listFile` 的分页字段为 `maxResult`（单数），传 `maxResults` 会被静默忽略。
- **Agent 配置约束**：`agent_config` 仅允许修改 `beta` 草稿版本；已发布版本只能修改 `agent_version_desc`，如需更新配置，必须先 `update` 草稿再 `deploy` 发布新版本，详见[更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)。

## 来源文档

- [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
- [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)
- [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)
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
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
- [新增连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [查询连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)
- [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)


