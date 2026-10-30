# rag api

RAG API 是百炼平台提供的知识库全生命周期管理与语义检索/问答服务接口集合，覆盖知识库创建、文档导入、切片管理、监控、Agent 封装及运行时调用等核心能力。所有接口通过统一的业务空间 Endpoint 提供 HTTPS 服务，采用 API Key 鉴权，请求与响应均为 UTF-8 编码的 JSON 格式。开发者可通过该 API 实现知识库自动化构建、策略化检索与智能问答集成。

## 支持的模型/功能

RAG API 不直接暴露大模型调用，而是通过预置模型能力支撑上层功能：

- **嵌入模型（Embedding）**：支持 `text-embedding-v4` 等文本向量化模型，可在创建知识库时通过 `embeddingModelName` 指定；多模态场景（如图片问答、视觉理解）需显式配置 `multimodalEmbeddingModelName`（例如 `qwen3-vl-embedding`），详见[创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)。
- **重排序模型（Rerank）**：默认使用 `qwen3-rerank`，可在知识库创建或更新时通过 `rerankModelName` 覆盖；检索服务（`knowledge/search`）中混排策略由 Agent 配置中的 `hybrid_rerank` 控制。
- **Agent 封装能力**：知识检索与问答均以 RAG Agent 为运行主体，其 `agent_config` 可配置 `agent_model`（如 `qwen3.7-plus`）、`agent_policy`（`turbo` 或 `agentic`）及安全策略（防泄漏、拒答、引用标注等），详见[创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md) 和 [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)。

> **注意**：文档中提及的 `visual_document_qa` 场景虽在[创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)中列为可选值，但明确标注“控制台已不再提供该入口”，建议避免在生产环境使用。

## 关键参数

