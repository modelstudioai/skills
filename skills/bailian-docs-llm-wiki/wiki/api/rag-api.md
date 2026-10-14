# rag api

RAG API 是百炼平台提供的面向开发者的一套 RESTful 接口，用于程序化管理知识库、数据源、切片及调用知识检索与问答服务。所有接口通过统一的业务空间 Endpoint 访问，采用 API Key 鉴权，返回结构化 JSON 响应。核心能力覆盖从数据接入（文件上传、类目管理）、知识构建（索引创建、切片控制）到运行时服务（检索、问答）的完整 RAG 工作流。

## 支持的模型/功能

RAG API 本身不直接暴露大语言模型调用，而是通过 **Agent 封装**集成模型能力，并支持多种向量与重排模型配置：

- **嵌入模型（Embedding）**：可在创建知识库时指定 `embeddingModelName`（如 `text-embedding-v4`）或 `multimodalEmbeddingModelName`（如 `qwen3-vl-embedding`），用于非结构化/多模态内容向量化 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。
- **重排序模型（Rerank）**：知识库级配置 `rerankModelName`（如 `qwen3-rerank`），影响检索结果精排质量；知识检索服务（Agent）中还可全局配置 `hybrid_rerank` [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)。
- **问答/检索模型**：Agent 级别通过 `agent_model` 字段指定（如 `qwen3.7-plus`），决定最终生成阶段的 LLM [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)。

功能上分为三大模块：
- **知识库管理**：CRUD 操作、监控、文档/切片全生命周期管理；
- **数据导入**：类目、连接器、文件的增删查、OSS 批量导入、标签管理；
- **知识服务**：基于已发布 Agent 的 `knowledge/search`（语义检索）与 `knowledge/chat`（SSE 流式问答）。

> **注意**：文档 34（知识检索与问答）指出知识检索与问答接口属于 DashScope 应用网关体系，其 Base URL 和鉴权方式与 OpenAPI（如 `CreateIndex`）一致，但路径前缀和语义不同；而文档 1（概览）将 `/api/v2/apps/knowledge/` 明确列为知识问答组接口。二者描述一致，无矛盾。

## 关键参数

- **认证参数**：所有请求必须携带 `Authorization: Bearer <API-Key>` 头，API Key 在[控制台 API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)获取 [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)。
- **业务空间标识**：Endpoint 中的 `{workspace_id}`（如 `llm-xxxxxxxxxxxx`）是必需路径组成部分，需在[业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)页面确认 [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)。
- **ID 类型参数**：
  - 知识库 ID：`index_id`（文档管理接口）、`id`（更新知识库）、`pipelineId`（切片管理）——命名不统一，需严格按各接口文档要求传参 [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)、[新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)。
  - 文件/切片 ID：`doc_ids`（删除文档）、`chunkIds`（删除切片）、`fileId`（查询文件详情）——注意复数/单数及下划线命名差异 [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)。
- **Agent 相关参数**：运行时接口（`knowledge/search` / `knowledge/chat`）必须传 `agent_id`，该 ID 由 Agent 管理 API 创建并发布后生成，不可自行构造 [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)。

## 使用方式

1. **准备凭证**：获取 `BAILIAN_API_KEY` 和 `workspace_id`，构造 Base URL：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com`。
2. **构建知识库**：
   - （可选）先通过数据导入接口（如 `addCategory`, `applyFileUploadLease`, `addFile`）准备文件；
   - 调用 `POST /api/v1/indices/rag/index/create_v2` 一步创建知识库并导入文件，获取 `pipelineId`。
3. **管理内容**：
   - 文档：用 `GET /api/v1/indices/rag/index/files` 查询，`POST /api/v1/indices/rag/index/delete_file` 删除；
   - 切片：用 `POST /api/v1/indices/rag/index/chunklist` 查询，`POST /api/v1/indices/rag/index/chunk/update` 更新。
4. **发布服务**：
   - 调用 Agent 管理 API（`POST /api/v1/indices/rag/app/create` → `POST /api/v1/indices/rag/app/deploy`）创建并发布 `chat` 或 `search` 场景的 Agent，获得 `agent_id`。
5. **调用服务**：
   - 知识检索：`POST /api/v1/indices/knowledge/search`，传 `agent_id` 和 `query`；
   - 知识问答：`POST /api/v2/apps/knowledge/chat`，传 `agent_id` 和 `messages`，`stream` 必须为 `true` [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)。

## 限制和注意事项

- **限流规则**：知识库管理接口 QPS 严格受限（如 `retrieve` 为 2000，`list` 为 10），数据导入接口普遍为 10 QPS；知识服务（`knowledge/search` / `knowledge/chat`）默认用户维度 25 QPS [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)。超限返回 `429`，需按 `Retry-After` 头或指数退避重试 [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)。
- **不可逆操作**：`DELETE` 类接口（删除知识库、文档、切片、类目、文件）均为软/硬删除且**不可恢复**，调用前务必确认 [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)、[删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)。
- **参数命名陷阱**：
  - 更新知识库使用 `id`，而非 `index_id` 或 `indexId`；
  - 删除文档使用 `index_id` 和 `doc_ids`（snake_case），而查询文档列表使用 `index_id`（GET query param），查询切片列表使用 `indexId`（camelCase）；
  - 文件注册（`addFile`）和申请租约（`applyFileUploadLease`）均使用 `category` 参数名，而非 `categoryId` [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)。
- **时间戳格式**：`/api/v1/indices/rag/index/monitor` 接口要求 `startTimestamp`/`endTimestamp` 为**秒级 Unix 时间戳**（字符串或整数），非毫秒 [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)。
- **Agent 配置约束**：`agent_config` 仅允许修改 `beta` 草稿版本；已发布版本只能修改 `agent_version_desc`，如需更新配置，必须走“update beta → deploy”流程 [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)。

## 来源文档

- [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
- [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)
- [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)
- [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md)
- [查询文档列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md)
- [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)
- [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)
- [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)
- [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)
- [查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)
- [查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)
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
- [更新切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
- [新增连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [查询连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)


