# rag api

RAG API 是百炼平台提供的知识库管理与检索服务接口，支持知识库全生命周期管理、文档导入、切片操作、跨库语义检索及智能问答。所有接口通过 DashScope 网关统一接入，采用 RESTful 设计，以业务空间（`workspace_id`）为租户隔离单元，需配合 API Key 进行 Bearer 鉴权。

## 支持的模型/功能

RAG API 提供三类核心能力：**知识库管理**（创建、更新、删除、监控）、**数据导入与文档管理**（类目/文件/连接器操作）、**知识检索与问答**（运行时服务）。  
- **知识库类型**支持 `document`（文档搜索）、`table`（数据查询）、`image`（图片问答）、`multimedia`（音视频搜索），对应不同 `knowledgeType` 与 `structureType` 组合，详见 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。  
- **检索与问答服务**依赖 Agent 实体，需先通过 Agent 管理 API 创建并发布，再调用 `/api/v1/indices/knowledge/search` 或 `/api/v2/apps/knowledge/chat` 接口；Agent 的策略、模型、混排配置均在 `agent_config` 中定义，[Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)详细说明了其生命周期与配置逻辑。  
- **向量模型**由 `embeddingModelName`（如 `text-embedding-v4`）和 `multimodalEmbeddingModelName`（如 `qwen3-vl-embedding`）指定，后者在 `knowledgeScene` 为 `image_qa` 或 `visual_perception_qa` 时必填。

> **注意**：文档 4 中 `knowledgeScene` 列出的 `visual_document_qa` 场景虽在 API 中支持，但控制台已移除该入口，实际使用应优先选择 `basic_document_qa` 或 `lite_document_qa`；文档 35 和 36 明确要求知识检索与问答服务必须在控制台**发布后**才能调用，未发布将返回 `Agent 未发布` 错误，此约束未在部分管理类文档中强调。

## 关键参数

- **认证与路由**：所有请求需携带 `Authorization: Bearer <API-Key>` 头，并使用形如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com` 的 Base URL，其中 `{workspace_id}` 在控制台[业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)获取。  
- **知识库标识**：参数名不统一——创建/更新接口用 `id`（见 [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)），删除/文档操作用 `index_id`（见 [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)），而切片/任务查询用 `indexId`（见 [查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)）。  
- **文件与切片关联**：`docIds` 字段用于创建知识库时批量导入（见 [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)），但 `delete_file` 接口要求 `doc_ids`（snake_case），且错误信息中提示的 `IndexId` 并非真实参数名，需严格按文档约定传参。  
- **时间戳格式**：监控接口 `/api/v1/indices/rag/index/monitor` 要求 `startTimestamp`/`endTimestamp` 为**秒级** Unix 时间戳（字符串或整数均可），与其他接口常用的毫秒级时间戳不同。

## 使用方式

1. **初始化**：获取 API Key（[认证方式](../../raw/application-api-reference/rag-api/rag-api-authentication.md)）和 `workspace_id`，构造 Base URL。  
2. **构建知识库**：  
   - 先通过数据导入 API（如 `addCategory`、`applyFileUploadLease`、`addFile`）准备文件；  
   - 再调用 `/api/v1/indices/rag/index/create_v2` 一键创建知识库并导入，或分步调用 `createIndex` + `submitSyncJob`。  
3. **运行时调用**：  
   - 检索：POST `/api/v1/indices/knowledge/search`，传入 `agent_id` 和 `query`；  
   - 问答：POST `/api/v2/apps/knowledge/chat`，`stream` 必须为 `true`，`input.messages` 需包含完整多轮历史。  
4. **Agent 管理**：使用 `/api/v1/indices/rag/app/` 系列接口（如 `create`、`update`、`deploy`）完成 Agent 生命周期操作，发布后获取 `agent_id` 供运行时调用。

## 限制和注意事项

- **限流**：知识库管理接口 QPS 差异大，如 `retrieve` 达 2000，而 `get-index-monitor` 仅 1；运行时接口（`knowledge/search`/`chat`）默认用户维度 25 QPS。超限返回 `429`，需按 `Retry-After` 头或指数退避重试（见 [限流策略](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md) 和 [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)）。  
- **不可逆操作**：删除知识库、文档、切片、类目、文件均为**永久删除**，无回收站机制，调用前务必确认。  
- **参数兼容性**：数据导入接口（路径前缀 `/api/v1/connector/dash/`）与知识库管理接口（`/api/v1/indices/rag/`）共用同一 Base URL 和鉴权，但参数命名风格混杂（如 `category` vs `categoryId`），需严格对照各接口文档。  
- **错误处理**：响应结构统一，失败时 `code` 字段含业务错误码（如 `KB_NOT_FOUND`），排查问题必须提供 `request_id`。

## 来源文档

- [API 概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [认证方式](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [限流策略](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
- [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)
- [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)
- [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)
- [查询文档列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md)
- [查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)
- [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)
- [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)
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
- [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
- [新增连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [查询连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)