- **认证与路由**：所有请求必须携带 `Authorization: Bearer <API-Key>` 头，并使用形如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com` 的 Base URL，其中 `{workspace_id}` 为业务空间 ID（如 `llm-xxxxxxxxxxxx`），在[业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)页面获取。
- **知识库标识**：知识库 ID 统一称作 `pipelineId`（部分接口误用 `index_id` 或 `id`），是创建知识库（`create_v2`）返回的 `data.pipelineId`，也是后续所有操作的核心路径参数或请求体字段。
- **命名不一致警告**：
  - 知识库管理接口（如 `/update`）使用 `id` 字段传入知识库 ID；
  - 文档管理接口（如 `/delete_file`）使用 `index_id`；
  - 切片与同步任务接口（如 `/chunklist`, `/job/create`）使用 `indexId` 或 `pipelineId`；
  - 数据导入接口（如 `/addFile`, `/applyFileUploadLease`）中类目 ID 参数名为 `category`，而非 `categoryId`（见[注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)和[申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)）。
- **分页与过滤**：查询类接口（如 `/list`, `/files`）普遍支持 `page_number`/`page_size`；部分接口（如 `/listCategory`）使用 `maxResult`（单数）且忽略 `maxResults`（复数）。

## 使用方式

1. **初始化**：获取 API Key（[认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)）与业务空间 ID，构造 Base URL。
2. **构建知识库**：
   - （可选）通过数据导入接口（`/connector/dash/` 前缀）管理类目、上传文件；
   - 调用 `/api/v1/indices/rag/index/create_v2` 创建知识库并导入文档，获取 `pipelineId`。
3. **管理内容**：
   - 文档：通过 `/index/files`（列表）、`/list/index/file/details`（详情）、`/index/delete_file`（删除）管理；
   - 切片：通过 `/index/chunklist`（列表）、`/index/chunk/create`（新增）、`/index/chunk/update`（更新）、`/index/chunk/delete`（删除）精细控制；
   - 同步任务：通过 `/index/job/create`（提交）与 `/index_job/status`（查状态）跟踪导入进度。
4. **封装与发布服务**：
   - 调用 Agent 管理 API（`/app/` 前缀）创建、配置、发布 `search` 或 `chat` 场景的 Agent，获取 `agent_id`；
   - 发布后，即可调用运行时接口 `/api/v1/indices/knowledge/search`（检索）或 `/api/v2/apps/knowledge/chat`（问答）。
5. **监控与运维**：调用 `/index/monitor` 获取知识库存储用量与 QPS 监控数据。

## 限制和注意事项

- **限流规则**：知识库管理接口有严格 QPS 限制，例如检索（`/retrieve`）上限 2000 QPS，而监控接口（`/monitor`）仅 1 QPS；Agent 运行时接口（`/knowledge/search`, `/knowledge/chat`）默认用户维度 25 QPS。超限返回 `429`，需按 `Retry-After` 头或指数退避重试（见[限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)）。
- **不可逆操作**：删除知识库（`/index/delete`）、删除文档（`/index/delete_file`）、删除切片（`/index/chunk/delete`）、删除类目（`/deleteCategory`）均为软删除但逻辑不可逆，操作前务必确认。
- **参数格式陷阱**：
  - 文件大小 `sizeBytes` 在 `applyFileUploadLease` 中必须为字符串（如 `"1048576"`），传数字将失败；
  - `kb_search_configs` 中的 `search_filters` 语法复杂，需参考[知识库 SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)；
  - 错误响应结构统一，但部分接口（如 `/addCategory`）业务失败时 HTTP 状态码仍为 `200`，需检查响应体中的 `status` 字段（见[错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)）。
- **Agent 生命周期约束**：`agent_config` 仅允许修改 `beta` 草稿版本；已发布版本（如 `1`, `2`）只能更新 `agent_version_desc`，如需变更配置，必须先 `update` 草稿再 `deploy` 新版本（见[更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)）。

## 来源文档

- [概览](../../raw/application-api-reference/rag-api/rag-api-overview.md)
- [认证](../../raw/application-api-reference/rag-api/rag-api-authentication.md)
- [错误码](../../raw/application-api-reference/rag-api/rag-api-errors.md)
- [限流](../../raw/application-api-reference/rag-api/rag-api-rate-limits.md)
- [知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base.md)
- [查询知识库列表](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-list-indices.md)
- [创建知识库并导入](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
- [删除知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-delete-index.md)
- [更新知识库](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)
- [文档管理](../../raw/application-api-reference/rag-api/rag-api-documents.md)
- [获取知识库监控数据](../../raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-get-index-monitor.md)
- [查询文档列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-documents.md)
- [查询文件详情列表](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-list-file-details.md)
- [删除文档](../../raw/application-api-reference/rag-api/rag-api-documents/rag-api-delete-document.md)
- [切片管理](../../raw/application-api-reference/rag-api/rag-api-chunks.md)
- [查询切片列表](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md)
- [更新切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-update-chunk.md)
- [删除切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-delete-chunk.md)
- [同步任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs.md)
- [查询任务状态](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-get-sync-job-status.md)
- [数据导入](../../raw/application-api-reference/rag-api/rag-api-data-import.md)
- [查询类目列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-category.md)
- [提交导入任务](../../raw/application-api-reference/rag-api/rag-api-sync-jobs/rag-api-submit-sync-job.md)
- [新增类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-category.md)
- [删除类目](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-category.md)
- [查询文件详情](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-describe-file.md)
- [删除文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-delete-file.md)
- [新增切片](../../raw/application-api-reference/rag-api/rag-api-chunks/rag-api-add-chunk.md)
- [批量更新文件标签](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-batch-update-tag.md)
- [注册文件](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)
- [从 OSS 批量导入](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-oss-import.md)
- [新增连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-connector.md)
- [查询连接器](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-get-connector.md)
- [知识检索与问答](../../raw/application-api-reference/rag-api/knowledge.md)
- [知识检索](../../raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
- [知识问答](../../raw/application-api-reference/rag-api/knowledge/knowledgechat.md)
- [查询文件列表](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-list-file.md)
- [Agent 管理概述](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)
- [创建 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-create.md)
- [更新 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-update.md)
- [申请上传租约](../../raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)
- [发布 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-deploy.md)
- [Agent 管理](../../raw/application-api-reference/rag-api/rag-api-agents.md)
- [删除 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-delete.md)
- [查询 Agent 详情](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-get.md)
- [复制 Agent](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-copy.md)
- [查询 Agent 列表](../../raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)


